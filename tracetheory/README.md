# TraceTheory - Intellectual Archaeology of Computing

A system for tracing the genealogy of computing ideas, starting from Turing's seminal 1936 paper and recursively expanding through citations.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                             │
│  (controls depth, parallelism, cache, state)               │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│  SEARCH   │  │  FETCH    │  │  EXTRACT  │
│  LAYER    │  │  LAYER    │  │  LAYER    │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
      ▼              ▼              ▼
┌───────────────────────────────────────────┐
│  Free APIs + Institutional Access         │
│  - Semantic Scholar (free, 200M+)         │
│  - OpenAlex (free, 250M+)                 │
│  - Crossref (DOI/metadata)                │
│  - DBLP (CS bibliography)                │
│  - arXiv (preprints)                      │
│  - EZProxy PUCRS (full PDFs)             │
└───────────────────────────────────────────┘
                      │
                      ▼
              ┌───────────┐
              │  STORAGE  │
              │  (graph)  │
              └───────────┘
```

## Components

### 1. Search Layer (`src/search/`)
Fetches paper metadata via free APIs:
- `semantic_scholar.py` - Primary API (citations, references)
- `openalex.py` - Fallback/expansion
- `crossref.py` - DOI resolution (TODO)
- `dblp.py` - Computer Science specific (TODO)

### 2. Fetch Layer (`src/fetch/`)
Downloads PDFs using institutional access:
- `ezproxy.py` - PUCRS authentication
- `pucrs_proxy.py` - Proxy management
- `pdf_downloader.py` - Download with retry (TODO)
- `cache_manager.py` - Local PDF cache (TODO)

### 3. Extract Layer (`src/extract/`)
Extracts references from PDFs:
- `ocr.py` - PyMuPDF/tesseract OCR
- `ref_extractor.py` - Bibliography parsing (TODO)
- `grobid_client.py` - Structured extraction (TODO)

### 4. Orchestrator (`src/orchestrator/`)
Controls recursive flow:
- `crawler.py` - BFS/DFS traversal
- `scheduler.py` - Parallelism and rate limits (TODO)
- `state.py` - State persistence (TODO)

### 5. Storage (`src/storage/`)
Stores citation graph:
- `graph.py` - NetworkX/Neo4j interface
- `models.py` - Data schemas
- `export.py` - Export to JSON/GraphML/Cytoscape (TODO)

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp config.example.yaml config.yaml
# Edit config.yaml with PUCRS email/password
```

## Usage

```bash
# Start with Turing 1936
python -m tracetheory --seed "On Computable Numbers, with an Application to the Entscheidungsproblem" --depth 5

# Resume interrupted execution
python -m tracetheory --resume

# Export graph
python -m tracetheory --export graph.json
```

## Data Sources

### Free APIs (no authentication required)
| Source | Type | Coverage | Rate Limit |
|--------|------|----------|------------|
| Semantic Scholar | Metadata + Citations | 200M+ papers | 5000/5min |
| OpenAlex | Metadata + Graph | 250M+ works | 100K/day |
| Crossref | DOI + Metadata | Universal | Generous |
| DBLP | CS Bibliography | ~6M papers | Public |
| arXiv | Preprints | ~2M papers | Public |

### Institutional Access (PUCRS)
- **Proxy**: `https://biblioteca.pucrs.br/recursos-tecnologicos/acesso-remoto/pucrs/`
- **Login**: Academic email `@edu.pucrs.br`
- **Databases**: CAPES Portal (126 databases) + PUCRS subscriptions

## Data Structure

```python
@dataclass
class Paper:
    id: str           # DOI or unique identifier
    title: str
    authors: List[str]
    year: int
    venue: str        # Journal/Conference
    abstract: str
    
    # References (cited_by)
    references: List[str]  # Papers this work cites
    
    # Citations (cites)
    citations: List[str]   # Papers that cite this work
    
    # Source
    source: str      # "semantic_scholar", "openalex", etc.
    pdf_url: Optional[str]
    pdf_local: Optional[str]  # Local path if downloaded
    
    # Metadata
    seed_id: str     # Original seed paper ID
    depth: int       # Depth in graph
    fetched_at: datetime
```

## Current Status

### Working
- OpenAlex API client
- Semantic Scholar API client
- Vintage reference extractor (regex for 1900-1950 papers)
- Citation graph builder
- D3.js visualization
- GROBID container (running)

### In Progress
- CLI orchestration
- Recursive expansion
- PDF download automation

### TODO
- Forward citations integration
- Cache system
- Checkpoint/resume
- Unit tests
- Documentation

## Project Structure

```
tracetheory/
├── config.yaml              # Configuration
├── requirements.txt         # Dependencies
├── README.md               # This file
├── REVIEW.md               # Project review (implementation status)
├── tracetheory/
│   ├── __init__.py
│   └── cli.py              # CLI entry point (TODO)
├── src/
│   ├── search/             # API clients
│   ├── fetch/              # PDF download
│   ├── extract/            # Reference extraction
│   ├── orchestrator/       # Crawler logic
│   └── storage/            # Graph storage
├── scripts/
│   ├── vintage_reference_extractor.py
│   ├── citation_graph.py
│   └── extract_footnotes.py
├── output/
│   ├── index.html          # D3.js visualization
│   ├── citation_graph_full.json
│   └── *.json              # Various exports
└── cache/
    └── W2126160338.pdf     # Cached Turing 1936
```

## See Also

- `REVIEW.md` - Detailed implementation status and action plan