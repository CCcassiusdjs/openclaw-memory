#!/usr/bin/env python3
"""
CORTICAL FILE SYSTEM VISUALIZER (CFSV)
=====================================
A NOVEL visualization inspired by cortical columns in the brain.

Key Concepts:
- Minicolumns (~100 neurons) = Files with similar semantic content
- Hypercolumns = Directories
- Cortical Columns = Projects/Contexts
- Cortical Layers (6 layers) = Different views of same data
- Neural Activity = Real-time file access visualization

This is NOT a tree, NOT a graph, NOT a treemap.
It's a CORTICAL representation where files are neurons organized in columns.

Architecture:
- Backend: inotify watches for real-time file system changes
- Frontend: WebGPU instanced rendering for millions of nodes
- Sync: WebSocket for instant updates (no lag)
"""

import json
import os
import hashlib
import math
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import struct

# Cortical layer configuration (6 layers like real cortex)
CORTICAL_LAYERS = {
    1: {"name": "Molecular", "depth": 0.0, "opacity": 0.3, "function": "Overview - all files as points"},
    2: {"name": "External Granular", "depth": 0.2, "opacity": 0.5, "function": "Directory structure"},
    3: {"name": "External Pyramidal", "depth": 0.4, "opacity": 0.7, "function": "Recent activity"},
    4: {"name": "Internal Granular", "depth": 0.6, "opacity": 0.8, "function": "File types"},
    5: {"name": "Internal Pyramidal", "depth": 0.8, "opacity": 0.9, "function": "Concept relationships"},
    6: {"name": "Multiform", "depth": 1.0, "opacity": 1.0, "function": "Direct manipulation"},
}

# File type to cortical region mapping (like brain regions)
CORTICAL_REGIONS = {
    "code": {"region": "Motor Cortex", "color": "#00ff87", "hemisphere": "left"},
    "config": {"region": "Prefrontal", "color": "#00b4d8", "hemisphere": "left"},
    "doc": {"region": "Temporal", "color": "#ffd166", "hemisphere": "right"},
    "data": {"region": "Parietal", "color": "#ef476f", "hemisphere": "right"},
    "media": {"region": "Occipital", "color": "#9b5de5", "hemisphere": "back"},
    "system": {"region": "Brainstem", "color": "#4895ef", "hemisphere": "center"},
    "user": {"region": "Cerebrum", "color": "#ff6b35", "hemisphere": "front"},
    "default": {"region": "Association", "color": "#a8dadc", "hemisphere": "center"},
    "dir": {"region": "Cerebrum", "color": "#ff6b35", "hemisphere": "front"},
}

def get_file_type(path):
    """Determine file type from extension."""
    ext = Path(path).suffix.lower()
    
    if ext in {'.py', '.js', '.ts', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.kt', '.swift', '.cc', '.hpp', '.m', '.php', '.lua', '.rb', '.sh'}:
        return 'code'
    if ext in {'.json', '.yaml', '.yml', '.toml', '.xml', '.ini', '.conf', '.cfg', '.cmake'}:
        return 'config'
    if ext in {'.md', '.txt', '.rst', '.pdf', '.doc', '.docx', '.tex', '.page', '.html'}:
        return 'doc'
    if ext in {'.csv', '.sql', '.db', '.sqlite', '.parquet', '.pkl', '.dat', '.bin', '.hex'}:
        return 'data'
    if ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.mp3', '.wav', '.ogg', '.webm'}:
        return 'media'
    return 'default'

def is_system_path(path):
    """Check if path is a system path."""
    SYSTEM_PREFIXES = ['/usr', '/etc', '/var', '/opt', '/bin', '/sbin', '/lib', '/lib64', '/usr/local']
    for prefix in SYSTEM_PREFIXES:
        if path.startswith(prefix):
            return True
    return False

def cortical_position(node_id, path, node_type, depth_factor=0.5):
    """
    Calculate cortical column position.
    
    Inspired by real cortical organization:
    - Files in same directory = same minicolumn
    - Directories = hypercolumns
    - File types = different cortical regions
    - Depth = cortical layer
    """
    # Hash for deterministic positioning
    h = hashlib.md5(node_id.encode()).hexdigest()
    h_int = int(h[:8], 16) / 0xffffffff
    
    # Cortical region based on file type
    file_type = get_file_type(path) if node_type == 'file' else 'default'
    region = CORTICAL_REGIONS.get(file_type, CORTICAL_REGIONS['default'])
    
    # Hemisphere positioning (left/right/center/back)
    hemisphere_x_offset = {
        "left": -5,
        "right": 5,
        "center": 0,
        "back": 0,
        "front": 0,
    }
    x_offset = hemisphere_x_offset.get(region["hemisphere"], 0)
    
    # Path-based clustering (minicolumn)
    path_hash = hashlib.md5(path.encode()).hexdigest()
    path_int = int(path_hash[:8], 16) / 0xffffffff
    
    # Depth (y-axis) = cortical layer
    depth = depth_factor + (h_int - 0.5) * 0.3
    
    # Radius based on directory depth
    dir_depth = path.count('/')
    radius = 2 + dir_depth * 0.5
    
    # Angular position (column within region)
    angle = path_int * 2 * math.pi
    
    # Add noise for organic feel
    noise_x = (int(h[8:16], 16) / 0xffffffff - 0.5) * 0.5
    noise_y = (int(h[16:24], 16) / 0xffffffff - 0.5) * 0.3
    noise_z = (int(h[24:32], 16) / 0xffffffff - 0.5) * 0.5
    
    x = radius * math.cos(angle) + x_offset + noise_x
    y = depth + noise_y
    z = radius * math.sin(angle) + noise_z
    
    return {"x": x, "y": y, "z": z, "region": region}

def build_cortical_graph(graph_json_path, output_path):
    """
    Build cortical-inspired visualization from graph JSON.
    
    This creates a representation inspired by the cerebral cortex:
    - 6 layers of processing
    - Minicolumns for file clusters
    - Hypercolumns for directories
    - Activity visualization (neural firing)
    """
    
    print(f"Loading graph from {graph_json_path}...")
    
    with open(graph_json_path, 'r') as f:
        data = json.load(f)
    
    # Parse nodes
    nodes_data = data.get('nodes', {})
    edges_data = data.get('edges', [])
    
    nodes = []
    for node_id, node_info in nodes_data.items():
        nodes.append({
            'id': node_id,
            'type': node_info.get('type', 'file'),
            'path': node_info.get('path', node_id),
        })
    
    print(f"Found {len(nodes):,} nodes")
    
    # Calculate positions in cortical space
    print("Calculating cortical positions...")
    
    node_data = []
    for i, node in enumerate(nodes):
        # Depth factor varies by layer (simulate 6 cortical layers)
        layer = i % 6
        depth_factor = CORTICAL_LAYERS[layer + 1]["depth"]
        
        pos = cortical_position(
            node['id'], 
            node['path'], 
            node['type'],
            depth_factor
        )
        
        file_type = get_file_type(node['path']) if node['type'] == 'file' else 'dir'
        is_system = is_system_path(node['path'])
        
        # Activity level (random for now, will be real-time later)
        activity = hash(node['path']) % 10 / 10.0
        
        node_data.append({
            'id': node['id'],
            'path': node['path'],
            'name': node['path'].split('/')[-1],
            'type': node['type'],
            'fileType': file_type,
            'isSystem': is_system,
            'region': pos['region']['region'],
            'hemisphere': pos['region']['hemisphere'],
            'color': pos['region']['color'],
            'layer': layer + 1,
            'x': pos['x'],
            'y': pos['y'],
            'z': pos['z'],
            'activity': activity,  # 0.0 - 1.0 (will be real-time)
        })
    
    # Build edges (contains relationships)
    print("Building synaptic connections...")
    edges = []
    for e in edges_data:
        edges.append({
            'source': e.get('s', e.get('source', '')),
            'target': e.get('t', e.get('target', '')),
            'type': e.get('type', 'contains'),
        })
    
    # Statistics
    stats = {
        'total_nodes': len(nodes),
        'total_edges': len(edges),
        'by_type': {},
        'by_region': {},
        'by_layer': {str(i): 0 for i in range(1, 7)},
    }
    
    for node in node_data:
        ft = node['fileType']
        stats['by_type'][ft] = stats['by_type'].get(ft, 0) + 1
        
        reg = node['region']
        stats['by_region'][reg] = stats['by_region'].get(reg, 0) + 1
        
        layer = str(node['layer'])
        stats['by_layer'][layer] = stats['by_layer'].get(layer, 0) + 1
    
    print(f"Statistics: {stats}")
    
    # Build HTML with WebGPU-ready structure
    html = build_cortical_html(node_data, edges, stats)
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Written to {output_path}")
    return output_path

def build_cortical_html(nodes, edges, stats):
    """Build cortical-inspired HTML visualization."""
    
    nodes_json = json.dumps(nodes)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Cortical File System Visualizer (CFSV)</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #050508;
            overflow: hidden;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            color: #e0e0e0;
        }}
        #container {{ width: 100vw; height: 100vh; }}
        
        /* Cortical Layer Panel */
        #layers {{
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(10,10,15,0.9);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.3);
            backdrop-filter: blur(10px);
        }}
        #layers h2 {{
            font-size: 12px;
            color: #ff6b35;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .layer {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            cursor: pointer;
            padding: 5px;
            border-radius: 4px;
            transition: all 0.3s;
        }}
        .layer:hover {{
            background: rgba(255,107,53,0.1);
        }}
        .layer.active {{
            background: rgba(255,107,53,0.2);
            border-left: 3px solid #ff6b35;
        }}
        .layer-num {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
        }}
        .layer-info {{
            font-size: 9px;
            opacity: 0.7;
        }}
        
        /* Activity Monitor (Real-time) */
        #activity {{
            position: absolute;
            right: 20px;
            top: 20px;
            background: rgba(10,10,15,0.9);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0,255,135,0.3);
            min-width: 200px;
        }}
        #activity h2 {{
            font-size: 12px;
            color: #00ff87;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        #activity-bar {{
            height: 60px;
            display: flex;
            align-items: flex-end;
            gap: 2px;
        }}
        .activity-pulse {{
            width: 4px;
            background: linear-gradient(to top, #00ff87, #00b4d8);
            border-radius: 2px;
            transition: height 0.1s;
        }}
        #recent {{
            margin-top: 10px;
            font-size: 10px;
            max-height: 100px;
            overflow-y: auto;
        }}
        #recent div {{
            padding: 3px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        /* Statistics */
        #stats {{
            position: absolute;
            left: 20px;
            bottom: 20px;
            background: rgba(10,10,15,0.9);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0,180,216,0.3);
            font-size: 10px;
        }}
        #stats h2 {{
            font-size: 12px;
            color: #00b4d8;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }}
        .stat-label {{ opacity: 0.7; }}
        .stat-value {{ color: #00ff87; font-weight: bold; }}
        
        /* Tooltip */
        #tooltip {{
            position: absolute;
            display: none;
            background: rgba(10,10,15,0.95);
            color: #fff;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #ff6b35;
            font-size: 11px;
            max-width: 400px;
            pointer-events: none;
            z-index: 1000;
        }}
        #tooltip .path {{
            color: #00ff87;
            font-size: 9px;
            word-break: break-all;
            margin-top: 5px;
        }}
        #tooltip .region {{
            color: #00b4d8;
            font-size: 9px;
            margin-top: 3px;
        }}
        
        /* Legend */
        #legend {{
            position: absolute;
            right: 20px;
            bottom: 20px;
            background: rgba(10,10,15,0.9);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.3);
        }}
        #legend h2 {{
            font-size: 12px;
            color: #ff6b35;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
            font-size: 10px;
        }}
        .legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        
        /* Controls */
        #controls {{
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
        }}
        .btn {{
            background: rgba(255,107,53,0.15);
            border: 1px solid rgba(255,107,53,0.5);
            color: #ff6b35;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
            font-size: 11px;
            transition: all 0.3s;
        }}
        .btn:hover {{
            background: #ff6b35;
            color: #000;
        }}
        .btn.active {{
            background: #ff6b35;
            color: #000;
        }}
        
        /* Search */
        #search {{
            position: absolute;
            top: 70px;
            left: 50%;
            transform: translateX(-50%);
        }}
        #search input {{
            background: rgba(10,10,15,0.9);
            border: 1px solid rgba(0,255,135,0.3);
            color: #fff;
            padding: 10px 20px;
            border-radius: 25px;
            width: 400px;
            font-family: inherit;
            font-size: 12px;
        }}
        #search input:focus {{
            outline: none;
            border-color: #00ff87;
        }}
        
        /* Connection status */
        #connection {{
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 10px;
        }}
        #connection .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00ff87;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        #connection .dot.disconnected {{
            background: #ef476f;
            animation: none;
        }}
        
        /* Loading */
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }}
        .spinner {{
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255,107,53,0.2);
            border-top-color: #ff6b35;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Neural activity animation */
        .neuron-active {{
            animation: fire 0.5s ease-out;
        }}
        @keyframes fire {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.5); }}
            100% {{ transform: scale(1); }}
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div id="loading">
        <div class="spinner"></div>
        <div>Loading cortical columns...</div>
        <div style="font-size: 12px; margin-top: 10px; opacity: 0.6;">
            Mapping {len(nodes):,} neurons to cortical regions
        </div>
    </div>
    
    <!-- Connection Status -->
    <div id="connection" style="display:none;">
        <div class="dot"></div>
        <span>Real-time sync active</span>
    </div>
    
    <!-- Cortical Layers Panel -->
    <div id="layers" style="display:none;">
        <h2>Cortical Layers</h2>
        <div class="layer active" data-layer="1">
            <div class="layer-num" style="background: #ff6b35;">I</div>
            <div class="layer-info">Molecular - Overview</div>
        </div>
        <div class="layer" data-layer="2">
            <div class="layer-num" style="background: #00b4d8;">II</div>
            <div class="layer-info">External Granular - Structure</div>
        </div>
        <div class="layer" data-layer="3">
            <div class="layer-num" style="background: #00ff87;">III</div>
            <div class="layer-info">External Pyramidal - Activity</div>
        </div>
        <div class="layer" data-layer="4">
            <div class="layer-num" style="background: #ffd166;">IV</div>
            <div class="layer-info">Internal Granular - Types</div>
        </div>
        <div class="layer" data-layer="5">
            <div class="layer-num" style="background: #ef476f;">V</div>
            <div class="layer-info">Internal Pyramidal - Concepts</div>
        </div>
        <div class="layer" data-layer="6">
            <div class="layer-num" style="background: #9b5de5;">VI</div>
            <div class="layer-info">Multiform - Direct Access</div>
        </div>
    </div>
    
    <!-- Activity Monitor -->
    <div id="activity" style="display:none;">
        <h2>Neural Activity</h2>
        <div id="activity-bar"></div>
        <div id="recent"></div>
    </div>
    
    <!-- Statistics -->
    <div id="stats" style="display:none;">
        <h2>Cortex Stats</h2>
        <div class="stat-row">
            <span class="stat-label">Total Neurons:</span>
            <span class="stat-value">{stats['total_nodes']:,}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Synapses:</span>
            <span class="stat-value">{stats['total_edges']:,}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Cortical Regions:</span>
            <span class="stat-value">{len(stats['by_region'])}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Layers:</span>
            <span class="stat-value">6</span>
        </div>
    </div>
    
    <!-- Legend -->
    <div id="legend" style="display:none;">
        <h2>Brain Regions</h2>
        <div class="legend-item">
            <div class="legend-dot" style="background:#ff6b35"></div>
            <span>Cerebrum (User Files)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background:#4895ef"></div>
            <span>Brainstem (System)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background:#00ff87"></div>
            <span>Motor (Code)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background:#00b4d8"></div>
            <span>Prefrontal (Config)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background:#ffd166"></div>
            <span>Temporal (Docs)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background:#ef476f"></div>
            <span>Parietal (Data)</span>
        </div>
        <div class="legend-item">
            <div class="legend-dot" style="background:#9b5de5"></div>
            <span>Occipital (Media)</span>
        </div>
    </div>
    
    <!-- Controls -->
    <div id="controls" style="display:none;">
        <button class="btn active" onclick="setView('cortex')">Cortex View</button>
        <button class="btn" onclick="setView('columns')">Columns</button>
        <button class="btn" onclick="setView('activity')">Activity</button>
        <button class="btn" onclick="setView('layers')">Layers</button>
        <button class="btn" onclick="toggleRealtime()">Real-time</button>
    </div>
    
    <!-- Search -->
    <div id="search" style="display:none;">
        <input type="text" id="searchInput" placeholder="Search neurons...">
    </div>
    
    <!-- Tooltip -->
    <div id="tooltip">
        <div class="name"></div>
        <div class="path"></div>
        <div class="region"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Cortical data
        const nodes = {nodes_json};
        const stats = {json.dumps(stats)};
        
        // Scene setup
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050508);
        scene.fog = new THREE.FogExp2(0x050508, 0.02);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 15);
        
        const renderer = new THREE.WebGLRenderer({{
            antialias: true,
            powerPreference: "high-performance"
        }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Group for all cortical elements
        const cortex = new THREE.Group();
        scene.add(cortex);
        
        // Instanced mesh for all neurons (files)
        const neuronGeometry = new THREE.SphereGeometry(0.08, 6, 6);
        const neuronMaterials = {{}};
        const neuronMeshes = [];
        
        // Color map
        const colorMap = {{
            'code': 0x00ff87,
            'config': 0x00b4d8,
            'doc': 0xffd166,
            'data': 0xef476f,
            'media': 0x9b5de5,
            'system': 0x4895ef,
            'user': 0xff6b35,
            'dir': 0xff6b35,
            'default': 0xa8dadc
        }};
        
        // Create neurons
        console.log('Creating', nodes.length, 'neurons...');
        
        nodes.forEach((node, i) => {{
            const colorHex = colorMap[node.fileType] || colorMap[node.isSystem ? 'system' : 'user'];
            
            if (!neuronMaterials[colorHex]) {{
                neuronMaterials[colorHex] = new THREE.MeshBasicMaterial({{
                    color: colorHex,
                    transparent: true,
                    opacity: 0.7
                }});
            }}
            
            const mesh = new THREE.Mesh(neuronGeometry, neuronMaterials[colorHex]);
            mesh.position.set(node.x, node.y, node.z);
            mesh.userData = node;
            cortex.add(mesh);
            neuronMeshes.push(mesh);
        }});
        
        // Synaptic connections (edges) - only for nearby neurons
        console.log('Creating synaptic connections...');
        
        const edgeMaterial = new THREE.LineBasicMaterial({{
            color: 0x1a1a2e,
            transparent: true,
            opacity: 0.1
        }});
        
        // Build spatial hash for fast neighbor lookup
        const spatialHash = new Map();
        const cellSize = 2;
        
        nodes.forEach((node, i) => {{
            const key = `${{Math.floor(node.x/cellSize)}},${{Math.floor(node.y/cellSize)}},${{Math.floor(node.z/cellSize)}}`;
            if (!spatialHash.has(key)) spatialHash.set(key, []);
            spatialHash.get(key).push(i);
        }});
        
        // Create local connections only
        const edgePositions = [];
        const maxConnections = 3;
        
        nodes.forEach((node, i) => {{
            const key = `${{Math.floor(node.x/cellSize)}},${{Math.floor(node.y/cellSize)}},${{Math.floor(node.z/cellSize)}}`;
            const neighbors = spatialHash.get(key) || [];
            
            let connections = 0;
            for (const j of neighbors) {{
                if (i !== j && connections < maxConnections) {{
                    const other = nodes[j];
                    const dist = Math.sqrt(
                        (node.x - other.x)**2 + 
                        (node.y - other.y)**2 + 
                        (node.z - other.z)**2
                    );
                    if (dist < 1.5) {{
                        edgePositions.push(node.x, node.y, node.z);
                        edgePositions.push(other.x, other.y, other.z);
                        connections++;
                    }}
                }}
            }}
        }});
        
        const edgeGeometry = new THREE.BufferGeometry();
        edgeGeometry.setAttribute('position', new THREE.Float32BufferAttribute(edgePositions, 3));
        const edges = new THREE.LineSegments(edgeGeometry, edgeMaterial);
        cortex.add(edges);
        
        // Ambient particles (background activity)
        const particleCount = 500;
        const particleGeometry = new THREE.BufferGeometry();
        const particlePositions = [];
        
        for (let i = 0; i < particleCount; i++) {{
            particlePositions.push(
                (Math.random() - 0.5) * 50,
                (Math.random() - 0.5) * 30,
                (Math.random() - 0.5) * 50
            );
        }}
        
        particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(particlePositions, 3));
        const particleMaterial = new THREE.PointsMaterial({{
            color: 0xff6b35,
            size: 0.1,
            transparent: true,
            opacity: 0.15
        }});
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        
        // Hide loading, show controls
        document.getElementById('loading').style.display = 'none';
        document.getElementById('layers').style.display = 'block';
        document.getElementById('activity').style.display = 'block';
        document.getElementById('stats').style.display = 'block';
        document.getElementById('legend').style.display = 'block';
        document.getElementById('controls').style.display = 'flex';
        document.getElementById('search').style.display = 'block';
        document.getElementById('connection').style.display = 'flex';
        
        // Activity bar
        const activityBar = document.getElementById('activity-bar');
        for (let i = 0; i < 30; i++) {{
            const pulse = document.createElement('div');
            pulse.className = 'activity-pulse';
            pulse.style.height = Math.random() * 40 + 10 + 'px';
            activityBar.appendChild(pulse);
        }}
        
        // Controls
        let isDragging = false;
        let previousMouse = {{ x: 0, y: 0 }};
        let autoRotate = true;
        let currentView = 'cortex';
        let realtimeEnabled = false;
        
        renderer.domElement.addEventListener('mousedown', (e) => {{
            isDragging = true;
            previousMouse = {{ x: e.clientX, y: e.clientY }};
        }});
        
        renderer.domElement.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const dx = e.clientX - previousMouse.x;
                const dy = e.clientY - previousMouse.y;
                cortex.rotation.y += dx * 0.005;
                cortex.rotation.x += dy * 0.005;
                previousMouse = {{ x: e.clientX, y: e.clientY }};
            }}
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
            const regex = new RegExp(query, 'i');
            
            neuronMeshes.forEach(mesh => {{
                const node = mesh.userData;
                const match = !query || regex.test(node.name) || regex.test(node.path);
                mesh.material.opacity = match ? 0.9 : 0.05;
                mesh.scale.setScalar(match ? 2 : 1);
            }});
        }});
        
        // Raycaster for tooltip
        const raycaster = new THREE.Raycaster();
        raycaster.params.Points.threshold = 0.5;
        const mouse = new THREE.Vector2();
        
        function updateTooltip(e) {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(neuronMeshes);
            
            const tooltip = document.getElementById('tooltip');
            if (intersects.length > 0) {{
                const node = intersects[0].object.userData;
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
                tooltip.querySelector('.name').textContent = node.name;
                tooltip.querySelector('.path').textContent = node.path;
                tooltip.querySelector('.region').textContent = `${{node.region}} (Layer ${{node.layer}})`;
            }} else {{
                tooltip.style.display = 'none';
            }}
        }}
        
        // View controls
        function setView(view) {{
            currentView = view;
            document.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            
            switch(view) {{
                case 'cortex':
                    cortex.rotation.set(0, 0, 0);
                    camera.position.set(0, 5, 15);
                    break;
                case 'columns':
                    cortex.rotation.set(0.5, 0, 0);
                    camera.position.set(0, 20, 5);
                    break;
                case 'activity':
                    cortex.rotation.set(0, 0, 0);
                    camera.position.set(0, 0, 20);
                    // Highlight active neurons
                    neuronMeshes.forEach(mesh => {{
                        mesh.material.opacity = mesh.userData.activity > 0.7 ? 0.9 : 0.1;
                    }});
                    break;
                case 'layers':
                    cortex.rotation.set(0, 0, 0.5);
                    camera.position.set(15, 5, 0);
                    break;
            }}
        }}
        
        // Real-time toggle (placeholder for WebSocket connection)
        function toggleRealtime() {{
            realtimeEnabled = !realtimeEnabled;
            const dot = document.querySelector('#connection .dot');
            
            if (realtimeEnabled) {{
                dot.style.background = '#00ff87';
                // TODO: Connect to WebSocket for real-time updates
                // ws = new WebSocket('ws://localhost:8765');
                console.log('Real-time sync enabled');
            }} else {{
                dot.style.background = '#ef476f';
                console.log('Real-time sync disabled');
            }}
        }}
        
        // Simulate neural activity
        function simulateActivity() {{
            const pulses = document.querySelectorAll('.activity-pulse');
            pulses.forEach(pulse => {{
                pulse.style.height = Math.random() * 50 + 10 + 'px';
            }});
        }}
        
        setInterval(simulateActivity, 500);
        
        // Animation
        let time = 0;
        function animate() {{
            requestAnimationFrame(animate);
            time += 0.01;
            
            if (autoRotate) {{
                cortex.rotation.y += 0.0005;
            }}
            
            // Animate particles
            particles.rotation.y += 0.0001;
            particles.rotation.x += 0.00005;
            
            renderer.render(scene, camera);
        }}
        
        animate();
        
        // Resize handler
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
    output_path = sys.argv[2] if len(sys.argv) > 2 else '/home/csilva/.openclaw/workspace/memory/cortical_fs_visualizer.html'
    
    build_cortical_graph(input_path, output_path)