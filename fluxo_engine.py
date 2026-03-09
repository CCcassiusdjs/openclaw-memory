#!/usr/bin/env python3
"""
FLUXO Engine - Motor de Memória Temporal

Uma arquitetura baseada na neurociência real:
- Streams (correntes) em vez de nodos
- Confluences (confluências) em vez de arestas
- Depths (profundidades) em vez de camadas
- Current (correnteza) em vez de cursor

O FLUXO representa memória como um PROCESSO TEMPORAL,
não como armazenamento estático.
"""

import os
import re
import json
import math
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
import numpy as np

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(WORKSPACE, 'MEMORY.md')
MEMORY_DIR = os.path.join(WORKSPACE, 'memory')
FLUXO_STATE = os.path.join(WORKSPACE, 'FLUXO_STATE.json')

@dataclass
class Stream:
    """
    Stream = Padrão em fluxo, não um nodo estático.
    
    Representa um conceito/padrão na mente, mas como algo
    DINÂMICO e FLUIDO, não fixo.
    """
    id: str
    pattern: str                    # O conceito (ex: "FortiGate 40F")
    depth: float = 0.5              # 0=surface, 1=deep (estabilidade)
    flow: float = 0.0              # Ativação atual (0-1)
    turbulence: float = 0.0         # Taxa de mudança
    created: str = ""               # Quando entrou no fluxo
    last_flow: str = ""             # Última ativação
    
    # Sedimentos: memórias que se depositaram aqui
    sediments: List[Dict] = field(default_factory=list)
    
    # Confluências: streams que se misturam
    confluences: Dict[str, float] = field(default_factory=dict)  # {stream_id: strength}
    
    # Metadados
    category: str = "concept"
    content: str = ""


@dataclass
class Current:
    """
    Current = Onde a consciência está AGORA.
    
    O "ponto de consciência" que flui através dos streams.
    Não é um ponteiro - é uma posição dinâmica.
    """
    stream_id: str = ""             # Stream atual
    depth: float = 0.0              # Profundidade atual
    momentum: List[float] = field(default_factory=list)  # Direção do fluxo
    history: List[str] = field(default_factory=list)     # Caminho recente
    active_since: str = ""


@dataclass
class Eddy:
    """
    Eddy = Remoinho de reconsolidação.
    
    Quando lembramos, o fluxo forma um remoinho - 
    o padrão é reconstruído, não recuperado.
    """
    stream_ids: List[str]           # Streams envolvidos
    intensity: float = 0.0          # Força do remoinho
    cycle_rate: float = 0.1         # Velocidade de ciclo
    created: str = ""               # Quando começou


class Fluxo:
    """
    O Motor FLUXO - representa memória como fluxo temporal.
    """
    
    def __init__(self):
        self.streams: Dict[str, Stream] = {}
        self.current = Current()
        self.eddies: List[Eddy] = []
        
        # Profundidades (níveis de consolidação)
        self.depths = [
            {"depth": 0.0, "name": "surface", "age": "seconds"},
            {"depth": 0.3, "name": "working", "age": "minutes"},
            {"depth": 0.5, "name": "episodic", "age": "hours-days"},
            {"depth": 0.7, "name": "semantic", "age": "months-years"},
            {"depth": 1.0, "name": "sediment", "age": "permanent"}
        ]
    
    # ==================== OPERAÇÕES PRINCIPAIS ====================
    
    def learn(self, pattern: str, context: Dict = None):
        """
        EXPERIÊNCIA → MEMÓRIA
        
        O processo de aprendizagem cria um stream na superfície.
        Se repetido ou conectado, desce para profundidades.
        """
        # Criar ou atualizar stream
        stream_id = self._pattern_to_id(pattern)
        
        if stream_id not in self.streams:
            # Novo stream - começa na superfície
            stream = Stream(
                id=stream_id,
                pattern=pattern,
                depth=0.1,  # Superfície
                flow=1.0,   # Ativo agora
                turbulence=0.5,  # Alta turbulência inicial
                created=datetime.now().isoformat(),
                last_flow=datetime.now().isoformat(),
                category=context.get('category', 'concept') if context else 'concept',
                content=context.get('content', '') if context else ''
            )
            self.streams[stream_id] = stream
        else:
            # Stream existente - reativar e possivelmente aprofundar
            stream = self.streams[stream_id]
            stream.flow = min(1.0, stream.flow + 0.3)
            stream.turbulence = min(1.0, stream.turbulence + 0.1)
            stream.last_flow = datetime.now().isoformat()
            
            # Se repetido, desce para profundidades (consolidação)
            if len(stream.sediments) > 2:
                stream.depth = min(0.9, stream.depth + 0.1)
        
        # Adicionar sedimento (memória desta experiência)
        sediment = {
            "date": datetime.now().isoformat(),
            "weight": stream.flow,
            "context": context or {}
        }
        stream.sediments.append(sediment)
        
        # Formar confluências com streams ativos
        if context and 'related' in context:
            for related in context['related']:
                related_id = self._pattern_to_id(related)
                if related_id in self.streams:
                    # Fortalecer confluência
                    strength = stream.confluences.get(related_id, 0.0)
                    stream.confluences[related_id] = min(1.0, strength + 0.2)
                    
                    # Bidirecional
                    other = self.streams[related_id]
                    strength = other.confluences.get(stream_id, 0.0)
                    other.confluences[stream_id] = min(1.0, strength + 0.2)
        
        return stream_id
    
    def recall(self, query: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        MEMÓRIA ← EXPERIÊNCIA
        
        Recall não recupera - RECONSTRÓI.
        O fluxo forma um eddy que recombina fragmentos.
        """
        # Ativar streams por similaridade
        query_id = self._pattern_to_id(query)
        activated = []
        
        for stream_id, stream in self.streams.items():
            # Similaridade por:
            # 1. Match exato
            # 2. Confluências
            # 3. Similaridade semântica (simplificada)
            
            similarity = 0.0
            
            # Match exato
            if stream_id == query_id:
                similarity = 1.0
            
            # Confluências
            elif query_id in stream.confluences:
                similarity = stream.confluences[query_id]
            
            # Similaridade de padrão (substring)
            elif query.lower() in stream.pattern.lower():
                similarity = 0.5
            
            # Adicionar profundidade (memórias profundas são mais estáveis)
            similarity *= (0.5 + 0.5 * stream.depth)
            
            # Adicionar flow atual
            similarity *= (0.3 + 0.7 * stream.flow)
            
            if similarity > 0.01:
                activated.append((stream_id, similarity))
        
        # Ordenar por similaridade
        activated.sort(key=lambda x: -x[1])
        
        # Formar eddy (reconsolidação)
        if activated:
            involved_streams = [s[0] for s in activated[:3]]
            self._form_eddy(involved_streams)
        
        # Ativar streams (reconsolidação aumenta profundidade)
        for stream_id, _ in activated[:n]:
            if stream_id in self.streams:
                stream = self.streams[stream_id]
                stream.flow = min(1.0, stream.flow + 0.1)
                # Recall reconsolida - memória muda!
                stream.turbulence += 0.05
        
        return activated[:n]
    
    def imagine(self, seed: str, n: int = 3) -> List[str]:
        """
        FUTURO ← PASSADO
        
        Imaginação usa os mesmos circuitos de memória,
        mas RECOMBINA fragmentos em novos patterns.
        """
        # Começar com seed
        seed_id = self._pattern_to_id(seed)
        
        if seed_id not in self.streams:
            return []
        
        seed_stream = self.streams[seed_id]
        
        # Seguir confluências
        imagined = []
        
        # Pegar confluências mais fortes
        confluent = sorted(
            seed_stream.confluences.items(),
            key=lambda x: -x[1]
        )[:n * 2]
        
        for related_id, strength in confluent:
            if related_id in self.streams:
                related = self.streams[related_id]
                
                # Combinar patterns (imaginação)
                # Na realidade, seria mais complexo
                combination = f"{seed_stream.pattern} + {related.pattern}"
                imagined.append(combination)
                
                if len(imagined) >= n:
                    break
        
        return imagined
    
    def predict(self, context: str) -> Dict:
        """
        ANTICIPAÇÃO
        
        O cérebro é uma máquina de predição.
        FLUXO simula o futuro a partir do passado.
        """
        # Ativar streams do contexto
        activated = self.recall(context, n=10)
        
        if not activated:
            return {"prediction": "unknown", "confidence": 0.0}
        
        # Seguir gradientes de confluência
        predictions = defaultdict(float)
        
        for stream_id, strength in activated:
            stream = self.streams[stream_id]
            
            # Streams confluentes têm maior probabilidade
            for confluent_id, confluent_strength in stream.confluences.items():
                if confluent_id in self.streams:
                    confluent_stream = self.streams[confluent_id]
                    
                    # Probabilidade = força da ativação * força da confluência * profundidade
                    prob = strength * confluent_strength * (0.5 + 0.5 * confluent_stream.depth)
                    predictions[confluent_id] += prob
        
        # Ordenar previsões
        sorted_predictions = sorted(predictions.items(), key=lambda x: -x[1])
        
        # Normalizar
        total_prob = sum(p[1] for p in sorted_predictions[:5]) + 0.001
        
        return {
            "predictions": [
                {
                    "stream": self.streams[p[0]].pattern if p[0] in self.streams else p[0],
                    "probability": p[1] / total_prob
                }
                for p in sorted_predictions[:5]
            ],
            "context": context,
            "confidence": min(1.0, total_prob / 5)
        }
    
    # ==================== MÉTODOS DE FLUXO ====================
    
    def flow(self, from_stream: str, to_stream: str):
        """
        Faz o current fluir de um stream para outro.
        """
        if from_stream not in self.streams or to_stream not in self.streams:
            return
        
        # Calcular gradiente (direção do fluxo)
        from_s = self.streams[from_stream]
        to_s = self.streams[to_stream]
        
        # Gradiente baseado em confluência
        confluent_strength = from_s.confluences.get(to_stream, 0.0)
        
        # Atualizar current
        self.current.stream_id = to_stream
        self.current.history.append(from_stream)
        if len(self.current.history) > 10:
            self.current.history.pop(0)
        
        # Atualizar flows
        from_s.flow = max(0.0, from_s.flow - 0.1)
        to_s.flow = min(1.0, to_s.flow + confluent_strength)
    
    def settle(self):
        """
        Consolidação temporal.
        
        Streams não usados afundam nas profundidades.
        Streams usados permanecem flutuando.
        """
        now = datetime.now()
        
        for stream_id, stream in self.streams.items():
            # Calcular tempo desde último uso
            if stream.last_flow:
                last = datetime.fromisoformat(stream.last_flow)
                age_hours = (now - last).total_seconds() / 3600
                
                # Decay do flow (memória de curto prazo)
                stream.flow *= math.exp(-age_hours / 24)  # Half-life de 24h
                
                # Sedimentação (memória de longo prazo)
                if stream.flow < 0.1 and len(stream.sediments) > 0:
                    # Stream está sedimentando
                    stream.depth = min(1.0, stream.depth + 0.01)
                    stream.turbulence *= 0.9
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _pattern_to_id(self, pattern: str) -> str:
        """Converte pattern para ID único."""
        return re.sub(r'[^a-z0-9_]', '_', pattern.lower().strip())
    
    def _form_eddy(self, stream_ids: List[str]):
        """Forma um eddy (remoinho de reconsolidação)."""
        eddy = Eddy(
            stream_ids=stream_ids,
            intensity=0.5,
            cycle_rate=0.1,
            created=datetime.now().isoformat()
        )
        self.eddies.append(eddy)
        
        # Manter apenas eddies recentes
        if len(self.eddies) > 100:
            self.eddies = self.eddies[-100:]
    
    # ==================== SERIALIZAÇÃO ====================
    
    def save(self, path: str = None):
        """Salva o estado do FLUXO."""
        path = path or FLUXO_STATE
        
        state = {
            "streams": {
                k: {
                    "id": v.id,
                    "pattern": v.pattern,
                    "depth": v.depth,
                    "flow": v.flow,
                    "turbulence": v.turbulence,
                    "created": v.created,
                    "last_flow": v.last_flow,
                    "sediments": v.sediments,
                    "confluences": v.confluences,
                    "category": v.category,
                    "content": v.content
                }
                for k, v in self.streams.items()
            },
            "current": {
                "stream_id": self.current.stream_id,
                "depth": self.current.depth,
                "momentum": self.current.momentum,
                "history": self.current.history,
                "active_since": self.current.active_since
            },
            "eddies": [
                {
                    "stream_ids": e.stream_ids,
                    "intensity": e.intensity,
                    "cycle_rate": e.cycle_rate,
                    "created": e.created
                }
                for e in self.eddies
            ],
            "depths": self.depths,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def load(self, path: str = None):
        """Carrega o estado do FLUXO."""
        path = path or FLUXO_STATE
        
        if not os.path.exists(path):
            return
        
        with open(path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # Carregar streams
        for k, v in state.get("streams", {}).items():
            self.streams[k] = Stream(
                id=v["id"],
                pattern=v["pattern"],
                depth=v["depth"],
                flow=v["flow"],
                turbulence=v["turbulence"],
                created=v["created"],
                last_flow=v["last_flow"],
                sediments=v["sediments"],
                confluences=v["confluences"],
                category=v["category"],
                content=v["content"]
            )
        
        # Carregar current
        c = state.get("current", {})
        self.current = Current(
            stream_id=c.get("stream_id", ""),
            depth=c.get("depth", 0.0),
            momentum=c.get("momentum", []),
            history=c.get("history", []),
            active_since=c.get("active_since", "")
        )
        
        # Carregar eddies
        for e in state.get("eddies", []):
            self.eddies.append(Eddy(
                stream_ids=e["stream_ids"],
                intensity=e["intensity"],
                cycle_rate=e["cycle_rate"],
                created=e["created"]
            ))
    
    # ==================== BUILDERS ====================
    
    def build_from_memories(self):
        """
        Constrói o FLUXO a partir das memórias existentes.
        
        Cada memória é aprendida como um padrão.
        """
        # Carregar MEMORY.md principal
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            self._extract_patterns(content, 'MEMORY.md', depth=0.7)
        
        # Carregar memórias diárias
        if os.path.exists(MEMORY_DIR):
            for filename in sorted(os.listdir(MEMORY_DIR)):
                if filename.endswith('.md'):
                    filepath = os.path.join(MEMORY_DIR, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Calcular profundidade baseada na idade
                    try:
                        date_str = filename.replace('.md', '')
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        age_days = (datetime.now() - date).days
                        depth = min(0.7, max(0.1, age_days / 30))  # ~1 mês = 0.7
                    except:
                        depth = 0.3
                    
                    self._extract_patterns(content, f'memory/{filename}', depth=depth)
        
        # Salvar estado
        self.save()
    
    def _extract_patterns(self, content: str, source: str, depth: float = 0.5):
        """Extrai patterns de um conteúdo."""
        # Títulos
        titles = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        for title in titles:
            title_clean = re.sub(r'[#*_`]', '', title).strip()
            self.learn(title_clean, {
                'category': 'title',
                'source': source,
                'content': title_clean,
                'depth': depth
            })
        
        # Termos técnicos
        technical = re.findall(r'\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b', content)  # CamelCase
        technical += re.findall(r'\b[A-Z]{2,}[0-9]*\b', content)  # VLAN, EKF3
        technical += re.findall(r'\b[A-Z]+-[A-Z0-9]+\b', content)  # FortiGate-40F
        
        for term in set(technical):
            if len(term) > 2:
                # Encontrar termos relacionados
                related = self._find_related(content, term)
                self.learn(term, {
                    'category': self._categorize(term),
                    'source': source,
                    'related': related[:5],
                    'depth': depth
                })
        
        # IPs
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content)
        for ip in set(ips):
            self.learn(ip, {
                'category': 'ip_address',
                'source': source,
                'depth': depth + 0.1
            })
    
    def _find_related(self, content: str, term: str) -> List[str]:
        """Encontra termos relacionados por proximidade."""
        related = []
        
        # Encontrar posição do termo
        pos = content.find(term)
        if pos == -1:
            return related
        
        # Pegar contexto ao redor
        context_start = max(0, pos - 200)
        context_end = min(len(content), pos + len(term) + 200)
        context = content[context_start:context_end]
        
        # Extrair outros termos técnicos do contexto
        other_terms = re.findall(r'\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b', context)
        other_terms += re.findall(r'\b[A-Z]{2,}[0-9]*\b', context)
        
        for other in set(other_terms):
            if other != term and len(other) > 2:
                related.append(other)
        
        return related
    
    def _categorize(self, term: str) -> str:
        """Categoriza um termo."""
        term_lower = term.lower()
        
        categories = {
            'network': ['vlan', 'dhcp', 'nat', 'ssh', 'dns', 'ip', 'network', 'wan', 'lan', 'port'],
            'hardware': ['forti', 'hp', 'dell', 'switch', 'router', 'firewall', 'idrac'],
            'software': ['ekf', 'framework', 'linux', 'kernel', 'python', 'code'],
            'project': ['test', 'radiation', 'experiment', 'report'],
            'person': ['cássio', 'user'],
        }
        
        for cat, keywords in categories.items():
            if any(k in term_lower for k in keywords):
                return cat
        
        return 'concept'
    
    # ==================== VISUALIZAÇÃO ====================
    
    def get_visualization_data(self) -> Dict:
        """
        Retorna dados para visualização do FLUXO.
        
        Formato otimizado para Three.js com fluid simulation.
        """
        # Streams como partículas fluidas
        particles = []
        for stream_id, stream in self.streams.items():
            # Posição baseada em profundidade e confluências
            # (será calculada pelo force-directed no cliente)
            particles.append({
                "id": stream_id,
                "pattern": stream.pattern,
                "depth": stream.depth,
                "flow": stream.flow,
                "turbulence": stream.turbulence,
                "category": stream.category,
                "size": 5 + stream.flow * 10,  # Tamanho baseado em ativação
                "opacity": 0.3 + stream.flow * 0.7,  # Opacidade baseada em flow
            })
        
        # Confluências como correntes
        currents = []
        for stream_id, stream in self.streams.items():
            for confluent_id, strength in stream.confluences.items():
                if strength > 0.1:  # Só mostrar conexões fortes
                    currents.append({
                        "source": stream_id,
                        "target": confluent_id,
                        "strength": strength,
                        "flow": min(stream.flow, self.streams.get(confluent_id, Stream(id="", pattern="")).flow)
                    })
        
        # Eddies como remoinhos
        eddies_data = []
        for eddy in self.eddies[-10:]:  # Últimos 10
            eddies_data.append({
                "streams": eddy.stream_ids,
                "intensity": eddy.intensity,
                "cycle_rate": eddy.cycle_rate
            })
        
        # Current como partícula brilhante
        current_data = {
            "stream_id": self.current.stream_id,
            "history": self.current.history[-5:]
        }
        
        return {
            "particles": particles,
            "currents": currents,
            "eddies": eddies_data,
            "current": current_data,
            "depths": self.depths
        }


if __name__ == '__main__':
    print("=" * 70)
    print("FLUXO - Motor de Memória Temporal")
    print("=" * 70)
    print()
    print("Uma arquitetura baseada na neurociência real:")
    print("- Streams (correntes) em vez de nodos")
    print("- Confluences em vez de arestas")
    print("- Depths em vez de camadas")
    print("- Current (correnteza) em vez de cursor")
    print()
    print("O FLUXO representa memória como PROCESSO TEMPORAL,")
    print("não como armazenamento estático.")
    print()
    
    # Criar e construir FLUXO
    fluxo = Fluxo()
    fluxo.build_from_memories()
    
    # Estatísticas
    print(f"Streams: {len(fluxo.streams)}")
    print(f"Confluences: {sum(len(s.confluences) for s in fluxo.streams.values())}")
    print(f"Eddies: {len(fluxo.eddies)}")
    print()
    
    # Testar recall
    print("Teste de recall 'FortiGate':")
    results = fluxo.recall("FortiGate", n=5)
    for stream_id, strength in results:
        print(f"  - {fluxo.streams[stream_id].pattern}: {strength:.2f}")
    print()
    
    # Testar predict
    print("Teste de predict 'rede':")
    prediction = fluxo.predict("rede")
    for pred in prediction.get("predictions", [])[:3]:
        print(f"  - {pred['stream']}: {pred['probability']:.2%}")
    print()
    
    # Testar imagine
    print("Teste de imagine 'VLAN':")
    imagined = fluxo.imagine("VLAN", n=3)
    for img in imagined:
        print(f"  - {img}")
    print()
    
    print(f"Estado salvo em: {FLUXO_STATE}")