#!/usr/bin/env python3
"""
Memory Graph Server
===================

Servidor Flask para grafo 3D de memórias.

Funcionalidades:
- Lê MEMORY.md e memory/*.md
- Extrai links entre arquivos
- Serve grafo como JSON
- Salva edições
"""

import os
import re
import json
import glob
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(WORKSPACE, 'MEMORY.md')
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')

def parse_markdown_file(filepath):
    """Extrai conteúdo e links de um arquivo markdown."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None, [], []
    
    # Extrair título (primeiro # ou nome do arquivo)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = os.path.basename(filepath)
    
    # Extrair links [[wikilink]]
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
    
    # Extrair links markdown [text](url)
    mdlinks = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    
    # Links para outros arquivos de memória
    links = []
    for link in wikilinks:
        links.append(link)
    for text, url in mdlinks:
        if url.endswith('.md') or url.startswith('memory/'):
            links.append(url)
    
    # Extrair tags #tag
    tags = re.findall(r'#(\w+)', content)
    
    # Extrair data do nome do arquivo (YYYY-MM-DD.md)
    basename = os.path.basename(filepath)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', basename)
    date = date_match.group(1) if date_match else None
    
    return {
        'id': filepath.replace(WORKSPACE, '').lstrip('/'),
        'title': title,
        'content': content,
        'links': links,
        'tags': tags,
        'date': date,
        'modified': os.path.getmtime(filepath)
    }

def build_graph():
    """Constrói o grafo de memórias."""
    nodes = []
    links = []
    
    # Adicionar MEMORY.md principal
    if os.path.exists(MEMORY_FILE):
        node = parse_markdown_file(MEMORY_FILE)
        if node:
            node['id'] = 'MEMORY.md'
            node['type'] = 'core'
            nodes.append(node)
    
    # Adicionar arquivos em memory/
    if os.path.exists(MEMORY_DIR):
        for filepath in glob.glob(os.path.join(MEMORY_DIR, '*.md')):
            node = parse_markdown_file(filepath)
            if node:
                # Determinar tipo
                if node['date']:
                    node['type'] = 'daily'
                else:
                    node['type'] = 'note'
                nodes.append(node)
    
    # Construir links entre nodos
    node_ids = {n['id'] for n in nodes}
    
    for node in nodes:
        for link in node['links']:
            # Normalizar link
            target = link
            if not target.endswith('.md'):
                target += '.md'
            if target in node_ids:
                links.append({
                    'source': node['id'],
                    'target': target,
                    'type': 'link'
                })
            elif f'memory/{target}' in node_ids:
                links.append({
                    'source': node['id'],
                    'target': f'memory/{target}',
                    'type': 'link'
                })
    
    # Links temporais (memórias diárias conectam ao dia anterior)
    daily_nodes = sorted([n for n in nodes if n['type'] == 'daily'], 
                         key=lambda x: x['date'] or '')
    for i in range(len(daily_nodes) - 1):
        links.append({
            'source': daily_nodes[i]['id'],
            'target': daily_nodes[i+1]['id'],
            'type': 'temporal'
        })
    
    # Todos os nodos conectam ao MEMORY.md principal
    core_node = next((n for n in nodes if n['type'] == 'core'), None)
    if core_node:
        for node in nodes:
            if node['id'] != core_node['id']:
                # Verificar se já existe link
                exists = any(l['source'] == core_node['id'] and l['target'] == node['id'] 
                           for l in links)
                if not exists:
                    links.append({
                        'source': core_node['id'],
                        'target': node['id'],
                        'type': 'core'
                    })
    
    return {'nodes': nodes, 'links': links}

@app.route('/')
def index():
    """Serve o arquivo HTML principal."""
    return send_from_directory(WORKSPACE, 'memory_graph.html')

@app.route('/api/graph')
def get_graph():
    """Retorna o grafo como JSON."""
    # Usar grafo conceitual se existir
    concept_path = os.path.join(WORKSPACE, 'concept_graph.json')
    if os.path.exists(concept_path):
        with open(concept_path, 'r', encoding='utf-8') as f:
            import json
            return jsonify(json.load(f))
    
    # Fallback para grafo temporal
    graph = build_graph()
    return jsonify(graph)

@app.route('/api/node/<path:node_id>')
def get_node(node_id):
    """Retorna um nodo específico."""
    if node_id == 'MEMORY.md':
        filepath = MEMORY_FILE
    else:
        filepath = os.path.join(WORKSPACE, node_id)
    
    if os.path.exists(filepath):
        node = parse_markdown_file(filepath)
        if node:
            return jsonify(node)
    
    return jsonify({'error': 'Node not found'}), 404

@app.route('/api/node/<path:node_id>', methods=['PUT'])
def update_node(node_id):
    """Atualiza um nodo."""
    if node_id == 'MEMORY.md':
        filepath = MEMORY_FILE
    else:
        filepath = os.path.join(WORKSPACE, node_id)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Node not found'}), 404
    
    data = request.json
    content = data.get('content', '')
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/node', methods=['POST'])
def create_node():
    """Cria um novo nodo."""
    data = request.json
    title = data.get('title', 'New Note')
    content = data.get('content', f'# {title}\n\n')
    
    # Criar nome de arquivo
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{safe_title}_{timestamp}.md'
    filepath = os.path.join(MEMORY_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        node = parse_markdown_file(filepath)
        return jsonify(node)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/node/<path:node_id>', methods=['DELETE'])
def delete_node(node_id):
    """Deleta um nodo."""
    if node_id == 'MEMORY.md':
        return jsonify({'error': 'Cannot delete core memory'}), 403
    
    filepath = os.path.join(WORKSPACE, node_id)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'Node not found'}), 404
    
    try:
        os.remove(filepath)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/link', methods=['POST'])
def create_link():
    """Cria um link entre nodos."""
    data = request.json
    source = data.get('source')
    target = data.get('target')
    
    if not source or not target:
        return jsonify({'error': 'Source and target required'}), 400
    
    # Adicionar link no arquivo fonte
    source_path = MEMORY_FILE if source == 'MEMORY.md' else os.path.join(WORKSPACE, source)
    
    if not os.path.exists(source_path):
        return jsonify({'error': 'Source node not found'}), 404
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Adicionar link no final se não existir
        link_text = f'[[{target}]]'
        if link_text not in content:
            content += f'\n\n{link_text}\n'
            with open(source_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"Memory Graph Server")
    print(f"===================")
    print(f"Workspace: {WORKSPACE}")
    print(f"Memory file: {MEMORY_FILE}")
    print(f"Memory dir: {MEMORY_DIR}")
    print(f"")
    print(f"Open: http://localhost:5001")
    print(f"")
    app.run(host='0.0.0.0', port=5001, debug=True)