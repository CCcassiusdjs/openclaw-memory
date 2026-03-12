# The Illustrated Transformer - Jay Alammar

**Source ID:** 002
**Type:** Blog Article (Illustrated Guide)
**Author:** Jay Alammar
**URL:** https://jalammar.github.io/illustrated-transformer/
**Read Date:** 2026-03-12

---

## 📖 Summary

This is a foundational visual guide to understanding the Transformer architecture, widely cited in academia (Stanford, Harvard, MIT, CMU courses). It breaks down the "Attention Is All You Need" paper into intuitive visual explanations with step-by-step walkthroughs.

### Core Value Proposition
- Visual explanations of transformer architecture
- Intuitive understanding of self-attention mechanism
- Clear matrix-level calculations
- Foundation for understanding modern LLMs

---

## 🏗️ Architecture Overview

### High-Level Structure
The Transformer consists of two main components:
1. **Encoder stack** - Processes input sequence
2. **Decoder stack** - Generates output sequence

Each stack contains N identical layers (paper uses N=6).

### Encoder Structure
Each encoder has two sub-layers:
1. **Self-Attention layer** - Allows encoder to look at other words while encoding
2. **Feed-Forward Network** - Applied independently to each position

### Decoder Structure
Each decoder has three sub-layers:
1. **Self-Attention layer** - Masked to prevent attending to future positions
2. **Encoder-Decoder Attention** - Focuses on relevant parts of input
3. **Feed-Forward Network** - Same as encoder

---

## 🔑 Key Concepts Learned

### 1. Self-Attention Mechanism

**Intuition:**
- When processing a word, the model looks at other words for context
- Example: "The animal didn't cross the street because it was too tired"
- "it" needs to associate with "animal" - self-attention enables this

**Calculation Steps:**
```
For each word in input:
1. Create Query (Q), Key (K), Value (V) vectors
   - Q = X × WQ (query weights)
   - K = X × WK (key weights)
   - V = X × WV (value weights)

2. Calculate attention scores
   - Score = Q · K^T (dot product)

3. Scale scores
   - Score = Score / √dk (stability)

4. Apply softmax
   - Weights = softmax(Score)

5. Weighted sum
   - Output = Weights × V
```

**Matrix Form:**
```
Attention(Q, K, V) = softmax(QK^T / √dk) × V
```

### 2. Multi-Head Attention

**Purpose:**
1. **Multiple representation subspaces** - Different heads learn different patterns
2. **Focus on different positions** - Each head can attend to different parts

**Implementation:**
- Paper uses 8 attention heads
- Each head has its own Q/K/V weight matrices
- Outputs are concatenated and projected

**Why multiple heads?**
- Single head might focus only on the word itself
- Multiple heads can capture different relationships
- Example: One head focuses on "animal", another on "tired" for "it"

### 3. Positional Encoding

**Problem:** Transformers have no inherent sense of position (unlike RNNs)

**Solution:** Add positional encoding vectors to input embeddings

**Pattern:**
```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

**Benefits:**
- Model learns position information
- Can generalize to longer sequences than training
- Sine/cosine pattern creates unique encodings

### 4. Residual Connections & Layer Normalization

**Architecture Pattern:**
```
x = LayerNorm(x + Sublayer(x))
```

Every sub-layer has:
1. Residual connection (add input to output)
2. Layer normalization (stabilize training)

### 5. Decoder Details

**Masked Self-Attention:**
- Future positions masked (set to -∞ before softmax)
- Prevents decoder from "cheating" by looking ahead

**Encoder-Decoder Attention:**
- Queries come from previous decoder layer
- Keys and Values come from encoder output
- Allows decoder to focus on relevant input parts

### 6. Output Generation

**Final Layers:**
1. **Linear layer** - Projects to vocabulary size (logits vector)
2. **Softmax** - Converts to probability distribution

**Training:**
- Compare output distribution with target (one-hot encoded)
- Loss function: Cross-entropy / KL divergence
- Backpropagation to update weights

---

## 📊 Dimensions & Hyperparameters

### Paper Defaults (Transformer Base)
| Component | Dimension |
|-----------|-----------|
| Model dimension (d_model) | 512 |
| Feed-forward dimension | 2048 |
| Attention heads | 8 |
| Key/Value dimension | 64 |
| Encoder layers | 6 |
| Decoder layers | 6 |

### Dimension Flow
```
Input: [batch, seq_len]
  ↓ Embedding
Embeddings: [batch, seq_len, 512]
  ↓ Positional Encoding
Encoded: [batch, seq_len, 512]
  ↓ Self-Attention (multi-head)
Attention Output: [batch, seq_len, 512]
  ↓ Feed-Forward
FFN Output: [batch, seq_len, 512]
  ↓ Linear (final)
Logits: [batch, seq_len, vocab_size]
```

---

## 🎯 Key Insights

### Why Transformers Work
1. **Parallelization** - No sequential processing like RNNs
2. **Long-range dependencies** - Self-attention connects any two positions
3. **Gradient flow** - Residual connections enable deep networks
4. **Scalability** - Architecture scales well with compute and data

### Computational Complexity
| Layer Type | Complexity | Operations |
|------------|------------|------------|
| Self-Attention | O(n² · d) | Q·K^T, then softmax |
| Feed-Forward | O(n · d²) | Two linear layers |
| Memory | O(n · d + n²) | Storing attention weights |

### Limitations
- **Quadratic attention** - O(n²) memory for sequence length n
- **Position encoding** - Fixed maximum sequence length (original)
- **No recurrence** - Harder to capture some sequential patterns

---

## 🔗 Related Resources

### Follow-up Works
- **LLM-Book.com** - Updated book chapter on modern Transformers
- **The Illustrated GPT-2** - Next in the series
- **The Illustrated BERT** - Encoder-only variant

### Implementations
- **Tensor2Tensor** - Official TensorFlow implementation
- **Harvard NLP** - Annotated PyTorch implementation
- **Hugging Face Transformers** - Modern library

### Courses Using This Guide
- Stanford CS224N
- Harvard Machine Learning
- MIT Deep Learning
- CMU Machine Learning

---

## 📝 Modern Updates (2025)

The original guide has been expanded into a book chapter covering:
- Multi-Query Attention (MQA)
- Grouped-Query Attention (GQA)
- RoPE Positional Embeddings
- Flash Attention optimizations
- Modern architecture variants

---

## 🎓 Concepts to Explore Further

1. **Flash Attention** - Memory-efficient attention implementation
2. **Sparse Attention** - Reducing O(n²) complexity
3. **Linear Attention** - Alternative attention formulations
4. **Cross-Attention** - Encoder-decoder attention details
5. **Attention Visualization** - Interpretability tools

---

**Relevância:** ★★★★★ (Essential Foundation)
**Status:** `completed`
**Reading Time:** ~1 hour for full understanding