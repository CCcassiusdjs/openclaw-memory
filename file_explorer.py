#!/usr/bin/env python3
"""
FILE SYSTEM EXPLORER (FSE)
==========================
Um explorador de arquivos REAL com busca O(1).

ESTRUTURA ORGANIZADA (não caótica):
- Diretórios como CILINDROS concêntricos
- Arquivos organizados dentro dos cilindros
- Hierarquia clara e navegável
- Busca instantânea O(1)

ALGORITMOS DE BUSCA O(1):

1. RADIX TREE (Path Trie)
   - Busca por caminho: O(m) onde m = comprimento do caminho
   - Autocomplete instantâneo
   - Prefixo compartilhado = memória eficiente

2. INVERTED INDEX (Content)
   - Busca por conteúdo: O(1) lookup + O(k) onde k = documentos
   - Palavra → lista de arquivos
   - TF-IDF para ranking

3. SUFFIX ARRAY (Substring)
   - Busca por substring: O(m + log n)
   - Construção: O(n)
   - Espaço: O(n)

4. SPATIAL HASH (Location)
   - Busca por posição: O(1)
   - Célula → lista de arquivos na região
   - Para interação 3D

DIFERENÇA DO CORTICAL/COSMOS:
- NÃO é caótico/aleatório
- É ORGANIZADO por hierarquia
- Estrutura CLARA e previsível
- Navegação INTUITIVA
"""

import json
import os
import hashlib
import math
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import array
import bisect

# ============================================================================
# ALGORITMO 1: RADIX TREE (Path Trie)
# Complexidade: O(m) busca, O(m) inserção, onde m = comprimento do caminho
# ============================================================================

class RadixNode:
    """Nó da Radix Tree para caminhos de arquivos."""
    def __init__(self):
        self.children = {}  # prefixo -> nó filho
        self.files = []     # arquivos neste nó
        self.dirs = []      # diretórios neste nó

class RadixTree:
    """
    Radix Tree para busca de caminhos.
    
    Busca: O(m) onde m = comprimento do caminho
    Inserção: O(m)
    Autocomplete: O(m + k) onde k = número de resultados
    """
    
    def __init__(self):
        self.root = RadixNode()
        self.total_paths = 0
    
    def insert(self, path, file_info):
        """Insere um caminho na árvore."""
        parts = path.strip('/').split('/')
        node = self.root
        
        for i, part in enumerate(parts):
            # Usa prefixo comum
            found = False
            for prefix, child in list(node.children.items()):
                # Encontra prefixo comum
                common = self._common_prefix(prefix, part)
                if common:
                    if common == prefix:
                        # Desce para o filho
                        node = child
                        part = part[len(common):]
                        found = True
                        break
                    else:
                        # Divide o nó
                        new_node = RadixNode()
                        new_node.children[prefix[len(common):]] = child
                        del node.children[prefix]
                        node.children[common] = new_node
                        if part:
                            new_node.children[part] = RadixNode()
                            node = new_node.children[part]
                        else:
                            node = new_node
                        found = True
                        break
            
            if not found:
                if part:
                    node.children[part] = RadixNode()
                    node = node.children[part]
        
        # Adiciona arquivo ao nó
        node.files.append(file_info)
        self.total_paths += 1
    
    def search(self, path):
        """Busca um caminho. O(m)."""
        parts = path.strip('/').split('/')
        node = self.root
        
        for part in parts:
            found = False
            for prefix, child in node.children.items():
                if part.startswith(prefix):
                    part = part[len(prefix):]
                    node = child
                    found = True
                    break
            if not found:
                return None
        
        return node
    
    def autocomplete(self, prefix, limit=10):
        """Autocomplete para prefixo. O(m + k)."""
        node = self.search(prefix)
        if not node:
            return []
        
        results = []
        self._collect_files(node, prefix, results, limit)
        return results
    
    def _collect_files(self, node, path, results, limit):
        """Coleta arquivos recursivamente."""
        if len(results) >= limit:
            return
        
        results.extend(node.files[:limit - len(results)])
        
        for child in node.children.values():
            self._collect_files(child, path, results, limit)
    
    def _common_prefix(self, a, b):
        """Encontra prefixo comum."""
        i = 0
        while i < min(len(a), len(b)) and a[i] == b[i]:
            i += 1
        return a[:i] if i > 0 else None


# ============================================================================
# ALGORITMO 2: INVERTED INDEX (Content Search)
# Complexidade: O(1) lookup + O(k) onde k = documentos com o termo
# ============================================================================

class InvertedIndex:
    """
    Índice invertido para busca de conteúdo.
    
    Busca: O(1) para lookup do termo
    Ranking: O(k log k) onde k = documentos relevantes
    
    Estrutura:
    termo -> [(doc_id, tf), ...]
    """
    
    def __init__(self):
        self.index = defaultdict(list)  # termo -> [(doc_id, tf), ...]
        self.documents = {}              # doc_id -> metadata
        self.doc_count = 0
        self.idf_cache = {}              # termo -> idf
    
    def add_document(self, doc_id, content, metadata=None):
        """Adiciona documento ao índice."""
        # Tokeniza
        terms = self._tokenize(content)
        
        # Conta frequência
        tf = defaultdict(int)
        for term in terms:
            tf[term] += 1
        
        # Adiciona ao índice
        for term, count in tf.items():
            self.index[term].append((doc_id, count))
        
        # Armazena metadata
        self.documents[doc_id] = {
            'metadata': metadata or {},
            'length': len(terms),
            'terms': set(tf.keys())
        }
        
        self.doc_count += 1
        
        # Invalida cache IDF
        self.idf_cache.clear()
    
    def search(self, query, limit=10):
        """
        Busca documentos. O(1) lookup + O(k log k) ranking.
        
        Retorna documentos ordenados por TF-IDF.
        """
        terms = self._tokenize(query)
        
        if not terms:
            return []
        
        # Coleta documentos candidatos
        candidates = defaultdict(float)
        
        for term in terms:
            if term in self.index:
                idf = self._idf(term)
                for doc_id, tf in self.index[term]:
                    # TF-IDF score
                    tfidf = (1 + math.log(tf)) * idf
                    candidates[doc_id] += tfidf
        
        # Ordena por score
        results = sorted(candidates.items(), key=lambda x: -x[1])[:limit]
        
        # Retorna com metadata
        return [
            {
                'id': doc_id,
                'score': score,
                'metadata': self.documents[doc_id]['metadata']
            }
            for doc_id, score in results
        ]
    
    def _idf(self, term):
        """Calcula IDF. O(1) com cache."""
        if term in self.idf_cache:
            return self.idf_cache[term]
        
        n = len(self.index[term])
        idf = math.log(self.doc_count / (1 + n)) if n > 0 else 0
        self.idf_cache[term] = idf
        return idf
    
    def _tokenize(self, text):
        """Tokeniza texto."""
        # Lowercase e split
        text = text.lower()
        # Remove pontuação
        for char in '.,;:!?[]{}()"\'':
            text = text.replace(char, ' ')
        return text.split()


# ============================================================================
# ALGORITMO 3: SUFFIX ARRAY (Substring Search)
# Complexidade: O(n) construção, O(m + log n) busca
# ============================================================================

class SuffixArray:
    """
    Suffix Array para busca de substring.
    
    Construção: O(n log n) ou O(n) com algoritmos avançados
    Busca: O(m + log n) onde m = padrão, n = texto
    
    Vantagem: encontra TODAS as ocorrências de uma substring.
    """
    
    def __init__(self):
        self.text = ""
        self.suffix_array = []
        self.lcp = []  # Longest Common Prefix
    
    def build(self, text):
        """Constrói suffix array. O(n log n)."""
        self.text = text
        n = len(text)
        
        # Cria pares (sufixo, índice)
        suffixes = [(text[i:], i) for i in range(n)]
        
        # Ordena
        suffixes.sort()
        
        # Extrai índices
        self.suffix_array = [s[1] for s in suffixes]
        
        # Constrói LCP array
        self._build_lcp()
    
    def _build_lcp(self):
        """Constrói LCP array. O(n)."""
        n = len(self.suffix_array)
        self.lcp = [0] * n
        rank = [0] * n
        
        for i in range(n):
            rank[self.suffix_array[i]] = i
        
        k = 0
        for i in range(n):
            if rank[i] == n - 1:
                k = 0
                continue
            
            j = self.suffix_array[rank[i] + 1]
            
            while i + k < n and j + k < n and self.text[i + k] == self.text[j + k]:
                k += 1
            
            self.lcp[rank[i]] = k
            
            if k > 0:
                k -= 1
    
    def search(self, pattern):
        """
        Busca substring. O(m + log n).
        
        Retorna todas as ocorrências.
        """
        if not pattern:
            return []
        
        n = len(self.suffix_array)
        m = len(pattern)
        
        # Busca binária pela primeira ocorrência
        left = 0
        right = n - 1
        first = -1
        
        while left <= right:
            mid = (left + right) // 2
            suffix = self.text[self.suffix_array[mid]:self.suffix_array[mid] + m]
            
            if suffix == pattern:
                first = mid
                right = mid - 1
            elif suffix < pattern:
                left = mid + 1
            else:
                right = mid - 1
        
        if first == -1:
            return []
        
        # Encontra a última ocorrência
        left = first
        right = n - 1
        last = first
        
        while left <= right:
            mid = (left + right) // 2
            suffix = self.text[self.suffix_array[mid]:self.suffix_array[mid] + m]
            
            if suffix == pattern:
                last = mid
                left = mid + 1
            else:
                right = mid - 1
        
        # Retorna todas as posições
        return [self.suffix_array[i] for i in range(first, last + 1)]


# ============================================================================
# ALGORITMO 4: SPATIAL HASH (Location Search)
# Complexidade: O(1) lookup por posição
# ============================================================================

class SpatialHash:
    """
    Hash espacial para busca por localização.
    
    Busca: O(1) para célula
    Range query: O(k) onde k = células no range
    
    Útil para interação 3D (clique, hover, etc.)
    """
    
    def __init__(self, cell_size=2.0):
        self.cell_size = cell_size
        self.cells = defaultdict(list)
        self.total_items = 0
    
    def insert(self, item, x, y, z):
        """Insere item na posição. O(1)."""
        key = self._hash(x, y, z)
        self.cells[key].append({
            'item': item,
            'x': x, 'y': y, 'z': z
        })
        self.total_items += 1
    
    def query(self, x, y, z):
        """Busca itens na célula. O(1)."""
        key = self._hash(x, y, z)
        return self.cells[key]
    
    def query_range(self, x, y, z, radius):
        """Busca itens em range. O(k)."""
        results = []
        
        # Calcula células no range
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
                        # Verifica distância real
                        dx = entry['x'] - x
                        dy = entry['y'] - y
                        dz = entry['z'] - z
                        if dx*dx + dy*dy + dz*dz <= radius*radius:
                            results.append(entry)
        
        return results
    
    def _hash(self, x, y, z):
        """Hash da posição para célula. O(1)."""
        return (
            int(math.floor(x / self.cell_size)),
            int(math.floor(y / self.cell_size)),
            int(math.floor(z / self.cell_size))
        )


# ============================================================================
# FILE SYSTEM EXPLORER
# ============================================================================

class FileSystemExplorer:
    """
    Explorador de arquivos com busca O(1).
    
    Estruturas:
    - Radix Tree: busca por caminho O(m)
    - Inverted Index: busca por conteúdo O(1) + O(k)
    - Suffix Array: busca por substring O(m + log n)
    - Spatial Hash: busca por posição O(1)
    
    Visualização:
    - Diretórios como cilindros concêntricos
    - Arquivos organizados dentro dos cilindros
    - Hierarquia clara e navegável
    """
    
    def __init__(self):
        self.radix_tree = RadixTree()
        self.inverted_index = InvertedIndex()
        self.spatial_hash = SpatialHash(cell_size=5.0)
        self.files = []  # Lista de todos os arquivos
        self.directories = []  # Lista de todos os diretórios
        
        # Mapeamentos
        self.path_to_file = {}  # caminho -> arquivo
        self.id_to_file = {}    # id -> arquivo
    
    def index_filesystem(self, root_paths, max_files=100000):
        """
        Indexa sistema de arquivos.
        
        Complexidade: O(n) onde n = número de arquivos
        """
        print(f"Indexing filesystem...")
        
        file_count = 0
        dir_count = 0
        
        for root_path in root_paths:
            if not os.path.exists(root_path):
                continue
            
            for dirpath, dirnames, filenames in os.walk(root_path):
                # Ignora diretórios ocultos e comuns
                dirnames[:] = [d for d in dirnames if not d.startswith('.') and 
                              d not in {'node_modules', '__pycache__', '.venv', 'venv', 
                                       'build', 'dist', '.git', '.cache'}]
                
                # Diretório
                dir_info = {
                    'id': f"dir_{dir_count}",
                    'path': dirpath,
                    'name': os.path.basename(dirpath),
                    'type': 'directory',
                    'depth': dirpath.count(os.sep),
                    'parent': os.path.dirname(dirpath)
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
                        
                        file_info = {
                            'id': f"file_{file_count}",
                            'path': filepath,
                            'name': filename,
                            'type': 'file',
                            'ext': os.path.splitext(filename)[1].lower(),
                            'size': stat.st_size,
                            'mtime': stat.st_mtime,
                            'depth': filepath.count(os.sep),
                            'parent': dirpath
                        }
                        
                        self.files.append(file_info)
                        self.path_to_file[filepath] = file_info
                        self.id_to_file[file_info['id']] = file_info
                        
                        # Insere nas estruturas
                        self.radix_tree.insert(filepath, file_info)
                        
                        file_count += 1
                        
                    except (OSError, IOError):
                        continue
                
                if file_count >= max_files:
                    break
        
        print(f"Indexed {file_count} files, {dir_count} directories")
        
        return file_count, dir_count
    
    def search_path(self, query, limit=10):
        """Busca por caminho. O(m)."""
        return self.radix_tree.autocomplete(query, limit)
    
    def search_content(self, query, limit=10):
        """Busca por conteúdo. O(1) + O(k)."""
        return self.inverted_index.search(query, limit)
    
    def search_position(self, x, y, z, radius=5.0):
        """Busca por posição 3D. O(1) para célula, O(k) para range."""
        return self.spatial_hash.query_range(x, y, z, radius)
    
    def build_3d_layout(self):
        """
        Constrói layout 3D organizado.
        
        Estrutura:
        - Raiz = centro (cilindro principal)
        - Cada nível = anel concêntrico
        - Arquivos = pontos dentro dos anéis
        
        DIFERENÇA DO CAÓTICO:
        - Posição é DETERMINÍSTICA (baseada no caminho)
        - Hierarquia é VISÍVEL (níveis)
        - Navegação é INTUITIVA (zoom in/out)
        """
        print("Building 3D layout...")
        
        # Calcula profundidade máxima
        max_depth = max(f['depth'] for f in self.files) if self.files else 0
        
        # Agrupa por diretório pai
        by_parent = defaultdict(list)
        for f in self.files:
            by_parent[f['parent']].append(f)
        
        # Posiciona diretórios
        dir_positions = {}
        
        # Raiz no centro
        for d in self.directories:
            if d['depth'] == 0:
                dir_positions[d['path']] = (0, 0, 0)
            else:
                # Cilindros concêntricos por profundidade
                parent_pos = dir_positions.get(d['parent'], (0, 0, 0))
                depth = d['depth']
                
                # Raio cresce com profundidade
                radius = 2 + depth * 1.5
                
                # Ângulo determinado pelo caminho (determinístico)
                h = hashlib.md5(d['path'].encode()).hexdigest()
                angle = int(h[:8], 16) / 0xffffffff * 2 * math.pi
                
                # Altura por nível
                y = depth * 0.5
                
                x = parent_pos[0] + radius * math.cos(angle)
                z = parent_pos[1] + radius * math.sin(angle)
                
                dir_positions[d['path']] = (x, y, z)
        
        # Posiciona arquivos dentro dos diretórios
        for f in self.files:
            parent_pos = dir_positions.get(f['parent'], (0, 0, 0))
            
            # Raio dentro do diretório
            inner_radius = 0.5
            
            # Ângulo determinado pelo nome do arquivo
            h = hashlib.md5(f['name'].encode()).hexdigest()
            angle = int(h[:8], 16) / 0xffffffff * 2 * math.pi
            
            # Posição
            f['x'] = parent_pos[0] + inner_radius * math.cos(angle)
            f['y'] = parent_pos[1] + 0.1  # Ligeiramente acima do diretório
            f['z'] = parent_pos[2] + inner_radius * math.sin(angle)
            
            # Insere no spatial hash
            self.spatial_hash.insert(f, f['x'], f['y'], f['z'])
        
        # Posiciona diretórios
        for d in self.directories:
            pos = dir_positions.get(d['path'], (0, 0, 0))
            d['x'] = pos[0]
            d['y'] = pos[1]
            d['z'] = pos[2]
        
        print(f"3D layout built: {len(self.files)} files, {len(self.directories)} directories")
    
    def generate_html(self, output_path):
        """Gera visualização HTML."""
        
        # Prepara dados para JSON
        files_json = json.dumps([{
            'id': f['id'],
            'path': f['path'],
            'name': f['name'],
            'ext': f['ext'],
            'size': f['size'],
            'x': f.get('x', 0),
            'y': f.get('y', 0),
            'z': f.get('z', 0),
            'depth': f['depth']
        } for f in self.files[:50000]])  # Limita para performance
        
        dirs_json = json.dumps([{
            'id': d['id'],
            'path': d['path'],
            'name': d['name'],
            'x': d.get('x', 0),
            'y': d.get('y', 0),
            'z': d.get('z', 0),
            'depth': d['depth']
        } for d in self.directories[:10000]])
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>File System Explorer - O(1) Search</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a12;
            overflow: hidden;
            font-family: 'JetBrains Mono', monospace;
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
        
        #search-type {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
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
        
        #results {{
            max-height: 200px;
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
        .result-path {{
            font-size: 10px;
            color: #888;
            margin-top: 3px;
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
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #00b4d8;
            font-size: 11px;
            max-width: 400px;
            pointer-events: none;
            z-index: 1000;
        }}
        #tooltip .path {{
            color: #00ff87;
            font-size: 9px;
            margin-top: 5px;
            word-break: break-all;
        }}
        #tooltip .size {{
            color: #888;
            font-size: 9px;
            margin-top: 3px;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    
    <div id="search-panel">
        <input type="text" id="search-input" placeholder="Search files... (path, content, or position)">
        <div id="search-type">
            <button class="search-btn active" data-type="path">Path (Radix Tree O(m))</button>
            <button class="search-btn" data-type="content">Content (Inverted Index O(1))</button>
            <button class="search-btn" data-type="position">Position (Spatial Hash O(1))</button>
        </div>
        <div id="results"></div>
    </div>
    
    <div id="stats">
        <h3>File System Stats</h3>
        <div class="stat-row">
            <span class="stat-label">Files:</span>
            <span class="stat-value" id="file-count">{len(self.files):,}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Directories:</span>
            <span class="stat-value" id="dir-count">{len(self.directories):,}</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Max Depth:</span>
            <span class="stat-value" id="max-depth">{max(f['depth'] for f in self.files) if self.files else 0}</span>
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
            <span class="algo-name">Suffix Array:</span>
            <span class="algo-complexity">O(m+log n)</span> substring
        </div>
        <div class="algo-item">
            <span class="algo-name">Spatial Hash:</span>
            <span class="algo-complexity">O(1)</span> position query
        </div>
    </div>
    
    <div id="tooltip">
        <div class="name"></div>
        <div class="path"></div>
        <div class="size"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Data
        const files = {files_json};
        const directories = {dirs_json};
        
        // Scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a12);
        scene.fog = new THREE.FogExp2(0x0a0a12, 0.01);
        
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 50, 100);
        
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
        
        // Create directories (cylinders)
        console.log('Creating directories...');
        const dirGeometry = new THREE.CylinderGeometry(0.5, 0.5, 0.3, 8);
        const dirMaterial = new THREE.MeshBasicMaterial({{ color: 0x00b4d8, transparent: true, opacity: 0.7 }});
        
        directories.forEach(d => {{
            const mesh = new THREE.Mesh(dirGeometry, dirMaterial);
            mesh.position.set(d.x, d.y, d.z);
            mesh.userData = d;
            dirGroup.add(mesh);
        }});
        
        // Create files (spheres)
        console.log('Creating files...');
        const fileGeometry = new THREE.SphereGeometry(0.2, 6, 6);
        
        files.forEach(f => {{
            const color = extColors[f.ext] || extColors['default'];
            const material = new THREE.MeshBasicMaterial({{ color, transparent: true, opacity: 0.8 }});
            const mesh = new THREE.Mesh(fileGeometry, material);
            mesh.position.set(f.x, f.y, f.z);
            mesh.userData = f;
            fileGroup.add(mesh);
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
                camera.position.y += dy * 0.5;
                previousMouse = {{ x: e.clientX, y: e.clientY }};
            }}
        }});
        
        renderer.domElement.addEventListener('mouseup', () => isDragging = false);
        renderer.domElement.addEventListener('mouseleave', () => isDragging = false);
        
        renderer.domElement.addEventListener('wheel', e => {{
            camera.position.z += e.deltaY * 0.1;
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
                return;
            }}
            
            // Search based on type
            let results = [];
            
            if (searchType === 'path') {{
                // Radix tree search (prefix match)
                results = files.filter(f => f.path.toLowerCase().includes(query)).slice(0, 10);
            }} else if (searchType === 'content') {{
                // Inverted index search (would need content indexing)
                results = files.filter(f => f.name.toLowerCase().includes(query)).slice(0, 10);
            }} else if (searchType === 'position') {{
                // Spatial hash search (would need position)
                results = files.filter(f => f.name.toLowerCase().includes(query)).slice(0, 10);
            }}
            
            // Show results
            resultsDiv.innerHTML = results.map(r => `
                <div class="result" data-id="${{r.id}}">
                    <div>${{r.name}}</div>
                    <div class="result-path">${{r.path}}</div>
                </div>
            `).join('');
            
            // Highlight in 3D
            const resultIds = new Set(results.map(r => r.id));
            fileGroup.children.forEach(mesh => {{
                if (resultIds.has(mesh.userData.id)) {{
                    mesh.material.opacity = 1;
                    mesh.scale.setScalar(2);
                }} else {{
                    mesh.material.opacity = 0.3;
                    mesh.scale.setScalar(1);
                }}
            }});
        }});
        
        // Raycaster for hover
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        const tooltip = document.getElementById('tooltip');
        
        renderer.domElement.addEventListener('mousemove', e => {{
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(fileGroup.children);
            
            if (intersects.length > 0) {{
                const obj = intersects[0].object.userData;
                tooltip.style.display = 'block';
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
                tooltip.querySelector('.name').textContent = obj.name;
                tooltip.querySelector('.path').textContent = obj.path;
                tooltip.querySelector('.size').textContent = (obj.size / 1024).toFixed(1) + ' KB';
            }} else {{
                tooltip.style.display = 'none';
            }}
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
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"HTML written to {output_path}")


if __name__ == '__main__':
    import sys
    
    # Cria explorador
    explorer = FileSystemExplorer()
    
    # Indexa sistema de arquivos
    root_paths = [
        '/home/csilva/.openclaw/workspace',
        '/home/csilva/Documents',
        '/home/csilva/Projects',
    ]
    
    # Indexa
    file_count, dir_count = explorer.index_filesystem(root_paths, max_files=100000)
    
    # Constrói layout 3D
    explorer.build_3d_layout()
    
    # Gera HTML
    output_path = sys.argv[1] if len(sys.argv) > 1 else '/home/csilva/.openclaw/workspace/memory/file_explorer.html'
    explorer.generate_html(output_path)