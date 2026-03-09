#!/usr/bin/env python3
"""
Concept Graph Builder - Constructs a navigable concept graph from indexed files.
Scans all QMD paths and creates a graph of concepts with weighted connections.
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Configuration
HOME = Path.home()
WORKSPACE = HOME / ".openclaw" / "workspace"
OUTPUT_DIR = WORKSPACE / "memory"
GRAPH_FILE = OUTPUT_DIR / "concept_graph.json"

# QMD paths to index
QMD_PATHS = [
    {"name": "workspace", "path": HOME / ".openclaw" / "workspace", "pattern": "**/*"},
    {"name": "documents", "path": HOME / "Documents", "pattern": "**/*"},
    {"name": "clionprojects", "path": HOME / "CLionProjects", "pattern": "**/*.{py,js,ts,c,cpp,h,go,rs,md,txt,json,yaml,yml,toml}"},
    {"name": "dataspellprojects", "path": HOME / "DataspellProjects", "pattern": "**/*.{py,ipynb,md,txt,json,yaml,yml}"},
    {"name": "pycharmprojects", "path": HOME / "PycharmProjects", "pattern": "**/*.{py,ipynb,md,txt,json,yaml,yml}"},
    {"name": "arducopter_doxy", "path": HOME / "arducopter_doxy", "pattern": "**/*"},
    {"name": "apps", "path": HOME / "apps", "pattern": "**/*"},
    {"name": "src", "path": HOME / "src", "pattern": "**/*.{py,js,ts,c,cpp,h,go,rs,md,txt,json,yaml,yml}"},
    {"name": "go", "path": HOME / "go", "pattern": "**/*.go"},
    {"name": "openclaw", "path": HOME / "openclaw", "pattern": "**/*"},
    {"name": "openclaw_audio", "path": HOME / "openclaw_audio", "pattern": "**/*"},
    {"name": "st_tools", "path": HOME / "st_tools", "pattern": "**/*"},
    {"name": "zabbix", "path": HOME / "zabbix", "pattern": "**/*"},
    {"name": "groundtruth", "path": HOME / "groundtruth", "pattern": "**/*"},
    {"name": "html", "path": HOME / "html", "pattern": "**/*.{html,css,js}"},
    {"name": "bin", "path": HOME / "bin", "pattern": "**/*"},
    {"name": "build", "path": HOME / "build", "pattern": "**/*.{py,c,cpp,h,md,json,yaml,yml}"}
]

# Concept extraction patterns
CONCEPT_PATTERNS = {
    "class": r"class\s+(\w+)",
    "function": r"def\s+(\w+)\s*\(",
    "import": r"import\s+([\w.]+)",
    "variable": r"(\w+)\s*=\s*[^=]",
    "heading_md": r"^#+\s+(.+)$",
    "title": r"#\s+(.+)$",
    "tag": r"(\w+):\s*",
    "email": r"[\w.-]+@[\w.-]+\.\w+",
    "url": r"https?://[^\s]+",
    "path": r"/[\w/.-]+",
    "date": r"\d{4}-\d{2}-\d{2}",
    "version": r"v?\d+\.\d+\.\d+",
    "error": r"error|Error|ERROR",
    "config": r"config|Config|CONFIG",
}

# Stop words and noise
STOP_WORDS = {"the", "a", "an", "is", "it", "to", "of", "and", "in", "for", "on", "with", "that", "this", "be", "are", "was", "were", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "shall", "can", "need", "dare", "ought", "used", "use", "using", "uses", "get", "set", "let", "put", "take", "make", "go", "come", "see", "know", "think", "want", "give", "say", "tell", "ask", "work", "seem", "feel", "try", "leave", "call"}

# File type weights (importance for concept extraction)
FILE_WEIGHTS = {
    ".md": 1.5,  # Markdown files have high semantic value
    ".py": 1.3,
    ".json": 1.0,
    ".yaml": 1.0,
    ".yml": 1.0,
    ".toml": 1.0,
    ".c": 1.2,
    ".cpp": 1.2,
    ".h": 1.1,
    ".go": 1.2,
    ".rs": 1.2,
    ".js": 1.1,
    ".ts": 1.1,
    ".txt": 0.8,
    "default": 0.5
}

def get_file_weight(filepath):
    """Get weight for a file based on its extension."""
    ext = Path(filepath).suffix.lower()
    return FILE_WEIGHTS.get(ext, FILE_WEIGHTS["default"])

def extract_concepts_from_file(filepath):
    """Extract concepts from a file."""
    concepts = defaultdict(int)
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (IOError, OSError):
        return dict(concepts)
    
    weight = get_file_weight(filepath)
    
    # Extract using patterns
    for concept_type, pattern in CONCEPT_PATTERNS.items():
        matches = re.findall(pattern, content, re.MULTILINE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            # Clean and normalize
            concept = match.strip().lower()
            if concept and concept not in STOP_WORDS and len(concept) > 2:
                concepts[f"{concept_type}:{concept}"] += int(1 * weight)
    
    # Extract word frequency for concept density
    words = re.findall(r'\b[a-zA-Z]{4,}\b', content)
    word_freq = defaultdict(int)
    for word in words:
        word_lower = word.lower()
        if word_lower not in STOP_WORDS:
            word_freq[word_lower] += 1
    
    # Add high-frequency words as concepts
    for word, freq in sorted(word_freq.items(), key=lambda x: -x[1])[:20]:
        if freq > 2:
            concepts[f"keyword:{word}"] += int(freq * weight * 0.5)
    
    return dict(concepts)

def scan_directory(path_config):
    """Scan a directory and extract all concepts."""
    path = path_config["path"]
    pattern = path_config["pattern"]
    
    if not path.exists():
        return {}
    
    file_concepts = {}
    
    # Parse glob pattern
    if pattern == "**/*":
        files = path.rglob("*")
    else:
        # Simple pattern matching
        import fnmatch
        files = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                filepath = Path(root) / filename
                if fnmatch.fnmatch(filepath.name, pattern.replace("**/*", "*")):
                    files.append(filepath)
    
    for filepath in files:
        if filepath.is_file():
            try:
                concepts = extract_concepts_from_file(filepath)
                if concepts:
                    rel_path = str(filepath.relative_to(path))
                    file_concepts[rel_path] = {
                        "concepts": concepts,
                        "weight": get_file_weight(filepath),
                        "path": str(filepath)
                    }
            except Exception:
                continue
    
    return file_concepts

def build_concept_graph(all_file_concepts):
    """Build a graph of concept relationships."""
    graph = {
        "nodes": {},
        "edges": defaultdict(lambda: {"weight": 0, "files": []}),
        "file_index": {}
    }
    
    # Build concept nodes
    for path_config, file_concepts in all_file_concepts.items():
        for filepath, data in file_concepts.items():
            full_path = data["path"]
            concepts = data["concepts"]
            weight = data["weight"]
            
            # Index file
            graph["file_index"][full_path] = {
                "path_config": path_config,
                "relative_path": filepath,
                "concept_count": len(concepts),
                "weight": weight
            }
            
            # Add concept nodes
            for concept, count in concepts.items():
                if concept not in graph["nodes"]:
                    graph["nodes"][concept] = {
                        "count": 0,
                        "files": [],
                        "type": concept.split(":")[0] if ":" in concept else "unknown"
                    }
                graph["nodes"][concept]["count"] += count
                graph["nodes"][concept]["files"].append(full_path)
    
    # Build edges (concept co-occurrence)
    for path_config, file_concepts in all_file_concepts.items():
        for filepath, data in file_concepts.items():
            concepts = list(data["concepts"].keys())
            
            # Create edges between co-occurring concepts
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i+1:]:
                    edge_key = tuple(sorted([concept1, concept2]))
                    graph["edges"][edge_key]["weight"] += 1
                    graph["edges"][edge_key]["files"].append(data["path"])
    
    # Convert edges to regular dict
    graph["edges"] = {f"{k[0]}|||{k[1]}": v for k, v in graph["edges"].items()}
    
    return graph

def calculate_importance_scores(graph):
    """Calculate importance scores for concepts using PageRank-like algorithm."""
    scores = {}
    
    # Simple scoring: sum of edge weights + node frequency
    for concept, node_data in graph["nodes"].items():
        # Base score from frequency
        score = node_data["count"] * 0.3
        
        # Add edge weights
        for edge_key, edge_data in graph["edges"].items():
            if concept in edge_key:
                score += edge_data["weight"] * 0.1
        
        # Boost for having many file associations
        score += len(node_data["files"]) * 0.2
        
        # Boost for specific concept types
        if concept.startswith("class:") or concept.startswith("function:"):
            score *= 1.5
        elif concept.startswith("heading_md:"):
            score *= 1.3
        
        scores[concept] = score
    
    return scores

def generate_navigation_report(graph, scores):
    """Generate a human-readable navigation report."""
    report = []
    report.append("# Concept Navigation Graph")
    report.append(f"\nGenerated: {datetime.now().isoformat()}")
    report.append(f"\n## Statistics")
    report.append(f"- Total concepts: {len(graph['nodes'])}")
    report.append(f"- Total files indexed: {len(graph['file_index'])}")
    report.append(f"- Total edges: {len(graph['edges'])}")
    
    # Top concepts by importance
    report.append("\n## Top Concepts by Importance")
    top_concepts = sorted(scores.items(), key=lambda x: -x[1])[:50]
    for i, (concept, score) in enumerate(top_concepts, 1):
        node = graph["nodes"][concept]
        concept_type = node["type"]
        file_count = len(node["files"])
        report.append(f"{i}. **{concept}** (score: {score:.2f}, files: {file_count})")
    
    # Concepts by type
    report.append("\n## Concepts by Type")
    by_type = defaultdict(list)
    for concept, score in scores.items():
        by_type[graph["nodes"][concept]["type"]].append((concept, score))
    
    for concept_type, concepts in sorted(by_type.items()):
        concepts.sort(key=lambda x: -x[1])
        report.append(f"\n### {concept_type} ({len(concepts)} concepts)")
        for concept, score in concepts[:10]:
            report.append(f"- {concept} ({score:.2f})")
    
    # File clusters (files with many shared concepts)
    report.append("\n## File Clusters")
    file_concept_counts = defaultdict(int)
    for concept, node in graph["nodes"].items():
        for filepath in node["files"]:
            file_concept_counts[filepath] += 1
    
    top_files = sorted(file_concept_counts.items(), key=lambda x: -x[1])[:20]
    for filepath, count in top_files:
        report.append(f"- `{filepath}` ({count} concepts)")
    
    # Related concepts (edges with high weight)
    report.append("\n## Strong Concept Relationships")
    top_edges = sorted(graph["edges"].items(), key=lambda x: -x[1]["weight"])[:30]
    for edge_key, edge_data in top_edges:
        concepts = edge_key.split("|||")
        report.append(f"- **{concepts[0]}** ↔ **{concepts[1]}** (weight: {edge_data['weight']})")
    
    return "\n".join(report)

def main():
    """Main entry point."""
    print("=== Concept Graph Builder ===")
    print(f"Scanning {len(QMD_PATHS)} directories...\n")
    
    # Scan all directories
    all_file_concepts = {}
    for path_config in QMD_PATHS:
        name = path_config["name"]
        print(f"Scanning {name}...")
        file_concepts = scan_directory(path_config)
        all_file_concepts[name] = file_concepts
        print(f"  Found {len(file_concepts)} files with concepts")
    
    # Build graph
    print("\nBuilding concept graph...")
    graph = build_concept_graph(all_file_concepts)
    
    # Calculate importance scores
    print("Calculating importance scores...")
    scores = calculate_importance_scores(graph)
    
    # Add scores to graph
    graph["importance_scores"] = scores
    
    # Generate report
    print("Generating navigation report...")
    report = generate_navigation_report(graph, scores)
    
    # Save graph
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f, indent=2)
    print(f"\nGraph saved to: {GRAPH_FILE}")
    
    # Save report
    report_file = OUTPUT_DIR / "concept_navigation.md"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_file}")
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Total concepts: {len(graph['nodes'])}")
    print(f"Total files indexed: {len(graph['file_index'])}")
    print(f"Total relationships: {len(graph['edges'])}")
    print(f"Top concept: {top_concepts[0][0] if top_concepts else 'none'}")
    
    return graph, scores

if __name__ == "__main__":
    main()