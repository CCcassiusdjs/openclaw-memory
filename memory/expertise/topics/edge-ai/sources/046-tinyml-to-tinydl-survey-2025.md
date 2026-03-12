# From Tiny Machine Learning to Tiny Deep Learning: A Survey (2025)

**Source:** https://arxiv.org/html/2506.18927v1
**Type:** Academic Survey (arXiv)
**Date:** June 2025
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

Comprehensive survey on the transition from TinyML to Tiny Deep Learning (TinyDL), covering 200+ sources through 2025. Addresses deploying deep learning models on severely resource-constrained hardware (microcontrollers with <1mW power, 32-512KB SRAM).

## Key Concepts

### TinyML vs TinyDL

| Aspect | TinyML | TinyDL |
|--------|--------|--------|
| **Focus** | Simple ML inference | Deep learning models |
| **Models** | Linear classifiers, decision trees | CNNs, RNNs, transformers |
| **Memory** | 32-512 KB SRAM | Similar constraints |
| **Power** | <1mW | <1mW |
| **Examples** | Keyword spotting, anomaly detection | Image classification, object detection |

### Hardware Constraints

| Constraint | Typical Range | Impact |
|------------|----------------|--------|
| **SRAM** | 32-512 KB | Runtime operations |
| **Flash** | <1-2 MB | Model storage |
| **Power** | mW to µW range | Battery/harvesting systems |
| **Clock Speed** | Tens to hundreds MHz | Compute throughput |
| **FPU** | Often absent | Requires quantization |

### Hardware Platforms

**Microcontrollers:**
- ARM Cortex-M series (M0, M4, M7)
- STM32 family
- ESP32 family

**Neural Accelerators:**
- Dedicated NPU chips
- Neuromorphic processors
- Processing-in-Memory (PIM)

### Model Compression Techniques

1. **Quantization**
   - FP32 → INT8/INT4/INT2
   - Quantization-aware training (QAT)
   - Post-training quantization (PTQ)

2. **Pruning**
   - Structured pruning
   - Unstructured pruning
   - Sparse model optimization

3. **Knowledge Distillation**
   - Teacher-student training
   - Attention transfer
   - Feature-based distillation

4. **Neural Architecture Search (NAS)**
   - MCUNet
   - TinyNAS
   - Hardware-aware optimization

### Architectural Innovations

**Lightweight Architectures:**
- MobileNet family
- EfficientNet-lite
- SqueezeNet
- Tiny-YOLO
- MCUNet variants

**Key Techniques:**
- Depthwise separable convolutions
- Inverted residuals
- Attention mechanisms for edge
- Efficient attention variants

### Software Toolchains

**Inference Frameworks:**
- TensorFlow Lite Micro
- PyTorch Mobile
- ONNX Runtime
- Apache TVM

**Compilers:**
- LLVM-based backends
- Hardware-specific compilers
- AutoML tools

**Deployment Tools:**
- Edge Impulse
- STM32Cube.AI
- NVIDIA TensorRT

## On-Device Learning

### Techniques for Edge Training
- Federated learning on MCUs
- Continual learning under memory constraints
- Transfer learning with frozen backbones
- Parameter-efficient fine-tuning (PEFT)

### Challenges
- Memory for gradients
- Catastrophic forgetting
- Energy efficiency
- Limited training data

## Applications

| Domain | Use Cases |
|--------|-----------|
| **Computer Vision** | Object detection, classification |
| **Audio Recognition** | Keyword spotting, voice commands |
| **Healthcare** | Wearable monitoring, diagnostics |
| **Industrial IoT** | Predictive maintenance, quality control |
| **Smart Home** | Occupancy detection, gesture recognition |
| **Agriculture** | Crop monitoring, pest detection |

## Benchmarking Framework

### Key Metrics
- Inference latency
- Memory usage (SRAM, Flash)
- Model size
- Energy efficiency (inferences/joule)
- Accuracy preservation

### Datasets
- ImageNet (scaled down)
- CIFAR-10/100
- Visual Wake Words
- Google Speech Commands
- Tiny ImageNet

## Future Directions

### Neuromorphic Computing
- Spiking neural networks
- Event-driven processing
- Ultra-low power inference

### Federated TinyDL
- Privacy-preserving distributed learning
- Communication-efficient aggregation
- Heterogeneous device coordination

### Edge-Native Foundation Models
- SLM architectures for edge
- Mobile-optimized transformers
- Quantized foundation models

### Domain-Specific Co-Design
- Hardware-aware NAS
- Application-specific accelerators
- Compiler-hardware optimization

## Key Takeaways

1. **Paradigm Shift** - From shallow ML to deep learning on MCUs
2. **Memory is Key** - Kilobyte-scale optimization is essential
3. **Co-Design Required** - Hardware, software, and model optimization together
4. **Real-Time Capability** - Sub-20ms latency achievable on MCUs
5. **Ecosystem Maturity** - Toolchains and frameworks are production-ready

## Related Topics

- Model quantization techniques
- Neural architecture search for edge
- Federated learning with TinyML
- Neuromorphic computing
- SLM deployment strategies