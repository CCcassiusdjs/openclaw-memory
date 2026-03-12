# The Transformer Family - Lilian Weng

**Source ID:** 024
**Type:** Blog Article (Technical Deep Dive)
**Author:** Lilian Weng
**URL:** https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/
**Read Date:** 2026-03-12

---

## 📖 Summary

Comprehensive technical deep dive into Transformer variants and improvements since the original paper. Covers architectural modifications for longer context, memory efficiency, and computational improvements.

### Core Value Proposition
- Mathematical formulations for all Transformer components
- Detailed coverage of attention span improvements
- Memory and computation optimization techniques
- Foundation for understanding modern LLM architectures

---

## 🔑 Key Concepts Covered

### 1. Notation Reference

| Symbol | Meaning |
|--------|---------|
| $d$ | Model dimension / hidden size |
| $h$ | Number of attention heads |
| $L$ | Sequence length |
| $\mathbf{X}$ | Input sequence $(L \times d)$ |
| $\mathbf{Q}, \mathbf{K}, \mathbf{V}$ | Query, Key, Value matrices |
| $a_{ij}$ | Attention score between query $i$ and key $j$ |
| $\mathbf{P}$ | Positional encoding matrix |

### 2. Attention Mechanisms

**Scaled Dot-Product Attention:**
$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}$$

**Multi-Head Attention:**
$$\text{MultiHead}(\mathbf{X}) = [\text{head}_1; ...; \text{head}_h]\mathbf{W}^O$$

### 3. Positional Encodings

| Type | Formula | Properties |
|------|---------|------------|
| Sinusoidal | $\sin/cos(position \times frequency)$ | Fixed, extrapolates |
| Learned | Embedding table | Flexible, fixed max length |
| Relative | $a_{ij}^{rel} = f(i-j)$ | Translation invariant |
| RoPE | Rotation matrix | Relative + absolute |

---

## 🏗️ Architecture Variants

### Vanilla Transformer

```
Encoder: Self-Attention → FFN → Add&Norm
Decoder: Masked Self-Attn → Cross-Attn → FFN → Add&Norm
```

### Key Improvements Covered

#### 1. Transformer-XL (Longer Context)

**Problem:** Fixed-length segments break information flow

**Solution:**
- Reuse hidden states from previous segments
- Relative positional encoding for consistency

$$\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)} = [\text{stop-gradient}(\mathbf{h}_{\tau}^{(n-1)}) \circ \mathbf{h}_{\tau+1}^{(n-1)}]$$

#### 2. Adaptive Attention Span

**Problem:** Different heads need different context lengths

**Solution:** Learnable mask function for each head

$$m_z(x) = \text{clamp}\left(\frac{1}{R}(R+z-x), 0, 1\right)$$

**Finding:** Lower layers need shorter spans; higher layers may use longer spans.

#### 3. Sparse Attention (Sparse Transformer)

**Problem:** $O(n^2)$ memory/compute for attention

**Solution:** Factorized attention patterns

- Strided attention (every k positions)
- Fixed attention (specific positions)
- Reduces to $O(n\sqrt{n})$ or $O(n \log n)$

#### 4. Image Transformer

**Problem:** Images have no natural order

**Solution:** Localized attention
- 1D: Flatten and use local windows
- 2D: Local rectangular neighborhoods

---

## 📊 Complexity Analysis

| Variant | Time | Memory | Context |
|---------|------|--------|---------|
| Vanilla | $O(n^2)$ | $O(n^2)$ | Fixed |
| Transformer-XL | $O(n^2)$ | $O(n^2)$ | Extended |
| Sparse | $O(n\sqrt{n})$ | $O(n\sqrt{n})$ | Longer |
| Longformer | $O(n)$ | $O(n)$ | Very long |

---

## 🔬 Deep Technical Insights

### 1. Relative Positional Encoding (Transformer-XL)

$$a_{ij}^{rel} = \underbrace{\mathbf{x}_i\mathbf{W}^q {\mathbf{W}_E^k}^T \mathbf{x}_j^T}_{\text{content-based}} + \underbrace{\mathbf{x}_i\mathbf{W}^q {\mathbf{W}_R^k}^T \mathbf{r}_{i-j}^T}_{\text{content-position}} + \underbrace{\mathbf{u} {\mathbf{W}_E^k}^T \mathbf{x}_j^T}_{\text{global content}} + \underbrace{\mathbf{v} {\mathbf{W}_R^k}^T \mathbf{r}_{i-j}^T}_{\text{global position}}$$

Key insight: Use relative position $(i-j)$ instead of absolute positions.

### 2. Adaptive Computation Time (ACT)

Dynamically decide computation steps:

$$N(t) = \min\left(\min\{n': \sum_{n=1}^{n'} h_t^n \geq 1-\epsilon\}, M\right)$$

- $h_t^n$: Halting probability at step $n$
- $\epsilon$: Threshold (e.g., 0.01)
- $M$: Maximum steps

### 3. Multi-Head Attention Implementation

```python
# Simplified multi-head attention
def multi_head_attention(Q, K, V, num_heads):
    d_model = Q.shape[-1]
    d_k = d_model // num_heads
    
    # Split into heads
    Q = Q.reshape(batch, seq, num_heads, d_k).transpose(1, 2)
    K = K.reshape(batch, seq, num_heads, d_k).transpose(1, 2)
    V = V.reshape(batch, seq, num_heads, d_k).transpose(1, 2)
    
    # Attention per head
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    attention = F.softmax(scores, dim=-1)
    output = torch.matmul(attention, V)
    
    # Concatenate heads
    output = output.transpose(1, 2).reshape(batch, seq, d_model)
    
    return output @ W_O
```

---

## 📚 Models Covered

| Model | Year | Key Innovation |
|-------|------|----------------|
| Vanilla Transformer | 2017 | Original architecture |
| Transformer-XL | 2019 | Segment-level recurrence |
| Adaptive Span | 2019 | Learnable context length |
| Sparse Transformer | 2019 | Sparse attention patterns |
| Image Transformer | 2018 | Localized attention |
| Longformer | 2020 | Local + global attention |
| Reformer | 2020 | LSH attention |
| Linformer | 2020 | Linear attention |

---

## 🎓 Key Takeaways

1. **Context length is critical** - Many improvements focus on extending context
2. **Memory is the bottleneck** - $O(n^2)$ limits applications
3. **Relative positions help** - More flexible than absolute encodings
4. **Sparse attention enables scale** - Trade-off between accuracy and efficiency
5. **Mathematical foundations matter** - Understanding attention mechanism is essential

---

## 🔗 Related Resources

- **The Illustrated Transformer** - Visual guide
- **Attention Is All You Need** - Original paper
- **Transformers from Scratch** - Implementation details
- **The Annotated Transformer** - Code with explanations

---

**Relevância:** ★★★★★ (Comprehensive Technical Reference)
**Status:** `completed`
**Reading Time:** Full article ~2 hours, Key concepts ~45 minutes