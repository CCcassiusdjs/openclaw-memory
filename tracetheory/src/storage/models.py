"""
Data models for TraceTheory
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Institution:
    """Academic institution"""
    name: str
    country: Optional[str] = None
    type: Optional[str] = None  # "university", "research_institute", "company"


@dataclass
class Author:
    """Paper author"""
    name: str
    affiliations: List[Institution] = field(default_factory=list)
    orcid: Optional[str] = None
    semantic_scholar_id: Optional[str] = None
    openalex_id: Optional[str] = None


@dataclass
class Venue:
    """Publication venue (journal, conference, etc.)"""
    name: str
    type: str  # "journal", "conference", "book", "preprint"
    publisher: Optional[str] = None
    issn: Optional[str] = None
    isbn: Optional[str] = None


@dataclass
class Reference:
    """A reference in a paper's bibliography"""
    raw_text: str                    # As it appears in the paper
    parsed_title: Optional[str] = None
    parsed_authors: List[str] = field(default_factory=list)
    parsed_year: Optional[int] = None
    parsed_venue: Optional[str] = None
    doi: Optional[str] = None
    matched_paper_id: Optional[str] = None  # If matched to known paper


@dataclass
class PaperMetadata:
    """Complete paper metadata"""
    # Identifiers
    id: str                          # Internal ID
    doi: Optional[str] = None
    semantic_scholar_id: Optional[str] = None
    openalex_id: Optional[str] = None
    arxiv_id: Optional[str] = None
    pmid: Optional[str] = None      # PubMed ID
    
    # Basic info
    title: str
    authors: List[Author] = field(default_factory=list)
    year: Optional[int] = None
    venue: Optional[Venue] = None
    
    # Content
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    
    # Citation counts
    citation_count: int = 0
    reference_count: int = 0
    
    # Links
    references: List[str] = field(default_factory=list)  # Paper IDs this cites
    citations: List[str] = field(default_factory=list)     # Paper IDs that cite this
    
    # PDF
    pdf_url: Optional[str] = None
    pdf_local_path: Optional[str] = None
    
    # Crawl metadata
    depth: int = 0
    seed_id: Optional[str] = None
    source: str = "unknown"          # "semantic_scholar", "openalex", "crossref", etc.
    fetched_at: Optional[datetime] = None
    
    # Quality
    is_seed: bool = False
    is_key_paper: bool = False       # Manually marked as important