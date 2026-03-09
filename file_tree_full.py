#!/usr/bin/env python3
"""
FILE SYSTEM TREE 3D - FULL SYSTEM
==================================
Visualização COMPLETA do sistema como árvore 3D.

Usa os dados do system_graph.json:
- 402,900 nós totais
- 4,944,003 conexões
- 43,414 diretórios
- 359,486 arquivos
"""

import json
import os
import math
from collections import defaultdict

class FullSystemTree3D:
    """
    Árvore 3D com TODOS os nós do sistema.
    """
    
    def __init__(self):
        self.nodes = {}  # id -> node
        self.edges = []  # [(source, target), ...]
        self.tree = {}   # parent_id -> [child_ids]
        
        # Cores por extensão
        self.ext_colors = {
            '.py': '#00ff87',
            '.js': '#f7df1e',
            '.ts': '#3178c6',
            '.go': '#00add8',
            '.rs': '#dea584',
            '.c': '#555555',
            '.cpp': '#00599c',
            '.h': '#808080',
            '.md': '#ffd166',
            '.txt': '#888888',
            '.json': '#00b4d8',
            '.yaml': '#cb171e',
            '.yml': '#cb171e',
            '.toml': '#9c3c3c',
            '.xml': '#006600',
            '.html': '#e34c26',
            '.css': '#264de4',
            '.sh': '#4eaa25',
            '.pdf': '#ff6b35',
            '.png': '#ff69b4',
            '.jpg': '#ff69b4',
            '.log': '#666666',
        }
    
    def load_from_graph(self, graph_path):
        """Carrega do system_graph.json."""
        print(f"Loading graph from {graph_path}...")
        
        with open(graph_path, 'r') as f:
            data = json.load(f)
        
        metadata = data.get('metadata', {})
        print(f"  Total nodes: {metadata.get('total_nodes', 0):,}")
        print(f"  Total edges: {metadata.get('total_edges', 0):,}")
        
        # Carrega nós
        nodes_data = data.get('nodes', {})
        for node_id, node_info in nodes_data.items():
            self.nodes[node_id] = {
                'id': node_id,
                'type': node_info.get('type', 'file'),
                'name': node_info.get('name', node_id),
                'path': node_info.get('path', ''),
                'ext': node_info.get('ext', ''),
                'size': node_info.get('size', 0),
                'depth': node_info.get('depth', 0),
                'parent_id': None,
                'children': []
            }
        
        # Carrega arestas e constrói árvore
        edges_data = data.get('edges', [])
        for edge in edges_data:
            source = edge.get('s')
            target = edge.get('t')
            
            if source and target:
                self.edges.append((source, target))
                
                # Apenas arestas 'contains' para a árvore
                if edge.get('type') == 'contains':
                    if source not in self.tree:
                        self.tree[source] = []
                    self.tree[source].append(target)
                    
                    if target in self.nodes:
                        self.nodes[target]['parent_id'] = source
        
        print(f"Loaded {len(self.nodes):,} nodes, {len(self.edges):,} edges")
        print(f"Tree has {len(self.tree):,} parent nodes")
        
        return len(self.nodes), len(self.edges)
    
    def build_tree_layout(self, sample_ratio=None):
        """
        Constrói layout de árvore 3D.
        
        Args:
            sample_ratio: Se None, usa todos. Se 0.1, usa 10%.
        """
        print(f"Building 3D tree layout...")
        print(f"  Sample ratio: {sample_ratio or 'ALL'}")
        
        # Encontra raízes (nós sem pai)
        roots = [n for n in self.nodes.values() if n['parent_id'] is None]
        print(f"  Roots found: {len(roots)}")
        
        # Amostragem se necessário
        if sample_ratio and sample_ratio < 1.0:
            import random
            random.seed(42)  # Reprodutível
            
            # Mantém todos os diretórios, amostra arquivos
            all_nodes = list(self.nodes.values())
            sampled_nodes = {}
            
            for node in all_nodes:
                if node['type'] == 'directory':
                    sampled_nodes[node['id']] = node
                elif random.random() < sample_ratio:
                    sampled_nodes[node['id']] = node
            
            self.nodes = sampled_nodes
            print(f"  Sampled to {len(self.nodes):,} nodes")
        
        # Posiciona raízes em círculo
        for i, root in enumerate(roots):
            if root['id'] not in self.nodes:
                continue
            
            angle = (2 * math.pi * i / len(roots)) if len(roots) > 1 else 0
            root['x'] = 0
            root['y'] = 0
            root['z'] = 0
            root['placed'] = True
        
        # Posiciona recursivamente com BFS
        from collections import deque
        
        queue = deque(roots)
        processed = set(n['id'] for n in roots)
        
        while queue:
            parent = queue.popleft()
            
            if parent['id'] not in self.tree:
                continue
            
            children = self.tree[parent['id']]
            child_nodes = [self.nodes[cid] for cid in children if cid in self.nodes]
            
            # Filtra apenas nós não processados
            child_nodes = [n for n in child_nodes if n['id'] not in processed]
            
            if not child_nodes:
                continue
            
            # Parâmetros do ramo
            parent_x = parent.get('x', 0)
            parent_y = parent.get('y', 0)
            parent_z = parent.get('z', 0)
            parent_depth = parent.get('depth', 0)
            
            n_children = len(child_nodes)
            
            # Posiciona filhos
            for i, child in enumerate(child_nodes):
                # Ângulo distribuído
                if n_children > 1:
                    angle = (2 * math.pi * i / n_children)
                else:
                    angle = 0
                
                # Comprimento do ramo (diminui com profundidade)
                branch_length = max(1, 5 - parent_depth * 0.3)
                
                # Raio aumenta com profundidade
                radius = branch_length * (1 + parent_depth * 0.5)
                
                # Posição 3D
                child['x'] = parent_x + radius * math.cos(angle)
                child['y'] = parent_y + 0.5  # Sob sobe
                child['z'] = parent_z + radius * math.sin(angle)
                child['placed'] = True
                
                processed.add(child['id'])
                queue.append(child)
        
        # Conta nós posicionados
        placed_count = sum(1 for n in self.nodes.values() if n.get('placed'))
        print(f"  Placed {placed_count:,} nodes")
    
    def generate_html(self, output_path, max_nodes=None):
        """Gera HTML com árvore 3D."""
        
        # Filtra nós posicionados
        placed_dirs = [n for n in self.nodes.values() 
                      if n.get('placed') and n['type'] == 'directory']
        placed_files = [n for n in self.nodes.values() 
                        if n.get('placed') and n['type'] == 'file']
        
        print(f"Generating HTML...")
        print(f"  Directories: {len(placed_dirs):,}")
        print(f"  Files: {len(placed_files):,}")
        
        # NÃO limita - mostra todos
        # max_nodes = None significa TODOS
        
        # Prepara dados
        dirs_json = json.dumps([{
            'id': d['id'],
            'name': d['name'],
            'path': d['path'],
            'x': d.get('x', 0),
            'y': d.get('y', 0),
            'z': d.get('z', 0),
            'depth': d.get('depth', 0),
            'parentId': d.get('parent_id')
        } for d in placed_dirs])
        
        files_json = json.dumps([{
            'id': f['id'],
            'name': f['name'],
            'ext': f.get('ext', ''),
            'path': f['path'],
            'x': f.get('x', 0),
            'y': f.get('y', 0),
            'z': f.get('z', 0),
            'depth': f.get('depth', 0),
            'color': self.ext_colors.get(f.get('ext', ''), '#666666')
        } for f in placed_files])
        
        # Conexões
        edges_json = json.dumps([{
            'x1': self.nodes.get(e[0], {}).get('x', 0),
            'y1': self.nodes.get(e[0], {}).get('y', 0),
            'z1': self.nodes.get(e[0], {}).get('z', 0),
            'x2': self.nodes.get(e[1], {}).get('x', 0),
            'y2': self.nodes.get(e[1], {}).get('y', 0),
            'z2': self.nodes.get(e[1], {}).get('z', 0)
        } for e in self.edges 
        if e[0] in self.nodes and e[1] in self.nodes 
        and self.nodes[e[0]].get('placed') 
        and self.nodes[e[1]].get('placed')][:100000])  # Limita conexões
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>File System Tree 3D - Full System</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #050510;
            overflow: hidden;
            font-family: 'JetBrains Mono', monospace;
            color: #e0e0e0;
        }}
        #container {{ width: 100vw; height: 100vh; }}
        
        #info {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(10,10,18,0.95);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0,255,135,0.3);
            max-width: 400px;
            z-index: 100;
        }}
        #info h2 {{
            color: #00ff87;
            font-size: 14px;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        #stats {{
            font-size: 11px;
            line-height: 1.6;
        }}
        .stat-label {{ opacity: 0.7; }}
        .stat-value {{ color: #00ff87; font-weight: bold; }}
        
        #controls {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(10,10,18,0.95);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.3);
            z-index: 100;
        }}
        #controls h3 {{
            color: #ff6b35;
            font-size: 12px;
            margin-bottom: 10px;
        }}
        .control-row {{
            display: flex;
            gap: 10px;
            margin-bottom: 8px;
            align-items: center;
        }}
        .control-label {{
            font-size: 10px;
            width: 80px;
            opacity: 0.7;
        }}
        input[type="range"] {{ width: 150px; }}
        .control-value {{
            font-size: 10px;
            color: #00ff87;
            width: 40px;
        }}
        
        #legend {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(10,10,18,0.95);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
            font-size: 10px;
            z-index: 100;
        }}
        #legend h3 {{
            color: #fff;
            font-size: 11px;
            margin-bottom: 10px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }}
        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        
        #tooltip {{
            position: absolute;
            display: none;
            background: rgba(10,10,18,0.95);
            color: #fff;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #00ff87;
            font-size: 11px;
            pointer-events: none;
            z-index: 1000;
            max-width: 400px;
        }}
        #tooltip .name {{
            color: #00ff87;
            font-size: 13px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        #tooltip .path {{
            color: #888;
            font-size: 9px;
            word-break: break-all;
            margin-bottom: 5px;
        }}
        #tooltip .type {{
            color: #ff6b35;
            font-size: 10px;
        }}
        
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #00ff87;
            font-size: 14px;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="loading">Building tree with {len(placed_dirs):,} directories and {len(placed_files):,} files...</div>
    
    <div id="info">
        <h2>Full System Tree 3D</h2>
        <div id="stats">
            <div><span class="stat-label">Total Nodes:</span> <span class="stat-value">{len(self.nodes):,}</span></div>
            <div><span class="stat-label">Directories:</span> <span class="stat-value">{len(placed_dirs):,}</span></div>
            <div><span class="stat-label">Files:</span> <span class="stat-value">{len(placed_files):,}</span></div>
            <div><span class="stat-label">Connections:</span> <span class="stat-value">{len(edges_json)//50:,}</span></div>
        </div>
    </div>
    
    <div id="controls">
        <h3>Tree Controls</h3>
        <div class="control-row">
            <span class="control-label">Node Size:</span>
            <input type="range" id="node-size" min="0.1" max="3" step="0.1" value="0.8">
            <span class="control-value" id="node-size-value">0.8</span>
        </div>
        <div class="control-row">
            <span class="control-label">Branch Opacity:</span>
            <input type="range" id="branch-opacity" min="0" max="1" step="0.1" value="0.2">
            <span class="control-value" id="branch-opacity-value">0.2</span>
        </div>
        <div class="control-row">
            <span class="control-label">Show Files:</span>
            <input type="checkbox" id="show-files" checked>
        </div>
        <div class="control-row">
            <span class="control-label">Show Branches:</span>
            <input type="checkbox" id="show-branches" checked>
        </div>
    </div>
    
    <div id="legend">
        <h3>File Types</h3>
        <div class="legend-item"><div class="legend-dot" style="background:#00ff87"></div>Python</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f7df1e"></div>JavaScript</div>
        <div class="legend-item"><div class="legend-dot" style="background:#00b4d8"></div>Config/JSON</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ffd166"></div>Markdown</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ff6b35"></div>Directory</div>
        <div class="legend-item"><div class="legend-dot" style="background:#666"></div>Other</div>
    </div>
    
    <div id="tooltip">
        <div class="name"></div>
        <div class="path"></div>
        <div class="type"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // Data
        const directories = {dirs_json};
        const files = {files_json};
        const edges = {edges_json};
        
        console.log('Directories:', directories.length);
        console.log('Files:', files.length);
        console.log('Edges:', edges.length);
        
        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050510);
        
        // Ambient particles (stars)
        const particleGeometry = new THREE.BufferGeometry();
        const particleCount = 10000;
        const positions = new Float32Array(particleCount * 3);
        for (let i = 0; i < particleCount * 3; i += 3) {{
            positions[i] = (Math.random() - 0.5) * 2000;
            positions[i + 1] = (Math.random() - 0.5) * 2000;
            positions[i + 2] = (Math.random() - 0.5) * 2000;
        }}
        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const particleMaterial = new THREE.PointsMaterial({{ color: 0x00ff87, size: 0.5, transparent: true, opacity: 0.2 }});
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 5000);
        camera.position.set(0, 100, 200);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true, powerPreference: 'high-performance' }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Controls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 10;
        controls.maxDistance = 1000;
        
        // Groups
        const dirGroup = new THREE.Group();
        const fileGroup = new THREE.Group();
        const branchGroup = new THREE.Group();
        scene.add(dirGroup);
        scene.add(fileGroup);
        scene.add(branchGroup);
        
        // Directories
        console.log('Creating directory nodes...');
        const dirGeometry = new THREE.SphereGeometry(1, 12, 12);
        const dirMaterial = new THREE.MeshBasicMaterial({{ color: 0xff6b35, transparent: true, opacity: 0.7 }});
        const dirInstanced = new THREE.InstancedMesh(dirGeometry, dirMaterial, directories.length);
        
        const dirMatrix = new THREE.Matrix4();
        const dirScale = new THREE.Vector3();
        
        directories.forEach((d, i) => {{
            const scale = Math.max(0.3, 2 - d.depth * 0.1);
            dirScale.set(scale, scale, scale);
            dirMatrix.makeScale(scale, scale, scale);
            dirMatrix.setPosition(d.x, d.y, d.z);
            dirInstanced.setMatrixAt(i, dirMatrix);
        }});
        
        dirInstanced.instanceMatrix.needsUpdate = true;
        dirGroup.add(dirInstanced);
        
        // Files
        console.log('Creating file leaves...');
        const fileGeometry = new THREE.SphereGeometry(0.3, 6, 6);
        const fileMaterial = new THREE.MeshBasicMaterial({{ color: 0x666666, transparent: true, opacity: 0.6 }});
        const fileInstanced = new THREE.Mesh(fileGeometry, fileMaterial);
        const fileColors = [];
        
        const fileMatrix = new THREE.Matrix4();
        const fileColor = new THREE.Color();
        
        files.forEach((f, i) => {{
            fileMatrix.setPosition(f.x, f.y, f.z);
            
            fileColor.set(f.color);
            fileColors.push(fileColor.r, fileColor.g, fileColor.b);
        }});
        
        // Use BufferGeometry for files
        const filePositions = new Float32Array(files.length * 3);
        const fileColorsBuffer = new Float32Array(files.length * 3);
        
        files.forEach((f, i) => {{
            filePositions[i * 3] = f.x;
            filePositions[i * 3 + 1] = f.y;
            filePositions[i * 3 + 2] = f.z;
            fileColorsBuffer[i * 3] = parseInt(f.color.slice(1, 3), 16) / 255;
            fileColorsBuffer[i * 3 + 1] = parseInt(f.color.slice(3, 5), 16) / 255;
            fileColorsBuffer[i * 3 + 2] = parseInt(f.color.slice(5, 7), 16) / 255;
        }});
        
        const fileBufferGeom = new THREE.BufferGeometry();
        fileBufferGeom.setAttribute('position', new THREE.BufferAttribute(filePositions, 3));
        fileBufferGeom.setAttribute('color', new THREE.BufferAttribute(fileColorsBuffer, 3));
        
        const filePointsMaterial = new THREE.PointsMaterial({{ 
            size: 0.5, 
            vertexColors: true, 
            transparent: true, 
            opacity: 0.7 
        }});
        const filePoints = new THREE.Points(fileBufferGeom, filePointsMaterial);
        fileGroup.add(filePoints);
        
        // Branches
        console.log('Creating branches...');
        const branchMaterial = new THREE.LineBasicMaterial({{ 
            color: 0x00b4d8, 
            transparent: true, 
            opacity: 0.2,
            linewidth: 1
        }});
        
        const branchGeometry = new THREE.BufferGeometry();
        const branchPositions = [];
        
        edges.forEach(e => {{
            if (e.x1 !== undefined && e.x2 !== undefined) {{
                branchPositions.push(e.x1, e.y1, e.z1);
                branchPositions.push(e.x2, e.y2, e.z2);
            }}
        }});
        
        branchGeometry.setAttribute('position', new THREE.Float32BufferAttribute(branchPositions, 3));
        const branches = new THREE.LineSegments(branchGeometry, branchMaterial);
        branchGroup.add(branches);
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        console.log('Tree rendering complete');
        
        // Controls
        document.getElementById('node-size').addEventListener('input', e => {{
            const size = parseFloat(e.target.value);
            document.getElementById('node-size-value').textContent = size.toFixed(1);
            
            directories.forEach((d, i) => {{
                const scale = Math.max(0.3, size - d.depth * 0.05);
                dirMatrix.makeScale(scale, scale, scale);
                dirMatrix.setPosition(d.x, d.y, d.z);
                dirInstanced.setMatrixAt(i, dirMatrix);
            }});
            dirInstanced.instanceMatrix.needsUpdate = true;
        }});
        
        document.getElementById('branch-opacity').addEventListener('input', e => {{
            const opacity = parseFloat(e.target.value);
            document.getElementById('branch-opacity-value').textContent = opacity.toFixed(1);
            branchMaterial.opacity = opacity;
        }});
        
        document.getElementById('show-files').addEventListener('change', e => {{
            fileGroup.visible = e.target.checked;
        }});
        
        document.getElementById('show-branches').addEventListener('change', e => {{
            branchGroup.visible = e.target.checked;
        }});
        
        // Raycaster
        const raycaster = new THREE.Raycaster();
        raycaster.params.Points.threshold = 1;
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        
        renderer.domElement.addEventListener('mousemove', e => {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObject(dirInstanced);
            
            if (intersects.length > 0) {{
                const instanceId = intersects[0].instanceId;
                const d = directories[instanceId];
                if (d) {{
                    tooltip.style.display = 'block';
                    tooltip.style.left = (e.clientX + 15) + 'px';
                    tooltip.style.top = (e.clientY + 15) + 'px';
                    tooltip.querySelector('.name').textContent = d.name;
                    tooltip.querySelector('.path').textContent = d.path || 'Root';
                    tooltip.querySelector('.type').textContent = 'Directory';
                    tooltip.querySelector('.type').style.color = '#ff6b35';
                }}
            }} else {{
                tooltip.style.display = 'none';
            }}
        }});
        
        // Animation
        function animate() {{
            requestAnimationFrame(animate);
            particles.rotation.y += 0.0001;
            controls.update();
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
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"HTML written to {output_path}")


if __name__ == '__main__':
    import sys
    
    # Caminho do grafo
    graph_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.openclaw/workspace/memory/system_graph_compressed.json')
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/.openclaw/workspace/memory/file_tree_full.html')
    
    # Cria árvore
    tree = FullSystemTree3D()
    
    # Carrega do grafo existente
    tree.load_from_graph(graph_path)
    
    # Constrói layout (todos os nós)
    tree.build_tree_layout(sample_ratio=None)
    
    # Gera HTML
    tree.generate_html(output_path)
    
    print(f"\\n=== Full System Tree 3D ===")
    print(f"Nodes: {len(tree.nodes):,}")
    print(f"\\nOpen {output_path} in your browser.")