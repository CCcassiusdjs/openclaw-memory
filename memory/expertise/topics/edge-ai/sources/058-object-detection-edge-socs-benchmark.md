# Object Detection on Low-Compute Edge SoCs: Benchmark & Deployment (2026)

**Source:** https://www.nature.com/articles/s41598-026-36862-y
**Type:** Academic Paper (Scientific Reports)
**Date:** January 2026
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

Comprehensive benchmark evaluating deep learning-based object detectors on low-compute edge AI SoCs. Reveals that real-world performance depends on factors beyond nominal TOPS ratings, including architectural design, memory bandwidth, and system-level contention.

## Key Findings

### TOPS ≠ Performance
- **Nominal TOPS ratings don't tell the full story**
- Architecture efficiency matters significantly
- Memory bandwidth critical bottleneck
- System-level contention impacts results

### Key Performance Factors

| Factor | Impact | Description |
|--------|--------|-------------|
| **Architectural Design** | High | GPU/NPU architecture efficiency |
| **Memory Bandwidth** | Critical | Data transfer bottlenecks |
| **System Contention** | Significant | Resource sharing overhead |
| **Thermal Throttling** | Variable | Sustained performance limits |

## Benchmark Results

### Tested Platforms
- ARM Cortex-M class MCUs
- ARM Cortex-A class SoCs
- NVIDIA Jetson family
- Intel Neural Compute Sticks
- Edge AI accelerators

### Key Metrics

| Platform | TOPS | Real FPS | Efficiency |
|----------|------|----------|-------------|
| MCU class | <0.5 | 1-15 FPS | High/W |
| SBC class | 0.5-5 | 10-60 FPS | Moderate |
| Edge GPU | 5-100 | 30-200 FPS | Variable |

### Model Comparison

| Model | Size | Accuracy (mAP) | Typical FPS (Edge) |
|-------|------|----------------|-------------------|
| YOLOv5s | 7M | 37.4 | 30-100 |
| YOLOv5n | 2M | 28.4 | 100-300 |
| YOLOv8n | 3M | 37.3 | 50-150 |
| MobileNet-SSD | 5M | 21.0 | 100-500 |
| EfficientDet-D0 | 4M | 34.6 | 40-120 |

## Deployment Guidelines

### Model Selection

**Accuracy vs Speed Trade-off:**
1. **YOLOv5/v8 Nano**: Best for real-time, lower accuracy
2. **YOLOv5/v8 Small**: Balanced performance
3. **EfficientDet-D0**: Good efficiency, moderate accuracy
4. **MobileNet-SSD**: Highest throughput, lowest accuracy

### Optimization Techniques

| Technique | Impact | Trade-off |
|-----------|--------|-----------|
| **Quantization (INT8)** | 2-4x faster | Minor accuracy loss |
| **Pruning** | 1.5-2x smaller | Moderate accuracy loss |
| **TensorRT Optimization** | 2-5x faster | Platform-specific |
| **Batch Size = 1** | Lowest latency | Lower throughput |

### Hardware Considerations

**Memory Bandwidth:**
- Largest bottleneck for vision models
- Higher bandwidth > higher TOPS
- Consider on-chip memory

**Thermal Management:**
- Edge devices throttle under load
- Sustained performance < burst performance
- Design for thermal limits

**Power Efficiency:**
- Performance per watt critical
- TOPS/W more meaningful than TOPS
- Consider duty cycle

## Key Insights

### Myth Busting

| Myth | Reality |
|------|---------|
| "More TOPS = Better" | Architecture and memory matter more |
| "Real-time always" | Thermal limits reduce sustained FPS |
| "INT8 = 4x smaller" | Quantization varies by model |
| "Edge = Slow" | Many models run >30 FPS on edge |

### Best Practices

1. **Test on target hardware** - Emulators unreliable
2. **Measure sustained FPS** - Burst performance misleading
3. **Profile memory bandwidth** - Often the bottleneck
4. **Consider thermal envelope** - Sustained vs peak
5. **Profile end-to-end** - Pre/post-processing overhead

## Key Takeaways

1. **TOPS ≠ Performance** - Architecture efficiency matters more
2. **Memory Bandwidth** - Critical bottleneck for vision models
3. **System Contention** - Resource sharing impacts results
4. **Thermal Limits** - Sustained < peak performance
5. **Benchmark on Target** - Emulators unreliable

## Related Topics

- Edge AI hardware selection
- Model optimization for edge
- YOLO variants comparison
- Thermal-aware deployment