#!/usr/bin/env python3
"""
FILE SYSTEM TREE 3D
====================
Visualização de sistema de arquivos como ÁRVORE 3D REAL.

Estrutura:
- Raiz no centro/base (tronco)
- Diretórios como ramos que saem do tronco
- Subpastas como galhos menores
- Arquivos como folhas/frutos nos galhos
- Linhas conectando TODOS os níveis

TODOS os arquivos visíveis.
"""

import json
import os
import hashlib
import math
from pathlib import Path
from collections import defaultdict

class FileSystemTree3D:
    """
    Visualização como Árvore 3D.
    
    Layout:
    - Raiz = centro (0, 0, 0)
    - Diretórios principais = ramos principais (cone)
    - Subpastas = galhos menores (cone)
    - Arquivos = folhas (esferas pequenas)
    - Linhas = conexões pai-filho (tubos)
    """
    
    def __init__(self):
        self.files = []
        self.directories = []
        self.path_to_node = {}
        self.id_to_node = {}
        self.tree = {}  # tree[parent_id] = [child_ids]
        
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
            '.gif': '#ff69b4',
        }
    
    def index_filesystem(self, root_paths, max_files=None):
        """Indexa TODO o sistema de arquivos."""
        print(f"Indexing filesystem as tree...")
        print(f"  Root paths: {root_paths}")
        print(f"  Max files: {max_files or 'ALL'}")
        
        file_count = 0
        dir_count = 0
        
        for root_path in root_paths:
            if not os.path.exists(root_path):
                continue
            
            # Raiz
            root_name = os.path.basename(root_path) or root_path
            root_node = {
                'id': f'root_{dir_count}',
                'path': root_path,
                'name': root_name,
                'type': 'root',
                'depth': 0,
                'parent': None,
                'parent_id': None,
                'children': [],
                'is_root': True
            }
            self.directories.append(root_node)
            self.path_to_node[root_path] = root_node
            self.id_to_node[root_node['id']] = root_node
            dir_count += 1
            
            # Caminha recursivamente
            for dirpath, dirnames, filenames in os.walk(root_path):
                # Ignora ocultos e comuns
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 
                              d not in {'node_modules', '__pycache__', '.venv', 'venv', 
                                       'build', 'dist', '.git', '.cache', 'env',
                                       'site-packages', '.mypy_cache', '.pytest_cache',
                                       'miniforge3', 'miniconda3', '.conda', '.npm',
                                       '.cargo', '.rustup', '.local'}]
                
                # Diretório
                parent_path = os.path.dirname(dirpath)
                parent_node = self.path_to_node.get(parent_path)
                
                if parent_node is None:
                    continue
                
                dir_name = os.path.basename(dirpath)
                dir_node = {
                    'id': f'dir_{dir_count}',
                    'path': dirpath,
                    'name': dir_name,
                    'type': 'directory',
                    'depth': dirpath.count(os.sep) - root_path.count(os.sep) + 1,
                    'parent': parent_path,
                    'parent_id': parent_node['id'],
                    'children': []
                }
                self.directories.append(dir_node)
                self.path_to_node[dirpath] = dir_node
                self.id_to_node[dir_node['id']] = dir_node
                
                # Adiciona à árvore
                if parent_node['id'] not in self.tree:
                    self.tree[parent_node['id']] = []
                self.tree[parent_node['id']].append(dir_node['id'])
                
                dir_count += 1
                
                # Arquivos
                for filename in filenames:
                    if max_files and file_count >= max_files:
                        break
                    
                    filepath = os.path.join(dirpath, filename)
                    
                    try:
                        stat = os.stat(filepath)
                        ext = os.path.splitext(filename)[1].lower()
                        
                        file_node = {
                            'id': f'file_{file_count}',
                            'path': filepath,
                            'name': filename,
                            'type': 'file',
                            'ext': ext,
                            'size': stat.st_size,
                            'depth': dirpath.count(os.sep) - root_path.count(os.sep) + 2,
                            'parent': dirpath,
                            'parent_id': dir_node['id']
                        }
                        
                        self.files.append(file_node)
                        self.path_to_node[filepath] = file_node
                        self.id_to_node[file_node['id']] = file_node
                        
                        # Adiciona à árvore
                        if dir_node['id'] not in self.tree:
                            self.tree[dir_node['id']] = []
                        self.tree[dir_node['id']].append(file_node['id'])
                        
                        file_count += 1
                        
                    except (OSError, IOError, PermissionError):
                        continue
                
                if max_files and file_count >= max_files:
                    break
        
        print(f"Indexed {file_count:,} files, {dir_count:,} directories")
        return file_count, dir_count
    
    def build_tree_layout(self):
        """
        Constrói layout de ÁRVORE 3D.
        
        Estrutura:
        - Raiz no centro (0, 0, 0)
        - Diretórios como ramos em espiral
        - Subpastas como galhos menores
        - Arquivos como folhas nos galhos
        """
        print("Building 3D tree layout...")
        
        # Encontra raízes
        roots = [d for d in self.directories if d.get('is_root')]
        
        if not roots:
            print("No roots found!")
            return
        
        # Posiciona raízes
        for i, root in enumerate(roots):
            # Raízes em círculo no centro
            angle = (2 * math.pi * i / len(roots)) if len(roots) > 1 else 0
            root['x'] = 0
            root['y'] = 0
            root['z'] = 0
            root['branch_angle'] = angle
            root['branch_length'] = 0
        
        # Posiciona recursivamente
        for root in roots:
            self._position_tree_node(root, start_angle=root.get('branch_angle', 0))
        
        print(f"Tree layout built: {len(self.directories)} dirs, {len(self.files)} files")
    
    def _position_tree_node(self, node, start_angle=0, depth=0, parent_pos=(0, 0, 0)):
        """
        Posiciona nó da árvore recursivamente.
        
        Layout de árvore:
        - Cada diretório é um ramo
        - Ângulo distribuído entre filhos
        - Comprimento diminui com profundidade
        """
        # Pega filhos
        child_ids = self.tree.get(node['id'], [])
        dir_children = [self.id_to_node[cid] for cid in child_ids 
                       if cid.startswith('dir_') and cid in self.id_to_node]
        file_children = [self.id_to_node[cid] for cid in child_ids 
                        if cid.startswith('file_') and cid in self.id_to_node]
        
        # Número de filhos
        n_dirs = len(dir_children)
        n_files = len(file_children)
        n_total = n_dirs + n_files
        
        if n_total == 0:
            return
        
        # Posição do nó atual
        x, y, z = node.get('x', 0), node.get('y', 0), node.get('z', 0)
        
        # Parâmetros do ramo
        branch_length = max(2, 5 - depth * 0.5)  # Comprimento diminui com profundidade
        branch_angle_spread = math.pi * 0.6  # Ângulo de abertura
        
        # Posiciona diretórios filhos (ramos)
        for i, child in enumerate(dir_children):
            # Ângulo distribuído
            if n_dirs > 1:
                angle = start_angle + (branch_angle_spread * (i / (n_dirs - 1) - 0.5))
            else:
                angle = start_angle
            
            # Comprimento do ramo
            length = branch_length * (1 - depth * 0.1)
            
            # Posição 3D (ramo saindo do nó)
            child_x = x + length * math.cos(angle)
            child_y = y + length * 0.3 + depth * 0.5  # Sob sobe com profundidade
            child_z = z + length * math.sin(angle)
            
            child['x'] = child_x
            child['y'] = child_y
            child['z'] = child_z
            child['branch_angle'] = angle
            
            # Recursão
            self._position_tree_node(child, start_angle=angle, depth=depth+1, 
                                     parent_pos=(x, y, z))
        
        # Posiciona arquivos filhos (folhas)
        file_radius = 0.5 + depth * 0.2
        
        for i, child in enumerate(file_children):
            # Ângulo distribuído em círculo
            file_angle = (2 * math.pi * i / n_files) if n_files > 1 else 0
            
            # Posição próxima ao diretório pai
            child_x = x + file_radius * math.cos(file_angle)
            child_y = y + 0.2  # Ligeiramente acima
            child_z = z + file_radius * math.sin(file_angle)
            
            child['x'] = child_x
            child['y'] = child_y
            child['z'] = child_z
    
    def generate_html(self, output_path):
        """Gera HTML com árvore 3D."""
        
        # Prepara dados
        nodes_json = json.dumps([{
            'id': d['id'],
            'name': d['name'],
            'type': d['type'],
            'x': d.get('x', 0),
            'y': d.get('y', 0),
            'z': d.get('z', 0),
            'depth': d['depth'],
            'parentId': d.get('parent_id')
        } for d in self.directories] + [{
            'id': f['id'],
            'name': f['name'],
            'type': 'file',
            'ext': f['ext'],
            'x': f.get('x', 0),
            'y': f.get('y', 0),
            'z': f.get('z', 0),
            'depth': f['depth'],
            'parentId': f['parent_id'],
            'color': self.ext_colors.get(f['ext'], '#666666')
        } for f in self.files])
        
        # Conexões
        edges = []
        for parent_id, child_ids in self.tree.items():
            parent = self.id_to_node.get(parent_id)
            if parent:
                for child_id in child_ids:
                    child = self.id_to_node.get(child_id)
                    if child:
                        edges.append({
                            'x1': parent.get('x', 0),
                            'y1': parent.get('y', 0),
                            'z1': parent.get('z', 0),
                            'x2': child.get('x', 0),
                            'y2': child.get('y', 0),
                            'z2': child.get('z', 0),
                            'type': 'dir-file' if child_id.startswith('file_') else 'dir-dir'
                        })
        
        edges_json = json.dumps(edges)
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>File System Tree 3D</title>
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
            max-width: 350px;
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
        input[type="range"] {{
            width: 150px;
        }}
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
    <div id="loading">Building tree with {len(self.directories):,} nodes and {len(self.files):,} leaves...</div>
    
    <div id="info">
        <h2>File System Tree 3D</h2>
        <div id="stats">
            <div><span class="stat-label">Roots:</span> <span class="stat-value">{len([d for d in self.directories if d.get('is_root')])}</span></div>
            <div><span class="stat-label">Directories:</span> <span class="stat-value">{len(self.directories):,}</span></div>
            <div><span class="stat-label">Files:</span> <span class="stat-value">{len(self.files):,}</span></div>
            <div><span class="stat-label">Connections:</span> <span class="stat-value">{len(edges):,}</span></div>
        </div>
    </div>
    
    <div id="controls">
        <h3>Tree Controls</h3>
        <div class="control-row">
            <span class="control-label">Node Size:</span>
            <input type="range" id="node-size" min="0.1" max="3" step="0.1" value="1">
            <span class="control-value" id="node-size-value">1.0</span>
        </div>
        <div class="control-row">
            <span class="control-label">Branch Width:</span>
            <input type="range" id="branch-width" min="0.5" max="5" step="0.5" value="2">
            <span class="control-value" id="branch-width-value">2.0</span>
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
        <div="legend-item"><div class="legend-dot" style="background:#00b4d8"></div>Config/JSON</div>
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
        const nodes = {nodes_json};
        const edges = {edges_json};
        
        const directories = nodes.filter(n => n.type === 'directory' || n.type === 'root');
        const files = nodes.filter(n => n.type === 'file');
        
        console.log('Directories:', directories.length);
        console.log('Files:', files.length);
        console.log('Edges:', edges.length);
        
        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050510);
        
        // Add ambient particles (like stars)
        const particleGeometry = new THREE.BufferGeometry();
        const particleCount = 5000;
        const positions = new Float32Array(particleCount * 3);
        for (let i = 0; i < particleCount * 3; i += 3) {{
            positions[i] = (Math.random() - 0.5) * 1000;
            positions[i + 1] = (Math.random() - 0.5) * 1000;
            positions[i + 2] = (Math.random() - 0.5) * 1000;
        }}
        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const particleMaterial = new THREE.PointsMaterial({{ color: 0x00ff87, size: 0.5, transparent: true, opacity: 0.3 }});
        const particles = new THREE.Points(particleGeometry, particleMaterial);
        scene.add(particles);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 5000);
        camera.position.set(0, 50, 100);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true, powerPreference: 'high-performance' }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Controls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 5;
        controls.maxDistance = 500;
        
        // Groups
        const dirGroup = new THREE.Group();
        const fileGroup = new THREE.Group();
        const branchGroup = new THREE.Group();
        scene.add(dirGroup);
        scene.add(fileGroup);
        scene.add(branchGroup);
        
        // Directories as nodes (spheres)
        console.log('Creating directory nodes...');
        const dirGeometry = new THREE.SphereGeometry(1, 16, 16);
        const dirMaterial = new THREE.MeshBasicMaterial({{ color: 0xff6b35, transparent: true, opacity: 0.8 }});
        const dirInstanced = new THREE.InstancedMesh(dirGeometry, dirMaterial, directories.length);
        
        const dirMatrix = new THREE.Matrix4();
        const dirScale = new THREE.Vector3(1, 1, 1);
        
        directories.forEach((d, i) => {{
            // Scale based on depth (larger at root)
            const scale = Math.max(0.3, 1.5 - d.depth * 0.1);
            dirScale.set(scale, scale, scale);
            dirMatrix.makeScale(scale, scale, scale);
            dirMatrix.setPosition(d.x, d.y, d.z);
            dirInstanced.setMatrixAt(i, dirMatrix);
        }});
        
        dirInstanced.instanceMatrix.needsUpdate = true;
        dirGroup.add(dirInstanced);
        
        // Files as leaves (smaller spheres with colors)
        console.log('Creating file leaves...');
        const fileGeometry = new THREE.SphereGeometry(0.3, 8, 8);
        const fileMaterial = new THREE.MeshBasicMaterial({{ color: 0x666666, transparent: true, opacity: 0.7 }});
        const fileInstanced = new THREE.InstancedMesh(fileGeometry, fileMaterial, files.length);
        
        const fileMatrix = new THREE.Matrix4();
        const fileColor = new THREE.Color();
        
        files.forEach((f, i) => {{
            fileMatrix.setPosition(f.x, f.y, f.z);
            fileInstanced.setMatrixAt(i, fileMatrix);
            
            fileColor.set(f.color);
            fileInstanced.setColorAt(i, fileColor);
        }});
        
        fileInstanced.instanceMatrix.needsUpdate = true;
        if (fileInstanced.instanceColor) fileInstanced.instanceColor.needsUpdate = true;
        fileGroup.add(fileInstanced);
        
        // Branches (lines connecting nodes)
        console.log('Creating branches...');
        const branchMaterial = new THREE.LineBasicMaterial({{ 
            color: 0x00b4d8, 
            transparent: true, 
            opacity: 0.4,
            linewidth: 2
        }});
        
        const branchGeometry = new THREE.BufferGeometry();
        const branchPositions = [];
        
        edges.forEach(e => {{
            branchPositions.push(e.x1, e.y1, e.z1);
            branchPositions.push(e.x2, e.y2, e.z2);
        }});
        
        branchGeometry.setAttribute('position', new THREE.Float32BufferAttribute(branchPositions, 3));
        const branches = new THREE.LineSegments(branchGeometry, branchMaterial);
        branchGroup.add(branches);
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        
        console.log('Tree rendering complete');
        
        // Raycaster
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        
        // Find closest node
        function findClosestNode(x, y, z, threshold = 3) {{
            let closest = null;
            let minDist = threshold;
            
            for (const d of directories) {{
                const dx = d.x - x;
                const dy = d.y - y;
                const dz = d.z - z;
                const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
                if (dist < minDist) {{
                    minDist = dist;
                    closest = d;
                }}
            }}
            
            for (const f of files) {{
                const dx = f.x - x;
                const dy = f.y - y;
                const dz = f.z - z;
                const dist = Math.sqrt(dx*dx + dy*dz + dz*dz);
                if (dist < minDist) {{
                    minDist = dist;
                    closest = f;
                }}
            }}
            
            return closest;
        }}
        
        // Mouse interaction
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
                    tooltip.querySelector('.type').textContent = d.type === 'root' ? 'Root Directory' : 'Directory';
                    tooltip.querySelector('.type').style.color = '#ff6b35';
                }}
            }} else {{
                // Check files
                const fileIntersects = raycaster.intersectObject(fileInstanced);
                if (fileIntersects.length > 0) {{
                    const instanceId = fileIntersects[0].instanceId;
                    const f = files[instanceId];
                    if (f) {{
                        tooltip.style.display = 'block';
                        tooltip.style.left = (e.clientX + 15) + 'px';
                        tooltip.style.top = (e.clientY + 15) + 'px';
                        tooltip.querySelector('.name').textContent = f.name;
                        tooltip.querySelector('.path').textContent = f.path || '';
                        tooltip.querySelector('.type').textContent = 'File (' + (f.ext || 'unknown') + ')';
                        tooltip.querySelector('.type').style.color = '#00ff87';
                    }}
                }} else {{
                    tooltip.style.display = 'none';
                }}
            }}
        }});
        
        // Controls
        document.getElementById('node-size').addEventListener('input', e => {{
            const size = parseFloat(e.target.value);
            document.getElementById('node-size-value').textContent = size.toFixed(1);
            
            directories.forEach((d, i) => {{
                const scale = Math.max(0.3, size - d.depth * 0.1);
                dirMatrix.makeScale(scale, scale, scale);
                dirMatrix.setPosition(d.x, d.y, d.z);
                dirInstanced.setMatrixAt(i, dirMatrix);
            }});
            dirInstanced.instanceMatrix.needsUpdate = true;
        }});
        
        document.getElementById('branch-width').addEventListener('input', e => {{
            const width = parseFloat(e.target.value);
            document.getElementById('branch-width-value').textContent = width.toFixed(1);
            branchMaterial.opacity = width / 10;
        }});
        
        document.getElementById('show-files').addEventListener('change', e => {{
            fileGroup.visible = e.target.checked;
        }});
        
        document.getElementById('show-branches').addEventListener('change', e => {{
            branchGroup.visible = e.target.checked;
        }});
        
        // Animation
        function animate() {{
            requestAnimationFrame(animate);
            
            // Slowly rotate particles
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
    
    # Cria árvore
    tree = FileSystemTree3D()
    
    # Indexa sistema de arquivos COMPLETO
    root_paths = [
        os.path.expanduser('~/.openclaw/workspace'),
        os.path.expanduser('~/Documents'),
    ]
    
    file_count, dir_count = tree.index_filesystem(root_paths, max_files=None)
    
    # Constrói layout de árvore
    tree.build_tree_layout()
    
    # Gera HTML
    output_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.openclaw/workspace/memory/file_tree_3d.html')
    tree.generate_html(output_path)
    
    print(f"\\n=== File System Tree 3D ===")
    print(f"Nodes: {dir_count:,} directories")
    print(f"Leaves: {file_count:,} files")
    print(f"Branches: {len(tree.tree):,} connections")
    print(f"\\nOpen {output_path} in your browser.")