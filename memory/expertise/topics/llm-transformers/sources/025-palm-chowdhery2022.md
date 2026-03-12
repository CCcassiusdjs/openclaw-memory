# PaLM: Scaling Language Modeling with Pathways

**Source ID:** 025
**Type:** Research Paper (ArXiv)
**Authors:** Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, et al. (Google)
**URL:** https://arxiv.org/abs/2204.02311
**Published:** 2022
**Read Date:** 2026-03-12

---

## 📖 Summary

PaLM (Pathways Language Model) is a 540-billion parameter, densely activated Transformer language model that demonstrated continued benefits of scaling for few-shot learning. Trained on 6144 TPU v4 chips using Google's Pathways system, it achieved state-of-the-art results on hundreds of benchmarks.

### Core Contribution
- **540B parameter model** - 10x larger than previous dense models
- **Pathways system** - Efficient training across multiple TPU Pods
- **Breakthrough reasoning** - Outperforms fine-tuned models on multi-step reasoning
- **Human-level performance** - BIG-bench average human performance matched

---

## 🔑 Key Concepts Learned

### 1. Model Scale

| Model | Parameters | Training Data | Hardware |
|-------|------------|---------------|----------|
| PaLM 540B | 540B | 780B tokens | 6144 TPU v4 |
| GPT-3 | 175B | 300B tokens | - |
| Chinchilla | 70B | 1.4T tokens | - |

### 2. Architecture

- **Transformer decoder-only** - Same as GPT-3
- **Parallel attention + FFN** - Modified architecture for efficiency
- **SwiGLU activation** - Better than ReLU/GELU
- **Multi-query attention** - Reduced memory bandwidth

### 3. Training Infrastructure

**Pathways System:**
- Multi-TPU Pod training
- Data parallelism across Pods
- Efficient scaling to 6144 chips
- First large-scale use of Pathways

---

## 📊 Performance Results

### Breakthrough Tasks

| Task | Performance | Significance |
|------|-------------|--------------|
| Multi-step reasoning | Outperforms fine-tuned | Breakthrough |
| BIG-bench | Above human average | Human-level |
| Math word problems | State-of-the-art | Strong |
| Code generation | Competitive | Good |
| Translation | Competitive | Good |

### Scaling Observations

- **Discontinuous improvements** - Some tasks show steep gains at scale
- **Few-shot learning** - Strong performance without fine-tuning
- **Chain-of-thought** - Benefits significantly from scale

---

## 🔬 Key Insights

### 1. Scaling Benefits Continue

Performance continues improving at 540B parameters, suggesting:
- Optimal model size may be larger
- Scaling laws hold across orders of magnitude
- Emergent capabilities at scale

### 2. Emergent Capabilities

Some capabilities emerge only at large scale:
- Multi-step reasoning
- Chain-of-thought prompting
- Complex task decomposition
- Novel word usage

### 3. Efficiency Improvements

**Parallel Attention + FFN:**
```
Standard: Attention → Add&Norm → FFN → Add&Norm
PaLM: Attention || FFN → Add&Norm (both)
```

**SwiGLU Activation:**
```
SwiGLU(x) = Swish(xW_gate) ⊙ (xW_in)
```

---

## 📝 Key Takeaways

1. **Scale continues to improve performance** - No plateau at 540B
2. **Pathways enables efficient training** - Multi-pod scaling
3. **Emergent capabilities appear** - At scale, new abilities emerge
4. **Open research impact** - Demonstrated what's possible
5. **Infrastructure matters** - Training efficiency crucial

---

**Relevância:** ★★★★★ (Major Milestone in LLM Scaling)
**Status:** `completed`
**Reading Time:** Paper ~70 pages, Core concepts ~30 minutes