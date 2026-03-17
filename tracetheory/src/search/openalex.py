"""
OpenAlex API Client

API gratuita com 250M+ works, incluindo grafo de citações completo.
Rate limit: 100K requests/day (sem key)
"""

import aiohttp
import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from urllib.parse import quote


@dataclass  
class Work:
    """Work metadata from OpenAlex"""
    work_id: str           # OpenAlex ID (W...)
    doi: Optional[str]
    title: str
    authors: List[str]
    year: Optional[int]
    venue: Optional[str]
    abstract: Optional[str]
    cited_by_count: int
    referenced_works: List[str]  # OpenAlex IDs
    cited_by: List[str]          # OpenAlex IDs
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "Work":
        """Create Work from API response"""
        return cls(
            work_id=data.get("id", ""),
            doi=data.get("doi"),
            title=data.get("title", ""),
            authors=[a.get("author", {}).get("display_name", "") for a in data.get("authorships", [])],
            year=data.get("publication_year"),
            venue=data.get("primary_location", {}).get("source", {}).get("display_name") if data.get("primary_location") else None,
            abstract=data.get("abstract"),
            cited_by_count=data.get("cited_by_count", 0),
            referenced_works=data.get("referenced_works", []),
            cited_by=data.get("cited_by", []),  # Note: requires extra API call
        )


class OpenAlexClient:
    """Client for OpenAlex API"""
    
    BASE_URL = "https://api.openalex.org"
    
    def __init__(self, email: Optional[str] = None):
        # Including email in requests helps with rate limiting
        self.email = email
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        headers = {}
        if self.email:
            headers["mailto"] = self.email
        
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        # Rate limiting via sleep
        await asyncio.sleep(0.1)  # ~10 req/sec
        
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def search_works(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for works by query"""
        params = {
            "search": query,
            "per_page": limit,
            "mailto": self.email
        }
        data = await self._request("works", params)
        return data.get("results", [])
    
    async def get_work(self, work_id: str) -> Optional[Work]:
        """Get work by OpenAlex ID"""
        try:
            data = await self._request(f"works/{work_id}")
            return Work.from_api(data)
        except aiohttp.ClientError:
            return None
    
    async def get_work_by_doi(self, doi: str) -> Optional[Work]:
        """Get work by DOI"""
        try:
            # OpenAlex accepts DOI URLs or bare DOIs
            doi_encoded = quote(doi, safe="")
            data = await self._request(f"works/doi:{doi_encoded}")
            return Work.from_api(data)
        except aiohttp.ClientError:
            return None
    
    async def get_references(self, work_id: str) -> List[str]:
        """Get referenced works (papers this work cites)"""
        work = await self.get_work(work_id)
        return work.referenced_works if work else []
    
    async def get_cited_by(self, work_id: str, limit: int = 200) -> List[str]:
        """Get works that cite this work"""
        params = {
            "filter": f"cites:{work_id}",
            "per_page": limit,
            "mailto": self.email
        }
        data = await self._request("works", params)
        return [w.get("id") for w in data.get("results", [])]


# Turing 1936 OpenAlex ID (approximate - will need to verify)
# W2123065505 is typically Turing's "On Computable Numbers"


async def main():
    """Demo: Search for Turing's paper"""
    async with OpenAlexClient(email="test@example.com") as client:
        # Search for Turing 1936
        results = await client.search_works("On Computable Numbers Turing Entscheidungsproblem", limit=5)
        
        print("Search results:")
        for i, work in enumerate(results, 1):
            print(f"{i}. {work.get('title', 'N/A')} ({work.get('publication_year', 'N/A')})")
            print(f"   ID: {work.get('id')}")
            print(f"   Citations: {work.get('cited_by_count', 0)}")


if __name__ == "__main__":
    asyncio.run(main())