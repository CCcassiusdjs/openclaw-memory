"""
PDF Downloader for TraceTheory

Downloads PDFs from URLs with:
- EZProxy support for institutional access
- Retry logic with exponential backoff
- Progress tracking
- Rate limiting
"""

import asyncio
import hashlib
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse
import aiohttp
from dataclasses import dataclass
from datetime import datetime

from .cache_manager import CacheManager


logger = logging.getLogger(__name__)


@dataclass
class PDFDownloadResult:
    """Result of a PDF download attempt"""
    paper_id: str
    success: bool
    local_path: Optional[str] = None
    error: Optional[str] = None
    cached: bool = False


class PDFDownloader:
    """
    Downloads PDFs with retry logic and proxy support.
    
    Usage:
        downloader = PDFDownloader(config, cache_manager)
        result = await downloader.download(paper_id, pdf_url)
    """
    
    # Common publisher PDF URL patterns
    PDF_PATTERNS = [
        "pdf",
        "/download",
        "/fulltext",
        "/article",
    ]
    
    def __init__(
        self,
        config: Dict[str, Any],
        cache_manager: CacheManager,
        use_proxy: bool = False,
        max_workers: int = 3,
        timeout: int = 120,
    ):
        self.config = config
        self.cache = cache_manager
        self.use_proxy = use_proxy
        self.max_workers = max_workers
        self.timeout = timeout
        
        # Rate limiting
        self._request_semaphore = asyncio.Semaphore(max_workers)
        self._last_request_time = 0
        self._min_request_interval = 1.0  # seconds between requests
        
        # Session
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Statistics
        self.stats = {
            "downloaded": 0,
            "cached": 0,
            "failed": 0,
            "retries": 0,
        }
    
    async def __aenter__(self):
        # Set up session
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        headers = {
            "User-Agent": "TraceTheory/1.0 (Academic PDF Fetcher; mailto: tracetheory@example.com)"
        }
        
        self._session = aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
            connector=aiohttp.TCPConnector(limit=self.max_workers),
        )
        
        return self
    
    async def __aexit__(self, *args):
        if self._session:
            await self._session.close()
    
    async def _rate_limit(self):
        """Apply rate limiting between requests"""
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        
        if elapsed < self._min_request_interval:
            await asyncio.sleep(self._min_request_interval - elapsed)
        
        self._last_request_time = asyncio.get_event_loop().time()
    
    def _get_proxy_url(self, url: str) -> str:
        """Convert URL to proxied version if needed"""
        if not self.use_proxy:
            return url
        
        institution = self.config.get("institution", {})
        proxy_config = institution.get("proxy_url", "")
        
        if not proxy_config:
            logger.warning("Proxy enabled but no proxy_url in config")
            return url
        
        parsed = urlparse(url)
        
        # Check if already proxied
        if "proxy" in parsed.netloc or "ezproxy" in parsed.netloc:
            return url
        
        # Use EZProxy URL prefix format
        # Format: https://login.ezproxy.institution.edu/login?url=https://original-url
        return f"{proxy_config}login?url={url}"
    
    async def _download_with_retry(
        self,
        url: str,
        output_path: Path,
        max_retries: int = 3,
    ) -> bool:
        """
        Download with exponential backoff retry.
        
        Args:
            url: URL to download from
            output_path: Where to save the file
            max_retries: Maximum retry attempts
        
        Returns:
            True if download successful
        """
        base_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                await self._rate_limit()
                
                async with self._session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Verify it's a PDF
                        content_type = response.headers.get("Content-Type", "")
                        if "pdf" not in content_type.lower() and not url.lower().endswith(".pdf"):
                            # Check content header
                            if content[:4] != b"%PDF":
                                logger.warning(f"Response doesn't appear to be PDF: {content_type}")
                                if attempt < max_retries - 1:
                                    continue
                                return False
                        
                        # Save file
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        output_path.write_bytes(content)
                        
                        logger.info(f"Downloaded: {output_path.name}")
                        return True
                    
                    elif response.status == 429:
                        # Rate limited - wait longer
                        retry_after = int(response.headers.get("Retry-After", base_delay * 2))
                        logger.warning(f"Rate limited, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    elif response.status in [401, 403]:
                        # Auth required - try proxy if not already
                        if not self.use_proxy:
                            logger.warning(f"Authentication required, trying proxy")
                            return await self._download_with_retry(
                                self._get_proxy_url(url),
                                output_path,
                                max_retries - attempt - 1,
                            )
                        return False
                    
                    else:
                        logger.warning(f"HTTP {response.status} for {url}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}")
                self.stats["retries"] += 1
                
            except aiohttp.ClientError as e:
                logger.warning(f"Download error: {e}")
                self.stats["retries"] += 1
            
            # Exponential backoff
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.debug(f"Retrying in {delay}s...")
                await asyncio.sleep(delay)
        
        return False
    
    async def download(
        self,
        paper_id: str,
        pdf_url: str,
        title: str = None,
    ) -> PDFDownloadResult:
        """
        Download PDF for a paper.
        
        Args:
            paper_id: Unique identifier for the paper
            pdf_url: URL of the PDF
            title: Optional title for logging
        
        Returns:
            PDFDownloadResult with success status and local path
        """
        # Check cache first
        if self.cache.exists(paper_id):
            cached_path = self.cache.get_path(paper_id)
            self.stats["cached"] += 1
            return PDFDownloadResult(
                paper_id=paper_id,
                success=True,
                local_path=str(cached_path),
                cached=True,
            )
        
        # Download
        try:
            output_path = self.cache.get_cache_path(paper_id)
            
            # Use proxy if enabled
            url = self._get_proxy_url(pdf_url) if self.use_proxy else pdf_url
            
            success = await self._download_with_retry(url, output_path)
            
            if success:
                # Update cache metadata
                self.cache.save_metadata(paper_id, {
                    "source_url": pdf_url,
                    "download_date": datetime.now().isoformat(),
                    "hash": self._compute_hash(output_path),
                })
                
                self.stats["downloaded"] += 1
                
                return PDFDownloadResult(
                    paper_id=paper_id,
                    success=True,
                    local_path=str(output_path),
                )
            else:
                self.stats["failed"] += 1
                return PDFDownloadResult(
                    paper_id=paper_id,
                    success=False,
                    error="Download failed after retries",
                )
                
        except Exception as e:
            self.stats["failed"] += 1
            logger.error(f"Download error for {paper_id}: {e}")
            return PDFDownloadResult(
                paper_id=paper_id,
                success=False,
                error=str(e),
            )
    
    async def download_batch(
        self,
        papers: List[Dict[str, str]],
    ) -> List[PDFDownloadResult]:
        """
        Download multiple PDFs in parallel.
        
        Args:
            papers: List of dicts with paper_id, pdf_url, (optional) title
        
        Returns:
            List of PDFDownloadResult
        """
        tasks = [
            self.download(
                p["paper_id"],
                p["pdf_url"],
                p.get("title"),
            )
            for p in papers
        ]
        
        return await asyncio.gather(*tasks)
    
    def _compute_hash(self, filepath: Path) -> str:
        """Compute SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def get_stats(self) -> Dict[str, int]:
        """Get download statistics"""
        return self.stats.copy()


async def main():
    """Demo: Test PDF downloader"""
    from .cache_manager import CacheManager
    
    config = {
        "institution": {
            "proxy_url": "https://biblioteca.pucrs.br/recursos-tecnologicos/acesso-remoto/pucrs/",
            "login": {
                "email": "test@edu.pucrs.br",
                "password": "test",
            }
        }
    }
    
    cache = CacheManager(Path("/tmp/tracetheory_cache"))
    cache.initialize()
    
    async with PDFDownloader(config, cache, use_proxy=False) as downloader:
        # Test download (will fail without valid URL)
        result = await downloader(
            "test_paper",
            "https://arxiv.org/pdf/2301.00001.pdf",
            "Test Paper"
        )
        
        print(f"Result: {result}")
        print(f"Stats: {downloader.get_stats()}")


if __name__ == "__main__":
    asyncio.run(main())