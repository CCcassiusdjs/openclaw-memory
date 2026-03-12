# ONNX Runtime Inference Overview

**Source:** ONNX Runtime Documentation
**Authors:** Microsoft
**Year:** 2025
**Category:** Cross-Platform Inference Framework
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for edge deployment)

---

## Summary

ONNX Runtime provides a high-performance, cross-platform solution for inference of ML models from various frameworks (PyTorch, TensorFlow, Hugging Face) on different hardware platforms (CPU, GPU, NPU, mobile).

---

## Core Benefits

| Benefit | Description |
|---------|-------------|
| **Performance** | Improved latency, throughput, memory utilization |
| **Hardware Acceleration** | Device-specific accelerators |
| **Cross-Framework** | Common interface for PyTorch, TensorFlow models |
| **Cross-Language** | Python, C++, C#, C, Java, JavaScript |
| **Cross-Platform** | Cloud, edge, mobile, browser |

---

## ONNX Runtime Mobile

### Supported Platforms

| Platform | Languages |
|----------|-----------|
| Android | Java, Kotlin, C, C++ |
| iOS | Swift, Objective-C, C, C++ |
| React Native | JavaScript |
| MAUI/Xamarin | C# |

### Example Applications

| App | Description |
|-----|-------------|
| **Image Classification** | Real-time object classification from camera |
| **Speech Recognition** | Transcribe speech from device audio |
| **Object Detection** | Detect objects with bounding boxes |
| **Question Answering** | NLP models with pre/post processing |

---

## ONNX Runtime Web

### Features
- Run ML models in browsers
- Cross-platform JavaScript
- No additional libraries/drivers

### Example Applications

| App | Description |
|-----|-------------|
| **Image Classification** | Web app template with VueJS |
| **Speech Recognition** | Whisper tiny.en in browser |
| **NLP** | BERT models in Excel functions |

---

## Key Features for Edge Deployment

1. **Universal Format:** ONNX as intermediate representation
2. **Graph Optimizations:** Constant folding, operator fusion
3. **Execution Providers:** CUDA, TensorRT, OpenVINO, CoreML
4. **Quantization Support:** INT8, FP16 optimizations
5. **Model Compatibility:** PyTorch, TensorFlow, scikit-learn

---

## Deployment Workflow

```
┌─────────────────────────────────────────────────────┐
│                 TRAINING FRAMEWORK                  │
│        PyTorch / TensorFlow / HuggingFace          │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                  EXPORT TO ONNX                      │
│    torch.onnx.export / tf2onnx / skl2onnx          │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              ONNX RUNTIME INFERENCE                 │
│     Python / C++ / C# / Java / JavaScript           │
│     CPU / GPU / NPU / Mobile / Browser             │
└─────────────────────────────────────────────────────┘
```

---

## Execution Providers

| Provider | Hardware | Use Case |
|----------|----------|----------|
| **CPU** | Intel, AMD, ARM | Default fallback |
| **CUDA** | NVIDIA GPU | GPU acceleration |
| **TensorRT** | NVIDIA GPU | Optimized inference |
| **OpenVINO** | Intel CPU/GPU/VPU | Intel optimization |
| **CoreML** | Apple devices | iOS/macOS |
| **NNAPI** | Android | Android neural API |
| **DirectML** | Windows GPU | DirectX acceleration |

---

## Next Steps

- [ ] Convert a PyTorch model to ONNX
- [ ] Test ONNX Runtime on different hardware
- [ ] Compare performance with native PyTorch
- [ ] Explore quantization with ONNX Runtime