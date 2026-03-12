# 004 - The Illustrated GPT-2

**Fonte:** https://jalammar.github.io/illustrated-gpt2/
**Autor:** Jay Alammar
**Tipo:** Blog Post (Visual Guide)
**Relevância:** ★★★★☆ (Arquitetura GPT)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo

Artigo didático que explica a arquitetura GPT-2 (decoder-only transformer) em detalhes visuais. Complementa o "Illustrated Transformer" focando especificamente em modelos de linguagem auto-regressivos.

---

## 🏗️ GPT-2 vs Transformer Original

### Diferença Arquitetural
| Aspecto | Transformer Original | GPT-2 |
|---------|---------------------|-------|
| **Tipo** | Encoder-Decoder | Decoder-only |
| **Blocos** | 6 encoder + 6 decoder | 12 decoder blocks |
| **Self-Attention** | Normal (encoder) + Masked (decoder) | Masked apenas |
| **Contexto** | Encoder vê toda a sequência | Só vê tokens passados |
| **Auto-regressivo** | Não (encoder) / Sim (decoder) | Sim, totalmente |

### Evolução do Transformer Block
1. **Encoder Block** → Self-attention normal (pode ver todo o contexto)
2. **Decoder Block Original** → Masked self-attention + encoder-decoder attention
3. **Decoder-Only Block (GPT-2)** → Apenas masked self-attention

---

## 🎯 Language Modeling com GPT-2

### O que é um Language Model
- Prediz próxima palavra baseado no contexto anterior
- GPT-2: "autocorrect do celular em esteroides"
- Treinado em 40GB de texto (WebText)
- Variantes: 124M (small) até 1.5B parâmetros (original)

### Auto-regressão
```
Input: "The robot"
Output: "must"
Next Input: "The robot must"
Output: "obey"
...e assim por diante
```

**Diferença do BERT:**
- BERT não é auto-regressivo (usa masked LM)
- BERT vê contexto bilateral
- GPT-2 vê apenas passado (masked attention)
- XLNet: combina auto-regressão + contexto bilateral

---

## 🔍 Arquitetura Detalhada do GPT-2

### Input Encoding
1. **Token Embedding**: Look up no embedding matrix (768 dims para small)
2. **Positional Encoding**: Adiciona vetor posicional (posição 1-1024)
3. **Feed to Transformer Block**: Processa através dos blocos

### Fluxo por Bloco Transformer
```
Input Vector
    ↓
[Masked Self-Attention Layer]
    ↓
[Add & Normalize]
    ↓
[Feed-Forward Network] (768 → 3072 → 768)
    ↓
[Add & Normalize]
    ↓
Output Vector
```

### Dimensões do GPT-2 Small
| Parâmetro | Valor |
|-----------|-------|
| Embedding dimension | 768 |
| Context window | 1024 tokens |
| Attention heads | 12 |
| Layers (blocks) | 12 |
| FFN inner dimension | 3072 (4x) |
| Vocabulary size | 50,000 tokens |

---

## 🧩 Masked Self-Attention

### O Problema
- Language model não pode "ver o futuro"
- Durante treino, precisa predizer próximo token
- Se pudesse ver tokens futuros, "trairia"

### A Solução: Masking
1. Calcular scores Q·K^T normalmente
2. **Aplicar máscara triangular** (-∞ para posições futuras)
3. Softmax normaliza os scores
4. Multiplica por V

### Exemplo Visual
```
Sequência: "robot must obey orders"
Posição 1 ("robot"): atenção 100% em "robot"
Posição 2 ("must"): atenção ~48% "robot", ~52% "must"
Posição 3 ("obey"): atenção distribuída nas 3 palavras anteriores
...
```

### Eficiência em Inferência
- Durante inferência, GPT-2 cacheia Key e Value vectors
- Não recalcula para tokens já processados
- Apenas processa o novo token

---

## 🔄 Processo Detalhado do Self-Attention

### Passos
1. **Criar Q, K, V**: Multiplicar input pela matriz de pesos
2. **Split em heads**: 12 heads, cada um com 64 dims (768/12)
3. **Score**: Q·K^T para cada head
4. **Apply mask**: -∞ para posições futuras
5. **Softmax**: Normalizar scores
6. **Weighted sum**: Scores × Values
7. **Concat heads**: Reunir resultados
8. **Project**: Multiplicar por W_O

### Matrizes de Pesos por Bloco
```
Atenção:
- W_Q, W_K, W_V (768 × 2304 cada, para Q, K, V combinados)
- W_O (768 × 768)

FFN:
- W_1 (768 × 3072)
- W_2 (3072 × 768)

Layer Norm: γ, β (768 cada)
```

### Contagem de Parâmetros (GPT-2 Small)
```
Embeddings:
- Token embedding: 50,000 × 768 = 38,400,000
- Position embedding: 1024 × 768 = 786,432

Per Block (x12):
- Attention: 768 × 2304 × 2 + 768 × 768 = 2,359,296 per layer
- FFN: 768 × 3072 + 3072 × 768 = 4,718,592 per layer
- Layer norms: ~3,072 per layer
- Total per block: ~7M parameters

Total: ~124M parameters
```

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Decoder-Only** | Arquitetura que elimina encoder, usa apenas masked self-attention |
| **Masked Self-Attention** | Attention que não pode ver tokens futuros (triangular mask) |
| **Auto-regressão** | Gera token a token, alimentando output como próximo input |
| **KV Cache** | Otimização em inferência que reusa Key/Value de tokens anteriores |
| **Top-k Sampling** | Considera top-k palavras, não apenas a mais provável |
| **Positional Encoding** | Adiciona informação posicional antes dos transformer blocks |

---

## 🔗 Aplicações Além de Language Modeling

### Machine Translation
- Decoder-only pode fazer tradução
- Input: texto fonte + [separator] → Output: tradução

### Summarization
- Treinar em artigos Wikipedia → resumos
- Pre-train em LM, fine-tune em sumarização

### Transfer Learning
- Pre-train em LM massivo
- Fine-tune para tarefas específicas
- Melhor que encoder-decoder em dados limitados

### Music Generation
- Music Transformer usa mesma arquitetura
- Trata música como "sequência de tokens"

---

## 📝 Diferenças Detalhadas: BERT vs GPT-2

| Aspecto | BERT | GPT-2 |
|---------|------|-------|
| **Arquitetura** | Encoder-only | Decoder-only |
| **Attention** | Bidirectional (não masked) | Unidirectional (masked) |
| **Objetivo de treino** | Masked LM + Next Sentence Prediction | Language Modeling (próxima palavra) |
| **Contexto** | Vê todo o contexto | Vê apenas passado |
| **Use case** | Understanding tasks | Generation tasks |
| **Fine-tuning** | Adiciona classificação layer | Prompt engineering ou fine-tune |

---

## 🎯 Notas Pessoais

- Excelente visualização de como masked self-attention funciona
- Clarifica diferença entre encoder, decoder, e decoder-only
- KV cache é otimização crucial para inferência eficiente
- Escala de parâmetros: 124M → 1.5B (original GPT-2)
- Próximo: entender RoPE (positional encoding moderno)

---

## 🎯 Próxima Fonte

Ler **"RoFormer: Rotary Position Embedding"** para entender positional encoding moderno.