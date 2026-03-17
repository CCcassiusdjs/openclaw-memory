"""
Citation Graph - NetworkX-based graph storage

Stores the citation network as a directed graph:
- Nodes: Papers
- Edges: Citations (A cites B = edge A -> B)

Supports export to multiple formats: JSON, GraphML, Cytoscape
"""

import json
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime

import networkx as nx


@dataclass
class PaperNode:
    """Node in the citation graph"""
    id: str                    # Unique identifier (DOI or semantic scholar ID)
    title: str
    authors: List[str]
    year: Optional[int]
    venue: Optional[str]
    doi: Optional[str]
    abstract: Optional[str]
    citation_count: int
    reference_count: int
    seed_id: Optional[str]     # ID of the seed paper that led to this
    depth: int                  # Depth in the crawl
    source: str                 # Where we found it (semantic_scholar, openalex, etc.)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PaperNode":
        return cls(**data)


class CitationGraph:
    """
    Directed graph of paper citations.
    
    Edge direction: A -> B means "A cites B"
    (A references B in its bibliography)
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.seed_papers: Set[str] = set()  # Starting papers
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "seed_paper": None,
            "max_depth": 0,
            "total_papers": 0,
        }
    
    def add_paper(self, paper: PaperNode) -> None:
        """Add a paper node to the graph"""
        self.graph.add_node(
            paper.id,
            **paper.to_dict()
        )
    
    def add_citation(self, source_id: str, target_id: str) -> None:
        """
        Add a citation edge.
        
        Args:
            source_id: Paper that cites (references)
            target_id: Paper that is cited
        """
        self.graph.add_edge(source_id, target_id, type="cites")
    
    def add_reference(self, paper_id: str, reference_id: str) -> None:
        """
        Add a reference (same as citation, but clearer semantics).
        
        Args:
            paper_id: The paper
            reference_id: Paper it references
        """
        self.add_citation(paper_id, reference_id)
    
    def get_paper(self, paper_id: str) -> Optional[PaperNode]:
        """Get paper by ID"""
        if paper_id in self.graph:
            data = self.graph.nodes[paper_id]
            return PaperNode.from_dict(data)
        return None
    
    def get_references(self, paper_id: str) -> List[str]:
        """Get papers this paper references (outgoing edges)"""
        return list(self.graph.successors(paper_id))
    
    def get_citations(self, paper_id: str) -> List[str]:
        """Get papers that cite this paper (incoming edges)"""
        return list(self.graph.predecessors(paper_id))
    
    def get_papers_by_year(self, year: int) -> List[PaperNode]:
        """Get all papers from a specific year"""
        papers = []
        for node_id in self.graph.nodes:
            data = self.graph.nodes[node_id]
            if data.get("year") == year:
                papers.append(PaperNode.from_dict(data))
        return papers
    
    def get_papers_by_depth(self, depth: int) -> List[PaperNode]:
        """Get all papers at a specific crawl depth"""
        papers = []
        for node_id in self.graph.nodes:
            data = self.graph.nodes[node_id]
            if data.get("depth") == depth:
                papers.append(PaperNode.from_dict(data))
        return papers
    
    def get_ancestors(self, paper_id: str) -> Set[str]:
        """Get all papers that lead to this paper (through citations)"""
        return nx.ancestors(self.graph, paper_id)
    
    def get_descendants(self, paper_id: str) -> Set[str]:
        """Get all papers descended from this paper"""
        return nx.descendants(self.graph, paper_id)
    
    def find_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """Find citation path between two papers"""
        try:
            return nx.shortest_path(self.graph, source_id, target_id)
        except nx.NetworkXNoPath:
            return None
    
    def find_common_ancestors(self, paper_a: str, paper_b: str) -> Set[str]:
        """Find papers that both papers cite (directly or indirectly)"""
        ancestors_a = self.get_ancestors(paper_a)
        ancestors_b = self.get_ancestors(paper_b)
        return ancestors_a & ancestors_b
    
    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        return {
            "total_papers": self.graph.number_of_nodes(),
            "total_citations": self.graph.number_of_edges(),
            "seed_papers": len(self.seed_papers),
            "max_depth": self.metadata.get("max_depth", 0),
            "is_connected": nx.is_weakly_connected(self.graph),
            "density": nx.density(self.graph),
            "most_cited": self._get_most_cited(10),
            "papers_by_year": self._get_papers_by_year_distribution(),
        }
    
    def _get_most_cited(self, n: int = 10) -> List[Dict]:
        """Get n most cited papers"""
        in_degrees = dict(self.graph.in_degree())
        sorted_papers = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:n]
        
        result = []
        for paper_id, count in sorted_papers:
            data = self.graph.nodes.get(paper_id, {})
            result.append({
                "id": paper_id,
                "title": data.get("title", "Unknown"),
                "year": data.get("year"),
                "citations_in_graph": count,
            })
        return result
    
    def _get_papers_by_year_distribution(self) -> Dict[int, int]:
        """Get distribution of papers by year"""
        distribution = {}
        for node_id in self.graph.nodes:
            year = self.graph.nodes[node_id].get("year")
            if year:
                distribution[year] = distribution.get(year, 0) + 1
        return dict(sorted(distribution.items()))
    
    # Export methods
    
    def to_json(self, filepath: str) -> None:
        """Export to JSON"""
        data = {
            "metadata": self.metadata,
            "nodes": [
                {"id": n, **self.graph.nodes[n]}
                for n in self.graph.nodes
            ],
            "edges": [
                {"source": u, "target": v, **self.graph.edges[u, v]}
                for u, v in self.graph.edges
            ],
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def to_graphml(self, filepath: str) -> None:
        """Export to GraphML (for Gephi, Cytoscape, etc.)"""
        # GraphML requires string attributes
        export_graph = nx.DiGraph()
        
        for node_id in self.graph.nodes:
            node_data = {}
            for k, v in self.graph.nodes[node_id].items():
                if v is not None:
                    node_data[k] = str(v) if not isinstance(v, (str, int, float, bool)) else v
            export_graph.add_node(node_id, **node_data)
        
        for u, v in self.graph.edges:
            export_graph.add_edge(u, v, **self.graph.edges[u, v])
        
        nx.write_graphml(export_graph, filepath)
    
    def to_cytoscape(self, filepath: str) -> None:
        """Export to Cytoscape JSON format"""
        data = {
            "elements": {
                "nodes": [
                    {"data": {"id": n, **self.graph.nodes[n]}}
                    for n in self.graph.nodes
                ],
                "edges": [
                    {"data": {"source": u, "target": v, **self.graph.edges[u, v]}}
                    for u, v in self.graph.edges
                ],
            }
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, filepath: str) -> "CitationGraph":
        """Import from JSON"""
        graph = cls()
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        graph.metadata = data.get("metadata", {})
        
        for node in data.get("nodes", []):
            node_id = node.pop("id")
            paper = PaperNode(id=node_id, **node)
            graph.add_paper(paper)
        
        for edge in data.get("edges", []):
            source = edge.pop("source")
            target = edge.pop("target")
            graph.add_citation(source, target)
        
        return graph


# Example usage
if __name__ == "__main__":
    # Create a simple test graph
    graph = CitationGraph()
    
    # Add Turing 1936
    turing = PaperNode(
        id="turing1936",
        title="On Computable Numbers, with an Application to the Entscheidungsproblem",
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
    graph.metadata["seed_paper"] = "turing1936"
    
    # Add a reference
    godel = PaperNode(
        id="godel1931",
        title="Über formal unentscheidbare Sätze der Principia Mathematica",
        authors=["Kurt Gödel"],
        year=1931,
        venue=None,
        doi=None,
        abstract=None,
        citation_count=25000,
        reference_count=10,
        seed_id="turing1936",
        depth=1,
        source="manual",
    )
    
    graph.add_paper(godel)
    graph.add_reference("turing1936", "godel1931")
    
    # Export
    print("Stats:", graph.get_stats())
    graph.to_json("test_graph.json")
    print("Exported to test_graph.json")