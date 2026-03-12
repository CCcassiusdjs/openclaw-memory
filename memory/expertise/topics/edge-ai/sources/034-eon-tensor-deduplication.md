# EON Compiler Tensor Deduplication

**Source:** https://www.edgeimpulse.com/blog/new-in-eon-compiler-automatically-reduce-memory-with-tensor-deduplication/
**Date:** 2026-03-12
**Status:** read

---

## Overview

EON Compiler optimization that automatically eliminates duplicate tensor data in neural network models, reducing both RAM and flash memory.

## Problem: Duplicate Tensor Data

In models like MobileNet, many tensors share identical properties:
- Tensor dimensions
- Quantization parameters
- Repeating block structures

The C++ compiler doesn't automatically deduplicate these constants.

## Solution: Hash-Based Deduplication

1. **Serialize** tensor property data to byte array
2. **Hash** the byte array (MD5)
3. **Check** hash map for existing match
4. **Reuse** if hash exists, otherwise emit new constant

## Benefits

| Metric | Improvement |
|--------|-------------|
| RAM Reduction | 10% (FOMO benchmark) |
| Flash Reduction | 10% (FOMO benchmark) |
| Duplicate Parameters | 48 of 72 removed |

## How It Works

Traditional TensorFlow Lite Micro:
1. Reads model from Flatbuffer format
2. Constructs inference graph
3. Plans memory allocation
4. Initializes, prepares, invokes operators
5. Heavy computational burden on embedded systems

EON Compiler:
1. Performs resource-intensive tasks on servers
2. Generates C++ files with Init, Prepare, Invoke functions
3. Deploys to embedded systems
4. Eliminates interpreter overhead

## Availability

Available to all Edge Impulse users when choosing EON Compiler or EON Compiler (RAM Optimized) deployment.

---

## Takeaways

1. **Automatic optimization** - no manual intervention needed
2. **Works on tensor metadata** - dimensions, quantization params
3. **Larger vision models benefit most** - more repeating structures
4. **Complementary to other optimizations** - stacks with quantization, pruning
5. **Free to all users** - included in EON Compiler deployment