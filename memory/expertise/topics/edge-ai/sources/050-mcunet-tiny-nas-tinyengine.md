# MCUNet: Tiny Deep Learning on IoT Devices (MIT HAN Lab)

**Source:** https://hanlab.mit.edu/projects/mcunet
**Type:** Research Project (MIT HAN Lab)
**Date:** NeurIPS 2020
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

MCUNet is a framework that jointly designs efficient neural architecture (TinyNAS) and lightweight inference engine (TinyEngine), enabling ImageNet-scale inference on microcontrollers. It's the first to achieve >70% ImageNet top-1 accuracy on commercial MCUs with significantly reduced memory footprint.

## Key Innovation

### System-Algorithm Co-Design
MCUNet jointly optimizes:
1. **TinyNAS** - Neural architecture search for tiny memory constraints
2. **TinyEngine** - Memory-efficient inference library

### The Challenge
- MCU memory is 2-3 orders of magnitude smaller than mobile phones
- Typical SRAM: 256KB - 1MB
- Typical Flash: 1MB - 2MB
- Existing methods reduce model size, but not activation size

## TinyNAS: Two-Stage Neural Architecture Search

### Stage 1: Search Space Optimization
- Optimizes search space to fit resource constraints
- Handles diverse constraints:
  - Device memory
  - Latency requirements
  - Energy budgets
  - Memory limitations

### Stage 2: Network Specialization
- Specializes network architecture in optimized search space
- Low search cost
- Automatic constraint handling

## TinyEngine: Memory-Efficient Inference Library

### Key Features
- Memory scheduling based on overall network topology
- Not layer-wise optimization
- Reduces memory usage by **3.4x**
- Accelerates inference by **1.7-3.3x**

### Comparison with Alternatives

| Framework | Memory Usage | Inference Speed |
|-----------|-------------|-----------------|
| TF-Lite Micro | Baseline | 1x |
| CMSIS-NN | ~1x | 1.5x |
| TinyEngine | **3.4x less** | **1.7-3.3x** |

## Experimental Results

### ImageNet on MCU
- **First** to achieve >70% ImageNet top-1 accuracy on commercial microcontroller
- Uses 3.5x less SRAM than quantized MobileNetV2
- Uses 5.7x less Flash than ResNet-18

### Visual Wake Words
- State-of-the-art accuracy
- **2.4-3.4x faster** than MobileNetV2
- **3.7-4.1x smaller peak SRAM** than ProxylessNAS

### Audio Wake Words
- Similar improvements in efficiency
- Real-time inference on MCUs

## Key Takeaways

1. **Co-design is Essential** - Joint architecture + inference engine optimization
2. **Memory-Aware Search** - NAS must consider memory constraints
3. **Activation Memory** - Critical bottleneck for MCUs (not just model size)
4. **ImageNet-Scale** - First to run full ImageNet on commercial MCUs
5. **Always-On ML** - Enables continuous inference on battery-powered devices

## Related Topics

- Neural Architecture Search (NAS)
- Memory-efficient inference
- TinyML deployment
- Model compression for edge
- MCU optimization techniques