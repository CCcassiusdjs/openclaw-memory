# MLPerf Inference: Edge Benchmark Suite (2025)

**Source:** https://mlcommons.org/benchmarks/inference-edge/
**Type:** Official Benchmark Documentation (MLCommons)
**Date:** September 2025
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

MLPerf Inference: Edge is the industry-standard benchmark suite measuring how fast systems can process inputs and produce results using trained ML models on edge devices. Covers vision, language, recommendation, and traditional ML workloads.

## Key Concepts

### Benchmark Categories

| Category | Workload | Description |
|----------|----------|-------------|
| **Computer Vision** | Object Detection | Real-time detection (YOLO-based) |
| | Image Classification | MobileNet, ResNet variants |
| | Image Segmentation | Semantic/instance segmentation |
| **Language** | Language Model | BERT, GPT-based inference |
| **Recommendation** | DLRM | Deep learning recommendation |
| **Traditional ML** | RNN-Transducer | Speech recognition |

### Edge vs Data Center Benchmarks

| Aspect | Edge | Data Center |
|--------|------|-------------|
| **Power Budget** | <100W | 200-700W |
| **Latency Focus** | Real-time | Throughput |
| **Model Size** | Smaller | Larger |
| **Batch Size** | 1-8 | Variable |

## Metrics

### Single-Stream Performance
- **Latency**: Time to process one input
- **Units**: ms/query
- **Use Case**: Real-time inference

### Multi-Stream Performance
- **Throughput**: Queries per second
- **Units**: queries/s
- **Use Case**: Batch processing

### Offline Performance
- **Throughput**: Samples per second
- **Units**: samples/s
- **Use Case**: Bulk processing

### Key Metrics
- **Top-1 Accuracy**: Image classification
- **mAP**: Object detection
- **F1 Score**: Segmentation
- **BLEU/ROUGE**: Language tasks

## Benchmark Models

### Vision Models

| Model | Task | Input Size | Typical Use |
|-------|------|------------|-------------|
| MobileNet-v1 | Classification | 224×224 | Mobile inference |
| MobileNet-v2 | Classification | 224×224 | Mobile inference |
| ResNet-50 | Classification | 224×224 | General purpose |
| EfficientNet | Classification | Various | Efficiency-focused |
| SSD-ResNet | Detection | 300×300 | Object detection |
| YOLO-based | Detection | 640×640 | Real-time detection |

### Language Models

| Model | Task | Input | Use Case |
|-------|------|-------|----------|
| BERT-Large | NLP | 512 tokens | Question answering |
| GPT-J | Generation | 1024 tokens | Text generation |

## Performance Measurement

### Test Conditions
- **System Under Test (SUT)**: Complete hardware + software
- **Query Count**: Minimum queries for statistical significance
- **Cooldown**: Between tests to ensure thermal consistency
- **Compliance**: Must meet accuracy thresholds

### Reporting Requirements
- **Code**: Open-source implementations
- **Models**: Standard, unmodified models
- **Data**: Reference datasets
- **Reproducibility**: Documented setup

## Key Takeaways

1. **Standardized Benchmarking** - Fair comparison across hardware
2. **Multiple Workloads** - Vision, language, recommendation
3. **Edge-Specific** - Power and latency constraints
4. **Open Source** - Reproducible results
5. **Industry Adoption** - NVIDIA, Intel, AMD, ARM participate

## Related Topics

- MLPerf Training benchmarks
- TinyML benchmarking
- Edge inference optimization
- Model compression techniques