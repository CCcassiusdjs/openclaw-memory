# Loss Functions for Machine Learning (Deep Dive)

**Source:** ML Glossary, DataCamp, Stack Overflow
**Category:** Optimization / Training
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Loss functions** quantify the difference between predicted and actual values. They guide optimization by providing feedback on model performance.

### Key Properties

1. **Differentiability** - Required for gradient-based optimization
2. **Convexity** - Guarantees global minimum (for some loss functions)
3. **Sensitivity** - How much penalty for wrong predictions

## Regression Loss Functions

### Mean Squared Error (MSE / L2 Loss)

**Formula:**
```
MSE = (1/m) Σ (yᵢ - ŷᵢ)²
```

**Properties:**
- **Range:** [0, +∞)
- **Convex:** Yes
- **Sensitive to outliers:** Yes (quadratic penalty)

**Advantages:**
- Differentiable everywhere
- Well-behaved gradient
- Corresponds to Gaussian noise assumption

**Disadvantages:**
- Outliers have large influence
- Scale-dependent

**Use case:** Regression with Gaussian noise

### Mean Absolute Error (MAE / L1 Loss)

**Formula:**
```
MAE = (1/m) Σ |yᵢ - ŷᵢ|
```

**Properties:**
- **Range:** [0, +∞)
- **Convex:** Yes
- **Sensitive to outliers:** Less than MSE

**Advantages:**
- Robust to outliers
- Linear penalty (not quadratic)

**Disadvantages:**
- Not differentiable at 0
- No unique solution (median)

**Use case:** Regression with outliers

### Huber Loss

**Formula:**
```
Lδ(y, ŷ) = {
    (1/2)(y - ŷ)²           if |y - ŷ| ≤ δ
    δ|y - ŷ| - (1/2)δ²      otherwise
}
```

**Properties:**
- **Hybrid:** MSE near zero, MAE far from zero
- **Parameter δ:** Controls transition point

**Advantages:**
- Combines benefits of MSE and MAE
- Differentiable everywhere
- Robust to outliers

**Use case:** Robust regression

### RMSE (Root Mean Square Error)

**Formula:**
```
RMSE = √(MSE) = √((1/m) Σ (yᵢ - ŷᵢ)²)
```

**Properties:**
- Same units as target variable
- More interpretable than MSE

## Classification Loss Functions

### Binary Cross-Entropy (Log Loss)

**Formula:**
```
BCE = -(y log(p) + (1-y) log(1-p))
```

Where:
- y ∈ {0, 1} (true label)
- p ∈ [0, 1] (predicted probability)

**Properties:**
- **Range:** [0, +∞)
- **Convex:** Yes
- **Penalizes confidence + wrongness heavily**

**Advantages:**
- Proper scoring rule
- Corresponds to maximum likelihood
- Well-behaved gradient

**Use case:** Binary classification with sigmoid output

### Categorical Cross-Entropy

**Formula:**
```
CE = -Σc yc log(pc)
```

Where:
- yc ∈ {0, 1} (one-hot true label)
- pc ∈ [0, 1] (predicted probability for class c)

**Properties:**
- Multi-class extension of binary cross-entropy
- Combined with softmax output

**Use case:** Multi-class classification with softmax

### Hinge Loss (SVM)

**Formula:**
```
L(y, f(x)) = max(0, 1 - y·f(x))
```

Where y ∈ {-1, +1}

**Properties:**
- **Range:** [0, +∞)
- **Convex:** Yes
- **Not differentiable at y·f(x) = 1**

**Advantages:**
- Maximum margin classification
- Sparse gradients (many zeros)

**Use case:** SVM, large margin classifiers

### Focal Loss

**Formula:**
```
FL = -α(1-p)^γ log(p)
```

Where:
- α: Weighting factor for class balance
- γ: Focusing parameter (typically 2)

**Advantages:**
- Handles class imbalance
- Focuses on hard examples
- Down-weights easy examples

**Use case:** Object detection (RetinaNet), class imbalance

## Loss Function Comparison

| Task | Loss Function | Use Case |
|------|---------------|----------|
| **Regression** | MSE | Gaussian noise, no outliers |
| **Regression** | MAE | Robust to outliers |
| **Regression** | Huber | Robust + differentiable |
| **Binary Classification** | BCE | Standard binary |
| **Multi-class** | Categorical CE | Standard multi-class |
| **SVM** | Hinge | Maximum margin |
| **Imbalanced** | Focal | Class imbalance |

## Why Cross-Entropy for Classification?

### Probabilistic Interpretation

Cross-entropy comes from maximum likelihood estimation:

```
MLE: maximize Π p(yᵢ|xᵢ)ᵗᵢ(1-p(yᵢ|xᵢ))^(1-tᵢ)
Log-likelihood: maximize Σ tᵢ log(pᵢ) + (1-tᵢ) log(1-pᵢ)
Minimize negative: BCE loss
```

**Key insight:** Cross-entropy is the log-likelihood of the Bernoulli distribution.

### Why Not MSE for Classification?

1. **Non-convex** with sigmoid/softmax (local minima)
2. **Saturated gradients** for confident predictions
3. **Cross-entropy has better gradient properties** for classification

## Gradient Properties

### MSE Gradient
```
∂MSE/∂ŷ = (2/m)(ŷ - y)
```
- Linear gradient
- Well-behaved

### Cross-Entropy + Sigmoid Gradient
```
∂CE/∂z = σ(z) - y  (where z is pre-activation)
```
- Beautiful simplification
- Gradient proportional to error
- No saturation for sigmoid

### Cross-Entropy + Softmax Gradient
```
∂CE/∂zⱼ = pⱼ - yⱼ
```
- Gradient = prediction - true label
- Elegant and efficient

## Key Takeaways

1. **MSE for regression** - Standard choice, quadratic penalty
2. **MAE for robust regression** - Robust to outliers
3. **Huber for best of both** - MSE near zero, MAE far
4. **Cross-entropy for classification** - Proper scoring rule, good gradients
5. **Match loss to task** - Consider noise distribution, outliers, class balance
6. **Cross-entropy + sigmoid/softmax** - Gradient simplifies beautifully
7. **Focal loss for imbalance** - Focuses on hard examples

## References

- Bishop (2006): "Pattern Recognition and Machine Learning"
- Goodfellow et al. (2016): "Deep Learning" - Chapter on Optimization
- Lin et al. (2017): "Focal Loss for Dense Object Detection"