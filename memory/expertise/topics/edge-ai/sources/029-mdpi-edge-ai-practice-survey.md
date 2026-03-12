# Edge AI in Practice - Systematic Survey

**Source:** https://www.mdpi.com/2079-9292/14/24/4877
**Date:** 2026-03-12
**Status:** read

---

## Overview

A systematic review (PRISMA-aligned) examining deep learning deployment on embedded hardware, covering optimization techniques, lightweight architectures, and hardware platforms.

## Key Findings

### Inference Process Stages
1. **Pre-processing**: Input data transformation (normalization, encoding, tensor creation)
2. **Model Execution**: Neural network forward pass
3. **Post-processing**: Output transformation to usable format

### Performance Metrics

| Metric | Description |
|--------|-------------|
| **Latency** | Time per inference (ms/μs) |
| **Throughput** | Inputs per second (IPS/FPS) |
| **Energy** | Power consumption (W/mW) |
| **Memory** | RAM usage (KB/MB) |

### Hardware Accelerator Metrics
- **TOPS**: Tera Operations Per Second (theoretical max)
- **TOPS/W**: Operations per watt (energy efficiency)
- **TOPS/W/MHz**: Energy efficiency per clock frequency
- **GOPS/W**: Giga Operations Per Second per Watt
- **FLOPS**: Floating-point Operations Per Second

### Benchmark Frameworks
- **MLPerf Inference**: Industry standard, 4 scenarios (Single-stream, Multi-stream, Server, Offline)
- **MLPerf Tiny**: Ultra-low-power benchmark (keyword spotting, visual wake words, image classification, anomaly detection)
- **EdgeAIBench**: Full computation chain (device–edge–cloud)

## Optimization Techniques

1. **Pruning**: Remove redundant weights/neurons
2. **Quantization**: Reduce precision (FP32 → INT8/INT4)
3. **Knowledge Distillation**: Teacher-student model compression
4. **Neural Architecture Search (NAS)**: Automated architecture optimization

## Deployment Methodology (5 Stages)

1. **Requirement Definition**: Latency, accuracy, power, memory constraints
2. **Model Selection**: Choose architecture based on requirements
3. **Optimization**: Apply pruning, quantization, distillation
4. **Hardware Alignment**: Match model to hardware capabilities
5. **Deployment**: Deploy and benchmark

## Emerging Trends

- **TinyML**: Ultra-low-power ML on microcontrollers
- **Hybrid Architectures**: Edge-cloud collaboration
- **Hardware-Software Co-design**: Joint optimization

## Persistent Gaps

- Limited ultra-low-precision inference support
- Variability in hardware toolchains
- Absence of standardized holistic benchmarking

---

## Takeaways

1. **Multi-objective trade-offs** are central to Edge AI deployment
2. **Standardized benchmarks** (MLPerf) enable fair comparison
3. **System-level metrics** capture real-world performance
4. **Methodology exists** for systematic deployment pipeline