# Adam Optimizer (Adaptive Moment Estimation)

**Source:** Multiple - Kingma & Ba (2015), GeeksforGeeks, apxml.com
**Category:** Optimization
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Adam** (Adaptive Moment Estimation) combines two key ideas:
1. **Momentum** - Accelerates gradient descent using exponentially weighted average of past gradients
2. **RMSprop** - Adapts learning rate per parameter using exponentially weighted average of squared gradients

### Update Rule

```
m_t = β₁ · m_{t-1} + (1 - β₁) · g_t         # First moment (mean of gradients)
v_t = β₂ · v_{t-1} + (1 - β₂) · g_t²        # Second moment (uncentered variance)
m̂_t = m_t / (1 - β₁^t)                      # Bias-corrected first moment
v̂_t = v_t / (1 - β₂^t)                      # Bias-corrected second moment
θ_t = θ_{t-1} - α · m̂_t / (√v̂_t + ε)       # Parameter update
```

Where:
- g_t = gradient at step t
- m_t = first moment estimate (momentum)
- v_t = second moment estimate (RMSprop-like)
- β₁, β₂ = exponential decay rates (typically β₁=0.9, β₂=0.999)
- α = learning rate (typically 0.001)
- ε = small constant for numerical stability (typically 10^-8)

## Key Components

### 1. First Moment (Momentum)

```
m_t = β₁ · m_{t-1} + (1 - β₁) · g_t
```

- Exponentially weighted moving average of gradients
- **Purpose:** Accelerate in consistent directions, dampen oscillations
- Similar to classical momentum but with (1 - β₁) coefficient

### 2. Second Moment (RMSprop-like)

```
v_t = β₂ · v_{t-1} + (1 - β₂) · g_t²
```

- Exponentially weighted moving average of squared gradients
- **Purpose:** Adaptive learning rate per parameter
- Larger gradients → larger denominator → smaller effective step
- Smaller gradients → smaller denominator → larger effective step

### 3. Bias Correction

```
m̂_t = m_t / (1 - β₁^t)
v̂_t = v_t / (1 - β₂^t)
```

**Why needed:** Initial moments m_0 and v_0 are initialized to zero, causing bias toward zero in early steps.

**Effect:** Corrects for initialization bias, especially important early in training.

## Properties

### Invariant Properties

1. **Scale invariant:** Gradients scaled by factor c → m scaled by c, v scaled by c² → update unchanged
2. **Step size invariant:** Effective step size Δ_t is invariant to gradient scale

### Automatic Annealing

Near optimum:
- Signal-to-noise ratio (SNR) → 0
- m_t → 0, v_t stays bounded
- Effective step size decreases automatically

## Hyperparameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| α (learning rate) | 0.001 | Step size |
| β₁ | 0.9 | First moment decay rate |
| β₂ | 0.999 | Second moment decay rate |
| ε | 10^-8 | Numerical stability constant |

### Tuning Recommendations

- **α:** Often left at default; can use 0.0001 for fine-tuning
- **β₁:** Rarely changed from 0.9
- **β₂:** Rarely changed from 0.999
- **ε:** Keep at 10^-8 for numerical stability

## Comparison with Other Optimizers

| Optimizer | Momentum | Adaptive LR | Memory |
|-----------|----------|-------------|--------|
| SGD | No | No | O(1) |
| SGD + Momentum | Yes | No | O(n) |
| RMSprop | No | Yes | O(n) |
| Adam | Yes | Yes | O(2n) |

### Advantages over SGD

1. **Per-parameter learning rates** - Adapts to sparse gradients
2. **Momentum built-in** - No separate momentum hyperparameter
3. **Bias correction** - Robust to initialization
4. **Works well with sparse gradients** - Good for NLP, embeddings

### Disadvantages

1. **Memory overhead** - Stores both m and v (2× memory)
2. **Can overshoot** - Especially in late training
3. **Weight decay issues** - L2 regularization not equivalent to weight decay (use AdamW)

## AdamW (Decoupled Weight Decay)

**Key insight from Loshchilov & Hutter (2019):**

Adam with L2 regularization ≠ Adam with weight decay

**Solution:** AdamW decouples weight decay from gradient-based update

```
θ_t = θ_{t-1} - α · m̂_t / (√v̂_t + ε) - λ · θ_{t-1}
```

Where λ is the weight decay coefficient.

**Benefit:** True weight decay regularization, not transformed by momentum.

## When to Use Adam

### Good For
- Sparse gradients (NLP, embeddings)
- Non-stationary objectives
- Noisy gradients
- Default choice for many problems
- Quick prototyping

### Consider Alternatives
- When memory is constrained → SGD + Momentum
- When best generalization needed → SGD (often better final accuracy)
- For vision tasks with large batches → SGD + Momentum

## Key Takeaways

1. **Combines momentum and adaptive LR** - Best of both worlds
2. **Bias correction essential** - Especially in early training
3. **Scale invariant** - Robust to gradient magnitude
4. **Default hyperparameters work well** - Rarely need tuning
5. **Use AdamW for weight decay** - Not Adam with L2 regularization
6. **Memory overhead** - Stores 2× parameters vs SGD
7. **Great default choice** - Works well across many domains

## References

- Kingma & Ba (2015): "Adam: A Method for Stochastic Optimization" (ICLR 2015)
- Loshchilov & Hutter (2019): "Decoupled Weight Decay Regularization"
- Reddi et al. (2018): "On the Convergence of Adam and Beyond"