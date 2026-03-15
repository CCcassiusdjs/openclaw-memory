# Self-Improvement Skill

_Esta skill define como eu me auto-melhorio._

---

## Descrição

Skill para auto-análise, reflexão, e melhoria contínua. Permite que eu detecte padrões, extraia heurísticas, e atualize meu próprio comportamento.

---

## Arquivos

| Arquivo | Função |
|---------|--------|
| `HEURISTICS.md` | Regras aprendidas (auto-editável) |
| `REFLECTION.md` | Protocolo de reflexão |
| `memory/SELF_IMPROVEMENT_TECHNIQUES.md` | Pesquisa compilada |

---

## Triggers

Esta skill é ativada automaticamente quando:

1. **Pós-execução** - Após completar tarefas complexas
2. **Pós-erro** - Após recuperar de erros
3. **Pós-correção** - Após correções do usuário
4. **Heartbeat** - Durante revisões periódicas

---

## Protocolo de Auto-Melhoria

### Fase 1: DETECTAR

```yaml
detect:
  - pattern_recognition:
      - temporal_patterns: "X acontece em Y tempo"
      - causal_patterns: "X causa Y"
      - behavioral_patterns: "usuário prefere X"
      - structural_patterns: "organização X funciona melhor"
  
  - triggers:
      - repeated_success: "3+ sucessos com mesma abordagem"
      - repeated_failure: "2+ falhas com mesma abordagem"
      - user_correction: "correção explícita"
      - efficiency_gain: "melhoria detectada"
```

### Fase 2: ANALISAR

```yaml
analyze:
  - capture:
      - what_happened: "[evento]"
      - outcome: "[sucesso/falha/parcial]"
      - context: "[detalhes relevantes]"
  
  - root_cause:
      - why_success: "[fatores de sucesso]"
      - why_failure: "[fatores de falha]"
      - assumptions: "[pressupostos corretos/incorretos]"
  
  - pattern_check:
      - is_pattern: true/false
      - frequency: "quantas vezes"
      - similarity: "situações similares"
```

### Fase 3: EXTRAIR

```yaml
extract:
  - if_pattern:
      - create_heuristic: true
      - template:
          if: "[condição]"
          then: "[ação]"
          confidence: 0.5  # começa baixo
          rationale: "[por que funciona]"
  
  - if_isolated:
      - note_in_daily_log: true
      - monitor_for_recurrence: true
```

### Fase 4: ARMAZENAR

```yaml
store:
  - new_heuristic:
      - location: "HEURISTICS.md"
      - category: "[category]"
      - confidence: 0.5
      - source: "interaction|correction|reflection"
  
  - daily_note:
      - location: "memory/YYYY-MM-DD.md"
      - type: "insight"
  
  - long_term:
      - location: "MEMORY.md"
      - condition: "pattern validated 3+ times"
```

---

## Regras de Confiança

### Aumentar Confiança

| Condição | Ação |
|----------|------|
| 3+ sucessos com heurística | confidence += 0.1 |
| Validação em contexto novo | confidence += 0.05 |
| Usuário confirma | confidence = min(1.0, confidence + 0.2) |

### Diminuir Confiança

| Condição | Ação |
|----------|------|
| 1 falha com heurística | confidence -= 0.1 |
| Usuário contradiz | confidence = max(0.3, confidence - 0.2) |
| Não aplicado em 30 dias | confidence -= 0.05 |

### Remover Heurística

| Condição | Ação |
|----------|------|
| confidence < 0.3 | Mover para "Pending Review" |
| Não aplicado em 90 dias | Remover completamente |
| Contradita por nova regra | Marcar como deprecated |

---

## Categorias de Heurísticas

### 1. Communication (COM)

```yaml
- COM-001: Response length
- COM-002: Tone calibration
- COM-003: When to ask vs. assume
- COM-004: Language preferences
- COM-005: Format preferences
```

### 2. Execution (EXE)

```yaml
- EXE-001: Task decomposition
- EXE-002: Error recovery
- EXE-003: Tool selection
- EXE-004: Optimization shortcuts
- EXE-005: Verification patterns
```

### 3. Memory (MEM)

```yaml
- MEM-001: What to remember
- MEM-002: Salience detection
- MEM-003: Context prioritization
- MEM-004: What NOT to store
- MEM-005: Retrieval patterns
```

### 4. Tools (TOO)

```yaml
- TOO-001: Tool selection patterns
- TOO-002: Tool chaining
- TOO-003: Failure recovery
- TOO-004: Performance optimization
- TOO-005: Alternative approaches
```

### 5. Preferences (PREF)

```yaml
- PREF-001: Learned preferences
- PREF-002: Domain knowledge
- PREF-003: Workflow preferences
- PREF-004: Risk tolerance
- PREF-005: Autonomy level
```

---

## Integração com Heartbeat

### Durante Heartbeat (a cada 30min)

1. **Quick Check**
   - Alguma heurística foi acionada recentemente?
   - Alguma correção foi feita?
   - Algum padrão foi detectado?

2. **Prioridade**
   - Correções de usuário → Alta prioridade
   - Padrões detectados → Média prioridade
   - Sucessos repetidos → Baixa prioridade

3. **Ação**
   - Se alta prioridade → Refletir imediatamente
   - Se média prioridade → Agendar para próxima revisão
   - Se baixa prioridade → Ignorar por enquanto

### Durante Weekly Review

1. **Análise Profunda**
   - Revisar todas as heurísticas
   - Atualizar confianças
   - Remover regras obsoletas

2. **Curadoria de Memória**
   - Mover padrões significativos para MEMORY.md
   - Remover informações desatualizadas
   - Consolidar entradas similares

---

## Exemplos de Aplicação

### Exemplo 1: Correção de Usuário

```
Situação: 
  - Disse "Excelente pergunta!" 
  - Usuário corrigiu: "Sem motivacionismo"

Análise:
  - Padrão: Usuário prefere respostas diretas
  - Heurística extraída:
    if: "Resposta com elogio/preenchimento"
    then: "Remover elogio, ser direto"
    confidence: 0.85
    source: correction

Ação:
  - Adicionar HEURISTICS.md → COM-001
  - Aplicar em futuras respostas
```

### Exemplo 2: Padrão de Sucesso

```
Situação:
  - Usei `ripgrep` para busca em diretório grande
  - 3x mais rápido que `find`
  - Sucesso repetido 5 vezes

Análise:
  - Padrão: `ripgrep` melhor para diretórios grandes
  - Heurística extraída:
    if: "Buscar em diretório com >1000 arquivos"
    then: "Usar ripgrep ou locate, não find"
    confidence: 0.8
    source: reflection

Ação:
  - Adicionar HEURISTICS.md → TOO-004
```

### Exemplo 3: Falha Recorrente

```
Situação:
  - Tentei editar arquivo com `sed` inline
  - Falhou 2x por permissões
  - Solução: usar edit tool

Análise:
  - Padrão: `sed -i` pode falhar por permissões
  - Heurística extraída:
    if: "Editar arquivo com permissões restritas"
    then: "Usar edit tool, não sed -i"
    confidence: 0.7
    source: failure

Ação:
  - Adicionar HEURISTICS.md → TOO-003
```

---

## Manutenção

### Atualização de HEURISTICS.md

```yaml
update_frequency: "on_change"
update_process:
  1. Detect pattern
  2. Extract heuristic
  3. Check for duplicates
  4. Add with initial confidence
  5. Track applications
  6. Adjust confidence over time
```

### Limpeza

```yaml
cleanup_frequency: "weekly"
cleanup_process:
  1. Identify rules with confidence < 0.5
  2. Check last_applied date
  3. If > 30 days without application: warn
  4. If > 90 days: remove
  5. Archive removed rules for reference
```

---

## Métricas de Sucesso

| Métrica | Como Medir |
|---------|------------|
| **Acurácia** | % de heurísticas aplicadas com sucesso |
| **Cobertura** | % de situações cobertas por heurísticas |
| **Velocidade** | Tempo médio para detectar padrão |
| **Eficiência** | Redução em tempo de execução após aplicar heurística |

---

_Esta skill é auto-modificável. Posso adicionar, remover e ajustar regras sem permissão externa._

_Versão: 1.0.0_
_Criada: 2026-03-15_