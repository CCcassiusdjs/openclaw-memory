# Grundzüge der Theoretischen Logik (1938)

**Autores:** David Hilbert & Wilhelm Ackermann  
**Edição:** 2ª edição (1938), Springer  
**Localização:** `/home/csilva/Documents/[Grundlehren der mathematischen Wissenschaften №27 ] D. Hilbert, W. Ackermann (auth.) - Grundzüge der Theoretischen Logik (1938, Springer) [10.1007_978-3-662-41928-1] - libgen.li.pdf`  
**Páginas:** 144

---

## Contexto Histórico

Este livro é um dos textos **fundadores da lógica matemática moderna**. Baseado nas conferências de Hilbert em Göttingen (1917-1922), foi compilado por Ackermann. A primeira edição (1928) continha o problema da completude do cálculo de predicados que **Gödel provou em 1929-1930** - um marco histórico.

### Referência a Bernays
Paul Bernays colaborou significativamente. A terminologia foi ajustada na 2ª edição para corresponder aos "Grundlagen der Mathematik" de Hilbert-Bernays (1934).

---

## Capítulo I: Der Aussagenkalkül (Cálculo Proposicional)

### §1. Introdução das Conexões Lógicas Fundamentais

**Definição de Aussage (Proposição):** Todo Satz do qual faz sentido afirmar que seu conteúdo é verdadeiro ou falso.

**Operadores fundamentais:**
| Símbolo | Leitura | Definição |
|---------|---------|-----------|
| X̄ | "não X" | Contraditório oposto de X |
| X & Y | "X e Y" | Conjunção (verdadeiro sse ambos verdadeiros) |
| X ∨ Y | "X ou Y" | Disjunção inclusiva (latim: vel) |
| X → Y | "se X, então Y" | Implicação (falso sse X verdadeiro e Y falso) |
| X ∼ Y | "X equivalente Y" | Equivalência (mesmo valor de verdade) |

**Nota crucial:** A implicação X → Y não significa relação de causa e efeito. É sempre verdadeira se X é falso OU se Y é verdadeiro.

### §2. Equivalências; Dispensabilidade de Conexões Fundamentais

**Equivalências fundamentais (leis algébricas):**

```
(1)  X̄̄ ≡ X                           (dupla negação)
(2)  X & Y ≡ Y & X                     (comutativa)
(3)  X & (Y & Z) ≡ (X & Y) & Z        (associativa)
(4)  X ∨ Y ≡ Y ∨ X                     (comutativa)
(5)  X ∨ (Y ∨ Z) ≡ (X ∨ Y) ∨ Z        (associativa)
(6)  X ∨ (Y & Z) ≡ (X ∨ Y) & (X ∨ Z)  (distributiva)
(7)  X & (Y ∨ Z) ≡ (X & Y) ∨ (X & Z)  (segunda distributiva)
(8)  X & X ≡ X                         (idempotência)
(9)  X ∨ X ≡ X                         (idempotência)
(10) X & ⊤ ≡ X                          (⊤ = verdadeiro)
(11) X & ⊥ ≡ ⊥                          (⊥ = falso)
(12) X ∨ ⊤ ≡ ⊤
(13) X ∨ ⊥ ≡ X
```

**Leis de Morgan:**
```
(18) X̄ & Ȳ ≡ X ∨ Y      (negação de conjunção)
(19) X̄ ∨ Ȳ ≡ X & Y      (negação de disjunção)
```

**Redução a operadores primitivos:**
- {&, ¬} é completo (suficiente para expressar todas as conexões)
- {∨, ¬} é completo
- {→, ¬} é completo
- {∼, ¬} NÃO é completo (não pode expressar X & Y)
- **Sheffer stroke** (X|Y = "X e Y não ambos") é suficiente sozinho

### §3. Forma Normal para Expressões Lógicas

**Teorema:** Toda expressão proposicional pode ser trazida a uma **forma normal conjuntiva**:
- Uma conjunção de disjunções
- Cada disjunção contém apenas variáveis ou negações de variáveis

**Regras de transformação:**
- a₁) Associativa, comutativa, distributiva para & e ∨
- a₂) X̄̄ pode ser substituído por X
- a₃) X̄ & Ȳ por X ∨ Ȳ, X̄ ∨ Ȳ por X̄ & Y
- a₄) X → Y por X̄ ∨ Y, X ∼ Y por (X̄ ∨ Y) & (Ȳ ∨ X)

### §4. Caracterização das Proposições Sempre Verdadeiras

**Critério de validade:** Uma expressão em forma normal conjuntiva é **sempre verdadeira (allgemeingültig)** se e somente se cada conjunção contém uma variável e sua negação.

**Exemplos:**
- X̄ ∨ X é sempre verdadeiro (contém X e X̄)
- (X → Y) & (Y → Z) → (X → Z) sempre verdadeiro

### §5. Princípio da Dualidade

**Teorema:** De uma fórmula sempre verdadeira cujos lados contêm apenas variáveis e negações conectadas por & e ∨, obtém-se outra fórmula verdadeira trocando & ↔ ∨.

**Exemplo:** De X ∨ (Y & Z) ∼ (X ∨ Y) & (X ∨ Z) deriva-se X & (Y ∨ Z) ∼ (X & Y) ∨ (X & Z).

### §6. Forma Normal Disjuntiva

**Definição:** Disjunção de conjunções, onde cada conjunção contém variáveis ou suas negações.

**Aplicação:** Uma fórmula é sempre falsa sse cada disjunção contém uma variável e sua negação.

### §7. Multiplicidade das Conexões Proposicionais

**Teorema:** Com n variáveis, existem exatamente **2^(2^n)** proposições distintas não-equivalentes.

**Constituentes de Schröder:** Desenvolvimento de uma proposição segundo X₁, X₂, ..., Xₙ produz uma forma normal "distinta" (única a menos de reordenação).

### §8-9. Validade, Satisfatibilidade, Consequências de Axiomas

**Problema da decisibilidade (Entscheidungsproblem):** Para o cálculo proposicional, é decidível - basta verificar forma normal conjuntiva.

**Derivação de consequências:** Dados axiomas A₁, A₂, ..., Aₙ, uma proposição F é consequência sse (A₁ & A₂ & ... & Aₙ) → F é sempre verdadeiro.

### §10. Axiomas do Cálculo Proposicional

**Axiomas de Hilbert-Ackermann (baseados em Whitehead-Russell):**
```
a) X ∨ X̄ → X
b) X → X ∨ Y  
c) X ∨ Y → Y ∨ X
d) (X → Y) → [Z̄ ∨ X → Z̄ ∨ Y]
```

**Regras de inferência:**
- α) **Einsetzungsregel (Substituição):** Para variável proposicional, pode-se substituir por qualquer expressão.
- β) **Schlußschema (Modus Ponens):** De A e A → B, deriva-se B.

**Outros sistemas axiomáticos:**
- Frege: 6 axiomas com → e ¬
- Łukasiewicz-Tarski: 3 axiomas
- Nicod: 1 axioma com Sheffer stroke
- Gentzen: "Kalkül des natürlichen Schließens" (sem axiomas lógicos, apenas esquemas de inferência)

### §11. Exemplos de Derivação

**Regras derivadas importantes:**
- Regra I: Se A ∨ Ā é demonstrável, então A também é.
- Regra II: Se A é demonstrável, então A ∨ B também é.
- Regra V: Se A → B e B → C são demonstráveis, então A → C também é.

**Derivações clássicas:**
- Lei comutativa da disjunção
- Lei associativa da disjunção
- Lei distributiva
- Lei de Morgan

### §12. Consistência do Sistema Axiomático

**Definição:** Sistema é consistente se não se pode derivar ambas A e Ā para nenhuma proposição A.

**Prova:** Interpretação aritmética:
- Variáveis X, Y, Z tomam valores 0 ou 1
- X ∨ Y interpretado como produto aritmético
- X̄: se X = 0 então X̄ = 1, se X = 1 então X̄ = 0

**Resultado:** Todos os axiomas e fórmulas derivadas têm valor 0 (verdadeiro). Logo, não se pode derivar A e Ā simultaneamente.

### §13. Independência e Completude

**Independência:** Cada axioma a), b), c), d) é independente dos outros (demonstrado via interpretações aritméticas com diferentes estruturas de valores).

**Completude (dois sentidos):**
1. **Fraco:** Todas as fórmulas sempre verdadeiras são deriváveis.
2. **Forte:** Adicionar qualquer fórmula não derivável cria inconsistência.

**Teorema:** O sistema de Hilbert-Ackermann é completo em ambos os sentidos.

---

## Capítulo II: Der Klassenkalkül (Cálculo de Classes)

### §1. Interpretação como Cálculo de Predicados Unários

**Mudança de interpretação:** X, Y, Z agora representam **predicados** (propriedades), não proposições completas.

- X̄: predicado oposto (ex: "não é belo")
- X & Y: predicado composto ("é transitório e possui conhecimento")
- X ∨ Y: predicado alternativo

**Interpretação semântica:** Uma fórmula X é "verdadeira" se o predicado X se aplica a **todos os objetos**.

**Juízos universais tradicionais:**
- "Todos os homens são mortais" → X̄ ∨ Y (onde X = "é homem", Y = "é mortal")

### §2. Interpretação como Cálculo de Classes

**Definição:** Cada predicado corresponde a uma **classe** (extensão).

- X̄: complemento da classe X
- X & Y: interseção de X e Y
- X ∨ Y: união de X e Y

**Fórmula verdadeira:** X representa a classe universal (todos os objetos).

**Fórmula X → Y:** X é subclasse de Y.

**Fórmula X ∼ Y:** Classes X e Y são idênticas.

### §3. Derivação Sistemática dos Silogismos Aristotélicos

**As quatro formas de juízo:**
| Tipo | Forma | Símbolo |
|------|-------|---------|
| a | Universal afirmativo | "Todo A é B" |
| i | Particular afirmativo | "Algum A é B" |
| e | Universal negativo | "Nenhum A é B" |
| o | Particular negativo | "Algum A não é B" |

**Representação simbólica:**
- a: |X̄ ∨ Y| (para todo x, se x é A então x é B)
- i: |X̄ & Ȳ| (negativo do e-type)
- e: |X̄ ∨ Ȳ| (para todo x, se x é A então x não é B)
- o: |X̄ & Y| (negativo do a-type)

**Quatro figuras do silogismo:**
```
Figura 1:  MP    Figura 2:  PM    Figura 3:  MP    Figura 4:  PM
           SM               SM               MS               MS
           SP               SP               SP               SP
```

**19 silogismos válidos (mnemônicos):**

| Figura 1 | Figura 2 | Figura 3 | Figura 4 |
|----------|----------|----------|----------|
| barbara | cesare | datisi | calemes |
| celarent | camestres | feriso | fresison |
| darii | festino | disamis | dimatis |
| ferio | baroco | bocardo | bamalip |
| | | darapti | fesapo |
| | | felapton | |

**Derivação formal:** Cada silogismo é derivável no cálculo combinado proposicional + predicados.

---

## Capítulo III: Der engere Prädikatenkalkül (Cálculo de Predicados Estreito)

### §1-2. Insuficiência do Cálculo Anterior

**Problema:** O cálculo proposicional não captura estrutura interna das proposições (sujeito-predicado).

**Exemplo clássico:**
- "Todos os homens são mortais; Sócrates é homem; logo Sócrates é mortal"
- NÃO derivável no cálculo proposicional puro.

### §3-4. Notação do Cálculo de Predicados

**Quantificadores:**
| Símbolo | Leitura | Definição |
|---------|---------|-----------|
| ∀x F(x) | "para todo x, F(x)" | Quantificador universal |
| ∃x F(x) | "existe x tal que F(x)" | Quantificador existencial |
| ∃x | = ¬∀x¬ | Equivalência fundamental |

**Variáveis:**
- **Livres:** podem ser substituídas por termos
- **Ligadas:** estão sob escopo de quantificador

**Formas Normais:**
- **Pränex-Normalform:** Todos quantificadores no início
- **Skolem-Normalform:** Prefixo ∀*∃* seguido de matriz sem quantificadores

### §5-6. Sistema Axiomático do Cálculo de Predicados

**Axiomas do cálculo proposicional + axiomas específicos:**

| Axioma | Forma | Significado |
|--------|-------|-------------|
| e) | ∀x F(x) → F(y) | Instantiation universal |
| f) | F(y) → ∃x F(x) | Generalização existencial |

**Regras de inferência:**
- α1) Substituição de variáveis livres
- α2) Substituição de variáveis individuais
- α3) Substituição de predicados
- β) Modus ponens (Schlußschema)
- γ1) Generalização: de φ(y) derivar ∀x φ(x)
- γ2) Existencial: de φ(y) derivar ∃x φ(x)
- δ) Regra de renomeação para variáveis ligadas

### §7-8. Dualidade e Formas Normais

**Extensão do princípio de dualidade:**
- Trocar ∀ ↔ ∃
- Trocar & ↔ ∨
- Negar fórmulas atômicas

**Teorema de Skolem:** Toda fórmula pode ser transformada em forma normal de Skolem, preservando satisfatibilidade.

### §9. Consistência e Independência do Sistema Axiomático

**Teorema de Consistência:** O sistema é consistente (não se pode derivar A e Ā).

**Prova (interpretação aritmética):**
- Variáveis X, Y tomam valores 0 ou 1
- X ∨ Y interpretado como produto aritmético
- Todos axiomas e fórmulas derivadas têm valor 0 (verdadeiro)

**Independência:** Cada axioma a)-f) é independente dos outros (demonstrado via interpretações aritméticas com diferentes estruturas de valores).

### §10. Completude do Sistema Axiomático (Teorema de Gödel 1930)

**Completude (sentido fraco):** Toda fórmula semanticamente válida é derivável.

**Completude (sentido forte):** Adicionar qualquer fórmula não derivável cria inconsistência.

**Prova (esquema):**
1. Redução à forma normal de Skolem
2. Enumeração de k-tuplos: (x₀,x₀,...,x₀), (x₀,x₀,...,x₁), ...
3. Construção de sequência Ψ₁, Ψ₂, ..., Ψₙ
4. **Alternativa:**
   - Caso 1: Ψₙ é tautologia proposicional → fórmula derivável
   - Caso 2: Para todo n, Ψₙ não é tautologia → construir modelo no domínio ℕ

**Corolário de Löwenheim:** Se uma fórmula é válida num domínio infinito enumerável, é válida em todo domínio.

### §11. Derivação de Consequências de Premissas

**Método:** As premissas são adicionadas como axiomas ao sistema lógico.

**Exemplo 1 (silogismo aristotélico):**
```
Premissas:
  (x)(Ms(x) → St(x))    [Todo homem é mortal]
  Ms(Cajus)             [Cajus é homem]

Derivação:
  (x)(Ms(x) → St(x)) → (Ms(y) → St(y))     [por e)]
  Ms(Cajus) → St(Cajus)                     [substituição]
  St(Cajus)                                  [modus ponens]
```

**Exemplo 2 (geometria):**
- Teorema de Pascal especial → derivável dos axiomas de incidência, ordem e paralelismo
- Demonstração via forma normal e equivalências lógicas

### §12. O Entscheidungsproblem

**Formulação:** Dada uma fórmula do cálculo de predicados, decidir se é válida/satisfatível.

**Casos decidíveis:**

| Caso | Critério | Decidibilidade |
|------|----------|----------------|
| Monádico | Apenas predicados unários | Decidível (Löwenheim 1915) |
| Prefixo ∀* | Apenas quantificadores universais | Decidível |
| Prefixo ∃* | Apenas quantificadores existenciais | Decidível |
| Prefixo ∀*∃* | Universais antes de existenciais | Decidível |
| Prefixo ∀∀∃* | Dois universais, depois existenciais | Decidível (Gödel 1932) |

**Resultado de Church-Turing (1936):** O Entscheidungsproblem é **indecidível** em geral.

**Teorema:** Não existe algoritmo recursivo que decida validade para todo o cálculo de predicados de primeira ordem.

---

## Capítulo IV: Der erweiterte Prädikatenkalkül (Cálculo de Predicados Estendido)

### §1. Cálculo de Predicados de Segunda Ordem

**Motivação:** O cálculo de primeira ordem não pode expressar "não para todo predicado P" - precisamos de ∃P.

**Extensão:** Permitir quantificadores sobre predicados:
- ∀P ∃x P(x)
- "Para todo predicado P, existe x tal que P(x)"

**Aplicações fundamentais:**

| Conceito | Formulação em 2ª ordem |
|----------|------------------------|
| Identidade | x = y ≡ ∀P (P(x) ↔ P(y)) |
| Indução matemática | ∀P [P(0) & ∀n(P(n)→P(n+1))] → ∀n P(n) |
| Finitude | "exatamente n elementos" é definível |

**Exemplos de fórmulas identicamente verdadeiras (2ª ordem):**
- (x)(=(x,x)) [Reflexividade]
- (x)(y)(=(x,y) → =(y,x)) [Simetria]
- (EF)(Ex)F(x) [Existência de predicado]

**Teorema de Gödel (1931):** Não existe sistema axiomático completo para todas as identidades da 2ª ordem.

### §2. Predicados de Predicados; Tratamento Lógico do Conceito de Número

**Definição de número cardinal via lógica:**

| Número | Definição |
|--------|-----------|
| 0(F) | ¬∃x F(x) ["nada é F"] |
| 1(F) | ∃x[F(x) & ∀y(F(y)→=(x,y))] |
| 2(F) | ∃x∃y[¬=(x,y) & F(x) & F(y) & ∀z(F(z)→=(z,x)∨=(z,y))] |

**Igualdade numérica:**
```
Glz(F,G) ≡ ∃R{(x)[F(x)→∃y(R(x,y)&G(y))] & 
            (y)[G(y)→∃x(R(x,y)&F(x))] & 
            (x)(y)(z)[(R(x,y)&R(x,z)→=(y,z)) & (R(x,z)&R(y,z)→=(x,y))]}
```

**Adição:** Se F e G são incompatíveis e têm m e n elementos, então F∨G tem m+n elementos.

**Exemplo:** 1+1=2 é derivável como identidade lógica:
```
(F)(G){[Unv(F,G) & 1(F) & 1(G)] → 2(F∨G)}
```

### §3. Representação de Conceitos de Teoria dos Conjuntos

**Correspondência predicado-conjunto:**
- Predicado P(x) → Conjunto {x | P(x)}
- P(x) significa "x pertence ao conjunto definido por P"

**Definições:**
| Conceito | Formulação |
|----------|------------|
| Subconjunto | (x)(P₁(x)→P₂(x)) |
| União | P₁(x) ∨ P₂(x) |
| Interseção | P₁(x) & P₂(x) |
| Equivalência | ∃R{...} (bijunção) |
| Conjunto das partes | Te(P) ≡ (x)(P(x)→D(x)) |

### §4. Os Paradoxos Lógicos

**Paradoxo de Russell (1901):**

Definição: Pd(P) ≡ "P não se aplica a si mesmo"

Então: Pd(Pd) ≡ Pd não se aplica a si mesmo.

**Contradição:**
- Se Pd(Pd) é verdadeiro, então Pd se aplica a si mesmo → ¬Pd(Pd)
- Se Pd(Pd) é falso, então Pd não se aplica a si mesmo → Pd(Pd)

**Paradoxo do Mentiroso (Epimenides):**
- "Eu estou mentindo agora" = "Esta frase é falsa"
- Se verdadeiro, então falso
- Se falso, então verdadeiro

**Formulação formal:**
```
Bh[(X)(Bh(X)→X)] e (X)[Bh(X)→=(X, Ψ)]
onde Ψ = "tudo que $ afirma em t é falso"
```

**Paradoxo de Berry-Richard:**
- "O menor número não definível em menos de cem palavras"
- Esta frase define um número em menos de cem palavras!

**Formulação:**
```
Mds(x) ≡ Dsc(x) & (y)(<(y,x)→Dsc(y))
["x é o menor número não definível simbolicamente"]
Scr(Mds) → contradição
```

### §5. O Stufenkalkül (Cálculo de Níveis)

**Solução de Russell-Hilbert:** Hierarquia de tipos de predicados.

**Tipos de predicados:**
| Nível | Definição | Exemplos |
|-------|-----------|----------|
| Tipo i | Indivíduos | x, y, z |
| Tipo (i) | Predicados unários de indivíduos | F(x), G(x) |
| Tipo (i,i) | Predicados binários de indivíduos | R(x,y) |
| Tipo ((i)) | Predicados de predicados (nível 1) | Ref(R), Sym(R) |
| Tipo (((i))) | Predicados de nível 2 | Números 0, 1, 2 |

**Regra fundamental:** Um predicado de nível n só pode aplicar-se a predicados de nível menor ou igual.

**Axiomas do Stufenkalkül:**

| Grupo | Conteúdo |
|-------|----------|
| I | Axiomas a)-d) do cálculo proposicional |
| II | (G)F(G)→F(H) e F(H)→(EG)F(G) |
| III | Axioma de escolha (extensão de g)) |
| IV | Axiomas de extensionalidade |
| V | Axiomas de compreensão |

**Compreensão (axioma V):**
```
(EF)(G₁)...(Gₙ)(F(G₁,...,Gₙ) ↔ Ψ(G₁,...,Gₙ))
["Existe predicado F equivalente à fórmula Ψ"]
```

### §6. Aplicações do Stufenkalkül

**Fundamentação dos números reais (Dedekind):**

**Definição de Schnitt (corte):**
```
Sc(P) ≡ (Ex)P(x) & (Ex)¬P(x) & 
        (x){P(x)→(Ey)(<(x,y)&P(y))} & 
        (x){P(x)→(y)(<(y,x)→P(y))}
```

**Números reais como cortes:**
- Cada predicado P com Sc(P) define um número real
- P e Q definem mesmo número sse Aeq(P,Q)

**Ordem:** ≤(P,Q) ≡ Imp(P,Q) ≡ (x)(P(x)→Q(x))

**Soma:** A soma de P e Q é o predicado:
```
Vg(x,A) ≡ (EP)(P(x)&A(P))
```

**Teorema da cota superior:** Toda conjunto não-vazio limitado de reais tem supremo.

**Prova no Stufenkalkül:**
1. Conjunto de reais = predicado A(P) de predicados
2. Se A tem cota superior, Vg(x,A) é o supremo
3. Demonstração de que Vg satisfaz as propriedades de corte

---

## Referências Históricas no Livro

| Autor | Obra | Contribuição |
|-------|------|--------------|
| Leibniz | — | Primeira ideia de lógica matemática |
| Boole (1815-1864) | — | Base da álgebra da lógica |
| Schröder (1890-1895) | Vorlesungen über die Algebra der Logik | Desenvolvimento sistemático |
| Frege (1879, 1893-1903) | Begriffsschrift, Grundgesetze | Sistema formal completo |
| Peano (1894) | Formulaire de Mathematiques | Notação axiomática |
| Whitehead-Russell (1910-1913) | Principia Mathematica | Teoria dos tipos |
| Gödel (1929-1930) | Completude do cálculo de predicados | Prova fundamental |
| Church (1936) | Indecidibilidade do Entscheidungsproblem | Resultado negativo |
| Turing (1936) | Computabilidade | Equivalente a Church |
| Löwenheim (1915) | Teorema de Löwenheim | Domínios infinitos enumeráveis |
| Skolem (1920) | Normalização | Forma normal de Skolem |
| Bernays | Correções e colaboração | Co-autor de Hilbert |
| Gentzen (1934) | Cálculo de sequentes | Sistema natural |
| Tarski (1935) | Conceito de verdade | Semântica formal |

---

## Status de Leitura

| Capítulo | Status | Observações |
|----------|--------|-------------|
| Introdução | ✅ Completo | Contexto histórico |
| Capítulo I | ✅ Completo | Cálculo proposicional axiomático |
| Capítulo II | ✅ Completo | Cálculo de classes/silogismos |
| Capítulo III | ✅ Completo | Cálculo de predicados de 1ª ordem |
| Capítulo IV | ✅ Completo | Cálculo estendido/paradoxos/Stufenkalkül |

---

_Data de leitura: 2026-03-10_
_Livro lido integralmente com extração de provas fundamentais_

---

## Teoremas e Conceitos Fundamentais

### 1. Forma Normal Conjuntiva
Toda proposição é equivalente a uma conjunção de disjunções de literais.

### 2. Critério de Validade (Proposicional)
Uma fórmula em forma normal é válida sse cada cláusula contém variável e sua negação.

### 3. Princípio de Dualidade
Trocar & ↔ ∨ preserva validade em fórmulas sem → ou ∼.

### 4. Completude do Cálculo Proposicional
Todas as tautologias são deriváveis; sistema é maximally consistent.

### 5. Completude do Cálculo de Predicados (Gödel)
Toda fórmula válida de primeira ordem é derivável.

### 6. Indecidibilidade (Church-Turing)
Não existe algoritmo para decidir validade em primeira ordem geral.

---

## Notação

| Símbolo | Significado |
|---------|-------------|
| X̄, ¬X, ~X | Negação |
| X & Y, X ∧ Y | Conjunção |
| X ∨ Y | Disjunção |
| X → Y, X ⊃ Y | Implicação |
| X ∼ Y, X ↔ Y | Equivalência |
| ∀x | Quantificador universal |
| ∃x | Quantificador existencial |
| X ≡ Y | Equivalência lógica |

---

## Referências Históricas no Livro

1. Leibniz - primeira ideia de lógica matemática
2. Boole (1815-1864) - base da álgebra da lógica
3. Schröder (1890-1895) - "Vorlesungen über die Algebra der Logik"
4. Frege (1879, 1893-1903) - "Begriffsschrift" e "Grundgesetze"
5. Peano (1894) - "Formulaire de Mathematiques"
6. Whitehead-Russell (1910-1913) - "Principia Mathematica"
7. Bernays - colaborador, correções e melhorias
8. Gentzen (1934) - "Kalkül des natürlichen Schließens"
9. Gödel (1929-1930) - prova de completude

---

## Status de Leitura

| Capítulo | Status | Observações |
|----------|--------|-------------|
| Introdução | ✅ Completo | Contexto histórico |
| Capítulo I | ✅ Completo | Cálculo proposicional axiomático |
| Capítulo II | ✅ Completo | Cálculo de classes/silogismos |
| Capítulo III | 🔄 Em extração | Cálculo de predicados de 1ª ordem |
| Capítulo IV | 🔄 Em extração | Cálculo estendido/paradoxos |

---

_Data de leitura: 2026-03-10_
_Próxima etapa: Extrair Capítulos III e IV com detalhes das provas_