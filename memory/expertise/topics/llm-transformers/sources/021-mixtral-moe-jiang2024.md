# Mixtral of Experts (Sparse Mixture of Experts)

**Source ID:** 021
**Type:** Research Paper (ArXiv)
**Authors:** Albert Q. Jiang, Alexandre Sablayrolles, et al. (Mistral AI)
**URL:** https://arxiv.org/abs/2401.04088
**Published:** 2024
**Read Date:** 2026-03-12

---

## 📖 Summary

Introduces Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language model that achieves the performance of a 47B model while only using 13B active parameters during inference. Each layer has 8 feedforward blocks (experts), with a router selecting 2 experts per token.

### Core Contribution
- **Sparse activation:** 47B total parameters, 13B active per token
- **Better than Llama 2 70B:** On mathematics, code, multilingual
- **Matches GPT-3.5:** Across benchmarks
- **Apache 2.0 license:** Open weights

---

## 🔑 Key Concepts Learned

### 1. Mixture of Experts (MoE) Architecture

```
Standard Transformer Block:
  Attention → Add&Norm → FFN → Add&Norm

MoE Transformer Block:
  Attention → Add&Norm → MoE Layer → Add&Norm

MoE Layer:
  Router network selects top-k experts from n experts
  For each token: select k=2 experts from n=8
  Combine outputs: y = Σ router_weight_i × Expert_i(x)
```

### 2. Mixtral Specifics

| Component | Value |
|-----------|-------|
| Total Parameters | 47B |
| Active Parameters | 13B per token |
| Experts per Layer | 8 |
| Experts Selected | 2 (top-k) |
| Context Length | 32k tokens |
| Architecture | Same as Mistral 7B |

### 3. Router Network

```
For each token x:
1. Router computes scores: s(x) = Softmax(Top-k(G(x)))
2. Select top-k experts (k=2 in Mixtral)
3. Compute expert outputs: E_i(x)
4. Combine: y = Σ s_i(x) × E_i(x)

Where:
  G(x) = Learned gating function
  Top-k selects k highest scores
```

---

## 📊 Performance Results

### vs. Llama 2 70B

| Benchmark | Mixtral 8x7B | Llama 2 70B |
|-----------|--------------|-------------|
| Mathematics | **Higher** | Lower |
| Code Generation | **Higher** | Lower |
| Multilingual | **Higher** | Lower |
| General | **On-par** | Baseline |

### vs. GPT-3.5

| Benchmark | Mixtral 8x7B | GPT-3.5 |
|-----------|--------------|---------|
| MT-Bench | Comparable | Baseline |
| Human Eval | **Higher** | Lower |

### Mixtral 8x7B Instruct

| Model | Score |
|-------|-------|
| Mixtral 8x7B Instruct | **Top** |
| GPT-3.5 Turbo | Lower |
| Claude-2.1 | Lower |
| Gemini Pro | Lower |
| Llama 2 70B Chat | Lower |

---

## 🔬 Key Insights

### 1. Sparse Activation Efficiency

**Compute Comparison:**
| Model | Total Params | Active Params | FLOPs |
|-------|-------------|---------------|-------|
| Llama 2 70B | 70B | 70B | 100% |
| Mixtral 8x7B | 47B | 13B | ~19% |

Mixtral uses ~19% of FLOPs per token compared to dense 70B model.

### 2. Expert Specialization

Studies show experts specialize:
- Some experts focus on specific domains
- Others are more general-purpose
- Routing patterns emerge during training

### 3. Inference Efficiency

**Throughput Benefits:**
- Lower latency per token (13B active vs 70B)
- Better throughput for batched inference
- Memory: Need to load all 47B, but compute is sparse

### 4. Training Efficiency

**Training Cost:**
- Similar to training a 47B dense model
- Inference is much cheaper
- Good trade-off for deployed models

---

## 🎯 Architecture Details

### MoE Layer Structure

```
Input x
   ↓
Router Network → Scores for 8 experts
   ↓
Select top-2 experts
   ↓
Expert_1(x), Expert_2(x)
   ↓
Weighted sum: w1*E1(x) + w2*E2(x)
   ↓
Output y
```

### Expert Design

Each expert is a feedforward network:
```
Expert(x) = W2(activation(W1(x)))

Where:
  W1: d_model → d_ff (expansion)
  W2: d_ff → d_model (projection)
  d_ff = 4 × d_model (typical)
```

### Router Implementation

```
Router(x) = Softmax(Linear(x))

Outputs: [score_1, ..., score_8]
Select top-k (k=2)
Normalize scores for selected experts
```

---

## 📈 Comparison with Other MoE Models

| Model | Year | Total | Active | Experts | Top-k |
|-------|------|-------|--------|---------|-------|
| Switch Transformer | 2021 | 1.6T | 1T | 2048 | 1 |
| GLaM | 2021 | 1.2T | 96B | - | 2 |
| Mixtral 8x7B | 2024 | 47B | 13B | 8 | 2 |

---

## 🔗 Modern Usage

### Deployment Considerations

| Factor | Dense Model | MoE Model |
|--------|-------------|-----------|
| Memory | Lower | Higher (load all experts) |
| Compute | Higher | Lower (sparse activation) |
| Latency | Higher | Lower |
| Throughput | Lower | Higher |

### Load Balancing

MoE training requires load balancing:
- Encourage equal expert utilization
- Auxiliary loss: L_balance = α × Σ_importance²
- Prevents router collapse (all tokens to one expert)

---

## 📝 Key Takeaways

1. **Sparse MoE scales efficiently** - 47B model at 13B compute cost
2. **Better than larger dense models** - Outperforms Llama 2 70B
3. **Expert routing learns specialization** - Domain-specific experts emerge
4. **Open weights democratize access** - Apache 2.0 license
5. **Foundation for modern MoE models** - Grok, DeepSeek, etc. follow similar approach

---

## 🎓 Follow-up Developments

### Mixtral 8x22B (2024)
- Larger variant: 8 experts × 22B each
- 141B total parameters, 39B active
- Better performance across benchmarks

### Other MoE Models
- **DeepSeek-MoE:** Modified routing architecture
- **Grok-1:** 314B parameters MoE
- **Qwen-MoE:** MoE variants of Qwen models

---

**Relevância:** ★★★★★ (State-of-the-art MoE Architecture)
**Status:** `completed`
**Reading Time:** Paper ~20 pages, Core concepts ~30 minutes