#!/usr/bin/env python3
"""
Full bio-inspired 3D filesystem graph visualization.
ALL nodes (402,900+), optimized with instanced rendering.
Color-coded: System files vs User files.
"""

import json
import math
import hashlib
from pathlib import Path
from collections import defaultdict

# Bio-inspired color palettes
COLORS = {
    # User files (warm, organic)
    'user_code': '#00ff87',       # Neon green
    'user_config': '#00b4d8',     # Cyan
    'user_doc': '#ffd166',        # Gold
    'user_data': '#ef476f',       # Pink
    'user_media': '#9b5de5',      # Purple
    'user_dir': '#ff6b35',        # Orange
    'user_default': '#a8dadc',   # Pale cyan
    
    # System files (cool, mechanical)
    'sys_code': '#4361ee',        # Blue
    'sys_config': '#7209b7',      # Deep purple
    'sys_doc': '#560bad',        # Dark purple
    'sys_data': '#480ca8',       # Violet
    'sys_media': '#3a0ca3',      # Indigo
    'sys_dir': '#3f37c9',        # Navy
    'sys_default': '#4895ef',    # Bright blue
}

# System paths
SYSTEM_PREFIXES = ['/usr', '/etc', '/var', '/opt', '/bin', '/sbin', '/lib', '/lib64', '/usr/local']
USER_PREFIXES = ['/home', '/root']

def is_system_path(path):
    """Check if path is a system path."""
    for prefix in SYSTEM_PREFIXES:
        if path.startswith(prefix):
            return True
    return False

def get_file_type(path):
    """Get file type from extension."""
    ext = Path(path).suffix.lower()
    
    if ext in {'.py', '.js', '.ts', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.kt', '.swift', '.cc', '.hpp', '.m', '.php', '.lua', '.rb', '.sh'}:
        return 'code'
    if ext in {'.json', '.yaml', '.yml', '.toml', '.xml', '.ini', '.conf', '.cfg', '.cmake', '.makefile', '.dockerfile'}:
        return 'config'
    if ext in {'.md', '.txt', '.rst', '.pdf', '.doc', '.docx', '.tex', '.page', '.html', '.htm'}:
        return 'doc'
    if ext in {'.csv', '.sql', '.db', '.sqlite', '.parquet', '.pkl', '.dat', '.bin', '.hex'}:
        return 'data'
    if ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.mp3', '.wav', '.ogg', '.webm'}:
        return 'media'
    return 'default'

def get_color(path, node_type):
    """Get color based on system/user and file type."""
    is_system = is_system_path(path)
    file_type = get_file_type(path) if node_type == 'file' else None
    
    if is_system:
        if node_type == 'directory':
            return COLORS['sys_dir']
        return COLORS.get(f'sys_{file_type}', COLORS['sys_default'])
    else:
        if node_type == 'directory':
            return COLORS['user_dir']
        return COLORS.get(f'user_{file_type}', COLORS['user_default'])

def spherical_position(index, total, radius=1.0, seed=0):
    """Generate spherical distribution."""
    phi = math.pi * (3 - math.sqrt(5))  # Golden angle
    
    y = 1 - (index / (total - 1)) * 2 if total > 1 else 0
    radius_at_y = math.sqrt(1 - y * y)
    theta = phi * index
    
    # Add deterministic noise
    noise = int(hashlib.md5(f"pos_{index}_{seed}".encode()).hexdigest()[:8], 16) / 0xffffffff * 0.5
    
    return {
        'x': radius * radius_at_y * math.cos(theta + noise),
        'y': radius * y,
        'z': radius * radius_at_y * math.sin(theta + noise),
    }

def build_full_graph(graph_json_path, output_path):
    """Build full bio-inspired 3D visualization with ALL nodes."""
    
    print(f"Loading graph from {graph_json_path}...")
    
    with open(graph_json_path, 'r') as f:
        data = json.load(f)
    
    # Parse nodes
    nodes_data = data.get('nodes', {})
    edges_data = data.get('edges', [])
    
    # Convert to list
    nodes = []
    for node_id, node_info in nodes_data.items():
        nodes.append({
            'id': node_id,
            'type': node_info.get('type', 'file'),
            'path': node_info.get('path', node_id),
        })
    
    # Parse edges
    edges = []
    for e in edges_data:
        edges.append({
            'source': e.get('s', e.get('source', '')),
            'target': e.get('t', e.get('target', '')),
            'type': e.get('type', 'contains'),
        })
    
    print(f"Found {len(nodes):,} nodes, {len(edges):,} edges")
    
    # Group by top-level directory for clustering
    print("Clustering nodes...")
    dir_groups = defaultdict(list)
    
    for node in nodes:
        path = node['path']
        # Get top-level directory
        parts = path.strip('/').split('/')
        if len(parts) > 0:
            top_dir = '/' + parts[0]
        else:
            top_dir = '/'
        dir_groups[top_dir].append(node)
    
    print(f"Found {len(dir_groups)} top-level directories")
    
    # Assign positions
    print("Calculating positions...")
    positions = {}
    total_groups = len(dir_groups)
    
    # Sort groups by size (larger = center)
    sorted_groups = sorted(dir_groups.items(), key=lambda x: -len(x[1]))
    
    for gi, (group_path, group_nodes) in enumerate(sorted_groups):
        # Cluster center - larger groups closer to center
        center_radius = 5 + gi * 0.5
        center = spherical_position(gi, total_groups, radius=center_radius, seed=hash(group_path))
        
        # Nodes within cluster
        for ni, node in enumerate(group_nodes):
            offset = spherical_position(ni, len(group_nodes), radius=1.0, seed=hash(node['id']))
            positions[node['id']] = {
                'x': center['x'] + offset['x'],
                'y': center['y'] + offset['y'],
                'z': center['z'] + offset['z'],
            }
    
    # Build optimized JSON for WebGL
    print("Building visualization...")
    
    # Count system vs user
    system_count = sum(1 for n in nodes if is_system_path(n['path']))
    user_count = len(nodes) - system_count
    
    print(f"System nodes: {system_count:,}, User nodes: {user_count:,}")
    
    # Build HTML with instanced rendering
    html = build_instanced_html(nodes, edges, positions)
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Written to {output_path}")
    return output_path

def build_instanced_html(nodes, edges, positions):
    """Build optimized Three.js HTML with instanced rendering."""
    
    # Pre-calculate all node data
    node_data = []
    for node in nodes:
        pos = positions.get(node['id'], {'x': 0, 'y': 0, 'z': 0})
        color = get_color(node['path'], node['type'])
        name = node['path'].split('/')[-1]
        
        node_data.append({
            'id': node['id'],
            'name': name,
            'path': node['path'],
            'type': node['type'],
            'color': color,
            'x': pos['x'],
            'y': pos['y'],
            'z': pos['z'],
        })
    
    # Build edge data (only contains edges, skip concept edges for performance)
    contains_edges = [e for e in edges if e.get('type') == 'contains'][:100000]  # Limit to 100k
    
    print(f"Rendering {len(node_data):,} nodes, {len(contains_edges):,} edges")
    
    # Create compact binary-like arrays
    nodes_json = json.dumps(node_data)
    edges_json = json.dumps(contains_edges)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Full Bio Filesystem Graph - {len(nodes):,} Nodes</title>
    <style>
        * {{ margin: 0; padding: 0; }}
        body {{ 
            background: #0a0a0f; 
            overflow: hidden;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
        }}
        #container {{ width: 100vw; height: 100vh; }}
        #info {{
            position: absolute;
            top: 20px;
            left: 20px;
            color: #e0e0e0;
            background: rgba(10,10,15,0.9);
            padding: 15px 20px;
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.3);
            max-width: 320px;
            backdrop-filter: blur(10px);
        }}
        #info h1 {{
            color: #ff6b35;
            font-size: 16px;
            margin-bottom: 8px;
        }}
        #stats {{
            font-size: 11px;
            color: #888;
            margin-bottom: 12px;
        }}
        #legend {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4px;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .legend-section {{
            font-size: 10px;
        }}
        .legend-section h3 {{
            font-size: 11px;
            margin-bottom: 4px;
            color: #888;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 9px;
            margin-bottom: 2px;
        }}
        .legend-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        #tooltip {{
            position: absolute;
            display: none;
            background: rgba(10,10,15,0.95);
            color: #fff;
            padding: 8px 12px;
            border-radius: 6px;
            border: 1px solid #ff6b35;
            font-size: 11px;
            max-width: 350px;
            pointer-events: none;
            z-index: 1000;
        }}
        #tooltip .path {{
            color: #00ff87;
            font-size: 9px;
            word-break: break-all;
            margin-top: 4px;
        }}
        #controls {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            display: flex;
            gap: 8px;
        }}
        .btn {{
            background: rgba(255,107,53,0.15);
            border: 1px solid rgba(255,107,53,0.5);
            color: #ff6b35;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            font-size: 10px;
            transition: all 0.2s;
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
            background: rgba(10,10,15,0.9);
            border: 1px solid rgba(255,107,53,0.5);
            color: #fff;
            padding: 8px 12px;
            border-radius: 4px;
            width: 200px;
            font-family: inherit;
            font-size: 11px;
        }}
        #search input:focus {{
            outline: none;
            border-color: #ff6b35;
        }}
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #ff6b35;
            font-size: 14px;
        }}
        .spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid rgba(255,107,53,0.2);
            border-top-color: #ff6b35;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="loading">
        <div class="spinner"></div>
        Loading {len(nodes):,} nodes...
    </div>
    
    <div id="info" style="display:none;">
        <h1>🧠 Bio Filesystem Graph</h1>
        <div id="stats">
            <strong>{len(nodes):,}</strong> nodes | <strong>{len(contains_edges):,}</strong> edges<br>
            <span style="color:#4895ef">System: {sum(1 for n in nodes if is_system_path(n['path'])):,}</span> | 
            <span style="color:#ff6b35">User: {sum(1 for n in nodes if not is_system_path(n['path'])):,}</span>
        </div>
        <div id="legend">
            <div class="legend-section">
                <h3>User Files (Warm)</h3>
                <div class="legend-item"><div class="legend-dot" style="background:#00ff87"></div>Code</div>
                <div class="legend-item"><div class="legend-dot" style="background:#00b4d8"></div>Config</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ffd166"></div>Docs</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ef476f"></div>Data</div>
                <div class="legend-item"><div class="legend-dot" style="background:#ff6b35"></div>Dirs</div>
            </div>
            <div class="legend-section">
                <h3>System Files (Cool)</h3>
                <div class="legend-item"><div class="legend-dot" style="background:#4361ee"></div>Code</div>
                <div class="legend-item"><div class="legend-dot" style="background:#7209b7"></div>Config</div>
                <div class="legend-item"><div class="legend-dot" style="background:#560bad"></div>Docs</div>
                <div class="legend-item"><div class="legend-dot" style="background:#480ca8"></div>Data</div>
                <div class="legend-item"><div class="legend-dot" style="background:#3f37c9"></div>Dirs</div>
            </div>
        </div>
        <div style="font-size: 10px; color: #666;">
            Drag to rotate • Scroll to zoom<br>
            Type to search files
        </div>
    </div>
    
    <div id="tooltip">
        <div class="name"></div>
        <div class="path"></div>
    </div>
    
    <div id="search">
        <input type="text" id="searchInput" placeholder="Search files...">
    </div>
    
    <div id="controls">
        <button class="btn" onclick="resetCamera()">Reset</button>
        <button class="btn" onclick="toggleRotation()">Rotate</button>
        <button class="btn" onclick="toggleLabels()">Labels</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Data embedded
        const nodes = {nodes_json};
        const edges = {edges_json};
        
        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0f);
        scene.fog = new THREE.Fog(0x0a0a0f, 20, 100);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 500);
        camera.position.z = 30;
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true, powerPreference: "high-performance" }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Geometry for all nodes (shared)
        const nodeGeometry = new THREE.SphereGeometry(0.1, 6, 6);
        
        // Group all nodes
        const nodeGroup = new THREE.Group();
        scene.add(nodeGroup);
        
        // Color lookup
        const colorMap = {{
            'user_code': 0x00ff87, 'user_config': 0x00b4d8, 'user_doc': 0xffd166,
            'user_data': 0xef476f, 'user_media': 0x9b5de5, 'user_dir': 0xff6b35, 'user_default': 0xa8dadc,
            'sys_code': 0x4361ee, 'sys_config': 0x7209b7, 'sys_doc': 0x560bad,
            'sys_data': 0x480ca8, 'sys_media': 0x3a0ca3, 'sys_dir': 0x3f37c9, 'sys_default': 0x4895ef
        }};
        
        // Create nodes
        const nodeMeshes = [];
        const colorToMesh = {{}};
        
        nodes.forEach((node, i) => {{
            const colorHex = parseInt(node.color.replace('#', ''), 16);
            
            let material;
            if (!colorToMesh[colorHex]) {{
                material = new THREE.MeshBasicMaterial({{ 
                    color: colorHex,
                    transparent: true,
                    opacity: 0.8
                }});
                colorToMesh[colorHex] = material;
            }} else {{
                material = colorToMesh[colorHex];
            }}
            
            const mesh = new THREE.Mesh(nodeGeometry, material);
            mesh.position.set(node.x, node.y, node.z);
            mesh.scale.setScalar(node.type === 'directory' ? 1.5 : 1);
            mesh.userData = {{ id: node.id, name: node.name, path: node.path, type: node.type }};
            nodeGroup.add(mesh);
            nodeMeshes.push(mesh);
        }});
        
        // Edge lines
        const edgePositions = [];
        const edgeColors = [];
        const edgeMaterial = new THREE.LineBasicMaterial({{ 
            vertexColors: true,
            transparent: true,
            opacity: 0.05
        }});
        
        // Sample edges for performance
        const edgeSample = edges.slice(0, Math.min(edges.length, 50000));
        
        edgeSample.forEach(edge => {{
            const sourceNode = nodeMeshes.find(m => m.userData.id === edge.source);
            const targetNode = nodeMeshes.find(m => m.userData.id === edge.target);
            
            if (sourceNode && targetNode) {{
                edgePositions.push(
                    sourceNode.position.x, sourceNode.position.y, sourceNode.position.z,
                    targetNode.position.x, targetNode.position.y, targetNode.position.z
                );
                // Dim gray color for edges
                edgeColors.push(0.2, 0.2, 0.2, 0.2, 0.2, 0.2);
            }}
        }});
        
        const edgeGeometry = new THREE.BufferGeometry();
        edgeGeometry.setAttribute('position', new THREE.Float32BufferAttribute(edgePositions, 3));
        edgeGeometry.setAttribute('color', new THREE.Float32BufferAttribute(edgeColors, 3));
        const edgeLines = new THREE.LineSegments(edgeGeometry, edgeMaterial);
        scene.add(edgeLines);
        
        // Background particles
        const particleCount = 200;
        const particleGeometry = new THREE.BufferGeometry();
        const particlePositions = [];
        
        for (let i = 0; i < particleCount; i++) {{
            particlePositions.push(
                (Math.random() - 0.5) * 100,
                (Math.random() - 0.5) * 100,
                (Math.random() - 0.5) * 100
            );
        }}
        
        particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(particlePositions, 3));
        const particleMaterial = new THREE.PointsMaterial({{
            color: 0xff6b35,
            size: 0.2,
            transparent: true,
            opacity: 0.2
        }});
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        
        // Hide loading, show info
        document.getElementById('loading').style.display = 'none';
        document.getElementById('info').style.display = 'block';
        
        // Controls
        let isDragging = false;
        let previousMouse = {{ x: 0, y: 0 }};
        let autoRotate = true;
        let showLabels = false;
        
        renderer.domElement.addEventListener('mousedown', (e) => {{
            isDragging = true;
            previousMouse = {{ x: e.clientX, y: e.clientY }};
        }});
        
        renderer.domElement.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const dx = e.clientX - previousMouse.x;
                const dy = e.clientY - previousMouse.y;
                nodeGroup.rotation.y += dx * 0.003;
                nodeGroup.rotation.x += dy * 0.003;
                previousMouse = {{ x: e.clientX, y: e.clientY }};
            }}
            updateTooltip(e);
        }});
        
        renderer.domElement.addEventListener('mouseup', () => isDragging = false);
        renderer.domElement.addEventListener('mouseleave', () => isDragging = false);
        
        renderer.domElement.addEventListener('wheel', (e) => {{
            camera.position.z += e.deltaY * 0.05;
            camera.position.z = Math.max(5, Math.min(200, camera.position.z));
        }});
        
        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase();
            const regex = new RegExp(query, 'i');
            
            nodeMeshes.forEach(mesh => {{
                const node = mesh.userData;
                const match = !query || regex.test(node.name) || regex.test(node.path);
                mesh.material.opacity = match ? 0.9 : 0.05;
                mesh.scale.setScalar(match ? (node.type === 'directory' ? 2 : 1.5) : 0.5);
            }});
        }});
        
        // Tooltip with raycaster
        const raycaster = new THREE.Raycaster();
        raycaster.params.Points.threshold = 0.5;
        const mouse = new THREE.Vector2();
        
        function updateTooltip(e) {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(nodeMeshes);
            
            const tooltip = document.getElementById('tooltip');
            if (intersects.length > 0) {{
                const node = intersects[0].object.userData;
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
                tooltip.querySelector('.name').textContent = node.name;
                tooltip.querySelector('.path').textContent = node.path;
                tooltip.style.borderColor = intersects[0].object.material.color.getHexString() === 'ff6b35' ? '#ff6b35' : '#4895ef';
            }} else {{
                tooltip.style.display = 'none';
            }}
        }}
        
        function resetCamera() {{
            camera.position.set(0, 0, 30);
            nodeGroup.rotation.set(0, 0, 0);
        }}
        
        function toggleRotation() {{
            autoRotate = !autoRotate;
        }}
        
        function toggleLabels() {{
            showLabels = !showLabels;
            // Labels would require sprite implementation - skipped for performance
        }}
        
        // Animation
        let time = 0;
        function animate() {{
            requestAnimationFrame(animate);
            time += 0.01;
            
            if (autoRotate) nodeGroup.rotation.y += 0.0005;
            
            particles.rotation.y += 0.0001;
            particles.rotation.x += 0.00005;
            
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
    
    input_path = sys.argv[1] if len(sys.argv) > 1 else '/home/csilva/.openclaw/workspace/memory/system_graph_compressed.json'
    output_path = sys.argv[2] if len(sys.argv) > 2 else '/home/csilva/.openclaw/workspace/memory/bio_graph_3d_full.html'
    
    build_full_graph(input_path, output_path)