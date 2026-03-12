# Introduction to Large Language Models - Google ML Crash Course

**Fonte:** https://developers.google.com/machine-learning/crash-course/llm
**Autor:** Google Developers
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Introdução didática e acessível sobre language models do Google ML Crash Course. Foca nos fundamentos: tokens, N-grams, contexto e evolução para LLMs.

---

## 🎯 O que é um Language Model?

**Definição**: Um language model estima a probabilidade de um token ou sequência de tokens ocorrer dentro de uma sequência maior.

**Aplicações**:
- Geração de texto
- Tradução automática
- Resumo de documentos

**Exemplo prático**:
```
Input: "When I hear rain on my roof, I _______ in my kitchen."

Probabilidades:
- 9.4% → "cook soup"
- 5.2% → "warm up a kettle"
- 3.6% → "cower"
- 2.5% → "nap"
- 2.2% → "relax"
```

---

## 🔤 Tokens

### Definição
Tokens são a **unidade atômica** do language modeling.

### Tipos
- **Words**: Token = palavra inteira
- **Subwords**: Token = parte semântica da palavra
- **Characters**: Token = caractere único

### Tokenização por Subwords

**Exemplos**:
| Palavra | Subwords |
|---------|----------|
| unwatched | un + watch + ed |
| cats | cat + s |
| antidisestablishmentarianism | anti + dis + establish + ment + arian + ism |

**Razão inglesa**: ~1 token ≈ 4 caracteres ≈ 3/4 palavra
**Regra prática**: 400 tokens ≈ 300 palavras (inglês)

---

## 📊 N-gram Language Models

### Definição
N-grams são sequências ordenadas de N palavras usadas para construir language models.

### Exemplos
Frase: "you are very nice"

**2-grams (bigrams)**:
- "you are"
- "are very"
- "very nice"

**3-grams (trigrams)**:
- "you are very"
- "are very nice"

### Problema de Esparsidade
Conforme N aumenta:
- ✅ Mais contexto
- ❌ Menos ocorrências no corpus
- ❌ Predições menos úteis (overfitting)

**Trade-off**: N grande → mais contexto, mas mais esparsidade

---

## 🧠 Contexto

### Definição
**Contexto** é informação útil antes ou depois do token alvo.

**Importância**: Ajuda a disambiguar significados.

**Exemplo**:
- "orange is ripe" → laranja (fruta)
- "orange is cheerful" → laranja (cor)

### Limitação dos N-grams
- 3-grams: contexto = 2 palavras anteriores
- Insuficiente para muitas tarefas

---

## 🔄 Recurrent Neural Networks (RNNs)

### Vantagens sobre N-grams
- Processam sequência token a token
- Aprendem contexto gradualmente
- Podem capturar dependências em frases maiores

### Limitações
- **Vanishing gradient**: Dificulta aprendizado de dependências longas
- **Contexto limitado**: Ainda processa token a token
- **Não paralelizável**: Processamento sequencial

---

## 🚀 Large Language Models (LLMs)

### Diferença Fundamental
**LLMs avaliam todo o contexto simultaneamente**, diferentemente de:
- N-grams (contexto fixo)
- RNNs (processamento sequencial)

### Capacidades
- Representações internas ricas de linguagem
- Geração de texto plausível
- Emergent abilities em escala

---

## 💡 Conceitos-Chave

1. **Tokens são fundamentais**: Unidade básica de processamento
2. **Contexto importa**: Quanto mais, melhor
3. **N-grams são limitados**: Esparsidade + contexto fixo
4. **RNNs melhoraram**: Mas ainda sequenciais
5. **LLMs são revolucionários**: Processam tudo de uma vez

---

## 🔗 Próximos Passos

- [ ] Estudar arquitetura Transformer
- [ ] Entender attention mechanism
- [ ] Praticar tokenização BPE

---

## 📝 Tags

`#intro-llm` `#google` `#tokens` `#ngrams` `#rnn` `#fundamentals`