# TraceTheory - Project Review

**Date:** 2026-03-16
**Status:** In Development

---

## 1. Project Overview

TraceTheory is a system for tracing the intellectual genealogy of computing, starting from Turing's seminal 1936 paper and recursively expanding through citations.

### 1.1 Objective
Given a seed paper (e.g., Turing 1936), recursively extract:
- **Backward citations**: References cited by the paper
- **Forward citations**: Papers that cite the seed paper
- Build a citation graph for visualization and analysis

### 1.2 Target Use Case
Analyze PDFs from papers before 1936 (or any historical papers) to find cited references in:
- Footnotes
- Inline text mentions
- Bibliography sections

---

## 2. Current Implementation Status

### 2.1 Completed Components

| Component | Location | Status | Description |
|-----------|----------|--------|-------------|
| **OpenAlex Client** | `src/search/openalex.py` | ✅ Working | API client for OpenAlex (250M+ works) |
| **Semantic Scholar Client** | `src/search/semantic_scholar.py` | ✅ Working | API client for S2 (200M+ papers) |
| **Crawler Orchestrator** | `src/orchestrator/crawler.py` | ✅ Working | BFS/DFS traversal of citation graph |
| **PDF OCR** | `src/extract/ocr.py` | ✅ Working | PyMuPDF text extraction |
| **EZProxy Client** | `src/fetch/ezproxy.py` | ✅ Implemented | PUCRS institutional access |
| **Vintage Reference Extractor** | `scripts/vintage_reference_extractor.py` | ✅ Working | Regex-based extraction for old papers |
| **Citation Graph Builder** | `scripts/citation_graph.py` | ✅ Working | Builds graph from API data |
| **Visualization (D3.js)** | `output/index.html` | ✅ Working | Force-directed graph visualization |
| **GROBID Integration** | Docker container | ✅ Working | Structured reference extraction |

### 2.2 Output Files Generated

| File | Size | Description |
|------|------|-------------|
| `W2126160338.pdf` | 2.2 MB | Turing 1936 PDF (cached) |
| `turing_1936_text.txt` | 70 KB | Extracted text from PDF |
| `turing_footnotes.json` | 1.9 KB | Extracted footnotes |
| `turing_references_complete.json` | 2.6 KB | Complete references with metadata |
| `vintage_references.json` | 2.3 KB | 8 references from regex extraction |
| `citation_graph_full.json` | 10.8 KB | Graph with 9 nodes, 8 edges |
| `visualization_graph.json` | 20 KB | D3.js visualization format |
| `index.html` | 22 KB | Interactive visualization |

---

## 3. What Works

### 3.1 API Integration
- OpenAlex API: Fully functional
- Semantic Scholar API: Implemented
- Rate limiting handled (100K/day for OpenAlex)
- Async HTTP with aiohttp

### 3.2 Reference Extraction from Vintage Papers
GROBID failed on Turing 1936 because:
- No formal "References" section in 1936 papers
- References embedded in footnotes and inline text

**Solution implemented:**
- `vintage_reference_extractor.py` - Custom regex patterns for 1900-1950 papers
- Detects: footnote markers (f, X, *), author mentions, year patterns
- Successfully extracted 8 references from Turing 1936

### 3.3 Graph Construction
- Nodes: Papers with metadata (title, authors, year, DOI)
- Edges: Citation relationships
- Export formats: JSON, BibTeX

### 3.4 Visualization
- D3.js force-directed graph
- Color-coded node types
- Interactive tooltips
- Sidebar with paper details

---

## 4. What's Missing

### 4.1 Critical Missing Features

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| **Recursive Expansion** | HIGH | Medium | Expand backward citations recursively (currently only 1 level) |
| **Forward Citations** | HIGH | Low | Fetch papers that cite Turing (API works, not integrated) |
| **PDF Download Automation** | HIGH | Medium | Automatically download PDFs for backward citations |
| **Correction Detection** | MEDIUM | Low | Auto-detect papers with "Correction" in title |
| **Translation Detection** | MEDIUM | Low | Auto-detect translations (e.g., German → English) |
| **Cache System** | MEDIUM | Medium | Avoid re-fetching same paper from APIs |
| **Progress Persistence** | MEDIUM | Low | Resume interrupted crawl |

### 4.2 Missing Components

| Component | Status | Location | Description |
|-----------|--------|----------|-------------|
| `src/search/crossref.py` | ❌ Missing | To create | DOI resolution and metadata |
| `src/search/dblp.py` | ❌ Missing | To create | CS bibliography database |
| `src/search/arxiv.py` | ❌ Missing | To create | Preprint server |
| `src/fetch/pdf_downloader.py` | ❌ Missing | To create | Download PDFs with retry |
| `src/fetch/cache_manager.py` | ❌ Missing | To create | Local PDF cache |
| `src/storage/export.py` | ❌ Missing | To create | GraphML/GML export for Gephi |
| `src/orchestrator/scheduler.py` | ❌ Missing | To create | Parallel execution |
| `src/orchestrator/state.py` | ❌ Missing | To create | Checkpoint/Resume |

### 4.3 Integration Gaps

1. **Crawler ↔ Extraction**: Crawler fetches metadata but doesn't trigger PDF download
2. **Extraction ↔ Storage**: Extracted references not stored in graph format
3. **EZProxy ↔ PDF Download**: Authentication works but not used for automated downloads
4. **GROBID ↔ Pipeline**: GROBID container running but not integrated in workflow

---

## 5. Architecture Review

### 5.1 Current Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  scripts/ (one-off scripts, not integrated)                 │
│  ├── vintage_reference_extractor.py                        │
│  ├── citation_graph.py                                     │
│  └── extract_footnotes.py                                  │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  src/ (module structure, partially implemented)             │
│  ├── search/                                               │
│  │   ├── openalex.py ✅                                    │
│  │   └── semantic_scholar.py ✅                            │
│  ├── fetch/                                                │
│  │   ├── ezproxy.py ✅                                     │
│  │   └── pucrs_proxy.py ✅                                 │
│  ├── extract/                                              │
│  │   └── ocr.py ✅                                          │
│  ├── orchestrator/                                         │
│  │   └── crawler.py ✅ (not integrated)                     │
│  └── storage/                                              │
│      ├── graph.py ✅                                        │
│      └── models.py ✅                                       │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Missing Pipeline Integration

**Current state:** Scripts run independently with manual data passing
**Needed:** CLI that orchestrates the full pipeline

```python
# Proposed CLI interface
$ tracetheory seed --doi "10.1112/plms/s2-42.1.230"
$ tracetheory expand --depth 3 --direction backward
$ tracetheory fetch-pdfs --use-proxy
$ tracetheory extract-references
$ tracetheory build-graph
$ tracetheory export --format graphml
$ tracetheory visualize --port 8000
```

---

## 6. Technical Debt

### 6.1 Code Quality Issues

1. **Language mix**: README.md in Portuguese, code comments in English
2. **Duplicate code**: Similar API clients in `openalex.py` and `semantic_scholar.py`
3. **No tests**: No unit tests for any module
4. **Hardcoded paths**: Some scripts have hardcoded paths

### 6.2 Missing Configuration

1. **No `requirements.txt`**: Dependencies not documented
2. **No `setup.py`**: Package not installable
3. **No logging**: Debug output via `print()` statements

### 6.3 Documentation Gaps

1. **API docs**: No docstrings for many functions
2. **Usage examples**: Only basic demo code
3. **Error handling**: Minimal error handling in API clients

---

## 7. Prioritized Action Plan

### Phase 1: Core Pipeline (Priority: HIGH)

| Task | Effort | Files |
|------|--------|-------|
| Create unified CLI (`tracetheory/cli.py`) | Medium | `tracetheory/cli.py` |
| Integrate recursive expansion | Medium | `src/orchestrator/crawler.py` |
| Add forward citations fetching | Low | `src/orchestrator/crawler.py` |
| Create requirements.txt | Low | `requirements.txt` |
| Add logging | Low | All files |

### Phase 2: PDF Pipeline (Priority: MEDIUM)

| Task | Effort | Files |
|------|--------|-------|
| Create PDF downloader | Medium | `src/fetch/pdf_downloader.py` |
| Integrate EZProxy authentication | Medium | `src/fetch/ezproxy.py` |
| Cache management | Low | `src/fetch/cache_manager.py` |
| GROBID integration in pipeline | Low | `src/extract/grobid_client.py` |

### Phase 3: Export & Visualization (Priority: MEDIUM)

| Task | Effort | Files |
|------|--------|-------|
| GraphML export | Low | `src/storage/export.py` |
| Cytoscape.js alternative viz | Medium | `output/cytoscape.html` |
| Summary statistics | Low | `src/storage/stats.py` |

### Phase 4: Polish (Priority: LOW)

| Task | Effort | Files |
|------|--------|-------|
| Unit tests | Medium | `tests/` |
| Error handling | Medium | All files |
| Documentation | Medium | `docs/` |
| Type hints | Low | All Python files |

---

## 8. Recommended Next Steps

### 8.1 Immediate (Today)

1. **Create `requirements.txt`** - Document dependencies
2. **Integrate recursive expansion** - Make crawler actually recurse
3. **Add forward citations** - One-line change to `follow_citations=True`
4. **Create simple CLI** - At least `seed` and `expand` commands

### 8.2 This Week

1. **PDF download pipeline** - Download PDFs for all nodes
2. **GROBID integration** - Use GROBID for modern papers, vintage extractor for old ones
3. **Cache system** - Avoid re-fetching papers
4. **GraphML export** - Enable Gephi import

### 8.3 Next Sprint

1. **Full integration test** - Run end-to-end on Turing 1936
2. **Add more seed papers** - Gödel 1931, Church 1936, etc.
3. **Visualization improvements** - Better interactivity
4. **Documentation** - Usage guide and API docs

---

## 9. File Locations

### 9.1 Project Root
```
/home/csilva/.openclaw/workspace/tracetheory/
```

### 9.2 Key Files

| File | Purpose |
|------|---------|
| `config.yaml` | Configuration (PUCRS credentials, API keys) |
| `README.md` | Project documentation (in Portuguese) |
| `requirements.txt` | ❌ MISSING - needs creation |
| `setup.py` | ❌ MISSING - needs creation |
| `tracetheory/cli.py` | ❌ EXISTS but empty - needs implementation |

### 9.3 Output Directory
```
/home/csilva/.openclaw/workspace/tracetheory/output/
```

### 9.4 Cache Directory
```
/home/csilva/.openclaw/workspace/tracetheory/cache/
└── W2126160338.pdf  (Turing 1936)
```

---

## 10. Configuration

### 10.1 PUCRS Credentials (in config.yaml)
```yaml
institution:
  name: "PUCRS"
  proxy_url: "https://biblioteca.pucrs.br/recursos-tecnologicos/acesso-remoto/pucrs/"
  login:
    email: "c.jones@edu.pucrs.br"
    password: "@CiaoMiau2955"
```

### 10.2 API Configuration
```yaml
apis:
  semantic_scholar:
    base_url: "https://api.semanticscholar.org"
    rate_limit:
      requests_per_5_minutes: 100
  
  openalex:
    base_url: "https://api.openalex.org"
    rate_limit:
      requests_per_day: 100000
```

---

## 11. Summary

**What works:**
- API clients (OpenAlex, Semantic Scholar)
- Vintage reference extraction (regex-based for 1900-1950 papers)
- Basic citation graph building
- D3.js visualization
- GROBID container running

**What's missing:**
- CLI orchestration
- Recursive expansion pipeline
- PDF download automation
- Forward citations integration
- Cache and checkpoint systems
- Tests and documentation

**Estimated effort to complete core pipeline:**
- Phase 1 (CLI + recursion): 4-6 hours
- Phase 2 (PDF pipeline): 6-8 hours
- Phase 3 (Export): 2-3 hours

**Total: ~12-17 hours to complete MVP**