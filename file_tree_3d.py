#!/usr/bin/env python3
"""
FILE SYSTEM TREE 3D - FULL SYSTEM
==================================
Visualização COMPLETA do sistema como ÁRVORE 3D.

Estrutura:
- Raiz no centro (tronco)
- Diretórios como ramos (esferas laranja)
- Subpastas como galhos menores
- Arquivos como folhas (esferas coloridas)
- Linhas conectando TODOS os níveis

ESPAÇAMENTO:
- Nós igualmente espaçados para evitar sobreposição
- Layout em cone/hiperbólico
- Distribuição angular uniforme

TODOS os arquivos do sistema.
"""

import os
import math
import json
from collections import defaultdict

class FileSystemTree3D:
    """
    Visualização como Árvore 3D com espaçamento uniforme.
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
            '.log': '#666666',
            '.so': '#9370db',
            '.a': '#9370db',
            '.o': '#9370db',
        }
        
        # Diretórios a ignorar
        self.skip_dirs = {
            'node_modules', '__pycache__', '.git', '.svn', '.hg',
            'venv', '.venv', 'env', 'build', 'dist', '.cache',
            '.mypy_cache', '.pytest_cache', 'miniforge3', 'miniconda3',
            '.conda', '.npm', '.cargo', '.rustup', '.local', 'site-packages',
            'miniconda3', '.mozilla', '.cache', 'cache', 'Cache',
            '.config', '.var', 'run', 'tmp', 'proc', 'sys', 'dev',
        }
    
    def index_filesystem(self, root_paths, max_files=None):
        """Indexa TODO o sistema de arquivos."""
        print(f"Indexing filesystem...")
        print(f"  Root paths: {root_paths}")
        print(f"  Max files: {max_files or 'ALL'}")
        
        file_count = 0
        dir_count = 0
        
        for root_path in root_paths:
            if not os.path.exists(root_path):
                print(f"  Skipping (not found): {root_path}")
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
            try:
                for dirpath, dirnames, filenames in os.walk(root_path):
                    # Ignora ocultos e comuns
                    dirnames[:] = [d for d in dirnames if not d.startswith('.') 
                                  and d not in self.skip_dirs]
                    
                    # Diretório atual
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
                        if filename.startswith('.'):
                            continue
                        
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
                        
            except PermissionError:
                print(f"  Permission denied: {root_path}")
        
        print(f"Indexed {file_count:,} files, {dir_count:,} directories")
        return file_count, dir_count
    
    def build_tree_layout(self):
        """
        Constrói layout de ÁRVORE 3D com ESPAÇAMENTO UNIFORME.
        
        Algoritmo:
        - Raiz no centro (0, 0, 0)
        - Filhos distribuídos em CONE ao redor do pai
        - Ângulo dividido igualmente entre filhos
        - Raio aumenta com profundidade
        - Altura aumenta com profundidade
        """
        print("Building 3D tree layout with UNIFORM SPACING...")
        
        # Encontra raízes
        roots = [d for d in self.directories if d.get('is_root')]
        
        if not roots:
            print("No roots found!")
            return
        
        print(f"Found {len(roots)} roots")
        
        # Posiciona raízes em círculo no centro
        for i, root in enumerate(roots):
            angle = (2 * math.pi * i / len(roots)) if len(roots) > 1 else 0
            root['x'] = 0
            root['y'] = 0
            root['z'] = 0
            root['placed'] = True
        
        # Processa recursivamente com espaçamento uniforme
        for root in roots:
            self._position_children_uniform(root)
        
        placed = sum(1 for n in self.directories if n.get('placed'))
        placed += sum(1 for n in self.files if n.get('placed'))
        print(f"Placed {placed:,} nodes")
    
    def _position_children_uniform(self, node):
        """
        Posiciona filhos com espaçamento UNIFORME em formato de CONE.
        
        Cada filho recebe uma fatia angular igual.
        Raio proporcional ao número de filhos.
        """
        # Pega filhos
        child_ids = self.tree.get(node['id'], [])
        
        if not child_ids:
            return
        
        dir_children = [self.id_to_node[cid] for cid in child_ids 
                       if cid.startswith('dir_') and cid in self.id_to_node]
        file_children = [self.id_to_node[cid] for cid in child_ids 
                        if cid.startswith('file_') and cid in self.id_to_node]
        
        n_dirs = len(dir_children)
        n_files = len(file_children)
        
        # Posição do nó atual
        x, y, z = node.get('x', 0), node.get('y', 0), node.get('z', 0)
        depth = node.get('depth', 0)
        
        # Parâmetros de espaçamento
        # Raio base aumenta com profundidade (cada nível mais aberto)
        base_radius = 3 + depth * 2
        
        # Posiciona diretórios filhos em CONE
        for i, child in enumerate(dir_children):
            # Ângulo igualmente distribuído
            if n_dirs > 1:
                angle = (2 * math.pi * i / n_dirs)
            else:
                angle = 0
            
            # Raio do cone (maior para mais filhos)
            radius = base_radius * max(1, math.sqrt(n_dirs) * 0.5)
            
            # Posição no cone
            child_x = x + radius * math.cos(angle)
            child_y = y + 2  # Sob sobe (cada nível sobe)
            child_z = z + radius * math.sin(angle)
            
            child['x'] = child_x
            child['y'] = child_y
            child['z'] = child_z
            child['placed'] = True
            
            # Recursão
            self._position_children_uniform(child)
        
        # Posiciona arquivos filhos em ESFERA ao redor do diretório
        file_radius = 1.5 + math.sqrt(n_files) * 0.3
        
        for i, child in enumerate(file_children):
            # Distribui em esfera (não círculo!)
            phi = math.acos(1 - 2 * (i + 0.5) / n_files) if n_files > 1 else 0
            theta = math.pi * (1 + 5**0.5) * i  # Golden angle para distribuição uniforme
            
            child_x = x + file_radius * math.sin(phi) * math.cos(theta)
            child_y = y + 0.5 + file_radius * math.cos(phi)
            child_z = z + file_radius * math.sin(phi) * math.sin(theta)
            
            child['x'] = child_x
            child['y'] = child_y
            child['z'] = child_z
            child['placed'] = True
    
    def generate_html(self, output_path):
        """Gera HTML com árvore 3D."""
        
        # Filtra nós posicionados
        placed_dirs = [d for d in self.directories if d.get('placed')]
        placed_files = [f for f in self.files if f.get('placed')]
        
        print(f"Generating HTML...")
        print(f"  Directories: {len(placed_dirs):,}")
        print(f"  Files: {len(placed_files):,}")
        
        # Prepara dados para JSON
        dirs_json = json.dumps([{
            'id': d['id'],
            'name': d['name'],
            'path': d['path'],
            'x': d.get('x', 0),
            'y': d.get('y', 0),
            'z': d.get('z', 0),
            'depth': d['depth'],
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
            'depth': f['depth'],
            'color': self.ext_colors.get(f.get('ext', ''), '#666666')
        } for f in placed_files])
        
        # Conexões
        edges = []
        for parent_id, child_ids in self.tree.items():
            parent = self.id_to_node.get(parent_id)
            if parent and parent.get('placed'):
                for child_id in child_ids:
                    child = self.id_to_node.get(child_id)
                    if child and child.get('placed'):
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
        <h2>File System Tree 3D</h2>
        <div id="stats">
            <div><span class="stat-label">Roots:</span> <span class="stat-value">{len([d for d in placed_dirs if d.get('is_root')])}</span></div>
            <div><span class="stat-label">Directories:</span> <span class="stat-value">{len(placed_dirs):,}</span></div>
            <div><span class="stat-label">Files:</span> <span class="stat-value">{len(placed_files):,}</span></div>
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
            <span class="control-label">Branch Opacity:</span>
            <input type="range" id="branch-opacity" min="0" max="1" step="0.1" value="0.4">
            <span class="control-value" id="branch-opacity-value">0.4</span>
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
        < class="legend-item"><div class="legend-dot" style="background:#00b4d8"></div>Config/JSON</div>
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
        const particleCount = 5000;
        const positions = new Float32Array(particleCount * 3);
        for (let i = 0; i < particleCount * 3; i += 3) {{
            positions[i] = (Math.random() - 0.5) * 2000;
            positions[i + 1] = (Math.random() - 0.5) * 2000;
            positions[i + 2] = (Math.random() - 0.5) * 2000;
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
        
        // Directories as spheres (instanced)
        console.log('Creating directory nodes...');
        const dirGeometry = new THREE.SphereGeometry(1, 16, 16);
        const dirMaterial = new THREE.MeshBasicMaterial({{ color: 0xff6b35, transparent: true, opacity: 0.8 }});
        const dirInstanced = new THREE.InstancedMesh(dirGeometry, dirMaterial, directories.length);
        
        const dirMatrix = new THREE.Matrix4();
        const dirScale = new THREE.Vector3();
        
        directories.forEach((d, i) => {{
            // Scale based on depth (larger at root)
            const scale = Math.max(0.5, 2 - d.depth * 0.1);
            dirScale.set(scale, scale, scale);
            dirMatrix.makeScale(scale, scale, scale);
            dirMatrix.setPosition(d.x, d.y, d.z);
            dirInstanced.setMatrixAt(i, dirMatrix);
        }});
        
        dirInstanced.instanceMatrix.needsUpdate = true;
        dirGroup.add(dirInstanced);
        
        // Files as points (GPU-efficient)
        console.log('Creating file leaves...');
        const filePositions = new Float32Array(files.length * 3);
        const fileColors = new Float32Array(files.length * 3);
        
        files.forEach((f, i) => {{
            filePositions[i * 3] = f.x;
            filePositions[i * 3 + 1] = f.y;
            filePositions[i * 3 + 2] = f.z;
            
            // Parse color
            const color = f.color || '#666666';
            fileColors[i * 3] = parseInt(color.slice(1, 3), 16) / 255;
            fileColors[i * 3 + 1] = parseInt(color.slice(3, 5), 16) / 255;
            fileColors[i * 3 + 2] = parseInt(color.slice(5, 7), 16) / 255;
        }});
        
        const fileGeometry = new THREE.BufferGeometry();
        fileGeometry.setAttribute('position', new THREE.BufferAttribute(filePositions, 3));
        fileGeometry.setAttribute('color', new THREE.BufferAttribute(fileColors, 3));
        
        const fileMaterial = new THREE.PointsMaterial({{ 
            size: 0.4, 
            vertexColors: true, 
            transparent: true, 
            opacity: 0.7 
        }});
        const filePoints = new THREE.Points(fileGeometry, fileMaterial);
        fileGroup.add(filePoints);
        
        // Branches (lines connecting nodes)
        console.log('Creating branches...');
        const branchMaterial = new THREE.LineBasicMaterial({{ 
            color: 0x00b4d8, 
            transparent: true, 
            opacity: 0.4,
            linewidth: 1
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
        
        // Controls
        document.getElementById('node-size').addEventListener('input', e => {{
            const size = parseFloat(e.target.value);
            document.getElementById('node-size-value').textContent = size.toFixed(1);
            
            directories.forEach((d, i) => {{
                const scale = Math.max(0.5, size - d.depth * 0.05);
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
    
    # Indexa TODO o sistema
    root_paths = [
        os.path.expanduser('~'),  # Home completo
        '/',  # Raiz do sistema
    ]
    
    # Limita para evitar travar (pode aumentar se quiser)
    max_files = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    
    file_count, dir_count = tree.index_filesystem(root_paths, max_files=max_files)
    
    # Constrói layout com espaçamento uniforme
    tree.build_tree_layout()
    
    # Gera HTML
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/.openclaw/workspace/memory/file_tree_full.html')
    tree.generate_html(output_path)
    
    print(f"\\n=== File System Tree 3D ===")
    print(f"Directories: {dir_count:,}")
    print(f"Files: {file_count:,}")
    print(f"\\nOpen {output_path} in your browser.")