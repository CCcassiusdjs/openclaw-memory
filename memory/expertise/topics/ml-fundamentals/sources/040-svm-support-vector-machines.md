# Support Vector Machines (SVM) - Deep Dive

**Source:** Wikipedia, Columbia University, GeeksforGeeks
**Category:** Classical ML Algorithms
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Support Vector Machines (SVM)** are supervised max-margin models that find the optimal hyperplane to separate data into classes by maximizing the margin between the hyperplane and the nearest data points (support vectors).

### Maximum Margin Principle

The goal is to find the hyperplane that:
1. **Separates the classes** (correct classification)
2. **Maximizes the margin** (distance to nearest points)
3. **Is robust to noise** (max-margin property)

## Mathematical Formulation

### Linear SVM (Hard Margin)

For linearly separable data, find w and b that:

```
Minimize: ½ ||w||²
Subject to: yᵢ(w·xᵢ + b) ≥ 1 for all i
```

**Geometric margin:** 2/||w||

**Support vectors:** Points where yᵢ(w·xᵢ + b) = 1 (exactly on the margin)

### Linear SVM (Soft Margin)

For non-linearly separable data, introduce slack variables ξᵢ:

```
Minimize: ½ ||w||² + C Σ ξᵢ
Subject to: yᵢ(w·xᵢ + b) ≥ 1 - ξᵢ, ξᵢ ≥ 0
```

**C parameter:** Trade-off between margin size and classification errors
- **Large C:** Penalize misclassification heavily → smaller margin
- **Small C:** Allow more misclassification → larger margin

## Kernel Trick

### Why Kernels?

Data may not be linearly separable in original space. Solution:
1. Map data to higher-dimensional space: φ(x)
2. Find linear hyperplane in that space
3. Non-linear boundary in original space

### The Trick

Instead of computing φ(x) explicitly, use kernel function:

```
K(x, x') = φ(x)·φ(x')
```

**Key insight:** Only need inner products between data points, not the explicit mapping.

### Common Kernels

| Kernel | Formula | Use Case |
|--------|---------|----------|
| **Linear** | K(x, x') = x·x' | Linearly separable data |
| **Polynomial** | K(x, x') = (x·x' + c)ᵈ | Polynomial boundaries |
| **RBF (Gaussian)** | K(x, x') = exp(-γ||x - x'||²) | General purpose, most common |
| **Sigmoid** | K(x, x') = tanh(κx·x' + c) | Neural network interpretation |

### RBF Kernel (Most Popular)

```
K(x, x') = exp(-γ||x - x'||²)
```

**γ (gamma) parameter:**
- **Large γ:** Narrow RBF → complex boundaries → overfitting risk
- **Small γ:** Wide RBF → smooth boundaries → underfitting risk

## Dual Problem

### Primal vs Dual

**Primal:** Minimize over w, b, ξ
**Dual:** Maximize over α (Lagrange multipliers)

```
Maximize: Σ αᵢ - ½ Σᵢ Σⱼ αᵢαⱼyᵢyⱼK(xᵢ, xⱼ)
Subject to: 0 ≤ αᵢ ≤ C, Σ αᵢyᵢ = 0
```

**Key properties:**
1. Only support vectors have αᵢ > 0 (others are 0)
2. Kernel appears only as K(xᵢ, xⱼ) → kernel trick applies
3. Number of support vectors << number of training samples

## Support Vectors

**Definition:** Training points where αᵢ > 0

**Properties:**
- They lie on or inside the margin
- The decision boundary depends ONLY on support vectors
- Removing non-support vectors doesn't change the boundary

**Decision function:**
```
f(x) = sign(Σᵢ αᵢyᵢK(xᵢ, x) + b)
```

Sum only over support vectors (αᵢ > 0).

## Hinge Loss

### Definition

```
L(y, f(x)) = max(0, 1 - y·f(x))
```

**Interpretation:**
- If y·f(x) ≥ 1: Loss = 0 (correctly classified with margin)
- If y·f(x) < 1: Loss = 1 - y·f(x) (penalty proportional to distance)

**Soft margin SVM minimizes:**
```
½ ||w||² + C Σ hinge_loss(yᵢ, f(xᵢ))
```

## SVM vs Other Classifiers

| Aspect | SVM | Logistic Regression | Perceptron |
|--------|-----|---------------------|------------|
| Margin | Maximum | Not explicit | Any separating |
| Loss | Hinge | Log-loss | 0-1 loss |
| Probabilities | Not directly | Yes | No |
| Outliers | Robust (margin) | Sensitive | Sensitive |
| Kernel | Native | Requires approximation | No |

## Multiclass SVM

### Approaches

1. **One-vs-All (OvA):** Train K classifiers, one per class
2. **One-vs-One (OvO):** Train K(K-1)/2 classifiers, vote
3. **Direct multiclass:** Single optimization (Crammer & Singer)

## SVM Regression (SVR)

### Objective

Find f(x) = w·x + b such that:
- |yᵢ - f(xᵢ)| ≤ ε for all training points
- Minimize ||w||²

**ε-insensitive loss:**
```
L(y, f(x)) = max(0, |y - f(x)| - ε)
```

Points within ε of the predicted value contribute 0 loss.

## Key Takeaways

1. **Maximum margin principle** - Find hyperplane with largest margin
2. **Kernel trick** - Implicit mapping to high-dimensional space
3. **Support vectors matter** - Only points near boundary affect model
4. **C controls regularization** - Trade-off margin vs misclassification
5. **RBF is default kernel** - Works well for most problems
6. **Scale matters** - Normalize features before SVM
7. **Hinge loss** - Robust to outliers, sparse gradients
8. **Dual problem enables kernels** - Only need inner products

## Hyperparameter Tuning

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| **C** | Regularization | 10⁻³ to 10³ |
| **γ (RBF)** | RBF width | 10⁻³ to 10³ |
| **ε (SVR)** | Insensitivity zone | 0.01 to 0.5 |
| **degree (Poly)** | Polynomial degree | 2 to 5 |

**Grid search:** Use exponential scales (2⁻³, 2⁻¹, 2¹, 2³, ...)

## References

- Cortes & Vapnik (1995): Original SVM paper
- Boser, Guyon, Vapnik (1992): Kernel trick for SVM
- Vapnik (1998): Statistical Learning Theory
- Schölkopf & Smola (2002): Learning with Kernels