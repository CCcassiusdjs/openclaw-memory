# Edge AI - Key Concepts Summary

**Topic:** Edge AI & Edge Computing
**Status:** In Progress (Reading Phase)
**Last Updated:** 2026-03-12

---

## Core Definition

**Edge AI:** Deployment of AI models directly on edge devices (smartphones, IoT, embedded systems, edge servers) for local inference rather than cloud processing.

---

## The Optimization Triad

```
┌─────────────────────────────────────────────────────────────────┐
│                    EDGE AI OPTIMIZATION TRIAD                    │
├─────────────────┬─────────────────┬─────────────────────────────┤
│      DATA       │     MODEL       │           SYSTEM            │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ - Cleaning      │ - Pruning       │ - Framework Support         │
│ - Compression   │ - Quantization  │ - Hardware Acceleration     │
│ - Augmentation  │ - Distillation  │ - Runtime Optimization      │
│ - Selection     │ - Architecture  │ - Deployment Strategies     │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

---

## Key Concepts Learned

### 1. Edge AI vs Cloud AI

| Aspect | Edge AI | Cloud AI |
|--------|---------|----------|
| Processing | On-device | Remote servers |
| Latency | Low (real-time) | Higher (network) |
| Privacy | High (local) | Lower (transmission) |
| Bandwidth | Minimal | High |
| Offline | Yes | No |
| Cost | Device (one-time) | Cloud (recurring) |

### 2. Model Compression Techniques

| Technique | What It Does | Size Reduction | Accuracy Impact |
|-----------|--------------|----------------|-----------------|
| **Quantization** | FP32 → INT8/INT4 | 75-90% | <1-3% |
| **Pruning** | Remove redundant weights | 30-75% | Variable |
| **Knowledge Distillation** | Teacher→Student model | 40-60% | <3% |

### 3. Hardware Accelerators

| Hardware | Use Case | Power | Latency |
|----------|----------|-------|---------|
| **NPU** | Edge inference | Low | Real-time |
| **TPU** | Cloud training | High | Batch |
| **GPU** | General parallel | Medium | Variable |
| **FPGA** | Reconfigurable | Low-Medium | Low |

### 4. Edge Inference Frameworks

| Framework | Hardware | Key Feature |
|-----------|----------|-------------|
| **TensorFlow Lite (LiteRT)** | Mobile/Embedded | Post-training quantization |
| **ONNX Runtime** | Cross-platform | Universal format |
| **OpenVINO** | Intel hardware | Model optimizer |
| **TensorRT** | NVIDIA GPUs | INT8 optimization |
| **CoreML** | Apple devices | Neural Engine |

### 5. Federated Learning for Edge

- **Privacy by design:** Data never leaves device
- **Distributed training:** Model updates aggregated centrally
- **Cloud-Edge-End architecture:** Layered deployment
- **Key challenges:** Data heterogeneity, communication constraints, security

### 6. Edge AI Applications

| Domain | Use Case |
|--------|----------|
| **Healthcare** | Wearable monitoring, fall detection, diagnostics |
| **Manufacturing** | Quality control, predictive maintenance |
| **Autonomous Vehicles** | Real-time perception, sensor fusion |
| **Smart Cities** | Traffic management, public safety |
| **Industrial IoT** | Machine monitoring, anomaly detection |

### 7. Deployment Considerations

- **Hardware selection:** Memory determines model size
- **Model optimization:** Quantization, pruning, distillation
- **Framework choice:** Hardware-specific optimizations
- **Calibration:** Representative data for static quantization
- **Testing:** Benchmark on target hardware

---

## Key Sources Read

1. arXiv: Edge AI Evaluation of Model Compression (002)
2. arXiv: Optimizing Edge AI Triad Survey (003)
3. Ultralytics: Edge AI Applications (004)
4. NVIDIA: Jetson LLM/VLM Deployment (005)
5. Ultralytics: Pruning & Quantization Guide (006)
6. Intel: OpenVINO Overview (007)
7. MDPI: Federated Learning Architectures (008)
8. Wevolver: NPU vs TPU Comparison (009)
9. Medium: Model Compression Techniques (010)
10. ONNX Runtime: Inference Overview (011)
11. Edge Impulse: Platform Overview (012)

---

## Questions to Explore

1. How does quantization-aware training compare to post-training quantization?
2. What are the trade-offs between structured vs unstructured pruning?
3. How does federated learning handle non-IID data distributions?
4. What are the practical differences between Edge TPU and Jetson for edge AI?
5. How can LLMs be effectively deployed on edge devices?

---

## Practical Skills to Develop

1. Convert PyTorch models to ONNX and optimize for edge
2. Implement quantization on a YOLO model
3. Deploy a model on Jetson Nano/Orin
4. Train a TinyML model with Edge Impulse
5. Compare TensorRT vs OpenVINO performance on Intel hardware

---

## Next Topics to Study

- [ ] TinyML for microcontrollers
- [ ] Model optimization for specific hardware (NPU, Edge TPU)
- [ ] LLM quantization techniques (GPTQ, AWQ)
- [ ] Split computing for edge-cloud hybrid
- [ ] Edge AI security considerations

---

## References

- bibliography.md: Complete source list
- sources/: Detailed source notes
- progress.json: Reading progress tracker