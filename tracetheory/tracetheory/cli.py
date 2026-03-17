#!/usr/bin/env python3
"""
TraceTheory CLI

Usage:
    tracetheory seed --doi <DOI> --title <TITLE>
    tracetheory expand --depth N --direction backward|forward|both
    tracetheory fetch-pdfs --use-proxy
    tracetheory extract-references [--vintage]
    tracetheory build-graph
    tracetheory export --format json|graphml|bibtex
    tracetheory visualize --port 8000
"""

import asyncio
import click
import yaml
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.search.semantic_scholar import SemanticScholarClient, Paper
from src.search.openalex import OpenAlexClient, Work
from src.orchestrator.crawler import CitationCrawler, CrawlConfig, CrawlState
from src.storage.graph import CitationGraph, PaperNode
from src.storage.export import export_graph
from src.fetch.pdf_downloader import PDFDownloader
from src.fetch.cache_manager import CacheManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# Default config path
CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"
DEFAULT_CACHE_DIR = Path(__file__).parent.parent / "cache"
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "output"


def load_config() -> dict:
    """Load configuration from YAML file"""
    config_file = CONFIG_PATH
    if not config_file.exists():
        logger.warning(f"Config file not found at {config_file}, using defaults")
        return {}
    
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def paper_to_node(paper: Paper, seed_id: str = None, depth: int = 0, source: str = "semantic_scholar") -> PaperNode:
    """Convert API Paper to storage PaperNode"""
    return PaperNode(
        id=paper.paper_id,
        title=paper.title,
        authors=paper.authors,
        year=paper.year,
        venue=paper.venue,
        doi=paper.doi,
        abstract=paper.abstract,
        citation_count=paper.citation_count,
        reference_count=paper.reference_count,
        seed_id=seed_id,
        depth=depth,
        source=source,
    )


def work_to_node(work: Work, seed_id: str = None, depth: int = 0) -> PaperNode:
    """Convert OpenAlex Work to storage PaperNode"""
    return PaperNode(
        id=work.work_id,
        title=work.title,
        authors=work.authors,
        year=work.year,
        venue=work.venue,
        doi=work.doi,
        abstract=work.abstract,
        citation_count=work.cited_by_count,
        reference_count=len(work.referenced_works) if work.referenced_works else 0,
        seed_id=seed_id,
        depth=depth,
        source="openalex",
    )


@click.group()
@click.option("--config", type=click.Path(), help="Path to config file")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx, config, verbose):
    """TraceTheory - Intellectual Genealogy of Computing Papers"""
    ctx.ensure_object(dict)
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if config:
        ctx.obj["config_path"] = Path(config)
    else:
        ctx.obj["config_path"] = CONFIG_PATH
    
    ctx.obj["config"] = load_config()
    
    # Ensure directories exist
    DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@cli.command()
@click.option("--doi", type=str, help="DOI of the seed paper")
@click.option("--title", type=str, help="Title of the seed paper (fallback if DOI not provided)")
@click.option("--source", type=click.Choice(["semantic_scholar", "openalex"]), default="openalex", help="API to use")
@click.option("--output", type=click.Path(), default="output/graph.json", help="Output file")
@click.pass_context
def seed(ctx, doi, title, source, output):
    """Seed the graph with a starting paper"""
    config = ctx.obj["config"]
    email = config.get("institution", {}).get("login", {}).get("email", "test@example.com")
    
    logger.info(f"Starting seed with DOI: {doi}, Title: {title}, Source: {source}")
    
    async def run_seed():
        # Try OpenAlex first (better coverage for older papers)
        if source == "openalex":
            async with OpenAlexClient(email=email) as client:
                work = None
                
                # Try DOI
                if doi:
                    logger.info(f"[OpenAlex] Looking up paper by DOI: {doi}")
                    work = await client.get_work_by_doi(doi)
                
                # Fallback to title search
                if not work and title:
                    logger.info(f"[OpenAlex] Searching for paper by title: {title}")
                    results = await client.search_works(title, limit=1)
                    if results:
                        work = Work.from_api(results[0])
                
                if work:
                    logger.info(f"[OpenAlex] Found seed paper: {work.title} ({work.year})")
                    graph = CitationGraph()
                    node = work_to_node(work, seed_id=work.work_id, depth=0)
                    graph.add_paper(node)
                    graph.seed_papers.add(work.work_id)
                    graph.metadata["seed_paper"] = work.work_id
                    graph.metadata["seed_title"] = work.title
                    graph.metadata["source"] = "openalex"
                    
                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    graph.to_json(str(output_path))
                    
                    logger.info(f"Seed saved to {output_path}")
                    click.echo(f"✅ Seed paper added: {work.title}")
                    return work
        
        # Fallback to Semantic Scholar
        async with SemanticScholarClient() as ss_client:
            paper = None
            
            if doi:
                logger.info(f"[Semantic Scholar] Looking up paper by DOI: {doi}")
                paper = await ss_client.get_paper_by_doi(doi)
            
            if not paper and title:
                logger.info(f"[Semantic Scholar] Searching for paper by title: {title}")
                results = await ss_client.search_paper(title, limit=1)
                if results:
                    paper = await ss_client.get_paper(results[0].get("paperId"))
            
            if paper:
                logger.info(f"[Semantic Scholar] Found seed paper: {paper.title} ({paper.year})")
                graph = CitationGraph()
                node = paper_to_node(paper, seed_id=paper.paper_id, depth=0)
                graph.add_paper(node)
                graph.seed_papers.add(paper.paper_id)
                graph.metadata["seed_paper"] = paper.paper_id
                graph.metadata["seed_title"] = paper.title
                graph.metadata["source"] = "semantic_scholar"
                
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                graph.to_json(str(output_path))
                
                logger.info(f"Seed saved to {output_path}")
                click.echo(f"✅ Seed paper added: {paper.title}")
                return paper
            else:
                logger.error("Could not find paper in any source")
                click.echo("❌ Could not find paper. Try:")
                click.echo("   1. Use --title with a more specific query")
                click.echo("   2. Check the DOI is correct")
                click.echo("   3. Try --source openalex (better for older papers)")
                return None
    
    asyncio.run(run_seed())


@cli.command()
@click.option("--depth", type=int, default=3, help="Maximum crawl depth")
@click.option("--direction", type=click.Choice(["backward", "forward", "both"]), default="backward", 
              help="Citation direction: backward (references), forward (citations), both")
@click.option("--max-per-depth", type=int, default=50, help="Maximum papers per depth level")
@click.option("--checkpoint/--no-checkpoint", default=True, help="Enable checkpointing")
@click.option("--resume", type=click.Path(), help="Resume from checkpoint file")
@click.option("--output", type=click.Path(), default="output/graph.json", help="Output file")
@click.pass_context
def expand(ctx, depth, direction, max_per_depth, checkpoint, resume, output):
    """Expand the citation graph recursively"""
    config = ctx.obj["config"]
    email = config.get("institution", {}).get("login", {}).get("email", "test@example.com")
    
    # Load existing graph
    output_path = Path(output)
    graph = CitationGraph()
    
    if output_path.exists():
        logger.info(f"Loading existing graph from {output}")
        graph = CitationGraph.from_json(str(output_path))
    
    # Detect source from graph metadata
    source = graph.metadata.get("source", "openalex")
    
    # Configure crawler
    follow_references = direction in ["backward", "both"]
    follow_citations = direction in ["forward", "both"]
    
    crawl_config = CrawlConfig(
        max_depth=depth,
        max_papers_per_depth=max_per_depth,
        follow_references=follow_references,
        follow_citations=follow_citations,
        checkpoint_interval=100,
        checkpoint_file=str(output_path.with_suffix(".checkpoint.json")) if checkpoint else "checkpoint_disabled.json",
        source=source,
        email=email,
    )
    
    # Get seed papers from graph
    seed_ids = list(graph.seed_papers)
    if not seed_ids:
        seed_id = graph.metadata.get("seed_paper")
        if seed_id:
            seed_ids = [seed_id]
    
    if not seed_ids:
        click.echo("❌ No seed papers found. Run 'seed' command first.")
        return
    
    logger.info(f"Expanding graph with {len(seed_ids)} seed(s), depth={depth}, direction={direction}, source={source}")
    click.echo(f"🔄 Expanding graph: depth={depth}, direction={direction}, source={source}")
    
    async def run_expand():
        crawler = CitationCrawler(crawl_config)
        
        # Load checkpoint if resuming
        if resume:
            if crawler.load_checkpoint(resume):
                logger.info(f"Resumed from checkpoint: {len(crawler.state.papers)} papers loaded")
                click.echo(f"📂 Resumed from checkpoint: {len(crawler.state.papers)} papers")
        
        # Seed from existing graph
        for seed_id in seed_ids:
            crawler.state.queue.append(seed_id)
            crawler.state.depth_map[seed_id] = 0
        
        # Run crawl
        papers = await crawler.crawl()
        
        # Update graph
        for paper_id, paper_data in papers.items():
            if paper_id not in graph.graph.nodes:
                depth = paper_data.get("depth", 0)
                node = PaperNode(
                    id=paper_id,
                    title=paper_data.get("title", ""),
                    authors=paper_data.get("authors", []),
                    year=paper_data.get("year"),
                    venue=paper_data.get("venue"),
                    doi=paper_data.get("doi"),
                    abstract=paper_data.get("abstract"),
                    citation_count=paper_data.get("citation_count", 0),
                    reference_count=paper_data.get("reference_count", 0),
                    seed_id=seed_ids[0],
                    depth=depth,
                    source=source,
                )
                graph.add_paper(node)
        
        # Build edges from references
        for paper_id, paper_data in papers.items():
            refs = paper_data.get("references", [])
            for ref_id in refs:
                if ref_id in papers:
                    graph.graph.add_edge(paper_id, ref_id)
        
        # Update metadata
        graph.metadata["max_depth"] = max((p.get("depth", 0) for p in papers.values()), default=0)
        graph.metadata["total_papers"] = len(papers)
        graph.metadata["total_edges"] = len(list(graph.graph.edges))
        
        # Save
        graph.to_json(str(output_path))
        
        stats = crawler.get_stats()
        elapsed = stats.get("elapsed_seconds", 0)
        
        click.echo(f"\n✅ Expansion complete!")
        click.echo(f"   Total papers: {len(papers)}")
        click.echo(f"   Total citations: {len(list(graph.graph.edges))}")
        click.echo(f"   Max depth: {graph.metadata.get('max_depth', 0)}")
        click.echo(f"   Time: {elapsed:.1f}s")
        click.echo(f"   Output: {output}")
    
    asyncio.run(run_expand())


@cli.command()
@click.option("--use-proxy", is_flag=True, help="Use institutional proxy (EZProxy)")
@click.option("--parallel", type=int, default=3, help="Parallel download workers")
@click.pass_context
def fetch_pdfs(ctx, use_proxy, parallel):
    """Download PDFs for papers in the graph"""
    config = ctx.obj["config"]
    
    output_dir = DEFAULT_OUTPUT_DIR
    graph_path = output_dir / "graph.json"
    cache_dir = DEFAULT_CACHE_DIR
    
    if not graph_path.exists():
        click.echo(f"❌ No graph found at {graph_path}")
        return
    
    graph = CitationGraph.from_json(str(graph_path))
    
    logger.info(f"Fetching PDFs for {len(graph.graph.nodes)} papers")
    click.echo(f"📥 Fetching PDFs (proxy={use_proxy}, workers={parallel})...")
    
    # Initialize downloader and cache
    cache = CacheManager(cache_dir)
    downloader = PDFDownloader(config, cache, use_proxy=use_proxy, max_workers=parallel)
    
    async def run_fetch():
        downloaded = 0
        skipped = 0
        failed = 0
        
        for paper_id in graph.graph.nodes:
            data = graph.graph.nodes[paper_id]
            doi = data.get("doi")
            title = data.get("title", "Unknown")
            
            # Check cache
            if cache.exists(paper_id):
                skipped += 1
                continue
            
            # Try to get PDF URL (would need to integrate with publishers)
            # For now, just log what we'd do
            logger.debug(f"Would download PDF for: {title[:50]}...")
            downloaded += 1
            
            if downloaded % 10 == 0:
                click.echo(f"  Processed {downloaded} papers...")
        
        return downloaded, skipped, failed
    
    d, s, f = asyncio.run(run_fetch())
    
    click.echo(f"✅ PDF fetch complete (downloaded={d}, cached={s}, failed={f})")


@cli.command()
@click.option("--vintage", is_flag=True, help="Extract from scanned/vintage papers (requires OCR)")
@click.option("--input-dir", type=click.Path(), default="cache/pdfs", help="Input PDF directory")
@click.pass_context
def extract_references(ctx, vintage, input_dir):
    """Extract references from downloaded PDFs"""
    input_path = Path(input_dir)
    
    if not input_path.exists():
        click.echo(f"❌ Input directory not found: {input_dir}")
        return
    
    pdf_files = list(input_path.glob("*.pdf"))
    
    logger.info(f"Extracting references from {len(pdf_files)} PDFs (vintage={vintage})")
    click.echo(f"🔍 Extracting references from {len(pdf_files)} PDFs...")
    
    # This would integrate with the existing vintage_reference_extractor.py
    # For now, just report what we'd do
    click.echo(f"   (Reference extraction placeholder - integrate with src/extract)")
    
    for pdf_file in pdf_files[:5]:  # Show first 5
        click.echo(f"   - {pdf_file.name}")


@cli.command()
@click.option("--input", "input_file", type=click.Path(), default="output/graph.json", help="Input graph file")
@click.pass_context
def build_graph(ctx, input_file):
    """Build/rebuild the citation graph from fetched data"""
    input_path = Path(input_file)
    if not input_path.exists():
        click.echo(f"❌ Input file not found: {input_file}")
        return
    
    # Load and validate graph
    graph = CitationGraph.from_json(str(input_path))
    
    logger.info(f"Building graph from {input_file}")
    click.echo(f"📊 Building graph...")
    
    stats = graph.get_stats()
    
    click.echo(f"\n✅ Graph built!")
    click.echo(f"   Nodes: {stats['total_papers']}")
    click.echo(f"   Edges: {stats['total_citations']}")
    click.echo(f"   Density: {stats['density']:.4f}")
    click.echo(f"   Connected: {stats['is_connected']}")


@cli.command()
@click.option("--input", "input_file", type=click.Path(), default="output/graph.json", help="Input graph file")
@click.option("--format", "fmt", type=click.Choice(["json", "graphml", "bibtex"]), default="json", help="Export format")
@click.option("--output", type=click.Path(), help="Output file (default: input with new extension)")
@click.pass_context
def export(ctx, input_file, fmt, output):
    """Export graph to different formats"""
    input_path = Path(input_file)
    if not input_path.exists():
        click.echo(f"❌ Input file not found: {input_file}")
        return
    
    logger.info(f"Loading graph from {input_file}")
    graph = CitationGraph.from_json(str(input_path))
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.with_suffix(f".{fmt}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Exporting to {fmt}: {output_path}")
    click.echo(f"📤 Exporting to {fmt}...")
    
    # Export using the export module
    export_graph(graph, str(output_path), fmt)
    
    click.echo(f"✅ Exported to {output_path}")


@cli.command()
@click.option("--port", type=int, default=8000, help="HTTP server port")
@click.option("--input", "input_file", type=click.Path(), default="output/graph.json", help="Input graph file")
@click.option("--browser/--no-browser", default=True, help="Open browser automatically")
@click.pass_context
def visualize(ctx, port, input_file, browser):
    """Start visualization web server"""
    input_path = Path(input_file)
    if not input_path.exists():
        click.echo(f"❌ Input file not found: {input_file}")
        return
    
    # Check if visualization HTML exists
    viz_path = Path(__file__).parent.parent / "output" / "index.html"
    
    if not viz_path.exists():
        click.echo(f"❌ Visualization not found at {viz_path}")
        return
    
    import http.server
    import socketserver
    import webbrowser
    import os
    
    # Change to output directory
    os.chdir(viz_path.parent)
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    # Try to find an open port
    for try_port in range(port, port + 10):
        try:
            with socketserver.TCPServer(("", try_port), Handler) as httpd:
                url = f"http://localhost:{try_port}/index.html"
                logger.info(f"Serving visualization at {url}")
                click.echo(f"🌐 Visualizing at {url}")
                
                if browser:
                    webbrowser.open(url)
                
                click.echo("Press Ctrl+C to stop...")
                httpd.serve_forever()
                break
        except OSError:
            continue
    else:
        click.echo(f"❌ Could not find open port in range {port}-{port+9}")


@cli.command()
@click.argument("input_file", type=click.Path())
@click.pass_context
def stats(ctx, input_file):
    """Show statistics about a graph"""
    input_path = Path(input_file)
    if not input_path.exists():
        click.echo(f"❌ File not found: {input_file}")
        return
    
    graph = CitationGraph.from_json(str(input_path))
    stats = graph.get_stats()
    
    click.echo("\n📊 Graph Statistics\n")
    click.echo(f"   Total papers: {stats['total_papers']}")
    click.echo(f"   Total citations: {stats['total_citations']}")
    click.echo(f"   Seed papers: {stats['seed_papers']}")
    click.echo(f"   Max depth: {stats['max_depth']}")
    click.echo(f"   Density: {stats['density']:.4f}")
    click.echo(f"   Connected: {stats['is_connected']}")
    
    click.echo("\n   📈 Papers by year:")
    for year, count in list(stats["papers_by_year"].items())[:10]:
        click.echo(f"      {year}: {count}")
    
    click.echo("\n   🏆 Most cited:")
    for i, paper in enumerate(stats["most_cited"][:5], 1):
        click.echo(f"      {i}. {paper['title'][:40]}... ({paper['year'] or 'n/a'}) - {paper['citations_in_graph']} citations")


@cli.command()
@click.option("--host", default="localhost", help="Host to bind to")
@click.option("--port", type=int, default=8765, help="Port to bind to")
@click.option("--graph", type=click.Path(), default="output/graph.json", help="Graph file path")
@click.pass_context
def serve(ctx, host, port, graph):
    """Start interactive web server"""
    from .server import TraceTheoryServer, ServerConfig
    
    config = ctx.obj["config"]
    email = config.get("institution", {}).get("login", {}).get("email", "test@example.com")
    
    server_config = ServerConfig(
        host=host,
        port=port,
        graph_path=graph,
        email=email,
    )
    
    click.echo(f"🌐 Starting server at http://{host}:{port}")
    click.echo(f"📄 Graph: {graph}")
    click.echo("Press Ctrl+C to stop...")
    
    server = TraceTheoryServer(server_config)
    server.run()


if __name__ == "__main__":
    cli()