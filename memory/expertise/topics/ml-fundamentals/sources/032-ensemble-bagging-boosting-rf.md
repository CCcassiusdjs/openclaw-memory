# Ensemble Methods: Bagging, Boosting, Random Forest

**Source:** Sebastian Raschka, scikit-learn documentation
**Category:** Ensemble Learning
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Ensemble methods** combine multiple models to achieve better predictive performance than any single model alone.

### Why Ensemble?

| Problem | Single Model | Ensemble Solution |
|---------|-------------|-------------------|
| Overfitting (high variance) | Decision trees memorize data | Bagging → Reduce variance |
| Underfitting (high bias) | Simple models miss patterns | Boosting → Reduce bias |

## Bagging (Bootstrap Aggregating)

### Definition

Train multiple models on **bootstrap samples** (random samples with replacement) and aggregate predictions.

### Algorithm

```
1. For b = 1 to B (number of models):
   a. Draw bootstrap sample D_b from training set D (with replacement)
   b. Train model M_b on D_b
   
2. Aggregate predictions:
   - Classification: Majority vote
   - Regression: Average
```

### Bootstrap Sampling

- Each bootstrap sample contains ~63.2% unique instances (with replacement)
- Remaining ~36.8% are "out-of-bag" (OOB) instances
- OOB can be used for validation without separate test set

### Why Bagging Works

**Variance reduction:**

```
Var(X̄) = σ²/n  (averaging n independent predictions)
```

If models are uncorrelated, averaging reduces variance significantly.

**Key insight:** Decision trees have high variance → Bagging reduces variance → Better generalization.

## Random Forest

### Definition

Bagging + **Random feature selection** at each split.

### Algorithm

```
1. For b = 1 to B:
   a. Draw bootstrap sample D_b from training set
   b. Grow decision tree T_b:
      - At each node, select random subset of m features (m << p)
      - Choose best split among m features only
      - Grow tree to maximum depth (no pruning)
      
2. Aggregate predictions:
   - Classification: Majority vote
   - Regression: Average
```

### Feature Subsampling

**m features at each split:**
- Classification: m = √p (sqrt of total features)
- Regression: m = p/3

**Purpose:** Decorrelate trees → Better variance reduction.

### Random Forest vs Bagging

| Aspect | Bagging | Random Forest |
|--------|---------|---------------|
| Features per split | All features | Random subset |
| Tree correlation | Higher | Lower |
| Variance reduction | Good | Better |
| Performance | Good | Often better |

### Why Random Feature Selection?

**Problem with bagging:** If one feature is very strong:
- All trees will use it for first split
- Trees become correlated
- Averaging correlated models reduces variance less

**Solution:** Random feature selection:
- Forces trees to use different features
- Decorrelates predictions
- Better ensemble effect

### Out-of-Bag (OOB) Error

- Use OOB samples for validation
- Each tree has ~36.8% OOB samples
- No need for separate validation set
- Built-in cross-validation

```
OOB Error = Average error on OOB predictions
```

## Boosting

### Definition

Train models **sequentially**, each correcting errors of previous ones.

### Key Idea

- Start with weak learner (e.g., decision stump)
- Focus on misclassified examples (increase their weights)
- Train next model on reweighted data
- Combine all models with weighted voting

### AdaBoost (Adaptive Boosting)

**Algorithm:**
```
1. Initialize weights w_i = 1/n for all samples

2. For t = 1 to T:
   a. Train weak learner h_t on weighted data
   b. Calculate weighted error: ε_t = Σ w_i × I(y_i ≠ h_t(x_i))
   c. Calculate model weight: α_t = 0.5 × log((1-ε_t)/ε_t)
   d. Update sample weights:
      - Increase for misclassified: w_i × exp(α_t)
      - Decrease for correctly classified: w_i × exp(-α_t)
   e. Normalize weights
   
3. Final prediction: H(x) = sign(Σ α_t × h_t(x))
```

### Gradient Boosting

**Algorithm:**
```
1. Initialize with constant model: F₀(x) = argmin_c Σ L(y_i, c)

2. For t = 1 to T:
   a. Compute pseudo-residuals: r_i = -∂L/∂F(x_i)
   b. Fit weak learner h_t to residuals r_i
   c. Find optimal step size: γ_t = argmin_γ Σ L(y_i, F_{t-1}(x_i) + γ × h_t(x_i))
   d. Update model: F_t(x) = F_{t-1}(x) + γ_t × h_t(x)
   
3. Final model: F_T(x)
```

### XGBoost / LightGBM / CatBoost

Modern gradient boosting implementations:
- **XGBoost:** Regularization, parallel processing, handling missing values
- **LightGBM:** Leaf-wise growth, faster training, large datasets
- **CatBoost:** Native categorical features, ordered boosting

## Comparison Summary

| Aspect | Bagging | Random Forest | Boosting |
|--------|---------|---------------|----------|
| Parallelization | Yes | Yes | No (sequential) |
| Reduces | Variance | Variance | Bias |
| Best for | High variance models | High variance models | High bias models |
| Overfitting risk | Low | Low | Higher (need tuning) |
| Training speed | Fast | Fast | Slower |
| Prediction speed | Fast | Fast | Depends on T |

## Key Takeaways

1. **Bagging reduces variance** - Averaging uncorrelated predictions
2. **Random Forest improves bagging** - Decorrelates trees via random features
3. **Boosting reduces bias** - Sequential learning from mistakes
4. **Bagging: parallel** - Trees trained independently
5. **Boosting: sequential** - Each tree learns from previous errors
6. **Random Forest best default** - Works well out of the box
7. **Boosting needs tuning** - More prone to overfitting
8. **OOB error** - Built-in validation for bagging methods

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Default choice | Random Forest |
| High accuracy needed | Gradient Boosting (with tuning) |
| Interpretability needed | Single decision tree |
| Limited compute | Bagging (parallel training) |
| Imbalanced classes | Boosting with class weights |

## References

- Breiman (1996): "Bagging Predictors"
- Breiman (2001): "Random Forests"
- Freund & Schapire (1997): "AdaBoost"
- Friedman (2001): "Greedy Function Approximation: A Gradient Boosting Machine"
- Chen & Guestrin (2016): "XGBoost"