#!/usr/bin/env python3
"""
Mind Constellation Server
==========================

Serve a Constelação Mental - uma representação 3D da mente
baseada em estrelas, nebulosas e linhas de força.

Conceitos são estrelas, organizados por:
1. Importância (tamanho)
2. Categoria (cor/nebulosa)
3. Tempo (altura no espaço 3D)
4. Conexões (linhas de força)

"""

import os
import re
import json
import math
from datetime import datetime
from collections import defaultdict
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(WORKSPACE, 'MEMORY.md')
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')

# Nebula colors (HSL)
NEBULA_COLORS = {
    'identity': {'h': 240, 's': 70, 'l': 60},
    'person': {'h': 300, 's': 70, 'l': 60},
    'hardware': {'h': 200, 's': 80, 'l': 60},
    'network': {'h': 140, 's': 70, 'l': 50},
    'software': {'h': 350, 's': 70, 'l': 60},
    'project': {'h': 50, 's': 80, 'l': 60},
    'tool': {'h': 180, 's': 70, 'l': 50},
    'integration': {'h': 160, 's': 60, 'l': 70},
    'security': {'h': 0, 's': 70, 'l': 60},
    'algorithm': {'h': 280, 's': 70, 'l': 60},
    'methodology': {'h': 20, 's': 70, 'l': 60},
    'technique': {'h': 30, 's': 60, 'l': 70},
    'protocol': {'h': 260, 's': 60, 'l': 70},
    'concept': {'h': 80, 's': 70, 'l': 50},
    'hostname': {'h': 270, 's': 70, 'l': 50},
    'ip_address': {'h': 220, 's': 80, 'l': 60},
}

# Core concepts (stars that others orbit around)
CORE_CONCEPTS = ['OpenClaw', 'Cássio', 'FortiGate 40F', 'Radiation Testing', 'ArduCopter EKF']

def extract_concepts(text, source_file):
    """Extrai conceitos de um texto."""
    concepts = {}
    
    # Títulos
    titles = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
    for title in titles:
        title_clean = re.sub(r'[#*_`]', '', title).strip()
        if len(title_clean) > 2:
            concepts[title_clean] = {
                'label': title_clean,
                'category': categorize(title_clean),
                'importance': 5,
                'sources': [source_file],
                'content': '',
                'type': 'regular',
            }
    
    # Termos técnicos
    technical = re.findall(r'\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b', text)  # CamelCase
    technical += re.findall(r'\b[A-Z]{2,}[0-9]*\b', text)  # VLAN, EKF3
    technical += re.findall(r'\b[A-Z]+-[A-Z0-9]+\b', text)  # FortiGate-40F
    
    for term in set(technical):
        if len(term) > 2:
            if term not in concepts:
                concepts[term] = {
                    'label': term,
                    'category': categorize(term),
                    'importance': count_importance(text, term),
                    'sources': [source_file],
                    'content': extract_context(text, term),
                    'type': 'core' if term in CORE_CONCEPTS else 'regular',
                }
            else:
                concepts[term]['sources'].append(source_file)
                concepts[term]['importance'] += count_importance(text, term)
    
    # IPs
    ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
    for ip in set(ips):
        concepts[ip] = {
            'label': ip,
            'category': 'ip_address',
            'importance': 3,
            'sources': [source_file],
            'content': f'Endereço IP mencionado em {source_file}',
            'type': 'satellite',
        }
    
    # Entidades nomeadas (após 'é', 'foi', etc.)
    entities = re.findall(r'(?:é|foi|da|do|nas|no|para|com)\s+([A-Z][a-zA-Z]+)', text)
    for entity in set(entities):
        if len(entity) > 2 and entity not in concepts:
            concepts[entity] = {
                'label': entity,
                'category': categorize(entity),
                'importance': 2,
                'sources': [source_file],
                'content': '',
                'type': 'satellite',
            }
    
    return concepts

def categorize(term):
    """Categoriza um termo."""
    term_lower = term.lower()
    
    if term_lower in ['openclaw', 'assistant', 'ai']:
        return 'identity'
    if term_lower in ['cássio', 'user', 'usuário']:
        return 'person'
    if any(w in term_lower for w in ['forti', 'hp', 'dell', 'switch', 'router', 'firewall', 'hardware', 'idrac']):
        return 'hardware'
    if any(w in term_lower for w in ['vlan', 'dhcp', 'nat', 'ssh', 'dns', 'ip', 'network', 'rede', 'wan', 'lan']):
        return 'network'
    if any(w in term_lower for w in ['ekf', 'framework', 'software', 'linux', 'kernel', 'ardupilot', 'code']):
        return 'software'
    if any(w in term_lower for w in ['test', 'radiation', 'experiment', 'project', 'relatório', 'report']):
        return 'project'
    if any(w in term_lower for w in ['latex', 'graphviz', 'python', 'flask', 'tool', 'ferramenta']):
        return 'tool'
    if any(w in term_lower for w in ['whatsapp', 'gmail', 'telegram', 'integration', 'email']):
        return 'integration'
    if any(w in term_lower for w in ['security', 'policy', 'firewall', 'auth', 'segurança']):
        return 'security'
    if any(w in term_lower for w in ['algorithm', 'kalman', 'math', 'física', 'physics']):
        return 'algorithm'
    if any(w in term_lower for w in ['method', 'methodology', 'método', 'processo']):
        return 'methodology'
    if any(w in term_lower for w in ['technique', 'técnica', 'emulation', 'simulação']):
        return 'technique'
    if any(w in term_lower for w in ['protocol', 'tcp', 'udp', 'http']):
        return 'protocol'
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', term):
        return 'ip_address'
    
    return 'concept'

def count_importance(text, term):
    """Conta a importância de um termo."""
    count = text.lower().count(term.lower())
    # Log scale
    return min(10, 3 + int(count / 5))

def extract_context(text, term, context_size=200):
    """Extrai contexto ao redor de um termo."""
    idx = text.lower().find(term.lower())
    if idx == -1:
        return ''
    
    start = max(0, idx - context_size // 2)
    end = min(len(text), idx + len(term) + context_size // 2)
    
    context = text[start:end]
    if start > 0:
        context = '...' + context
    if end < len(text):
        context = context + '...'
    
    return context.replace('\n', ' ').strip()

def build_constellation():
    """Constrói a constelação mental."""
    
    # Coletar conceitos de todas as memórias
    all_concepts = {}
    
    # MEMORY.md principal
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            concepts = extract_concepts(content, 'MEMORY.md')
            for k, v in concepts.items():
                if k in all_concepts:
                    all_concepts[k]['sources'].extend(v['sources'])
                    all_concepts[k]['importance'] += v['importance']
                else:
                    all_concepts[k] = v
    
    # Memórias diárias
    if os.path.exists(MEMORY_DIR):
        for filename in sorted(os.listdir(MEMORY_DIR)):
            if filename.endswith('.md'):
                filepath = os.path.join(MEMORY_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    concepts = extract_concepts(content, f'memory/{filename}')
                    for k, v in concepts.items():
                        if k in all_concepts:
                            all_concepts[k]['sources'].extend(v['sources'])
                            all_concepts[k]['importance'] += v['importance']
                        else:
                            all_concepts[k] = v
    
    # Extrair data de criação do filename
    for concept_id, concept in all_concepts.items():
        if concept['sources']:
            # Usar a primeira fonte como data de criação
            first_source = sorted(concept['sources'])[0]
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', first_source)
            concept['created'] = date_match.group(1) if date_match else None
    
    # Construir estrelas
    stars = []
    for concept_id, concept in all_concepts.items():
        # Determinar tipo
        star_type = concept.get('type', 'regular')
        if concept_id in CORE_CONCEPTS:
            star_type = 'core'
        
        # Limitar importância
        importance = min(10, max(1, concept['importance']))
        
        # Posição baseada em categoria e importância
        category_index = list(NEBULA_COLORS.keys()).index(concept['category']) if concept['category'] in NEBULA_COLORS else 0
        angle = (category_index / len(NEBULA_COLORS)) * 2 * 3.14159
        
        # Distância do centro baseada em importância (core = mais perto)
        distance = 20 if star_type == 'core' else (50 if star_type == 'regular' else 100)
        distance += (10 - importance) * 10
        
        # Altura (z) baseada em data
        z = 0
        if concept.get('created'):
            days_old = (datetime.now() - datetime.strptime(concept['created'], '%Y-%m-%d')).days
            z = -days_old * 0.5  # Mais antigo = mais baixo
        
        stars.append({
            'id': concept_id,
            'label': concept['label'],
            'category': concept['category'],
            'importance': importance,
            'frequency': len(concept['sources']),
            'type': star_type,
            'content': concept.get('content', ''),
            'sources': concept['sources'],
            'created': concept.get('created'),
            'position': {
                'x': distance * math.cos(angle),
                'y': distance * math.sin(angle),
                'z': z,
            }
        })
    
    # Construir conexões
    connections = []
    star_ids = set(s['id'] for s in stars)
    
    # Conexões baseadas em co-ocorrência
    for i, star1 in enumerate(stars):
        for j, star2 in enumerate(stars[i+1:], i+1):
            # Co-ocorrência em fontes
            common_sources = set(star1['sources']) & set(star2['sources'])
            if len(common_sources) > 0:
                strength = min(1.0, len(common_sources) / 5)
                
                # Verificar se categorias relacionadas
                cat1, cat2 = star1['category'], star2['category']
                
                # Categorias relacionadas têm conexões mais fortes
                related_categories = [
                    ('hardware', 'network'),
                    ('software', 'algorithm'),
                    ('project', 'methodology'),
                    ('identity', 'person'),
                    ('tool', 'project'),
                ]
                
                if (cat1, cat2) in related_categories or (cat2, cat1) in related_categories:
                    strength *= 1.5
                
                connections.append({
                    'source': star1['id'],
                    'target': star2['id'],
                    'relation': 'relates',
                    'strength': strength,
                })
    
    # Conexões de core para satellite
    core_stars = [s for s in stars if s['type'] == 'core']
    for core in core_stars:
        # Conectar a outros na mesma categoria
        same_category = [s for s in stars if s['category'] == core['category'] and s['id'] != core['id']]
        for star in same_category[:5]:  # Max 5 conexões por core
            connections.append({
                'source': core['id'],
                'target': star['id'],
                'relation': 'contains',
                'strength': 0.8,
            })
    
    # Calcular posições finais usando force-directed (simplificado)
    # (O 3d-force-graph fará isso no browser)
    
    return {
        'stars': stars,
        'connections': connections,
        'nebulae': list(NEBULA_COLORS.keys()),
        'stats': {
            'total_stars': len(stars),
            'total_connections': len(connections),
            'categories': len(NEBULA_COLORS),
        }
    }

@app.route('/')
def index():
    """Serve a página da constelação."""
    return send_from_directory(WORKSPACE, 'mind_constellation.html')

@app.route('/api/constellation')
def get_constellation():
    """Retorna os dados da constelação."""
    constellation = build_constellation()
    return jsonify(constellation)

@app.route('/api/star', methods=['POST'])
def create_star():
    """Cria uma nova estrela."""
    data = request.json
    label = data.get('label')
    
    if not label:
        return jsonify({'error': 'Label required'}), 400
    
    # Adicionar ao MEMORY.md
    star_entry = f"\n## {label}\n\n*New concept added on {datetime.now().strftime('%Y-%m-%d')}*\n\n"
    
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(star_entry)
    
    return jsonify({'success': True, 'label': label})

if __name__ == '__main__':
    print("=" * 60)
    print("Mind Constellation Server")
    print("=" * 60)
    print()
    print("Uma representação 3D da mente como constelação de estrelas.")
    print()
    print("Abra: http://localhost:5002")
    print()
    
    app.run(host='0.0.0.0', port=5002, debug=True)