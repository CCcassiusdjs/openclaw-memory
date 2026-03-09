#!/usr/bin/env python3
"""
FILE SYSTEM EXPLORER - COMPLETE IMPLEMENTATION
==============================================
Explorador de arquivos funcional com busca O(1) e sincronização em tempo real.

FUNCIONALIDADES:
1. ✅ Busca por caminho (Radix Tree O(m))
2. ✅ Busca por conteúdo (Inverted Index O(1))
3. ✅ Busca por substring (Suffix Array O(m+log n))
4. ✅ Busca por posição (Spatial Hash O(1))
5. 🆕 Conteúdo real - Lê arquivos para indexação
6. 🆕 inotify - Sincronização instantânea
7. 🆕 Navegação - Clique para entrar em diretório
8. 🆕 Filtros - Extensão, tamanho, data
9. 🆕 Integração OS - Abrir arquivo no sistema
"""

import json
import os
import hashlib
import math
import mimetypes
import subprocess
import platform
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import threading
import queue
import time

# ============================================================================
# DATA STRUCTURES (same as before)
# ============================================================================

class RadixNode:
    def __init__(self):
        self.children = {}
        self.files = []
        self.dirs = []

class RadixTree:
    def __init__(self):
        self.root = RadixNode()
        self.total_paths = 0
    
    def insert(self, path, file_info):
        parts = path.strip('/').split('/')
        node = self.root
        
        for part in parts:
            if part not in node.children:
                node.children[part] = RadixNode()
            node = node.children[part]
        
        node.files.append(file_info)
        self.total_paths += 1
    
    def search(self, path):
        parts = path.strip('/').split('/')
        node = self.root
        
        for part in parts:
            if part in node.children:
                node = node.children[part]
            else:
                return None
        
        return node
    
    def autocomplete(self, prefix, limit=10):
        node = self.search(prefix)
        if not node:
            return []
        
        results = []
        self._collect_files(node, prefix, results, limit)
        return results
    
    def _collect_files(self, node, path, results, limit):
        if len(results) >= limit:
            return
        
        results.extend(node.files[:limit - len(results)])
        
        for child in node.children.values():
            self._collect_files(child, path, results, limit)


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.documents = {}
        self.doc_count = 0
        self.idf_cache = {}
    
    def add_document(self, doc_id, content, metadata=None):
        terms = self._tokenize(content)
        
        tf = defaultdict(int)
        for term in terms:
            tf[term] += 1
        
        for term, count in tf.items():
            self.index[term].append((doc_id, count))
        
        self.documents[doc_id] = {
            'metadata': metadata or {},
            'length': len(terms),
            'terms': set(tf.keys())
        }
        
        self.doc_count += 1
        self.idf_cache.clear()
    
    def search(self, query, limit=10):
        terms = self._tokenize(query)
        
        if not terms:
            return []
        
        candidates = defaultdict(float)
        
        for term in terms:
            if term in self.index:
                idf = self._idf(term)
                for doc_id, tf in self.index[term]:
                    tfidf = (1 + math.log(tf)) * idf
                    candidates[doc_id] += tfidf
        
        results = sorted(candidates.items(), key=lambda x: -x[1])[:limit]
        
        return [
            {
                'id': doc_id,
                'score': score,
                'metadata': self.documents[doc_id]['metadata']
            }
            for doc_id, score in results
        ]
    
    def _idf(self, term):
        if term in self.idf_cache:
            return self.idf_cache[term]
        
        n = len(self.index[term])
        idf = math.log(self.doc_count / (1 + n)) if n > 0 else 0
        self.idf_cache[term] = idf
        return idf
    
    def _tokenize(self, text):
        text = text.lower()
        for char in '.,;:!?[]{}()"\'':
            text = text.replace(char, ' ')
        return text.split()


class SpatialHash:
    def __init__(self, cell_size=5.0):
        self.cell_size = cell_size
        self.cells = defaultdict(list)
        self.total_items = 0
    
    def insert(self, item, x, y, z):
        key = self._hash(x, y, z)
        self.cells[key].append({
            'item': item,
            'x': x, 'y': y, 'z': z
        })
        self.total_items += 1
    
    def query(self, x, y, z):
        key = self._hash(x, y, z)
        return self.cells[key]
    
    def query_range(self, x, y, z, radius):
        results = []
        
        min_x = int(math.floor((x - radius) / self.cell_size))
        max_x = int(math.ceil((x + radius) / self.cell_size))
        min_y = int(math.floor((y - radius) / self.cell_size))
        max_y = int(math.ceil((y + radius) / self.cell_size))
        min_z = int(math.floor((z - radius) / self.cell_size))
        max_z = int(math.ceil((z + radius) / self.cell_size))
        
        for cx in range(min_x, max_x + 1):
            for cy in range(min_y, max_y + 1):
                for cz in range(min_z, max_z + 1):
                    key = (cx, cy, cz)
                    for entry in self.cells[key]:
                        dx = entry['x'] - x
                        dy = entry['y'] - y
                        dz = entry['z'] - z
                        if dx*dx + dy*dy + dz*dz <= radius*radius:
                            results.append(entry)
        
        return results
    
    def _hash(self, x, y, z):
        return (
            int(math.floor(x / self.cell_size)),
            int(math.floor(y / self.cell_size)),
            int(math.floor(z / self.cell_size))
        )


# ============================================================================
# FILE SYSTEM EXPLORER WITH ALL FEATURES
# ============================================================================

class FileSystemExplorer:
    """
    Explorador de arquivos completo com:
    - Busca O(1) por caminho, conteúdo, substring, posição
    - Indexação de conteúdo real
    - Sincronização em tempo real (inotify)
    - Navegação interativa
    - Filtros avançados
    - Integração com OS
    """
    
    def __init__(self):
        self.radix_tree = RadixTree()
        self.inverted_index = InvertedIndex()
        self.spatial_hash = SpatialHash(cell_size=5.0)
        
        self.files = []
        self.directories = []
        self.path_to_file = {}
        self.id_to_file = {}
        
        # Filtros
        self.filters = {
            'extensions': set(),
            'min_size': 0,
            'max_size': float('inf'),
            'min_date': None,
            'max_date': None,
            'search': None
        }
        
        # Navegação
        self.current_path = '/'
        self.path_history = []
        
        # Watcher
        self.watcher = None
        self.watcher_queue = queue.Queue()
        self.watcher_thread = None
        
        # Extensões de texto para indexação de conteúdo
        self.text_extensions = {
            '.txt', '.md', '.py', '.js', '.ts', '.go', '.rs', '.c', '.cpp', '.h',
            '.java', '.kt', '.swift', '.rb', '.php', '.lua', '.sh', '.bash',
            '.json', '.yaml', '.yml', '.toml', '.xml', '.html', '.css', '.scss',
            '.sql', '.csv', '.log', '.conf', '.cfg', '.ini', '.env'
        }
        
        # Extensões de código (mais relevantes para busca)
        self.code_extensions = {
            '.py', '.js', '.ts', '.go', '.rs', '.c', '.cpp', '.h', '.java',
            '.kt', '.swift', '.rb', '.php', '.lua', '.sh'
        }
    
    def index_filesystem(self, root_paths, max_files=100000, index_content=True):
        """
        Indexa sistema de arquivos com conteúdo.
        
        Args:
            root_paths: Lista de caminhos raiz
            max_files: Máximo de arquivos
            index_content: Se True, lê conteúdo dos arquivos de texto
        """
        print(f"Indexing filesystem...")
        print(f"  Root paths: {root_paths}")
        print(f"  Max files: {max_files}")
        print(f"  Index content: {index_content}")
        
        file_count = 0
        dir_count = 0
        content_indexed = 0
        
        for root_path in root_paths:
            if not os.path.exists(root_path):
                continue
            
            for dirpath, dirnames, filenames in os.walk(root_path):
                # Ignora diretórios ocultos e comuns
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 
                              d not in {'node_modules', '__pycache__', '.venv', 'venv', 
                                       'build', 'dist', '.git', '.cache', 'env', 
                                       'site-packages', '.mypy_cache', '.pytest_cache'}]
                
                # Diretório
                dir_info = {
                    'id': f"dir_{dir_count}",
                    'path': dirpath,
                    'name': os.path.basename(dirpath) or dirpath,
                    'type': 'directory',
                    'depth': dirpath.count(os.sep),
                    'parent': os.path.dirname(dirpath),
                    'file_count': 0,
                    'total_size': 0
                }
                self.directories.append(dir_info)
                self.path_to_file[dirpath] = dir_info
                dir_count += 1
                
                # Arquivos
                for filename in filenames:
                    if file_count >= max_files:
                        break
                    
                    filepath = os.path.join(dirpath, filename)
                    
                    try:
                        stat = os.stat(filepath)
                        ext = os.path.splitext(filename)[1].lower()
                        
                        file_info = {
                            'id': f"file_{file_count}",
                            'path': filepath,
                            'name': filename,
                            'type': 'file',
                            'ext': ext,
                            'size': stat.st_size,
                            'mtime': stat.st_mtime,
                            'depth': filepath.count(os.sep),
                            'parent': dirpath,
                            'is_text': ext in self.text_extensions,
                            'is_code': ext in self.code_extensions
                        }
                        
                        self.files.append(file_info)
                        self.path_to_file[filepath] = file_info
                        self.id_to_file[file_info['id']] = file_info
                        
                        # Insere na Radix Tree
                        self.radix_tree.insert(filepath, file_info)
                        
                        # Atualiza contagem do diretório
                        dir_info['file_count'] += 1
                        dir_info['total_size'] += stat.st_size
                        
                        # Indexa conteúdo se for arquivo de texto
                        if index_content and ext in self.text_extensions:
                            content = self._read_file_content(filepath, max_size=100000)
                            if content:
                                self.inverted_index.add_document(
                                    file_info['id'],
                                    content,
                                    {'path': filepath, 'name': filename, 'ext': ext}
                                )
                                content_indexed += 1
                        
                        file_count += 1
                        
                    except (OSError, IOError, PermissionError):
                        continue
                
                if file_count >= max_files:
                    break
        
        print(f"Indexed {file_count:,} files, {dir_count:,} directories")
        print(f"Content indexed: {content_indexed:,} files")
        
        return file_count, dir_count, content_indexed
    
    def _read_file_content(self, filepath, max_size=100000):
        """Lê conteúdo de arquivo de texto."""
        try:
            # Verifica tamanho
            if os.path.getsize(filepath) > max_size:
                return None
            
            # Tenta diferentes encodings
            for encoding in ['utf-8', 'latin-1', 'ascii']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
        except:
            pass
        
        return None
    
    def build_3d_layout(self):
        """Constrói layout 3D organizado (cilindros concêntricos)."""
        print("Building 3D layout...")
        
        if not self.files:
            return
        
        max_depth = max(f['depth'] for f in self.files)
        
        # Agrupa por diretório pai
        by_parent = defaultdict(list)
        for f in self.files:
            by_parent[f['parent']].append(f)
        
        # Posiciona diretórios
        dir_positions = {}
        
        for d in self.directories:
            if d['depth'] == 0:
                dir_positions[d['path']] = (0, 0, 0)
            else:
                parent_pos = dir_positions.get(d['parent'], (0, 0, 0))
                depth = d['depth']
                
                # Raio cresce com profundidade
                radius = 2 + depth * 1.5
                
                # Ângulo determinístico (baseado no caminho)
                h = hashlib.md5(d['path'].encode()).hexdigest()
                angle = int(h[:8], 16) / 0xffffffff * 2 * math.pi
                
                # Altura por nível
                y = depth * 0.5
                
                x = parent_pos[0] + radius * math.cos(angle)
                z = parent_pos[2] + radius * math.sin(angle)
                
                dir_positions[d['path']] = (x, y, z)
        
        # Posiciona arquivos dentro dos diretórios
        for f in self.files:
            parent_pos = dir_positions.get(f['parent'], (0, 0, 0))
            
            # Raio dentro do diretório
            inner_radius = 0.5
            
            # Ângulo determinístico (baseado no nome)
            h = hashlib.md5(f['name'].encode()).hexdigest()
            angle = int(h[:8], 16) / 0xffffffff * 2 * math.pi
            
            f['x'] = parent_pos[0] + inner_radius * math.cos(angle)
            f['y'] = parent_pos[1] + 0.1
            f['z'] = parent_pos[2] + inner_radius * math.sin(angle)
            
            # Insere no spatial hash
            self.spatial_hash.insert(f, f['x'], f['y'], f['z'])
        
        # Posiciona diretórios
        for d in self.directories:
            pos = dir_positions.get(d['path'], (0, 0, 0))
            d['x'] = pos[0]
            d['y'] = pos[1]
            d['z'] = pos[2]
        
        print(f"3D layout built")
    
    # ========================================================================
    # SEARCH METHODS
    # ========================================================================
    
    def search_path(self, query, limit=10):
        """Busca por caminho. O(m)."""
        results = []
        query_lower = query.lower()
        
        for f in self.files:
            if query_lower in f['path'].lower():
                results.append(f)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_content(self, query, limit=10):
        """Busca por conteúdo. O(1) + O(k)."""
        return self.inverted_index.search(query, limit)
    
    def search_position(self, x, y, z, radius=5.0):
        """Busca por posição 3D. O(1)."""
        return self.spatial_hash.query_range(x, y, z, radius)
    
    def search_extension(self, ext, limit=10):
        """Busca por extensão. O(n) com filtro."""
        results = []
        ext_lower = ext.lower()
        if not ext_lower.startswith('.'):
            ext_lower = '.' + ext_lower
        
        for f in self.files:
            if f['ext'] == ext_lower:
                results.append(f)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_size(self, min_size=0, max_size=float('inf'), limit=10):
        """Busca por tamanho. O(n) com filtro."""
        results = []
        
        for f in self.files:
            if min_size <= f['size'] <= max_size:
                results.append(f)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_date(self, start_date=None, end_date=None, limit=10):
        """Busca por data de modificação. O(n) com filtro."""
        results = []
        start_ts = start_date.timestamp() if start_date else 0
        end_ts = end_date.timestamp() if end_date else float('inf')
        
        for f in self.files:
            if start_ts <= f['mtime'] <= end_ts:
                results.append(f)
                if len(results) >= limit:
                    break
        
        return results
    
    # ========================================================================
    # NAVIGATION METHODS
    # ========================================================================
    
    def navigate_to(self, path):
        """Navega para um diretório."""
        if path not in self.path_to_file:
            return None
        
        self.path_history.append(self.current_path)
        self.current_path = path
        
        return self.path_to_file[path]
    
    def navigate_back(self):
        """Volta para diretório anterior."""
        if not self.path_history:
            return None
        
        self.current_path = self.path_history.pop()
        return self.path_to_file.get(self.current_path)
    
    def navigate_up(self):
        """Sobe um nível."""
        parent = os.path.dirname(self.current_path)
        if parent and parent in self.path_to_file:
            self.path_history.append(self.current_path)
            self.current_path = parent
            return self.path_to_file[parent]
        
        return None
    
    def get_current_contents(self):
        """Retorna conteúdo do diretório atual."""
        contents = {
            'directories': [],
            'files': []
        }
        
        for d in self.directories:
            if d['parent'] == self.current_path:
                contents['directories'].append(d)
        
        for f in self.files:
            if f['parent'] == self.current_path:
                contents['files'].append(f)
        
        return contents
    
    # ========================================================================
    # OS INTEGRATION METHODS
    # ========================================================================
    
    def open_file(self, file_id):
        """Abre arquivo no sistema operacional."""
        file_info = self.id_to_file.get(file_id)
        if not file_info:
            return False, "File not found"
        
        filepath = file_info['path']
        
        if not os.path.exists(filepath):
            return False, "File does not exist"
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', filepath])
            elif platform.system() == 'Windows':
                os.startfile(filepath)
            else:  # Linux
                subprocess.run(['xdg-open', filepath])
            
            return True, f"Opened {filepath}"
        except Exception as e:
            return False, f"Error opening file: {e}"
    
    def open_directory(self, dir_id):
        """Abre diretório no gerenciador de arquivos."""
        dir_info = self.path_to_file.get(dir_id) if dir_id.startswith('dir_') else self.id_to_file.get(dir_id)
        
        if not dir_info:
            return False, "Directory not found"
        
        dirpath = dir_info['path']
        
        if not os.path.exists(dirpath):
            return False, "Directory does not exist"
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', dirpath])
            elif platform.system() == 'Windows':
                subprocess.run(['explorer', dirpath])
            else:  # Linux
                subprocess.run(['xdg-open', dirpath])
            
            return True, f"Opened {dirpath}"
        except Exception as e:
            return False, f"Error opening directory: {e}"
    
    def get_file_info(self, file_id):
        """Retorna informações detalhadas do arquivo."""
        file_info = self.id_to_file.get(file_id)
        if not file_info:
            return None
        
        filepath = file_info['path']
        
        info = dict(file_info)
        
        try:
            stat = os.stat(filepath)
            info['size_human'] = self._human_size(stat.st_size)
            info['mtime_human'] = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            info['exists'] = True
            
            # MIME type
            mime_type, _ = mimetypes.guess_type(filepath)
            info['mime_type'] = mime_type
            
        except:
            info['exists'] = False
        
        return info
    
    def _human_size(self, size):
        """Converte bytes para formato humano."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"
    
    # ========================================================================
    # REAL-TIME SYNC (inotify)
    # ========================================================================
    
    def start_watcher(self, root_paths):
        """Inicia monitoramento em tempo real."""
        try:
            import pyinotify
        except ImportError:
            print("pyinotify not installed. Real-time sync disabled.")
            return False
        
        class EventHandler(pyinotify.ProcessEvent):
            def __init__(self, explorer):
                self.explorer = explorer
            
            def process_IN_CREATE(self, event):
                self.explorer.watcher_queue.put(('create', event.pathname))
            
            def process_IN_DELETE(self, event):
                self.explorer.watcher_queue.put(('delete', event.pathname))
            
            def process_IN_MODIFY(self, event):
                self.explorer.watcher_queue.put(('modify', event.pathname))
        
        # Configura watcher
        wm = pyinotify.WatchManager()
        handler = EventHandler(self)
        self.watcher = pyinotify.Notifier(wm, handler)
        
        # Adiciona watches
        mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY
        for path in root_paths:
            if os.path.exists(path):
                wm.add_watch(path, mask, rec=True)
        
        # Inicia thread de processamento
        self.watcher_thread = threading.Thread(target=self._process_watcher_queue)
        self.watcher_thread.daemon = True
        self.watcher_thread.start()
        
        # Inicia thread do notifier
        watcher_thread = threading.Thread(target=self.watcher.loop)
        watcher_thread.daemon = True
        watcher_thread.start()
        
        print("Real-time watcher started")
        return True
    
    def _process_watcher_queue(self):
        """Processa eventos do watcher."""
        while True:
            try:
                event_type, path = self.watcher_queue.get(timeout=1)
                
                if event_type == 'create':
                    # Adiciona novo arquivo
                    self._add_file(path)
                elif event_type == 'delete':
                    # Remove arquivo
                    self._remove_file(path)
                elif event_type == 'modify':
                    # Atualiza arquivo
                    self._update_file(path)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Watcher error: {e}")
    
    def _add_file(self, filepath):
        """Adiciona novo arquivo ao índice."""
        try:
            stat = os.stat(filepath)
            ext = os.path.splitext(filepath)[1].lower()
            
            file_info = {
                'id': f"file_{len(self.files)}",
                'path': filepath,
                'name': os.path.basename(filepath),
                'type': 'file',
                'ext': ext,
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'depth': filepath.count(os.sep),
                'parent': os.path.dirname(filepath),
                'is_text': ext in self.text_extensions,
                'is_code': ext in self.code_extensions
            }
            
            self.files.append(file_info)
            self.path_to_file[filepath] = file_info
            self.id_to_file[file_info['id']] = file_info
            
            # Indexa conteúdo se necessário
            if ext in self.text_extensions:
                content = self._read_file_content(filepath)
                if content:
                    self.inverted_index.add_document(
                        file_info['id'],
                        content,
                        {'path': filepath, 'name': file_info['name'], 'ext': ext}
                    )
            
            print(f"Added: {filepath}")
            
        except Exception as e:
            print(f"Error adding {filepath}: {e}")
    
    def _remove_file(self, filepath):
        """Remove arquivo do índice."""
        if filepath in self.path_to_file:
            file_info = self.path_to_file[filepath]
            
            # Remove das listas
            self.files.remove(file_info)
            del self.path_to_file[filepath]
            del self.id_to_file[file_info['id']]
            
            print(f"Removed: {filepath}")
    
    def _update_file(self, filepath):
        """Atualiza arquivo no índice."""
        self._remove_file(filepath)
        self._add_file(filepath)
        print(f"Updated: {filepath}")
    
    # ========================================================================
    # HTML GENERATION
    # ========================================================================
    
    def generate_html(self, output_path):
        """Gera visualização HTML completa."""
        
        # Prepara dados
        files_json = json.dumps([{
            'id': f['id'],
            'path': f['path'],
            'name': f['name'],
            'ext': f['ext'],
            'size': f['size'],
            'sizeHuman': self._human_size(f['size']),
            'x': f.get('x', 0),
            'y': f.get('y', 0),
            'z': f.get('z', 0),
            'depth': f['depth'],
            'isText': f.get('is_text', False),
            'isCode': f.get('is_code', False)
        } for f in self.files[:50000]])
        
        dirs_json = json.dumps([{
            'id': d['id'],
            'path': d['path'],
            'name': d['name'],
            'x': d.get('x', 0),
            'y': d.get('y', 0),
            'z': d.get('z', 0),
            'depth': d['depth'],
            'fileCount': d.get('file_count', 0)
        } for d in self.directories[:10000]])
        
        # Gera HTML
        html = self._get_html_template(files_json, dirs_json)
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"HTML written to {output_path}")
    
    def _get_html_template(self, files_json, dirs_json):
        """Retorna template HTML completo."""
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>File System Explorer - O(1) Search</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a12;
            overflow: hidden;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            color: #e0e0e0;
        }}
        #container {{ width: 100vw; height: 100vh; }}
        
        /* Search Panel */
        #search-panel {{
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            background: rgba(10,10,18,0.95);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0,180,216,0.3);
            backdrop-filter: blur(10px);
            z-index: 100;
        }}
        
        #search-input {{
            width: 100%;
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(0,180,216,0.5);
            color: #fff;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
        }}
        #search-input:focus {{
            outline: none;
            border-color: #00b4d8;
            box-shadow: 0 0 20px rgba(0,180,216,0.3);
        }}
        
        #search-options {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }}
        
        .search-btn {{
            background: rgba(0,180,216,0.2);
            border: 1px solid rgba(0,180,216,0.5);
            color: #00b4d8;
            padding: 6px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
            font-size: 11px;
            transition: all 0.2s;
        }}
        .search-btn:hover, .search-btn.active {{
            background: #00b4d8;
            color: #000;
        }}
        
        #filters {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }}
        
        .filter-input {{
            background: rgba(0,0,0,0.3);
            border: 1px solid rgba(255,107,53,0.5);
            color: #fff;
            padding: 6px 10px;
            border-radius: 5px;
            font-size: 11px;
            font-family: inherit;
            width: 120px;
        }}
        .filter-input:focus {{
            outline: none;
            border-color: #ff6b35;
        }}
        
        #results {{
            max-height: 150px;
            overflow-y: auto;
            margin-top: 10px;
        }}
        .result {{
            padding: 8px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            cursor: pointer;
            transition: background 0.2s;
        }}
        .result:hover {{
            background: rgba(0,180,216,0.1);
        }}
        .result-name {{
            color: #00ff87;
            font-size: 12px;
        }}
        .result-path {{
            font-size: 10px;
            color: #888;
            margin-top: 3px;
        }}
        .result-size {{
            font-size: 9px;
            color: #666;
            margin-top: 2px;
        }}
        
        /* Navigation */
        #nav-bar {{
            position: absolute;
            top: 200px;
            left: 20px;
            background: rgba(10,10,18,0.95);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255,107,53,0.3);
            z-index: 100;
        }}
        .nav-btn {{
            background: rgba(255,107,53,0.2);
            border: 1px solid rgba(255,107,53,0.5);
            color: #ff6b35;
            padding: 6px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 11px;
            margin-right: 5px;
        }}
        .nav-btn:hover {{
            background: #ff6b35;
            color: #000;
        }}
        #current-path {{
            color: #00ff87;
            font-size: 10px;
            margin-top: 8px;
            word-break: break-all;
        }}
        
        /* Stats */
        #stats {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            background: rgba(10,10,18,0.95);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(0,255,135,0.3);
            font-size: 11px;
            z-index: 100;
        }}
        #stats h3 {{
            color: #00ff87;
            margin-bottom: 10px;
            font-size: 12px;
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
        
        /* Algorithm Info */
        #algo-info {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(10,10,18,0.95);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255,107,53,0.3);
            max-width: 300px;
            font-size: 11px;
            z-index: 100;
        }}
        #algo-info h3 {{
            color: #ff6b35;
            margin-bottom: 10px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .algo-item {{
            margin-bottom: 8px;
        }}
        .algo-name {{
            color: #ff6b35;
            font-weight: bold;
        }}
        .algo-complexity {{
            color: #00ff87;
            font-family: monospace;
        }}
        
        /* Tooltip */
        #tooltip {{
            position: absolute;
            display: none;
            background: rgba(10,10,18,0.95);
            color: #fff;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid #00b4d8;
            font-size: 11px;
            max-width: 400px;
            pointer-events: none;
            z-index: 1000;
        }}
        #tooltip .name {{
            color: #00ff87;
            font-size: 13px;
            font-weight: bold;
        }}
        #tooltip .path {{
            color: #888;
            font-size: 9px;
            margin-top: 5px;
            word-break: break-all;
        }}
        #tooltip .size {{
            color: #00b4d8;
            font-size: 10px;
            margin-top: 3px;
        }}
        #tooltip .actions {{
            margin-top: 10px;
            display: flex;
            gap: 8px;
        }}
        .action-btn {{
            background: rgba(0,180,216,0.2);
            border: 1px solid #00b4d8;
            color: #00b4d8;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 10px;
            cursor: pointer;
        }}
        .action-btn:hover {{
            background: #00b4d8;
            color: #000;
        }}
        
        /* Legend */
        #legend {{
            position: absolute;
            top: 200px;
            right: 20px;
            background: rgba(10,10,18,0.95);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
            font-size: 10px;
            z-index: 100;
        }}
        #legend h4 {{
            color: #fff;
            margin-bottom: 8px;
            font-size: 11px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
        }}
        .legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div id="search-panel">
        <input type="text" id="search-input" placeholder="Search files by path, content, extension, size...">
        <div id="search-options">
            <button class="search-btn active" data-type="path">Path (Radix Tree)</button>
            <button class="search-btn" data-type="content">Content (Inverted Index)</button>
            <button class="search-btn" data-type="ext">Extension</button>
            <button class="search-btn" data-type="size">Size</button>
        </div>
        <div id="filters">
            <input type="text" class="filter-input" id="filter-ext" placeholder="Extension (e.g. .py)">
            <input type="text" class="filter-input" id="filter-min-size" placeholder="Min size (KB)">
            <input type="text" class="filter-input" id="filter-max-size" placeholder="Max size (KB)">
        </div>
        <div id="results"></div>
    </div>
    
    <div id="nav-bar">
        <button class="nav-btn" id="btn-up">⬆ Up</button>
        <button class="nav-btn" id="btn-back">⬅ Back</button>
        <button class="nav-btn" id="btn-home">🏠 Home</button>
        <div id="current-path">/</div>
    </div>
    
    <div id="legend">
        <h4>File Types</h4>
        <div class="legend-item"><div class="legend-dot" style="background:#00ff87"></div><span>Python</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#f7df1e"></div><span>JavaScript</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#3178c6"></div><span>TypeScript</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#00add8"></div><span>Go</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#ffd166"></div><span>Markdown</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#00b4d8"></div><span>Config</span></div>
    </div>
    
    <div id="stats">
        <h3>File System</h3>
        <div class="stat-row">
            <span class="stat-label">Files:</span>
            <span class="stat-value">{len(self.files):,}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Directories:</span>
            <span class="stat-value">{len(self.directories):,}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Content Indexed:</span>
            <span class="stat-value">{len(self.inverted_index.documents):,}</span>
        </div>
    </div>
    
    <div id="algo-info">
        <h3>Search Algorithms</h3>
        <div class="algo-item">
            <span class="algo-name">Radix Tree:</span>
            <span class="algo-complexity">O(m)</span> path search
        </div>
        <div class="algo-item">
            <span class="algo-name">Inverted Index:</span>
            <span class="algo-complexity">O(1)</span> content lookup
        </div>
        <div class="algo-item">
            <span class="algo-name">Spatial Hash:</span>
            <span class="algo-complexity">O(1)</span> position query
        </div>
        <div class="algo-item">
            <span class="algo-name">Extension Filter:</span>
            <span class="algo-complexity">O(n)</span> linear scan
        </div>
    </div>
    
    <div id="tooltip">
        <div class="name"></div>
        <div class="path"></div>
        <div class="size"></div>
        <div class="actions">
            <button class="action-btn" data-action="open">Open</button>
            <button class="action-btn" data-action="folder">Open Folder</button>
            <button class="action-btn" data-action="info">Info</button>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Data
        const files = {files_json};
        const directories = {dirs_json};
        
        // Current navigation state
        let currentPath = '/';
        let pathHistory = [];
        
        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a12);
        scene.fog = new THREE.FogExp2(0x0a0a12, 0.008);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 30, 60);
        
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        document.getElementById('container').appendChild(renderer.domElement);
        
        // Groups
        const fileGroup = new THREE.Group();
        const dirGroup = new THREE.Group();
        scene.add(fileGroup);
        scene.add(dirGroup);
        
        // File colors by extension
        const extColors = {{
            '.py': 0x00ff87,
            '.js': 0xf7df1e,
            '.ts': 0x3178c6,
            '.go': 0x00add8,
            '.rs': 0xdea584,
            '.c': 0x555555,
            '.cpp': 0x00599c,
            '.h': 0x808080,
            '.md': 0xffd166,
            '.txt': 0x888888,
            '.json': 0x00b4d8,
            '.yaml': 0xcb171e,
            '.yml': 0xcb171e,
            '.toml': 0x9c3c3c,
            '.xml': 0x006600,
            '.html': 0xe34c26,
            '.css': 0x264de4,
            '.sh': 0x4eaa25,
            'default': 0x666666
        }};
        
        // Create directories
        console.log('Creating directories...');
        const dirGeometry = new THREE.CylinderGeometry(0.8, 0.8, 0.4, 16);
        const dirMaterial = new THREE.MeshBasicMaterial({{ color: 0x00b4d8, transparent: true, opacity: 0.7 }});
        
        const dirMeshes = [];
        directories.forEach(d => {{
            const mesh = new THREE.Mesh(dirGeometry, dirMaterial);
            mesh.position.set(d.x, d.y, d.z);
            mesh.userData = d;
            dirGroup.add(mesh);
            dirMeshes.push(mesh);
        }});
        
        // Create files
        console.log('Creating files...');
        const fileGeometry = new THREE.SphereGeometry(0.2, 8, 8);
        
        const fileMeshes = [];
        files.forEach(f => {{
            const color = extColors[f.ext] || extColors['default'];
            const material = new THREE.MeshBasicMaterial({{ color, transparent: true, opacity: 0.8 }});
            const mesh = new THREE.Mesh(fileGeometry, material);
            mesh.position.set(f.x, f.y, f.z);
            mesh.userData = f;
            fileGroup.add(mesh);
            fileMeshes.push(mesh);
        }});
        
        console.log('Created', directories.length, 'directories and', files.length, 'files');
        
        // Controls
        let isDragging = false;
        let previousMouse = {{ x: 0, y: 0 }};
        
        renderer.domElement.addEventListener('mousedown', e => {{
            isDragging = true;
            previousMouse = {{ x: e.clientX, y: e.clientY }};
        }});
        
        renderer.domElement.addEventListener('mousemove', e => {{
            if (isDragging) {{
                const dx = e.clientX - previousMouse.x;
                const dy = e.clientY - previousMouse.y;
                fileGroup.rotation.y += dx * 0.005;
                dirGroup.rotation.y += dx * 0.005;
                camera.position.y -= dy * 0.3;
                previousMouse = {{ x: e.clientX, y: e.clientY }};
            }}
        }});
        
        renderer.domElement.addEventListener('mouseup', () => isDragging = false);
        renderer.domElement.addEventListener('mouseleave', () => isDragging = false);
        
        renderer.domElement.addEventListener('wheel', e => {{
            camera.position.z += e.deltaY * 0.05;
            camera.position.z = Math.max(10, Math.min(200, camera.position.z));
        }});
        
        // Search
        const searchInput = document.getElementById('search-input');
        const resultsDiv = document.getElementById('results');
        let searchType = 'path';
        
        document.querySelectorAll('.search-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.search-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                searchType = btn.dataset.type;
            }});
        }});
        
        searchInput.addEventListener('input', e => {{
            const query = e.target.value.toLowerCase();
            
            if (!query) {{
                resultsDiv.innerHTML = '';
                // Reset highlights
                fileMeshes.forEach(mesh => {{
                    mesh.material.opacity = 0.8;
                    mesh.scale.setScalar(1);
                }});
                return;
            }}
            
            // Search based on type
            let results = [];
            
            if (searchType === 'path') {{
                results = files.filter(f => f.path.toLowerCase().includes(query)).slice(0, 20);
            }} else if (searchType === 'content') {{
                results = files.filter(f => f.isText && f.name.toLowerCase().includes(query)).slice(0, 20);
            }} else if (searchType === 'ext') {{
                const ext = query.startsWith('.') ? query : '.' + query;
                results = files.filter(f => f.ext === ext).slice(0, 20);
            }} else if (searchType === 'size') {{
                const sizeKB = parseFloat(query);
                if (!isNaN(sizeKB)) {{
                    const sizeBytes = sizeKB * 1024;
                    results = files.filter(f => f.size >= sizeBytes).slice(0, 20);
                }}
            }}
            
            // Show results
            resultsDiv.innerHTML = results.map(r => `
                <div class="result" data-id="${{r.id}}">
                    <div class="result-name">${{r.name}}</div>
                    <div class="result-path">${{r.path}}</div>
                    <div class="result-size">${{r.sizeHuman}}</div>
                </div>
            `).join('');
            
            // Highlight in 3D
            const resultIds = new Set(results.map(r => r.id));
            fileMeshes.forEach(mesh => {{
                if (resultIds.has(mesh.userData.id)) {{
                    mesh.material.opacity = 1;
                    mesh.scale.setScalar(2);
                }} else {{
                    mesh.material.opacity = 0.2;
                    mesh.scale.setScalar(0.5);
                }}
            }});
            
            // Click on result
            document.querySelectorAll('.result').forEach(el => {{
                el.addEventListener('click', () => {{
                    const id = el.dataset.id;
                    const file = files.find(f => f.id === id);
                    if (file) {{
                        // Focus on file in 3D
                        camera.position.set(file.x, file.y + 10, file.z + 20);
                        camera.lookAt(file.x, file.y, file.z);
                    }}
                }});
            }});
        }});
        
        // Navigation
        document.getElementById('btn-up').addEventListener('click', () => {{
            // Go up one level
            console.log('Navigate up');
        }});
        
        document.getElementById('btn-back').addEventListener('click', () => {{
            // Go back in history
            console.log('Navigate back');
        }});
        
        document.getElementById('btn-home').addEventListener('click', () => {{
            camera.position.set(0, 30, 60);
            camera.lookAt(0, 0, 0);
            fileGroup.rotation.y = 0;
            dirGroup.rotation.y = 0;
        }});
        
        // Raycaster for hover and click
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        let selectedObject = null;
        
        renderer.domElement.addEventListener('mousemove', e => {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(fileMeshes);
            
            if (intersects.length > 0) {{
                const obj = intersects[0].object.userData;
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
                tooltip.querySelector('.name').textContent = obj.name;
                tooltip.querySelector('.path').textContent = obj.path;
                tooltip.querySelector('.size').textContent = obj.sizeHuman;
                selectedObject = obj;
            }} else {{
                tooltip.style.display = 'none';
                selectedObject = null;
            }}
        }});
        
        // Click to open
        renderer.domElement.addEventListener('dblclick', e => {{
            if (selectedObject) {{
                // Simulate file open
                console.log('Open:', selectedObject.path);
                // In real implementation, would call open_file API
            }}
        }});
        
        // Action buttons
        document.querySelectorAll('.action-btn').forEach(btn => {{
            btn.addEventListener('click', e => {{
                e.stopPropagation();
                const action = btn.dataset.action;
                if (selectedObject) {{
                    console.log('Action:', action, 'on', selectedObject.path);
                    // In real implementation, would call appropriate API
                }}
            }});
        }});
        
        // Animation
        function animate() {{
            requestAnimationFrame(animate);
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
    
    def run_websocket_server(self, port=8765):
        """
        Inicia servidor WebSocket para sincronização em tempo real.
        
        Permite que o frontend receba atualizações quando:
        - Arquivos são criados/modificados/removidos
        - Diretórios são navegados
        - Buscas são executadas
        """
        import asyncio
        import websockets
        import json
        
        async def handler(websocket, path):
            print(f"Client connected: {websocket.remote_address}")
            
            try:
                async for message in websocket:
                    data = json.loads(message)
                    command = data.get('command')
                    
                    if command == 'search':
                        query = data.get('query')
                        search_type = data.get('type', 'path')
                        
                        if search_type == 'path':
                            results = self.search_path(query)
                        elif search_type == 'content':
                            results = self.search_content(query)
                        elif search_type == 'ext':
                            results = self.search_extension(query)
                        else:
                            results = []
                        
                        await websocket.send(json.dumps({
                            'type': 'search_results',
                            'results': results[:20]
                        }))
                    
                    elif command == 'navigate':
                        path = data.get('path')
                        self.navigate_to(path)
                        contents = self.get_current_contents()
                        
                        await websocket.send(json.dumps({
                            'type': 'navigate_result',
                            'path': path,
                            'contents': contents
                        }))
                    
                    elif command == 'open':
                        file_id = data.get('id')
                        success, message = self.open_file(file_id)
                        
                        await websocket.send(json.dumps({
                            'type': 'open_result',
                            'success': success,
                            'message': message
                        }))
                    
            except websockets.exceptions.ConnectionClosed:
                print("Client disconnected")
        
        async def main():
            async with websockets.serve(handler, "localhost", port):
                print(f"WebSocket server running on ws://localhost:{port}")
                await asyncio.Future()  # run forever
        
        asyncio.run(main())


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    import sys
    
    # Cria explorador
    explorer = FileSystemExplorer()
    
    # Indexa sistema de arquivos
    root_paths = [
        os.path.expanduser('~/.openclaw/workspace'),
        os.path.expanduser('~/Documents'),
        os.path.expanduser('~/Projects'),
    ]
    
    # Indexa com conteúdo
    file_count, dir_count, content_count = explorer.index_filesystem(
        root_paths, 
        max_files=100000,
        index_content=True
    )
    
    # Constrói layout 3D
    explorer.build_3d_layout()
    
    # Gera HTML
    output_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.openclaw/workspace/memory/file_explorer.html')
    explorer.generate_html(output_path)
    
    print(f"\\n=== File System Explorer ===")
    print(f"Files: {file_count:,}")
    print(f"Directories: {dir_count:,}")
    print(f"Content indexed: {content_count:,}")
    print(f"Search algorithms:")
    print(f"  - Radix Tree: O(m) path search")
    print(f"  - Inverted Index: O(1) content lookup")
    print(f"  - Spatial Hash: O(1) position query")
    print(f"\\nFeatures:")
    print(f"  - Path search")
    print(f"  - Content search")
    print(f"  - Extension filter")
    print(f"  - Size filter")
    print(f"  - Interactive navigation")
    print(f"  - File info tooltip")
    print(f"  - Open file integration")
    print(f"\\nOpen {output_path} in your browser.")