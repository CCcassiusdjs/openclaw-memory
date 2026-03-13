# Quantization and Pruning Mechanics for Edge AI

**Source:** Medium - "How Quantization and Pruning Actually Work and Why They Matter for Edge AI"
**URL:** https://medium.com/@thekzgroupllc/how-quantization-and-pruning-actually-work-and-why-they-matter-for-edge-ai-8ee7a239466f
**Author:** TheKzGroup LLC
**Date:** November 2025
**Relevance:** ⭐⭐⭐⭐

---

## Summary

Technical deep-dive into the mechanics of quantization and pruning, explaining how these techniques compress neural networks for edge deployment without losing intelligence.

---

## Key Concepts

### Why Edge AI Needs Smaller Models
- Edge devices (phones, drones, IoT) have limited compute and memory
- A 7B parameter model needs dozens of GB in full precision
- Compression makes AI usable on-device without retraining from scratch

---

## Quantization: Turning Floats into Integers

### Core Mechanism
- Replace 32-bit floating-point (FP32) with smaller integers (INT8, INT4, INT2)
- Each weight stored as: `weight = q_int × scale_factor`
- Scale factor (s) unique per layer, block, or channel

### Example: 4-bit Quantization
```
FP32 weight: 0.7534
INT4 range: -8 to +7 (8 values)
Quantized: q_int = 6, scale = 0.125
Reconstructed: 6 × 0.125 = 0.75 (close approximation)
```

### Size Reduction
- **FP32 → INT8**: 4× smaller
- **FP32 → INT4**: 8× smaller
- **70B model**: 280GB → 35GB (INT4, fits single GPU)

### Uniform Affine Quantization
Most common approach used in PyTorch, TensorRT, BitsAndBytes:
- Integer codes + per-layer scale factors
- Reconstructs approximate floats during inference
- Loses fine-grained variation, preserves structure

---

## Weight Sharing & Lookup Tables

### Vector Quantization (VQ)
- Multiple weights share same value in codebook
- Store small table of common values (e.g., 256 entries)
- Each weight stores index into table
- 32-bit weights → 8-bit indices = 4× reduction

### Used In
- MobileNet optimization
- EdgeTPU models
- K-means weight clustering

---

## Pruning: Cutting Redundant Weights

### Two Major Approaches

| Type | Method | Pros | Cons |
|------|--------|------|------|
| **Unstructured** | Zero out low-magnitude weights | High compression | Irregular memory access, less hardware-friendly |
| **Structured** | Remove entire channels/heads/layers | Hardware-efficient | Requires careful retraining |

### Key Insight
Most deep networks are over-parameterized → many weights barely affect outputs → removing them improves speed and generalization (reduces noise)

### Iterative Pruning Process
1. Train model to convergence
2. Remove lowest-magnitude weights
3. Fine-tune to recover accuracy
4. Repeat for higher compression

---

## Quantization + Pruning in Practice

### PyTorch Example
```python
# Dynamic Quantization
from torch.ao.quantization import quantize_dynamic
quantized_model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

# Pruning
import torch.nn.utils.prune as prune
prune.l1_unstructured(model.fc, name='weight', amount=0.3)
```

### Typical Results
- **5× to 10× model size reduction**
- **90-95% accuracy maintained**
- Combined with frameworks: AWQ, GPTQ, SparseGPT

---

## Edge AI Benefits

Quantized and pruned networks enable:
- ✅ Inference on CPUs, mobile NPUs, microcontrollers
- ✅ **70% energy reduction**
- ✅ Private, offline AI (no cloud needed)
- ✅ Millisecond response times

### Real-World Examples
| Model | Application | Edge Deployment |
|-------|-------------|------------------|
| Whisper Tiny / DistilWhisper | Speech recognition | Mobile devices |
| Mobile SAM | Vision segmentation | Embedded systems |
| TinyLlama / Phi-3 Mini | On-device reasoning | Phones, IoT |

---

## Advanced Research Directions

1. **Mixed-precision quantization**: Adaptive bit width per layer
2. **Dynamic sparsity**: Real-time pruning during inference
3. **Hardware-aware training**: Models co-designed for NPUs

---

## Notable Quotes

> "Quantization and pruning are not hacks, they're engineering disciplines that transform neural networks into deployable systems. They make intelligence portable, efficient, and scalable, moving AI out of the cloud and into the real world."

> "Most deep networks are over-parameterized—many weights barely change outputs. Removing them can make networks faster and generalize better."

---

## Key Takeaways

1. **Quantization** reduces precision (FP32 → INT8/INT4) with minimal accuracy loss
2. **Pruning** reduces quantity of weights by removing low-importance connections
3. Both techniques can be **combined** for 5-10× compression
4. **Structured pruning** is hardware-friendly; **unstructured** needs special support
5. Edge AI depends on these techniques for real-world deployment

---

## Cross-References

- Related to: [[005-quantization-techniques]] (fundamentals)
- Related to: [[006-pruning-methods]] (pruning methods)
- Related to: [[007-knowledge-distillation]] (distillation)
- Related to: [[047-low-bit-quantization-llm-edge-microsoft]] (low-bit for LLMs)