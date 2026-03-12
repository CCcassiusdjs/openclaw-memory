# Model Compression Techniques: Quantization, Pruning & Distillation

**Source:** Medium (Amit Kharche)
**Year:** 2025
**Category:** Model Optimization Techniques
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for real-world deployment)

---

## Summary

Practical guide to model compression techniques for real-world AI deployment. Covers quantization, pruning, and knowledge distillation with code examples, benchmarks, and strategic business context.

---

## Why Model Compression Matters

### Business Benefits

| Benefit | Description |
|---------|-------------|
| **Speed** | Real-time UX, faster inference |
| **Cost** | Reduced cloud/compute costs |
| **Edge Enablement** | Deploy where connectivity is limited |
| **Sustainability** | Lower energy consumption |

### ROI Example
> "Deploying object detection on 10,000 POS systems. Compression can cut infrastructure costs by 40% while preserving model accuracy within 1%."

---

## Technique 1: Quantization

### Concept
Reduce precision of weights and activations (typically FP32 → INT8 or FP16).

### Types

| Type | Description | When |
|------|-------------|------|
| **Post-Training Dynamic** | On-the-fly quantization | Runtime |
| **Post-Training Static** | Calibrated quantization | Before deployment |
| **Quantization-Aware Training** | Integrated in training | During training |

### Code Example (PyTorch)
```python
import torch
from torchvision.models import resnet18
from torch.quantization import quantize_dynamic

model_fp32 = resnet18(pretrained=True)
model_fp32.eval()

model_int8 = quantize_dynamic(
    model_fp32,
    {torch.nn.Linear},
    dtype=torch.qint8
)

torch.save(model_int8.state_dict(), 'quantized_resnet18.pth')
```

### Benchmarks

| Model | Original | Quantized | Reduction |
|-------|----------|-----------|-----------|
| ResNet-50 | 25MB | 6.3MB | 75% (INT8) |
| MobileNet | 14MB | 3.5MB | 75% |

### Hardware-Aware Libraries

| Platform | Library |
|----------|---------|
| NVIDIA | TensorRT (FP16/INT8) |
| Intel | OpenVINO with calibration |
| Apple | CoreML INT8 |

---

## Technique 2: Pruning

### Concept
Remove low-importance weights, channels, filters, or neurons.

### Types

| Type | Description | Hardware-Friendly |
|------|-------------|-------------------|
| **Unstructured** | Remove individual weights | No |
| **Structured** | Remove entire channels/filters | Yes |
| **Global** | Prune across entire network | Varies |
| **Local** | Prune per-layer | Yes |

### Code Example (TensorFlow)
```python
import tensorflow_model_optimization as tfmot

prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude

pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
    initial_sparsity=0.0,
    final_sparsity=0.5,
    begin_step=2000,
    end_step=10000
)

model = ... # Your Keras model
pruned_model = prune_low_magnitude(model, pruning_schedule=pruning_schedule)
```

### Benchmarks

| Model | Reduction | Accuracy Impact |
|-------|-----------|-----------------|
| MobileNetV2 | 30% parameters | <1% drop |

### Tools

| Tool | Description |
|------|-------------|
| TensorFlow Model Optimization | Pruning utilities |
| PyTorch Pruning | Built-in pruning API |
| DeepSparse (Neural Magic) | Sparse inference |

### Cautions
- Retraining often required post-pruning
- Compatibility issues with unsupported sparse formats

---

## Technique 3: Knowledge Distillation

### Concept
Train a compact "student" model to mimic a larger "teacher" model's output (soft labels).

### Key Elements

| Element | Description |
|---------|-------------|
| **Teacher logits** | Soft probability distribution |
| **Temperature scaling** | Smooth probability gaps |
| **Loss blending** | Student vs label + student vs teacher |

### Code Example (PyTorch)
```python
def distillation_loss(student_logits, teacher_logits, labels, T=2.0, alpha=0.7):
    kd_loss = nn.KLDivLoss()(
        F.log_softmax(student_logits/T, dim=1),
        F.softmax(teacher_logits/T, dim=1)
    ) * (T*T)
    
    ce_loss = F.cross_entropy(student_logits, labels)
    
    return alpha * ce_loss + (1 - alpha) * kd_loss
```

### Examples

| Model | Size Reduction | Speed | Accuracy |
|-------|----------------|-------|----------|
| DistilBERT | 40% smaller | 60% faster | 97% of BERT-base |
| TinyYOLO | Smaller | Faster | Acceptable for mobile |

### Tools

| Tool | Description |
|------|-------------|
| Hugging Face Transformers | DistilBERT, TinyBERT, MobileBERT |
| PyTorch Distiller | Custom distillation |
| TensorFlow Distillation API | Built-in distillation |

---

## Combining Techniques for Maximum Efficiency

### Sequential Strategy

```
1. Distillation → Create small but accurate model
2. Pruning      → Reduce computation further
3. Quantization → Optimize for deployment
```

### Compatibility Matrix

| Combination | Order | Benefit |
|-------------|-------|---------|
| Distill → Prune → Quantize | Sequential | Maximum compression |
| Prune → Quantize | Two-stage | Moderate compression |
| Quantize only | Single-stage | Quick deployment |

---

## Real-World Applications

| Domain | Use Case | Compression Used |
|--------|----------|-----------------|
| **Mobile Apps** | On-device ML | All three |
| **Edge Devices** | IoT inference | Quantize + Prune |
| **Healthcare** | Diagnostics | Distillation |
| **Autonomous Vehicles** | Real-time perception | All three |
| **Enterprise** | Scalable AI services | All three |

---

## Best Practices

1. **Benchmark both accuracy and latency** post-compression
2. **Choose hardware-aware libraries** (TensorRT, OpenVINO, CoreML)
3. **Use observability tools** for drift detection (Arize, Fiddler, Evidently)
4. **Document trade-offs and failure cases** in testing reports

---

## Strategic ROI

| Metric | Impact |
|--------|--------|
| **Inference Cost** | 40-75% reduction |
| **Latency** | 50-90% improvement |
| **Model Size** | 60-95% reduction |
| **Accuracy** | <1-3% typical loss |

---

## Key Quote

> "Compression is no longer an afterthought. It's a strategic lever that transforms research-grade models into ROI-driving assets."

---

## Next Steps

- [ ] Implement distillation for a BERT model
- [ ] Benchmark pruning on MobileNetV2
- [ ] Test quantization on target hardware
- [ ] Combine all three for edge deployment