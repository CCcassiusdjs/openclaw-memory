# CPU vs GPU vs TPU vs NPU Architecture Guide

**Source:** https://www.thepurplestruct.com/blog/cpu-vs-gpu-vs-tpu-vs-npu-ai-hardware-architecture-guide-2025
**Date:** 2026-03-12
**Status:** read

---

## The AI Hardware Revolution

### Why Traditional CPUs Struggle with AI
- Neural networks require **massive parallel computations** (matrix multiplications, convolutions)
- CPU architecture: **sequential processing**, branch prediction, complex instruction sets
- Matrix multiplication (1024×1024): **>1 billion operations**
- CPU with 16 cores: 16-32 operations in parallel (vector extensions)
- GPU with 10,000 cores: **tens of thousands in parallel**

### Key Metrics

| Metric | Description | Range |
|--------|-------------|-------|
| **TOPS** | Trillions of Operations/Second | 1-50 (edge NPU) to 90-420 (datacenter TPU) |
| **FLOPS** | Floating Point Operations/Second | 1-5 TFLOPS (CPU), 80-300 TFLOPS (GPU) |
| **TOPS/W** | Operations per Watt | 10-20 (NPU), 0.5-5 (GPU), 0.01-0.05 (CPU) |
| **Ops/Cycle** | Useful computations per clock | 1-10 (CPU), thousands (GPU), 65K-128K (TPU) |

## CPU Architecture for AI

### Design Characteristics
- **Cores**: 4-64 (server: up to 128)
- **Clock Speed**: 3-5 GHz
- **Cache Hierarchy**: L1 (32-64 KB), L2 (256-512 KB), L3 (8-64 MB)
- **Vector Extensions**: AVX-512 (16 float32 ops simultaneously)

### Best For
- Traditional ML algorithms (decision trees, XGBoost)
- Prototyping and small-scale inference
- Sequential operations and orchestration

### Limitations
- **Memory Bandwidth**: 50-100 GB/s (vs 1-3 TB/s for GPUs)
- **Limited Parallelism**: 64 cores vs 18,000 GPU cores
- **No Dedicated Matrix Hardware**: Separate multiply and add instructions
- **Poor TOPS/W**: Least efficient for AI workloads

### Optimization Techniques
| Technique | Benefit |
|-----------|---------|
| SIMD Vectorization | 10-16× speedup |
| Multi-threading | Near-linear to core count |
| Cache Blocking | Reduces memory access |
| Int8 Quantization | 2-4× speedup, 4× bandwidth reduction |
| Optimized BLAS (MKL) | 5-10× faster than naive |

## GPU Architecture for AI

### Design Characteristics
- **Cores**: 5,000-18,000 CUDA/stream cores
- **Clock Speed**: 1-2 GHz (lower than CPU)
- **Streaming Multiprocessors**: 80-140 SMs
- **Memory Bandwidth**: 1-3 TB/s
- **Architecture**: SIMT (Single Instruction Multiple Thread)

### Strengths
- Massive parallelism for matrix operations
- High throughput for batch processing
- Excellent for training deep learning models
- Mature software ecosystem (CUDA)

### Limitations
- High power consumption (100-300W+)
- Suboptimal for small batch inference
- PCIe bottlenecks for small workloads
- Overhead for real-time latency

## TPU Architecture

### Design Characteristics
- **Systolic Array**: Matrix multiplication optimized
- **Operations/Cycle**: 65,000-128,000
- **TOPS**: 1-10 (edge), 90-420 (cloud)
- **Architecture**: Purpose-built for TensorFlow

### Strengths
- **83× better TOPS/W than CPU** (Google TPU v1)
- **29× better TOPS/W than GPU**
- Optimized for matrix multiplication
- High throughput training and inference

### Limitations
- TensorFlow-centric ecosystem
- Limited flexibility for custom operations
- Cloud TPU availability constraints

## NPU Architecture

### Design Characteristics
- **Purpose**: Edge inference, mobile AI
- **Power**: Milliwatts to watts
- **TOPS**: 1-50
- **Integration**: SoC embedded (mobile phones, IoT)

### Strengths
- Lowest power consumption
- SoC integration (no external hardware)
- Real-time low latency
- Ideal for battery-powered devices

### Examples
| NPU | Device/Platform |
|-----|-----------------|
| Arm Ethos-U85 | Cortex-M based systems |
| Qualcomm Hexagon | Snapdragon processors |
| Apple Neural Engine | iPhone/Mac |
| Intel Movidius VPU | Edge AI boards |

## Comparison Summary

| Aspect | CPU | GPU | TPU | NPU |
|--------|-----|-----|-----|-----|
| **Parallelism** | Limited | Massive | Systolic | Moderate |
| **Power** | 15-65W | 100-300W | 50-200W | 1-5W |
| **TOPS/W** | 0.01-0.05 | 0.5-5 | 20-50 | 10-20 |
| **Latency** | Low | Medium | Medium | Very Low |
| **Use Case** | Orchestration | Training | Both | Edge Inference |
| **Batch Size** | 1 | 8-128 | 16-64 | 1 |

---

## Key Insight

> For neural networks, the same operations repeat across **millions of data elements**. This enables **Single Instruction Multiple Data (SIMD)** execution. The question is: how many parallel operations can you execute?

- **CPU**: 1-10 operations per cycle
- **GPU**: Tens of thousands per cycle
- **TPU**: 65,000-128,000 per cycle

---

## Takeaways

1. **CPU for orchestration** - sequential tasks, small models, prototyping
2. **GPU for training** - massive parallelism, mature ecosystem
3. **TPU for throughput** - optimized matrix multiplication, TensorFlow
4. **NPU for edge** - lowest power, real-time inference, mobile integration
5. **TOPS/W matters more than TOPS** - efficiency drives edge deployment
6. **Memory bandwidth is the bottleneck** - Von Neumann limit for all architectures