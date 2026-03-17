#!/usr/bin/env python3
"""
TraceTheory Crawler - OpenAlex API

Recursive citation graph crawler starting from Turing 1936.
"""

import asyncio
import aiohttp
import json
import time
from pathlib import Path
from typing import Dict, Set, List, Optional
from dataclasses import dataclass, field, asdict
from collections import deque

# Config
OUTPUT_DIR = Path(__file__).parent.parent / "output"
CHECKPOINT_DIR = Path(__file__).parent.parent / "checkpoints"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

EMAIL = "cassiojonesdhein@gmail.com"  # For OpenAlex API
BASE_URL = "https://api.openalex.org"

# Rate limiting: ~10 req/sec
REQUEST_DELAY = 0.15


@dataclass
class Paper:
    """Paper metadata from OpenAlex"""
    id: str
    title: str
    authors: List[str]
    year: Optional[int]
    doi: Optional[str]
    citation_count: int
    referenced_works: List[str] = field(default_factory=list)
    cited_by_api_url: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass 
class CrawlState:
    """State of the crawl"""
    visited: Set[str] = field(default_factory=set)
    queue: deque = field(default_factory=lambda: deque())
    depth_map: Dict[str, int] = field(default_factory=dict)
    papers: Dict[str, Paper] = field(default_factory=dict)
    edges: List[tuple] = field(default_factory=list)  # (source, target) citations
    
    def to_json(self) -> dict:
        return {
            "visited": list(self.visited),
            "queue": list(self.queue),
            "depth_map": self.depth_map,
            "papers": {k: v.to_dict() for k, v in self.papers.items()},
            "edges": self.edges,
        }


class OpenAlexCrawler:
    """Crawl citation graph via OpenAlex API"""
    
    def __init__(self, max_depth: int = 3, max_per_depth: int = 50):
        self.max_depth = max_depth
        self.max_per_depth = max_per_depth
        self.state = CrawlState()
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _request(self, url: str, params: dict = None) -> dict:
        """Make rate-limited API request"""
        await asyncio.sleep(REQUEST_DELAY)
        
        headers = {"mailto": EMAIL}
        async with self.session.get(url, params=params, headers=headers) as resp:
            if resp.status == 404:
                return None  # Work not found
            if resp.status == 429:
                # Rate limited - wait and retry
                await asyncio.sleep(5)
                return await self._request(url, params)
            resp.raise_for_status()
            return await resp.json()
    
    async def get_work(self, work_id: str) -> Optional[Paper]:
        """Get work by OpenAlex ID"""
        url = f"{BASE_URL}/works/{work_id}"
        data = await self._request(url)
        if data is None:
            return None
        return self._parse_work(data)
    
    async def search_work(self, query: str) -> Optional[Paper]:
        """Search for a work by query"""
        url = f"{BASE_URL}/works"
        params = {"search": query, "per_page": 1}
        data = await self._request(url, params)
        
        if data.get("results"):
            return self._parse_work(data["results"][0])
        return None
    
    async def get_citations(self, work_id: str, limit: int = 100) -> List[str]:
        """Get works that cite this work"""
        url = f"{BASE_URL}/works"
        params = {
            "filter": f"cites:{work_id}",
            "per_page": limit,
            "sort": "cited_by_count:desc"
        }
        data = await self._request(url, params)
        return [w["id"].replace("https://openalex.org/", "") for w in data.get("results", [])]
    
    async def get_references(self, work_id: str) -> List[str]:
        """Get works cited by this work"""
        url = f"{BASE_URL}/works/{work_id}"
        data = await self._request(url)
        
        refs = data.get("referenced_works", [])
        return [r.replace("https://openalex.org/", "") for r in refs]
    
    def _parse_work(self, data: dict) -> Paper:
        """Parse OpenAlex work response"""
        work_id = data.get("id", "").replace("https://openalex.org/", "")
        authors = [
            a.get("author", {}).get("display_name", "?")
            for a in data.get("authorships", [])[:5]
        ]
        refs = [
            r.replace("https://openalex.org/", "")
            for r in data.get("referenced_works", [])
        ]
        
        return Paper(
            id=work_id,
            title=data.get("title", "Unknown"),
            authors=authors,
            year=data.get("publication_year"),
            doi=data.get("doi"),
            citation_count=data.get("cited_by_count", 0),
            referenced_works=refs,
        )
    
    async def crawl_from_seed(self, seed_query: str = "On Computable Numbers Turing 1936") -> Dict[str, Paper]:
        """
        Start crawl from seed paper.
        
        Traverses both:
        - References (back in time): What did this paper cite?
        - Citations (forward in time): Who cited this paper?
        """
        print(f"🔍 Finding seed paper: {seed_query}")
        
        # Find seed
        seed = await self.search_work(seed_query)
        if not seed:
            # Try by DOI
            seed = await self.get_work("W2126160338")  # Known Turing 1936 ID
        
        if not seed:
            print("❌ Could not find seed paper")
            return {}
        
        print(f"✅ Found: {seed.title} ({seed.year})")
        print(f"   Citations: {seed.citation_count:,}")
        print()
        
        # Initialize queue
        self.state.queue.append(seed.id)
        self.state.depth_map[seed.id] = 0
        self.state.papers[seed.id] = seed
        
        # BFS traversal
        while self.state.queue:
            current_id = self.state.queue.popleft()
            
            if current_id in self.state.visited:
                continue
            
            current_depth = self.state.depth_map.get(current_id, 0)
            
            if current_depth > self.max_depth:
                continue
            
            print(f"📊 Depth {current_depth}: {current_id}")
            
            # Fetch paper details if not cached
            if current_id not in self.state.papers:
                paper = await self.get_work(current_id)
                if not paper:
                    continue
                self.state.papers[current_id] = paper
            else:
                paper = self.state.papers[current_id]
            
            self.state.visited.add(current_id)
            
            # Get references (backward in time)
            if current_depth < self.max_depth:
                refs = paper.referenced_works[:self.max_per_depth]
                print(f"   References: {len(refs)} papers")
                
                for ref_id in refs:
                    if ref_id and ref_id not in self.state.visited:
                        self.state.queue.append(ref_id)
                        self.state.depth_map[ref_id] = current_depth + 1
                        self.state.edges.append((current_id, ref_id))  # current cites ref
            
            # Get citations (forward in time) - only for depth 0 and 1
            if current_depth < self.max_depth - 1:
                citations = await self.get_citations(current_id, limit=self.max_per_depth)
                print(f"   Citations: {len(citations)} papers")
                
                for cit_id in citations:
                    if cit_id and cit_id not in self.state.visited:
                        self.state.queue.append(cit_id)
                        self.state.depth_map[cit_id] = current_depth + 1
                        self.state.edges.append((cit_id, current_id))  # cit cites current
            
            # Checkpoint every 10 papers
            if len(self.state.visited) % 10 == 0:
                await self._save_checkpoint()
        
        # Final save
        await self._save_checkpoint()
        await self._export_graph()
        
        return self.state.papers
    
    async def _save_checkpoint(self):
        """Save current state"""
        checkpoint_file = CHECKPOINT_DIR / "state.json"
        with open(checkpoint_file, "w") as f:
            json.dump(self.state.to_json(), f, indent=2)
        print(f"   💾 Checkpoint saved ({len(self.state.visited)} papers)")
    
    async def _export_graph(self):
        """Export to JSON"""
        output_file = OUTPUT_DIR / "citation_graph.json"
        
        graph_data = {
            "metadata": {
                "seed": "Turing 1936",
                "max_depth": self.max_depth,
                "total_papers": len(self.state.papers),
                "total_edges": len(self.state.edges),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "nodes": [
                {
                    "id": pid,
                    "title": p.title,
                    "authors": p.authors,
                    "year": p.year,
                    "citation_count": p.citation_count,
                    "depth": self.state.depth_map.get(pid, -1),
                }
                for pid, p in self.state.papers.items()
            ],
            "edges": [
                {"source": src, "target": tgt, "type": "cites"}
                for src, tgt in self.state.edges
            ],
        }
        
        with open(output_file, "w") as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"\n✅ Graph exported to {output_file}")
        print(f"   Papers: {len(self.state.papers)}")
        print(f"   Edges: {len(self.state.edges)}")


async def main():
    print("🚀 TraceTheory Crawler")
    print("=" * 50)
    print()
    
    crawler = OpenAlexCrawler(max_depth=3, max_per_depth=30)
    
    async with crawler:
        papers = await crawler.crawl_from_seed("On Computable Numbers Turing 1936")
    
    # Print stats
    print("\n" + "=" * 50)
    print("📈 Statistics:")
    print(f"   Papers collected: {len(papers)}")
    
    # Top cited
    sorted_papers = sorted(papers.values(), key=lambda p: p.citation_count, reverse=True)
    print("\n🏆 Top 10 most cited papers:")
    for i, p in enumerate(sorted_papers[:10], 1):
        print(f"   {i:2}. {p.title[:50]}... ({p.year}) - {p.citation_count:,} cites")
    
    # Depth distribution
    depths = {}
    for pid, d in crawler.state.depth_map.items():
        depths[d] = depths.get(d, 0) + 1
    print("\n📊 Papers by depth:")
    for d in sorted(depths.keys()):
        print(f"   Depth {d}: {depths[d]} papers")


if __name__ == "__main__":
    asyncio.run(main())