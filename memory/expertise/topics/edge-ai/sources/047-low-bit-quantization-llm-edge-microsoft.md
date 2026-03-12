# Low-Bit Quantization for LLMs on Edge Devices (Microsoft Research 2025)

**Source:** https://www.microsoft.com/en-us/research/blog/advances-to-low-bit-quantization-enable-llms-on-edge-devices/
**Type:** Industry Research (Microsoft Research)
**Date:** February 2025
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

Microsoft Research presents advances in low-bit quantization enabling LLMs on edge devices. Introduces three key technologies: Ladder (data type compiler), T-MAC (table-lookup mpGEMM library), and LUT Tensor Core (hardware architecture for mixed-precision computation).

## Key Concepts

### Mixed-Precision Matrix Multiplication (mpGEMM)

Traditional quantization requires dequantization for hardware compatibility, adding overhead. mpGEMM enables direct computation with different precision formats:

| Operation | Description |
|-----------|-------------|
| int8 × int1 | 8-bit activation × 1-bit weight |
| int8 × int2 | 8-bit activation × 2-bit weight |
| FP16 × int4 | 16-bit activation × 4-bit weight |

### Hardware Limitations

Most hardware accelerators support only **symmetric computations** (same format for both operands). This creates a gap between:
- Emerging custom data types (NF4, OCP-MXFP)
- Hardware-supported types (FP16, INT8, FP8)

## Ladder: Data Type Compiler

### Purpose
Bridge the gap between emerging custom data formats and hardware-supported precision types.

### Key Features
1. **Separation of Concerns** - Data storage from computation
2. **Lossless Conversion** - Custom types → hardware-compatible formats
3. **Performance Optimization** - Maps low-bit data to efficient instructions

### Architecture
```
Custom Data Types → Ladder Transform → Hardware Native Types → Compute
```

### Performance Results
- Up to **14.6× speedup** for custom data types on GPUs
- Supports NVIDIA and AMD GPU architectures
- No hardware modifications required

## T-MAC: Table-Lookup mpGEMM

### Purpose
Enable efficient mpGEMM on CPUs without dequantization or multiplication.

### Key Innovation
**Replaces multiplication with bit-wise table lookups**

### How It Works
1. Precompute lookup tables for weight bits
2. Store tables on-chip (reduced memory access)
3. Use bit-serial operations for multiplication-free GEMM
4. No dequantization required

### Performance Results (Surface Laptop 7, Snapdragon X Elite)

| Model | Speed | Comparison |
|-------|-------|------------|
| BitNet-b1.58 (3B) | 48 tokens/s | 4-5× faster than llama.cpp |
| Llama-2-7B (2-bit) | 30 tokens/s | Exceeds average reading rate |
| Llama-2-7B (4-bit) | 20 tokens/s | 2× faster than dedicated NPU |

### Raspberry Pi 5 Results
- **BitNet-b1.58 (3B)**: 11 tokens/s
- **Power efficiency**: 1/4 to 1/6 CPU cores for same throughput as llama.cpp

### Key Benefits
- No GPU/NPU required
- Standard CPU deployment
- Significant power efficiency
- Scalable across edge devices

## LUT Tensor Core: Hardware Architecture

### Purpose
Dedicated hardware accelerator for LUT-based mpGEMM.

### Design Challenges Addressed

1. **Table Precompute & Storage**
   - Software-based DFG transformation
   - Operator fusion
   - Table symmetrization

2. **Bit-Width Flexibility**
   - Support int4/2/1 for weights
   - Support FP16/8, int8 for activations
   - Various precision combinations

3. **LUT Tiling Shape**
   - Elongated tiling for table reuse
   - Reduced storage costs

4. **Instruction & Compilation**
   - Extended MMA → LMMA instructions
   - cuBLAS-like software stack
   - End-to-end compiler integration

### Performance Results

| Metric | Value |
|--------|-------|
| **Inference Speed** | 6.93× faster than traditional Tensor Core |
| **Area** | 38.3% of traditional Tensor Core |
| **Computational Density** | 20.9× improvement |
| **Energy Efficiency** | 11.2× improvement |

### Architecture
```
LMMA Instructions → LUT Tables → Bit-Serial Compute → Accumulator
```

## BitNet Integration

### BitNet Model
- Starts with low-bit configuration
- Scales up while maintaining efficiency
- Demonstrates capability improvements through quantization scaling

### Key Insight
Low-bit quantization enables **model scaling** while reducing memory and compute demands.

## Applications

### Embodied AI
- Robots with real-time perception
- Dynamic environmental interaction
- On-device LLM inference

### Edge Devices
- Smartphones
- Laptops
- IoT devices
- Autonomous systems

## Open Source

| Project | URL |
|---------|-----|
| T-MAC | github.com/microsoft/T-MAC |
| Ladder/BitBLAS | github.com/microsoft/BitBLAS |

## Key Takeaways

1. **Multiplication-Free** - LUT approach eliminates traditional GEMM multiplication
2. **CPU-First** - Standard CPUs can run quantized LLMs efficiently
3. **Hardware Co-Design** - Dedicated accelerators provide order-of-magnitude gains
4. **Mixed Precision** - Different formats for weights vs activations
5. **Practical Edge Deployment** - Real-time inference on resource-constrained devices

## Related Topics

- INT8/INT4 quantization techniques
- BitNet architecture
- LLM compression strategies
- Edge deployment frameworks
- Hardware accelerator design