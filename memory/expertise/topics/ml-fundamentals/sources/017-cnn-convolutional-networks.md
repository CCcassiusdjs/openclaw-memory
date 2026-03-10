# Convolutional Neural Networks (CNNs) - Deep Dive

**Source:** CS231n, Stanford, GeeksforGeeks
**Category:** Deep Learning Architectures
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Convolutional Neural Networks (CNNs)** are specialized neural networks for processing data with grid-like topology (e.g., images, time series). They exploit spatial locality and translation invariance through convolution operations.

### Why Convolutions?

For image classification with fully connected layers:
- Input: 224×224×3 image = 150,528 inputs
- Hidden layer: 1000 neurons
- Parameters: 150 million per layer!

**Problems:**
1. **Too many parameters** - Overfitting risk
2. **No spatial structure** - Ignores local patterns
3. **No translation invariance** - Different positions = different inputs

**Solution: Convolutions**
- Few parameters (shared weights)
- Exploit spatial locality
- Translation invariance

## Convolution Operation

### Definition

**2D Convolution:**
```
(I * K)(i, j) = Σ_m Σ_n I(i+m, j+n) × K(m, n)
```

Where:
- I = input image/feature map
- K = kernel (filter)
- * = convolution operation

**Intuition:** Slide a filter across the input, compute dot products at each position.

### Hyperparameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| **Kernel size** | Size of filter | 3×3, 5×5, 7×7 |
| **Stride** | Step size of slide | 1, 2 |
| **Padding** | Border handling | 'valid', 'same' |
| **Dilation** | Spacing between kernel elements | 1, 2, 3 |

### Output Size Calculation

For input size W×W, kernel size K, stride S, padding P:

```
Output size = floor((W - K + 2P) / S) + 1
```

**Example:**
- Input: 224×224
- Kernel: 3×3, stride 1, padding 1
- Output: 224×224 (same size preserved)

## Key Concepts

### 1. Local Connectivity

Each neuron connects to only a small region of the input (receptive field):
- **Local receptive field:** Small spatial region
- **Weight sharing:** Same filter applied across image
- **Translation invariance:** Same feature detected anywhere

### 2. Feature Hierarchy

**Early layers:** Low-level features (edges, corners)
**Middle layers:** Mid-level features (shapes, textures)
**Later layers:** High-level features (objects, parts)

### 3. Parameter Sharing

**Key insight:** A feature detector useful in one location is likely useful elsewhere.

- Share weights across spatial positions
- Dramatically reduces parameters
- Enables translation invariance

## Pooling Layers

### Types of Pooling

| Type | Operation | Purpose |
|------|-----------|---------|
| **Max pooling** | max(xᵢⱼ) over window | Strong activation detection |
| **Average pooling** | mean(xᵢⱼ) over window | Smooth representation |
| **Global average** | mean over entire map | Feature summarization |

### Why Pooling?

1. **Spatial invariance** - Small translations don't change output much
2. **Downsampling** - Reduce spatial dimensions
3. **Computational efficiency** - Fewer parameters in later layers

### Common Configuration

- Pool size: 2×2
- Stride: 2
- Output size: Input/2

## CNN Architecture Pattern

### Typical Structure

```
[CONV → ReLU → POOL] × N → [FC] × M
```

Where:
- CONV = Convolution layer
- ReLU = Activation function
- POOL = Pooling layer
- FC = Fully connected layer

### Layer Patterns

1. **CONV-RELU-CONV-RELU-POOL** (common pattern)
2. **CONV-RELU-POOL** (simpler)
3. **CONV-CONV-CONV-POOL** (VGG-style)

### Modern Architectures

| Architecture | Year | Key Innovation |
|--------------|------|----------------|
| LeNet-5 | 1998 | First practical CNN |
| AlexNet | 2012 | ReLU, dropout, GPU |
| VGGNet | 2014 | Small filters, deep |
| GoogLeNet | 2015 | Inception modules |
| ResNet | 2015 | Skip connections |
| DenseNet | 2017 | Dense connections |
| EfficientNet | 2019 | Compound scaling |

## Receptive Field

### Definition

The **receptive field** of a neuron is the region of input that affects its output.

### Calculation

For a stack of layers:
- Each layer increases receptive field based on kernel size and stride

**Effective receptive field:**
```
RF_n = RF_{n-1} + (K_n - 1) × ∏_{i=1}^{n-1} S_i
```

Where:
- RF_n = receptive field after layer n
- K_n = kernel size of layer n
- S_i = stride of layer i

### Key Insight

- **Early layers:** Small receptive field (local patterns)
- **Later layers:** Large receptive field (global patterns)
- **Deep networks** → larger receptive fields → more context

## Feature Maps

### Definition

Each filter produces one feature map (activation map):
- Number of filters = depth of output
- Each feature map detects different patterns

**Example:**
- Input: 224×224×3 (RGB image)
- Filter: 3×3×3, with 64 filters
- Output: 224×224×64 (64 feature maps)

### Channels

| Layer | Input Shape | Output Shape | Parameters |
|-------|-------------|--------------|------------|
| CONV1 | 224×224×3 | 112×112×64 | 3×3×3×64 + 64 = 1,792 |
| CONV2 | 112×112×64 | 56×56×128 | 3×3×64×128 + 128 = 73,856 |
| FC | 7×7×512 | 4096 | 7×7×512×4096 + 4096 = 102,760,448 |

## Key Takeaways

1. **Convolutions exploit locality** - Local patterns matter
2. **Weight sharing reduces parameters** - Same filter everywhere
3. **Pooling adds invariance** - Robust to small translations
4. **Feature hierarchy** - Low → mid → high-level features
5. **Receptive field grows with depth** - More context in deeper layers
6. **Architecture patterns** - CONV→RELU→POOL repeated

## References

- LeCun et al. (1998): "Gradient-Based Learning Applied to Document Recognition"
- Krizhevsky et al. (2012): "ImageNet Classification with Deep Convolutional Neural Networks"
- Simonyan & Zisserman (2014): "Very Deep Convolutional Networks for Large-Scale Image Recognition"
- He et al. (2016): "Deep Residual Learning for Image Recognition"