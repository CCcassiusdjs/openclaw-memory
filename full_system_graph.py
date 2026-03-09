#!/usr/bin/env python3
"""
Full System Graph Builder - Creates a complete graph of the entire filesystem.
Every folder, subfolder, and file becomes a node.
Target: 20,000+ nodes with navigable relationships.
"""

import os
import json
import re
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import stat

# Configuration
HOME = Path.home()
WORKSPACE = HOME / ".openclaw" / "workspace"
OUTPUT_DIR = WORKSPACE / "memory"
GRAPH_FILE = OUTPUT_DIR / "system_graph.json"

# Directories to scan (all user directories + key system paths)
SCAN_PATHS = [
    HOME,  # All user files
    Path("/usr/local"),
    Path("/usr/share"),
    Path("/etc"),
    Path("/var/log"),
    Path("/opt"),
]

# Directories to skip (too large or not useful)
SKIP_DIRS = {
    ".cache", ".local", ".npm", "node_modules", "__pycache__", 
    ".git", ".svn", ".hg", ".idea", ".vscode", ".venv", "venv",
    "miniconda3", ".conda", "miniforge3", "SitePackages",
    "site-packages", "dist-packages", ".mypy_cache", ".pytest_cache",
    "build", "dist", "egg-info", ".eggs", ".tox", ".nox",
    "STM32Cube", "STM32CubeMX", ".STM32CubeMX", ".STM32Cube",
    ".cache", ".config", ".local", ".npm-global/lib",
    ".bun", ".rustup", ".cargo", ".gem", ".nvm",
    "lost+found", "proc", "sys", "dev", "run", "tmp",
}

# File extensions to include (prioritize text/code files)
INCLUDE_EXTENSIONS = {
    # Code
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".c", ".cpp", ".h", ".hpp",
    ".java", ".kt", ".swift", ".m", ".mm", ".rb", ".php", ".cs", ".scala",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    # Config
    ".json", ".yaml", ".yml", ".toml", ".ini", ".conf", ".cfg", ".env",
    ".xml", ".html", ".css", ".scss", ".sass", ".less",
    # Docs
    ".md", ".txt", ".rst", ".adoc", ".tex", ".pdf", ".doc", ".docx",
    # Data
    ".csv", ".tsv", ".sql", ".db", ".sqlite",
    # Images (for metadata)
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg",
    # Other
    ".log", ".lock", ".sum", ".mod", ".proto", ".graphql",
}

# Minimum file size to include (skip tiny files)
MIN_FILE_SIZE = 100  # bytes

def get_file_hash(filepath):
    """Get a unique hash for a file."""
    try:
        st = os.stat(filepath)
        return hashlib.md5(f"{filepath}:{st.st_size}:{st.st_mtime}".encode()).hexdigest()[:12]
    except:
        return hashlib.md5(str(filepath).encode()).hexdigest()[:12]

def get_file_metadata(filepath):
    """Get metadata for a file."""
    try:
        st = os.stat(filepath)
        return {
            "size": st.st_size,
            "mtime": st.st_mtime,
            "mode": oct(st.st_mode)[-3:],
            "is_executable": bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)),
        }
    except:
        return {}

def scan_directory_full(path, skip_dirs, include_exts, min_size):
    """Scan a directory recursively and return all nodes and edges."""
    nodes = {}
    edges = []
    file_count = 0
    dir_count = 0
    
    path = Path(path)
    if not path.exists():
        return nodes, edges, 0, 0
    
    for root, dirs, files in os.walk(path, topdown=True):
        # Skip directories in skip list
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        
        root_path = Path(root)
        
        # Add directory node
        try:
            rel_path = root_path.relative_to(path)
            node_id = f"dir:{path.name}/{rel_path}" if str(rel_path) != "." else f"dir:{path.name}"
        except:
            node_id = f"dir:{root}"
        
        nodes[node_id] = {
            "type": "directory",
            "name": root_path.name,
            "path": str(root_path),
            "depth": len(root_path.parts) - len(path.parts),
        }
        dir_count += 1
        
        # Add parent-child edge
        if root_path != path:
            parent_path = root_path.parent
            try:
                parent_rel = parent_path.relative_to(path)
                parent_id = f"dir:{path.name}/{parent_rel}" if str(parent_rel) != "." else f"dir:{path.name}"
            except:
                parent_id = f"dir:{parent_path}"
            edges.append({
                "source": parent_id,
                "target": node_id,
                "type": "contains"
            })
        
        # Process files
        for filename in files:
            filepath = root_path / filename
            ext = filepath.suffix.lower()
            
            # Skip if not in include list and not small
            try:
                size = os.path.getsize(filepath)
                if ext not in include_exts and size < min_size:
                    continue
            except:
                continue
            
            # Add file node
            file_node_id = f"file:{get_file_hash(filepath)}"
            
            # Get metadata
            metadata = get_file_metadata(filepath)
            
            nodes[file_node_id] = {
                "type": "file",
                "name": filename,
                "ext": ext,
                "path": str(filepath),
                "size": metadata.get("size", 0),
                "mtime": metadata.get("mtime", 0),
                "depth": len(root_path.parts) - len(path.parts) + 1,
            }
            file_count += 1
            
            # Add directory-file edge
            edges.append({
                "source": node_id,
                "target": file_node_id,
                "type": "contains"
            })
    
    return nodes, edges, file_count, dir_count

def extract_concepts_from_text(filepath):
    """Extract concepts from text files."""
    concepts = defaultdict(int)
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(10000)  # Read first 10KB only
    except:
        return dict(concepts)
    
    # Extract patterns
    patterns = {
        "function": r'(?:def|function|func|fn)\s+(\w+)',
        "class": r'class\s+(\w+)',
        "import": r'(?:import|from|require|include)\s+([\w.]+)',
        "constant": r'([A-Z][A-Z0-9_]+)\s*=',
        "url": r'https?://[^\s<>"]+',
        "email": r'[\w.-]+@[\w.-]+\.\w+',
        "version": r'v?\d+\.\d+\.\d+',
    }
    
    for concept_type, pattern in patterns.items():
        for match in re.findall(pattern, content):
            if isinstance(match, tuple):
                match = match[0]
            concept = match.strip().lower()
            if len(concept) > 2:
                concepts[f"{concept_type}:{concept}"] += 1
    
    # Extract keywords (high-frequency words)
    words = re.findall(r'\b[a-zA-Z]{4,15}\b', content)
    stop_words = {"this", "that", "these", "those", "with", "from", "have", "been", "were", "they", "their", "what", "when", "where", "which", "while"}
    word_freq = defaultdict(int)
    for word in words:
        w = word.lower()
        if w not in stop_words:
            word_freq[w] += 1
    
    for word, freq in sorted(word_freq.items(), key=lambda x: -x[1])[:10]:
        if freq > 1:
            concepts[f"keyword:{word}"] = freq
    
    return dict(concepts)

def build_concept_edges(nodes):
    """Build edges between files that share concepts."""
    concept_edges = []
    file_concepts = {}
    
    # Extract concepts from all files
    for node_id, node in nodes.items():
        if node.get("type") == "file" and node.get("ext", "") in {".py", ".js", ".ts", ".go", ".rs", ".c", ".cpp", ".h", ".md", ".txt", ".json", ".yaml", ".yml"}:
            concepts = extract_concepts_from_text(node["path"])
            if concepts:
                file_concepts[node_id] = concepts
    
    # Find files with shared concepts
    concept_files = defaultdict(list)
    for node_id, concepts in file_concepts.items():
        for concept in concepts:
            concept_files[concept].append(node_id)
    
    # Create edges for shared concepts
    for concept, files in concept_files.items():
        if len(files) > 1 and len(files) < 100:  # Avoid overly connected nodes
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    concept_edges.append({
                        "source": file1,
                        "target": file2,
                        "type": "shares_concept",
                        "concept": concept
                    })
    
    return concept_edges

def scan_system_parallel():
    """Scan all directories in parallel."""
    print("=== Full System Graph Builder ===")
    print(f"Target: 20,000+ nodes")
    print(f"Scanning directories: {len(SCAN_PATHS)}")
    print()
    
    all_nodes = {}
    all_edges = []
    total_files = 0
    total_dirs = 0
    
    # Scan each path in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {}
        for scan_path in SCAN_PATHS:
            if scan_path.exists():
                future = executor.submit(
                    scan_directory_full,
                    scan_path,
                    SKIP_DIRS,
                    INCLUDE_EXTENSIONS,
                    MIN_FILE_SIZE
                )
                futures[future] = scan_path
        
        for future in as_completed(futures):
            scan_path = futures[future]
            try:
                nodes, edges, files, dirs = future.result()
                all_nodes.update(nodes)
                all_edges.extend(edges)
                total_files += files
                total_dirs += dirs
                print(f"  ✓ {scan_path.name}: {dirs} dirs, {files} files")
            except Exception as e:
                print(f"  ✗ {scan_path.name}: {e}")
    
    print(f"\nTotal: {total_dirs} directories, {total_files} files")
    print(f"Total nodes: {len(all_nodes)}")
    
    # Build concept edges
    print("\nBuilding concept relationships...")
    concept_edges = build_concept_edges(all_nodes)
    all_edges.extend(concept_edges)
    print(f"Concept edges: {len(concept_edges)}")
    
    # Create summary statistics
    by_type = defaultdict(int)
    by_ext = defaultdict(int)
    by_depth = defaultdict(int)
    
    for node_id, node in all_nodes.items():
        by_type[node.get("type", "unknown")] += 1
        if "ext" in node:
            by_ext[node["ext"]] += 1
        by_depth[node.get("depth", 0)] += 1
    
    # Create the final graph
    graph = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "total_nodes": len(all_nodes),
            "total_edges": len(all_edges),
            "scan_paths": [str(p) for p in SCAN_PATHS],
            "skip_dirs": list(SKIP_DIRS),
        },
        "statistics": {
            "by_type": dict(by_type),
            "by_ext": dict(sorted(by_ext.items(), key=lambda x: -x[1])[:50]),
            "by_depth": dict(by_depth),
        },
        "nodes": all_nodes,
        "edges": all_edges,
    }
    
    return graph

def generate_html_visualization(graph):
    """Generate an HTML visualization of the graph."""
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>System Graph Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { margin: 0; background: #0a0a0a; }
        svg { width: 100vw; height: 100vh; }
        .node { cursor: pointer; }
        .node circle { stroke: #333; stroke-width: 1px; }
        .node.directory circle { fill: #4a9eff; }
        .node.file circle { fill: #50c878; }
        .node text { fill: #ccc; font-size: 10px; }
        .link { stroke: #333; stroke-opacity: 0.3; }
        .link.contains { stroke: #4a9eff; }
        .link.shares_concept { stroke: #ff6b6b; stroke-dasharray: 2,2; }
        .tooltip { position: absolute; background: #1a1a1a; color: #fff; padding: 10px; border-radius: 5px; font-size: 12px; pointer-events: none; }
        #search { position: fixed; top: 10px; left: 10px; width: 300px; padding: 8px; background: #1a1a1a; color: #fff; border: 1px solid #333; }
        #stats { position: fixed; top: 10px; right: 10px; background: #1a1a1a; color: #fff; padding: 10px; font-size: 12px; }
    </style>
</head>
<body>
    <input type="text" id="search" placeholder="Search nodes...">
    <div id="stats"></div>
    <svg></svg>
    <script>
        const graph = ''' + json.dumps({"nodes": [{"id": k, **v} for k, v in list(graph["nodes"].items())[:5000]], "links": graph["edges"][:10000]}) + ''';
        
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const svg = d3.select("svg");
        const g = svg.append("g");
        
        const zoom = d3.zoom().on("zoom", (event) => g.attr("transform", event.transform));
        svg.call(zoom);
        
        const simulation = d3.forceSimulation(graph.nodes)
            .force("link", d3.forceLink(graph.links).id(d => d.id).distance(50))
            .force("charge", d3.forceManyBody().strength(-100))
            .force("center", d3.forceCenter(width/2, height/2));
        
        const link = g.append("g")
            .selectAll("line")
            .data(graph.links)
            .enter().append("line")
            .attr("class", d => "link " + d.type);
        
        const node = g.append("g")
            .selectAll(".node")
            .data(graph.nodes)
            .enter().append("g")
            .attr("class", d => "node " + d.type)
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        node.append("circle").attr("r", 5);
        
        node.append("title").text(d => d.name + "\\n" + d.path);
        
        simulation.on("tick", () => {
            link.attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            node.attr("transform", d => "translate(" + d.x + "," + d.y + ")");
        });
        
        function dragstarted(event, d) { if (!event.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }
        function dragged(event, d) { d.fx = event.x; d.fy = d.y; }
        function dragended(event, d) { if (!event.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }
        
        document.getElementById("stats").innerHTML = "Nodes: " + graph.nodes.length + "<br>Edges: " + graph.links.length;
    </script>
</body>
</html>'''
    
    return html

def main():
    """Main entry point."""
    print("=" * 60)
    print("FULL SYSTEM GRAPH BUILDER")
    print("Target: 20,000+ nodes")
    print("=" * 60)
    print()
    
    # Scan system
    graph = scan_system_parallel()
    
    # Check if we hit target
    total_nodes = graph["metadata"]["total_nodes"]
    print(f"\n{'='*60}")
    print(f"FINAL COUNT: {total_nodes} nodes")
    if total_nodes >= 20000:
        print("✅ TARGET ACHIEVED!")
    else:
        print(f"⚠️ Need {20000 - total_nodes} more nodes")
    print(f"{'='*60}")
    
    # Save graph
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save full JSON
    print("\nSaving full graph...")
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f, indent=2)
    print(f"Saved to: {GRAPH_FILE}")
    
    # Save compressed version for faster loading
    compressed_file = OUTPUT_DIR / "system_graph_compressed.json"
    compressed = {
        "metadata": graph["metadata"],
        "statistics": graph["statistics"],
        "nodes": {k: {"type": v["type"], "name": v["name"], "path": v["path"]} for k, v in graph["nodes"].items()},
        "edges": [{"s": e["source"], "t": e["target"], "type": e["type"]} for e in graph["edges"]]
    }
    with open(compressed_file, 'w') as f:
        json.dump(compressed, f)
    print(f"Compressed: {compressed_file}")
    
    # Generate HTML visualization
    print("\nGenerating HTML visualization...")
    html = generate_html_visualization(graph)
    html_file = OUTPUT_DIR / "system_graph.html"
    with open(html_file, 'w') as f:
        f.write(html)
    print(f"HTML: {html_file}")
    
    # Generate summary report
    report_file = OUTPUT_DIR / "system_graph_report.md"
    report = f"""# System Graph Report

## Statistics

- **Total Nodes**: {total_nodes:,}
- **Total Edges**: {len(graph['edges']):,}

### By Type
"""
    for t, count in sorted(graph["statistics"]["by_type"].items()):
        report += f"- {t}: {count:,}\n"
    
    report += "\n### Top Extensions\n"
    for ext, count in graph["statistics"]["by_ext"][:20]:
        report += f"- {ext or 'no ext'}: {count:,}\n"
    
    report += "\n### By Depth\n"
    for depth, count in sorted(graph["statistics"]["by_depth"].items())[:10]:
        report += f"- Depth {depth}: {count:,}\n"
    
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"Report: {report_file}")
    
    return graph

if __name__ == "__main__":
    main()