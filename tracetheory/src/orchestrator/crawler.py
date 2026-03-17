"""
Crawler - Recursive paper traversal with proper checkpoint/resume

Implements BFS/DFS traversal of the citation graph, starting from a seed paper
and recursively fetching references/citations.

Supports both OpenAlex and Semantic Scholar APIs.
"""

import asyncio
from typing import Dict, Set, List, Optional, Callable, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import json
import logging
from pathlib import Path

from ..search.semantic_scholar import SemanticScholarClient, Paper
from ..search.openalex import OpenAlexClient, Work


logger = logging.getLogger(__name__)


def is_openalex_id(paper_id: str) -> bool:
    """Check if ID is OpenAlex format"""
    return paper_id.startswith("https://openalex.org/") or paper_id.startswith("W")


def normalize_openalex_id(paper_id: str) -> str:
    """Normalize OpenAlex ID to full URL format"""
    if paper_id.startswith("W") and not paper_id.startswith("https://"):
        return f"https://openalex.org/{paper_id}"
    return paper_id


@dataclass
class CrawlState:
    """State of the crawl"""
    visited: Set[str] = field(default_factory=set)
    queue: deque = field(default_factory=lambda: deque())
    depth_map: Dict[str, int] = field(default_factory=dict)
    papers: Dict[str, Dict] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)
    last_checkpoint: Optional[str] = None
    source: str = "openalex"  # Track which API we're using
    
    def to_dict(self) -> Dict:
        """Serialize state for checkpointing"""
        return {
            "visited": list(self.visited),
            "queue": list(self.queue),
            "depth_map": self.depth_map,
            "papers": self.papers,
            "errors": self.errors,
            "last_checkpoint": datetime.now().isoformat(),
            "source": self.source,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "CrawlState":
        """Deserialize state from checkpoint"""
        state = cls()
        state.visited = set(data.get("visited", []))
        state.queue = deque(data.get("queue", []))
        state.depth_map = data.get("depth_map", {})
        state.papers = data.get("papers", {})
        state.errors = data.get("errors", {})
        state.last_checkpoint = data.get("last_checkpoint")
        state.source = data.get("source", "openalex")
        return state
    
    def paper_count(self) -> int:
        """Number of papers fetched"""
        return len(self.papers)
    
    def queue_size(self) -> int:
        """Remaining papers to process"""
        return len(self.queue)


@dataclass
class CrawlConfig:
    """Crawler configuration"""
    max_depth: int = 5
    max_papers_per_depth: int = 100
    max_workers: int = 5
    follow_references: bool = True   # Follow papers cited by current paper (backward)
    follow_citations: bool = False    # Follow papers that cite current paper (forward)
    checkpoint_interval: int = 100
    checkpoint_file: str = "checkpoint.json"
    rate_limit_delay: float = 0.1     # Delay between API calls (seconds)
    source: str = "openalex"          # API to use: "openalex" or "semantic_scholar"
    email: str = ""                   # Email for OpenAlex API (better rate limits)


class CitationCrawler:
    """
    Recursive citation graph crawler.
    
    Starting from a seed paper, recursively fetches references/citations
    to build a genealogy of intellectual influence.
    
    Features:
    - BFS traversal for level-by-level expansion
    - Checkpoint/resume capability
    - Rate limiting
    - Progress callbacks
    - Error handling with logging
    - Support for both OpenAlex and Semantic Scholar
    """
    
    def __init__(
        self,
        config: CrawlConfig,
        on_paper_fetched: Optional[Callable] = None,
        on_error: Optional[Callable[[str, Exception], None]] = None,
    ):
        self.config = config
        self.state = CrawlState()
        self.state.source = config.source
        self.on_paper_fetched = on_paper_fetched
        self.on_error = on_error
        
        self._checkpoint_counter = 0
        self._fetch_count = 0
        self._start_time: Optional[datetime] = None
    
    def seed_from_graph(self, graph_data: Dict) -> None:
        """
        Seed crawler from existing graph data.
        
        Args:
            graph_data: Dict with 'nodes', 'edges', 'metadata' from graph JSON
        """
        # Get seed papers from metadata
        seed_id = graph_data.get("metadata", {}).get("seed_paper")
        if seed_id:
            self.state.queue.append(seed_id)
            self.state.depth_map[seed_id] = 0
            logger.info(f"Seeded with: {seed_id}")
        
        # Add all existing papers as visited
        for node in graph_data.get("nodes", []):
            self.state.visited.add(node["id"])
            self.state.papers[node["id"]] = node
        
        # Set source from metadata
        self.state.source = graph_data.get("metadata", {}).get("source", "openalex")
    
    async def crawl_openalex(self, email: str = "") -> Dict[str, Dict]:
        """
        Execute the crawl using OpenAlex API.
        
        Args:
            email: Email for better rate limits
            
        Returns:
            Dict mapping paper IDs to paper data
        """
        self._start_time = datetime.now()
        self._fetch_count = 0
        
        logger.info("Starting OpenAlex citation crawl...")
        logger.info(f"Config: max_depth={self.config.max_depth}, "
                   f"max_per_depth={self.config.max_papers_per_depth}, "
                   f"refs={self.config.follow_references}, "
                   f"cits={self.config.follow_citations}")
        
        async with OpenAlexClient(email=email or self.config.email) as client:
            while self.state.queue:
                current_id = self.state.queue.popleft()
                
                if current_id in self.state.visited:
                    continue
                
                current_depth = self.state.depth_map.get(current_id, 0)
                
                if current_depth >= self.config.max_depth:
                    logger.debug(f"Skipping {current_id[:30]}... - max depth reached")
                    continue
                
                await asyncio.sleep(self.config.rate_limit_delay)
                
                try:
                    # Normalize ID
                    normalized_id = normalize_openalex_id(current_id)
                    work = await client.get_work(normalized_id)
                    
                    if work:
                        self.state.visited.add(current_id)
                        paper_data = self._work_to_dict(work, current_depth)
                        self.state.papers[current_id] = paper_data
                        self._fetch_count += 1
                        
                        logger.info(f"[Depth {current_depth}] Fetched: {work.title[:50]}...")
                        
                        # Add references (backward citations)
                        if self.config.follow_references:
                            refs = work.referenced_works[:self.config.max_papers_per_depth]
                            for ref_id in refs:
                                if ref_id and ref_id not in self.state.visited and ref_id not in self.state.depth_map:
                                    self.state.queue.append(ref_id)
                                    self.state.depth_map[ref_id] = current_depth + 1
                        
                        # Add citations (forward citations)
                        if self.config.follow_citations:
                            cits = await client.get_cited_by(normalized_id, limit=self.config.max_papers_per_depth)
                            for cit_id in cits[:self.config.max_papers_per_depth]:
                                if cit_id and cit_id not in self.state.visited and cit_id not in self.state.depth_map:
                                    self.state.queue.append(cit_id)
                                    self.state.depth_map[cit_id] = current_depth + 1
                        
                        # Progress
                        if self._fetch_count % 10 == 0:
                            elapsed = (datetime.now() - self._start_time).total_seconds()
                            rate = self._fetch_count / elapsed if elapsed > 0 else 0
                            logger.info(f"Progress: {self._fetch_count} papers, "
                                       f"{self.state.queue_size()} in queue, "
                                       f"{rate:.1f} papers/sec")
                        
                        # Checkpoint
                        self._checkpoint_counter += 1
                        if self._checkpoint_counter >= self.config.checkpoint_interval:
                            await self._save_checkpoint()
                            self._checkpoint_counter = 0
                    else:
                        logger.warning(f"Could not fetch work: {current_id}")
                        self.state.errors[current_id] = "Work not found"
                        
                except Exception as e:
                    error_msg = str(e)
                    self.state.errors[current_id] = error_msg
                    logger.warning(f"Error fetching {current_id[:30]}...: {error_msg}")
                    
                    if self.on_error:
                        self.on_error(current_id, e)
        
        await self._save_checkpoint()
        
        elapsed = (datetime.now() - self._start_time).total_seconds()
        logger.info(f"Crawl complete: {len(self.state.papers)} papers in {elapsed:.1f}s")
        
        return self.state.papers
    
    async def crawl_semantic_scholar(self) -> Dict[str, Paper]:
        """
        Execute the crawl using Semantic Scholar API.
        
        Returns:
            Dict mapping paper IDs to Paper objects
        """
        self._start_time = datetime.now()
        self._fetch_count = 0
        
        logger.info("Starting Semantic Scholar citation crawl...")
        logger.info(f"Config: max_depth={self.config.max_depth}, "
                   f"max_per_depth={self.config.max_papers_per_depth}, "
                   f"refs={self.config.follow_references}, "
                   f"cits={self.config.follow_citations}")
        
        async with SemanticScholarClient() as client:
            while self.state.queue:
                current_id = self.state.queue.popleft()
                
                if current_id in self.state.visited:
                    continue
                
                current_depth = self.state.depth_map.get(current_id, 0)
                
                if current_depth >= self.config.max_depth:
                    logger.debug(f"Skipping {current_id[:20]}... - max depth reached")
                    continue
                
                await asyncio.sleep(self.config.rate_limit_delay)
                
                try:
                    paper = await client.get_paper(current_id)
                    
                    if paper:
                        self.state.visited.add(current_id)
                        self.state.papers[current_id] = self._paper_to_dict(paper, current_depth)
                        self._fetch_count += 1
                        
                        logger.info(f"[Depth {current_depth}] Fetched: {paper.title[:50]}...")
                        
                        # Add references
                        if self.config.follow_references:
                            refs = paper.references[:self.config.max_papers_per_depth]
                            for ref_id in refs:
                                if ref_id and ref_id not in self.state.visited and ref_id not in self.state.depth_map:
                                    self.state.queue.append(ref_id)
                                    self.state.depth_map[ref_id] = current_depth + 1
                        
                        # Add citations
                        if self.config.follow_citations:
                            cits = paper.citations[:self.config.max_papers_per_depth]
                            for cit_id in cits:
                                if cit_id and cit_id not in self.state.visited and cit_id not in self.state.depth_map:
                                    self.state.queue.append(cit_id)
                                    self.state.depth_map[cit_id] = current_depth + 1
                        
                        # Progress
                        if self._fetch_count % 10 == 0:
                            elapsed = (datetime.now() - self._start_time).total_seconds()
                            rate = self._fetch_count / elapsed if elapsed > 0 else 0
                            logger.info(f"Progress: {self._fetch_count} papers, "
                                       f"{self.state.queue_size()} in queue, "
                                       f"{rate:.1f} papers/sec")
                        
                        # Checkpoint
                        self._checkpoint_counter += 1
                        if self._checkpoint_counter >= self.config.checkpoint_interval:
                            await self._save_checkpoint()
                            self._checkpoint_counter = 0
                    else:
                        logger.warning(f"Could not fetch paper: {current_id}")
                        self.state.errors[current_id] = "Paper not found"
                        
                except Exception as e:
                    error_msg = str(e)
                    self.state.errors[current_id] = error_msg
                    logger.warning(f"Error fetching {current_id[:20]}...: {error_msg}")
                    
                    if self.on_error:
                        self.on_error(current_id, e)
        
        await self._save_checkpoint()
        
        elapsed = (datetime.now() - self._start_time).total_seconds()
        logger.info(f"Crawl complete: {len(self.state.papers)} papers in {elapsed:.1f}s")
        
        return {
            pid: self._dict_to_paper(data) 
            for pid, data in self.state.papers.items()
        }
    
    async def crawl(self) -> Dict[str, Dict]:
        """
        Execute the crawl using the configured API.
        
        Returns:
            Dict mapping paper IDs to paper data
        """
        if self.state.source == "openalex":
            return await self.crawl_openalex()
        else:
            return await self.crawl_semantic_scholar()
    
    def _work_to_dict(self, work: Work, depth: int = 0) -> Dict:
        """Convert OpenAlex Work to dict for storage"""
        return {
            "paper_id": work.work_id,
            "title": work.title,
            "authors": work.authors,
            "year": work.year,
            "venue": work.venue,
            "doi": work.doi,
            "abstract": work.abstract,
            "citation_count": work.cited_by_count,
            "reference_count": len(work.referenced_works) if work.referenced_works else 0,
            "references": work.referenced_works,
            "citations": work.cited_by,
            "depth": depth,
            "source": "openalex",
            "fetched_at": datetime.now().isoformat(),
        }
    
    def _paper_to_dict(self, paper: Paper, depth: int = 0) -> Dict:
        """Convert Semantic Scholar Paper to dict for storage"""
        return {
            "paper_id": paper.paper_id,
            "title": paper.title,
            "authors": paper.authors,
            "year": paper.year,
            "venue": paper.venue,
            "doi": paper.doi,
            "abstract": paper.abstract,
            "citation_count": paper.citation_count,
            "reference_count": paper.reference_count,
            "references": paper.references,
            "citations": paper.citations,
            "depth": depth,
            "source": "semantic_scholar",
            "fetched_at": datetime.now().isoformat(),
        }
    
    def _dict_to_paper(self, data: Dict) -> Paper:
        """Convert dict back to Paper"""
        return Paper(
            paper_id=data["paper_id"],
            title=data["title"],
            authors=data["authors"],
            year=data.get("year"),
            venue=data.get("venue"),
            abstract=data.get("abstract"),
            doi=data.get("doi"),
            url="",
            citation_count=data.get("citation_count", 0),
            reference_count=data.get("reference_count", 0),
            references=data.get("references", []),
            citations=data.get("citations", []),
        )
    
    async def _save_checkpoint(self) -> None:
        """Save current state to checkpoint file"""
        if self.config.checkpoint_file == "checkpoint_disabled.json":
            return
            
        try:
            Path(self.config.checkpoint_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(self.state.to_dict(), f, indent=2, ensure_ascii=False)
            logger.debug(f"Checkpoint saved: {self.config.checkpoint_file}")
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
    
    def load_checkpoint(self, filepath: str) -> bool:
        """Load state from checkpoint file"""
        try:
            path = Path(filepath)
            if not path.exists():
                logger.warning(f"Checkpoint file not found: {filepath}")
                return False
            
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.state = CrawlState.from_dict(data)
            self._checkpoint_counter = 0
            
            logger.info(f"Loaded checkpoint: {len(self.state.papers)} papers, "
                       f"{self.state.queue_size()} in queue")
            return True
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get crawl statistics"""
        elapsed = 0
        if self._start_time:
            elapsed = (datetime.now() - self._start_time).total_seconds()
        
        return {
            "total_papers": len(self.state.papers),
            "visited": len(self.state.visited),
            "remaining_in_queue": self.state.queue_size(),
            "errors": len(self.state.errors),
            "max_depth_reached": max(self.state.depth_map.values()) if self.state.depth_map else 0,
            "elapsed_seconds": elapsed,
            "papers_per_second": self._fetch_count / elapsed if elapsed > 0 else 0,
        }


# Convenience function for finding Turing 1936
TURING_1936_OPENALEX = "W2126160338"
TURING_1936_SEMANTIC_SCHOLAR = "4def0e61b7d6b13f6c2e35a5893e5fb6a5e7c6a8"


async def find_turing_paper(client, use_openalex: bool = True) -> Optional[Any]:
    """Find Turing's 1936 paper"""
    if use_openalex:
        work = await client.get_work(TURING_1936_OPENALEX)
        return work
    else:
        paper = await client.get_paper(TURING_1936_SEMANTIC_SCHOLAR)
        return paper


async def main():
    """Demo: Crawl from Turing 1936"""
    config = CrawlConfig(max_depth=2, max_papers_per_depth=10, source="openalex")
    crawler = CitationCrawler(config)
    
    # Seed with Turing 1936
    crawler.state.queue.append(TURING_1936_OPENALEX)
    crawler.state.depth_map[TURING_1936_OPENALEX] = 0
    
    print("Starting crawl from Turing 1936...")
    papers = await crawler.crawl_openalex(email="test@example.com")
    
    print(f"\nCrawl complete!")
    print(f"Total papers: {len(papers)}")
    print(f"Stats: {crawler.get_stats()}")


if __name__ == "__main__":
    asyncio.run(main())