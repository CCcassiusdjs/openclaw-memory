# Activation Functions in Neural Networks

**Source:** Google ML Crash Course, GeeksforGeeks
**Category:** Neural Networks
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Activation functions** introduce non-linearity into neural networks, enabling them to learn complex patterns. Without activation functions, stacking linear operations still produces linear transformations, severely limiting model capacity.

### Why Non-linearity?

```
Linear operation on linear operation = Linear operation

With activation function:
Linear operation → Non-linear transform → Linear operation
= Non-linear relationship
```

**Key insight:** Each layer learns a more complex, higher-level function over raw inputs.

## Common Activation Functions

### 1. Sigmoid (Logistic)

**Formula:**
```
σ(x) = 1 / (1 + e^(-x))
```

**Properties:**
- **Range:** (0, 1)
- **Smooth, differentiable**
- **Centered at 0.5**

**Advantages:**
- Interpretable as probability
- Historically popular for binary classification

**Disadvantages:**
- **Vanishing gradient problem** (saturates for large |x|)
- **Not zero-centered** (causes zigzag gradient dynamics)
- **Computationally expensive** (exponential)

**Use case:** Output layer for binary classification

### 2. Tanh (Hyperbolic Tangent)

**Formula:**
```
tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x)) = 2σ(2x) - 1
```

**Properties:**
- **Range:** (-1, 1)
- **Smooth, differentiable**
- **Zero-centered**

**Advantages:**
- Zero-centered (better gradient dynamics than sigmoid)
- Stronger gradients than sigmoid

**Disadvantages:**
- Still suffers from vanishing gradient for large |x|
- Computationally expensive

**Use case:** Hidden layers (when zero-centered output needed)

### 3. ReLU (Rectified Linear Unit)

**Formula:**
```
ReLU(x) = max(0, x)
```

**Properties:**
- **Range:** [0, +∞)
- **Non-smooth at x=0** (but continuous)

**Advantages:**
- **Computationally efficient** (simple threshold)
- **Mitigates vanishing gradient** for positive inputs
- **Sparse activation** (negative outputs are 0)
- **Biologically plausible** (like neurons)

**Disadvantages:**
- **Dying ReLU problem** (neurons can "die" if always negative)
- **Not zero-centered** (output is always ≥ 0)

**Use case:** Default choice for hidden layers

### Comparison Table

| Function | Range | Zero-Centered | Vanishing Gradient | Computational Cost |
|----------|-------|---------------|--------------------|--------------------|
| **Sigmoid** | (0, 1) | ❌ | Yes (high) | High |
| **Tanh** | (-1, 1) | ✅ | Yes (moderate) | High |
| **ReLU** | [0, +∞) | ❌ | No (positive) | Low |

## Modern Activation Functions

### 4. Leaky ReLU

**Formula:**
```
LeakyReLU(x) = max(αx, x), where α is small (e.g., 0.01)
```

**Advantage:** Addresses dying ReLU by allowing small gradient for negative inputs.

**Use case:** When ReLU neurons are dying.

### 5. ELU (Exponential Linear Unit)

**Formula:**
```
ELU(x) = {
  x,          if x ≥ 0
  α(e^x - 1), if x < 0
}
```

**Advantages:**
- Zero-centered outputs (unlike ReLU)
- Smooth everywhere (unlike ReLU)
- Negative outputs for negative inputs

**Disadvantage:** More computationally expensive than ReLU.

### 6. SELU (Scaled ELU)

**Formula:**
```
SELU(x) = λ × SELU(x), where λ ≈ 1.0507, α ≈ 1.6733
```

**Advantage:** Self-normalizing (mean → 0, variance → 1 automatically).

**Use case:** Self-normalizing networks (SNNs).

### 7. GELU (Gaussian Error Linear Unit)

**Formula:**
```
GELU(x) = x × Φ(x), where Φ is Gaussian CDF
```

**Advantages:**
- Smooth (differentiable everywhere)
- Used in modern Transformers (BERT, GPT)
- Better performance than ReLU in some cases

**Use case:** Transformer architectures.

### 8. Swish (SiLU - Sigmoid Linear Unit)

**Formula:**
```
Swish(x) = x × σ(x) = x / (1 + e^(-x))
```

**Advantages:**
- Smooth, non-monotonic
- Self-gated (learnable)
- Often better than ReLU

**Use case:** Modern architectures (EfficientNet).

## Comparison of Modern Activations

| Function | Dying ReLU | Zero-Centered | Smooth | Popularity |
|----------|------------|---------------|--------|------------|
| ReLU | Yes | ❌ | ❌ | Very High |
| Leaky ReLU | No | ❌ | ❌ | High |
| ELU | No | ✅ | ✅ | Medium |
| SELU | No | ✅ | ✅ | Medium |
| GELU | No | ✅ | ✅ | High (Transformers) |
| Swish | No | ✅ | ✅ | Medium |

## Choosing Activation Functions

### Recommendations

| Layer Type | Default | Alternative |
|------------|---------|-------------|
| **Hidden layers** | ReLU | Leaky ReLU, GELU |
| **Output (binary)** | Sigmoid | - |
| **Output (multiclass)** | Softmax | - |
| **Output (regression)** | Linear | - |
| **Transformers** | GELU | Swish |

### Best Practices

1. **Start with ReLU** - Simple, fast, works well
2. **If dying ReLU** - Switch to Leaky ReLU or ELU
3. **For Transformers** - GELU is standard
4. **For Self-Normalizing Networks** - SELU with proper initialization
5. **Output layer** - Match to task (sigmoid/softmax/linear)

## Vanishing Gradient Problem

**Cause:** Activation functions like sigmoid/tanh have flat regions where gradients approach zero.

**Effect:** Gradients in earlier layers become very small, slowing or stopping learning.

**Solutions:**
- Use ReLU (or variants) instead of sigmoid/tanh
- Batch normalization
- Residual connections
- Careful initialization (He for ReLU, Xavier for tanh)

## Key Takeaways

1. **Non-linearity is essential** - Enables learning complex patterns
2. **ReLU is default** - Fast, simple, avoids vanishing gradient
3. **Sigmoid for output** - Binary classification probability
4. **Modern activations (GELU, Swish)** - Better for deep networks
5. **Dying ReLU is real** - Consider Leaky ReLU or ELU
6. **Match output to task** - Sigmoid, softmax, or linear

## References

- Nair & Hinton (2010): ReLU introduction
- Clevert et al. (2016): ELU paper
- Klambauer et al. (2017): SELU paper
- Hendrycks & Gimpel (2016): GELU paper
- Ramachandran et al. (2017): Swish paper