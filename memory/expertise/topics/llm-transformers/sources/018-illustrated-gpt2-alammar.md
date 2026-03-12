# The Illustrated GPT-2 - Jay Alammar

**Source ID:** 018
**Type:** Blog Article (Illustrated Guide)
**Author:** Jay Alammar
**URL:** https://jalammar.github.io/illustrated-gpt2/
**Read Date:** 2026-03-12

---

## 📖 Summary

Visual guide explaining GPT-2's architecture as a decoder-only transformer. The article breaks down how autoregressive language models work, explaining masked self-attention and the evolution from the original transformer.

### Core Value Proposition
- Visual explanation of decoder-only transformers
- Detailed breakdown of masked self-attention
- Understanding autoregressive generation
- Foundation for understanding GPT-3, GPT-4, and modern LLMs

---

## 🔑 Key Concepts Learned

### 1. Language Modeling Definition

A language model predicts the next token given previous tokens:
```
P(w_t | w_1, ..., w_{t-1})
```

GPT-2 is essentially a "next word prediction" feature scaled up massively.

### 2. Architecture Evolution

| Model | Architecture | Key Feature |
|-------|-------------|-------------|
| Original Transformer | Encoder-Decoder | Translation focus |
| BERT | Encoder-only | Bidirectional context |
| GPT-2 | Decoder-only | Autoregressive generation |
| Transformer-Decoder | Decoder-only | Language modeling |

**Key insight:** GPT-2 uses decoder-only blocks without the encoder-decoder attention layer.

### 3. Decoder-Only Block

```
Input → Embedding + Positional Encoding
     ↓
Masked Self-Attention
     ↓
Add & Norm
     ↓
Feed-Forward Network
     ↓
Add & Norm
     ↓ (x N layers)
```

### 4. Masked Self-Attention

**Critical difference from encoder attention:**
- Tokens can only attend to previous positions
- Future tokens are masked (set to -∞ before softmax)
- This enables autoregressive generation

```
Attention Mask:
Position 1: [1,    -∞,   -∞,   -∞  ]
Position 2: [0.5,  0.5,  -∞,   -∞  ]
Position 3: [0.33, 0.33, 0.33, -∞  ]
Position 4: [0.25, 0.25, 0.25, 0.25]
```

### 5. Autoregressive Generation

GPT-2 generates tokens sequentially:
1. Process input tokens
2. Predict next token probability distribution
3. Sample from distribution (top-k sampling)
4. Add sampled token to sequence
5. Repeat until EOS or max length

**Training:** Process entire sequences at once with masking
**Inference:** Process one token at a time, use previous K,V cache

---

## 📊 GPT-2 Model Sizes

| Variant | Parameters | Layers | d_model | Heads |
|---------|------------|--------|---------|-------|
| Small | 117M | 12 | 768 | 12 |
| Medium | 345M | 24 | 1024 | 16 |
| Large | 774M | 36 | 1280 | 20 |
| XL | 1.5B | 48 | 1600 | 25 |

---

## 🔬 Detailed Architecture

### Input Processing
1. **Tokenization:** BPE (Byte Pair Encoding)
2. **Embedding Lookup:** Token embedding matrix
3. **Positional Encoding:** Learned positional embeddings
4. **Combined:** Token embedding + positional embedding

### Self-Attention Process

**Step-by-step for each token:**
1. Multiply input by weight matrix W_attn → Q, K, V vectors
2. Split into multiple heads
3. Compute attention scores: Q · K^T
4. Scale: divide by √d_k
5. Apply mask (future positions = -∞)
6. Apply softmax
7. Multiply by V
8. Concatenate heads
9. Project with W_O

### Key-Value Caching

During inference:
- Store K and V vectors from previous tokens
- Only compute Q, K, V for new token
- Reuse cached K, V for earlier positions
- Dramatically speeds up generation

---

## 🎯 Applications Beyond Language Modeling

### Machine Translation
- Use encoder to process source language
- Use decoder to generate translation
- GPT-2 can be adapted for translation tasks

### Summarization
- Fine-tune on summarization datasets
- Generate summaries from articles

### Transfer Learning
- Pre-train on massive corpus
- Fine-tune for specific tasks

### Music Generation
- Treat music as sequence
- Apply same autoregressive approach

---

## 📈 GPT-2 vs BERT

| Feature | GPT-2 | BERT |
|---------|-------|------|
| Architecture | Decoder-only | Encoder-only |
| Attention | Masked (unidirectional) | Bidirectional |
| Generation | Autoregressive | Not generative |
| Use Case | Text generation | Understanding tasks |
| Pre-training | Next token prediction | Masked LM + NSP |

**Trade-off:** 
- GPT-2: Better for generation, worse for understanding tasks
- BERT: Better for understanding, can't generate

---

## 🔗 Key Insights

### Why Decoder-Only Works
1. **Simplicity:** Single stack of identical blocks
2. **Scalability:** Easy to stack more layers
3. **Generation:** Natural for autoregressive tasks
4. **Transfer:** Pre-train once, fine-tune for tasks

### Model Scale Impact
- Larger models capture more patterns
- Better few-shot performance
- More coherent long-form generation

---

## 🎓 Modern LLM Evolution

GPT-2 established the decoder-only paradigm that continues:
- **GPT-3** (175B) - Few-shot learning
- **GPT-4** - Multimodal capabilities
- **LLaMA** - Open-source decoder-only
- **Mistral** - Efficient decoder-only
- **Claude** - Constitutional AI on decoder-only

---

**Relevância:** ★★★★★ (Essential for Understanding Modern LLMs)
**Status:** `completed`
**Reading Time:** ~1.5 hours for full understanding