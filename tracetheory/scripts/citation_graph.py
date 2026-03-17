#!/usr/bin/env python3
"""
TraceTheory - Motor de Recursão para Arqueologia Intelectual

Processa citações recursivamente:
1. Backward citations (referências que o paper cita)
2. Forward citations (papers que citam o paper)
3. Correções (erratas, retratações)
4. Traduções

Gera grafo para visualização interativa.

Autor: TraceTheory
Data: 2026-03-16
"""

import json
import time
import requests
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Set
from datetime import datetime

# Configurações
OPENALEX_API = "https://api.openalex.org"
OPENALEX_EMAIL = "cassiojonesdhein@gmail.com"
RATE_LIMIT_DELAY = 0.1  # 10 req/sec

# Tipos de nodos
NODE_TYPES = {
    "original": {"color": "#3498db", "icon": "📄", "label": "Paper Original"},
    "correction": {"color": "#e74c3c", "icon": "✏️", "label": "Correção"},
    "book": {"color": "#27ae60", "icon": "📚", "label": "Livro"},
    "backward_citation": {"color": "#e67e22", "icon": "⬅️", "label": "Citação Backward"},
    "forward_citation": {"color": "#1abc9c", "icon": "➡️", "label": "Citação Forward"},
    "translation": {"color": "#f39c12", "icon": "🌐", "label": "Tradução"},
    "review": {"color": "#9b59b6", "icon": "📝", "label": "Review"},
}

@dataclass
class Node:
    """Nó do grafo de citações."""
    id: str
    type: str
    label_short: str
    label_full: str
    authors: List[str]
    year: int
    venue: str
    volume: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    openalex_id: Optional[str] = None
    citation_count: Optional[int] = None
    reference_count: Optional[int] = None
    summary: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    significance: Optional[str] = None
    tooltip: Dict = field(default_factory=dict)
    is_seed: bool = False
    depth: int = 0
    expanded: bool = False

@dataclass
class Edge:
    """Aresta do grafo de citações."""
    source: str
    target: str
    type: str
    label: str
    weight: float = 1.0
    context: Optional[str] = None

class CitationGraph:
    """Grafo de citações com recursão."""
    
    def __init__(self, seed_node: Node):
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.seed_id = seed_node.id
        
        # Adicionar seed node
        self.nodes[seed_node.id] = seed_node
    
    def add_node(self, node: Node):
        """Adiciona um nó ao grafo."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
    
    def add_edge(self, edge: Edge):
        """Adiciona uma aresta ao grafo."""
        self.edges.append(edge)
    
    def fetch_openalex_work(self, openalex_id: str) -> Optional[Dict]:
        """Busca dados de um trabalho no OpenAlex."""
        try:
            url = f"{OPENALEX_API}/works/{openalex_id}"
            params = {"mailto": OPENALEX_EMAIL}
            
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            time.sleep(RATE_LIMIT_DELAY)
            
            return resp.json()
        except Exception as e:
            print(f"Erro ao buscar OpenAlex {openalex_id}: {e}")
            return None
    
    def fetch_backward_citations(self, openalex_id: str, max_papers: int = 50) -> List[Node]:
        """Busca citações backward (referências)."""
        nodes = []
        
        try:
            # Buscar trabalho
            work = self.fetch_openalex_work(openalex_id)
            if not work:
                return nodes
            
            referenced_works = work.get("referenced_works", [])[:max_papers]
            
            for ref_id in referenced_works:
                ref_work = self.fetch_openalex_work(ref_id)
                if ref_work:
                    # Extrair dados
                    authors = [a.get("author", {}).get("display_name", "") 
                              for a in ref_work.get("authorships", [])[:5]]
                    
                    node = Node(
                        id=ref_work.get("id", "").split("/")[-1],
                        type="backward_citation",
                        label_short=self._short_label(ref_work),
                        label_full=ref_work.get("title", "Unknown"),
                        authors=authors,
                        year=ref_work.get("publication_year", 0),
                        venue=self._get_venue(ref_work),
                        doi=ref_work.get("doi"),
                        url=f"https://doi.org/{ref_work.get('doi')}" if ref_work.get('doi') else None,
                        openalex_id=ref_work.get("id", "").split("/")[-1],
                        citation_count=ref_work.get("cited_by_count", 0),
                        reference_count=len(ref_work.get("referenced_works", [])),
                        summary=ref_work.get("abstract_inverted_index"),
                        keywords=[kw.get("display_name", "") for kw in ref_work.get("keywords", [])[:5]],
                        depth=self.nodes[openalex_id].depth + 1 if openalex_id in self.nodes else 1
                    )
                    nodes.append(node)
            
        except Exception as e:
            print(f"Erro ao buscar backward citations: {e}")
        
        return nodes
    
    def fetch_forward_citations(self, openalex_id: str, max_papers: int = 50) -> List[Node]:
        """Busca citações forward (papers que citam)."""
        nodes = []
        
        try:
            url = f"{OPENALEX_API}/works"
            params = {
                "mailto": OPENALEX_EMAIL,
                "filter": f"cites:{openalex_id}",
                "per_page": max_papers
            }
            
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            time.sleep(RATE_LIMIT_DELAY)
            
            data = resp.json()
            results = data.get("results", [])
            
            for work in results:
                authors = [a.get("author", {}).get("display_name", "") 
                          for a in work.get("authorships", [])[:5]]
                
                node = Node(
                    id=work.get("id", "").split("/")[-1],
                    type="forward_citation",
                    label_short=self._short_label(work),
                    label_full=work.get("title", "Unknown"),
                    authors=authors,
                    year=work.get("publication_year", 0),
                    venue=self._get_venue(work),
                    doi=work.get("doi"),
                    url=f"https://doi.org/{work.get('doi')}" if work.get('doi') else None,
                    openalex_id=work.get("id", "").split("/")[-1],
                    citation_count=work.get("cited_by_count", 0),
                    reference_count=len(work.get("referenced_works", [])),
                    keywords=[kw.get("display_name", "") for kw in work.get("keywords", [])[:5]],
                    depth=self.nodes[openalex_id].depth + 1 if openalex_id in self.nodes else 1
                )
                nodes.append(node)
            
        except Exception as e:
            print(f"Erro ao buscar forward citations: {e}")
        
        return nodes
    
    def expand_node(self, node_id: str, direction: str = "both", max_papers: int = 50) -> int:
        """Expande um nó buscando suas citações."""
        node = self.nodes.get(node_id)
        if not node or not node.openalex_id:
            return 0
        
        count = 0
        
        # Backward citations
        if direction in ["backward", "both"]:
            backward_nodes = self.fetch_backward_citations(node.openalex_id, max_papers)
            for n in backward_nodes:
                self.add_node(n)
                self.add_edge(Edge(
                    source=node_id,
                    target=n.id,
                    type="cites",
                    label="cita"
                ))
                count += 1
        
        # Forward citations
        if direction in ["forward", "both"]:
            forward_nodes = self.fetch_forward_citations(node.openalex_id, max_papers)
            for n in forward_nodes:
                self.add_node(n)
                self.add_edge(Edge(
                    source=n.id,
                    target=node_id,
                    type="cites",
                    label="cita"
                ))
                count += 1
        
        # Marcar como expandido
        self.nodes[node_id].expanded = True
        
        return count
    
    def _short_label(self, work: Dict) -> str:
        """Gera label curto para o nó."""
        authors = work.get("authorships", [])
        if authors:
            first_author = authors[0].get("author", {}).get("display_name", "Unknown")
            last_name = first_author.split()[-1] if first_author else "Unknown"
        else:
            last_name = "Unknown"
        
        year = work.get("publication_year", "????")
        return f"{last_name} {year}"
    
    def _get_venue(self, work: Dict) -> str:
        """Extrai venue do trabalho."""
        location = work.get("primary_location", {})
        if location:
            source = location.get("source", {})
            if source:
                return source.get("display_name", "Unknown")
        return "Unknown"
    
    def to_json(self) -> Dict:
        """Converte grafo para JSON."""
        return {
            "metadata": {
                "project": "TraceTheory - Arqueologia Intelectual Interativa",
                "version": "2.0",
                "created": datetime.now().isoformat(),
                "seed_id": self.seed_id,
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "visualization": {
                    "engine": "D3.js / Cytoscape.js",
                    "node_types": NODE_TYPES
                }
            },
            "nodes": [asdict(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges],
            "ui_config": {
                "node_size": {
                    "by": "citation_count",
                    "min": 20,
                    "max": 100,
                    "null_value": 30
                },
                "tooltip": {
                    "show_on_hover": True,
                    "fields": ["title", "authors_line", "venue_line", "citations", "links"]
                }
            },
            "statistics": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "by_type": self._count_by_type(),
                "by_year": self._count_by_year()
            }
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Conta nós por tipo."""
        counts = {}
        for node in self.nodes.values():
            counts[node.type] = counts.get(node.type, 0) + 1
        return counts
    
    def _count_by_year(self) -> Dict[int, int]:
        """Conta nós por ano."""
        counts = {}
        for node in self.nodes.values():
            if node.year:
                counts[node.year] = counts.get(node.year, 0) + 1
        return counts
    
    def save(self, output_path: str):
        """Salva grafo em JSON."""
        data = self.to_json()
        Path(output_path).write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"Grafo salvo em: {output_path}")


def main():
    """Demo do CitationGraph."""
    print("=" * 78)
    print("TRACETHEORY - Motor de Recursão para Arqueologia Intelectual")
    print("=" * 78)
    
    # Criar nó seed (Turing 1936)
    seed = Node(
        id="W2126160338",
        type="original",
        label_short="Turing 1936",
        label_full="On Computable Numbers, with an Application to the Entscheidungsproblem",
        authors=["Alan M. Turing"],
        year=1936,
        venue="Proceedings of the London Mathematical Society",
        volume="42",
        pages="230-265",
        doi="10.1112/plms/s2-42.1.230",
        url="https://doi.org/10.1112/plms/s2-42.1.230",
        pdf_url="https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf",
        openalex_id="W2126160338",
        citation_count=8021,
        reference_count=8,
        summary="Foundational paper introducing the concept of a 'universal machine'",
        keywords=["Turing machine", "computability", "Entscheidungsproblem"],
        is_seed=True,
        depth=0
    )
    
    # Criar grafo
    graph = CitationGraph(seed)
    
    # Carregar citações backward já extraídas
    backward_json = Path("/home/csilva/.openclaw/workspace/tracetheory/output/turing_1936_backward_citations.json")
    if backward_json.exists():
        data = json.loads(backward_json.read_text())
        for ref in data.get("references", []):
            node = Node(
                id=ref.get("id", f"BACKWARD_{ref['year']}"),
                type="backward_citation",
                label_short=f"{ref['authors'][0].split()[-1]} {ref['year']}" if ref.get('authors') else f"Unknown {ref.get('year', '????')}",
                label_full=ref.get("title", "Unknown"),
                authors=ref.get("authors", []),
                year=ref.get("year", 0),
                venue=ref.get("venue", "Unknown"),
                doi=ref.get("doi"),
                url=ref.get("url"),
                pdf_url=ref.get("pdf_url"),
                summary=ref.get("significance"),
                keywords=ref.get("keywords", []),
                depth=1
            )
            graph.add_node(node)
            graph.add_edge(Edge(
                source="W2126160338",
                target=node.id,
                type="cites",
                label="cita",
                context=ref.get("context")
            ))
    
    # Salvar grafo
    output_path = "/home/csilva/.openclaw/workspace/tracetheory/output/citation_graph_full.json"
    graph.save(output_path)
    
    # Mostrar estatísticas
    print("\n" + "=" * 78)
    print("ESTATÍSTICAS DO GRAFO:")
    print("=" * 78)
    print(f"Total de nós: {len(graph.nodes)}")
    print(f"Total de arestas: {len(graph.edges)}")
    print("\nPor tipo:")
    for type_name, count in graph._count_by_type().items():
        print(f"  {NODE_TYPES.get(type_name, {}).get('label', type_name)}: {count}")
    print("\nPor ano:")
    for year, count in sorted(graph._count_by_year().items()):
        print(f"  {year}: {count}")
    
    print("\n" + "=" * 78)
    print(f"Arquivo salvo: {output_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()