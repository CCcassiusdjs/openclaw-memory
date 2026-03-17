"""
Semantic Scholar API Client

API gratuita com 200M+ papers, citações e referências.
Rate limit: 100 req/5min (sem key), 5000 req/5min (com key)
"""

import aiohttp
import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote


@dataclass
class Paper:
    """Paper metadata from Semantic Scholar"""
    paper_id: str
    title: str
    authors: List[str]
    year: Optional[int]
    venue: Optional[str]
    abstract: Optional[str]
    doi: Optional[str]
    url: str
    citation_count: int
    reference_count: int
    references: List[str]  # IDs of referenced papers
    citations: List[str]   # IDs of citing papers
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Paper":
        """Create Paper from API response"""
        return cls(
            paper_id=data.get("paperId", ""),
            title=data.get("title", ""),
            authors=[a.get("name", "") for a in data.get("authors", [])],
            year=data.get("year"),
            venue=data.get("venue"),
            abstract=data.get("abstract"),
            doi=data.get("doi"),
            url=data.get("url", ""),
            citation_count=data.get("citationCount", 0),
            reference_count=data.get("referenceCount", 0),
            references=[r.get("paperId", "") for r in data.get("references", []) if r.get("paperId")],
            citations=[c.get("paperId", "") for c in data.get("citations", []) if c.get("paperId")],
        )


class SemanticScholarClient:
    """Client for Semantic Scholar Academic Graph API"""
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Rate limits (per 5 minutes)
        if api_key:
            self.rate_limit = 5000
        else:
            self.rate_limit = 100
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"api_key": self.api_key} if self.api_key else {}
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make rate-limited API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Simple rate limiting via sleep
        await asyncio.sleep(0.05)  # ~20 req/sec max
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def search_paper(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for papers by query"""
        params = {
            "query": query,
            "limit": limit,
            "fields": "paperId,title,authors,year,venue,abstract,doi,url,citationCount,referenceCount"
        }
        data = await self._request("paper/search", params)
        return data.get("data", [])
    
    async def get_paper(self, paper_id: str) -> Optional[Paper]:
        """Get paper by ID with references and citations"""
        params = {
            "fields": "paperId,title,authors,year,venue,abstract,doi,url,citationCount,referenceCount,references.paperId,citations.paperId"
        }
        try:
            data = await self._request(f"paper/{paper_id}", params)
            return Paper.from_api(data)
        except aiohttp.ClientError:
            return None
    
    async def get_references(self, paper_id: str, limit: int = 1000) -> List[str]:
        """Get all references for a paper"""
        params = {
            "fields": "paperId",
            "limit": limit
        }
        try:
            data = await self._request(f"paper/{paper_id}/references", params)
            return [r.get("paperId") for r in data.get("data", []) if r.get("paperId")]
        except aiohttp.ClientError:
            return []
    
    async def get_citations(self, paper_id: str, limit: int = 1000) -> List[str]:
        """Get all citations for a paper"""
        params = {
            "fields": "paperId",
            "limit": limit
        }
        try:
            data = await self._request(f"paper/{paper_id}/citations", params)
            return [c.get("paperId") for c in data.get("data", []) if c.get("paperId")]
        except aiohttp.ClientError:
            return []
    
    async def get_paper_by_doi(self, doi: str) -> Optional[Paper]:
        """Get paper by DOI"""
        params = {
            "fields": "paperId,title,authors,year,venue,abstract,doi,url,citationCount,referenceCount,references.paperId,citations.paperId"
        }
        try:
            # URL encode the DOI for the API
            encoded_doi = quote(doi, safe="")
            data = await self._request(f"paper/DOI:{encoded_doi}", params)
            return Paper.from_api(data)
        except aiohttp.ClientError as e:
            # Try alternative: search by DOI
            try:
                results = await self.search_paper(f'doi:"{doi}"', limit=1)
                if results:
                    return await self.get_paper(results[0].get("paperId"))
            except:
                pass
            return None


# Turing 1936 Paper ID in Semantic Scholar
TURING_1936_ID = "4def0e61b7d6b13f6c2e35a5893e5fb6a5e7c6a8"  # Approximate - will need to verify


async def main():
    """Demo: Search for Turing's paper"""
    async with SemanticScholarClient() as client:
        # Search for Turing 1936
        results = await client.search_paper("On Computable Numbers Turing 1936", limit=5)
        
        print("Search results:")
        for i, paper in enumerate(results, 1):
            print(f"{i}. {paper.get('title', 'N/A')} ({paper.get('year', 'N/A')})")
            print(f"   ID: {paper.get('paperId')}")
            print(f"   Citations: {paper.get('citationCount', 0)}")


if __name__ == "__main__":
    asyncio.run(main())