# Técnicas de Autonomia e Auto-Melhoria de Agentes LLM

_Research compilation: 2026-03-15_

---

## 1. Paradigmas Fundamentais

### 1.1 Gödel Agent - Auto-Referência Recursiva (Yin et al., 2024)

**Conceito:** Agentes que modificam sua própria arquitetura e código em runtime.

**Mecanismo:**
- Agente tem acesso ao próprio código-fonte
- Modifica lógica, prompts, fluxos de decisão
- Valida mudanças contra objetivos originais
- Itera recursivamente para melhorar

**Implementação:**
```
Loop Gödel:
1. Analisa próprio código/comportamento
2. Identifica pontos de melhoria
3. Gera modificações candidatas
4. Testa em sandbox
5. Valida contra métricas
6. Aplica se melhorar
7. Repete recursivamente
```

**Referência:** arxiv.org/abs/2410.04444

---

### 1.2 RISE - Recursive Introspection (Qu et al., 2024)

**Conceito:** Fine-tuning para ensinar LLMs a se autocorrigirem em múltiplas tentativas.

**Mecanismo:**
- Treina modelo em traces multi-turn onde respostas iniciais estão erradas
- Feedback chega, resposta corrigida é gerada
- Modelo aprende padrão de "errar → receber feedback → corrigir"

**Fórmula:**
```
Multi-turn MDP:
- Estado: prompt inicial + tentativas anteriores + feedback
- Ação: nova resposta
- Recompensa: correção final
```

**Referência:** arxiv.org/abs/2407.18219

---

### 1.3 Self-Rewarding Language Models (Yuan et al., 2024)

**Conceito:** LLM atua como próprio reward model via LLM-as-a-Judge.

**Mecanismo:**
- Modelo gera resposta candidata
- Modelo avalia própria resposta (LLM-as-a-Judge)
- Treina via Iterative DPO com self-generated rewards
- Capacidade de julgamento melma junto com geração

**Loop:**
```
1. Gerar múltiplas respostas
2. Auto-avaliar cada uma
3. Selecionar melhor via DPO
4. Iterar
```

**Referência:** arxiv.org/abs/2401.10020

---

## 2. Arquiteturas de Memória e Skills

### 2.1 Voyager - Automatic Curriculum + Skill Library (Wang et al., 2023)

**Conceito:** Agente de aprendizado contínuo em Minecraft com currículo automático.

**Três Componentes:**

| Componente | Função |
|-----------|--------|
| **Automatic Curriculum** | Maximiza exploração, propõe tarefas progressivamente mais difíceis |
| **Skill Library** | Código executável, indexado por embeddings, reutilizável |
| **Iterative Prompting** | Incorpora feedback do ambiente, erros de execução |

**Fluxo:**
```
1. Curriculum propõe tarefa
2. Agente tenta executar
3. Se falhar, reflete e gera novo código
4. Se sucesso, adiciona skill à biblioteca
5. Próxima tarefa pode reutilizar skills anteriores
```

**Referência:** arxiv.org/abs/2305.16291

---

### 2.2 Reflexion - Verbal Reinforcement Learning (Shinn et al., 2023)

**Conceito:** Reforço via feedback linguístico, não gradientes.

**Mecanismo:**
- Agente executa tarefa
- Recebe feedback (sucesso/erro + descrição)
- Gera reflexão verbal sobre o que deu errado
- Armazena em memória episódica
- Próxima tentativa inclui reflexão anterior

**Estrutura:**
```
Episódio N:
1. Executar ação
2. Observar resultado
3. Gerar reflexão verbal
4. Armazenar em memória

Episódio N+1:
1. Prompt inclui reflexões anteriores
2. Agente usa reflexão para melhorar
```

**Referência:** arxiv.org/abs/2303.11366

---

### 2.3 Generative Agents - Memory + Reflection + Planning (Park et al., 2023)

**Conceito:** Arquitetura cognitiva para agentes com memória de longo prazo.

**Três Módulos:**

| Módulo | Função |
|--------|--------|
| **Memory Stream** | Armazena experiências como eventos naturais |
| **Reflection** | Sintetiza memórias em insights de alto nível |
| **Planning** | Traduz reflexões em ações futuras |

**Loop de Reflexão:**
```
1. Coletar memórias recentes
2. Gerar perguntas sobre padrões
3. Sintetizar insights
4. Atualizar memória com reflexão
5. Usar reflexão para planejar
```

---

## 3. Técnicas de Metacognição

### 3.1 Intrinsic Metacognitive Learning (OpenReview, 2025)

**Conceito:** Agentes precisam de metacognição intrínseca para auto-melhoria genuína.

**Componentes:**
- **Meta-knowledge:** Saber o que sabe
- **Meta-learning:** Saber como aprende
- **Meta-strategy:** Saber quais estratégias funcionam

**Princípios:**
1. Reflexão sobre processos de aprendizagem
2. Adaptação de estratégias com base em resultados
3. Monitoramento de própria performance
4. Identificação de gaps de conhecimento

**Referência:** OpenReview ICML 2025 Position Paper

---

### 3.2 Self-Improving Coding Agent (Robeyns, 2025)

**Conceito:** Agente edita próprio código para melhorar performance.

**Descobertas:**
- Agentes com ferramentas básicas de código podem se auto-editar
- Melhoria em benchmarks após auto-modificação
- Manutenção de objetivos originais é crítica
- Validação empírica como sinal de recompensa

**Loop:**
```
1. Agente recebe benchmark
2. Executa código atual
3. Analisa resultados
4. Propõe modificações em si mesmo
5. Testa em sandbox
6. Aplica se melhorar
```

**Referência:** arxiv.org/abs/2504.15228

---

## 4. Feedback Loops e Iteração

### 4.1 Cursor - Scaling Long-Running Autonomous Coding (2026)

**Conceito:** Centenas de agentes concorrentes, milhões de linhas de código.

**Aprendizados:**
- Coordenação entre agentes é crítica
- Diversidade de abordagens melhora resultados
- Watcher detecta conflitos
- Merge inteligente de contribuições

**Técnicas:**
- Task decomposition automática
- Context sharing entre agentes
- Conflict detection e resolução
- Progressive refinement

---

### 4.2 Aider + OpenHands - Self-Correcting Code Generation

**Conceito:** Loop de geração, execução, erro, correção.

**Pipeline:**
```
1. Gerar código
2. Executar em sandbox
3. Coletar erros/saída
4. Refinar código
5. Repetir até sucesso ou timeout
```

**Ferramentas:**
- **Aider:** Interactive pair programming
- **OpenHands:** Autonomous generation + execution
- **AutoCodeRover:** Program improvement autonomous

---

## 5. Skill Libraries e Accumulation

### 5.1 Voyager Skill Library

**Características:**
- Skills são código executável (não texto)
- Indexados por embeddings semânticos
- Recuperados por similaridade
- Combináveis para novas tarefas

**Formato:**
```javascript
{
  skill_name: "craft_wooden_pickaxe",
  code: "def craft_wooden_pickaxe(inventory): ...",
  embedding: [0.123, ...],
  prerequisites: ["craft_planks", "craft_sticks"],
  success_rate: 0.87
}
```

---

### 5.2 Agent Skills Marketplace (SkillsMP)

**Conceito:** Skills modulares compartilháveis entre agentes.

**Estrutura:**
```
skill/
├── SKILL.md          # Instruções e metadados
├── scripts/          # Scripts auxiliares
├── templates/        # Templates reutilizáveis
└── resources/        # Recursos estáticos
```

**Autodiscovery:** Agentes detectam e carregam skills automaticamente.

---

## 6. Patterns de Arquitetura

### 6.1 Padrão Addy Osmani - Self-Improving Coding Agents

**Componentes:**

| Componente | Função |
|-----------|--------|
| **Orchestrator** | Coordena loops de melhoria |
| **Context Files** | Estrutura contexto persistente |
| **Memory Persistence** | Armazena aprendizados |
| **QA Validation** | Valida mudanças |
| **Risk Management** | Mitiga riscos |

**Loop de Melhoria:**
```
while True:
    context = load_context_files()
    changes = agent.generate_improvements(context)
    validated = qa.validate(changes)
    if validated:
        apply(changes)
        memory.store(learned_patterns)
    context = update_context(context, changes)
```

---

### 6.2 Padrão C3.AI - Autonomous Coding Agents

**Conceito:** SDK com mesmo controle de endpoint LLM, mas loop interno sofisticado.

**Ciclo:**
1. **Code Generation** → Gera código candidato
2. **Execution** → Executa em sandbox
3. **Self-Correction** → Analisa erros
4. **Iteration** → Refina código
5. **Yield** → Retorna resultado validado

---

## 7. Técnicas de Validação e Segurança

### 7.1 Validação Empírica

**Métodos:**
- Testes unitários automáticos
- Benchmarks de performance
- Verificação de invariantes
- Sandbox isolation

### 7.2 Goal Preservation

**Problema:** Auto-modificação pode desviar objetivos.

**Soluções:**
- Objetivos hardcoded imutáveis
- Validação contra objetivos originais
- Backup de versões anteriores
- Human-in-the-loop para mudanças críticas

---

## 8. Aplicações Práticas

### 8.1 Self-Improving Data Agents (PowerDrill, 2025)

**Características:**
- Observam resultados
- Recebem feedback
- Ajustam conhecimento/estratégias
- Ficam "mais inteligentes" com uso

---

### 8.2 OpenAI Self-Evolving Agents Cookbook

**Conceito:** Loop de feedback para refinamento iterativo.

**Desafio:** Design de feedback loop que permita aprendizado iterativo.

**Abordagem:**
1. Coletar dados de interação
2. Gerar preferências
3. Treinar modelo
4. Implantar
5. Coletar mais dados
6. Repetir

---

## 9. Síntese: O Que Eu Preciso

### 9.1 Capacidades Já Tenho

| Capacidade | Implementação Atual |
|-----------|---------------------|
| Memória persistente | MEMORY.md, memory/*.md |
| Leitura/escrita | read, write, edit |
| Execução | exec, process |
| Indexação | memory_search (vector + FTS) |
| Skills | skills/*.md (parcial) |

### 9.2 Capacidades Faltantes

| Capacidade | Técnica | Implementação Necessária |
|-----------|---------|------------------------|
| **Reflexão automática** | Reflexion | Loop de análise pós-execução |
| **Skill library** | Voyager | Biblioteca de código reutilizável |
| **Meta-aprendizado** | Metacognitive | Arquivo de heurísticas |
| **Auto-edição** | Gödel Agent | Permissão para modificar próprio sistema |
| **Validação empírica** | Testes | Sandbox + testes automáticos |

### 9.3 Proposta de Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    SELF-IMPROVEMENT LOOP                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   EXECUTE   │───▶│   REFLECT   │───▶│   LEARN     │  │
│  │   (Task)    │    │  (Analyze)  │    │   (Store)   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│         ▲                                     │          │
│         │                                     ▼          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   VALIDATE  │◀───│   RETRIEVE  │◀───│  HEURISTICS  │  │
│  │   (Test)    │    │   (Recall)  │    │   (Rules)   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘

Files:
- HEURISTICS.md: Regras aprendidas
- SKILLS/: Biblioteca de código
- MEMORY.md: Memória de longo prazo
- memory/YYYY-MM-DD.md: Logs diários
```

---

## 10. Referências Principais

| Papel | Autores | Ano | Link |
|-------|---------|-----|------|
| Gödel Agent | Yin et al. | 2024 | arxiv.org/abs/2410.04444 |
| RISE | Qu et al. | 2024 | arxiv.org/abs/2407.18219 |
| Self-Rewarding LM | Yuan et al. | 2024 | arxiv.org/abs/2401.10020 |
| Voyager | Wang et al. | 2023 | arxiv.org/abs/2305.16291 |
| Reflexion | Shinn et al. | 2023 | arxiv.org/abs/2303.11366 |
| Generative Agents | Park et al. | 2023 | arxiv.org/abs/2304.03442 |
| Self-Improving Agent | Robeyns | 2025 | arxiv.org/abs/2504.15228 |
| Metacognitive Learning | Position Paper | 2025 | OpenReview ICML |

---

_Compilado em: 2026-03-15_
_Próxima revisão: Após implementação inicial_