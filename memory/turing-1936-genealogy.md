# Árvore Genealógica Acadêmica Completa: Turing 1936

## O Paper Fundacional

**Alan Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem" (1936)**

Este paper é um dos mais importantes da história da computação. Nele, Turing:
1. Define formalmente o que é um "número computável"
2. Introduz a noção de "máquina de Turing"
3. Prova que o Entscheidungsproblem é insolúvel (independentemente de Church)
4. Constrói a Máquina Universal de Turing

---

## Árvore Genealógica Completa (Multi-Radicada)

A genealogia acadêmica de Turing 1936 **não é uma árvore simples** — é uma **rede multi-radicada** com múltiplas linhagens que convergem. Cada linhagem representa uma tradição intelectual distinta.

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                        CONVERGÊNCIA EM TURING (1936)                          ║
║                                                                                ║
║  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    ║
║  │   CHURCH     │   │    GÖDEL     │   │    POST      │   │   KLEENE     │    ║
║  │   (1936)     │   │   (1931)     │   │   (1936)     │   │   (1936)     │    ║
║  │ Lambda Cálc. │   │Incompletude │   │Sist. Normais │   │Recursividade │    ║
║  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘    ║
║         │                  │                  │                  │             ║
║         └──────────────────┴──────────────────┴──────────────────┘             ║
║                                      │                                        ║
║                                      ▼                                        ║
║                            ┌─────────────────┐                                ║
║                            │     TURING      │                                ║
║                            │     (1936)      │                                ║
║                            │ Máq. Universais │                                ║
║                            └────────┬────────┘                                ║
║                                     │                                         ║
╚═════════════════════════════════════╪═════════════════════════════════════════╝
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
            ┌───────▼───────┐                   ┌───────▼───────┐
            │  ENTSCHEIDUNG  │                   │ HILBERT'S     │
            │   PROBLEM      │                   │  PROGRAM      │
            │ Hilbert-Ack.   │                   │   (1920s)     │
            │   (1928)       │                   └───────┬───────┘
            └────────────────┘                           │
                                                         │
╔════════════════════════════════════════════════════════════════════════════════╗
║                              RAÍzes HISTÓRICAS                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## LINHAGEM 1: Tradição Lógica (Aristóteles → Boole → Frege)

```
ARISTÓTELES (~350 a.C.)
    │ Organon: silogística, primeira lógica formal
    │ "O silogismo é um discurso em que, dadas certas coisas,
    │  algo diferente delas resulta necessariamente"
    ▼
ESTOICOS (~300 a.C.)
    │ Crisipo: lógica proposicional
    │ Fragmentos perdidos, redescobertos no séc. XIX
    ▼
ESCOLÁSTICA (1100-1500)
    │ Tomás de Aquino, Duns Scotus, Guilherme de Ockham
    │ Desenvolvimento sofisticado da silogística
    │ Ockham: "Navalha de Ockham" — economia ontológica
    ▼
LEIBNIZ (1670s)
    │ Characteristica Universalis
    │ Calculus Ratiocinator
    │ "Calculemus!" — visão de raciocínio mecânico
    │ **RAIZ DE TODA A TRADIÇÃO**
    ▼
BOOLE (1847, 1854)
    │ The Mathematical Analysis of Logic
    │ An Investigation of the Laws of Thought
    │ **Álgebra da Lógica**: lógica como cálculo algébrico
    │ Variáveis: classes ou proposições
    │ Operações: × (interseção), + (união), − (complemento)
    ▼
    ├─► DE MORGAN (1847, 1860)
    │       Formal Logic: or, The Calculus of Inference
    │       Leis de De Morgan (dualidade)
    │       Lógica de relações (precursora de Peirce)
    │
    ├─► PEIRCE (1860s-1880s)
    │       Extensão da álgebra booleana
    │       Quantificadores existenciais e universais
    │       Lógica de relações de primeira ordem
    │
    └─► SCHRÖDER (1890-1905)
            Vorlesungen über die Algebra der Logik
            **Sistematização monumental** (3 volumes)
            Prepara o terreno para Hilbert
            Influência direta em Peano e Hilbert
            ▼
        FREGE (1879, 1884, 1893/1903)
        │   Begriffsschrift (1879)
        │   Die Grundlagen der Arithmetik (1884)
        │   Grundgesetze der Arithmetik (1893/1903)
        │
        │   **Contribuições fundamentais:**
        │   • Primeira lógica de predicados de alta ordem
        │   • Quantificadores modernos (∀, ∃)
        │   • Distinção sentido/referência
        │   • Logicismo: aritmética = lógica
        │
        │   **Problema:** Paradoxo de Russell derruba o sistema
        │
        └───► RUSSELL (1902)
              │ Carta para Frege: o paradoxo
              │ "O conjunto de todos os conjuntos que não contêm
              │  a si mesmos contém a si mesmo?"
              │
              └───► PRINCIPIA MATHEMATICA (1910-1913)
                    Russell & Whitehead
                    • 3 volumes, ~2000 páginas
                    • Teoria dos Tipos (evita paradoxos)
                    • Redução da matemática à lógica
                    • **Base para Hilbert**
```

---

## LINHAGEM 2: Tradição da Teoria dos Conjuntos (Cantor → Zermelo)

```
CANTOR (1874-1897)
    │ "Über eine Eigenschaft des Inbegriffes aller reellen
    │  algebraischen Zahlen" (1874)
    │
    │ **Fundamentos:**
    │ • Conjuntos infinitos como objetos matemáticos
    │ • Diferentes tamanhos de infinito
    │ • Teorema de Cantor: |P(X)| > |X|
    │ • Hipótese do Contínuo
    │ • Números transfinitos (ℵ₀, ℵ₁, ...)
    │
    │ **Problema:** Paradoxos surgem (Cantor, Russell, Burali-Forti)
    │
    ▼
    ├─► ZERMELO (1908)
    │       "Untersuchungen über die Grundlagen der Mengenlehre"
    │       **Primeira axiomatização da teoria dos conjuntos**
    │       • Axioma de Separacão (evita paradoxos)
    │       • Axioma da Escolha (controverso)
    │       • Conjuntos bem-fundados
    │
    │       **Reação:** Crítica de Poincaré, refinamentos
    │
    └─► DEDIKIND (1888)
            "Was sind und was sollen die Zahlen?"
            • Definição de infinito (bijecção com parte própria)
            • Caracterização dos números naturais
            • Influência em Peano
            ▼
        PEANO (1889)
            Arithmetices Principia, Nova Methodo Exposita
            • Axiomas de Peano para aritmética
            • Notação simbólica moderna (∈, ⊂, ...)
            • Influência em Russell/Hilbert
            ▼
        FRAENKEL (1922)
            Refinamentos aos axiomas de Zermelo
            • Axioma de Substituição
            • ZFC (Zermelo-Fraenkel + Choice)
            ▼
        VON NEUMANN (1925)
            • Funções como conjuntos
            • Ordinais como conjuntos
            • Cumulative hierarchy
            ▼
        GÖDEL (1938-1940)
            • Construtibilidade (L)
            • Consistência relativa de AC e CH
            ▼
        COHEN (1963)
            • Forcing
            • Independência de CH
```

---

## LINHAGEM 3: Tradição Aritmética/Recursiva (Dedekind → Peano → Skolem → Gödel)

```
DEDEKIND (1888)
    │ Was sind und was sollen die Zahlen?
    │ Definição de números naturais via indução
    │ "Cadeia" (Kette) — precursor de recursão
    ▼
PEANO (1889)
    │ Arithmetices Principia
    │ Axiomas de Peano
    │ Notação simbólica sistemática
    ▼
SKOLEM (1920, 1923)
    │ Forma normal de Skolem (redução lógica)
    │ Aritmética Recursiva Primitiva (precursora)
    │
    │ **Contribuição-chave:**
    │ • Funções recursivas primitivas
    │ • Link entre recursão e computabilidade
    │ • Precursor de Gödel (aritmetização)
    ▼
GÖDEL (1931)
    │ Teoremas da Incompletude
    │
    │ **Aritmetização da sintaxe:**
    │ • Números de Gödel
    │ • Funções recursivas primitivas
    │ • Decodificação de sintaxe em aritmética
    │
    │ **Conexão:** As funções usadas por Gödel
    │ são exatamente as funções recursivas primitivas
    │ de Skolem (generalizadas)
    ▼
KLEENE (1936)
    │ Funções recursivas gerais
    │ Equivalência com λ-definibilidade
    │ Normal Form Theorem
    │
    │ **Church-Kleene-Turing Theorem:**
    │ λ-definível ⟺ Turing-computável ⟺ recursivo geral
```

---

## LINHAGEM 4: Tradição Intuitionista (Krönecker → Brouwer → Weyl)

```
KRÖNECKER (1880s)
    │ "Die ganzen Zahlen hat der liebe Gott gemacht,
    │  alles andere ist Menschenwerk"
    │ Rejeição de infinito atual, construtivismo
    ▼
BROUWER (1907, 1912)
    │ Over de Grondslagen der Wiskunde (tese, 1907)
    │ Intuitionism and Formalism (1912)
    │
    │ **Princípios intuitionistas:**
    │ • Matemática = construção mental
    │ • Rejeição do tertium non datur (infinito)
    │ • Sequências de escolha (choice sequences)
    │ • Continuum intuitivo
    │
    │ **Conflito com Hilbert:**
    │ • Brouwer rejeita matemática clássica
    │ • Hilbert: "Tirar o tertium non datur
    │   do matemático é como proibir o boxeador
    │   de usar os punhos"
    ▼
WEYL (1918, 1921)
    │ Das Kontinuum (1918)
    │ "Über die neue Grundlagenkrise der Mathematik" (1921)
    │
    │ **Defesa pública do intuitionismo**
    │ "A análise como hoje ensinada está errada"
    │
    │ **Reação de Hilbert (1922):**
    │ "Neubegründung der Mathematik"
    │ → Programa de Hilbert formalizado
    ▼
HEYTING (1930)
    │ Lógica intuitionista formal
    │ Axiomas para lógica sem tertium non datur
    │
    │ **Legado:**
    │ • Lógica intuitionista (sem lei do meio excluído)
    │ • Semântica de Kripke (1965)
    │ • Teoria dos tipos intuitionista (Martin-Löf)
    │ • Computação: Curry-Howard, teoria dos tipos dependentes
```

---

## LINHAGEM 5: Programa de Hilbert (1900-1928)

```
HILBERT (1900)
    │ 23 Problemas — Congresso Internacional, Paris
    │
    │ **Problemas relevantes:**
    │ • 1º: Hipótese do Contínuo (resolvido: independente de ZFC)
    │ • 2º: Consistência dos axiomas da aritmética
    │ • 10º: Algoritmo para equações diofantinas (indecidível)
    │
    ▼
HILBERT's PROGRAM (1920s)
    │
    │ **Objetivos:**
    │ 1. Formalizar toda matemática
    │ 2. Provar consistência (por meios finitários)
    │ 3. Provar completude (toda verdade = demonstrável)
    │ 4. Decidibilidade (Entscheidungsproblem)
    │
    │ **Lema famoso:**
    │ "Wir müssen wissen. Wir werden wissen."
    │ (Devemos saber. Saberemos.)
    │
    ▼
    ├─► HILBERT & ACKERMANN (1928)
    │       Grundzüge der theoretischen Logik
    │       **Primeira apresentação sistemática de
    │        lógica de primeira ordem**
    │       Formulação explícita do ENTSCHEIDUNGSPROBLEM:
    │       "Existe algoritmo que decide se uma fórmula
    │        de primeira ordem é universalmente válida?"
    │
    └─► HILBERT & BERNAYS (1934-1939)
            Grundlagen der Mathematik
            Dois volumes
            Formalização completa do programa
            (Já afetado por Gödel)
```

---

## LINHAGEM 6: Desenvolvimentos Paralelos (1936)

**O ano milagroso da computabilidade:** 1936 viu **quatro** caracterizações independentes e equivalentes.

```
CHURCH (abril 1936)
    │ "An Unsolvable Problem of Elementary Number Theory"
    │
    │ **Contribuição:**
    │ • Lambda cálculo (desenvolvido desde 1932)
    │ • Funções λ-definíveis
    │ • Prova de que Entscheidungsproblem é insolúvel
    │   (via lambda cálculo)
    │
    │ **Problema:** Lambda cálculo é abstrato, não-obviamente
    │               "mecânico" no sentido intuitivo
    │
    │ **Tese de Church:** "efetivamente calculável = λ-definível"
    │
    ▼
GÖDEL (1934, Princeton lectures)
    │ Funções recursivas gerais
    │ (Baseado em Herbrand 1931, refinado por Kleene)
    │
    │ **Contribuição:**
    │ • Definição de funções recursivas gerais
    │ • Equivalência com λ-definíveis (provado por Kleene)
    │
    ▼
TURING (submetido maio 1936, publicado 1936-37)
    │ "On Computable Numbers..."
    │
    │ **Contribuição:**
    │ • Máquinas de Turing (modelo intuitivo, mecânico)
    │ • Máquina Universal de Turing
    │ • Prova de indecidibilidade do Entscheidungsproblem
    │ • Prova de equivalência com λ-definíveis
    │
    │ **Por que Turing prevaleceu:**
    │ • Definição claramente "mecânica"
    │ • Máquina universal (computador programável)
    │ • Intuitivamente "o que um humano pode calcular"
    │
    ▼
POST (outubro 1936)
    │ "Finite Combinatory Processes"
    │
    │ **Contribuição:**
    │ • Sistemas canônicos/ normais de Post
    │ • Modelo equivalente às máquinas de Turing
    │ • Desenvolvido independentemente (desde 1920s!)
    │
    │ **Nota:** Post chegou aos resultados antes de Turing
    │ mas não publicou. Seu trabalho de 1936 foi escrito
    │ após ver o paper de Turing.
    │
    ▼
KLEENE (1936)
    │ Funções recursivas gerais
    │
    │ **Contribuição:**
    │ • Equivalência: λ-definível ⟺ recursivo geral ⟺ TM
    │ • Teorema da Forma Normal
    │ • Cunhou "Tese de Church" e "Tese de Turing"
    │
    ▼
══════════════════════════════════════════════
CONVERGÊNCIA: CHURCH-TURING THESIS (1936-1937)
══════════════════════════════════════════════

"Toda função efetivamente calculável é computável por uma
 máquina de Turing (equivalentemente: λ-definível, recursiva)"

Esta é uma **tese** (hipótese), não um teorema:
• Não pode ser provada (conecta intuitivo e formal)
• Evidência empírica: todas as formalizações convergem
• Consequência: TM = limite absoluto da computação
```

---

## LINHAGEM 7: Pós-Turing (Computabilidade e Complexidade)

```
TURING (1936-1950s)
    │
    ├─► (1936) Máquinas de Turing
    ├─► (1937) Demonstração de equivalência Church-Turing
    ├─► (1939) Máquinas de Turing com oráculo
    ├─► (1950) "Computing Machinery and Intelligence"
    │        Teste de Turing
    │
    ▼
GÖDEL (1931-1950s)
    │
    ├─► (1931) Incompletude
    ├─► (1940) Consistência relativa de AC, CH (L)
    │
    ▼
POST (1940s-1950s)
    │
    ├─► (1944) "Recursively Enumerable Sets of Positive
    │          Integers and Their Decision Problems"
    │          Problema de Post (graus de Turing)
    ├─► (1946) Sistemas canônicos
    │
    ▼
KLEENE (1950s-1960s)
    │
    ├─► (1952) Introduction to Metamathematics
    ├─► (1954) Graus intermediários (com Post)
    │
    ▼
DESENVOLVIMENTOS POSTERIORES:
    │
    ├─► FRIEDMAN & SPECKER (1950s-1960s)
    │       Teoria recursiva, graus de Turing
    │
    ├─► BLUM (1967)
    │       Teoria da complexidade (axiomas)
    │
    ├─► COOK (1971)
    │       P vs NP
    │       SAT é NP-completo
    │
    ├─► LEVIN (1973, independente)
    │       NP-completude (URSS)
    │
    ├─► KARP (1972)
    │       21 problemas NP-completos
    │
    └─► Hoje
            Hierarquia de complexidade
            Computabilidade, Lógica, Tipos dependentes
            Verificação formal, Teoria da prova
```

---

## Cronologia Completa (Séculos XVII-XX)

### Raízes (Séculos XVII-XIX)

| Ano | Autor | Obra | Contribuição |
|-----|-------|------|--------------|
| ~1670 | Leibniz | Characteristica Universalis (não pub.) | Visão de cálculo mecânico |
| 1847 | Boole | Mathematical Analysis of Logic | Álgebra da lógica |
| 1847 | De Morgan | Formal Logic | Lógica de relações, dualidade |
| 1874 | Cantor | "Über eine Eigenschaft..." | Teoria dos conjuntos |
| 1879 | Frege | Begriffsschrift | Lógica de predicados |
| 1884 | Frege | Grundlagen der Arithmetik | Logicismo |
| 1888 | Dedekind | Was sind und was sollen die Zahlen | Definição de infinito |
| 1889 | Peano | Arithmetices Principia | Axiomas de Peano |
| 1893/1903 | Frege | Grundgesetze der Arithmetik | Sistema lógico completo |
| 1890-1905 | Schröder | Vorlesungen über die Algebra der Logik | Sistematização monumental |

### Crise dos Fundamentos (1900-1930)

| Ano | Autor | Obra/Evento | Impacto |
|-----|-------|-------------|---------|
| 1900 | Hilbert | 23 Problemas | Agenda do século XX |
| 1902 | Russell | Carta para Frege | Paradoxo derruba Frege |
| 1907 | Brouwer | Tese | Intuitionismo |
| 1908 | Zermelo | Axiomatização de conjuntos | ZFC precursor |
| 1910-13 | Russell & Whitehead | Principia Mathematica | Formalização da matemática |
| 1912 | Brouwer | "Intuitionism and Formalism" | Debate público |
| 1920 | Skolem | Forma normal | Redução lógica |
| 1921 | Weyl | "Neue Grundlagenkrise" | Defesa do intuitionismo |
| 1922 | Hilbert | "Neubegründung" | Resposta formalista |
| 1928 | Hilbert & Ackermann | Grundzüge der theoretischen Logik | Entscheidungsproblem |

### O Ano Milagroso e Consequências (1931-1950)

| Ano | Autor | Obra | Contribuição |
|-----|-------|------|--------------|
| 1931 | Gödel | Incompletude | Fim do programa de Hilbert |
| 1936 (Abr) | Church | "Unsolvable Problem" | Lambda cálculo, indecidibilidade |
| 1936 (Mai) | Turing | "On Computable Numbers" | Máquinas de Turing |
| 1936 (Out) | Post | "Finite Combinatory Processes" | Sistemas canônicos |
| 1936-37 | Kleene | Vários papers | Equivalência Church-Turing-Kleene |
| 1944 | Post | "Recursively Enumerable Sets" | Problema de Post |
| 1950 | Turing | "Computing Machinery and Intelligence" | Teste de Turing |

---

## Diagrama de Influência Direta (Simplificado)

```
                    LEIBNIZ (1670s)
                         │
                         │ "Calculemus!"
                         │
                         ▼
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
 BOOLE (1847)       CANTOR (1874)        DEDEKIND (1888)
    │                    │                    │
    │ Álgebra            │ Teoria dos        │ Indução/
    │ da Lógica          │ Conjuntos         │ Recursão
    ▼                    ▼                    ▼
 DE MORGAN        ZERMELO (1908)        PEANO (1889)
 PEIRCE                │                    │
    │                    │                    │
    ▼                    ▼                    ▼
SCHRÖDER (1890)   FRAENKEL (1922)      SKOLEM (1920)
    │                    │                    │
    └──────────────┬─────┴────────────────────┘
                   │
                   ▼
              FREGE (1879-1903)
                   │
                   │ Logicismo
                   │ Quantificadores
                   │
                   ▼
         RUSSELL (1902: Paradoxo)
                   │
                   │ Teoria dos Tipos
                   │
                   ▼
         PRINCIPIA MATHEMATICA (1910-13)
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
BROUWER      HILBERT        GÖDEL (1931)
(1907)       (1900-1928)        │
    │              │            │
    │ Intuitionismo│            │ Incompletude
    │              │            │
    ▼              ▼            ▼
 WEYL (1921) ──► HILBERT & ACKERMANN (1928)
                    │
                    │ Entscheidungsproblem
                    │
                    ▼
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   CHURCH      TURING       POST
   (Abr 1936)  (Mai 1936)   (Out 1936)
   Lambda      Máquinas    Sistemas
   Cálculo     de Turing   Canônicos
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
              KLEENE (1936)
              Equivalência
                    │
                    ▼
        ═══════════════════════════
        CHURCH-TURING THESIS (1937)
        ═══════════════════════════
                    │
                    ▼
              Toda a Computação
              Moderna
```

---

## A Raiz Primordial: Leibniz

**Gottfried Wilhelm Leibniz (1646-1716)**

A ideia que motiva toda esta tradição:

> "The only way to rectify our reasonings is to make them as tangible as those of the Mathematicians, so that we can find our error at a glance, and when there are disputes between persons, we can simply say: Let us calculate [calculemus], without further ado, to see who is right."
> 
> — Leibniz, *The Art of Discovery* (1685)

**Characteristica Universalis** (Linguagem Universal):
- Uma notação precisa para todo conhecimento
- Símbolos que representam conceitos primitivos
- Combinação de símbolos = combinação de conceitos

**Calculus Ratiocinator** (Cálculo do Raciocínio):
- Regras formais para manipular símbolos
- Mecânico, sem ambiguidade
- Resolve disputas por cálculo, não argumento

**A ironia:** Leibniz queria uma máquina para resolver disputas. Turing provou que existem problemas que **nenhuma** máquina pode resolver.

---

## Conclusão

A árvore genealógica de Turing 1936 é uma **convergência de múltiplas tradições**:

1. **Tradição Lógica:** Aristóteles → Escolástica → Leibniz → Boole/De Morgan → Schröder → Frege → Russell → Hilbert

2. **Tradição Conjuntista:** Cantor → Zermelo → Fraenkel → von Neumann

3. **Tradição Aritmética:** Dedekind → Peano → Skolem → Gödel → Kleene

4. **Tradição Intuitionista:** Krönecker → Brouwer → Weyl → Heyting

5. **Tradição Computacional:** Leibniz → Boole → Church/Turing/Post/Kleene

**O momento de convergência (1936):**
- Church (abril): Lambda cálculo
- Turing (maio): Máquinas de Turing
- Post (outubro): Sistemas canônicos
- Kleene: Equivalência

**O resultado:** A **Tese de Church-Turing** — "efetivamente calculável" é capturado por todas estas formalizações.

**Turing é o ponto culminante** porque:
1. Modelo **intuitivo** (máquinas mecânicas)
2. Máquina **Universal** (computador programável)
3. Base para **toda a ciência da computação**

---

## Referências Principais por Período

### Raízes (Séculos XVII-XIX)
- Leibniz, *The Art of Discovery* (1685)
- Boole, *Mathematical Analysis of Logic* (1847)
- Cantor, "Über eine Eigenschaft..." (1874)
- Frege, *Begriffsschrift* (1879)
- Dedekind, *Was sind und was sollen die Zahlen* (1888)
- Peano, *Arithmetices Principia* (1889)
- Schröder, *Vorlesungen über die Algebra der Logik* (1890-1905)

### Crise (1900-1930)
- Hilbert, *23 Probleme* (1900)
- Russell, Carta para Frege (1902)
- Russell & Whitehead, *Principia Mathematica* (1910-1913)
- Brouwer, *Over de Grondslagen der Wiskunde* (1907)
- Weyl, "Über die neue Grundlagenkrise" (1921)
- Hilbert & Ackermann, *Grundzüge der theoretischen Logik* (1928)

### O Ano Milagroso (1931-1936)
- Gödel, "Über formal unentscheidbare Sätze..." (1931)
- Church, "An Unsolvable Problem..." (1936)
- Turing, "On Computable Numbers..." (1936)
- Post, "Finite Combinatory Processes" (1936)
- Kleene, "λ-definability and recursiveness" (1936)

### Desenvolvimentos (Pós-1936)
- Turing, "Computing Machinery and Intelligence" (1950)
- Kleene, *Introduction to Metamathematics* (1952)
- Cook, "The Complexity of Theorem-Proving Procedures" (1971)
- Karp, "Reducibility among Combinatorial Problems" (1972)

---

_Gerado: 2026-03-09_
_Fontes: Stanford Encyclopedia of Philosophy, Wikipedia, fontes académicas primárias_
_Estrutura: Árvore genealógica multi-radicada com 7 linhagens convergentes_