# EON Compiler (RAM Optimized) - Edge Impulse

**Source:** https://www.edgeimpulse.com/blog/introducing-eon-compiler-ram-optimized/
**Date:** 2026-03-12
**Status:** read

---

## Overview

The EON (Edge Optimized Neural) Compiler compiles ML models into highly efficient C++ source code, reducing RAM usage by up to 65% compared to TensorFlow Lite.

## Key Benefits

| Metric | Improvement |
|--------|-------------|
| RAM Reduction | 40-65% vs TensorFlow Lite |
| Flash Reduction | Up to 35% |
| Model Support | TensorFlow, PyTorch, scikit-learn, LightGBM, XGBoost |
| Accuracy | Retained (same predictions) |

## How It Works

### Traditional Approach
- Computes layer by layer
- Stores intermediate results
- High RAM requirements

### EON Approach
- Analyzes model architecture
- Identifies RAM usage from intermediate results
- Slices model graph into smaller segments
- Computes values directly as required
- Minimizes intermediate storage

## RAM vs ROM Trade-off

| Version | RAM Usage | ROM Usage | Latency |
|---------|-----------|-----------|---------|
| EON (Default) | Lower | Baseline | Baseline |
| EON (RAM Optimized) | Lowest | Slightly higher | Slightly higher |

## Target Applications

- Smaller, less expensive MCUs
- Battery-powered devices
- Resource-constrained deployments

## Availability

- **Default EON**: Available to all users
- **EON (RAM Optimized)**: Enterprise customers only

---

## Takeaways

1. **EON eliminates interpreter overhead** - compiles to direct kernel calls
2. **RAM optimization trades ROM/latency for RAM** - 40-65% RAM reduction
3. **Enables smaller MCUs** - run models on cheaper hardware
4. **Supports multiple frameworks** - TensorFlow, PyTorch, classical ML
5. **Enterprise feature** - RAM-optimized version requires enterprise license