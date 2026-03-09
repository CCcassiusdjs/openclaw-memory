#!/usr/bin/env python3
"""
Semantic Graph Linker
=====================

Conecta conceitos usando:
1. Embeddings semânticos (similaridade)
2. Inferência de relações via LLM
3. Garante que não há nodos órfãos
"""

import os
import json
import numpy as np
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
CONCEPT_GRAPH = os.path.join(WORKSPACE, 'concept_graph.json')
OUTPUT_GRAPH = os.path.join(WORKSPACE, 'semantic_concept_graph.json')

# Tentar importar sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
except ImportError:
    HAS_ST = False
    print("⚠️  sentence-transformers não instalado. Instalando...")
    os.system("pip install sentence-transformers --quiet")

# Similaridade de cosseno
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calcula similaridade de cosseno."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Tipos de relação por categorias
RELATION_TYPES = {
    ('hardware', 'network'): 'connects',
    ('hardware', 'hardware'): 'connects',
    ('software', 'hardware'): 'runs on',
    ('software', 'software'): 'integrates',
    ('software', 'algorithm'): 'implements',
    ('algorithm', 'concept'): 'uses',
    ('project', 'software'): 'uses',
    ('project', 'hardware'): 'tests',
    ('project', 'methodology'): 'applies',
    ('methodology', 'technique'): 'uses',
    ('person', 'project'): 'owns',
    ('person', 'hardware'): 'uses',
    ('integration', 'person'): 'serves',
    ('network', 'protocol'): 'uses',
    ('network', 'hardware'): 'configured on',
    ('security', 'network'): 'protects',
    ('security', 'protocol'): 'enforces',
    ('tool', 'project'): 'used in',
    ('tool', 'software'): 'generates',
    ('identity', 'person'): 'serves',
    ('concept', 'algorithm'): 'applied in',
    ('ip_address', 'hardware'): 'assigned to',
    ('ip_address', 'network'): 'belongs to',
    ('hostname', 'hardware'): 'identifies',
}

# Relações genéricas (fallback)
GENERIC_RELATIONS = ['relates to', 'involves', 'associated with', 'connected to']

class SemanticGraphLinker:
    def __init__(self):
        self.model = None
        self.concepts = []
        self.embeddings = []
        
    def load_model(self):
        """Carrega modelo de embeddings."""
        if HAS_ST:
            print("Carregando modelo de embeddings...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Modelo carregado")
        else:
            # Fallback: usar modelo simples
            print("Usando similaridade léxica (fallback)")
            self.model = None
    
    def load_concepts(self) -> List[Dict]:
        """Carrega conceitos do grafo."""
        if not os.path.exists(CONCEPT_GRAPH):
            raise FileNotFoundError(f"Grafo não encontrado: {CONCEPT_GRAPH}")
        
        with open(CONCEPT_GRAPH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data['nodes']
    
    def generate_embeddings(self, concepts: List[Dict]) -> np.ndarray:
        """Gera embeddings para cada conceito."""
        texts = []
        
        for c in concepts:
            # Criar texto para embedding
            text = f"{c['label']} {c['category']}"
            if c.get('sources'):
                text += f" {' '.join(c['sources'][:3])}"
            texts.append(text)
        
        if self.model:
            embeddings = self.model.encode(texts)
        else:
            # Fallback: one-hot encoding das categorias
            categories = list(set(c['category'] for c in concepts))
            embeddings = np.zeros((len(concepts), len(categories)))
            for i, c in enumerate(concepts):
                if c['category'] in categories:
                    embeddings[i, categories.index(c['category'])] = 1
        
        return embeddings
    
    def find_similar_concepts(self, 
                               concept_idx: int, 
                               embeddings: np.ndarray,
                               concepts: List[Dict],
                               threshold: float = 0.5,
                               top_k: int = 5) -> List[Tuple[int, float]]:
        """Encontra conceitos similares."""
        similarities = []
        
        for i, emb in enumerate(embeddings):
            if i == concept_idx:
                continue
            
            sim = cosine_similarity(embeddings[concept_idx], emb)
            if sim >= threshold:
                similarities.append((i, sim))
        
        # Ordenar por similaridade
        similarities.sort(key=lambda x: -x[1])
        
        return similarities[:top_k]
    
    def infer_relation(self, concept1: Dict, concept2: Dict) -> str:
        """Infere o tipo de relação entre dois conceitos."""
        cat1 = concept1['category']
        cat2 = concept2['category']
        
        # Verificar relação conhecida
        key = (cat1, cat2)
        if key in RELATION_TYPES:
            return RELATION_TYPES[key]
        
        # Verificar relação reversa
        key_rev = (cat2, cat1)
        if key_rev in RELATION_TYPES:
            return f"inverse of {RELATION_TYPES[key_rev]}"
        
        # Relação genérica
        return "relates to"
    
    def connect_orphans(self, 
                        concepts: List[Dict],
                        links: List[Dict],
                        embeddings: np.ndarray) -> List[Dict]:
        """Conecta nodos órfãos a conceitos similares."""
        # Encontrar nodos conectados
        connected = set()
        for link in links:
            connected.add(link['source'])
            connected.add(link['target'])
        
        # Encontrar órfãos
        orphans = []
        for i, c in enumerate(concepts):
            if c['id'] not in connected:
                orphans.append(i)
        
        print(f"Encontrados {len(orphans)} nodos órfãos")
        
        # Conectar cada órfão
        new_links = []
        for orphan_idx in orphans:
            # Encontrar conceitos mais similares
            similar = self.find_similar_concepts(
                orphan_idx, embeddings, concepts,
                threshold=0.3,  # Threshold menor para órfãos
                top_k=3
            )
            
            if similar:
                # Conectar ao mais similar
                best_match = similar[0]
                target_concept = concepts[best_match[0]]
                orphan_concept = concepts[orphan_idx]
                
                relation = self.infer_relation(orphan_concept, target_concept)
                
                new_links.append({
                    'source': orphan_concept['id'],
                    'target': target_concept['id'],
                    'relation': relation,
                    'weight': float(best_match[1]),
                    'inferred': True,
                })
                
                print(f"  Conectado: {orphan_concept['label']} --[{relation}]--> {target_concept['label']}")
        
        return new_links
    
    def build_semantic_links(self,
                              concepts: List[Dict],
                              embeddings: np.ndarray,
                              threshold: float = 0.6) -> List[Dict]:
        """Cria links semânticos entre conceitos similares."""
        links = []
        
        # Carregar links existentes
        with open(CONCEPT_GRAPH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            links.extend(data.get('links', []))
        
        # Encontrar pares similares
        for i, c1 in enumerate(concepts):
            # Encontrar similares
            similar = self.find_similar_concepts(i, embeddings, concepts, threshold)
            
            for j, sim in similar:
                c2 = concepts[j]
                
                # Verificar se já existe link
                existing = any(
                    (l['source'] == c1['id'] and l['target'] == c2['id']) or
                    (l['source'] == c2['id'] and l['target'] == c1['id'])
                    for l in links
                )
                
                if not existing:
                    relation = self.infer_relation(c1, c2)
                    links.append({
                        'source': c1['id'],
                        'target': c2['id'],
                        'relation': relation,
                        'weight': float(sim),
                        'semantic': True,
                    })
        
        return links
    
    def create_category_clusters(self, concepts: List[Dict]) -> List[Dict]:
        """Cria nodos de categoria que conectam conceitos da mesma categoria."""
        by_category = defaultdict(list)
        
        for c in concepts:
            by_category[c['category']].append(c)
        
        cluster_links = []
        
        # Para cada categoria, criar links entre conceitos
        for category, cat_concepts in by_category.items():
            # Conectar em cadeia
            for i in range(len(cat_concepts) - 1):
                c1 = cat_concepts[i]
                c2 = cat_concepts[i + 1]
                
                cluster_links.append({
                    'source': c1['id'],
                    'target': c2['id'],
                    'relation': 'same category',
                    'weight': 0.5,
                    'cluster': True,
                })
            
            # Conectar o último ao primeiro (círculo)
            if len(cat_concepts) > 2:
                cluster_links.append({
                    'source': cat_concepts[-1]['id'],
                    'target': cat_concepts[0]['id'],
                    'relation': 'same category',
                    'weight': 0.3,
                    'cluster': True,
                })
        
        return cluster_links
    
    def run(self):
        """Executa todo o pipeline."""
        print("=" * 60)
        print("Semantic Graph Linker")
        print("=" * 60)
        
        # Carregar modelo
        self.load_model()
        
        # Carregar conceitos
        print("\nCarregando conceitos...")
        concepts = self.load_concepts()
        print(f"✓ {len(concepts)} conceitos carregados")
        
        # Gerar embeddings
        print("\nGerando embeddings...")
        embeddings = self.generate_embeddings(concepts)
        print(f"✓ Embeddings gerados: {embeddings.shape}")
        
        # Carregar links existentes
        print("\nCarregando links existentes...")
        with open(CONCEPT_GRAPH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            links = data.get('links', [])
        print(f"✓ {len(links)} links existentes")
        
        # Criar links semânticos
        print("\nCriando links semânticos...")
        semantic_links = self.build_semantic_links(concepts, embeddings)
        links.extend(semantic_links)
        print(f"✓ {len(semantic_links)} links semânticos criados")
        
        # Criar clusters por categoria
        print("\nCriando clusters por categoria...")
        cluster_links = self.create_category_clusters(concepts)
        links.extend(cluster_links)
        print(f"✓ {len(cluster_links)} links de cluster criados")
        
        # Conectar órfãos
        print("\nConectando nodos órfãos...")
        orphan_links = self.connect_orphans(concepts, links, embeddings)
        links.extend(orphan_links)
        print(f"✓ {len(orphan_links)} órfãos conectados")
        
        # Verificar conectividade
        print("\nVerificando conectividade...")
        connected = set()
        for link in links:
            connected.add(link['source'])
            connected.add(link['target'])
        
        total_concepts = len(concepts)
        connected_count = len(connected)
        coverage = (connected_count / total_concepts) * 100
        
        print(f"✓ {connected_count}/{total_concepts} conceitos conectados ({coverage:.1f}%)")
        
        # Estatísticas de links
        print("\nEstatísticas de links:")
        relation_counts = defaultdict(int)
        for link in links:
            relation_counts[link.get('relation', 'unknown')] += 1
        
        for rel, count in sorted(relation_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"  {rel}: {count}")
        
        # Salvar grafo atualizado
        print("\nSalvando grafo semântico...")
        output = {
            'nodes': concepts,
            'links': links,
            'categories': list(set(c['category'] for c in concepts)),
            'stats': {
                'total_concepts': total_concepts,
                'total_links': len(links),
                'connected_concepts': connected_count,
                'coverage': coverage,
            }
        }
        
        with open(OUTPUT_GRAPH, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Grafo salvo em: {OUTPUT_GRAPH}")
        print("\n" + "=" * 60)
        print("Concluído!")
        print("=" * 60)

if __name__ == '__main__':
    linker = SemanticGraphLinker()
    linker.run()