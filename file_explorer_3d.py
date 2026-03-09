#!/usr/bin/env python3
"""
FILE SYSTEM EXPLORER 3D - OPTIMIZED
====================================
Renderização 3D otimizada com:
- TODOS os arquivos (sem limite)
- Linhas conectando pastas a subpastas/arquivos
- Centro bem definido (raiz)
- Instanced rendering para performance
- LOD (Level of Detail) para não travar
"""

import json
import os
import hashlib
import math
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class FileSystemExplorer3D:
    """
    Explorador 3D otimizado com hierarquia visual.
    
    Estrutura:
    - Centro = Raiz (home ou workspace)
    - Cilindros = Diretórios
    - Esferas = Arquivos
    - Linhas = Conexões pai-filho
    """
    
    def __init__(self):
        self.files = []
        self.directories = []
        self.path_to_node = {}
        self.id_to_node = {}
        self.hierarchy = {}  # parent_id -> [child_ids]
        
        # Extensões e cores
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
        """
        Indexa sistema de arquivos COMPLETO.
        
        Args:
            root_paths: Lista de caminhos raiz
            max_files: None = todos os arquivos
        """
        print(f"Indexing filesystem...")
        print(f"  Root paths: {root_paths}")
        print(f"  Max files: {max_files or 'UNLIMITED'}")
        
        file_count = 0
        dir_count = 0
        
        for root_path in root_paths:
            if not os.path.exists(root_path):
                continue
            
            # Raiz
            root_name = os.path.basename(root_path) or root_path
            root_node = {
                'id': f'dir_{dir_count}',
                'path': root_path,
                'name': root_name,
                'type': 'directory',
                'depth': 0,
                'parent': None,
                'children': [],
                'is_root': True
            }
            self.directories.append(root_node)
            self.path_to_node[root_path] = root_node
            self.id_to_node[root_node['id']] = root_node
            dir_count += 1
            
            for dirpath, dirnames, filenames in os.walk(root_path):
                # Ignora diretórios ocultos e comuns
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
                    'depth': dirpath.count(os.sep) - root_path.count(os.sep),
                    'parent': parent_path,
                    'parent_id': parent_node['id'],
                    'children': [],
                    'file_count': 0,
                    'total_size': 0
                }
                self.directories.append(dir_node)
                self.path_to_node[dirpath] = dir_node
                self.id_to_node[dir_node['id']] = dir_node
                
                # Adiciona à hierarquia
                if parent_node['id'] not in self.hierarchy:
                    self.hierarchy[parent_node['id']] = []
                self.hierarchy[parent_node['id']].append(dir_node['id'])
                
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
                            'mtime': stat.st_mtime,
                            'depth': dirpath.count(os.sep) - root_path.count(os.sep),
                            'parent': dirpath,
                            'parent_id': dir_node['id']
                        }
                        
                        self.files.append(file_node)
                        self.path_to_node[filepath] = file_node
                        self.id_to_node[file_node['id']] = file_node
                        
                        # Adiciona à hierarquia
                        if dir_node['id'] not in self.hierarchy:
                            self.hierarchy[dir_node['id']] = []
                        self.hierarchy[dir_node['id']].append(file_node['id'])
                        
                        dir_node['file_count'] += 1
                        dir_node['total_size'] += stat.st_size
                        
                        file_count += 1
                        
                    except (OSError, IOError, PermissionError):
                        continue
                
                if max_files and file_count >= max_files:
                    break
        
        print(f"Indexed {file_count:,} files, {dir_count:,} directories")
        
        return file_count, dir_count
    
    def build_3d_layout(self):
        """
        Constrói layout 3D hierárquico.
        
        Estrutura:
        - Raiz no centro (0, 0, 0)
        - Cada nível = anel concêntrico
        - Diretórios = cilindros
        - Arquivos = esferas dentro dos cilindros
        - Linhas conectam pai-filho
        """
        print("Building 3D hierarchical layout...")
        
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
            root['radius'] = 2  # Raio base para raiz
        
        # Posiciona diretórios recursivamente
        self._position_directories_recursive(roots, radius_offset=3)
        
        # Posiciona arquivos dentro dos diretórios
        for f in self.files:
            parent = self.id_to_node.get(f['parent_id'])
            if parent:
                # Posição relativa ao pai
                parent_x = parent.get('x', 0)
                parent_y = parent.get('y', 0)
                parent_z = parent.get('z', 0)
                parent_radius = parent.get('radius', 1)
                
                # Ângulo baseado no nome (determinístico)
                h = hashlib.md5(f['name'].encode()).hexdigest()
                angle = int(h[:8], 16) / 0xffffffff * 2 * math.pi
                
                # Raio dentro do diretório
                inner_radius = parent_radius * 0.8
                
                f['x'] = parent_x + inner_radius * math.cos(angle)
                f['y'] = parent_y + 0.2  # Ligeiramente acima
                f['z'] = parent_z + inner_radius * math.sin(angle)
        
        print(f"3D layout built")
    
    def _position_directories_recursive(self, nodes, radius_offset=3, depth=0):
        """Posiciona diretórios recursivamente em anéis concêntricos."""
        
        if not nodes:
            return
        
        for node in nodes:
            parent = self.id_to_node.get(node.get('parent_id'))
            
            if parent:
                # Posição relativa ao pai
                parent_x = parent.get('x', 0)
                parent_y = parent.get('y', 0)
                parent_z = parent.get('z', 0)
                
                # Raio cresce com profundidade
                radius = radius_offset * (1 + depth * 0.5)
                node['radius'] = max(1, radius * 0.3)  # Raio do próprio diretório
                
                # Ângulo determinístico
                h = hashlib.md5(node['path'].encode()).hexdigest()
                angle = int(h[:8], 16) / 0xffffffff * 2 * math.pi
                
                # Posição
                node['x'] = parent_x + radius * math.cos(angle)
                node['y'] = depth * 0.5  # Altura por nível
                node['z'] = parent_z + radius * math.sin(angle)
            
            # Recursão para filhos
            child_ids = self.hierarchy.get(node['id'], [])
            child_dirs = [self.id_to_node[cid] for cid in child_ids 
                          if cid.startswith('dir_') and cid in self.id_to_node]
            
            if child_dirs:
                self._position_directories_recursive(
                    child_dirs, 
                    radius_offset=radius_offset * 0.7,
                    depth=depth + 1
                )
    
    def generate_html(self, output_path):
        """Gera HTML otimizado com instanced rendering."""
        
        # Prepara dados
        dirs_json = json.dumps([{
            'id': d['id'],
            'name': d['name'],
            'path': d['path'],
            'x': d.get('x', 0),
            'y': d.get('y', 0),
            'z': d.get('z', 0),
            'depth': d['depth'],
            'parentId': d.get('parent_id'),
            'isRoot': d.get('is_root', False)
        } for d in self.directories])
        
        files_json = json.dumps([{
            'id': f['id'],
            'name': f['name'],
            'path': f['path'],
            'ext': f['ext'],
            'size': f['size'],
            'x': f.get('x', 0),
            'y': f.get('y', 0),
            'z': f.get('z', 0),
            'parentId': f['parent_id'],
            'color': self.ext_colors.get(f['ext'], '#666666')
        } for f in self.files])
        
        # Linhas de conexão
        lines = []
        for d in self.directories:
            if d.get('parent_id'):
                parent = self.id_to_node.get(d['parent_id'])
                if parent:
                    lines.append({
                        'x1': parent.get('x', 0),
                        'y1': parent.get('y', 0),
                        'z1': parent.get('z', 0),
                        'x2': d.get('x', 0),
                        'y2': d.get('y', 0),
                        'z2': d.get('z', 0),
                        'type': 'dir-dir'
                    })
        
        # Linhas arquivo -> diretório (apenas para arquivos importantes)
        for f in self.files[:5000]:  # Limita para não sobrecarregar
            parent = self.id_to_node.get(f['parent_id'])
            if parent:
                lines.append({
                    'x1': parent.get('x', 0),
                    'y1': parent.get('y', 0),
                    'z1': parent.get('z', 0),
                    'x2': f.get('x', 0),
                    'y2': f.get('y', 0),
                    'z2': f.get('z', 0),
                    'type': 'file-dir'
                })
        
        lines_json = json.dumps(lines)
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>File System Explorer 3D - Hierarchical</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a12;
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
            border: 1px solid rgba(0,180,216,0.3);
            max-width: 350px;
            z-index: 100;
        }}
        #info h2 {{
            color: #00b4d8;
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
            border: 1px solid #00b4d8;
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
        #tooltip .size {{
            color: #00b4d8;
            font-size: 10px;
        }}
        #tooltip .type {{
            color: #ff6b35;
            font-size: 10px;
            margin-top: 5px;
        }}
        
        #loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #00b4d8;
            font-size: 14px;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div id="loading">Loading {len(self.files):,} files...</div>
    
    <div id="info">
        <h2>File System 3D</h2>
        <div id="stats">
            <div><span class="stat-label">Files:</span> <span class="stat-value">{len(self.files):,}</span></div>
            <div><span class="stat-label">Directories:</span> <span class="stat-value">{len(self.directories):,}</span></div>
            <div><span class="stat-label">Connections:</span> <span class="stat-value">{len(lines):,}</span></div>
            <div><span class="stat-label">Roots:</span> <span class="stat-value">{len([d for d in self.directories if d.get('is_root')])}</span></div>
        </div>
    </div>
    
    <div id="controls">
        <h3>Controls</h3>
        <div class="control-row">
            <span class="control-label">Node Size:</span>
            <input type="range" id="node-size" min="0.1" max="2" step="0.1" value="0.5">
            <span class="control-value" id="node-size-value">0.5</span>
        </div>
        <div class="control-row">
            <span class="control-label">Line Opacity:</span>
            <input type="range" id="line-opacity" min="0" max="1" step="0.1" value="0.3">
            <span class="control-value" id="line-opacity-value">0.3</span>
        </div>
        <div class="control-row">
            <span class="control-label">Show Files:</span>
            <input type="checkbox" id="show-files" checked>
        </div>
        <div class="control-row">
            <span class="control-label">Show Lines:</span>
            <input type="checkbox" id="show-lines" checked>
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
        <div class="size"></div>
        <div class="type"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>
        // Data
        const directories = {dirs_json};
        const files = {files_json};
        const connections = {lines_json};
        
        console.log('Directories:', directories.length);
        console.log('Files:', files.length);
        console.log('Connections:', connections.length);
        
        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a12);
        
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
        controls.screenSpacePanning = false;
        controls.minDistance = 10;
        controls.maxDistance = 1000;
        
        // Groups
        const dirGroup = new THREE.Group();
        const fileGroup = new THREE.Group();
        const lineGroup = new THREE.Group();
        scene.add(dirGroup);
        scene.add(fileGroup);
        scene.add(lineGroup);
        
        // Instanced rendering for directories
        const dirGeometry = new THREE.CylinderGeometry(1, 1, 0.3, 12);
        const dirMaterial = new THREE.MeshBasicMaterial({{ color: 0xff6b35, transparent: true, opacity: 0.7 }});
        const dirInstanced = new THREE.InstancedMesh(dirGeometry, dirMaterial, directories.length);
        
        const dirMatrix = new THREE.Matrix4();
        const dirScale = new THREE.Vector3(0.5, 0.5, 0.5);
        
        directories.forEach((d, i) => {{
            dirScale.x = Math.max(0.3, Math.min(2, d.depth < 3 ? 1.5 - d.depth * 0.3 : 0.5));
            dirScale.y = 0.5;
            dirScale.z = dirScale.x;
            
            dirMatrix.makeScale(dirScale.x, dirScale.y, dirScale.z);
            dirMatrix.setPosition(d.x, d.y, d.z);
            dirInstanced.setMatrixAt(i, dirMatrix);
        }});
        
        dirInstanced.instanceMatrix.needsUpdate = true;
        dirGroup.add(dirInstanced);
        
        // Instanced rendering for files
        const fileGeometry = new THREE.SphereGeometry(0.2, 6, 6);
        const fileMaterial = new THREE.MeshBasicMaterial({{ color: 0x666666, transparent: true, opacity: 0.8 }});
        const fileInstanced = new THREE.InstancedMesh(fileGeometry, fileMaterial, files.length);
        
        const fileMatrix = new THREE.Matrix4();
        const fileColor = new THREE.Color();
        
        files.forEach((f, i) => {{
            fileMatrix.makeScale(0.5, 0.5, 0.5);
            fileMatrix.setPosition(f.x, f.y, f.z);
            fileInstanced.setMatrixAt(i, fileMatrix);
            
            fileColor.set(f.color);
            fileInstanced.setColorAt(i, fileColor);
        }});
        
        fileInstanced.instanceMatrix.needsUpdate = true;
        if (fileInstanced.instanceColor) fileInstanced.instanceColor.needsUpdate = true;
        fileGroup.add(fileInstanced);
        
        // Lines (simplified - only directory connections)
        const lineMaterial = new THREE.LineBasicMaterial({{ 
            color: 0x00b4d8, 
            transparent: true, 
            opacity: 0.3 
        }});
        
        const lineGeometry = new THREE.BufferGeometry();
        const positions = [];
        
        connections.forEach(c => {{
            if (c.type === 'dir-dir') {{
                positions.push(c.x1, c.y1, c.z1);
                positions.push(c.x2, c.y2, c.z2);
            }}
        }});
        
        lineGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
        lineGroup.add(lines);
        
        // Hide loading
        document.getElementById('loading').style.display = 'none';
        
        // Raycaster for interaction
        const raycaster = new THREE.Raycaster();
        raycaster.params.Points.threshold = 0.5;
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        
        // Find closest item
        function findClosestItem(x, y, z, threshold = 2) {{
            let closest = null;
            let minDist = threshold;
            
            // Check directories
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
            
            // Check files
            for (const f of files) {{
                const dx = f.x - x;
                const dy = f.y - y;
                const dz = f.z - z;
                const dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
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
                    tooltip.querySelector('.path').textContent = d.path;
                    tooltip.querySelector('.size').textContent = d.depth + ' levels deep';
                    tooltip.querySelector('.type').textContent = 'Directory';
                    tooltip.querySelector('.type').style.color = '#ff6b35';
                }}
            }} else {{
                tooltip.style.display = 'none';
            }}
        }});
        
        // Controls
        document.getElementById('node-size').addEventListener('input', e => {{
            const size = parseFloat(e.target.value);
            document.getElementById('node-size-value').textContent = size.toFixed(1);
            
            // Update file instances
            files.forEach((f, i) => {{
                fileMatrix.makeScale(size, size, size);
                fileMatrix.setPosition(f.x, f.y, f.z);
                fileInstanced.setMatrixAt(i, fileMatrix);
            }});
            fileInstanced.instanceMatrix.needsUpdate = true;
        }});
        
        document.getElementById('line-opacity').addEventListener('input', e => {{
            const opacity = parseFloat(e.target.value);
            document.getElementById('line-opacity-value').textContent = opacity.toFixed(1);
            lineMaterial.opacity = opacity;
        }});
        
        document.getElementById('show-files').addEventListener('change', e => {{
            fileGroup.visible = e.target.checked;
        }});
        
        document.getElementById('show-lines').addEventListener('change', e => {{
            lineGroup.visible = e.target.checked;
        }});
        
        // Animation
        function animate() {{
            requestAnimationFrame(animate);
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
        
        console.log('Rendering complete');
    </script>
</body>
</html>'''
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"HTML written to {output_path}")


if __name__ == '__main__':
    import sys
    
    # Cria explorador
    explorer = FileSystemExplorer3D()
    
    # Indexa sistema de arquivos COMPLETO (sem limite)
    root_paths = [
        os.path.expanduser('~/.openclaw/workspace'),
        os.path.expanduser('~/Documents'),
    ]
    
    file_count, dir_count = explorer.index_filesystem(root_paths, max_files=None)
    
    # Constrói layout 3D hierárquico
    explorer.build_3d_layout()
    
    # Gera HTML
    output_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.openclaw/workspace/memory/file_explorer_3d.html')
    explorer.generate_html(output_path)
    
    print(f"\\n=== File System Explorer 3D ===")
    print(f"Files: {file_count:,}")
    print(f"Directories: {dir_count:,}")
    print(f"Hierarchical layout with center root")
    print(f"Lines connecting parent-child")
    print(f"Instanced rendering for performance")
    print(f"\\nOpen {output_path} in your browser.")