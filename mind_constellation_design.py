"""
Mind Constellation - Uma Nova Metáfora para Memória
====================================================

Por que grafos falham em representar a mente:

1. GRAFOS SÃO PLANOS
   - A mente tem profundidade temporal
   - Memórias recentes estão "no topo"
   - Memórias antigas formam "fundações"

2. GRAFOS SÃO ESTÁTICOS
   - A mente é dinâmica, conceitos mudam de importância
   - Conexões fortalecem com uso, enfraquecem sem uso
   - Novos conceitos "nascem", antigos "morrem"

3. GRAFOS SÃO SINTÉTICOS
   - A mente é orgânica, conceitos crescem uns dos outros
   - Ramificações naturais, não conexões arbitrárias
   - Hierarquias emergentes, não impostas

4. GRAFOS NÃO CAPTAM TEMPO
   - A mente tem "caminhos" - sequências de pensamento
   - Associações temporais, não apenas relacionais
   - Memória episódica vs. semântica

5. GRAFOS NÃO MOSTRAM INTENSIDADE
   - Conceitos têm "peso" variável
   - Conexões têm "força" variável
   - EMOÇÃO importa - memórias emocionais são mais fortes

====================================================

A METÁFORA: CONSTELAÇÃO MENTAL
==============================

Imagine o universo da mente como um espaço 3D com:

1. ESTRELAS (Conceitos)
   - Tamanho = Importância
   - Brilho = Frequência de uso
   - Cor = Categoria
   - Idade = Tempo desde criação

2. NEBULOSAS (Domínios de Conhecimento)
   - Regiões onde conceitos se agrupam
   - Densidade = Coesão do domínio
   - Cor = Área temática

3. ESTRELAS-GUIA (Conceitos Nucleares)
   - Estrelas centrais ao redor das quais outras orbitam
   - Ex: "OpenClaw", "Cássio", "FortiGate"
   - As mais brilhantes e estáveis

4. LINHAS DE FORÇA (Conexões)
   - Espessura = Força da conexão
   - Cor = Tipo de relação
   - Animadas no sentido do fluxo de pensamento

5. CAMADAS TEMPORAIS (Profundidade)
   - Memórias recentes = Camada superior (z alto)
   - Memórias antigas = Camadas profundas (z baixo)
   - Cresce como sedimentos geológicos

6. COMETAS (Pensamentos Ativos)
   - Movem-se entre estrelas
   - Representam pensamentos ativos
   - Deixam "rabo" de ativação

7. BURACOS NEGROS (Conceitos Ocultos)
   - Conceitos implícitos, não nomeados
   - Detectados pela atração que exercem
   - Ex: "rede" atrai muitos conceitos sem ser explícito

8. GALÁXIAS (Contextos Separados)
   - Grupos de conceitos pouco conectados entre si
   - Ex: "Radiation Testing" vs. "FortiGate"
   - Pontes inter-galácticas = Insights

====================================================

IMPLEMENTAÇÃO
==============

Camada 1: POSICIONAMENTO (Onde as estrelas estão)

- Conceitos nucleares no centro (0, 0, 0)
- Conceitos relacionados orbitam ao redor
- Distância = 1 / similaridade
- Altura (z) = recente - antigo

Camada 2: ATRIBUTOS (Como as estrelas são)

- Raio = log(importância + 1)
- Brilho = frequência de uso / max_frequência
- Cor = hash(categoria) em HSV
- Animação = pulsação se ativo recentemente

Camada 3: CONEXÕES (Como as estrelas se conectam)

- Força = co-ocorrência / max_co-ocorrência
- Direção = conceito_mais_importante → menos_importante
- Espessura = força
- Partículas fluem na direção do pensamento

Camada 4: INTERAÇÃO (Como o usuário explora)

- Zoom: aproximarse de uma nebulosa
- Rotação: ver de diferentes ângulos
- Clique em estrela: ver detalhes
- Clique em linha: ver relação
- Filtro por categoria: ver apenas uma nebulosa
- Timeline: ver como evoluiu

Camada 5: EDITOR (Como o usuário modifica)

- Adicionar estrela: criar novo conceito
- Adicionar linha: criar nova conexão
- Mover estrela: reorganizar
- Fundir estrelas: combinar conceitos
- Explodir estrela: criar sub-conceitos

====================================================

ESTRUTURA DE DADOS
==================

{
  "stars": [
    {
      "id": "fortigate_40f",
      "label": "FortiGate 40F",
      "category": "hardware",
      "position": [x, y, z],
      "importance": 8,
      "frequency": 19,
      "created": "2026-03-04",
      "last_accessed": "2026-03-07",
      "type": "core",  // core, regular, satellite
      "content": "Firewall de rede...",
      "sources": ["memory/2026-03-04.md"]
    }
  ],
  
  "nebulae": [
    {
      "id": "network_infra",
      "label": "Infraestrutura de Rede",
      "category": "network",
      "stars": ["fortigate_40f", "hp_v1910", "vlan", ...],
      "center": [cx, cy, cz],
      "radius": r
    }
  ],
  
  "connections": [
    {
      "source": "fortigate_40f",
      "target": "cassio",
      "relation": "managed_by",
      "strength": 0.8,
      "type": "ownership",
      "particles": true
    }
  ],
  
  "comets": [
    {
      "id": "active_thought",
      "path": ["star1", "star2", "star3"],
      "current": "star3",
      "trail": [...]
    }
  ],
  
  "blackholes": [
    {
      "position": [x, y, z],
      "mass": soma das atrações,
      "inferred_concept": "rede" (opcional)
    }
  ]
}

====================================================

ALGORITMOS
===========

1. POSICIONAMENTO INICIAL
   - Force-directed graph em 3D
   - Categoria como "galáxia"
   - Tempo como eixo Z
   
2. ATRAÇÃO GRAVITACIONAL
   - Estrelas-guia atraem outras
   - Similaridade semântica = força
   - Resistência = distância (anti-colisão)
   
3. PULSAÇÃO DE BRILHO
   - Estrelas ativas recentemente pulsam
   - Fade-out ao longo do tempo
   - Reativação aumenta brilho novamente
   
4. FLUXO DE PARTÍCULAS
   - Partículas fluem nas linhas de força
   - Direção = importância relativa
   - Velocidade = força da conexão
   
5. DETECÇÃO DE BURACOS NEGROS
   - Regiões com alta densidade mas sem estrelas centrais
   - Atração gravitacional sem fonte visível
   - Sugere conceito implícito a nomear

====================================================

DIFERENCIAL
===========

Por que isso é MELHOR que um grafo:

1. VISUALMENTE INTUITIVO
   - Estrelas grandes = importantes
   - Estrelas brilhantes = usadas recentemente
   - Agrupamentos visíveis naturalmente
   
2. TEMPORALMENTE ORGANIZADO
   - Ver o "fundo" da memória
   - Ver camadas de conhecimento acumulado
   - Timeline de aprendizado
   
3. DINÂMICO
   - Memória não é estática
   - Conceitos "nascem" e "morrem"
   - Conexões fortalecem com uso
   
4. ORGÂNICO
   - Cresce como um organismo
   - Ramificações naturais
   - Não artificial/sintético
   
5. EDITÁVEL
   - Adicionar conceitos cria estrelas
   - Conectar conceitos cria linhas de força
   - Organizar cria nebulosas
   
6. EXPLORÁVEL
   - Navegar como no espaço
   - Descobrir conexões inesperadas
   - Ver "buracos" (conhecimento faltando)

====================================================

PRÓXIMOS PASSOS
===============

1. Implementar com Three.js + 3D-force-graph
2. Extrair conceitos das memórias
3. Calcular similaridades semânticas
4. Posicionar estrelas inicialmente
5. Aplicar física gravitacional
6. Renderizar com partículas e brilho
7. Adicionar interação e edição

"""

print(__doc__)