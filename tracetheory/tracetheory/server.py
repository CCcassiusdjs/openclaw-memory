#!/usr/bin/env python3
"""
TraceTheory Interactive Server

Web server for interactive citation graph exploration.
Provides REST API for:
- GET /api/graph - current graph state
- POST /api/expand - expand specific node
- GET /api/paper/:id - paper details
- GET /api/status - server status
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from aiohttp import web
import urllib.parse

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.search.openalex import OpenAlexClient, Work
from src.search.semantic_scholar import SemanticScholarClient
from src.storage.graph import CitationGraph, PaperNode
from src.orchestrator.crawler import CitationCrawler, CrawlConfig

logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "localhost"
    port: int = 8765
    graph_path: str = "output/graph.json"
    cache_dir: str = "cache"
    email: str = "test@example.com"


class TraceTheoryServer:
    """
    Interactive server for TraceTheory.
    
    Features:
    - REST API for graph operations
    - Interactive node expansion
    - PDF reference extraction
    """
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.app = web.Application()
        
        # Graph state
        self.graph = CitationGraph()
        self.graph_path = Path(config.graph_path)
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get('/', self.serve_index)
        self.app.router.add_get('/api/graph', self.get_graph)
        self.app.router.add_get('/api/paper/{paper_id:.*}', self.get_paper)
        self.app.router.add_post('/api/expand', self.expand_node)
        self.app.router.add_post('/api/seed', self.seed_paper)
        self.app.router.add_get('/api/status', self.get_status)
        self.app.router.add_static('/static', self.graph_path.parent)
    
    async def serve_index(self, request: web.Request) -> web.Response:
        """Serve index.html"""
        index_path = self.graph_path.parent / "index.html"
        if index_path.exists():
            return web.Response(
                text=index_path.read_text(),
                content_type='text/html'
            )
        return web.Response(text="Index not found", status=404)
    
    async def get_graph(self, request: web.Request) -> web.Response:
        """Get current graph state"""
        return web.Response(
            text=json.dumps(self.graph.to_dict()),
            content_type='application/json'
        )
    
    async def get_paper(self, request: web.Request) -> web.Response:
        """Get paper details by ID"""
        paper_id = request.match_info['paper_id']
        
        # URL decode
        import urllib.parse
        paper_id = urllib.parse.unquote(paper_id)
        
        if paper_id in self.graph.graph.nodes:
            data = self.graph.graph.nodes[paper_id]
            return web.Response(
                text=json.dumps(data),
                content_type='application/json'
            )
        
        # Try to fetch from OpenAlex
        async with OpenAlexClient(email=self.config.email) as client:
            work = await client.get_work(paper_id)
            if work:
                return web.Response(
                    text=json.dumps(self._work_to_dict(work)),
                    content_type='application/json'
                )
        
        return web.Response(text="Paper not found", status=404)
    
    async def expand_node(self, request: web.Request) -> web.Response:
        """Expand a specific node"""
        try:
            data = await request.json()
            paper_id = data.get('paper_id')
            direction = data.get('direction', 'backward')  # backward, forward, both
            depth = data.get('depth', 1)
            
            if not paper_id:
                return web.Response(
                    text=json.dumps({"error": "paper_id required"}),
                    content_type='application/json',
                    status=400
                )
            
            # Import urllib.parse
            import urllib.parse
            paper_id = urllib.parse.unquote(paper_id)
            
            # Queue expansion
            logger.info(f"Expanding node: {paper_id[:50]}... (direction={direction}, depth={depth})")
            
            # Run expansion
            result = await self._expand_node_async(paper_id, direction, depth)
            
            return web.Response(
                text=json.dumps(result),
                content_type='application/json'
            )
        except Exception as e:
            logger.exception("Expansion failed")
            return web.Response(
                text=json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )
    
    async def seed_paper(self, request: web.Request) -> web.Response:
        """Seed graph with starting paper"""
        try:
            data = await request.json()
            doi = data.get('doi')
            title = data.get('title')
            
            result = await self._seed_async(doi, title)
            return web.Response(
                text=json.dumps(result),
                content_type='application/json'
            )
        except Exception as e:
            logger.exception("Seed failed")
            return web.Response(
                text=json.dumps({"error": str(e)}),
                content_type='application/json',
                status=500
            )
    
    async def get_status(self, request: web.Request) -> web.Response:
        """Get server status"""
        return web.Response(
            text=json.dumps({
                "status": "ok",
                "papers": len(self.graph.graph.nodes),
                "edges": len(list(self.graph.graph.edges)),
                "seed_papers": list(self.graph.seed_papers),
            }),
            content_type='application/json'
        )
    
    async def _expand_node_async(self, paper_id: str, direction: str, depth: int) -> Dict:
        """Expand a node asynchronously"""
        follow_references = direction in ['backward', 'both']
        follow_citations = direction in ['forward', 'both']
        
        config = CrawlConfig(
            max_depth=depth,
            max_papers_per_depth=50,
            follow_references=follow_references,
            follow_citations=follow_citations,
            source="openalex",
            email=self.config.email,
        )
        
        crawler = CitationCrawler(config)
        crawler.state.queue.append(paper_id)
        crawler.state.depth_map[paper_id] = 0
        
        papers = await crawler.crawl_openalex(email=self.config.email)
        
        # Add to graph
        added = 0
        for pid, pdata in papers.items():
            if pid not in self.graph.graph.nodes:
                node = PaperNode(
                    id=pid,
                    title=pdata.get("title", ""),
                    authors=pdata.get("authors", []),
                    year=pdata.get("year"),
                    venue=pdata.get("venue"),
                    doi=pdata.get("doi"),
                    abstract=pdata.get("abstract"),
                    citation_count=pdata.get("citation_count", 0),
                    reference_count=pdata.get("reference_count", 0),
                    seed_id=paper_id,
                    depth=pdata.get("depth", 0),
                    source="openalex",
                )
                self.graph.add_paper(node)
                added += 1
            
            # Add edges
            for ref_id in pdata.get("references", []):
                if ref_id in papers:
                    self.graph.graph.add_edge(pid, ref_id)
        
        # Save graph
        self.graph.to_json(str(self.graph_path))
        
        # Build new papers dict for response
        new_papers = {}
        new_edges = []
        for pid, pdata in papers.items():
            if pid not in self.graph.graph.nodes or added > 0:
                new_papers[pid] = pdata
            for ref_id in pdata.get("references", []):
                if ref_id in papers:
                    new_edges.append({"source": pid, "target": ref_id, "type": "backward"})
        
        return {
            "status": "ok",
            "added": added,
            "total_papers": len(self.graph.graph.nodes),
            "total_edges": len(list(self.graph.graph.edges)),
            "new_papers": new_papers,
            "new_edges": new_edges,
        }
    
    async def _seed_async(self, doi: Optional[str], title: Optional[str]) -> Dict:
        """Seed graph with a paper"""
        async with OpenAlexClient(email=self.config.email) as client:
            work = None
            
            if doi:
                work = await client.get_work_by_doi(doi)
            
            if not work and title:
                results = await client.search_works(title, limit=1)
                if results:
                    work = Work.from_api(results[0])
            
            if work:
                self.graph = CitationGraph()
                node = self._work_to_node(work, depth=0)
                self.graph.add_paper(node)
                self.graph.seed_papers.add(work.work_id)
                self.graph.metadata["seed_paper"] = work.work_id
                self.graph.metadata["seed_title"] = work.title
                self.graph.metadata["source"] = "openalex"
                
                self.graph.to_json(str(self.graph_path))
                
                return {
                    "status": "ok",
                    "paper": self._work_to_dict(work),
                    "graph_size": len(self.graph.graph.nodes),
                }
        
        return {"status": "error", "message": "Paper not found"}
    
    def _work_to_node(self, work: Work, depth: int = 0, seed_id: str = None) -> PaperNode:
        """Convert Work to PaperNode"""
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
            seed_id=seed_id or work.work_id,
            depth=depth,
            source="openalex",
        )
    
    def _work_to_dict(self, work: Work) -> Dict:
        """Convert Work to dict"""
        return {
            "id": work.work_id,
            "title": work.title,
            "authors": work.authors,
            "year": work.year,
            "venue": work.venue,
            "doi": work.doi,
            "abstract": work.abstract,
            "citation_count": work.cited_by_count,
            "reference_count": len(work.referenced_works) if work.referenced_works else 0,
            "references": work.referenced_works[:10],  # First 10
        }
    
    async def startup(self, app: web.Application):
        """Startup: load graph"""
        if self.graph_path.exists():
            try:
                self.graph = CitationGraph.from_json(str(self.graph_path))
                logger.info(f"Loaded graph: {len(self.graph.graph.nodes)} papers")
            except Exception as e:
                logger.warning(f"Could not load graph: {e}")
        
        logger.info(f"Server started on http://{self.config.host}:{self.config.port}")
    
    async def cleanup(self, app: web.Application):
        """Cleanup"""
        pass
    
    def run(self):
        """Run the server"""
        self.app.on_startup.append(self.startup)
        self.app.on_cleanup.append(self.cleanup)
        web.run_app(self.app, host=self.config.host, port=self.config.port)


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TraceTheory Interactive Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind to")
    parser.add_argument("--graph", default="output/graph.json", help="Graph file path")
    parser.add_argument("--email", default="test@example.com", help="Email for OpenAlex API")
    
    args = parser.parse_args()
    
    config = ServerConfig(
        host=args.host,
        port=args.port,
        graph_path=args.graph,
        email=args.email,
    )
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    server = TraceTheoryServer(config)
    server.run()


if __name__ == "__main__":
    main()