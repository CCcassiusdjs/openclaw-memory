# Árvore Genealógica Acadêmica COMPLETA: Turing 1936

## Visão Geral

Este documento traça a genealogia **exaustiva** do paper de Turing (1936), desde as raízes antigas (Aristóteles, ~350 a.C.) até os desenvolvimentos modernos (P vs NP, verificação formal). Inclui:

- **~80 figuras históricas** com contribuições específicas
- **7 linhagens principais** convergentes
- **Desenvolvimentos pós-Turing** (complexidade, tipos dependentes)
- **Cronologia completa** de 2600+ anos

---

## A Convergência em Turing (1936)

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                           CONVERGÊNCIA EM TURING (1936)                          ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                  ║
║   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      ║
║   │   CHURCH     │   │    GÖDEL     │   │    POST      │   │   KLEENE     │      ║
║   │   (Abr 1936) │   │   (1931)     │   │   (Out 1936) │   │   (1936)     │      ║
║   │ Lambda Cálc. │   │Incompletude  │   │Sist. Normais │   │Recursividade│      ║
║   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘      ║
║          │                  │                  │                  │              ║
║          └──────────────────┴──────────────────┴──────────────────┘              ║
║                                     │                                           ║
║                                     ▼                                           ║
║                           ┌─────────────────┐                                    ║
║                           │     TURING      │                                    ║
║                           │   (Mai 1936)    │                                    ║
║                           │ Máq. Universais│                                    ║
║                           │ Entschiedungs-  │                                    ║
║                           │ problem insolúvel                                   ║
║                           └────────┬────────┘                                    ║
║                                    │                                             ║
╚════════════════════════════════════╪════════════════════════════════════════════╝
                                     │
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
┌───────▼───────┐           ┌────────▼────────┐           ┌───────▼───────┐
│ENTSCHEIDUNGS- │           │   HILBERT'S     │           │  PRINCIPIA    │
│   PROBLEM     │           │    PROGRAM     │           │  MATHEMATICA  │
│Hilbert-Ack.   │           │    (1920s)      │           │  (1910-1913)  │
│   (1928)      │           └────────┬────────┘           └───────┬───────┘
└───────────────┘                    │                            │
                                     │                            │
                                     ▼                            ▼
                        ┌────────────────────────┐    ┌────────────────────┐
                        │      HILBERT (1900)    │    │ TEORIA DOS TIPOS   │
                        │   23 Problemas (Paris) │    │ Evitar paradoxos   │
                        └────────────┬───────────┘    └──────────┬─────────┘
                                     │                           │
                                     ▼                           ▼
                        ┌────────────────────────┐    ┌────────────────────┐
                        │   FUNDAMENTOS DA       │    │   PARADOXO DE      │
                        │   MATEMÁTICA           │    │   RUSSELL (1902)   │
                        │   (Crise 1890-1930)    │    └──────────┬─────────┘
                        └────────────┬───────────┘               │
                                     │                           │
                                     ▼                           ▼
                        ┌────────────────────────┐    ┌────────────────────┐
                        │   CANTOR (1874)        │    │   FREGE (1879-1903)│
                        │   Teoria dos Conjuntos │    │   Logicismo        │
                        └────────────┬───────────┘    └──────────┬─────────┘
                                     │                           │
                                     ▼                           ▼
                        ┌─────────────────────────────────────────────────────┐
                        │            TRADIÇÃO LÓGICA                          │
                        │   Aristóteles → Estoicos → Escolástica → Leibniz    │
                        │   → Boole → De Morgan → Peirce → Schröder → Frege   │
                        └─────────────────────────────────────────────────────┘
```

---

## LINHAGEM 0: Raízes Antigas (350 a.C. - 1600 d.C.)

### Aristóteles e a Primeira Lógica Formal

```
ARISTÓTELES (~350 a.C.)
    │
    │ Obra: Organon (≈ "instrumento")
    │
    │ ├── Categorias
    │ ├── Sobre a Interpretação
    │ ├── Analíticos Anteriores (silogística)
    │ ├── Analíticos Posteriores
    │ ├── Tópicos
    │ └── Refutações Sofísticas
    │
    │ **Contribuições:**
    │ • Primeira lógica formal sistemática
    │ • Teoria do silogismo
    │ • Distinção entre dedução e indução
    │ • Noção de variável (letras para termos)
    │ • Identificação de figuras e modos válidos
    │
    │ **Legado:**
    │ • Dominou lógica por 2000+ anos
    │ • Base para toda tradição posterior
    │ • A única lógica "oficial" até o séc. XIX
    │
    ▼
ESCOLA MEGÁRICA (~400-250 a.C.)
    │
    │ Figuras: Euclides de Megara, Estilpo, Diodoro Cronos
    │
    │ **Contribuições:**
    │ • Lógica proposicional (vs. silogística aristotélica)
    │ • Paradoxos (o mentiroso, o monte)
    │ • Modalidade ("o possível" vs "o necessário")
    │ • Argumento dominador de Diodoro
    │
    │ **Importância:**
    │ • Precursores da lógica estoica
    │ • Precursores da lógica modal moderna
    │
    ▼
ESTOICOS (~300 a.C. - 200 d.C.)
    │
    │ Figuras principais:
    │ ├── ZENO DE CÍTIO (~300 a.C.) — Fundador
    │ ├── CLEANTES (~260 a.C.) — Sucessor
    │ └── CRISIPO DE SOLI (~240 a.C.) — O Grande Sistemático
    │
    │ CRISIPO (~240 a.C.)
    │ │
    │ │ Obras: >700 (fragmentos sobreviventes)
    │ │
    │ │ **Contribuições FUNDAMENTAIS:**
    │ │
    │ │ 1. LÓGICA PROPOSICIONAL
    │ │    • Primeira lógica proposicional completa
    │ │    • Conectivos: "se...então", "e", "ou", "não"
    │ │    • Definições truth-functional (!!)
    │ │    • Modos: "Se o primeiro, então o segundo"
    │ │
    │ │ 2. DEDUÇÃO NATURAL
    │ │    • Regras de inferência
    │ │    • Argumentos válidos vs inválidos
    │ │    • "Um silogismo é válido se a conclusão
    │ │       segue necessariamente das premissas"
    │ │
    │ │ 3. SINTAXE E SEMÂNTICA
    │ │    • Distinção entre significante (lekton)
    │ │      e significado
    │ │    • Precursores de teoria de significação
    │ │
    │ │ 4. PARADOXOS
    │ │    • O Mentiroso (versão estoica)
    │ │    • O Monte (sorites)
    │ │    • Análise de vaguidade
    │ │
    │ │ **Importância:**
    │ │ • "Crisipo foi o maior lógico da antiguidade"
    │ │   (Stanford Encyclopedia of Philosophy)
    │ │ • Dominou por 400 anos
    │ │ • Redescoberto no séc. XX como
    │ │   "antecipação do cálculo proposicional"
    │ │
    ▼
NEOPLATÔNICOS (200-600 d.C.)
    │
    │ Porfírio, Amônio, Boécio
    │
    │ **Contribuição:**
    │ • Preservaram lógica aristotélica
    │ • Isagoge de Porfírio (comentário sobre Categorias)
    │ • Traduções de Boécio para latim
    │ • Transmissão para a Idade Média
    │
    ▼
ESCOLÁSTICA (1100-1500 d.C.)
    │
    │ Figuras principais:
    │ ├── PEDRO ABELARDO (1079-1142)
    │ │   Sic et Non — método dialético
    │ │
    │ ├── PEDRO HISPANO (séc. XIII)
    │ │   Summulae Logicales — texto padrão por séculos
    │ │
    │ ├── TOMÁS DE AQUINO (1225-1274)
    │ │   Comentários sobre Aristóteles
    │ │   Integração com teologia
    │ │
    │ ├── DUNS SCOTUS (~1266-1308)
    │ │   Lógica modal
    │ │   Teoria da individuação
    │ │
    │ └── GUILHERME DE OCKHAM (~1287-1347)
    │     Summa Logicae
    │     • Navalha de Ockham ("entia non sunt
    │       multiplicanda praeter necessitatem")
    │     • Nominalismo
    │     • Lógica de termos avançada
    │
    │ **Contribuições:**
    │ • Desenvolvimento sofisticado de silogística
    │ • Teoria da suposição (semântica)
    │ • Lógica modal e temporal
    │ • Análise de paradoxos (obrigações)
    │ • Precursores de lógica deôntica
    │
    │ **Declínio:**
    │ • Renascimento rejeita "escolasticismo"
    │ • Humanismo prefere retórica
    │ • Lógica estagnou por ~300 anos
    │
    ▼
DESCARTES (1596-1650)
    │
    │ Regulae, Discurso do Método (1637)
    │
    │ **Crítica à lógica escolástica:**
    │ • "A lógica é mais um instrumento de falar
    │   do que de pensar"
    │ • Prefere matemática como modelo
    │
    │ **Contribuição indireta:**
    │ • Método analítico
    │ • Ênfase em clareza e distinção
    │ • Inspirou Leibniz (correspondência)
    │
    ▼
LEIBNIZ (1646-1716) ← PONTO DE VIRADA
    │
    │ VIDE LINHAGEM 1
    │
```

### Cronologia Antiga

| Período | Autor | Obra | Contribuição |
|---------|-------|------|--------------|
| ~350 a.C. | Aristóteles | Organon | Primeira lógica formal (silogística) |
| ~400 a.C. | Megáricos | — | Lógica proposicional, paradoxos |
| ~280 a.C. | Crisipo | ~700 obras | Lógica proposicional sistemática |
| 200-600 | Neoplatônicos | Comentários | Preservação, transmissão |
| ~1200 | Pedro Hispano | Summulae Logicales | Texto padrão medieval |
| ~1300 | Ockham | Summa Logicae | Lógica de termos, navalha |
| 1637 | Descartes | Discurso do Método | Crítica à lógica escolástica |
| 1666 | Leibniz | Dissertatio | **Início da lógica moderna** |

---

## LINHAGEM 1: Tradição Lógica Moderna (Leibniz → Hilbert)

```
LEIBNIZ (1646-1716)
    │
    │ Obras Principais:
    │ ├── Dissertatio de Arte Combinatoria (1666)
    │ ├── Characteristica Universalis (não publicado)
    │ ├── Calculus Ratiocinator (não publicado)
    │ └── Nouveaux Essais (1765, póstumo)
    │
    │ **VISÃO FUNDACIONAL:**
    │
    │ 1. CHARACTERISTICA UNIVERSALIS
    │    • Linguagem universal para representar todo conhecimento
    │    • Símbolos para conceitos primitivos
    │    • Combinação de símbolos = combinação de conceitos
    │    • "Como caracteres chineses, mas com significado"
    │
    │ 2. CALCULUS RATIOCINATOR
    │    • Cálculo mecânico do raciocínio
    │    • Regras formais para manipular símbolos
    │    • Sem ambiguidade, sem interpretação
    │    • "Como cálculo, não argumento"
    │
    │ 3. "CALCULEMUS!"
    │    > "Se houver controvérsia, podemos dizer:
    │    > 'Calculemos!' para ver quem está certo."
    │
    │ **Contribuições Técnicas:**
    │ • Sistema binário (0 e 1)
    │ • Antecipação de AND, OR, NOT lógicos
    │ • Interseção, união, complemento
    │ • Álgebra de classes (precursora de Boole)
    │
    │ **Legado:**
    │ • Visionário — antecipou computação em 300 anos
    │ • Stephen Wolfram: "O primeiro pensador
    │   moderno sobre computação"
    │ • Base conceitual para toda a tradição
    │
    ▼
BOOLE (1815-1864)
    │
    │ Obras:
    │ ├── The Mathematical Analysis of Logic (1847)
    │ └── An Investigation of the Laws of Thought (1854)
    │
    │ **Contribuições:**
    │
    │ 1. ÁLGEBRA DA LÓGICA
    │    • Variáveis = classes (extensão)
    │    • Operações: × (interseção), + (união), − (complemento)
    │    • 1 = universo, 0 = vazio
    │    • Leis algébricas para lógica
    │
    │ 2. LÓGICA PROPOSICIONAL COMO ÁLGEBRA
    │    • Proposições como classes
    │    • x = "verdadeiro", 0 = "falso"
    │    • x(1−x) = 0 (princípio de não-contradição)
    │
    │ 3. MÉTODO DE BOOLE
    │    • Reduzir problemas lógicos a equações
    │    • Resolver equações algebricamente
    │    • Interpretar solução
    │
    │ **Limitações:**
    │ • Não distingue classes de proposições
    │ • Não tem quantificadores
    │ • Sistema inconsistente (x + y pode ser
    │   interpretado de formas diferentes)
    │
    │ **Legado:**
    │ • Primeira álgebra lógica bem-sucedida
    │ • Base para Boole-De Morgan-Schröder
    │ • "Pai da lógica algébrica"
    │
    ▼
    ├─► DE MORGAN (1806-1871)
    │       │
    │       │ Obras:
    │       │ ├── Formal Logic (1847)
    │       │ └── Syllabus of Logic (1860)
    │       │
    │       │ **Contribuições:**
    │       │ • Leis de De Morgan (dualidade)
    │       │   ¬(A ∨ B) = ¬A ∧ ¬B
    │       │   ¬(A ∧ B) = ¬A ∨ ¬B
    │       │ • Lógica de relações
    │       │   "A é pai de B"
    │       │   "O pai de um pai é avô"
    │       │   Precursores de lógica de predicados
    │       │ • Quantificação de relativos
    │       │
    │       │ **Legado:**
    │       │ • Estendeu álgebra booleana
    │       │ • Preparou terreno para Peirce
    │       │
    │       ▼
    │   PEIRCE (1839-1914)
    │       │
    │       │ Obras: >12.000 páginas publicadas
    │       │ Papéis principais: "On the Algebra of Logic" (1880, 1885)
    │       │
    │       │ **Contribuições FUNDAMENTAIS:**
    │       │
    │       │ 1. LÓGICA DE RELAÇÕES
    │       │    • Extensão completa de De Morgan
    │       │    • Álgebra de relações binárias
    │       │    • Composição, inversão, fecho transitivo
    │       │
    │       │ 2. QUANTIFICADORES (∏, ∑)
    │       │    • ∏x = "para todo x" (produto lógico)
    │       │    • ∑x = "existe x" (soma lógica)
    │       │    • Primeira notação sistemática
    │       │    • (Frege independentemente)
    │       │
    │       │ 3. INFERÊNCIA LÓGICA
    │       │    • Regras de dedução natural
    │       │    • Diagramas existenciais
    │       │    • Abdução, dedução, indução
    │       │
    │       │ 4. TEORIA DOS TIPOS IMPLÍCITA
    │       │    • Distinção entre níveis
    │       │    • Prevenção de paradoxos
    │       │
    │       │ **Controvérsia Peirce vs Frege:**
    │       │ • Peirce desenvolveu quantificadores (1880-1885)
    │       │ • Frege desenvolveu independentemente (1879)
    │       │ • Peirce: notação mais intuitiva (∏, ∑)
    │       │ • Frege: notação mais rigorosa (2D)
    │       │ • Peirce influenciou Schröder, Peano
    │       │ • Frege influenciou Russell, Wittgenstein
    │       │
    │       │ **Legado:**
    │       │ • "Um dos maiores lógicos"
    │       │ • Infelizmente negligenciado
    │       │   (publicação fragmentada)
    │       │
    │       ▼
    │   SCHRÖDER (1841-1902)
    │       │
    │       │ Obra: Vorlesungen über die Algebra der Logik (1890-1905)
    │       │ Três volumes monumentais
    │       │
    │       │ **Contribuições:**
    │       │
    │       │ 1. SISTEMATIZAÇÃO
    │       │    • Áreas: lógica de classes, proposições, relações
    │       │    • Notação unificada
    │       │    • Provas rigorosas
    │       │
    │       │ 2. ÁLGEBRA DE RELAÇÕES
    │       │    • Extensão completa de Peirce
    │       │    • Teoremas de equivalência
    │       │    • "Álgebra relativa"
    │       │
    │       │ 3. INFLUÊNCIA
    │       │    • Referência padrão por décadas
    │       │    • Hilbert estudou Schröder
    │       │    • Löwenheim baseou-se em Schröder
    │       │    • Tarski: "A álgebra de relações
    │       │      de Peirce e Schröder"
    │       │
    │       │ **Limite de Löwenheim-Skolem:**
    │       │ • Löwenheim (1915) usou sistema de Schröder
    │       │ • Skolem (1920) refinou
    │       │ • Teorema fundamental de model theory
    │       │
    │       │ **Legado:**
    │       │ • "O último grande álgebra-logista"
    │       │ • Superado por Frege/Russell
    │       │ • Renascido em álgebra relacional
    │       │
    │       ▼
    │   FREGE (1848-1925)
    │       │
    │       │ Obras:
    │       │ ├── Begriffsschrift (1879)
    │       │ ├── Die Grundlagen der Arithmetik (1884)
    │       │ └── Grundgesetze der Arithmetik (1893/1903)
    │       │
    │       │ **Contribuições FUNDAMENTAIS:**
    │       │
    │       │ 1. BEGRIFFSSCHRIFT (1879)
    │       │    "Ideografia" ou "Escrita de Conceitos"
    │       │
    │       │    • Primeira lógica de predicados de
    │       │      alta ordem completa
    │       │    • Notação bidimensional (árvores)
    │       │    • Quantificadores modernos
    │       │    • "Se...então" como condicional
    │       │    • Variáveis ligadas e livres
    │       │
    │       │    Exemplo de notação Frege:
    │       │    ┌───┐
    │       │    │ ∀x (P(x) → Q(x))
    │       │    └───┘
    │       │    (na verdade uma árvore gráfica 2D)
    │       │
    │       │ 2. GRUNDLAGEN (1884)
    │       │    "Os Fundamentos da Aritmética"
    │       │
    │       │    • Crítica de Kant, Mill, etc.
    │       │    • Definição de número via extensão de conceito
    │       │    • "O número de F é a extensão do conceito:
    │       │       'igual a F'"
    │       │    • Logicismo: números são objetos lógicos
    │       │
    │       │ 3. GRUNDGESETZE (1893/1903)
    │       │    "Leis Fundamentais da Aritmética"
    │       │
    │       │    • Formalização completa do logicismo
    │       │    • Derivação da aritmética da lógica
    │       │    • Lei Básica V (extensão de conceitos)
    │       │    • Volume II recebido em 1902...
    │       │
    │       │ **DESVASTAÇÃO (1902):**
    │       │
    │       │ Carta de Russell para Frege (16/06/1902):
    │       │
    │       │ > "Caro colega,
    │       │ > 
    │       │ > Encontro-me em total acordo com você
    │       │ > quanto ao conteúdo... Mas encontro
    │       │ > uma dificuldade no seu sistema...
    │       │ > 
    │       │ > Seja W o predicado 'ser um predicado
    │       │ > que não pode ser predicado de si mesmo'.
    │       │ > Pode W ser predicado de si mesmo?
    │       │ > Se sim, então não; se não, então sim."
    │       │ >
    │       │ > — Bertrand Russell
    │       │
    │       │ Resposta de Frege (22/06/1902):
    │       │
    │       │ > "Seu descobrimento da contradição causou-me
    │       │ > surpresa e, receio, grande consternação.
    │       │ > 
    │       │ > Deve ser possível encontrar uma solução...
    │       │ > Mas a confiança na ciência é abalada."
    │       │
    │       │ **O PARADOXO DE RUSSELL:**
    │       │
    │       │ Lei Básica V de Frege implica:
    │       │
    │       │ {x : x ∉ x} ∈ {x : x ∉ x}
    │       │                     ⇕
    │       │ {x : x ∉ x} ∉ {x : x ∉ x}
    │       │
    │       │ CONTRADIÇÃO.
    │       │
    │       │ **Impacto:**
    │       │ • O sistema de Frege é INCONSISTENTE
    │       │ • Logicismo clássico falhou
    │       │ • Início da "crise dos fundamentos"
    │       │
    │       │ **Legado:**
    │       │ • "O maior lógico desde Aristóteles"
    │       │   (Quine)
    │       │ • Apesar do paradoxo, seu sistema
    │       │   de lógica de predicados estava correto
    │       │ • Base para Russell, Hilbert, Gödel
    │       │
    │       ▼
    │   RUSSELL (1872-1970)
    │       │
    │       │ Obra principal: Principia Mathematica (1910-1913)
    │       │ Com Alfred North Whitehead
    │       │
    │       │ **ANTECEDENTES:**
    │       │
    │       │ 1. Paradoxo de Russell (1901-1902)
    │       │    • Descoberto lendo Grundgesetze
    │       │    • "O conjunto de todos os conjuntos que
    │       │      não contêm a si mesmos"
    │       │    • Variante do paradoxo do barbeiro
    │       │    • Derruba sistema de Frege
    │       │
    │       │ 2. Principles of Mathematics (1903)
    │       │    • Tentativa inicial de resolver paradoxos
    │       │    • Não conseguiu — teoria de tipos
    │       │      ainda não estava clara
    │       │
    │       │ **PRINCIPIA MATHEMATICA (1910-1913):**
    │       │
    │       │ • 3 volumes
    │       │ • ~2000 páginas
    │       │ • "O trabalho mais monumental da lógica"
    │       │
    │       │ **Solução: TEORIA DOS TIPOS**
    │       │
    │       │ Níveis (tipos):
    │       │
    │       │ Tipo 0: indivíduos (a, b, c)
    │       │ Tipo 1: classes de indivíduos ({a}, {b})
    │       │ Tipo 2: classes de classes ({{a}})
    │       │ ...
    │       │
    │       │ Regra: Uma classe só pode conter
    │       │        elementos de tipos inferiores.
    │       │
    │       │ Resultado: x ∈ x é SEMPRE FALSO ou
    │       │           SEMPRE VERDADEIRO, nunca
    │       │           pode levar a contradição.
    │       │
    │       │ **Objetivo:**
    │       │ Derivar toda matemática da lógica:
    │       │ • Definir número natural
    │       │ • Definir adição, multiplicação
    │       │ • Provar propriedades
    │       │ • Tudo a partir de axiomas lógicos
    │       │
    │       │ **Axiomas:**
    │       │ 1. Proposições elementares
    │       │ 2. Teoria da quantificação
    │       │ 3. Axioma da redutibilidade
    │       │ 4. Axioma do infinito
    │       │ 5. Axioma da multiplicação
    │       │
    │       │ **Problemas:**
    │       │ • Axioma da redutibilidade é AD HOC
    │       │ • Axioma do infinito não é lógico
    │       │ • Não é realmente "derivado da lógica"
    │       │
    │       │ **Legado:**
    │       │ • Base para Hilbert
    │       │ • Influenciou Gödel
    │       │ • "O último grande logicista"
    │       │
    │       ▼
    │   HILBERT (1862-1943)
            │
            │ VIDE LINHAGEM 5
            │
```

---

## LINHAGEM 2: Tradição Conjuntista (Cantor → Zermelo → Gödel)

```
CANTOR (1845-1918)
    │
    │ Obras principais:
    │ ├── "Über eine Eigenschaft des Inbegriffes aller
    │ │   reellen algebraischen Zahlen" (1874)
    │ ├── "Über unendliche lineare Punktmannigfaltigkeiten" (1879-1884)
    │ └── "Beiträge zur Begründung der transfiniten Mengenlehre" (1895-1897)
    │
    │ **CONTRIBUIÇÕES FUNDAMENTAIS:**
    │
    │ 1. TEORIA DOS CONJUNTOS
    │    • Conjuntos infinitos como objetos matemáticos
    │    • "Um conjunto é uma coleção de objetos
    │       determinados e distintos"
    │    • Notação {x : P(x)}
    │
    │ 2. INFINITOS DE TAMANHOS DIFERENTES
    │    
    │    Teorema: ℝ não é enumerável (1874)
    │    
    │    Prova: Diagonalização de Cantor
    │    
    │    |ℕ| = |ℤ| = |ℚ| = ℵ₀ (enumeráveis)
    │    |ℝ| = 2^ℵ₀ = c (contínuo)
    │    ℵ₀ < c
    │
    │ 3. TEOREMA DE CANTOR
    │    
    │    Para todo conjunto A: |P(A)| > |A|
    │    
    │    Resultado: Existem INFINITOS tamanhos de infinito
    │    
    │    ℵ₀ < 2^ℵ₀ < 2^(2^ℵ₀) < ...
    │
    │ 4. HIPÓTESE DO CONTÍNUO (1878)
    │    
    │    Não existe cardinal entre ℵ₀ e c?
    │    
    │    Hipótese: CH é verdadeira
    │    
    │    (Provado independente de ZFC em 1963)
    │
    │ 5. NÚMEROS TRANSFINITOS
    │    
    │    ω = primeiro ordinal transfinito
    │    ω+1, ω+2, ..., ω·2, ω², ω^ω, ...
    │    
    │    Aritmética transfinita
    │
    │ **PARADOXOS (descobertos por Cantor):**
    │
    │ • Paradoxo de Cantor:
    │   |P(U)| > |U|, mas P(U) ⊆ U
    │   → Contradição se existe "conjunto universal"
    │
    │ • Paradoxo de Burali-Forti (1897):
    │   Conjunto de todos os ordinais
    │   → Não pode ser um ordinal
    │
    │ • Estes paradoxos mostraram que
    │   a teoria ingênua de conjuntos é inconsistente
    │
    │ **Legado:**
    │ • Criou a base para toda matemática moderna
    │ • "O Cantor do infinito"
    │ • Problemas de fundamentação motivaram
    │   axiomatização (Zermelo)
    │
    ▼
    ├─► DEDEKIND (1831-1916)
    │       │
    │       │ Obras:
    │       │ ├── Was sind und was sollen die Zahlen? (1888)
    │       │ └── Stetigkeit und irrationale Zahlen (1872)
    │       │
    │       │ **Contribuições:**
    │       │
    │       │ 1. DEFINIÇÃO DE INFINITO
    │       │    
    │       │    Um conjunto S é infinito se existe
    │       │    bijeção entre S e um subconjunto próprio de S
    │       │    
    │       │    S infinito ⇔ ∃f: S → S injetiva e não sobrejetiva
    │       │
    │       │ 2. CORTE DE DEDEKIND
    │       │    
    │       │    Definição de ℝ como cortes:
    │       │    (A, B) onde A < B e A ∪ B = ℚ
    │       │    
    │       │    Cada real = um corte
    │       │    ℝ = conjunto de todos os cortes
    │       │
    │       │ 3. DEFINIÇÃO DE NATURAIS
    │       │    
    │       │    Via "cadeias" (Ketten):
    │       │    • 1 ∈ N
    │       │    • Se n ∈ N, então φ(n) ∈ N
    │       │    • Indução transfinita
    │       │    
    │       │    Precursores de recursão primitiva
    │       │
    │       │ **Legado:**
    │       │ • Influência em Peano
    │       │ • Base para construção de ℝ
    │       │ • Precursores de Skolem, Gödel
    │       │
    │       ▼
    │   PEANO (1858-1932)
    │       │
    │       │ Obra: Arithmetices Principia, Nova Methodo Exposita (1889)
    │       │
    │       │ **AXIOMAS DE PEANO:**
    │       │
    │       │ 1. 0 ∈ ℕ
    │       │ 2. n ∈ ℕ → S(n) ∈ ℕ
    │       │ 3. S(n) = S(m) → n = m
    │       │ 4. ∀n ∈ ℕ: S(n) ≠ 0
    │       │ 5. (P(0) ∧ ∀n(P(n)→P(S(n)))) → ∀n P(n)
    │       │    (Indução)
    │       │
    │       │ **Contribuições:**
    │       │ • Axiomatização clara de ℕ
    │       │ • Notação simbólica moderna
    │       │   (∈, ⊂, ∪, ∩, etc.)
    │       │ • Formulário matemático (projeto de
    │       │   enciclopédia de símbolos)
    │       │
    │       │ **Legado:**
    │       │ • Influência em Russell/Hilbert
    │       │ • Base para sistemas formais
    │       │
    │       ▼
    │   ZERMELO (1871-1953)
    │       │
    │       │ Obra: "Untersuchungen über die Grundlagen der Mengenlehre I" (1908)
    │       │
    │       │ **CONTEXTO:**
    │       │ • Paradoxo de Russell (1902)
    │       │ • Paradoxos de Cantor/Burali-Forti
    │       │ • Crise dos fundamentos
    │       │ • Precisa-se de axiomatização
    │       │
    │       │ **AXIOMAS DE ZERMELO (1908):**
    │       │
    │       │ I.   Axioma da Extensão
    │       │      ∀A∀B(∀x(x∈A↔x∈B)→A=B)
    │       │
    │       │ II.  Axioma da Separacão
    │       │      ∀A∀P∃B(B={x∈A : P(x)})
    │       │      (Evita paradoxos — subconjunto de A)
    │       │
    │       │ III. Axioma do Par
    │       │      ∀x∀y∃A(x∈A∧y∈A)
    │       │
    │       │ IV.  Axioma da União
    │       │      ∀A∃B(B={x : ∃y(y∈A∧x∈y)})
    │       │
    │       │ V.   Axioma do Infinito
    │       │      ∃A(∅∈A∧∀x(x∈A→x∪{x}∈A))
    │       │
    │       │ VI.  Axioma da Potência
    │       │      ∀A∃B(B=P(A))
    │       │
    │       │ VII. Axioma da Escolha
    │       │      ∀F(∀A∈F(A≠∅)→∃f(A∈F→f(A)∈A))
    │       │      (Controverso!)
    │       │
    │       │ **Importância:**
    │       │ • Primeira axiomatização consistente
    │       │ • Restringe "compreensão irrestrita"
    │       │ • Base para ZFC
    │       │
    │       │ **Controvérsia do Axioma da Escolha:**
    │       │ • Zermelo provou que todo conjunto pode
    │       │   ser bem ordenado (1904)
    │       │ • Usou AC implicitamente
    │       │ • Crítica intensa (Borel, Baire, Lebesgue)
    │       │ • "Este axioma tem algo de teológico"
    │       │
    │       │ **Legado:**
    │       │ • Z → ZF → ZFC
    │       │ • Base para matemática moderna
    │       │
    │       ▼
    │   FRAENKEL (1891-1965)
    │       │
    │       │ Contribuições (1922):
    │       │
    │       │ VIII. Axioma de Substituição
    │       │      ∀A∀F(F é função →
    │       │        ∃B(B={F(x) : x∈A}))
    │       │
    │       │ • Permite construir conjuntos grandes
    │       │   (ordinais, V_α)
    │       │ • Necessário para teoria de modelos
    │       │
    │       │ **Resultado:** ZF (Zermelo-Fraenkel)
    │       │
    │       ▼
    │   VON NEUMANN (1903-1957)
            │
            │ Contribuições (1925, 1928):
            │
            │ 1. TEORIA DE CONJUNTOS COM CLASSES
            │    
            │    • Conjuntos vs Classes próprias
            │    • Classes: coleções "grandes demais"
            │    • V (universo) é classe própria
            │    
            │ 2. ORDINAIS COMO CONJUNTOS
            │    
            │    Ordinal = conjunto transitivo bem-ordenado
            │    ∅ = 0
            │    {0} = 1
            │    {0, 1} = 2
            │    ...
            │    
            │    ω = {0, 1, 2, ...}
            │    ω+1 = ω ∪ {ω}
            │    ...
            │    
            │ 3. HIERARQUIA CUMULATIVA
            │    
            │    V₀ = ∅
            │    V_{α+1} = P(V_α)
            │    V_λ = ⋃_{α<λ} V_α (para λ limite)
            │    
            │    V = ⋃_{α ∈ Ord} V_α
            │    
            │    Todo conjunto está em algum V_α
            │
            │ 4. AXIOMA DA REGULARIDADE
            │    
            │    ∀x(x≠∅ → ∃y∈x(y∩x=∅))
            │    
            │    Resultado: Não há ∈-ciclos
            │    x ∉ x
            │    ¬∃y₀,y₁,...(y₀∈y₁∧y₁∈y₂∧...)
            │
            │ **Legado:**
            │ • NBG (von Neumann-Bernays-Gödel)
            │ • Hierarquia V_α padrão
            │ • Ordinais como conjuntos
            │ • Fundamentação
            │
            ▼
        SKOLEM (1887-1963)
            │
            │ Obras principais:
            │ ├── "Logisch-kombinatorische Untersuchungen" (1920)
            │ └── "Some remarks on axiomatized set theory" (1922-23)
            │
            │ **CONTRIBUIÇÕES:**
            │
            │ 1. FORMA NORMAL DE SKOLEM (1920)
            │    
            │    Toda fórmula de primeira ordem pode ser
            │    reduzida a forma:
            │    
            │    ∀x₁...∀xₙ∃y₁...∃yₘ F(x₁,...,yₘ)
            │    
            │    (prenex, skolemização)
            │    
            │    • Importância para decidibilidade
            │    • Base para resolução automática
            │
            │ 2. PARADOXO DE SKOLEM (1922)
            │    
            │    Teorema de Löwenheim-Skolem:
            │    "Se uma fórmula de primeira ordem tem
            │     modelo, tem modelo enumerável"
            │    
            │    Paradoxo: ZFC tem modelos enumeráveis?!
            │    Mas ZFC prova que existem não-enumeráveis!
            │    
            │    Resolução: Enumerabilidade é relativa
            │    ao metalinguagem, não absoluta.
            │
            │ 3. ARITMÉTICA RECURSIVA PRIMITIVA (1923)
            │    
            │    Precursores de funções recursivas:
            │    • Definição por recursão
            │    • Link entre recursão e computabilidade
            │    • Influência em Gödel
            │
            │ **Legado:**
            │ • Skolemização fundamental para SAT
            │ • Paradoxo → teoria de modelos
            │ • Recursão → Gödel → Kleene
            │
            ▼
        GÖDEL (1906-1978)
            │
            │ Obras principais:
            │ ├── "Über formal unentscheidbare Sätze..." (1931)
            │ ├── Consistency of AC and CH (1938-1940)
            │ └── Princeton lectures (1934)
            │
            │ VIDE LINHAGEM 6 PARA DETALHES
            │
```

---

## LINHAGEM 3: Tradição Intuitionista (Brouwer → Weyl → Heyting)

```
KRÖNECKER (1823-1891)
    │
    │ Matemático alemão, aluno de Dirichlet
    │
    │ **Posição:**
    │ • "Die ganzen Zahlen hat der liebe Gott gemacht,
    │   alles andere ist Menschenwerk"
    │   (Os números inteiros foram feitos por Deus,
    │    todo o resto é obra humana)
    │
    │ • Rejeição de infinito atual
    │ • Apenas construções explícitas são válidas
    │ • Crítica de teoria de Cantor
    │ • "Não existem números irracionais, apenas
    │   extensões de campos"
    │
    │ **Legado:**
    │ • Precursores do construtivismo
    │ • Influência em Brouwer
    │
    ▼
POINCARÉ (1854-1912)
    │
    │ Matemático francês, "o último universalista"
    │
    │ **Posição:**
    │ • Ceticismo sobre lógica formal
    │ • "A lógica é estéril; a intuição é criativa"
    │ • Crítica do logicismo
    │ • Pragmatismo matemático
    │
    │ **Controvérsia com Russell/Hilbert:**
    │ • Rejeita axioma de escolha
    │ • "Definições não-predicativas são circulares"
    │ • Influência em Brouwer
    │
    │ **Importância:**
    │ • Crítica respeitada do formalismo
    │ • "A intuição do espaço não é lógica"
    │
    ▼
BROUWER (1881-1966)
    │
    │ Obras:
    │ ├── Over de Grondslagen der Wiskunde (tese, 1907)
    │ ├── "Intuitionism and Formalism" (1912)
    │ └── Artigos sobre continuidade (1918-1928)
    │
    │ **INTUITIONISMO:**
    │
    │ 1. MATEMÁTICA = CONSTRUÇÃO MENTAL
    │    
    │    "Matemática é uma construção livre do
    │     intelecto humano"
    │    
    │    • Não existe "realidade matemática" externa
    │    • Teoremas são relatos de construções
    │    • Provas devem ser construtivas
    │
    │ 2. REJEIÇÃO DO TERCEIRO EXCLUÍDO
    │    
    │    A ∨ ¬A não é universalmente válido!
    │    
    │    Exemplo: "Todo real é racional ou irracional"
    │    
    │    Mas: não podemos CONSTRUIR a resposta!
    │    Então: A ∨ ¬A não é válido para infinitos
    │
    │ 3. REJEIÇÃO DO INFINITO ATUAL
    │    
    │    • Apenas infinito potencial (ω como processo)
    │    • Não existe "o conjunto de todos os naturais"
    │    • Conjuntos são apenas construções em progressão
    │
    │ 4. SEQUÊNCIAS DE ESCOLHA
    │    
    │    Sequência: α₁, α₂, α₃, ...
    │    
    │    Cada termo é escolhido livremente
    │    A sequência nunca é "completa"
    │    O continuum é criado dinamicamente
    │
    │ **CONTROVÉRSIA COM HILBERT:**
    │
    │ Hilbert (1922):
    │ > "Tirar o tertium non datur do matemático
    │ >  é como proibir o boxeador de usar os punhos"
    │
    │ Brouwer (1923):
    │ > "A lógica clássica é derivada de casos finitos
    │ >  e erroneamente estendida ao infinito"
    │
    │ **Legado:**
    │ • Base para lógica intuitionista (Heyting)
    │ • Influência em teoria dos tipos (Martin-Löf)
    │ • Computação: Curry-Howard
    │
    ▼
WEYL (1885-1955)
    │
    │ Obras:
    │ ├── Das Kontinuum (1918)
    │ └── "Über die neue Grundlagenkrise der Mathematik" (1921)
    │
    │ **Posição:**
    │ • Aluno de Hilbert
    │ • Convertido ao intuitionismo (temp.)
    │ • "A análise como ensinada está errada"
    │
    │ **Das Kontinuum (1918):**
    │ • Análise predicativa
    │ • Rejeita definições impredicativas
    │ • Reconstrução da análise
    │
    │ **Nova Crise (1921):**
    │ • Defesa pública do intuitionismo
    │ • "O programa de Hilbert falhou"
    │ • Crítica da prova de consistência
    │
    │ **Resposta de Hilbert (1922):**
    │ • Palestras em Hamburgo
    │ • "Neubegründung der Mathematik"
    │ • Formulação do programa formalista
    │
    │ **Legado:**
    │ • Catalisou debate
    │ • Depois voltou ao formalismo
    │ • Contribuições à física (grupos)
    │
    ▼
HEYTING (1898-1980)
    │
    │ Obra: "Die formalen Regeln der intuitionistischen Logik" (1930)
    │
    │ **LÓGICA INTUITIONISTA:**
    │
    │ Sem lei do terceiro excluído:
    │
    │ │ Axiomas:
    │ │   A → (B → A)
    │ │   (A → B) → ((A → (B → C)) → (A → C))
    │ │   A → (A ∨ B)
    │ │   B → (A ∨ B)
    │ │   (A → C) → ((B → C) → ((A ∨ B) → C))
    │ │   (A ∧ B) → A
    │ │   (A ∧ B) → B
    │ │   A → (B → (A ∧ B))
    │ │   (A → B) → ((A → ¬B) → ¬A)
    │ │   ¬A → (A → B)
    │ │
    │ │ NÃO inclui: A ∨ ¬A
    │
    │ **Semântica de Heyting (1930s):**
    │ • Álgebras de Heyting
    │ • Topos como modelos
    │ • Semântica de Kripke (1965)
    │
    │ **Legado:**
    │ • Lógica intuitionista formalizada
    │ • Base para teoria dos tipos dependente
    │ • Conexão com computação (Curry-Howard)
    │
    ▼
MARTIN-LÖF (1942-)
    │
    │ Obra: Intuitionistic Type Theory (1972, 1984)
    │
    │ **TEORIA DOS TIPOS INTUITIONISTA:**
    │
    │ • Tipos como proposições
    │ • Termos como provas
    │ • Computação = verificação de provas
    │
    │ **Isomorfismo de Curry-Howard-Martin-Löf:**
    │
    │ | Lógica            | Tipos          |
    │ |-------------------|----------------|
    │ | Proposição        | Tipo           |
    │ | Prova             | Termo          |
    │ | A → B             | A → B (função) |
    │ | A ∧ B             | A × B (par)    |
    │ | A ∨ B             | A + B (soma)   |
    │ | ∀x.P(x)           | Πx:A.P(x)      |
    │ | ∃x.P(x)           | Σx:A.P(x)      |
    │
    │ **Legado:**
    │ • Base para Coq, Agda, Lean
    │ • Verificação formal moderna
    │ • Homotopy Type Theory
```

---

## LINHAGEM 4: Desenvolvimentos em Lógica (Löwenheim → Tarski → Gentzen)

```
LÖWENHEIM (1878-1957)
    │
    │ Obra: "Über Möglichkeiten im Relativkalkül" (1915)
    │
    │ **TEOREMA DE LÖWENHEIM (1915):**
    │
    │ "Se uma fórmula de primeira ordem é satisfatível,
    │  então é satisfatível em um domínio enumerável"
    │
    │ **Importância:**
    │ • Primeiro teorema de model theory
    │ • Base para Skolem
    │ • Precursores de Gödel (completude)
    │
    │ **Problema:**
    │ • Usou König's Lemma implicitamente
    │ • Prova não completamente rigorosa
    │
    ▼
SKOLEM (1887-1963)
    │
    │ (Já coberto na LINHAGEM 2)
    │
    │ **Refinamento de Löwenheim:**
    │ • Teorema Löwenheim-Skolem (1920)
    │ • Skolem normal form
    │ • Funções de Skolem
    │
    ▼
GÖDEL (1906-1978) — COMPLETUDE (1929)
    │
    │ Tese de doutorado (1929)
    │
    │ **TEOREMA DA COMPLETUDE (1929):**
    │
    │ "Toda fórmula válida de primeira ordem é demonstrável"
    │
    │ Ou: Se ⊨ F, então ⊢ F
    │
    │ **Prova:**
    │ • Constrói modelo a partir de demonstrações
    │ • Usa construção de Löwenheim-Skolem
    │ • Modelo de Henkin
    │
    │ **Importância:**
    │ • Lógica de primeira ordem é COMPLETA
    │ • Não há verdades indemonstráveis
    │ • Base para teoria de modelos
    │
    ▼
TARSKI (1901-1983)
    │
    │ Obras principais:
    │ ├── Pojęcie prawdy w językach nauk dedukcyjnych (1933)
    │ ├── "Der Wahrheitsbegriff" (1935, alemão)
    │ └── "The Concept of Truth in Formalized Languages" (1956, inglês)
    │
    │ **DEFINIÇÃO DE VERDADE (1933):**
    │
    │ Para cada linguagem L, definimos verdade em L
    │ em uma metalinguagem ML:
    │
    │ Sentença "A neve é branca" é verdadeira
    │ se e somente se a neve é branca.
    │
    │ (T-schema)
    │
    │ **Condições:**
    │ 1. Materialmente adequada
    │    (Captura o significado intuitivo)
    │ 2. Formalmente correta
    │    (Definição precisa na metalinguagem)
    │
    │ **Teorema da Indefinibilidade da Verdade:**
    │
    │ Em linguagens suficientemente expressivas,
    │ verdade não pode ser definida na própria linguagem.
    │
    │ (Relacionado ao paradoxo do mentiroso)
    │
    │ **CONSEQUÊNCIAS:**
    │ • Verdade = satisfação em modelo
    │ • Semântica de Tarski
    │ • Base para model theory
    │
    │ **TEORIA DE MODELOS:**
    │
    │ Desenvolvida por Tarski e alunos:
    │ • Eliminação de quantificadores
    │ • Modelos completos
    │ • Teorias decidíveis
    │ • Aplicações à álgebra
    │
    │ **Legado:**
    │ • Semântica moderna
    │ • Base para Kripke, etc.
    │
    ▼
GENTZEN (1909-1945)
    │
    │ Obras principais:
    │ ├── "Untersuchungen über das logische Schließen" (1934-1935)
    │ └── "Die Widerspruchsfreiheit der reinen Zahlentheorie" (1936)
    │
    │ **DEDUÇÃO NATURAL (1934):**
    │
    │ Sistema de inferência sem axiomas:
    │
    │ Introdução:
    │   A    B           A → B
    │   ────────         ───────  (→I)
    │    A ∧ B           [A] ⊢ B
    │
    │ Eliminação:
    │   A ∧ B           A → B    A
    │   ─────           ────────────
    │    A              B        (∧E)
    │
    │ **SEQUENT CALCULUS (LK, LJ) (1934-1935):**
    │
    │ Sequentes: Γ ⊢ Δ
    │
    │ Regras estruturais:
    │   Axioma:    A ⊢ A
    │   Corte:     Γ ⊢ A    A, Δ ⊢ B
    │              ─────────────────
    │                 Γ, Δ ⊢ B
    │
    │ Regras lógicas:
    │   (∧R):    Γ ⊢ A    Γ ⊢ B
    │            ─────────────
    │              Γ ⊢ A ∧ B
    │
    │ **HAUPTSATZ (Corte-Eliminação):**
    │
    │ "Todo sequente demonstrável tem demonstração
    │  sem corte (cut-free)"
    │
    │ **Consequências:**
    │ • Subfórmula property
    │ • Decidibilidade da lógica intuicionista
    │ • Consistência relativa
    │
    │ **PROVA DE CONSISTÊNCIA DA ARITMÉTICA (1936):**
    │
    │ Objetivo: Provar consistência de PA
    │
    │ Método: Indução transfinita até ε₀
    │
    │ Resultado: PA é consistente
    │
    │ (Mas: prova é não-finitária!)
    │
    │ **Legado:**
    │ • Dedução natural
    │ • Sequent calculus
    │ • Base para provadores automáticos
    │ • Curry-Howard-Lambek
```

---

## LINHAGEM 5: Programa de Hilbert e Crise (1900-1931)

```
HILBERT (1862-1943)
    │
    │ Obras principais:
    │ ├── 23 Problemas (Congresso Internacional, 1900)
    │ ├── "Neubegründung der Mathematik" (1922)
    │ └── Grundzüge der theoretischen Logik (com Ackermann, 1928)
    │
    │ **23 PROBLEMAS (1900):**
    │
    │ Congresso Internacional de Matemáticos, Paris
    │
    │ | #  | Problema                          | Status         |
    │ |----|-----------------------------------|----------------|
    │ | 1º | Hipótese do Contínuo              | Independente  |
    │ | 2º | Consistência da Aritmética       | Parcial       |
    │ | 3º | Equivalência de volumes          | Resolvido     |
    │ | 6º | Axiomatização da Física          | Parcial       |
    │ | 7º | Irracionais algébricos           | Resolvido     |
    │ | 8º | Hipótese de Riemann               | Aberto        |
    │ | 10º| Equações diofantinas             | Indecidível   |
    │ | ...| ...                               | ...           |
    │
    │ **Segundo Problema:**
    │ "Provar que os axiomas da aritmética são consistentes"
    │
    │ Este problema motivou todo o programa de Hilbert.
    │
    │ **PROGRAMA DE HILBERT (1920s):**
    │
    │ Contexto:
    │ • Paradoxo de Russell (1902)
    │ • Crise dos fundamentos
    │ • Intuitionismo de Brouwer
    │ • Weyl: "A matemática está errada"
    │
    │ Objetivo: SALVAR A MATEMÁTICA CLÁSSICA
    │
    │ Três pilares:
    │
    │ 1. FORMALIZAÇÃO
    │    • Toda matemática em linguagem formal
    │    • Sintaxe precisa, sem ambiguidade
    │    • Regras de inferência mecânicas
    │
    │ 2. COMPLETUDE
    │    • Toda verdade matemática é demonstrável
    │    • Sem lacunas no sistema
    │    • "Deus não joga dados com a matemática"
    │
    │ 3. CONSISTÊNCIA (por meios FINITÁRIOS)
    │    • Provar que os axiomas não levam a contradição
    │    • Usar apenas matemática "segura"
    │    • Métodos construtivos, finitos
    │
    │ 4. DECIDIBILIDADE (Entscheidungsproblem)
    │    • Existe algoritmo para decidir verdade?
    │    • "Todo problema matemático tem solução"
    │
    │ **LEMA FAMOSO:**
    │
    │ "Wir müssen wissen. Wir werden wissen."
    │ (Devemos saber. Saberemos.)
    │
    │ Discurso em Königsberg, 1930
    │
    │ (No mesmo dia, Gödel anunciou seu teorema...)
    │
    ▼
    ├─► HILBERT & ACKERMANN (1928)
    │       │
    │       │ Grundzüge der theoretischen Logik
    │       │
    │       │ **Contribuições:**
    │       │ • Primeira apresentação sistemática de
    │       │   lógica de primeira ordem
    │       │ • Distinção entre primeira e segunda ordem
    │       │ • Formulação explícita do ENTSCHEIDUNGSPROBLEM
    │       │
    │       │ **Entscheidungsproblem:**
    │       │
    │       │ "Existe um procedimento efetivo (algoritmo) que,
    │       │  dada uma fórmula de primeira ordem, determina
    │       │  se ela é universalmente válida?"
    │       │
    │       │ Formalmente:
    │       │ Dado φ, determinar se ⊨ φ
    │       │
    │       │ **Importância:**
    │       │ • Este é O PROBLEMA que Turing resolve em 1936
    │       │ • A resposta é NEGATIVA
    │       │ • Não existe tal algoritmo
    │       │
    │       ▼
    │   HILBERT & BERNAYS (1934-1939)
    │       │
    │       │ Grundlagen der Mathematik (2 volumes)
    │       │
    │       │ **Contribuições:**
    │       │ • Formalização completa do programa
    │       │ • Análise de consistência
    │       │ • Desenvolvimento de aritmética recursiva
    │       │
    │       │ (Já afetado por Gödel...)
    │       │
    │       ▼
    │   GÖDEL (1906-1978) — A CATÁSTROFE
            │
            │ Obra: "Über formal unentscheidbare Sätze der
            │       Principia Mathematica und verwandter Systeme I"
            │       (1931)
            │
            │ **CONTEXTO:**
            │ Hilbert (1928): "Vamos provar consistência!"
            │ Gödel (1931): "Não dá."
            │
            │ **TEOREMAS DA INCOMPLETUDE:**
            │
            │ PRIMEIRO TEOREMA:
            │
            │ "Qualquer sistema formal consistente F,
            │  suficientemente expressivo para aritmética,
            │  contém proposições verdadeiras mas indemonstráveis em F"
            │
            │ Formalmente:
            │ Se F é consistente, então existe G tal que:
            │ • F ⊬ G
            │ • F ⊬ ¬G
            │ • G é verdadeira (no modelo padrão)
            │
            │ SEGUNDO TEOREMA:
            │
            │ "Um sistema formal F não pode provar sua própria
            │  consistência dentro de F"
            │
            │ Formalmente:
            │ Se F é consistente, então F ⊬ Con(F)
            │
            │ **IDEIA DA PROVA:**
            │
            │ 1. ARITMETIZAÇÃO DA SINTAXE
            │    
            │    Gödel numbering:
            │    • Cada símbolo → número
            │    • Cada fórmula → número
            │    • Cada demonstração → número
            │    
            │    Exemplo:
            │    "0 = 0" → ⟨7, 5, 7⟩ → 2⁷·3⁵·5⁷ = n
            │
            │ 2. AUTO-REFERÊNCIA
            │    
            │    Construir sentença G que diz:
            │    "Eu não sou demonstrável"
            │    
            │    Similar ao paradoxo do mentiroso
            │    Mas: evita contradição via hierarquia
            │
            │ 3. DIAGONALIZAÇÃO
            │    
            │    Se G fosse demonstrável:
            │    • G diz "G não é demonstrável"
            │    • Se demonstrável, é verdadeira
            │    • Logo, não é demonstrável
            │    • Contradição!
            │    
            │    Se ¬G fosse demonstrável:
            │    • ¬G = "G é demonstrável"
            │    • Se demonstrável...
            │    • (análise mais complexa)
            │
            │ **IMPACTO:**
            │
            │ Hilbert ficou SURPRESO E DESAPONTADO.
            │
            │ O programa de Hilbert FALHOU:
            │ • Completude: FALSO (existem indecidíveis)
            │ • Consistência: IMPOSSÍVEL provar dentro do sistema
            │ • Decidibilidade: ABERTO (Gödel não resolveu)
            │
            │ MAS:
            │ Gödel NÃO resolveu o Entscheidungsproblem.
            │ Ele mostrou que ALGUMAS proposições são indecidíveis.
            │ Mas não mostrou que NÃO EXISTE algoritmo geral.
            │
            │ Isso foi feito por CHURCH e TURING em 1936.
            │
            │ **Legado:**
            │ • Fim do programa de Hilbert
            │ • Limites da prova formal
            │ • Base para computabilidade
            │ • Números de Gödel = aritmetização
            │
```

---

## LINHAGEM 6: Convergência em Turing (1931-1937)

```
GÖDEL (1931)
    │
    │ Teoremas da Incompletude
    │
    │ **Funções Recursivas Primitivas:**
    │
    │ Gödel usou funções recursivas primitivas
    │ para aritmetizar a sintaxe:
    │
    │ • zero(x) = 0
    │ • succ(x) = x + 1
    │ • proj_i(x₁,...,xₙ) = x_i
    │ • composição
    │ • recursão primitiva
    │
    │ Estas são CALCULÁVEIS.
    │
    │ **Mas:** Recursivas primitivas não são TODAS
    │ as calculáveis.
    │
    │ Exemplo: Função de Ackermann não é RP.
    │
    ▼
HERBRAND (1908-1931)
    │
    │ Tese (1930), carta para Gödel (1931)
    │
    │ **Funções Herbrand-Gödel (1930-1931):**
    │
    │ Esquema mais geral que recursão primitiva:
    │
    │ f(x) = y ↔ ∃z₁...zₘ[E(x, y, z₁,...,zₘ)]
    │
    │ onde E é uma equação system.
    │
    │ **Contribuição:**
    │ • Esquema geral de recursão
    │ • Influência em Gödel (1934 lectures)
    │ • Base para Kleene
    │
    │ **Tragédia:**
    │ Herbrand morreu em acidente de montanha
    │ em 1931, aos 23 anos.
    │
    ▼
GÖDEL (1934) — PRINCETON LECTURES
    │
    │ "On Undecidable Propositions"
    │
    │ Gödel apresentou definição de
    │ "funções recursivas gerais"
    │ baseadas no esquema de Herbrand.
    │
    │ **Definição:**
    │ Uma função é recursiva geral se pode ser
    │ definida por:
    │ • Zero, sucessor, projeções
    │ • Composição
    │ • Recursão primitiva
    │ • MINIMIZAÇÃO (μ-operador) ← NOVO!
    │
    │ μy.P(x, y) = "o menor y tal que P(x, y)"
    │
    │ **Importância:**
    │ Esta definição CAPTURA as funções computáveis.
    │
    │ (Kleene provou isso depois.)
    │
    ▼
    ├─► CHURCH (1903-1995)
    │       │
    │       │ Obras:
    │       │ ├── "A set of postulates for the foundation of logic" (1932-33)
    │       │ ├── "An Unsolvable Problem of Elementary Number Theory" (1936)
    │       │ └── "A Note on the Entscheidungsproblem" (1936)
    │       │
    │       │ **LAMBDA CÁLCULO (desenvolvido desde 1932):**
    │       │
    │       │ Sintaxe:
    │       │   x, y, z       (variáveis)
    │       │   (M N)         (aplicação)
    │       │   (λx.M)        (abstração)
    │       │
    │       │ Redução:
    │       │   (λx.M) N → M[N/x]
    │       │
    │       │ Exemplo:
    │       │   (λx.x) y → y   (identidade)
    │       │   (λx.(λy.x)) a b → a   (projeção)
    │       │
    │       │ **Funções λ-definíveis:**
    │       │
    │       │ Uma função f: ℕ → ℕ é λ-definível se
    │       │ existe termo F tal que:
    │       │   F n =ₗ f(n)   para todo n ∈ ℕ
    │       │
    │       │ (onde =ₗ é conversão lambda)
    │       │
    │       │ **TESE DE CHURCH (1934-1935):**
    │       │
    │       │ "Uma função é efetivamente calculável
    │       │  se e somente se é λ-definível"
    │       │
    │       │ Esta é uma TESE, não um teorema.
    │       │ Conecta o conceito INTUITIVO
    │       │ (calculável) com o FORMAL (λ-definível).
    │       │
    │       │ **ENTSCHEIDUNGSPROBLEM (1936):**
    │       │
    │       │ Church provou que o Entscheidungsproblem
    │       │ é INSOLÚVEL via lambda cálculo.
    │       │
    │       │ Método:
    │       │ 1. Mostrar que λ-conversão é indecidível
    │       │ 2. Reduzir λ-conversão a FOL
    │       │ 3. Concluir: FOL é indecidível
    │       │
    │       │ **Publicação:**
    │       │ "An Unsolvable Problem of Elementary Number Theory"
    │       │ (abril de 1936)
    │       │
    │       │ **Problema:**
    │       │ λ-definibilidade é ABSTRATA.
    │       │ Não é obviamente "mecânica".
    │       │ Alguns matemáticos ficaram céticos.
    │       │
    │       │ **Legado:**
    │       │ • Lambda cálculo = base de PL funcionais
    │       │ • Church-Rosser theorem
    │       │ • Tipos (simple types, 1940)
    │       │
    │       │
    │       ▼
    │   KLEENE (1909-1994)
    │       │
    │       │ Obras principais:
    │       │ ├── "λ-definability and recursiveness" (1936)
    │       │ ├── "General recursive functions of natural numbers" (1936)
    │       │ └── Introduction to Metamathematics (1952)
    │       │
    │       │ **Contribuições:**
    │       │
    │       │ 1. EQUIVALÊNCIA (1936)
    │       │    
    │       │    Kleene provou:
    │       │    λ-definível ⟺ recursivo geral ⟺ TM-computável
    │       │    
    │       │    Este é o TEOREMA DE EQUIVALÊNCIA
    │       │    que fundamenta a Tese de Church-Turing.
    │       │
    │       │ 2. NORMAL FORM THEOREM
    │       │    
    │       │    Toda função recursiva geral pode ser escrita:
    │       │    f(x) = U(μy.T(e, x, y))
    │       │    
    │       │    onde T é primitiva recursiva.
    │       │
    │       │ 3. RECURSÃO PARCIAL
    │       │    
    │       │    Funções parciais: podem não terminar
    │       │    Importante para computabilidade
    │       │
    │       │ 4. HIERARQUIA ARITMÉTICA
    │       │    
    │       │    Σ⁰ₙ, Π⁰ₙ, Δ⁰ₙ
    │       │    Classificação de complexidade
    │       │
    │       │ **Legado:**
    │       │ • Cunhou "Tese de Church" e "Tese de Turing"
    │       │ • Fundamentos rigorosos de computabilidade
    │       │ • Introdução a Metamatemática (texto clássico)
    │       │
    │       │
    │       ▼
    │   POST (1897-1954)
    │       │
    │       │ Obras:
    │       │ ├── "Introduction to a General Theory of Elementary Propositions" (1921)
    │       │ ├── "Finite Combinatory Processes" (1936)
    │       │ └── "Recursively Enumerable Sets" (1944)
    │       │
    │       │ **TRABALHO INDEPENDENTE:**
    │       │
    │       │ Post desenvolveu ideias de computabilidade
    │       │ desde 1920, mas não publicou.
    │       │
    │       │ Quando viu o paper de Turing (1936),
    │       │ escreveu seu próprio paper (outubro 1936).
    │       │
    │       │ **SISTEMAS CANÔNICOS/NORMAIS (1936):**
    │       │
    │       │ Regras de produção:
    │       │   P → Q
    │       │
    │       │ Sistema canônico:
    │       │   • Alfabeto finito
    │       │   • Axiomas
    │       │   • Regras de produção
    │       │   • Linguagem gerada = deriváveis
    │       │
    │       │ **Equivalência:**
    │       │ Sistemas canônicos = Máquinas de Turing
    │       │
    │       │ **PROBLEMA DE POST (1944):**
    │       │
    │       │ Dado um conjunto recursivamente enumerável S,
    │       │ S é recursivo?
    │       │
    │       │ (Relacionado ao problema da parada)
    │       │
    │       │ **GRAUS DE TURING:**
    │       │ Post desenvolveu teoria de graus
    │       │ (com Kleene)
    │       │
    │       │ **Legado:**
    │       │ • Predecessor independente
    │       │ • Sistemas de produção
    │       │ • Problema de Post
    │       │ • Graus de Turing
    │       │
    │       │
    │       ▼
    │   TURING (1912-1954)
            │
            │ Obra: "On Computable Numbers, with an Application
            │       to the Entscheidungsproblem" (1936-1937)
            │
            │ **CONTEXTO:**
            │
            │ • Gödel (1931): Incompletude
            │ • Church (abril 1936): Lambda cálculo
            │ • Turing (submetido maio 1936)
            │
            │ **MÁQUINAS DE TURING:**
            │
            │ Definição:
            │ Uma máquina de Turing é uma tupla M = (Q, Σ, Γ, δ, q₀, q_accept, q_reject)
            │
            │ • Q: estados finitos
            │ • Σ: alfabeto de entrada
            │ • Γ: alfabeto da fita (inclui branco)
            │ • δ: Q × Γ → Q × Γ × {L, R}
            │ • q₀: estado inicial
            │ • q_accept, q_reject: estados finais
            │
            │ Operação:
            │ 1. Começa em q₀ com entrada na fita
            │ 2. Lê símbolo sob a cabeça
            │ 3. Aplica δ(q, símbolo)
            │ 4. Escreve, move, muda estado
            │ 5. Repete até q_accept ou q_reject
            │
            │ **INTUIÇÃO:**
            │
            │ Turing argumentou que uma máquina de Turing
            │ captura "o que um humano calculador pode fazer":
            │
            │ 1. Memória finita (estados)
            │ 2. Papel infinito (fita)
            │ 3. Operações simples:
            │    • Ler símbolo
            │    • Escrever símbolo
            │    • Mover esquerda/direita
            │    • Mudar estado de mente
            │
            │ Este é o ARGUMENTO INTUITIVO
            │ para a Tese de Church-Turing.
            │
            │ **MÁQUINA UNIVERSAL:**
            │
            │ Existe U tal que:
            │ U(M, w) = M(w) para toda M e entrada w
            │
            │ U é um PROGRAMA ARMAZENADO!
            │
            │ **Importância:**
            │ • Primeira descrição de computador
            │   programável
            │ • Separação entre hardware e software
            │ • Base para arquitetura de von Neumann
            │
            │ **PROBLEMA DA PARADA:**
            │
            │ Teorema: Não existe TM que decide
            │ se uma TM arbitrária para.
            │
            │ Prova (diagonalização):
            │
            │ Suponha que H existe:
            │ H(M, w) = aceita se M(w) para
            │          = rejeita se M(w) não para
            │
            │ Defina D(M):
            │   Se H(M, M) aceita, D não para
            │   Se H(M, M) rejeita, D para
            │
            │ D(D) = ?
            │
            │ Se D(D) para, então H(D, D) aceita,
            │ então D(D) não para. Contradição!
            │
            │ Se D(D) não para, então H(D, D) rejeita,
            │ então D(D) para. Contradição!
            │
            │ Logo, H não pode existir.
            │
            │ **ENTSCHEIDUNGSPROBLEM:**
            │
            │ Redução do problema da parada para FOL:
            │
            │ Dada TM M e entrada w, construir fórmula φ
            │ tal que φ é satisfatível ↔ M(w) para.
            │
            │ Como problema da parada é indecidível,
            │ FOL satisfatibilidade é indecidível.
            │
            │ Logo: ENTSCHEIDUNGSPROBLEM É INSOLÚVEL.
            │
            │ **EQUIVALÊNCIA COM CHURCH:**
            │
            │ Turing (seção do paper) provou:
            │ TM-computável ⟺ λ-definível
            │
            │ Esta equivalência estabeleceu a
            │ TESE DE CHURCH-TURING.
            │
            │ **POR QUE TURING PREVALECEU:**
            │
            │ 1. INTUIÇÃO CLARA
            │    Máquinas são obviamente mecânicas.
            │    Lambda cálculo é abstrato.
            │
            │ 2. MÁQUINA UNIVERSAL
            │    Primeira descrição de computador armazenado.
            │
            │ 3. PROVA DIRETA
            │    Redução do problema da parada é simples.
            │
            │ 4. CONEXÃO COM FÍSICA
            │    "O que é calculável é o que uma máquina
            │     física pode fazer"
            │
            │ **Legado:**
            │ • Fundamentos da ciência da computação
            │ • Computabilidade
            │ • Complexidade (P vs NP deriva de TM)
            │ • Arquitetura de computadores
            │ • Inteligência artificial (teste de Turing)
```

---

## LINHAGEM 7: Desenvolvimentos Pós-Turing

```
TURING (1936-1954) — DESENVOLVIMENTOS POSTERIORES
    │
    │ 1936: On Computable Numbers
    │ 1937: Demonstração de equivalência com Church
    │ 1939: Sistemas lógicos com oráculos
    │      (Graus de Turing, redução relativa)
    │ 1950: Computing Machinery and Intelligence
    │      (Teste de Turing)
    │
    │ **MÁQUINAS DE TURING COM ORÁCULO:**
    │
    │ TM com acesso a oráculo O:
    │ Pode perguntar "x ∈ O?" em um passo
    │
    │ Graus de Turing:
    │ A ≡_T B se A é computável relativo a B
    │ e B é computável relativo a A
    │
    │ Hierarquia de graus:
    │ 0 < 0' < 0'' < ... < 0^(ω) < ...
    │
    │ **TESTE DE TURING (1950):**
    │
    │ "Uma máquina pode pensar?"
    │
    │ Teste: Juiz conversa com máquina e humano.
    │ Se juiz não distingue, máquina "pensa".
    │
    │ (Não é relevante para genealogia lógica,
    │  mas importante para IA)
    │
    ▼
CHURCH-TURING THESIS (1937)
    │
    │ Formulação de Kleene:
    │
    │ "As seguintes noções são equivalentes:
    │  1. λ-definível (Church)
    │  2. Recursivo geral (Gödel-Herbrand-Kleene)
    │  3. Turing-computável (Turing)
    │  4. Post-computável (Post)
    │
    │  E todas capturam a noção intuitiva de
    │  'efetivamente calculável'"
    │
    │ **Evidência:**
    │
    │ • Todos os formalismos convergem
    │ • Nenhuma função conhecida é calculável
    │   intuitivamente mas não-TM-computável
    │ • Argumento de Turing (intuição humana)
    │ • Convergência com física
    │
    │ **Formas:**
    │
    │ Tese (Church-Turing):
    │   Efetivamente calculável ⟺ TM-computável
    │
    │ Tese Forte (Church-Turing-Deutsch):
    │   Qualquer sistema físico pode ser simulado
    │   por uma TM (até quantum?)
    │
    │ Tese Polinomial (Cobham-Edmonds):
    │   Eficientemente calculável ⟺ P
    │
    ▼
DESENVOLVIMENTOS EM COMPUTABILIDADE (1940-1960)
    │
    │ POST (1944)
    │ │ "Recursively Enumerable Sets of Positive Integers"
    │ │
    │ │ • Problema de Post
    │ │ • Graus de insolubilidade
    │ │ • Conjuntos RE vs recursivos
    │ │
    │ ▼
    │ KLEENE & POST (1954)
    │ │
    │ │ • Graus de Turing intermediários
    │ │ • Hierarquia de graus
    │ │ • 0 < 0' < ... (infinitos graus)
    │ │
    │ ▼
    │ FRIEDBERG (1957) & MUCHNIK (1956)
    │ │
    │ │ Independentemente:
    │ │ Existem graus entre 0 e 0'
    │ │ (Conjuntos RE não-recursivos mas < problema da parada)
    │ │
    │ ▼
    │ SACKS (1960s)
    │ │
    │ │ Teoria dos graus de Turing
    │ │ Estrutura dos graus RE
    │ │
    ▼
DESENVOLVIMENTOS EM COMPLEXIDADE (1960s-present)
    │
    │ HARTMANIS & STEARNS (1965)
    │ │
    │ │ "On the Computational Complexity of Algorithms"
    │ │
    │ │ • Classes de complexidade
    │ │ • Hierarquia de tempo
    │ │ • Pioneiros da teoria da complexidade
    │ │
    │ ▼
    │ COOK (1971)
    │ │
    │ │ "The Complexity of Theorem-Proving Procedures"
    │ │
    │ │ • SAT é NP-completo
    │ │ • Definição de P e NP
    │ │ • Redução polinomial
    │ │
    │ │ **Teorema de Cook:**
    │ │ SAT ∈ P ⇔ P = NP
    │ │
    │ ▼
    │ LEVIN (1973, independente)
    │ │
    │ │ Na URSS, independentemente de Cook:
    │ │ • Problemas universais
    │ │ • NP-completude
    │ │
    │ ▼
    │ KARP (1972)
    │ │
    │ │ "Reducibility among Combinatorial Problems"
    │ │
    │ │ • 21 problemas NP-completos
    │ │ • Reduções polinomiais
    │ │ • Estabeleceu NP-completude como
    │ │   área central
    │ │
    │ ▼
    │ P VS NP (1971-present)
    │ │
    │ │ Um dos Millennium Problems
    │ │ Prêmio: $1.000.000
    │ │
    │ │ Até hoje: ABERTO
    │ │
    │ ▼
    │ DESENVOLVIMENTOS MODERNOS
    │ │
    │ │ • Criptografia (RSA, P vs NP)
    │ │ • Complexidade quântica (BQP)
    │ │ • Verificação formal (Coq, Lean)
    │ │ • Homotopy Type Theory
    │ │ • Teoria dos tipos dependentes
```

---

## Cronologia Completa (Séculos IV a.C. - XXI)

### Antiguidade (350 a.C. - 600 d.C.)

| Ano | Autor | Obra/Evento | Contribuição |
|-----|-------|-------------|--------------|
| ~350 a.C. | Aristóteles | Organon | Primeira lógica formal (silogística) |
| ~300 a.C. | Crisipo | ~700 obras | Lógica proposicional sistemática |
| ~250 a.C. | Megáricos | Fragmentos | Paradoxos, lógica modal |
| 200-600 | Neoplatônicos | Comentários | Preservação |

### Idade Média (1100-1500)

| Ano | Autor | Obra | Contribuição |
|-----|-------|------|--------------|
| ~1150 | Pedro Abelardo | Sic et Non | Método dialético |
| ~1250 | Pedro Hispano | Summulae Logicales | Texto padrão |
| ~1270 | Tomás de Aquino | Comentários | Integração teológica |
| ~1300 | Duns Scotus | Lógica modal | Teoria da individuação |
| ~1320 | Ockham | Summa Logicae | Navalha, lógica de termos |

### Renascimento e Início da Idade Moderna (1500-1700)

| Ano | Autor | Obra | Contribuição |
|-----|-------|------|--------------|
| 1637 | Descartes | Discurso do Método | Crítica à lógica escolástica |
| 1666 | Leibniz | Dissertatio | Início da lógica moderna |
| ~1670 | Leibniz | Characteristica (não pub.) | Linguagem universal |

### Século XIX (1800-1900)

| Ano | Autor | Obra | Contribuição |
|-----|-------|------|--------------|
| 1847 | Boole | Mathematical Analysis of Logic | Álgebra da lógica |
| 1847 | De Morgan | Formal Logic | Lógica de relações |
| 1874 | Cantor | "Über eine Eigenschaft..." | Teoria dos conjuntos |
| 1879 | Frege | Begriffsschrift | Lógica de predicados |
| 1884 | Frege | Grundlagen | Logicismo |
| 1888 | Dedekind | Was sind und was sollen die Zahlen | Definição de infinito |
| 1889 | Peano | Arithmetices Principia | Axiomas de Peano |
| 1890-05 | Schröder | Vorlesungen | Sistematização álgebra lógica |
| 1893/03 | Frege | Grundgesetze | Sistema lógico completo |

### Crise dos Fundamentos (1900-1930)

| Ano | Autor | Obra/Evento | Impacto |
|-----|-------|-------------|---------|
| 1900 | Hilbert | 23 Problemas | Agenda do séc. XX |
| 1902 | Russell | Carta para Frege | Paradoxo derruba sistema |
| 1907 | Brouwer | Tese | Intuitionismo |
| 1908 | Zermelo | Axiomatização de conjuntos | ZFC precursor |
| 1910-13 | Russell & Whitehead | Principia Mathematica | Formalização |
| 1912 | Brouwer | "Intuitionism and Formalism" | Debate público |
| 1915 | Löwenheim | Teorema | Model theory início |
| 1920 | Skolem | Forma normal | Refinamento Löwenheim |
| 1921 | Weyl | "Neue Grundlagenkrise" | Defesa intuitionismo |
| 1922 | Hilbert | "Neubegründung" | Resposta formalista |
| 1922 | Fraenkel | Axioma de substituição | ZF |
| 1925 | von Neumann | Teoria de conjuntos | Ordinais, classes |
| 1928 | Hilbert & Ackermann | Grundzüge | Entscheidungsproblem |
| 1930 | Heyting | Lógica intuitionista | Formalização |

### O Ano Milagroso e Consequências (1931-1950)

| Ano | Autor | Obra | Contribuição |
|-----|-------|------|--------------|
| 1931 | Gödel | Incompletude | Fim programa Hilbert |
| 1933 | Tarski | Definição de verdade | Semântica |
| 1934 | Gentzen | Dedução natural | Sistema de inferência |
| 1934 | Gödel | Princeton lectures | Recursão geral |
| 1936 (Abr) | Church | "Unsolvable Problem" | Lambda cálculo |
| 1936 (Mai) | Turing | "On Computable Numbers" | Máquinas de Turing |
| 1936 (Out) | Post | "Finite Combinatory" | Sistemas canônicos |
| 1936 | Kleene | Equivalência | Church-Turing-Kleene |
| 1937 | Church & Turing | Equivalência | Tese Church-Turing |
| 1938 | Gödel | L (construtível) | Consistência AC/CH |
| 1944 | Post | "RE Sets" | Problema de Post |
| 1950 | Turing | "Computing Machinery" | Teste de Turing |

### Desenvolvimentos Modernos (1950-presente)

| Ano | Autor | Contribuição |
|-----|-------|--------------|
| 1956 | Muchnik | Graus intermediários |
| 1957 | Friedberg | Graus intermediários |
| 1963 | Cohen | Forcing, independência CH |
| 1965 | Hartmanis & Stearns | Complexidade |
| 1971 | Cook | P vs NP, SAT NP-completo |
| 1972 | Karp | 21 problemas NP-completos |
| 1973 | Levin | NP-completude (URSS) |
| 1972-84 | Martin-Löf | Teoria dos tipos int. |
| 1980s | Tipos dependentes | Coq, Agda, Lean |

---

## Diagrama de Influência Final (Simplificado)

```
                    ╔════════════════════════════════════════════╗
                    ║          RAIZ: LEIBNIZ (~1670)             ║
                    ║     "Calculemus!" - Visão de cálculo       ║
                    ╚════════════════════════════════════════════╝
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
    ╔═════════════╗          ╔═════════════╗          ╔═════════════╗
    ║   LÓGICA    ║          ║ CONJUNTOS   ║          ║ARITMÉTICA   ║
    ║  Boole      ║          ║  Cantor     ║          ║ Dedekind   ║
    ║  De Morgan  ║          ║  Zermelo    ║          ║  Peano      ║
    ║  Peirce     ║          ║ Fraenkel    ║          ║  Skolem     ║
    ║  Schröder   ║          ║ von Neumann ║          ║  Gödel      ║
    ║  Frege      ║          ║  Gödel      ║          ║  Kleene     ║
    ╚═════╦═══════╝          ╚═════╦═══════╝          ╚═════╦═══════╝
          │                         │                         │
          │                         │                         │
          ▼                         ▼                         ▼
    ╔═════════════╗          ╔═════════════╗          ╔═════════════╗
    ║ PRINCIPIA   ║          ║   ZFC      ║          ║RECURSIVIDADE║
    ║ Russell     ║          ║ Axiomatiza- ║          ║ Herbrand    ║
    ║ Whitehead   ║          ║ ção         ║          ║ Gödel (1934)║
    ╚═════╦═══════╝          ╚═════╦═══════╝          ╚═════╦═══════╝
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                                    ▼
                    ╔════════════════════════════════════════════╗
                    ║     HILBERT'S PROGRAM (1920s)               ║
                    ║  Completude + Consistência + Decidibilidade ║
                    ╚════════════════════════════════════════════╝
                                    │
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ╔═════════════╗ ╔═════════════╗ ╔═════════════╗
            ║  Gödel      ║ ║   Church    ║ ║   Turing    ║
            ║  (1931)     ║ ║   (Abr 36)  ║ ║   (Mai 36)  ║
            ║Incompletude ║ ║ Lambda Cálc.║ ║ Máquinas    ║
            ╚═════╦═══════╝ ╚═════╦═══════╝ ╚═════╦═══════╝
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                    ╔════════════════════════════════════════════╗
                    ║     CHURCH-TURING THESIS (1937)             ║
                    ║   λ-definível ⟺ recursivo ⟺ TM-computável  ║
                    ╚════════════════════════════════════════════╝
                                  │
                                  ▼
                    ╔════════════════════════════════════════════╗
                    ║        COMPUTAÇÃO MODERNA                   ║
                    ║  Complexidade (P vs NP)                     ║
                    ║  Verificação formal (Coq, Lean)             ║
                    ║  Teoria dos tipos dependentes               ║
                    ║  Homotopy Type Theory                        ║
                    ╚════════════════════════════════════════════╝
```

---

## Conclusão

A genealogia acadêmica de Turing 1936 é uma **convergência de múltiplas tradições milenares**:

1. **Tradição Lógica:** Aristóteles → Estoicos → Escolásticos → Leibniz → Boole → Frege → Russell → Hilbert

2. **Tradição Conjuntista:** Cantor → Zermelo → Fraenkel → von Neumann → Gödel

3. **Tradição Aritmética:** Dedekind → Peano → Skolem → Gödel → Kleene

4. **Tradição Intuitionista:** Krönecker → Brouwer → Weyl → Heyting

5. **Tradição Computacional:** Leibniz → Boole → Church → Post → Turing

6. **Tradição Recursiva:** Herbrand → Gödel → Kleene

**O momento de convergência (1936)** foi único na história:
- Church (abril): Lambda cálculo
- Turing (maio): Máquinas de Turing
- Post (outubro): Sistemas canônicos
- Kleene: Equivalência provada

**O resultado — a Tese de Church-Turing** — estabeleceu que todas essas formalizações capturam a mesma noção: **computabilidade efetiva**.

E isso tudo começou com Leibniz querendo que disputas fossem resolvidas por cálculo. Turing provou que **existem disputas que nenhum cálculo pode resolver**.

---

_Gerado: 2026-03-09_
_Fontes: Stanford Encyclopedia of Philosophy, Internet Encyclopedia of Philosophy, Wikipedia, fontes primárias_
_Estrutura: 7 linhagens, ~80 figuras, cronologia 2600+ anos_