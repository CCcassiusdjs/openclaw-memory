# Feature Engineering Techniques for ML

**Fonte:** https://www.projectpro.io/article/8-feature-engineering-techniques-for-machine-learning/423
**Data:** 2026-03-10
**Status:** Completed

---

## Resumo

Feature engineering é a arte de transformar dados brutos em features que melhorem a performance de modelos de ML. Prof. Andrew Ng: "Applied machine learning is basically feature engineering."

---

## Tipos de Features

### 1. Numerical Features
- Valores contínuos mensuráveis
- Exemplos: idade, altura, peso, renda
- Podem ser usados diretamente em algoritmos

### 2. Categorical Features
- Valores discretos agrupáveis em categorias
- Exemplos: gênero, cor, CEP
- Precisam ser convertidos para numéricos (one-hot, label encoding)

### 3. Time-series Features
- Medições ao longo do tempo
- Exemplos: preços de ações, dados meteorológicos
- Usados para previsão de valores futuros

### 4. Text Features
- Strings de texto
- Exemplos: reviews, posts, registros médicos
- Usados para classificação, análise de sentimento

---

## Técnicas de Feature Engineering

### 1. Imputation (Tratamento de Missing Values)

**Categorical Imputation:**
- Substituir valores faltantes pela categoria mais frequente (mode)
- Alternativa: nova categoria "Unknown" ou "Missing"

**Numerical Imputation:**
- Substituir por média (mean)
- Alternativa: mediana, ou valor de distribuição normal

```python
# Imputation em Python
from sklearn.impute import SimpleImputer

# Numérico - média
num_imputer = SimpleImputer(strategy='mean')
X_num = num_imputer.fit_transform(X_numerical)

# Categórico - mais frequente
cat_imputer = SimpleImputer(strategy='most_frequent')
X_cat = cat_imputer.fit_transform(X_categorical)
```

### 2. Handling Outliers

**Métodos:**
- Remoção (se justificado)
- Capping/Clipping (limitar valores extremos)
- Transformação (log, sqrt)

### 3. Binning (Discretização)

Converter variáveis contínuas em categorias:

```python
# Binning em Python
import pandas as pd

# Quantile-based binning
df['age_group'] = pd.qcut(df['age'], q=4, labels=['Young', 'Adult', 'Middle', 'Senior'])

# Fixed-width binning
df['income_bracket'] = pd.cut(df['income'], bins=[0, 30000, 60000, 100000, float('inf')])
```

### 4. Log Transformation

Reduzir skewness e outliers:

```python
import numpy as np

# Log transform para valores positivos
df['log_income'] = np.log1p(df['income'])

# Log1p para evitar log(0)
df['log_feature'] = np.log1p(df['feature'])
```

### 5. One-Hot Encoding

Converter categorias em colunas binárias:

```python
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

# One-hot encoding
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
X_encoded = encoder.fit_transform(df[['category']])

# Ou com pandas
df_encoded = pd.get_dummies(df, columns=['category'])
```

### 6. Label Encoding

Converter categorias em números:

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])
```

### 7. Feature Scaling

**Standardization (Z-score):**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

**Min-Max Scaling:**
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

### 8. Feature Creation (Interaction Features)

Criar novas features combinando existentes:

```python
# Interação entre features
df['price_per_sqft'] = df['price'] / df['sqft']
df['age_income_ratio'] = df['age'] / df['income']

# Multiplicação (polynomial features)
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly.fit_transform(X)
```

---

## Feature Selection Techniques

### Filter Methods
- Correlation analysis
- Chi-squared test
- Mutual information
- Variance threshold

### Wrapper Methods
- Recursive Feature Elimination (RFE)
- Forward selection
- Backward elimination

### Embedded Methods
- Lasso (L1 regularization)
- Tree-based importance
- Regularized models

---

## Exemplo Prático: Seleção de Features

```python
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.datasets import load_iris

# Carregar dados
X, y = load_iris(return_X_y=True)

# Selecionar top K features
selector = SelectKBest(chi2, k=2)
X_selected = selector.fit_transform(X, y)

print(f"Features selecionadas: {selector.get_support(indices=True)}")
```

---

## Boas Práticas

1. **Entender o problema**: Quais features são mais relevantes?
2. **Explorar os dados**: Distribuições, outliers, missing values
3. **Usar técnicas de seleção**: Filter, wrapper, embedded
4. **Avaliar resultados**: Performance com features selecionadas
5. **Iterar**: Feature engineering é um processo iterativo

---

## Conceitos Aprendidos

1. **Tipos de Features**: Numerical, categorical, time-series, text
2. **Imputation**: Tratamento de missing values
3. **Encoding**: One-hot, label, ordinal
4. **Scaling**: Standardization, Min-Max
5. **Feature Creation**: Interaction features, polynomial features
6. **Feature Selection**: Filter, wrapper, embedded methods
7. **Binning**: Discretização de variáveis contínuas
8. **Log Transform**: Redução de skewness e outliers

---

*Atualizado em: 2026-03-10*