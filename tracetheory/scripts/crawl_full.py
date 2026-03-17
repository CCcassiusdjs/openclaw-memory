#!/usr/bin/env python3
"""
TraceTheory Crawler Completo - OpenAlex + Proxy PUCRS + PDF Download

Integra:
1. OpenAlex API para metadados e grafo de citações
2. Proxy PUCRS para download de PDFs
3. PyMuPDF para extração de referências
"""

import asyncio
import aiohttp
import json
import time
import re
from pathlib import Path
from typing import Dict, Set, List, Optional
from dataclasses import dataclass, field, asdict
from collections import deque
import fitz

# ================== CONFIG ==================

OUTPUT_DIR = Path(__file__).parent.parent / "output"
CACHE_DIR = Path(__file__).parent.parent / "cache"
CHECKPOINT_DIR = Path(__file__).parent.parent / "checkpoints"

for d in [OUTPUT_DIR, CACHE_DIR, CHECKPOINT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

OPENALEX_EMAIL = "cassiojonesdhein@gmail.com"
OPENALEX_URL = "https://api.openalex.org"
REQUEST_DELAY = 0.1

PUCRS_EMAIL = "c.jones@edu.pucrs.br"
PUCRS_PASSWORD = "@CiaoMiau2955"
PUCRS_PROXY = "http://prx.pucrs.br:3128"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

PROXY_DOMAINS = {"springer", "nature", "ieee", "acm", "sciencedirect", "wiley", "jstor"}


def needs_proxy(url: str) -> bool:
    url_lower = url.lower()
    for domain in PROXY_DOMAINS:
        if domain in url_lower:
            return True
    return False


# ================== MODELS ==================

@dataclass
class Paper:
    id: str
    title: str
    authors: List[str]
    year: Optional[int]
    doi: Optional[str]
    citation_count: int
    referenced_works: List[str]
    pdf_url: Optional[str] = None
    pdf_local: Optional[str] = None
    open_access: bool = False
    
    def to_dict(self) -> dict:
        return asdict(self)


# ================== OPENALEX CLIENT ==================

class OpenAlexClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"mailto": OPENALEX_EMAIL, "User-Agent": USER_AGENTS[0]}
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _request(self, url: str, params: dict = None) -> Optional[dict]:
        await asyncio.sleep(REQUEST_DELAY)
        try:
            async with self.session.get(url, params=params) as resp:
                if resp.status == 404:
                    return None
                if resp.status == 429:
                    await asyncio.sleep(5)
                    return await self._request(url, params)
                resp.raise_for_status()
                return await resp.json()
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
            return None
    
    async def get_work(self, work_id: str) -> Optional[Paper]:
        url = f"{OPENALEX_URL}/works/{work_id}"
        data = await self._request(url)
        return self._parse_work(data) if data else None
    
    async def search_work(self, query: str) -> Optional[Paper]:
        url = f"{OPENALEX_URL}/works"
        params = {"search": query, "per_page": 1}
        data = await self._request(url, params)
        if data and data.get("results"):
            return self._parse_work(data["results"][0])
        return None
    
    async def get_citations(self, work_id: str, limit: int = 100) -> List[str]:
        url = f"{OPENALEX_URL}/works"
        params = {"filter": f"cites:{work_id}", "per_page": limit, "sort": "cited_by_count:desc"}
        data = await self._request(url, params)
        if data:
            return [w["id"].replace("https://openalex.org/", "") for w in data.get("results", [])]
        return []
    
    def _parse_work(self, data: dict) -> Paper:
        if not data:
            return None
        work_id = data.get("id", "").replace("https://openalex.org/", "")
        authors = [a.get("author", {}).get("display_name", "?") for a in data.get("authorships", [])[:5]]
        refs = [r.replace("https://openalex.org/", "") for r in data.get("referenced_works", [])]
        pdf_url = None
        oa = data.get("open_access", {})
        if oa.get("is_oa"):
            pdf_url = oa.get("oa_url")
        return Paper(
            id=work_id,
            title=data.get("title", "Unknown"),
            authors=authors,
            year=data.get("publication_year"),
            doi=data.get("doi"),
            citation_count=data.get("cited_by_count", 0),
            referenced_works=refs,
            pdf_url=pdf_url,
            open_access=oa.get("is_oa", False),
        )


# ================== PDF DOWNLOADER ==================

class PDFDownloader:
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        proxy_auth = aiohttp.BasicAuth(PUCRS_EMAIL, PUCRS_PASSWORD)
        self.session = aiohttp.ClientSession(
            proxy=PUCRS_PROXY,
            proxy_auth=proxy_auth,
            timeout=aiohttp.ClientTimeout(total=120),
            headers={"User-Agent": USER_AGENTS[0]}
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def download(self, paper: Paper) -> Optional[str]:
        if not paper.pdf_url:
            return None
        cache_file = self.cache_dir / f"{paper.id}.pdf"
        if cache_file.exists():
            print(f"   📄 PDF em cache: {cache_file.name}")
            return str(cache_file)
        try:
            async with self.session.get(paper.pdf_url) as resp:
                if resp.status != 200:
                    print(f"   ⚠️ PDF indisponível: {resp.status}")
                    return None
                content = await resp.read()
                with open(cache_file, "wb") as f:
                    f.write(content)
                print(f"   ✅ PDF baixado: {len(content):,} bytes")
                return str(cache_file)
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return None


# ================== REFERENCE EXTRACTOR ==================

class ReferenceExtractor:
    def __init__(self):
        self.year_pattern = re.compile(r'\b(19|20)\d{2}\b')
        self.doi_pattern = re.compile(r'10\.\d{4,}/[^\s]+')
    
    def extract_references(self, pdf_path: str) -> List[dict]:
        try:
            doc = fitz.open(pdf_path)
            text = "".join(page.get_text() for page in doc)
            doc.close()
            refs_text = self._find_references_section(text)
            return self._parse_references(refs_text) if refs_text else []
        except Exception as e:
            print(f"   ⚠️ Erro refs: {e}")
            return []
    
    def _find_references_section(self, text: str) -> Optional[str]:
        for pattern in [r'\n\s*References?\s*\n', r'\n\s*Bibliography\s*\n']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return text[match.end():]
        return text[int(len(text) * 0.8):]
    
    def _parse_references(self, text: str) -> List[dict]:
        refs = []
        for ref_text in re.split(r'\n\s*(?:\[\d+\]|\d+\.)\s*', text):
            if len(ref_text) > 20:
                ref = {"raw": ref_text[:200], "confidence": 0.5}
                doi_match = self.doi_pattern.search(ref_text)
                if doi_match:
                    ref["doi"] = doi_match.group(0)
                years = self.year_pattern.findall(ref_text)
                if years:
                    ref["year"] = int(years[0])
                refs.append(ref)
        return refs


# ================== CRAWLER ==================

@dataclass
class CrawlState:
    visited: Set[str] = field(default_factory=set)
    queue: deque = field(default_factory=lambda: deque())
    depth_map: Dict[str, int] = field(default_factory=dict)
    papers: Dict[str, Paper] = field(default_factory=dict)
    edges: List[tuple] = field(default_factory=list)
    downloaded_pdfs: int = 0
    extracted_refs: int = 0
    
    def to_json(self) -> dict:
        return {
            "visited": list(self.visited),
            "queue": list(self.queue),
            "depth_map": self.depth_map,
            "papers": {k: v.to_dict() for k, v in self.papers.items()},
            "edges": list(self.edges),
        }


class TraceTheoryCrawler:
    def __init__(self, max_depth: int = 100, max_per_depth: int = 50, 
                 max_papers: int = 10000, download_pdfs: bool = True):
        self.max_depth = max_depth
        self.max_per_depth = max_per_depth
        self.max_papers = max_papers
        self.download_pdfs = download_pdfs
        self.state = CrawlState()
        self.openalex = OpenAlexClient()
        self.pdf_downloader = PDFDownloader() if download_pdfs else None
        self.ref_extractor = ReferenceExtractor() if download_pdfs else None
    
    async def crawl_from_seed(self, seed_query: str) -> Dict[str, Paper]:
        print(f"🚀 TraceTheory Full Crawler")
        print(f"   Depth: {self.max_depth}, Per-depth: {self.max_per_depth}")
        
        async with self.openalex:
            print(f"🔍 Finding seed: {seed_query}")
            seed = await self.openalex.search_work(seed_query)
            if not seed:
                print("   Trying known ID: W2126160338")
                seed = await self.openalex.get_work("W2126160338")
            
            if not seed:
                print("❌ Seed não encontrado")
                return {}
            
            print(f"✅ Found: {seed.title[:60]}... ({seed.year})")
            print(f"   Citations: {seed.citation_count:,}\n")
            
            self.state.queue.append(seed.id)
            self.state.depth_map[seed.id] = 0
            self.state.papers[seed.id] = seed
            
            if self.pdf_downloader:
                async with self.pdf_downloader:
                    await self._crawl_loop()
            else:
                await self._crawl_loop()
        
        await self._export()
        return self.state.papers
    
    async def _crawl_loop(self):
        while self.state.queue:
            current_id = self.state.queue.popleft()
            if current_id in self.state.visited:
                continue
            
            depth = self.state.depth_map.get(current_id, 0)
            if depth >= self.max_depth:
                continue
            
            print(f"📊 Depth {depth}: {current_id}")
            
            if current_id not in self.state.papers:
                paper = await self.openalex.get_work(current_id)
                if not paper:
                    continue
                self.state.papers[current_id] = paper
            else:
                paper = self.state.papers[current_id]
            
            self.state.visited.add(current_id)
            
            # Download PDF
            if self.pdf_downloader and paper.pdf_url and depth < 1 and self.state.downloaded_pdfs < 20:
                pdf_path = await self.pdf_downloader.download(paper)
                if pdf_path:
                    paper.pdf_local = pdf_path
                    self.state.downloaded_pdfs += 1
                    if self.ref_extractor:
                        refs = self.ref_extractor.extract_references(pdf_path)
                        print(f"   📖 Refs extraídas: {len(refs)}")
                        self.state.extracted_refs += len(refs)
            
            # References
            for ref_id in paper.referenced_works[:self.max_per_depth]:
                if ref_id and ref_id not in self.state.visited:
                    self.state.queue.append(ref_id)
                    self.state.depth_map[ref_id] = depth + 1
                    self.state.edges.append((current_id, ref_id))
            
            # Citations
            if depth < self.max_depth - 1:
                citations = await self.openalex.get_citations(current_id, self.max_per_depth)
                print(f"   Citations: {len(citations)}")
                for cit_id in citations:
                    if cit_id and cit_id not in self.state.visited:
                        self.state.queue.append(cit_id)
                        self.state.depth_map[cit_id] = depth + 1
                        self.state.edges.append((cit_id, current_id))
            
            if len(self.state.visited) % 10 == 0:
                await self._save_checkpoint()
    
    async def _save_checkpoint(self):
        with open(CHECKPOINT_DIR / "state.json", "w") as f:
            json.dump(self.state.to_json(), f, indent=2)
    
    async def _export(self):
        output_file = OUTPUT_DIR / "citation_graph_full.json"
        graph_data = {
            "metadata": {
                "total_papers": len(self.state.papers),
                "total_edges": len(self.state.edges),
                "downloaded_pdfs": self.state.downloaded_pdfs,
                "extracted_refs": self.state.extracted_refs,
            },
            "nodes": [{"id": k, "title": v.title, "year": v.year, "cites": v.citation_count} 
                      for k, v in self.state.papers.items()],
            "edges": [{"source": s, "target": t} for s, t in self.state.edges],
        }
        with open(output_file, "w") as f:
            json.dump(graph_data, f, indent=2)
        print(f"\n✅ Exported: {output_file}")
        print(f"   Papers: {len(self.state.papers)}, Edges: {len(self.state.edges)}")
        print(f"   PDFs: {self.state.downloaded_pdfs}, Refs: {self.state.extracted_refs}")


async def main():
    print("=" * 60)
    print("TraceTheory Full Crawler")
    print("=" * 60)
    
    crawler = TraceTheoryCrawler(
        max_depth=100,      # Quase ilimitado
        max_per_depth=50,   # 50 papers por nível
        max_papers=10000,   # Limite de segurança
        download_pdfs=False  # Desabilita PDFs para velocidade
    )
    papers = await crawler.crawl_from_seed("On Computable Numbers Turing 1936")
    
    print("\n🏆 Top 10:")
    for i, p in enumerate(sorted(papers.values(), key=lambda x: x.citation_count, reverse=True)[:10], 1):
        print(f"{i:2}. {p.title[:50]}... ({p.year}) - {p.citation_count:,}")


if __name__ == "__main__":
    asyncio.run(main())