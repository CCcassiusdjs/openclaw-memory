# Decision Tree Algorithms: ID3, C4.5, CART (Deep Dive)

**Source:** bitmask93.github.io, GeeksforGeeks
**Category:** Classical ML Algorithms
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Decision Trees** create hierarchical decision rules by recursively splitting data based on feature values, forming a tree structure where:
- **Internal nodes** = Tests on attributes
- **Branches** = Outcomes of tests
- **Leaf nodes** = Class labels (classification) or values (regression)

## ID3 Algorithm (Iterative Dichotomiser 3)

### Overview
- **Introduced by:** Quinlan Ross (1986)
- **Purpose:** Classification (categorical features only)
- **Splitting criterion:** Information Gain (based on entropy)

### Algorithm Steps

```
1. If all instances belong to same class → create leaf with that class
2. If no more attributes to test → create leaf with majority class
3. Else:
   a. Calculate Information Gain for each attribute
   b. Select attribute with maximum Information Gain
   c. Create decision node for that attribute
   d. Recursively apply to each subset
```

### Entropy and Information Gain

**Entropy** (measure of impurity):
```
H(S) = -Σ pᵢ log₂(pᵢ)
```

Where pᵢ = proportion of class i in set S.

**Information Gain** for attribute A:
```
Gain(S, A) = H(S) - Σ (|Sᵥ|/|S|) × H(Sᵥ)
```

Where Sᵥ = subset where attribute A has value v.

### ID3 Limitations

1. **Bias toward multi-valued attributes** - Attributes with many values get preference
2. **Only categorical features** - Cannot handle continuous values
3. **No pruning** - Prone to overfitting
4. **No missing values handling**

## C4.5 Algorithm

### Overview
- **Extension of:** ID3
- **Improvements:** Handles continuous features, missing values, pruning
- **Splitting criterion:** Gain Ratio

### Key Improvements over ID3

| Feature | ID3 | C4.5 |
|---------|-----|------|
| Continuous features | ❌ | ✅ |
| Missing values | ❌ | ✅ |
| Pruning | ❌ | ✅ (post-pruning) |
| Splitting criterion | Information Gain | Gain Ratio |

### Gain Ratio

**Intrinsic Value** (split information):
```
IV(A) = -Σ (|Sᵥ|/|S|) × log₂(|Sᵥ|/|S|)
```

**Gain Ratio:**
```
GainRatio(S, A) = Gain(S, A) / IV(A)
```

**Purpose:** Penalizes attributes with many values, reducing bias.

### Continuous Features

For numerical attribute A:
1. Sort values
2. Find threshold h that maximizes Gain Ratio
3. Create binary split: A ≤ h and A > h

### Missing Values

- Marked separately, not used in calculations
- Fractional weights assigned during split

## CART (Classification and Regression Trees)

### Overview
- **Binary splits only** (unlike ID3/C4.5 which can have multiple branches)
- **Classification AND regression** (unlike ID3 which is classification only)
- **Splitting criterion:** Gini impurity (classification), MSE (regression)

### Gini Impurity

```
Gini(S) = 1 - Σ pᵢ²
```

Where pᵢ = proportion of class i.

**Gini for split:**
```
Gini_split = Σ (|Sᵥ|/|S|) × Gini(Sᵥ)
```

Select split that minimizes Gini_split.

### CART for Regression

- **Prediction:** Mean or median of samples in leaf
- **Splitting criterion:** Minimize sum of squared errors (SSE) or absolute errors

```
SSE = Σ (yᵢ - ȳ)²
```

Where ȳ = mean of samples in node.

### CART Features

| Feature | Description |
|---------|-------------|
| Binary splits | Always two branches |
| Numerical features | Native support |
| Categorical features | One-vs-rest splits |
| Linear combination splits | Optional (less interpretable) |

## Pruning Techniques

### Why Prune?

Overfitting occurs when:
- Tree is too deep
- Leaves contain very few samples
- Model memorizes training data

### Post-Pruning (After Tree Construction)

**1. Reduced Error Pruning (REP)**
- Requires separate validation set
- Replace subtree with leaf if it improves validation accuracy
- Simple but requires extra data

**2. Cost-Complexity Pruning (CCP)**
- Generate sequence of pruned trees
- Balance tree complexity vs accuracy
- Select tree using cross-validation or validation set

**Cost-complexity measure:**
```
Rα(T) = R(T) + α × |T|
```

Where R(T) = misclassification rate, |T| = number of leaves, α = complexity parameter.

### Pre-Pruning (During Tree Construction)

Stop growing when:
- Node samples < threshold
- All samples same class
- Information gain < threshold
- Tree depth > threshold

**Chi-square pruning:**
- Statistical test for split significance
- Reject split if not statistically significant (p-value > α)

## Algorithm Comparison

| Aspect | ID3 | C4.5 | CART |
|--------|-----|------|------|
| Split type | Multi-way | Multi-way | Binary only |
| Features | Categorical | Both | Both |
| Criterion | Info Gain | Gain Ratio | Gini/MSE |
| Pruning | None | Post-pruning | Cost-complexity |
| Missing values | No | Yes | Surrogate splits |
| Tasks | Classification | Classification | Both |

## Key Takeaways

1. **ID3 is simplest** - Uses Information Gain, categorical only
2. **C4.5 improves ID3** - Gain Ratio, continuous features, pruning
3. **CART is most general** - Binary splits, both tasks, Gini/MSE
4. **Pruning essential** - Prevents overfitting
5. **Pre-pruning faster** - But may miss optimal splits
6. **Post-pruning more accurate** - But requires more computation/data

## References

- Quinlan (1986): ID3 original paper
- Quinlan (1993): C4.5: Programs for Machine Learning
- Breiman et al. (1984): CART: Classification and Regression Trees