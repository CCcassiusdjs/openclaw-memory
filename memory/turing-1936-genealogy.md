# Árvore Genealógica Acadêmica: Turing 1936

## O Paper Fundacional

**Alan Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem" (1936)**

Este paper é um dos mais importantes da história da computação. Nele, Turing:
1. Define formalmente o que é um "número computável"
2. Introduz a noção de "máquina de Turing"
3. Prova que o Entscheidungsproblem é insolúvel (independentemente de Church)

---

## Árvore Genealógica (do paper até as raízes)

```
TURING (1936)
    │
    ├─► ENTSCHEIDUNGSPROBLEM (Hilbert & Ackermann, 1928)
    │       │
    │       └─► "Principles of Mathematical Logic"
    │           Formulação: "Existe um algoritmo que decide
    │           se uma fórmula de primeira ordem é válida?"
    │
    ├─► HILBERT'S PROGRAM (1920s)
    │       │
    │       ├─► Resposta ao INTUITIONISM (Brouwer, Weyl, 1921)
    │       │   Crise dos fundamentos - debate sobre o que é
    │       │   matemática válida
    │       │
    │       └─► HILBERT'S PROBLEMS (1900)
    │           Especialmente o 2º problema:
    │           "Provar a consistência dos axiomas da aritmética"
    │
    ├─► GÖDEL'S INCOMPLETENESS THEOREMS (1931)
    │       │
    │       └─► Mostrou que sistemas formais suficientemente
    │           expressivos são incompletos ou inconsistentes
    │           (Resposta ao programa de Hilbert)
    │
    ├─► CHURCH (1936) - Lambda Calculus
    │       │
    │       └─► Prova independente do Entscheidungsproblem
    │           via cálculo lambda (publicado antes de Turing)
    │
    └─► PRINCIPIA MATHEMATICA (Russell & Whitehead, 1910-1913)
            │
            └─► Tentativa de fundar toda matemática na lógica
                (Resposta à crise dos paradoxos)

```

---

## Linha do Tempo Completa (Raízes até Turing)

### RAIZ PRIMORDIAL: Leibniz (século XVII)

**Gottfried Wilhelm Leibniz (1646-1716)**

- **Characteristica Universalis** - Visão de uma linguagem universal para representar todo conhecimento
- **Calculus Ratiocinator** - Cálculo de raciocínio que permitiria resolver disputas por computação
- **Visão:** "Se houver controvérsia, podemos dizer: 'Calculemos!'"

Esta é a ideia seminal que motiva toda a tradição: **reduzir raciocínio a cálculo mecânico.**

---

### NÍVEL 1: Os Fundamentos (Século XIX)

#### Georg Cantor (1874)
- **Paper fundador da Teoria dos Conjuntos:** "Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen"
- Introduz conceito de cardinalidade infinita
- Mostra que existem "diferentes tamanhos de infinito"
- **Cria o solo sobre o qual os paradoxos surgirão**

#### Gottlob Frege (1879, 1884, 1893/1903)

| Ano | Obra | Contribuição |
|-----|------|--------------|
| 1879 | **Begriffsschrift** | Primeiro sistema de lógica formal moderna (cálculo de predicados de segunda ordem) |
| 1884 | **Die Grundlagen der Arithmetik** | Filosofia dos números, crítica de outras teorias |
| 1893/1903 | **Grundgesetze der Arithmetik** | Tentativa de derivar toda aritmética da lógica (Logicismo) |

**Influência de Frege:**
- Russell: "Frege é o maior lógico desde Aristóteles"
- Whitehead & Russell basearam grande parte de Principia Mathematica no trabalho de Frege
- O paradoxo de Russell (1902) foi descoberto analisando o sistema de Frege

---

### NÍVEL 2: A Crise dos Paradoxos (1900-1910)

#### Paradoxo de Russell (1901/1902)

**Bertrand Russell** descobre que o sistema de Frege leva a contradição:

> O conjunto de todos os conjuntos que não contêm a si mesmos
> contém a si mesmo? (Se sim, não. Se não, sim.)

**Carta para Frege (16 de junho de 1902):**
- Frege estava prestes a publicar o Vol. II de Grundgesetze
- O paradoxo derruba seu sistema lógico
- Frege responde: "Sua descoberta da contradição causou-me surpresa
  e, temo, grande consternação"

**Importância:** Este paradoxo foi o catalisador que mostrou a necessidade
de fundamentos mais rigorosos para matemática e lógica.

#### Principia Mathematica (Russell & Whitehead, 1910-1913)

**Resposta ao paradoxo:** Teoria dos Tipos

- Três volumes, ~2000 páginas
- Tentativa de derivar toda matemática da lógica
- Introduz teoria dos tipos para evitar paradoxos
- **Objetivo:** "Mostrar que toda matemática é derivável de
  princípios lógicos puros"

**Legado:**
- Forneceu a base lógica que Hilbert precisava
- Influenciou Gödel, Church, Turing

---

### NÍVEL 3: Hilbert e o Programa Formalista (1900-1928)

#### Hilbert's Problems (1900)

**Congresso Internacional de Matemáticos, Paris**

Os 23 problemas de Hilbert definiram a agenda matemática do século XX.

**Problemas relevantes:**

| # | Problema | Status |
|---|----------|--------|
| 1º | Hipótese do Contínuo (Cantor) | Resolvido (independente de ZFC) |
| **2º** | **Consistência dos axiomas da aritmética** | **Parcialmente por Gödel (incompletude)** |
| 10º | Algoritmo para resolver equações diofantinas | Resolvido (indecidível - Matiyasevich, 1970) |

#### Hilbert's Program (1920s)

**Contexto:** Crise dos fundamentos

- **Intuitionism (Brouwer, Weyl):** Rejeita matemática não construtiva
- **Weyl (1921):** "A nova crise nos fundamentos da matemática"
- **Hilbert (1921):** Resposta em três palestras em Hamburgo

**O Programa:**
1. **Consistência:** Provar que axiomas não levam a contradições
2. **Completude:** Toda verdade matemática é demonstrável
3. **Decidibilidade:** Existe algoritmo para decidir qualquer proposição

**Lema famoso:**
> "Wir müssen wissen. Wir werden wissen."
> ("Devemos saber. Saberemos.")

#### Hilbert & Ackermann (1928)

**"Grundzüge der theoretischen Logik" (Principles of Mathematical Logic)**

- Primeira apresentação sistemática de lógica de primeira ordem
- Formulação explícita do **Entscheidungsproblem**:
  
  > "Existe um procedimento efetivo (algoritmo) que, dada uma
  > fórmula lógica de primeira ordem, determina se ela é
  > universalmente válida?"

**Este é o problema que Turing resolve em 1936.**

---

### NÍVEL 4: O Impacto de Gödel (1931)

#### Kurt Gödel (1931)

**"Über formal unentscheidbare Sätze der Principia Mathematica
und verwandter Systeme I"**

**Teoremas da Incompletude:**

1. **Primeiro Teorema:** Qualquer sistema formal consistente
   suficientemente expressivo para aritmética contém proposições
   verdadeiras mas indemonstráveis.

2. **Segundo Teorema:** Um sistema formal não pode provar
   sua própria consistência.

**Impacto no Programa de Hilbert:**
- Hilbert ficou surpreso e chateado
- O objetivo de provar consistência da aritmética "de dentro"
  tornou-se impossível
- Porém: Gödel não resolveu o Entscheidungsproblem

**Conexão com Turing:**
- Gödel usou "funções recursivas" para definir computabilidade
- Turing (1936) deu uma definição equivalente via máquinas
- Gödel reconheceu que a definição de Turing era "a definição
  precisa e indubitavelmente adequada" de sistema formal

---

### NÍVEL 5: Church e Lambda Cálculo (1936)

#### Alonzo Church (1936)

**"An Unsolvable Problem in Elementary Number Theory"**

- Publicado **antes** de Turing (abril 1936)
- Usa **lambda cálculo** para provar indecidibilidade
- Introduz a **Tese de Church-Turing** (noção de "efetivamente calculável")

**Resultado:** O Entscheidungsproblem é insolúvel.

**Problema:** A definição de "função lambda-definível" era abstrata
e não claramente equivalente a "calculável por algoritmo".

---

### NÍVEL 6: Turing (1936)

#### Alan Turing (1936)

**"On Computable Numbers, with an Application to the Entscheidungsproblem"**

**Contribuições fundamentais:**

1. **Máquina de Turing:** Modelo computacional simples e mecânico
   - Fita infinita
   - Cabeça de leitura/escrita
   - Estados finitos
   - Regras de transição

2. **Números Computáveis:** Definição precisa de "computável"
   - Números cujos dígitos podem ser calculados por máquina

3. **Prova do Entscheidungsproblem:**
   - Constrói a "Máquina Universal de Turing"
   - Mostra que problema da parada é indecidível
   - Conclui que Entscheidungsproblem é insolúvel

4. **Equivalência com Church:**
   - Turing prova que suas máquinas computam
     exatamente as funções lambda-definíveis
   - Estabelece a **Tese de Church-Turing**

**Por que Turing é mais famoso que Church?**
- Definição mecânica e intuitiva (máquinas)
- Construção explícita da máquina universal
- Base para ciência da computação teórica

---

## Linha de Influência Direta

```
Leibniz (1600s)
    │ "Calculemus!" - reduzir raciocínio a cálculo
    ▼
Cantor (1874)
    │ Teoria dos conjuntos - fundamento
    ▼
Frege (1879-1903)
    │ Lógica formal moderna, logicismo
    ▼
Russell (1902) ─────► Principia Mathematica (1910-1913)
    │ Paradoxo │     │ Teoria dos tipos
    ▼         │      ▼
Hilbert (1900) ──── Hilbert's Program (1920s)
    │ 2º problema    │ Consistência, Completude, Decidibilidade
    ▼                ▼
    └──────► Hilbert & Ackermann (1928)
              │ Formulação do Entscheidungsproblem
              ▼
         Gödel (1931)
         │ Incompletude - limites de sistemas formais
         ▼
         ┌────────┴────────┐
         ▼                 ▼
    Church (1936)     Turing (1936)
    Lambda cálculo     Máquinas de Turing
         │                 │
         └────► Mesmo resultado ◄─────┘
               (Entscheidungsproblem insolúvel)
```

---

## A Raiz Motivacional: "Calculemus!"

**A ideia primordial vem de Leibniz (século XVII):**

> "The only way to rectify our reasonings is to make them
> as tangible as those of the Mathematicians, so that we can
> find our error at a glance, and when there are disputes
> between persons, we can simply say: Let us calculate
> [calculemus], without further ado, to see who is right."

**Esta visão motiva:**
- Frege: Fundar aritmética na lógica (cálculo de predicados)
- Russell & Whitehead: Formalizar toda matemática
- Hilbert: Provar consistência e completude mecanicamente
- Church & Turing: Definir precisamente "cálculo mecânico"

**A ironia:** Leibniz queria uma máquina para resolver disputas.
Turing provou que existem problemas que nenhuma máquina pode resolver.

---

## Referências Principais

| Ano | Autor | Obra |
|-----|-------|------|
| 1670s | Leibniz | Characteristica Universalis (não publicado) |
| 1874 | Cantor | "Über eine Eigenschaft..." (Teoria dos conjuntos) |
| 1879 | Frege | Begriffsschrift |
| 1884 | Frege | Die Grundlagen der Arithmetik |
| 1893/1903 | Frege | Grundgesetze der Arithmetik |
| 1900 | Hilbert | 23 Problemas (Paris) |
| 1902 | Russell | Carta para Frege (Paradoxo) |
| 1910-1913 | Russell & Whitehead | Principia Mathematica |
| 1928 | Hilbert & Ackermann | Grundzüge der theoretischen Logik |
| 1931 | Gödel | Teoremas da Incompletude |
| 1936 (Abril) | Church | "An Unsolvable Problem..." |
| 1936-1937 | Turing | "On Computable Numbers..." |

---

## Conclusão

A árvore genealógica acadêmica de Turing 1936 tem como **raiz primordial**
a visão de Leibniz de uma linguagem universal de raciocínio mecânico.

A cadeia de influência direta é:

**Leibniz → Cantor → Frege → Russell → Hilbert → Gödel → Church/Turing**

Cada elo responde a uma crise ou necessidade criada pelo anterior:

1. **Cantor** cria a teoria de conjuntos (novos fundamentos)
2. **Frege** tenta fundar aritmética na lógica (logicismo)
3. **Russell** descobre paradoxo, cria teoria dos tipos
4. **Hilbert** propõe formalismo para salvar fundamentos
5. **Gödel** mostra limites da prova formal
6. **Church & Turing** mostram limites da decisão algorítmica

**Turing é o ponto culminante** de 300 anos de busca por
fundamentos rigorosos para matemática e computação.

---

_Gerado: 2026-03-09_
_Baseado em: Stanford Encyclopedia of Philosophy, Wikipedia, fontes académicas_