# EON Compiler - Official Documentation

**Source:** https://docs.edgeimpulse.com/docs/edge-impulse-studio/deployment/eon-compiler
**Date:** 2026-03-12
**Status:** read

---

## Overview

The Edge Optimized Neural (EON) compiler compiles ML models into efficient C++ source code, reducing RAM usage by 25-65% compared to TensorFlow Lite.

## Key Benefits

| Metric | Improvement vs TFLite |
|--------|----------------------|
| RAM Reduction | 25-65% |
| Flash Reduction | 10-35% |
| Accuracy | Same |
| Inference | Faster |

## How It Works

### Traditional TFLite Micro
1. Read model from Flatbuffer format
2. Construct inference graph
3. Plan memory allocation
4. Initialize, prepare, invoke operators
5. Heavy computational burden on embedded systems

### EON Compiler Approach
1. Perform resource-intensive tasks on servers
2. Generate C++ files with Init, Prepare, Invoke functions
3. Deploy to embedded systems
4. Eliminate interpreter overhead

### EON Compiler (RAM Optimized)
- Computes values directly as needed
- Minimizes storage of intermediate results
- 40-65% RAM reduction vs TFLite
- Slightly higher latency/flash cost

## EON Compiler Options

| Option | RAM | Flash | Latency | Availability |
|--------|-----|-------|---------|--------------|
| TFLite Micro | Baseline | Baseline | Baseline | All |
| EON Compiler | 25-40% less | 10-35% less | Faster | All |
| EON (RAM Optimized) | 40-65% less | Higher | Slightly higher | Enterprise |

## Performance by Architecture

### Image Classification
- MobileNet variants benefit significantly
- ResNet shows 30-50% RAM reduction
- EfficientNet shows 20-40% reduction

### Object Detection
- FOMO (Faster Objects, More Objects) optimized
- YOLO variants benefit from tensor deduplication
- SSD models show consistent improvements

### Keyword Spotting
- MFCC/MFE feature extraction optimized
- Small CNNs benefit from reduced overhead
- Memory-efficient for continuous listening

### Time Series
- Anomaly detection models optimized
- Classification models benefit
- Regression models show improvements

## Limitations

### Unsupported Operators
- Not all TFLite operators supported
- Complex operations may prevent optimization
- Check operator matrix for compatibility

### Residual Layers
- Supported for direct feed-forward (MobileNet style)
- Complex residual processing may not optimize effectively

### RAM Optimized Constraints
- Slicing algorithm supports limited operators
- Standard convolutions work well
- Custom operators may not be supported

## Supported Operators

EON Compiler supports a subset of TensorFlow Lite operators:
- Core operators: Conv2D, Dense, ReLU, MaxPool, BatchNorm
- Activation functions: Softmax, Sigmoid, Tanh
- Reshape operators: Reshape, Flatten, Transpose
- Arithmetic: Add, Mul, Sub, Div
- And many more (see operator matrix)

---

## Takeaways

1. **EON eliminates interpreter overhead** - compiles to direct C++ calls
2. **RAM Optimized trades latency for memory** - 40-65% less RAM
3. **Same accuracy** - no model quality loss
4. **Enterprise feature for RAM Optimized** - standard EON available to all
5. **Check operator support** - not all operations are compatible