# A Survey of Model Compression Techniques: Past, Present, and Future (2025)

**Source:** https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1518965/full
**Type:** Academic Survey (Frontiers in Robotics and AI)
**Date:** February 2025
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

Comprehensive survey of model compression techniques from shallow networks (pre-2012) through deep models (2012-2022) to large models (2022-present). Covers quantization, pruning, low-rank decomposition, and knowledge distillation with historical context and future directions.

## Historical Evolution

### Three Eras of Model Compression

| Era | Period | Key Characteristics |
|-----|--------|---------------------|
| **Shallow Networks** | Before 2012 | Pruning for computational reduction |
| **Deep Models** | 2012-2022 | Quantization, deep compression |
| **Large Models** | 2022-present | LLM compression, extreme quantization |

### Shallow Network Era (Before 2012)

**Key Methods:**
- **Optimal Brain Damage (OBD)** - LeCun et al. (1989)
- **Optimal Brain Surgeon (OBS)** - Hassibi & Stork (1992)
- **Gaussian Synapse Networks** - Becerra et al. (2002)

**Characteristics:**
- Eliminate non-essential parameters
- Calculate second-order derivatives
- Suited for networks with <3 layers
- Retraining costs too high for modern deep networks

### Deep Model Era (2012-2022)

**Landmark Methods:**

| Method | Year | Innovation |
|--------|------|------------|
| **Deep Compression** | 2016 | Pruning + quantization + Huffman coding |
| **Binary Neural Networks** | 2016 | 1-bit weights and activations |
| **BinaryConnect** | 2015 | Binary weights during training |
| **XNOR-Net** | 2016 | Binary convolutions |
| **INT8 Standard** | 2018 | TensorFlow Lite, PyTorch, ONNX |

**Deep Compression Pipeline (Han et al., 2016):**
```
Pruning → Quantization Training → Huffman Coding
```

**Key Insight:** Training quantization groups weight parameters into clusters, each sharing a floating-point value.

### Large Model Era (2022-Present)

**LLM Compression Milestones:**

| Method | Model | Achievement |
|--------|-------|-------------|
| **oBERT** | BERT | 10x model reduction with <1% accuracy drop |
| **OPTQ** | GPT-175B | 3-4 bit quantization, 4 GPU hours |
| **TEQ** | LLMs | 3-4 bit with FP32 output precision |
| **AWQ** | LLMs | Activation-aware 4-bit quantization |
| **BitNet** | LLMs | 1-bit quantization, 90% memory reduction |

## Four Compression Methods

### 1. Quantization

**Definition:** Reduce precision of weights and activations (FP32 → INT8 or lower).

**Theory:**
- Quantization: Float → Fixed-point
- Dequantization: Fixed-point → Float
- Information loss in quantization, minimal in dequantization

**Bit Width Comparison:**

| Format | Bytes | Use Case |
|--------|-------|----------|
| FP32 | 4 | Training, high precision |
| FP16 | 2 | Mixed precision training |
| INT8 | 1 | Inference standard |
| INT4 | 0.5 | Compressed inference |
| INT2/INT1 | 0.25-0.125 | Extreme compression |

**Post-Training Static Quantization Results:**

| Model | Domain | INT8 Accuracy | FP32 Accuracy | Drop |
|-------|--------|---------------|---------------|------|
| ResNet50 v1.0 | Vision | 74.11% | 74.27% | -0.22% |
| MobileNet V3 | Vision | 76.72% | 76.75% | -0.03% |
| BERT large | NLP | 92.36% | 92.98% | -0.67% |
| YOLOv3 | Detection | 83.28% | 82.35% | +1.12% |

### 2. Pruning

**Definition:** Remove redundant parameters from network.

**Types:**
- **Unstructured** - Individual weight removal
- **Structured** - Channel/layer removal
- **Magnitude-based** - Remove smallest weights

**Key Methods:**
- Optimal Brain Damage (OBD)
- Optimal Brain Surgeon (OBS)
- Lottery Ticket Hypothesis
- Movement Pruning

### 3. Low-Rank Decomposition

**Definition:** Decompose large parameter tensors into smaller tensors.

**Methods:**
- SVD-based decomposition
- Tensor factorization
- CP decomposition
- Tucker decomposition

### 4. Knowledge Distillation

**Definition:** Train smaller network to replicate larger network's performance.

**Approaches:**
- **Response-based** - Match output logits
- **Feature-based** - Match intermediate features
- **Relation-based** - Match sample relationships

## Key Takeaways

1. **Evolution** - Compression techniques evolved with model complexity
2. **INT8 Standard** - 8-bit quantization is practical for most deployments
3. **Extreme Quantization** - 1-4 bit viable for large models
4. **Combined Methods** - Best results from combining techniques
5. **Hardware Matters** - Compression methods must consider hardware constraints

## Future Directions

- LLM-specific compression
- Hardware-aware compression
- Dynamic quantization
- Adaptive precision
- Mixed-precision inference

## Related Topics

- Quantization-aware training
- Post-training quantization
- Structured vs unstructured pruning
- Knowledge distillation for LLMs
- Hardware-aware neural architecture search