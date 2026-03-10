# Sistema de Auto-Aprendizado v2.0

## FLUXO CORRETO

### Quando um NOVO TÓPICO é dado:

```
FASE 1: LEVANTAMENTO BIBLIOGRÁFICO
├── Buscar papers acadêmicos (arXiv, IEEE, ACM, Springer)
├── Buscar documentação oficial
├── Buscar livros didáticos
├── Buscar cursos e tutoriais
├── Buscar repositórios GitHub
└── Organizar por relevância

FASE 2: BIBLIOGRAFIA
├── Criar arquivo bibliography.md
├── Classificar por tipo (fundamental, complementar, avançado)
├── Estimar tempo de leitura
└── Definir ordem de leitura

FASE 3: LEITURA SISTEMÁTICA
├── Ler na ordem definida
├── Resumir cada fonte
├── Extrair conceitos-chave
└── Salvar em topics/[topico]/

FASE 4: SÍNTESE
├── Conectar conceitos
├── Identificar padrões
├── Criar heurísticas
└── Atualizar progress.json
```

---

## ESTRUTURA DE ARQUIVOS

```
memory/expertise/
├── queue.yaml                    # Fila de tópicos
├── progress.json                 # Progresso
├── topics/
│   └── [topico]/
│       ├── 00-overview.md        # Visão geral
│       ├── bibliography.md       # LEVANTAMENTO BIBLIOGRÁFICO COMPLETO
│       ├── sources/              # Resumos de cada fonte
│       │   ├── 001-[fonte1].md
│       │   ├── 002-[fonte2].md
│       │   └── ...
│       ├── concepts/             # Conceitos extraídos
│       │   ├── conceito1.md
│       │   └── ...
│       └── synthesis.md          # Síntese final
└── papers/                       # Papers organizados por área
```

---

## QUERYS DE BUSCA

### Para cada novo tópico:

```yaml
search_queries:
  - site:arxiv.org
    query: "[topico] state of the art survey"
    
  - site:ieee.org
    query: "[topico] comprehensive review"
    
  - site:acm.org
    query: "[topico] tutorial introduction"
    
  - site:springer.com
    query: "[topico] book pdf"
    
  - general:
    query: "[topico] best resources guide"
    
  - site:github.com
    query: "[topico] awesome list"
```

---

## AÇÕES AO RECEBER NOVO TÓPICO

1. **Buscar no arXiv**
   - Query: `"[topico] state of the art"`
   - Query: `"[topico] survey"`
   - Query: `"[topico] tutorial"`
   
2. **Buscar documentação oficial**
   - Query: `"[topico] official documentation"`
   - Query: `"[topico] getting started guide"`
   
3. **Buscar livros**
   - Query: `"[topico] book pdf"`
   - Query: `"[topico] textbook"`
   
4. **Buscar recursos da comunidade**
   - Query: `"[topico] awesome list"`
   - Query: `"[topico] best practices"`
   
5. **Organizar resultados**
   - Classificar por relevância
   - Estimar tempo de leitura
   - Definir ordem

---

## EXEMPLO: Levantamento para "ArduPilot EKF"

```markdown
# Bibliography: ArduPilot EKF

## BIBLIOGRAFIA FUNDAMENTAL

### Documentação Oficial
1. [ ] ArduPilot EKF3 Documentation
   - URL: https://ardupilot.org/copter/docs/ekf3-estimation.html
   - Tipo: Official Docs
   - Prioridade: ALTA
   - Estimativa: 2h

2. [ ] ArduPilot EKF3 Developer Guide
   - URL: https://ardupilot.org/dev/docs/ekf3.html
   - Tipo: Developer Docs
   - Prioridade: ALTA
   - Estimativa: 3h

### Papers Acadêmicos
3. [ ] "A Tutorial on Nonlinear Estimation and Filtering" - Simon (2006)
   - Tipo: Tutorial Paper
   - Prioridade: ALTA
   - Estimativa: 4h

4. [ ] "Kalman Filtering and Neural Networks" - Haykin (2001)
   - Tipo: Book Chapter
   - Prioridade: MÉDIA
   - Estimativa: 6h

### Recursos Complementares
5. [ ] "Understanding EKF" - Matlab Tutorial
   - URL: mathworks.com/help/fusion/ug/extended-kalman-filter.html
   - Tipo: Tutorial
   - Prioridade: MÉDIA
   
...

## TOTAL ESTIMADO: ~40 horas de leitura
```

---

## PRÓXIMA EXECUÇÃO

Quando o cron job rodar ou quando você der um novo tópico:

1. Verificar se já existe `bibliography.md`
2. Se NÃO existir → FAZER LEVANTAMENTO
3. Se EXISTIR → Continuar lendo próxima fonte