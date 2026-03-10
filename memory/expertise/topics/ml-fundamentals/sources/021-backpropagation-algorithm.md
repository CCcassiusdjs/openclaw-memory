# Backpropagation Algorithm (Deep Dive)

**Source:** CS231n, Wikipedia, GeeksforGeeks
**Category:** Neural Networks / Optimization
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Backpropagation** efficiently computes gradients of a loss function with respect to all parameters in a neural network by recursively applying the chain rule, propagating gradients backward from output to input.

### Problem Statement

Given:
- A neural network with parameters θ
- A loss function L(θ)
- Training data (x, y)

Compute:
- ∂L/∂θ for all parameters θ

**Key insight:** Naive approach would require separate computation for each parameter. Backpropagation computes all gradients in a single forward + backward pass.

## Chain Rule Foundation

### Simple Derivatives

| Operation | Local Gradient |
|-----------|---------------|
| f(x,y) = x·y | ∂f/∂x = y, ∂f/∂y = x |
| f(x,y) = x+y | ∂f/∂x = 1, ∂f/∂y = 1 |
| f(x) = max(x,y) | ∂f/∂x = 1(x≥y), ∂f/∂y = 1(y≥x) |

### Chain Rule for Composed Functions

```
If y = f(x) and z = g(y)
Then: ∂z/∂x = (∂z/∂y) · (∂y/∂x)
```

**Key insight:** Multiply local gradients as you propagate backward.

## Backpropagation Algorithm

### Forward Pass

1. Compute activations layer by layer:
   ```
   z₁ = W₁x + b₁
   a₁ = σ(z₁)
   z₂ = W₂a₁ + b₂
   a₂ = σ(z₂)
   ...
   ```
2. Compute loss L(aₙ, y)

### Backward Pass

1. Compute gradient of loss with respect to output:
   ```
   δₙ = ∂L/∂aₙ
   ```

2. Propagate backward through each layer:
   ```
   For layer l = n-1, n-2, ..., 1:
       ∂L/∂Wₗ = δₗ · aₗ₋₁ᵀ
       ∂L/∂bₗ = δₗ
       δₗ₋₁ = (Wₗᵀ · δₗ) ⊙ σ'(zₗ₋₁)
   ```

Where ⊙ is element-wise multiplication.

## Intuitive Understanding

### Gates as Gradient Signals

Each gate in the computational graph:
1. **Receives** upstream gradient from above
2. **Multiplies** by its local gradient
3. **Passes** result to inputs

**Analogy:** Gates "communicate" whether they want their inputs to increase or decrease, and by how much.

### Common Gate Behaviors

| Gate | Behavior | Gradient Flow |
|------|----------|---------------|
| **Add (+)** | Distribute | Passes gradient equally to all inputs |
| **Max** | Route | Passes gradient to max input only |
| **Multiply (×)** | Swap | Gradient = other input × upstream |

**Example:**
```
x = 3, y = -4
f = x × y = -12

∂f/∂x = y = -4
∂f/∂y = x = 3

If upstream gradient = 1:
  Gradient on x: -4 × 1 = -4
  Gradient on y: 3 × 1 = 3
```

### Scale Sensitivity

**Important:** The scale of inputs affects gradient magnitude:
- If x → 1000x, then ∂f/∂W → 1000x
- Need to adjust learning rate accordingly

**Implication:** Preprocessing matters!

## Staged Computation

### Key Implementation Pattern

**Forward pass:** Cache intermediate values
```python
# Forward pass
z1 = W1 @ x + b1
a1 = relu(z1)
z2 = W2 @ a1 + b2
a2 = sigmoid(z2)
loss = cross_entropy(a2, y)
```

**Backward pass:** Compute gradients in reverse order
```python
# Backward pass
da2 = (a2 - y) / batch_size  # dL/da2
dW2 = da2 @ a1.T             # dL/dW2
db2 = da2.sum(axis=1)        # dL/db2
da1 = W2.T @ da2 * relu_grad(z1)
dW1 = da1 @ x.T
db1 = da1.sum(axis=1)
```

### Implementation Tips

1. **Cache forward values** - Needed for backward pass
2. **Use += for variables used multiple times** - Gradients accumulate
3. **Dimension analysis** - Shapes must align
4. **Work with small examples first** - Then generalize

## Sigmoid Gradient Simplification

**Sigmoid function:**
```
σ(x) = 1 / (1 + e^(-x))
```

**Derivative:**
```
dσ/dx = σ(x) × (1 - σ(x))
```

**Key insight:** Derivative depends only on σ(x), not x directly.

**Implementation:**
```python
# Forward
sigmoid_x = 1.0 / (1.0 + exp(-x))

# Backward (gradient from above: dsigmoid)
dsigmoid = sigmoid_x * (1 - sigmoid_x) * upstream_gradient
```

## Vectorized Operations

### Matrix-Matrix Multiplication

**Forward:**
```
D = W @ X
```

**Backward:**
```python
dW = dD @ X.T
dX = W.T @ dD
```

**Dimension analysis:**
- W: [m × n]
- X: [n × k]
- D: [m × k]
- dW must be [m × n]
- dX must be [n × k]

## Common Patterns

### Pattern 1: Gradient Adds at Forks

If variable is used multiple times:
```python
# Forward
x1 = x + y
x2 = x * z

# Backward - use += for x!
dx = dx1 + dx2  # Not dx = dx1 or dx = dx2
```

### Pattern 2: Max Gate Routes

```python
# Forward
m = max(x, y)

# Backward
if x > y:
    dx = upstream
    dy = 0
else:
    dx = 0
    dy = upstream
```

### Pattern 3: Multiply Swaps

```python
# Forward
f = x * y

# Backward
dx = y * upstream
dy = x * upstream
```

## Key Takeaways

1. **Chain rule is local** - Each gate computes its own gradient independently
2. **Backward flow** - Gradients propagate from output to input
3. **Cache forward values** - Needed for efficient backward pass
4. **Scale matters** - Input scale affects gradient magnitude
5. **Dimension analysis** - Check shapes to verify correctness
6. **Accumulate at forks** - Use += for variables used multiple times
7. **Max routes, add distributes, multiply swaps** - Gate behaviors

## Computational Complexity

| Approach | Complexity |
|----------|------------|
| Naive (one gradient at a time) | O(N²) |
| Backpropagation (all gradients at once) | O(N) |

**N = number of parameters**

**Speedup:** Factor of N (e.g., 1000x faster for network with 1000 parameters)

## References

- LeCun et al. (1989): Original backpropagation paper
- Rumelhart, Hinton, Williams (1986): Backpropagation popularization
- Karpathy (2016): CS231n course notes
- Baydin et al. (2018): "Automatic differentiation in machine learning: a survey"