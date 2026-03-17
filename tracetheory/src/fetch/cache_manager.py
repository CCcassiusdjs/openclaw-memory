"""
Cache Manager for TraceTheory

Manages local PDF cache with:
- Metadata tracking (source URL, download date, hash)
- Integrity verification
- Avoids redundant downloads
"""

import json
import hashlib
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import shutil


logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry metadata"""
    paper_id: str
    source_url: str
    download_date: str
    hash: str
    file_size: int = 0
    title: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "CacheEntry":
        return cls(**data)


class CacheManager:
    """
    Manages PDF cache for downloaded papers.
    
    Usage:
        cache = CacheManager(Path("./cache"))
        cache.initialize()
        
        if cache.exists(paper_id):
            path = cache.get_path(paper_id)
        else:
            cache.save_metadata(paper_id, {...})
            cache.get_cache_path(paper_id)  # For saving
    """
    
    METADATA_FILE = "cache_metadata.json"
    PDF_DIR = "pdfs"
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.pdf_dir = self.cache_dir / self.PDF_DIR
        self.metadata_file = self.cache_dir / self.METADATA_FILE
        
        # In-memory metadata cache
        self._metadata: Dict[str, CacheEntry] = {}
    
    def initialize(self) -> None:
        """Initialize cache directories and load metadata"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing metadata
        self._load_metadata()
        
        logger.info(f"Cache initialized at {self.cache_dir}")
    
    def _load_metadata(self) -> None:
        """Load metadata from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._metadata = {
                        k: CacheEntry.from_dict(v) 
                        for k, v in data.items()
                    }
                logger.debug(f"Loaded {len(self._metadata)} cache entries")
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Could not load cache metadata: {e}")
                self._metadata = {}
    
    def _save_metadata(self) -> None:
        """Save metadata to disk"""
        data = {
            k: v.to_dict() 
            for k, v in self._metadata.items()
        }
        
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def exists(self, paper_id: str) -> bool:
        """Check if paper PDF is cached"""
        # Check metadata
        if paper_id not in self._metadata:
            return False
        
        # Verify file exists
        entry = self._metadata[paper_id]
        pdf_path = self.pdf_dir / f"{paper_id}.pdf"
        
        if not pdf_path.exists():
            # File missing - clean up metadata
            logger.warning(f"Cache entry exists but file missing: {paper_id}")
            del self._metadata[paper_id]
            self._save_metadata()
            return False
        
        # Verify integrity
        if not self._verify_integrity(paper_id):
            logger.warning(f"Cache entry failed integrity check: {paper_id}")
            return False
        
        return True
    
    def _verify_integrity(self, paper_id: str) -> bool:
        """Verify file integrity using hash"""
        entry = self._metadata.get(paper_id)
        if not entry:
            return False
        
        pdf_path = self.pdf_dir / f"{paper_id}.pdf"
        if not pdf_path.exists():
            return False
        
        # Compute current hash
        sha256 = hashlib.sha256()
        with open(pdf_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        
        current_hash = sha256.hexdigest()
        
        return current_hash == entry.hash
    
    def get_path(self, paper_id: str) -> Path:
        """Get path to cached PDF (must verify exists first)"""
        return self.pdf_dir / f"{paper_id}.pdf"
    
    def get_cache_path(self, paper_id: str) -> Path:
        """Get path where PDF should be saved"""
        return self.pdf_dir / f"{paper_id}.pdf"
    
    def save_metadata(
        self,
        paper_id: str,
        metadata: Dict[str, Any],
        title: str = None,
    ) -> None:
        """
        Save metadata for a cached PDF.
        
        Args:
            paper_id: Unique paper identifier
            metadata: Dict with source_url, download_date, hash
            title: Optional paper title
        """
        # Compute file hash if file exists
        pdf_path = self.pdf_dir / f"{paper_id}.pdf"
        file_hash = metadata.get("hash", "")
        file_size = 0
        
        if pdf_path.exists() and not file_hash:
            sha256 = hashlib.sha256()
            with open(pdf_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
                file_hash = sha256.hexdigest()
            file_size = pdf_path.stat().st_size
        
        entry = CacheEntry(
            paper_id=paper_id,
            source_url=metadata.get("source_url", ""),
            download_date=metadata.get("download_date", datetime.now().isoformat()),
            hash=file_hash,
            file_size=file_size,
            title=title,
        )
        
        self._metadata[paper_id] = entry
        self._save_metadata()
        
        logger.debug(f"Saved cache entry: {paper_id}")
    
    def get_metadata(self, paper_id: str) -> Optional[CacheEntry]:
        """Get metadata for a cached paper"""
        return self._metadata.get(paper_id)
    
    def remove(self, paper_id: str) -> bool:
        """Remove paper from cache"""
        if paper_id in self._metadata:
            # Remove file
            pdf_path = self.pdf_dir / f"{paper_id}.pdf"
            if pdf_path.exists():
                pdf_path.unlink()
            
            # Remove metadata
            del self._metadata[paper_id]
            self._save_metadata()
            
            logger.info(f"Removed from cache: {paper_id}")
            return True
        
        return False
    
    def clear(self) -> int:
        """Clear entire cache"""
        count = len(self._metadata)
        
        # Remove all files
        if self.pdf_dir.exists():
            shutil.rmtree(self.pdf_dir)
            self.pdf_dir.mkdir(parents=True, exist_ok=True)
        
        # Clear metadata
        self._metadata = {}
        self._save_metadata()
        
        logger.info(f"Cleared {count} cache entries")
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_size = sum(
            entry.file_size 
            for entry in self._metadata.values()
        )
        
        return {
            "total_papers": len(self._metadata),
            "total_size_mb": total_size / (1024 * 1024),
            "cache_dir": str(self.cache_dir),
        }
    
    def list_cached(self) -> list:
        """List all cached paper IDs"""
        return list(self._metadata.keys())
    
    def get_size(self, paper_id: str) -> int:
        """Get file size of cached PDF"""
        entry = self._metadata.get(paper_id)
        if entry:
            return entry.file_size
        return 0


async def main():
    """Demo: Test cache manager"""
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_dir = Path(tmpdir) / "cache"
        cache = CacheManager(cache_dir)
        cache.initialize()
        
        # Save a test file
        test_path = cache.get_cache_path("test_paper_1")
        test_path.write_text("fake pdf content")
        
        # Save metadata
        cache.save_metadata("test_paper_1", {
            "source_url": "https://example.com/paper.pdf",
            "download_date": datetime.now().isoformat(),
        }, "Test Paper")
        
        # Check
        print(f"Exists: {cache.exists('test_paper_1')}")
        print(f"Stats: {cache.get_stats()}")
        
        # Get path
        path = cache.get_path("test_paper_1")
        print(f"Path: {path}")
        
        # List
        print(f"Cached: {cache.list_cached()}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())