# AI Hardware Accelerators Comparison (NPU/TPU/VPU)

**Source:** Multiple sources (Gateworks, ThePurpleStruct, TechTarget)
**Date:** 2026-03-12
**Status:** read

---

## Overview

Comparison of specialized AI accelerators for edge and cloud inference workloads.

## Accelerator Types

| Type | Full Name | Primary Use Case | Performance |
|------|-----------|------------------|-------------|
| **NPU** | Neural Processing Unit | Edge inference, mobile | 1-50 TOPS |
| **TPU** | Tensor Processing Unit | Cloud training/inference | 90-420 TOPS |
| **VPU** | Vision Processing Unit | Computer vision, video | 1-10 TOPS |
| **GPU** | Graphics Processing Unit | Training, batch inference | 100-1000+ TOPS |
| **FPGA** | Field-Programmable Gate Array | Custom acceleration | Varies |

## NPU (Neural Processing Unit)

### Characteristics
- Integrated into SoCs (Snapdragon, Apple Silicon, MediaTek)
- Designed for **low-power inference**
- Optimized for neural network operations (convolutions, activations)
- Ideal for edge devices, mobile phones, IoT

### Key Features
| Aspect | NPU |
|--------|-----|
| Power | Very low (milliwatts) |
| Latency | Low (real-time) |
| Integration | SoC embedded |
| Use Case | Edge inference, mobile AI |

### Examples
- Arm Ethos-U85
- Qualcomm Hexagon
- Apple Neural Engine
- Intel Movidius VPU

## TPU (Tensor Processing Unit)

### Characteristics
- Custom ASIC by Google
- Designed for **high-throughput training and inference**
- Systolic array architecture for matrix multiplication
- Available in cloud and edge variants

### Key Features
| Aspect | Edge TPU | Cloud TPU |
|--------|----------|-----------|
| TOPS | 1-10 | 90-420 |
| Power | Low | High |
| Use Case | Edge inference | Cloud training |

### Examples
- Google Coral Edge TPU
- Google Cloud TPU v4

## VPU (Vision Processing Unit)

### Characteristics
- Specialized for **computer vision workloads**
- Optimized for image/video processing
- Lower power than GPU
- Often includes image signal processor (ISP)

### Examples
- Intel Movidius Myriad 2/X
- Intel Neural Compute Stick

## Performance Comparison

| Metric | NPU | TPU (Edge) | GPU | CPU |
|--------|-----|------------|-----|-----|
| TOPS | 1-50 | 1-10 | 100-1000+ | 0.1-1 |
| Power | 1-5W | 2-15W | 100-300W | 15-65W |
| TOPS/W | 10-20 | 2-4 | 0.5-5 | 0.01-0.05 |
| Latency | Very low | Low | Medium | High |
| Integration | SoC | USB/PCIe | PCIe | Built-in |

## Selection Criteria

### Choose NPU When:
- Battery-powered devices
- Real-time inference needed
- SoC integration preferred
- Mobile/embedded deployment

### Choose TPU When:
- TensorFlow models dominant
- Cloud-to-edge pipeline
- Google ecosystem
- High throughput edge inference

### Choose GPU When:
- Batch processing acceptable
- Training and inference on same hardware
- Maximum throughput needed
- Datacenter deployment

### Choose FPGA When:
- Custom acceleration required
- Low latency critical
- Reconfigurability needed
- Specialized workloads

## TOPS vs TOPS/W

- **TOPS**: Raw computational throughput
- **TOPS/W**: Energy efficiency (critical for edge/battery)
- Modern edge NPUs: 10-20 TOPS/W
- Cloud GPUs: 0.5-5 TOPS/W

## Key Insight

> Small models on edge devices often favor CPUs and edge TPUs over high-end GPUs due to:
> - Lower latency for single-inference workloads
> - Better TOPS/W efficiency
> - No PCIe/PCI bottlenecks for small batches
> - Simpler deployment stack

---

## Takeaways

1. **NPU = Edge-optimized inference** - low power, SoC integration
2. **TPU = Throughput-optimized** - both edge and cloud variants
3. **GPU = Versatile but power-hungry** - best for training/batch inference
4. **TOPS/W matters for edge** - efficiency more important than raw throughput
5. **Match accelerator to use case** - mobile AI ≠ datacenter AI