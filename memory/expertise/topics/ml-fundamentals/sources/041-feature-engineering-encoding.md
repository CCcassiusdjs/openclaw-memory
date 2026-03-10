# Feature Engineering: Encoding Categorical Variables

**Source:** MachineLearningMastery, scikit-learn documentation
**Category:** Feature Engineering
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Feature engineering** transforms raw data into features that better represent the underlying problem, improving model performance. **Categorical encoding** is a crucial step for handling non-numeric data.

## Types of Variables

### Numerical Variables
- **Integer:** Count data (e.g., number of rooms)
- **Float:** Continuous data (e.g., temperature, price)

### Categorical Variables
- **Nominal:** No natural order (e.g., color, country)
- **Ordinal:** Natural order exists (e.g., education level, size)

## Encoding Techniques

### 1. Ordinal Encoding (Label Encoding)

**Definition:** Assign integer to each category.

```
"red" → 0
"green" → 1
"blue" → 2
```

**Use case:**
- Ordinal variables (natural order exists)
- Tree-based models (can handle integers natively)

**Problem:**
- Implies ordering where none may exist
- Can mislead linear models (0 < 1 < 2)

**Implementation:**
```python
from sklearn.preprocessing import OrdinalEncoder

encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)
```

### 2. One-Hot Encoding

**Definition:** Create binary column for each category.

```
"red" → [1, 0, 0]
"green" → [0, 1, 0]
"blue" → [0, 0, 1]
```

**Use case:**
- Nominal variables (no natural order)
- Linear models, neural networks

**Problem:**
- High cardinality → many columns (sparse)
- Linearly dependent columns (dummy variable trap)

**Implementation:**
```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse=False)  # or sparse=True
X_encoded = encoder.fit_transform(X)
```

### 3. Dummy Variable Encoding

**Definition:** One-hot encoding but drop one column (C-1 columns for C categories).

```
"red" → [0, 1]
"green" → [1, 0]
"blue" → [0, 0]  # Reference category
```

**Use case:**
- Linear regression (avoids singular matrix)
- Avoids dummy variable trap

**Implementation:**
```python
encoder = OneHotEncoder(drop='first', sparse=False)
X_encoded = encoder.fit_transform(X)
```

## Choosing Encoding Method

| Scenario | Recommended Encoding |
|----------|---------------------|
| **Ordinal variable** | Ordinal encoding |
| **Nominal, few categories** | One-hot encoding |
| **Nominal, many categories** | Target encoding, frequency encoding |
| **Linear models** | One-hot or dummy (not ordinal) |
| **Tree-based models** | Ordinal OK, one-hot also works |
| **Neural networks** | One-hot or embeddings |

## Advanced Encoding Techniques

### Target Encoding (Mean Encoding)

**Definition:** Replace category with mean of target for that category.

```
city = "Seattle" → target_mean(Seattle) = 0.75
city = "Portland" → target_mean(Portland) = 0.60
```

**Pros:**
- Handles high cardinality
- Captures relationship with target

**Cons:**
- Risk of overfitting (data leakage)
- Requires regularization

### Frequency Encoding

**Definition:** Replace category with its frequency in the data.

```
city = "Seattle" → count(Seattle) / n = 0.30
city = "Portland" → count(Portland) / n = 0.15
```

**Pros:**
- Simple, no data leakage
- Works for high cardinality

**Cons:**
- Loses category identity
- May not capture predictive power

## Best Practices

### 1. Fit on Training Data Only

```python
# CORRECT
encoder.fit(X_train)
X_train_encoded = encoder.transform(X_train)
X_test_encoded = encoder.transform(X_test)

# WRONG - data leakage!
encoder.fit(X)  # Includes test data
```

### 2. Handle Unknown Categories

```python
encoder = OneHotEncoder(handle_unknown='ignore')
# Unknown categories become all zeros
```

### 3. Handle Missing Values

```python
# Option 1: Treat NaN as a category
encoder = OneHotEncoder(handle_unknown='ignore')
# NaN becomes a separate category

# Option 2: Impute first, then encode
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='most_frequent')
X_imputed = imputer.fit_transform(X)
```

### 4. Use ColumnTransformer for Mixed Data

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['age', 'income']),
    ('cat', OneHotEncoder(), ['city', 'gender'])
])

X_processed = preprocessor.fit_transform(X)
```

## High Cardinality Handling

### Problem
When categories > 100+, one-hot creates:
- Many sparse columns
- Computational overhead
- Overfitting risk

### Solutions

| Method | Description |
|--------|-------------|
| **Target encoding** | Replace with target mean |
| **Frequency encoding** | Replace with frequency |
| **Hash encoding** | Hash categories to fixed size |
| **Embedding** | Learn dense representation (deep learning) |
| **Group rare** | Group infrequent categories as "Other" |

## Key Takeaways

1. **Ordinal for ordered categories** - Natural order preserved
2. **One-hot for nominal** - No order assumption
3. **Dummy for linear models** - Avoid singular matrix
4. **Fit on train, transform test** - Prevent data leakage
5. **Handle unknown categories** - Use handle_unknown='ignore'
6. **High cardinality** - Use target/frequency encoding
7. **ColumnTransformer** - Mix numeric and categorical processing
8. **Tree models** - Can handle ordinal encoding natively

## Common Pitfalls

| Pitfall | Consequence | Solution |
|---------|-------------|----------|
| Fit on full data | Data leakage | Fit on train only |
| Ignore unknown categories | Error on test | handle_unknown='ignore' |
| High cardinality one-hot | Curse of dimensionality | Target/frequency encoding |
| Ordinal for nominal | False ordering | Use one-hot |
| No missing handling | Encoding fails | Impute or treat as category |

## References

- Machine Learning Mastery (2020): "Ordinal and One-Hot Encodings for Categorical Data"
- scikit-learn documentation: OneHotEncoder, OrdinalEncoder
- Kuhn & Johnson (2013): "Applied Predictive Modeling"