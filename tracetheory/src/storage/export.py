"""
Export Module for TraceTheory

Supports exporting citation graphs to multiple formats:
- JSON (native format with full metadata)
- GraphML (for Gephi, Cytoscape, etc.)
- BibTeX (for LaTeX/BibLaTeX bibliography)
"""

import json
import html
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

import networkx as nx

from .graph import CitationGraph, PaperNode


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters"""
    if not text:
        return ""
    
    # Unicode to LaTeX conversions for common characters
    unicode_replacements = {
        'ö': '{\"o}', 'Ö': '{\"O}',
        'ä': '{\"a}', 'Ä': '{\"A}',
        'ü': '{\"u}', 'Ü': '{\"U}',
        'é': "\\'{e}", 'è': "\\`{e}",
        'à': "\\`{a}", 'á': "\\'{a}",
        'ç': "\\c{c}", 'ß': '{\\ss}',
        'ø': '{\\o}', 'Ø': '{\\O}',
        'ñ': "\\~{n}", '~': '{\\textasciitilde}',
    }
    
    for char, replacement in unicode_replacements.items():
        text = text.replace(char, replacement)
    
    # Basic LaTeX escaping for special symbols
    replacements = {
        '\\': '\\textbackslash{}',
        '{': '\\{',
        '}': '\\}',
        '_': '\\_',
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '^': '\\textasciicircum{}',
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text


def paper_to_bibtex(paper: PaperNode, key: str = None) -> str:
    """Convert a PaperNode to BibTeX format"""
    if key is None:
        # Generate key from first author and year
        author_last = paper.authors[0].split()[-1] if paper.authors else "unknown"
        key = f"{author_last}{paper.year or 'ny'}"
    
    # Determine entry type
    if paper.venue:
        venue_lower = paper.venue.lower()
        if "conference" in venue_lower or "proc" in venue_lower:
            entry_type = "inproceedings"
        elif "journal" in venue_lower or "IEEE" in paper.venue or "ACM" in paper.venue:
            entry_type = "article"
        else:
            entry_type = "article"
    else:
        entry_type = "article"
    
    lines = [f"@{entry_type}{{{key}}},"]
    
    # Title
    if paper.title:
        title_escaped = escape_latex(paper.title)
        lines.append(f"  title = {{{title_escaped}}},")
    
    # Authors
    if paper.authors:
        authors_str = " and ".join(paper.authors)
        authors_escaped = escape_latex(authors_str)
        lines.append(f"  author = {{{authors_escaped}}},")
    
    # Year
    if paper.year:
        lines.append(f"  year = {{{paper.year}}},")
    
    # Venue
    if paper.venue:
        venue_escaped = escape_latex(paper.venue)
        lines.append(f"  journal = {{{venue_escaped}}},")
    
    # DOI
    if paper.doi:
        lines.append(f"  doi = {{{paper.doi}}},")
    
    # Citation count (as note)
    if paper.citation_count:
        lines.append(f"  note = {{{paper.citation_count} citations}},")
    
    # Abstract
    if paper.abstract:
        abstract = paper.abstract[:500] + "..." if len(paper.abstract) > 500 else paper.abstract
        abstract_escaped = escape_latex(abstract)
        lines.append(f"  abstract = {{{abstract_escaped}}},")
    
    lines.append("}")
    
    return "\n".join(lines)


def export_bibtex(graph: CitationGraph, filepath: str) -> None:
    """
    Export graph to BibTeX format.
    
    Each paper becomes a BibTeX entry.
    """
    entries: List[str] = []
    
    # Header comment
    entries.append(f"% BibTeX export from TraceTheory")
    entries.append(f"% Generated: {datetime.now().isoformat()}")
    entries.append(f"% Total papers: {len(graph.graph.nodes)}")
    entries.append("")
    
    # Generate unique keys for papers
    key_counter: Dict[str, int] = {}
    
    for node_id in graph.graph.nodes:
        data = graph.graph.nodes[node_id]
        paper = PaperNode.from_dict(data)
        
        # Generate unique key
        author_last = paper.authors[0].split()[-1] if paper.authors else "unknown"
        base_key = f"{author_last}{paper.year or 'ny'}"
        
        if base_key in key_counter:
            key_counter[base_key] += 1
            key = f"{base_key}_{key_counter[base_key]}"
        else:
            key_counter[base_key] = 0
            key = base_key
        
        entries.append(paper_to_bibtex(paper, key))
        entries.append("")
    
    # Write file
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(entries))
    
    return filepath


def export_json(graph: CitationGraph, filepath: str) -> None:
    """Export graph to JSON format (delegates to CitationGraph)"""
    graph.to_json(filepath)


def export_graphml(graph: CitationGraph, filepath: str) -> None:
    """Export graph to GraphML format (delegates to CitationGraph)"""
    graph.to_graphml(filepath)


def export_cytoscape(graph: CitationGraph, filepath: str) -> None:
    """Export graph to Cytoscape JSON format (delegates to CitationGraph)"""
    graph.to_cytoscape(filepath)


def export_graph(graph: CitationGraph, filepath: str, format: str = "json") -> str:
    """
    Export citation graph to specified format.
    
    Args:
        graph: The CitationGraph to export
        filepath: Output file path
        format: One of "json", "graphml", "bibtex", "cytoscape"
    
    Returns:
        The output filepath
    """
    format = format.lower()
    
    if format == "json":
        export_json(graph, filepath)
    elif format == "graphml":
        export_graphml(graph, filepath)
    elif format == "bibtex":
        export_bibtex(graph, filepath)
    elif format == "cytoscape":
        export_cytoscape(graph, filepath)
    else:
        raise ValueError(f"Unknown export format: {format}. Supported: json, graphml, bibtex, cytoscape")
    
    return filepath


# Format descriptions for CLI help
EXPORT_FORMATS = {
    "json": "Native JSON format with full metadata",
    "graphml": "GraphML format for Gephi/Cytoscape",
    "bibtex": "BibTeX format for LaTeX bibliography",
    "cytoscape": "Cytoscape.js JSON format",
}


if __name__ == "__main__":
    # Quick test
    from .graph import CitationGraph, PaperNode
    
    # Create test graph
    graph = CitationGraph()
    
    turing = PaperNode(
        id="turing1936",
        title="On Computable Numbers",
        authors=["Alan M. Turing"],
        year=1936,
        venue="Proceedings of the London Mathematical Society",
        doi="10.1112/plms/s2-42.1.230",
        abstract=None,
        citation_count=15000,
        reference_count=5,
        seed_id=None,
        depth=0,
        source="manual",
    )
    
    graph.add_paper(turing)
    graph.seed_papers.add("turing1936")
    
    # Export to all formats
    print("Testing exports...")
    
    export_json(graph, "/tmp/test_graph.json")
    print("  ✓ JSON")
    
    export_graphml(graph, "/tmp/test_graph.graphml")
    print("  ✓ GraphML")
    
    export_bibtex(graph, "/tmp/test_graph.bibtex")
    print("  ✓ BibTeX")
    
    print("\nAll exports successful!")