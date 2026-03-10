# Weight Decay vs L2 Regularization

**Source:** paepper.com, Loshchilov & Hutter (2019)
**Category:** Regularization
**Priority:** High (Practical Importance)
**Read:** 2026-03-10

## Core Concept

Both **L2 regularization** and **weight decay** aim to reduce weight magnitudes for better generalization, but they are **not equivalent** for adaptive optimizers like Adam.

### Big Idea

Networks with **smaller weights tend to generalize better** and overfit less. Both techniques encourage smaller weights, but through different mechanisms.

## L2 Regularization

### Definition

Adds a penalty term to the loss function:

```
L_reg(θ) = L(θ) + (λ/2) ||θ||²
```

### Gradient Calculation

```
∇_θ L_reg = ∇_θ L + λ · θ
```

The gradient of the squared weights becomes just the weights themselves (after differentiation).

### Update Step (SGD)

```
θ_t = θ_{t-1} - α · (∇_θ L + λ · θ_{t-1})
     = θ_{t-1} - α · ∇_θ L - α · λ · θ_{t-1}
     = (1 - α · λ) · θ_{t-1} - α · ∇_θ L
```

This shows why L2 regularization is sometimes called "weight decay" in SGD context.

## Weight Decay

### Definition

**Directly modifies the weight update step** - does NOT add to the loss function:

```
θ_t = θ_{t-1} - α · ∇_θ L - λ · θ_{t-1}
```

The weight decay term is applied **after** computing the gradient update.

### Key Difference

| Aspect | L2 Regularization | Weight Decay |
|--------|------------------|--------------|
| Applied to | Loss function | Weight update |
| Gradient calculation | Modified gradients | Original gradients |
| Momentum interaction | Gradient goes through momentum | Direct weight subtraction |

## Equivalence in SGD

**In vanilla SGD, they are equivalent:**

```
L2:  θ_t = (1 - α·λ) · θ_{t-1} - α · ∇_θ L
WD:  θ_t = (1 - λ) · θ_{t-1} - α · ∇_θ L
```

Set λ_L2 = λ_WD / α, and they produce identical updates.

**This is why they've been used synonymously in literature.**

## Non-Equivalence in Adam

### The Problem with Adam + L2

In Adam, the gradient is processed through momentum:

```
m_t = β₁ · m_{t-1} + (1 - β₁) · (∇_θ L + λ · θ)
v_t = β₂ · v_{t-1} + (1 - β₂) · (∇_θ L + λ · θ)²
θ_t = θ_{t-1} - α · m̂_t / (√v̂_t + ε)
```

**Issue:** The L2 penalty term goes through momentum and adaptive scaling, getting transformed in ways that don't match true weight decay.

### AdamW Solution (Loshchilov & Hutter)

Decouple weight decay from gradient:

```
m_t = β₁ · m_{t-1} + (1 - β₁) · ∇_θ L    # Pure gradient
v_t = β₂ · v_{t-1} + (1 - β₂) · (∇_θ L)²
θ_t = θ_{t-1} - α · m̂_t / (√v̂_t + ε) - λ · θ_{t-1}
```

**Key insight:** Weight decay is applied directly to weights, not through momentum.

## Visual Comparison

```
L2 Regularization with Adam:
  Gradient → Momentum → Adaptive Scaling → Weight Update
     ↑
  Penalty added here, goes through entire chain

Weight Decay with AdamW:
  Gradient → Momentum → Adaptive Scaling → Weight Update
                                              ↑
                                    Direct subtraction here
```

## Experimental Results

Loshchilov & Hutter (2019) showed:

| Optimizer | Top-1 Accuracy (ImageNet) |
|-----------|---------------------------|
| Adam + L2 | ~76% |
| AdamW | ~77-78% |

**AdamW consistently outperforms Adam + L2 regularization.**

## When to Use Each

| Scenario | Recommendation |
|----------|----------------|
| SGD / Momentum | L2 regularization (equivalent to weight decay) |
| Adam | Use **AdamW** with weight decay, NOT Adam + L2 |
| RMSprop | Use weight decay variant (RMSpropW) |
| Adagrad | Weight decay preferred |

## Implementation

### PyTorch - L2 Regularization (Wrong for Adam!)

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)
# This is L2 regularization, NOT true weight decay!
```

### PyTorch - AdamW (Correct!)

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
# This is true decoupled weight decay
```

### TensorFlow / Keras

```python
# TensorFlow 2.x AdamW
optimizer = tfa.optimizers.AdamW(learning_rate=0.001, weight_decay=0.01)
```

## Key Takeaways

1. **L2 regularization ≠ Weight decay** for adaptive optimizers
2. **They ARE equivalent for vanilla SGD** (hence the confusion)
3. **Use AdamW, not Adam + L2** for proper weight decay regularization
4. **Weight decay is applied directly** - not transformed by momentum
5. **Better generalization** with proper weight decay in adaptive methods
6. **Default choice for Adam:** AdamW with weight_decay=0.01

## References

- Loshchilov & Hutter (2019): "Decoupled Weight Decay Regularization" (ICLR 2019)
- PyTorch AdamW documentation
- Hansen & Salamon (1990): Neural network ensembles (original weight decay concept)