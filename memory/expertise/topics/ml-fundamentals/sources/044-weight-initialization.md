# Weight Initialization in Neural Networks (Deep Dive)

**Source:** Pinecone, Wikipedia, Glorot & Bengio (2010), He et al. (2015)
**Category:** Neural Networks / Training
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Weight initialization** determines the starting point on the loss landscape, affecting:
- Training speed
- Convergence to good local minima
- Gradient flow in deep networks

### Why Initialization Matters

The loss surface of deep networks is:
- **High-dimensional** - Millions of parameters
- **Non-convex** - Many local minima
- **Complex** - Saddle points, plateaus

**Initial weights determine** which local minimum the network converges to.

## Problems with Poor Initialization

### 1. Zero/Constant Initialization

**Problem:** Symmetry breaking

```
All weights = 0 (or constant k)
→ All neurons receive same input
→ All neurons compute same output
→ All neurons receive same gradient
→ All neurons update identically
```

**Result:** Network cannot learn different features. All neurons learn the "same" thing.

### 2. Small Random Initialization

**Problem:** Vanishing gradients

```
Weights ~ N(0, 0.01²)
→ Activations shrink with depth
→ Gradients proportional to activations
→ Gradients vanish in deep layers
```

**Result:** Neurons in deep layers don't learn.

### 3. Large Random Initialization

**Problem:** Saturating activations

```
Weights ~ N(0, 1²)
→ Activations saturate (|z| → large)
→ sigmoid/tanh gradients → 0
→ Vanishing gradients again
```

**Result:** Training stalls.

## Optimal Initialization Strategy

### The Key Insight

For stable forward and backward passes:
- Activations should neither vanish nor explode
- Gradients should neither vanish nor explode

**Derivation:**

For layer l, if inputs are normalized (mean 0, variance 1):
```
z_l = W_l · a_{l-1} + b_l
```

If W_l has variance Var(W) = 1/n_in:
```
Var(z_l) = Var(W) × n_in × Var(a_{l-1}) = Var(a_{l-1})
```

**This preserves variance through layers.**

## Xavier/Glorot Initialization

### Formula

**Normal distribution:**
```
W ~ N(0, 2 / (n_in + n_out))
```

**Uniform distribution:**
```
W ~ U(-√(6 / (n_in + n_out)), √(6 / (n_in + n_out)))
```

Where:
- n_in = number of inputs to the neuron (fan_in)
- n_out = number of outputs from the neuron (fan_out)

### Why It Works

- Forward pass: Var(W) = 1/n_in preserves activation variance
- Backward pass: Var(W) = 1/n_out preserves gradient variance
- Glorot uses average: 2/(n_in + n_out)

### Best For

- **Sigmoid** activation (zero-centered)
- **Tanh** activation (zero-centered)
- Works well with saturating activations

### Not Best For

- **ReLU** activation (not zero-centered)
- Can lead to dead neurons

## He Initialization (Kaiming)

### Formula

**Normal distribution:**
```
W ~ N(0, 2 / n_in)
```

**Uniform distribution:**
```
W ~ U(-√(6 / n_in), √(6 / n_in))
```

### Why It Works

ReLU kills half the neurons (negative inputs → 0):
- Only half of the activations propagate
- Need to compensate with factor of 2

```
Var(W) = 2 / n_in (instead of 1/n_in)
```

### Best For

- **ReLU** activation
- **Leaky ReLU** activation
- Modern default for deep networks

## Comparison Table

| Initialization | Variance | Best For | Year |
|----------------|----------|----------|------|
| **Zero/Constant** | 0 | Never! | - |
| **Small random** | Very small | Never! | - |
| **Xavier/Glorot** | 2/(n_in + n_out) | Sigmoid, Tanh | 2010 |
| **He/Kaiming** | 2/n_in | ReLU, variants | 2015 |
| **LeCun** | 1/n_in | SELU | 1998 |

## Implementation

### PyTorch

```python
import torch.nn as nn

# Xavier/Glorot
nn.init.xavier_uniform_(layer.weight)
nn.init.xavier_normal_(layer.weight)

# He/Kaiming
nn.init.kaiming_uniform_(layer.weight, mode='fan_in', nonlinearity='relu')
nn.init.kaiming_normal_(layer.weight, mode='fan_in', nonlinearity='relu')
```

### TensorFlow/Keras

```python
from tensorflow.keras import initializers

# Xavier/Glorot (default for Dense layers)
initializer = initializers.GlorotUniform()
layer = Dense(64, kernel_initializer=initializer)

# He/Kaiming
initializer = initializers.HeNormal()
layer = Dense(64, kernel_initializer=initializer)
```

## Key Takeaways

1. **Never use zero/constant initialization** - Symmetry problem
2. **Match initialization to activation** - Xavier for sigmoid/tanh, He for ReLU
3. **Variance matters** - Preserve variance through layers
4. **Default choice** - He initialization for ReLU-based networks
5. **Modern frameworks** - Use built-in initializers (they handle this automatically)
6. **BatchNorm helps** - Reduces initialization sensitivity

## References

- Glorot & Bengio (2010): "Understanding the difficulty of training deep feedforward neural networks"
- He et al. (2015): "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification"
- LeCun (1998): "Efficient BackProp"