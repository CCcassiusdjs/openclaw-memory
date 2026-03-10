# Cosine Annealing with Warmup

**Source:** gaohongnan.com - https://www.gaohongnan.com/playbook/training/why_cosine_annealing_warmup_stabilize_training.html
**Category:** Learning Rate Scheduling
**Priority:** High (Practical Training)
**Read:** 2026-03-10

## Core Concept

**Cosine Annealing with Warmup** is a learning rate schedule that combines:
1. **Warmup phase:** Linear increase from 0 to max learning rate
2. **Cosine decay phase:** Smooth decrease following a cosine curve

### Mathematical Definition

**Learning rate multiplier α_t:**

```
α_t = {
    t / t_warmup                                    if t < t_warmup
    α_f + (1 - α_f) × (1 + cos(π × τ_w)) / 2       otherwise
}
```

Where:
- t = current step
- t_warmup = warmup duration (steps)
- t_max = total training steps
- τ_w = (t - t_warmup) / t_max (fraction of post-warmup time)
- α_f = final learning rate multiplier (e.g., 0.1)
- η_max = initial (max) learning rate

**Actual learning rate:**
```
η_t = α_t × η_max
```

## Why Warmup Works

### Problem: Early Training Instability

In early training:
1. **Adam optimizer** has high variance in bias correction factors
2. **Transformers** can have very high gradients in first iterations
3. **Large learning rates** can destabilize training immediately

### Solution: Warmup

**RAdam paper insight:** Warmup acts as a **variance reduction technique**, stabilizing bias correction in Adam.

**Key mechanism:**
- Early steps have high variance in moment estimates
- Warmup allows estimates to stabilize before full learning rate
- Reduces variance in adaptive learning rates

## Why Cosine Annealing

### Properties of Cosine Schedule

1. **Gentle start:** Starts with gradual decrease (not steep)
2. **Smooth end:** Flattens near zero (fine-tuning)
3. **Theoretical support:** Loshchilov & Hutter (SGDR paper)

### Comparison with Other Schedules

| Schedule | Start | End | Shape |
|----------|-------|-----|-------|
| Step decay | Abrupt drops | Abrupt | Discontinuous |
| Linear decay | Steep | Linear | Linear |
| Exponential decay | Steep | Exponential | Curved |
| Cosine annealing | Gentle | Smooth | Cosine curve |

### Visual Comparison

```
Learning Rate
    ↑
η_max │╮
      │ ╲
      │  ╲
      │   ╲        ← Cosine: gentle start, smooth end
      │    ╲___
      │        ───
η_min │            ───
      └────────────────→ Training Steps
        Warmup   Decay
```

## Warmup Phase Details

### Linear Increase

```
α_t = t / t_warmup
η_t = α_t × η_max
```

**Example (η_max = 3e-4, t_warmup = 5):**

| Step | α_t | η_t |
|------|-----|-----|
| 1 | 0.2 | 6e-5 |
| 2 | 0.4 | 1.2e-4 |
| 3 | 0.6 | 1.8e-4 |
| 4 | 0.8 | 2.4e-4 |
| 5 | 1.0 | 3e-4 |

## Cosine Decay Phase Details

### Formula Breakdown

```
α_t = α_f + (1 - α_f) × (1 + cos(π × τ_w)) / 2
```

**At τ_w = 0 (start of decay):**
- cos(0) = 1
- α_t = α_f + (1 - α_f) × (1 + 1) / 2 = α_f + (1 - α_f) = 1

**At τ_w = 1 (end of training):**
- cos(π) = -1
- α_t = α_f + (1 - α_f) × (1 - 1) / 2 = α_f

### Mathematical Insight

The formula ensures:
- **Start:** α_t = 1 (full learning rate)
- **End:** α_t = α_f (scaled minimum)
- **Shape:** Smooth cosine transition

**Example (η_max = 3e-4, t_warmup = 5, t_max = 10, α_f = 0.5):**

| Step | τ_w | cos(π × τ_w) | α_t | η_t |
|------|-----|--------------|-----|-----|
| 6 | 0.1 | cos(0.1π) ≈ 0.951 | 0.975 | 2.93e-4 |
| 7 | 0.2 | cos(0.2π) ≈ 0.809 | 0.905 | 2.72e-4 |
| 8 | 0.3 | cos(0.3π) ≈ 0.588 | 0.794 | 2.38e-4 |
| 9 | 0.4 | cos(0.4π) ≈ 0.309 | 0.655 | 1.96e-4 |
| 10 | 0.5 | cos(0.5π) = 0 | 0.500 | 1.50e-4 |

## PyTorch Implementation

```python
from torch.optim.lr_scheduler import LambdaLR
import math

def get_cosine_annealing_with_warmup(
    optimizer, 
    num_warmup_steps, 
    num_training_steps, 
    alpha_f=0.1
):
    def lr_lambda(current_step):
        if current_step < num_warmup_steps:
            return current_step / num_warmup_steps
        tau_w = (current_step - num_warmup_steps) / num_training_steps
        tau_w = min(1.0, tau_w)
        return alpha_f + (1 - alpha_f) * (1 + math.cos(math.pi * tau_w)) / 2
    
    return LambdaLR(optimizer, lr_lambda)
```

## Equivalence with PyTorch CosineAnnealingLR

PyTorch's formula:
```
η_t = η_min + (η_max - η_min) × (1 + cos(t × π / t_max)) / 2
```

Setting η_min = α_f × η_max:
```
η_t = α_f × η_max + (η_max - α_f × η_max) × (1 + cos(...)) / 2
    = η_max × (α_f + (1 - α_f) × (1 + cos(...)) / 2)
    = α_t × η_max
```

**Key equivalence:** PyTorch's η_min corresponds to α_f × η_max.

## Oscillation vs Single Cycle

### Single Cycle (No Oscillation)
- Set t_max to cover exactly one half-cycle
- Learning rate monotonically decreases after warmup
- Most common configuration

### Multiple Cycles (Oscillation)
- Allow t_max to span multiple cosine periods
- Learning rate decreases then increases
- Requires restart mechanism (CosineAnnealingWarmRestarts)

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Transformers | Use warmup (essential for stability) |
| Large batch training | Use warmup + cosine |
| Transfer learning | May skip warmup, use cosine |
| Small models | Simple cosine or step decay |
| Very long training | Consider warm restarts |

## Key Takeaways

1. **Warmup stabilizes early training** - Reduces variance in moment estimates
2. **Cosine shape is principled** - Gentle start, smooth end
3. **Two-phase schedule** - Linear warmup → cosine decay
4. **α_f controls final LR** - Typically 0.1 (10% of max)
5. **Essential for Transformers** - Prevents early training divergence
6. **PyTorch equivalent** - CosineAnnealingLR + manual warmup

## References

- Loshchilov & Hutter (2016): "SGDR: Stochastic Gradient Descent with Restarts"
- Liu et al. (2019): "On the Variance of the Adaptive Learning Rate and Beyond" (RAdam)
- Zhang et al. (2023): "Dive into Deep Learning" - Chapter 12.11