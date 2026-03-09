#!/usr/bin/env python3
"""
Bio-inspired 3D filesystem graph visualization.
Neural/mycelial aesthetic with organic clustering.
"""

import json
import os
import hashlib
from collections import defaultdict
from pathlib import Path
import math

# Bio-inspired color palettes
COLORS = {
    # Directory colors (warm, organic)
    'directory': {
        'root': '#ff6b35',      # Orange (heart)
        'home': '#f7c59f',      # Peach
        'project': '#efa8b8',   # Rose
        'system': '#c8b6ff',   # Lavender
        'default': '#e8d5b7',   # Bone
    },
    # File type colors (cool, neural)
    'code': '#00ff87',         # Neon green (neurons)
    'config': '#00b4d8',       # Cyan (synapses)
    'doc': '#ffd166',          # Gold (dendrites)
    'data': '#ef476f',         # Pink (axons)
    'media': '#9b5de5',        # Purple (nuclei)
    'default': '#a8dadc',      # Pale cyan
}

def get_file_type_color(filename):
    """Get color based on file type."""
    ext = Path(filename).suffix.lower()
    
    # Code files
    if ext in {'.py', '.js', '.ts', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.kt', '.swift'}:
        return COLORS['code']
    # Config files
    if ext in {'.json', '.yaml', '.yml', '.toml', '.xml', '.ini', '.conf', '.cfg'}:
        return COLORS['config']
    # Documentation
    if ext in {'.md', '.txt', '.rst', '.pdf', '.doc', '.docx'}:
        return COLORS['doc']
    # Data files
    if ext in {'.csv', '.sql', '.db', '.sqlite', '.parquet', '.pkl'}:
        return COLORS['data']
    # Media files
    if ext in {'.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mp3', '.wav', '.ogg'}:
        return COLORS['media']
    
    return COLORS['default']

def get_directory_color(path_parts):
    """Get directory color based on type."""
    if not path_parts:
        return COLORS['directory']['root']
    
    first = path_parts[0].lower()
    
    if first in {'home', 'users', 'usr'}:
        return COLORS['directory']['home']
    if first in {'projects', 'src', 'code', 'repos'}:
        return COLORS['directory']['project']
    if first in {'etc', 'var', 'opt', 'usr'}:
        return COLORS['directory']['system']
    
    return COLORS['directory']['default']

def hash_to_float(s, seed=0):
    """Convert string to deterministic float 0-1."""
    h = hashlib.md5(f"{s}{seed}".encode()).hexdigest()
    return int(h[:8], 16) / 0xffffffff

def spherical_position(index, total, radius=1.0, seed=0):
    """Generate spherical distribution with randomness."""
    # Golden angle for even distribution
    phi = math.pi * (3 - math.sqrt(5))
    
    y = 1 - (index / (total - 1)) * 2 if total > 1 else 0
    radius_at_y = math.sqrt(1 - y * y)
    theta = phi * index
    
    # Add randomness
    noise = hash_to_float(f"pos_{index}_{seed}", seed)
    theta += noise * 0.5
    
    return {
        'x': radius * radius_at_y * math.cos(theta),
        'y': radius * y,
        'z': radius * radius_at_y * math.sin(theta),
    }

def build_bio_graph(graph_json_path, output_path, max_nodes=20000):
    """Build bio-inspired 3D visualization from graph JSON."""
    
    import random
    
    print(f"Loading graph from {graph_json_path}...")
    
    with open(graph_json_path, 'r') as f:
        data = json.load(f)
    
    # Handle both array and dict formats for nodes
    nodes_data = data.get('nodes', {})
    edges_data = data.get('edges', [])
    
    # Convert dict format to list
    if isinstance(nodes_data, dict):
        nodes_list = []
        for node_id, node_info in nodes_data.items():
            node_info['id'] = node_id
            nodes_list.append(node_info)
        nodes = nodes_list
    else:
        nodes = list(nodes_data)
    
    # Handle both array and dict formats for edges
    if isinstance(edges_data, dict):
        edges_list = []
        for edge_id, edge_info in edges_data.items():
            edge_info['id'] = edge_id
            edges_list.append(edge_info)
        edges = edges_list
    else:
        edges = list(edges_data)
    
    print(f"Found {len(nodes):,} nodes, {len(edges):,} edges")
    
    # Sample nodes if too many
    if len(nodes) > max_nodes:
        print(f"Sampling to {max_nodes:,} nodes...")
        # Prioritize directories and important files
        dirs = [n for n in nodes if n.get('type') == 'directory']
        files = [n for n in nodes if n.get('type') == 'file']
        
        # Take all directories (up to limit)
        sample_dirs = dirs[:int(max_nodes * 0.3)]
        
        # Sample files weighted by size
        sample_files = random.sample(files, min(len(files), max_nodes - len(sample_dirs)))
        
        nodes = sample_dirs + sample_files
        print(f"Sampled: {len(sample_dirs):,} directories, {len(sample_files):,} files")
    
    # Build node index
    node_index = {n['id']: i for i, n in enumerate(nodes)}
    
    # Calculate positions using force-directed in 3D
    print("Calculating 3D positions...")
    
    # Group by directory for clustering
    dir_groups = defaultdict(list)
    for node in nodes:
        path = node.get('path', '')
        parts = path.split('/')
        parent = '/'.join(parts[:3]) if len(parts) > 3 else path
        dir_groups[parent].append(node)
    
    # Assign positions
    positions = {}
    total_groups = len(dir_groups)
    
    for gi, (group_path, group_nodes) in enumerate(dir_groups.items()):
        # Cluster center
        center = spherical_position(gi, total_groups, radius=10.0, seed=gi)
        
        # Nodes within cluster
        for ni, node in enumerate(group_nodes):
            offset = spherical_position(ni, len(group_nodes), radius=0.5, seed=hash(node['id']))
            positions[node['id']] = {
                'x': center['x'] + offset['x'] * 0.5,
                'y': center['y'] + offset['y'] * 0.5,
                'z': center['z'] + offset['z'] * 0.5,
            }
    
    # Filter edges to only include sampled nodes (use 's' and 't' keys)
    valid_ids = set(node_index.keys())
    filtered_edges = []
    for e in edges:
        src = e.get('s', e.get('source', ''))
        tgt = e.get('t', e.get('target', ''))
        if src in valid_ids and tgt in valid_ids:
            filtered_edges.append({'source': src, 'target': tgt})
    
    # Limit edges
    max_edges = max_nodes * 3
    if len(filtered_edges) > max_edges:
        print(f"Limiting edges to {max_edges:,}...")
        filtered_edges = filtered_edges[:max_edges]
    
    print(f"Final: {len(nodes):,} nodes, {len(filtered_edges):,} edges")
    
    # Build HTML
    html = build_html(nodes, filtered_edges, positions)
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Written to {output_path}")
    return output_path

def build_html(nodes, edges, positions):
    """Build Three.js HTML visualization."""
    
    # Node data
    nodes_json = []
    for node in nodes:
        pos = positions.get(node['id'], {'x': 0, 'y': 0, 'z': 0})
        path = node.get('path', node['id'])
        name = path.split('/')[-1] if '/' in path else path
        
        node_type = 'directory' if node.get('type') == 'directory' else 'file'
        
        if node_type == 'directory':
            # Directory color based on depth
            depth = path.count('/')
            if depth <= 1:
                color = COLORS['directory']['root']
            elif 'home' in path.lower():
                color = COLORS['directory']['home']
            elif any(p in path.lower() for p in ['project', 'src', 'code']):
                color = COLORS['directory']['project']
            else:
                color = COLORS['directory']['default']
        else:
            color = get_file_type_color(path)
        
        nodes_json.append({
            'id': node['id'],
            'name': name,
            'path': path,
            'type': node_type,
            'color': color,
            'size': 2 if node_type == 'directory' else 1,
            'x': pos['x'],
            'y': pos['y'],
            'z': pos['z'],
        })
    
    edges_json = [{'source': e['source'], 'target': e['target']} for e in edges]
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Bio-Inspired Filesystem Graph</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ 
            background: #0a0a0f; 
            overflow: hidden;
            font-family: 'JetBrains Mono', monospace;
        }}
        #container {{ width: 100vw; height: 100vh; }}
        #info {{
            position: absolute;
            top: 20px;
            left: 20px;
            color: #e0e0e0;
            background: rgba(0,0,0,0.7);
            padding: 15px 20px;
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.3);
            max-width: 350px;
        }}
        #info h1 {{
            color: #ff6b35;
            font-size: 18px;
            margin-bottom: 10px;
        }}
        #stats {{
            font-size: 12px;
            color: #888;
            margin-bottom: 15px;
        }}
        #legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 11px;
        }}
        .legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        #tooltip {{
            position: absolute;
            display: none;
            background: rgba(0,0,0,0.9);
            color: #fff;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #ff6b35;
            font-size: 12px;
            max-width: 400px;
            pointer-events: none;
            z-index: 1000;
        }}
        #tooltip .path {{
            color: #00ff87;
            font-size: 10px;
            word-break: break-all;
        }}
        #controls {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            display: flex;
            gap: 10px;
        }}
        .btn {{
            background: rgba(255,107,53,0.2);
            border: 1px solid #ff6b35;
            color: #ff6b35;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
            font-size: 12px;
            transition: all 0.3s;
        }}
        .btn:hover {{
            background: #ff6b35;
            color: #000;
        }}
        #search {{
            position: absolute;
            top: 20px;
            right: 20px;
        }}
        #search input {{
            background: rgba(0,0,0,0.7);
            border: 1px solid rgba(255,107,53,0.5);
            color: #fff;
            padding: 8px 15px;
            border-radius: 5px;
            width: 250px;
            font-family: inherit;
        }}
        #search input:focus {{
            outline: none;
            border-color: #ff6b35;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div id="info">
        <h1>🧠 Bio Filesystem Graph</h1>
        <div id="stats">
            Nodes: {len(nodes):,} | Edges: {len(edges):,}
        </div>
        <div id="legend">
            <div class="legend-item"><div class="legend-dot" style="background:#00ff87"></div>Code</div>
            <div class="legend-item"><div class="legend-dot" style="background:#00b4d8"></div>Config</div>
            <div class="legend-item"><div class="legend-dot" style="background:#ffd166"></div>Docs</div>
            <div class="legend-item"><div class="legend-dot" style="background:#ef476f"></div>Data</div>
            <div class="legend-item"><div class="legend-dot" style="background:#9b5de5"></div>Media</div>
            <div class="legend-item"><div class="legend-dot" style="background:#ff6b35"></div>Dirs</div>
        </div>
        <div style="font-size: 11px; color: #666;">
            Drag to rotate • Scroll to zoom<br>
            Click node for details
        </div>
    </div>
    
    <div id="search">
        <input type="text" id="searchInput" placeholder="Search files/directories...">
    </div>
    
    <div id="tooltip">
        <div class="name"></div>
        <div class="path"></div>
    </div>
    
    <div id="controls">
        <button class="btn" onclick="resetCamera()">Reset View</button>
        <button class="btn" onclick="toggleRotation()">Auto Rotate</button>
        <button class="btn" onclick="togglePulse()">Pulse</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Data
        const nodes = {json.dumps(nodes_json)};
        const edges = {json.dumps(edges_json)};
        
        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0f);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 20;
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Node objects
        const nodeGroup = new THREE.Group();
        scene.add(nodeGroup);
        
        const nodeMeshes = {{}};
        const nodeGeometry = new THREE.SphereGeometry(0.15, 8, 8);
        
        nodes.forEach(node => {{
            const color = new THREE.Color(node.color);
            const material = new THREE.MeshBasicMaterial({{ 
                color: color,
                transparent: true,
                opacity: 0.9
            }});
            const mesh = new THREE.Mesh(nodeGeometry, material);
            mesh.position.set(node.x, node.y, node.z);
            mesh.userData = node;
            mesh.scale.setScalar(node.size);
            nodeGroup.add(mesh);
            nodeMeshes[node.id] = mesh;
        }});
        
        // Edge lines (neural connections)
        const edgeGeometry = new THREE.BufferGeometry();
        const edgePositions = [];
        const edgeColors = [];
        
        edges.forEach(edge => {{
            const source = nodeMeshes[edge.source];
            const target = nodeMeshes[edge.target];
            if (source && target) {{
                edgePositions.push(
                    source.position.x, source.position.y, source.position.z,
                    target.position.x, target.position.y, target.position.z
                );
                // Gradient color
                const srcColor = new THREE.Color(source.userData.color);
                const tgtColor = new THREE.Color(target.userData.color);
                edgeColors.push(srcColor.r, srcColor.g, srcColor.b);
                edgeColors.push(tgtColor.r, tgtColor.g, tgtColor.b);
            }}
        }});
        
        edgeGeometry.setAttribute('position', new THREE.Float32BufferAttribute(edgePositions, 3));
        edgeGeometry.setAttribute('color', new THREE.Float32BufferAttribute(edgeColors, 3));
        
        const edgeMaterial = new THREE.LineBasicMaterial({{ 
            vertexColors: true,
            transparent: true,
            opacity: 0.15
        }});
        const edgeLines = new THREE.LineSegments(edgeGeometry, edgeMaterial);
        scene.add(edgeLines);
        
        // Ambient particles (background neurons)
        const particleCount = 500;
        const particleGeometry = new THREE.BufferGeometry();
        const particlePositions = [];
        
        for (let i = 0; i < particleCount; i++) {{
            particlePositions.push(
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 40,
                (Math.random() - 0.5) * 40
            );
        }}
        
        particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(particlePositions, 3));
        const particleMaterial = new THREE.PointsMaterial({{
            color: 0xff6b35,
            size: 0.05,
            transparent: true,
            opacity: 0.3
        }});
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        
        // Controls
        let isDragging = false;
        let previousMousePosition = {{ x: 0, y: 0 }};
        let autoRotate = true;
        let pulse = true;
        
        renderer.domElement.addEventListener('mousedown', (e) => {{
            isDragging = true;
            previousMousePosition = {{ x: e.clientX, y: e.clientY }};
        }});
        
        renderer.domElement.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const deltaX = e.clientX - previousMousePosition.x;
                const deltaY = e.clientY - previousMousePosition.y;
                nodeGroup.rotation.y += deltaX * 0.005;
                nodeGroup.rotation.x += deltaY * 0.005;
                previousMousePosition = {{ x: e.clientX, y: e.clientY }};
            }}
            
            // Tooltip
            updateTooltip(e);
        }});
        
        renderer.domElement.addEventListener('mouseup', () => isDragging = false);
        renderer.domElement.addEventListener('mouseleave', () => isDragging = false);
        
        renderer.domElement.addEventListener('wheel', (e) => {{
            camera.position.z += e.deltaY * 0.02;
            camera.position.z = Math.max(5, Math.min(50, camera.position.z));
        }});
        
        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            Object.values(nodeMeshes).forEach(mesh => {{
                const node = mesh.userData;
                const match = !query || node.name.toLowerCase().includes(query) || 
                              node.path.toLowerCase().includes(query);
                mesh.material.opacity = match ? 0.9 : 0.1;
                mesh.scale.setScalar(match ? node.size * 1.5 : node.size * 0.5);
            }});
        }});
        
        // Tooltip update
        function updateTooltip(e) {{
            // Raycaster for node selection
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2(
                (e.clientX / window.innerWidth) * 2 - 1,
                -(e.clientY / window.innerHeight) * 2 + 1
            );
            raycaster.setFromCamera(mouse, camera);
            
            const intersects = raycaster.intersectObjects(Object.values(nodeMeshes));
            const tooltip = document.getElementById('tooltip');
            
            if (intersects.length > 0) {{
                const node = intersects[0].object.userData;
                tooltip.style.display = 'block';
                tooltip.style.left = e.clientX + 15 + 'px';
                tooltip.style.top = e.clientY + 15 + 'px';
                tooltip.querySelector('.name').textContent = node.name;
                tooltip.querySelector('.path').textContent = node.path;
            }} else {{
                tooltip.style.display = 'none';
            }}
        }}
        
        // Controls
        function resetCamera() {{
            camera.position.set(0, 0, 20);
            nodeGroup.rotation.set(0, 0, 0);
        }}
        
        function toggleRotation() {{
            autoRotate = !autoRotate;
        }}
        
        function togglePulse() {{
            pulse = !pulse;
        }}
        
        // Animation
        let time = 0;
        function animate() {{
            requestAnimationFrame(animate);
            time += 0.01;
            
            if (autoRotate) {{
                nodeGroup.rotation.y += 0.001;
            }}
            
            if (pulse) {{
                // Breathing animation
                const breathe = Math.sin(time) * 0.1 + 1;
                particles.rotation.y += 0.0005;
                particles.rotation.x += 0.0002;
            }}
            
            renderer.render(scene, camera);
        }}
        
        animate();
        
        // Resize
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>'''
    
    return html

if __name__ == '__main__':
    import sys
    
    input_path = sys.argv[1] if len(sys.argv) > 1 else '/home/csilva/.openclaw/workspace/memory/system_graph.json'
    output_path = sys.argv[2] if len(sys.argv) > 2 else '/home/csilva/.openclaw/workspace/memory/bio_graph_3d.html'
    
    build_bio_graph(input_path, output_path)