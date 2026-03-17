"""
PDF OCR and Reference Extraction

Uses PyMuPDF for PDF parsing and regex-based reference extraction.
For better results, GROBID can be used (requires running Docker container).
"""

import fitz  # PyMuPDF
from typing import List, Optional, Tuple
from pathlib import Path
import re
from dataclasses import dataclass


@dataclass
class ExtractedReference:
    """A reference extracted from a PDF"""
    raw_text: str
    title: Optional[str] = None
    authors: List[str] = None
    year: Optional[int] = None
    venue: Optional[str] = None
    doi: Optional[str] = None
    confidence: float = 0.0  # Extraction confidence
    
    def __post_init__(self):
        if self.authors is None:
            self.authors = []


class PDFProcessor:
    """Process PDFs to extract text and references"""
    
    def __init__(self):
        # Common reference patterns
        self.year_pattern = re.compile(r'\b(19|20)\d{2}\b')
        self.doi_pattern = re.compile(r'10\.\d{4,}/[^\s]+')
        self.author_patterns = [
            # "Smith, J." or "Smith, J. K."
            re.compile(r'([A-Z][a-z]+),\s+([A-Z]\.(?:\s+[A-Z]\.)*)'),
            # "J. Smith" or "J. K. Smith"
            re.compile(r'([A-Z]\.(?:\s+[A-Z]\.)*)\s+([A-Z][a-z]+)'),
        ]
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract all text from PDF"""
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
        
        doc.close()
        return text
    
    def extract_text_by_page(self, pdf_path: str) -> List[str]:
        """Extract text page by page"""
        doc = fitz.open(pdf_path)
        pages = []
        
        for page in doc:
            pages.append(page.get_text())
        
        doc.close()
        return pages
    
    def find_references_section(self, text: str) -> Optional[Tuple[int, int]]:
        """
        Find the references/bibliography section in the text.
        
        Returns:
            Tuple of (start_index, end_index) or None if not found
        """
        # Common section headers
        patterns = [
            r'\n\s*References?\s*\n',
            r'\n\s*Bibliography\s*\n',
            r'\n\s*Works\s+Cited\s*\n',
            r'\n\s*Literature\s+Cited\s*\n',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Find start of section
                start = match.end()
                
                # Find end of section (next major section or end of document)
                next_section = re.search(r'\n\s*[A-Z][a-z]+\s*\n', text[start:])
                if next_section:
                    end = start + next_section.start()
                else:
                    end = len(text)
                
                return (start, end)
        
        return None
    
    def parse_references_text(self, text: str) -> List[ExtractedReference]:
        """Parse references from a references section"""
        references = []
        
        # Split by common patterns
        # References are often numbered like [1], 1., (1), etc.
        splits = re.split(r'\n\s*(?:\[\d+\]|\d+\.|\(\d+\))\s*', text)
        
        for ref_text in splits:
            ref_text = ref_text.strip()
            if not ref_text:
                continue
            
            # Try to extract components
            ref = ExtractedReference(raw_text=ref_text)
            
            # Extract DOI
            doi_match = self.doi_pattern.search(ref_text)
            if doi_match:
                ref.doi = doi_match.group(0)
            
            # Extract year
            year_matches = self.year_pattern.findall(ref_text)
            if year_matches:
                # Usually the year is one of the first numbers found
                # and should be a reasonable publication year
                for year_str in year_matches:
                    year = int(year_str)
                    if 1800 <= year <= 2030:  # Reasonable year range
                        ref.year = year
                        break
            
            # Extract title (usually the longest quoted or italicized text)
            # This is a simplification - real extraction needs more sophisticated parsing
            title_match = re.search(r'["\x1c]([^"]+)["\x1d]', ref_text)
            if title_match:
                ref.title = title_match.group(1).strip()
            
            # Authors extraction is complex - requires NLP or GROBID
            # Here we just try simple patterns
            for pattern in self.author_patterns:
                matches = pattern.findall(ref_text)
                if matches:
                    for match in matches:
                        if isinstance(match, tuple):
                            author = ' '.join(match)
                        else:
                            author = match
                        if author and author not in ref.authors:
                            ref.authors.append(author)
                    break
            
            # Set confidence based on how much we extracted
            ref.confidence = (
                0.2 * (1 if ref.title else 0) +
                0.2 * (1 if ref.year else 0) +
                0.2 * (1 if ref.doi else 0) +
                0.2 * (1 if ref.authors else 0) +
                0.2 * (1 if ref.venue else 0)
            )
            
            references.append(ref)
        
        return references
    
    def extract_references_from_pdf(self, pdf_path: str) -> List[ExtractedReference]:
        """
        Extract references from a PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of ExtractedReference objects
        """
        # Extract text
        text = self.extract_text(pdf_path)
        
        # Find references section
        refs_section = self.find_references_section(text)
        
        if refs_section:
            refs_text = text[refs_section[0]:refs_section[1]]
        else:
            # Try last 20% of document
            start = int(len(text) * 0.8)
            refs_text = text[start:]
        
        # Parse references
        return self.parse_references_text(refs_text)
    
    def ocr_page(self, pdf_path: str, page_num: int) -> str:
        """
        OCR a specific page (for scanned PDFs).
        
        Note: Requires Tesseract to be installed.
        For better OCR, consider using pdfplumber or pytesseract directly.
        """
        doc = fitz.open(pdf_path)
        
        if page_num < 0 or page_num >= len(doc):
            raise ValueError(f"Page {page_num} out of range")
        
        page = doc[page_num]
        
        # Get page as image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
        
        # Convert to PIL Image
        # img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # OCR with tesseract (requires pytesseract)
        # import pytesseract
        # text = pytesseract.image_to_string(img)
        
        doc.close()
        
        # For now, just return the extracted text
        return page.get_text()


# GROBID integration (optional)
class GROBIDClient:
    """
    Client for GROBID API (better reference extraction).
    
    GROBID is a machine learning library for extracting, parsing, and
    restructuring raw documents (especially scientific articles).
    
    Requires running GROBID Docker container:
    docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.3
    """
    
    def __init__(self, grobid_url: str = "http://localhost:8070"):
        self.grobid_url = grobid_url
    
    async def process_references(self, pdf_path: str) -> List[ExtractedReference]:
        """Process PDF with GROBID for better reference extraction"""
        # Requires aiohttp and running GROBID container
        # Implementation would POST to /api/processReferences
        raise NotImplementedError("GROBID integration not implemented yet")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        processor = PDFProcessor()
        refs = processor.extract_references_from_pdf(sys.argv[1])
        
        print(f"Found {len(refs)} references:\n")
        for i, ref in enumerate(refs[:10], 1):
            print(f"{i}. {ref.title or 'Unknown title'} ({ref.year or 'n/a'})")
            if ref.authors:
                print(f"   Authors: {', '.join(ref.authors[:3])}")
            if ref.doi:
                print(f"   DOI: {ref.doi}")
            print(f"   Confidence: {ref.confidence:.0%}")
            print()
    else:
        print("Usage: python ocr.py <pdf_path>")