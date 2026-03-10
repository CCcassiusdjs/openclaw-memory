# K-Fold Cross-Validation (Deep Dive)

**Source:** MachineLearningMastery, scikit-learn documentation
**Category:** Model Evaluation
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**K-fold cross-validation** is a resampling procedure to estimate model performance on unseen data by partitioning data into k groups and systematically using each as test set.

### Why Cross-Validation?

**Problem with single train/test split:**
- Single evaluation may be lucky or unlucky
- High variance in performance estimate
- Waste of data (test set not used for training)

**Cross-validation solution:**
- Evaluate model multiple times
- More reliable performance estimate
- Every observation used for both training and testing

## K-Fold Procedure

### Algorithm

```
1. Shuffle dataset randomly
2. Split into k groups (folds)
3. For each fold i = 1 to k:
   a. Use fold i as test set
   b. Use remaining k-1 folds as training set
   c. Fit model on training set
   d. Evaluate on test set
   e. Discard model (keep score only)
4. Summarize: mean ± std of k scores
```

### Key Property

Each observation:
- Used as test **exactly once**
- Used as training **k-1 times**

## Choosing K

### Common Values

| K | Name | Use Case |
|---|------|----------|
| 2 | Train/test split | Quick validation |
| 5 | 5-fold | Smaller datasets |
| 10 | 10-fold | Standard choice |
| n | LOOCV | Very small datasets |

### Bias-Variance Trade-off

| K | Bias | Variance | Computational Cost |
|---|------|----------|---------------------|
| Small (2-3) | High (overestimate skill) | Low | Low |
| Medium (5-10) | Low | Medium | Medium |
| Large (n) | Very Low | High | Very High |

**Empirical recommendation:** K = 5 or 10 provides good balance.

### Choosing K Guidelines

1. **Representative:** Each fold should be statistically representative
2. **Common practice:** K = 10 is widely accepted
3. **Small datasets:** Use LOOCV (K = n)
4. **Large datasets:** K = 5 is sufficient
5. **Even splits:** Prefer K that divides n evenly

## Variations

### 1. Stratified K-Fold

**Purpose:** Preserve class distribution in each fold.

```
Each fold has same proportion of each class as original dataset.
```

**When to use:**
- Imbalanced classification
- Multi-class problems
- Small datasets

### 2. Repeated K-Fold

**Purpose:** Reduce variance through repetition.

```
Repeat k-fold n times with different random splits.
Result: n × k scores (more reliable estimate)
```

**When to use:**
- Need more reliable estimate
- High variance in scores
- Computational resources available

### 3. Leave-One-Out CV (LOOCV)

**Purpose:** Maximum training data, single test observation.

```
K = n (number of observations)
Each fold: n-1 train, 1 test
```

**When to use:**
- Very small datasets (n < 100)
- Maximum training data needed
- Computational resources available

**Trade-off:**
- Low bias (almost all data for training)
- High variance (single observation test)
- High computational cost (n model fits)

### 4. Nested Cross-Validation

**Purpose:** Hyperparameter tuning + unbiased evaluation.

```
Outer loop: Model evaluation
Inner loop: Hyperparameter tuning
```

**Structure:**
```
For each outer fold:
    Split into outer train/test
    For each inner fold:
        Split outer train into inner train/val
        Tune hyperparameters
    Train with best hyperparameters on outer train
    Evaluate on outer test
```

**When to use:**
- Model selection + hyperparameter tuning
- Need unbiased performance estimate
- Sufficient data for nested splits

### 5. Time Series Cross-Validation

**Purpose:** Temporal data where order matters.

```
Fold 1: Train[1:50], Test[51:60]
Fold 2: Train[1:60], Test[61:70]
Fold 3: Train[1:70], Test[71:80]
...
```

**Key constraint:** Training data must precede test data chronologically.

## Important Considerations

### Data Leakage Prevention

**Critical:** All preprocessing must happen within cross-validation loop.

```python
# WRONG - leakage!
X_scaled = StandardScaler().fit_transform(X)
cross_val_score(model, X_scaled, y)

# CORRECT - no leakage
pipeline = Pipeline([('scaler', StandardScaler()), ('model', model)])
cross_val_score(pipeline, X, y)
```

### Model Selection vs. Final Model

**Important distinction:**

```
K-fold CV evaluates MODEL DESIGN, not a particular trained model.
The k models are DISCARDED after evaluation.
Final model is trained on ALL data with best hyperparameters.
```

### Scikit-Learn Implementation

```python
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold

# Basic k-fold
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kfold)

# Stratified (for classification)
skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skfold)

# Summary
print(f"Mean: {scores.mean():.3f} ± {scores.std():.3f}")
```

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Preprocessing before CV | Data leakage, optimistic estimate | Pipeline within CV |
| Using CV for final model | Confusion about model selection | CV for design, retrain on all data |
| Wrong K for imbalanced data | Non-representative folds | Stratified K-fold |
| Not shuffling | Systematic bias | shuffle=True |
| Information leakage | Optimistic estimate | Careful feature engineering |

## Key Takeaways

1. **K-fold CV estimates model skill** on unseen data
2. **K = 5 or 10** is standard (bias-variance balance)
3. **Stratified for classification** - preserve class distribution
4. **No data leakage** - preprocessing inside CV loop
5. **CV evaluates design, not particular model** - models are discarded
6. **Final model on all data** - after hyperparameter selection
7. **Nested CV for tuning** - unbiased hyperparameter selection
8. **Time series special handling** - respect temporal order

## References

- Hastie et al. (2009): "The Elements of Statistical Learning"
- James et al. (2013): "An Introduction to Statistical Learning"
- Kuhn & Johnson (2013): "Applied Predictive Modeling"
- scikit-learn: sklearn.model_selection.KFold