# Momentum and Nesterov Accelerated Gradient (Deep Dive)

**Source:** jlmelville.github.io - https://jlmelville.github.io/mize/nesterov.html
**Category:** Optimization
**Priority:** High (Technical Implementation)
**Read:** 2026-03-10

## Core Concept

Momentum accelerates gradient descent by accumulating a velocity vector in directions of persistent reduction, helping escape shallow local minima and accelerate convergence.

### Classical Momentum (CM)

```
v_{t+1} = μ_t · v_t - ε_t · ∇f(θ_t)
θ_{t+1} = θ_t + v_{t+1}
```

Where:
- v = velocity vector (accumulated gradient)
- μ = momentum coefficient (typically 0.9)
- ε = learning rate
- ∇f(θ_t) = gradient at current parameters

**Intuition:** Like a ball rolling downhill, accumulating speed in consistent directions.

### Nesterov Accelerated Gradient (NAG)

The key insight: **compute gradient at the "looked-ahead" position**

```
θ_{t+1} = θ_t + s_t + μ(θ_t + s_t - θ_{t-1} - s_{t-1})
```

Where s_t = -ε_t · ∇f(θ_t) (the steepest descent step).

**Equivalent formulation (Sutskever):**
```
θ_{t+1} = θ_t + μ_t · v_t - ε_t · ∇f(θ_t + μ_t · v_t)
```

The gradient is computed at the **future position** (after momentum step), then corrected.

## Sutskever Formulation (Practical Implementation)

Reinterpret NAG as momentum first, then gradient:

```
v_{t+1} = μ_t · v_t - ε_t · ∇f(θ_t + μ_t · v_t)
θ_{t+1} = θ_t + v_{t+1}
```

**Implementation steps:**
1. Compute velocity: v_new = μ · v
2. Move parameters: θ_temp = θ + v_new
3. Compute gradient at θ_temp
4. Apply gradient correction: θ_final = θ_temp - ε · ∇f(θ_temp)

## Bengio Formulation

Another equivalent expression:

```
θ_{t+1} = θ_t + μ_{t-1} · μ_t · b_t - (1 + μ_t) · ε_t · ∇f(θ_t)
```

Where b_t = θ_t - μ_{t-1} · b_{t-1} - ε_{t-1} · ∇f(θ_{t-1})

**Key insight:** The Bengio formulation doesn't require computing gradient at non-standard position.

## Key Differences: CM vs NAG

### Unrolled Weights

After 4 iterations, the weights applied to gradients:

| Momentum Type | s_3 | s_2 | s_1 | s_0 |
|--------------|-----|-----|-----|-----|
| Classical | 1 | μ | μ² | μ³ |
| NAG | 1+μ | μ² | μ³ | μ⁴ |

**NAG places more weight on recent gradients** → faster adaptation to changing landscape.

### Weight Comparison (High Momentum μ=0.9)

| Momentum Type | Current Gradient Weight |
|---------------|----------------------|
| Classical CM | ~29% |
| NAG | ~46% |

**NAG "forgets" old gradients faster**, responding more to current landscape.

## Why NAG Works Better

1. **Lookahead correction** → If momentum would overshoot, gradient correction brings it back
2. **Escaping ravines** → NAG oscillates less in steep narrow valleys
3. **Anticipatory** → Uses gradient at where parameters *will be*, not where they *are*

### Visual Analogy

- **Classical Momentum**: Ball rolling down, using velocity from past
- **NAG**: Ball "peeking" ahead, seeing where velocity would take it, then correcting course

## Variants and Generalizations

### Dozat Nesterov Momentum (NAdam)

Used in Adam optimizer with Nesterov momentum:

```
m'_{t+1} = μ_{t-1} · m'_t + s_t
v_{t+1} = μ_t · m'_{t+1} + s_t
```

**Key insight:** Separates the momentum coefficient for history vs current update.

### Quasi-Hyperbolic Momentum (QHM)

Generalizes CM and NAG:

```
q_{t+1} = ν_t · q_t + s_t
v_{t+1} = μ_t · q_{t+1} + s_t
```

- ν_t = 0 → Steepest descent (nearly)
- ν_t = μ_{t-1} → Nesterov momentum
- ν_t = 1 → Classical momentum (nearly)

### Unified Momentum (Zou et al. 2018)

```
v_{t+1} = μ_t · v_t - ε_t · ∇f(θ_t) + β_t · μ_t · (s_{t-1} - s_t)
```

- β = 0 → Classical momentum
- β = 1 → Nesterov

## Practical Implementation Notes

### First Iteration Handling

On first iteration, there's no momentum history:
- **Option 1:** Use (1+μ)·s_0 (long step)
- **Option 2:** Use s_0 only (short step, matches CM)

Recommendation: Use the long step for consistency with NAG's theoretical formulation.

### Momentum Schedules

When μ varies (e.g., learning rate schedules), the relationship between CM and NAG weights becomes more complex:
- Each gradient needs re-weighting by different μ_t
- Not a simple re-parameterization of CM

### Convergence Guarantees

NAG has **optimal convergence rate** for convex functions:
- O(1/t²) vs O(1/t) for standard gradient descent
- Requires specific learning rate and momentum schedules for theory

## Key Takeaways

1. **Momentum accelerates convergence** by accumulating velocity in consistent directions
2. **NAG computes gradient at "looked-ahead" position** → anticipatory correction
3. **NAG weights recent gradients more** → adapts faster to changing landscape
4. **Multiple equivalent formulations** → Sutskever, Bengio, Dozat implementations
5. **Practical benefit** → Less oscillation in ravines, faster convergence
6. **Theoretical advantage** → Optimal convergence rate for convex functions

## When to Use

| Scenario | Recommendation |
|----------|---------------|
| Deep neural networks | NAG (or Adam with Nesterov) |
| Stochastic optimization | Momentum with schedule |
| Convex optimization | NAG with theoretical learning rates |
| Simple problems | Either CM or NAG works |

## References

- Sutskever et al. (2013): "On the importance of initialization and momentum in deep learning"
- Bengio et al. (2012): "Advances in optimizing recurrent networks"
- Dozat (2016): "Incorporating Nesterov momentum into Adam"
- Zou et al. (2018): "Unified stochastic momentum"