#!/usr/bin/env python3
"""
Concept Graph Builder
=====================

Extrai conceitos das memórias e cria um grafo organizado por tópicos.

Conceitos são extraídos de:
1. Títulos e cabeçalhos
2. Termos técnicos
3. Entidades nomeadas
4. Relações explícitas ([[links]])
"""

import os
import re
import json
from collections import defaultdict
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(WORKSPACE, 'MEMORY.md')
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')

# Conceitos conhecidos (seed)
KNOWN_CONCEPTS = {
    # Identity
    'OpenClaw': {'category': 'identity', 'importance': 10},
    'Cássio': {'category': 'person', 'importance': 9},
    
    # Network Infrastructure
    'FortiGate 40F': {'category': 'hardware', 'importance': 8},
    'Firewall-LSA': {'category': 'hostname', 'importance': 7},
    'HP V1910-16G': {'category': 'hardware', 'importance': 7},
    'DataCom DM956': {'category': 'hardware', 'importance': 6},
    'VLAN': {'category': 'network', 'importance': 8},
    'Hard-switch': {'category': 'network', 'importance': 6},
    'Trunk': {'category': 'network', 'importance': 6},
    
    # Network Concepts
    'DHCP': {'category': 'protocol', 'importance': 5},
    'NAT': {'category': 'protocol', 'importance': 5},
    'SSH': {'category': 'protocol', 'importance': 6},
    'iDRAC': {'category': 'hardware', 'importance': 6},
    
    # Projects
    'Radiation Testing': {'category': 'project', 'importance': 8},
    'ArduCopter EKF': {'category': 'software', 'importance': 8},
    'MultiRad Framework': {'category': 'software', 'importance': 7},
    'Dataset Orchestrator': {'category': 'software', 'importance': 6},
    
    # Tools
    'LaTeX': {'category': 'tool', 'importance': 5},
    'Graphviz': {'category': 'tool', 'importance': 5},
    'Flask': {'category': 'tool', 'importance': 5},
    
    # Concepts
    'Bit Flip': {'category': 'concept', 'importance': 7},
    'Dead Reckoning': {'category': 'concept', 'importance': 6},
    'EKF3': {'category': 'algorithm', 'importance': 7},
    'Sensor Emulation': {'category': 'technique', 'importance': 6},
    
    # Communication
    'WhatsApp': {'category': 'integration', 'importance': 7},
    'Gmail': {'category': 'integration', 'importance': 6},
    
    # Security
    'FortiOS': {'category': 'software', 'importance': 6},
    'Firewall Policy': {'category': 'security', 'importance': 6},
}

# Relações conhecidas
KNOWN_RELATIONS = [
    ('OpenClaw', 'Cássio', 'serves'),
    ('FortiGate 40F', 'Firewall-LSA', 'hostname'),
    ('FortiGate 40F', 'FortiOS', 'runs'),
    ('FortiGate 40F', 'VLAN', 'configures'),
    ('FortiGate 40F', 'HP V1910-16G', 'connects'),
    ('HP V1910-16G', 'VLAN', 'trunk'),
    ('DataCom DM956', 'FortiGate 40F', 'bridge'),
    ('Radiation Testing', 'ArduCopter EKF', 'tests'),
    ('Radiation Testing', 'MultiRad Framework', 'uses'),
    ('Radiation Testing', 'Bit Flip', 'injects'),
    ('ArduCopter EKF', 'EKF3', 'implements'),
    ('EKF3', 'Dead Reckoning', 'uses'),
    ('MultiRad Framework', 'Sensor Emulation', 'performs'),
    ('Sensor Emulation', 'LD_PRELOAD', 'technique'),
    ('LaTeX', 'Graphviz', 'generates diagrams'),
    ('WhatsApp', 'Cássio', 'integration'),
    ('Gmail', 'Cássio', 'integration'),
]

def extract_concepts(text):
    """Extrai conceitos de um texto."""
    concepts = set()
    
    # Títulos markdown
    titles = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
    for title in titles:
        # Limpar título
        title = re.sub(r'[#*_`]', '', title).strip()
        concepts.add(title)
    
    # Termos técnicos (palavras com maiúscula no meio ou símbolos)
    technical = re.findall(r'\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b', text)  # CamelCase
    technical += re.findall(r'\b[A-Z]{2,}[0-9]*\b', text)  # VLAN, EKF3
    technical += re.findall(r'\b[A-Z]+-[A-Z0-9]+\b', text)  # FortiGate-40F
    concepts.update(technical)
    
    # Entidades nomeadas (palavras após "é", "foi", "da", "do")
    entities = re.findall(r'(?:é|foi|da|do|nas|no)\s+([A-Z][a-zA-Z]+)', text)
    concepts.update(entities)
    
    # IPs e endereços
    ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
    concepts.update(ips)
    
    # Wikilinks
    wikilinks = re.findall(r'\[\[([^\]]+)\]\]', text)
    concepts.update(wikilinks)
    
    # URLs
    urls = re.findall(r'https?://[^\s]+', text)
    concepts.update(urls)
    
    return concepts

def extract_relations(text, concepts):
    """Extrai relações entre conceitos."""
    relations = []
    
    # Padrões de relação
    patterns = [
        r'(\w+)\s+conect[aiu]\s+(\w+)',
        r'(\w+)\s+usa\s+(\w+)',
        r'(\w+)\s+configura\s+(\w+)',
        r'(\w+)\s+testa\s+(\w+)',
        r'(\w+)\s+→\s+(\w+)',
        r'(\w+)\s+->\s+(\w+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match[0] in concepts and match[1] in concepts:
                relations.append((match[0], match[1], 'relates'))
    
    return relations

def categorize_concept(concept):
    """Categoriza um conceito."""
    if concept in KNOWN_CONCEPTS:
        return KNOWN_CONCEPTS[concept]['category']
    
    # Heurísticas
    concept_lower = concept.lower()
    
    if any(w in concept_lower for w in ['vlan', 'dhcp', 'nat', 'ssh', 'dns', 'ip', 'network']):
        return 'network'
    if any(w in concept_lower for w in ['forti', 'hp', 'dell', 'datacom', 'switch', 'router', 'firewall']):
        return 'hardware'
    if any(w in concept_lower for w in ['ekf', 'framework', 'software', 'linux', 'kernel']):
        return 'software'
    if any(w in concept_lower for w in ['test', 'radiation', 'experiment', 'method']):
        return 'methodology'
    if any(w in concept_lower for w in ['algorithm', 'math', 'physics', 'ekf', 'kalman']):
        return 'algorithm'
    if any(w in concept_lower for w in ['integration', 'whatsapp', 'gmail', 'telegram', 'signal']):
        return 'integration'
    if any(w in concept_lower for w in ['security', 'policy', 'firewall', 'auth']):
        return 'security'
    if any(w in concept_lower for w in ['tool', 'latex', 'graphviz', 'python', 'flask']):
        return 'tool'
    if any(w in concept_lower for w in ['project', 'report', 'document']):
        return 'project'
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', concept):
        return 'ip_address'
    
    return 'concept'

def build_concept_graph():
    """Constrói o grafo de conceitos."""
    
    # Coletar todos os textos
    texts = {}
    
    # MEMORY.md principal
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            texts['MEMORY.md'] = f.read()
    
    # Arquivos diários
    if os.path.exists(MEMORY_DIR):
        for filepath in sorted(os.listdir(MEMORY_DIR)):
            if filepath.endswith('.md'):
                path = os.path.join(MEMORY_DIR, filepath)
                with open(path, 'r', encoding='utf-8') as f:
                    texts[f'memory/{filepath}'] = f.read()
    
    # Extrair conceitos
    all_concepts = set()
    concept_sources = defaultdict(list)
    concept_occurrences = defaultdict(int)
    
    for source, text in texts.items():
        concepts = extract_concepts(text)
        all_concepts.update(concepts)
        for concept in concepts:
            concept_sources[concept].append(source)
            concept_occurrences[concept] += text.count(concept)
    
    # Adicionar conceitos conhecidos
    all_concepts.update(KNOWN_CONCEPTS.keys())
    
    # Extrair relações
    all_relations = list(KNOWN_RELATIONS)
    
    for source, text in texts.items():
        relations = extract_relations(text, all_concepts)
        all_relations.extend(relations)
    
    # Construir nodos
    nodes = []
    
    for concept in sorted(all_concepts):
        # Ignorar conceitos muito comuns ou irrelevantes
        if len(concept) < 2 or concept.lower() in ['the', 'and', 'for', 'with', 'from', 'this', 'that']:
            continue
        
        category = categorize_concept(concept)
        importance = KNOWN_CONCEPTS.get(concept, {}).get('importance', 
                      min(10, concept_occurrences.get(concept, 1)))
        
        nodes.append({
            'id': concept,
            'label': concept,
            'category': category,
            'importance': importance,
            'occurrences': concept_occurrences.get(concept, 0),
            'sources': concept_sources.get(concept, []),
            'size': importance * 2,
        })
    
    # Construir links
    links = []
    
    for source, target, relation in all_relations:
        if source in all_concepts and target in all_concepts:
            links.append({
                'source': source,
                'target': target,
                'relation': relation,
            })
    
    # Adicionar links de co-ocorrência
    for concept1 in all_concepts:
        for concept2 in all_concepts:
            if concept1 != concept2:
                # Se aparecem juntos em mais de 1 fonte
                common_sources = set(concept_sources.get(concept1, [])) & \
                                  set(concept_sources.get(concept2, []))
                if len(common_sources) > 1:
                    links.append({
                        'source': concept1,
                        'target': concept2,
                        'relation': 'co-occurs',
                        'weight': len(common_sources),
                    })
    
    return {
        'nodes': nodes,
        'links': links,
        'categories': list(set(n['category'] for n in nodes)),
        'stats': {
            'total_concepts': len(nodes),
            'total_relations': len(links),
            'sources': list(texts.keys()),
        }
    }

if __name__ == '__main__':
    import json
    
    graph = build_concept_graph()
    
    print(f"Conceitos extraídos: {graph['stats']['total_concepts']}")
    print(f"Relações encontradas: {graph['stats']['total_relations']}")
    print(f"Categorias: {len(graph['categories'])}")
    print()
    
    # Mostrar por categoria
    by_category = defaultdict(list)
    for node in graph['nodes']:
        by_category[node['category']].append(node)
    
    for category in sorted(by_category.keys()):
        nodes = by_category[category]
        print(f"\n{category.upper()} ({len(nodes)} conceitos):")
        for node in sorted(nodes, key=lambda x: -x['importance'])[:5]:
            print(f"  - {node['label']} (importância: {node['importance']}, ocorrências: {node['occurrences']})")
    
    # Salvar grafo
    output_path = os.path.join(WORKSPACE, 'concept_graph.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    
    print(f"\nGrafo salvo em: {output_path}")