# Learning Rate Scheduling (Deep Dive)

**Source:** Multiple sources, Keras documentation, apxml.com
**Category:** Optimization
**Priority:** High
**Read:** 2026-03-10

## Core Concept

**Learning rate scheduling** adjusts the learning rate during training to balance fast convergence (high LR) with stable convergence (low LR).

### Why Scheduling?

| Phase | Learning Rate | Goal |
|-------|---------------|------|
| **Early training** | High | Rapid progress, escape local minima |
| **Mid training** | Medium | Refine weights, avoid oscillation |
| **Late training** | Low | Fine-tune, converge to minimum |

## Common Learning Rate Schedules

### 1. Step Decay

**Definition:** Reduce learning rate by a factor at specific epochs.

**Formula:**
```
η_t = η₀ × γ^(floor(t / drop_rate))
```

**Example:**
```
Initial LR: 0.1
Drop factor: 0.5 every 30 epochs
Epoch 0-29:   LR = 0.1
Epoch 30-59:  LR = 0.05
Epoch 60-89:  LR = 0.025
```

**Advantages:**
- Simple to implement
- Often works well
- Predictable behavior

**Disadvantages:**
- Abrupt changes can destabilize training
- Requires manual tuning of drop points

**Use case:** Classic schedule for CNNs.

### 2. Exponential Decay

**Definition:** Continuously decrease learning rate exponentially.

**Formula:**
```
η_t = η₀ × γ^(t / decay_steps)
```

**Alternative:**
```
η_t = η₀ × e^(-λt)
```

**Advantages:**
- Smooth decrease
- Works well for many problems

**Disadvantages:**
- May decrease too quickly
- Can end with very small LR

**Use case:** General purpose, simple schedule.

### 3. Polynomial Decay

**Definition:** Decrease learning rate polynomially to a minimum.

**Formula:**
```
η_t = (η₀ - η_end) × (1 - t/T)^power + η_end
```

Where:
- T = total training steps
- η_end = final learning rate
- power = polynomial degree (typically 1 or 2)

**Advantages:**
- Smooth decrease
- Controllable end LR
- More flexible than exponential

**Use case:** Common in TensorFlow/Transformer training.

### 4. Cosine Annealing

**Definition:** Follow cosine curve from initial to final LR.

**Formula:**
```
η_t = η_min + (η_max - η_min) × (1 + cos(πt/T)) / 2
```

**Properties:**
- Starts with high LR
- Decreases slowly at first
- Decreases rapidly in middle
- Flattens near minimum

**Advantages:**
- Smooth transition
- "Warm restarts" variant available
- Works well for deep networks

**Use case:** Modern deep learning, transformers.

### 5. Cosine Annealing with Warm Restarts (SGDR)

**Definition:** Cosine annealing with periodic restarts.

**Formula:**
```
η_t = η_min + (η_max - η_min) × (1 + cos(π × T_cur/T_i)) / 2
```

Where:
- T_cur = current epoch within cycle
- T_i = cycle length (may increase with i)

**Key insight:** Restarts help escape local minima.

**Advantages:**
- Can escape local minima
- Often achieves better final accuracy
- Implicit ensembling effect

**Use case:** State-of-the-art image classification.

### 6. Linear Warmup + Decay

**Definition:** Linear increase from 0 to η_max, then decay.

**Formula:**
```
η_t = {
    η_max × t / warmup_steps,     if t < warmup_steps
    schedule(t - warmup_steps),   otherwise
}
```

**Why warmup?**
- Stabilizes early training
- Reduces variance in moment estimates (Adam)
- Essential for Transformers

**Use case:** Transformers, large batch training.

## Comparison Table

| Schedule | Smoothness | Tuning | When to Use |
|----------|------------|--------|-------------|
| **Step** | Abrupt | Manual epochs | CNNs, classic training |
| **Exponential** | Smooth | Decay rate | General purpose |
| **Polynomial** | Smooth | Power, end LR | Transformer pretraining |
| **Cosine** | Smooth | Min LR | Modern deep learning |
| **Cosine + Restarts** | Smooth + jumps | Cycle length | State-of-the-art |
| **Warmup + Decay** | Custom | Warmup steps | Transformers |

## Implementation Examples

### PyTorch

```python
from torch.optim.lr_scheduler import StepLR, ExponentialLR, CosineAnnealingLR

# Step decay
scheduler = StepLR(optimizer, step_size=30, gamma=0.1)

# Exponential decay
scheduler = ExponentialLR(optimizer, gamma=0.95)

# Cosine annealing
scheduler = CosineAnnealingLR(optimizer, T_max=100, eta_min=0)
```

### TensorFlow/Keras

```python
from tensorflow.keras.optimizers.schedules import ExponentialDecay, CosineDecay

# Exponential decay
lr_schedule = ExponentialDecay(
    initial_learning_rate=0.1,
    decay_steps=1000,
    decay_rate=0.96
)

# Cosine decay
lr_schedule = CosineDecay(
    initial_learning_rate=0.1,
    decay_steps=10000
)
```

### Custom Warmup + Cosine

```python
def get_lr(t, warmup_steps, total_steps, max_lr, min_lr):
    if t < warmup_steps:
        return max_lr * t / warmup_steps
    progress = (t - warmup_steps) / (total_steps - warmup_steps)
    return min_lr + (max_lr - min_lr) * (1 + cos(pi * progress)) / 2
```

## Choosing a Schedule

### Guidelines

| Model Type | Recommended Schedule |
|------------|----------------------|
| **CNNs (small)** | Step decay |
| **CNNs (large)** | Cosine + warmup |
| **Transformers** | Linear warmup + cosine/polynomial decay |
| **RNNs** | Exponential or step decay |
| **Large batch training** | Linear warmup + decay |

### Hyperparameters

| Parameter | Typical Range | Tuning Priority |
|-----------|---------------|-----------------|
| **Initial LR** | 10^-5 to 10^-1 | High |
| **Warmup steps** | 0 to 10% of training | Medium |
| **Decay rate** | 0.9 to 0.99 | Medium |
| **Final LR** | 0 to 1% of initial | Low |

## Key Takeaways

1. **Start high, end low** - Fast early progress, fine-tune later
2. **Step decay is classic** - Simple, often good enough
3. **Cosine is modern** - Smooth, works well for deep networks
4. **Warmup for Transformers** - Essential for stability
5. **Restarts help** - Cosine with warm restarts can improve final accuracy
6. **Monitor LR** - Log learning rate to verify schedule

## References

- Smith (2017): "Cyclical Learning Rates"
- Loshchilov & Hutter (2017): "SGDR: Stochastic Gradient Descent with Warm Restarts"
- Goyal et al. (2017): "Large Batch Training of Convolutional Networks"
- Devlin et al. (2019): "BERT: Pre-training of Deep Bidirectional Transformers"