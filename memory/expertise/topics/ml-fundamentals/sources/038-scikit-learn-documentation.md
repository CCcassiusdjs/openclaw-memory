# scikit-learn: Machine Learning in Python

**Fonte:** scikit-learn Documentation (Consolidado)
**URL:** https://scikit-learn.org/
**Tipo:** Framework de ML
**Licença:** BSD

---

## Visão Geral

scikit-learn é a biblioteca padrão de ML em Python, oferecendo ferramentas simples e eficientes para:
- **Classificação**: Identificar categorias
- **Regressão**: Predizer valores contínuos
- **Clustering**: Agrupar dados não-labelizados
- **Dimensionality Reduction**: Reduzir features
- **Model Selection**: Selecionar e validar modelos
- **Preprocessing**: Preparar dados

---

## Aprendizado Supervisionado

### Classificadores

| Algoritmo | Classe | Uso Principal |
|-----------|--------|---------------|
| **Linear Models** | `LogisticRegression`, `SGDClassifier` | Alto dimensional, texto |
| **SVM** | `SVC`, `LinearSVC` | Margem máxima, kernels |
| **Decision Trees** | `DecisionTreeClassifier` | Interpretabilidade |
| **Random Forest** | `RandomForestClassifier` | Robusto, feature importance |
| **Gradient Boosting** | `GradientBoostingClassifier`, `XGBoost` | Alta performance |
| **Nearest Neighbors** | `KNeighborsClassifier` | Similaridade |
| **Naive Bayes** | `GaussianNB`, `MultinomialNB` | Texto, rápido |

### Regressores

| Algoritmo | Classe | Uso Principal |
|-----------|--------|---------------|
| **Linear Models** | `LinearRegression`, `Ridge`, `Lasso` | Baseline, interpretabilidade |
| **SVR** | `SVR` | Não-linearidade |
| **Decision Trees** | `DecisionTreeRegressor` | Interpretabilidade |
| **Random Forest** | `RandomForestRegressor` | Robusto |
| **Gradient Boosting** | `GradientBoostingRegressor` | Alta performance |

---

## API Consistente

### Padrão Estimator
```python
# Todos estimadores seguem este padrão
estimator.fit(X_train, y_train)  # Treino
y_pred = estimator.predict(X_test)  # Predição

# Hiperparâmetros no construtor
model = RandomForestClassifier(n_estimators=100, max_depth=5)

# Parâmetros aprendidos
model.fit(X, y)
print(model.feature_importances_)
print(model.classes_)
```

### Métodos Comuns
```python
# Supervisionado
model.fit(X, y)
model.predict(X)
model.predict_proba(X)  # Probabilidades
model.score(X, y)  # Acurácia

# Não-supervisionado
model.fit(X)
model.transform(X)  # Redução
model.fit_transform(X)  # Ambos
model.predict(X)  # Clusters
```

---

## Preprocessing

### Scaling
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Standard (z-score)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# MinMax [0, 1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Robust a outliers
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

### Encoding
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder

# Label encoding (1, 2, 3...)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# One-hot encoding
ohe = OneHotEncoder()
X_encoded = ohe.fit_transform(X_categorical)
```

### Feature Engineering
```python
from sklearn.preprocessing import PolynomialFeatures

# Polinômios
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
```

---

## Model Selection

### Train-Test Split
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold

# 5-fold CV
scores = cross_val_score(model, X, y, cv=5)

# Stratified para classes desbalanceadas
skf = StratifiedKFold(n_splits=5)
scores = cross_val_score(model, X, y, cv=skf)
```

### Grid Search
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy'
)
grid_search.fit(X_train, y_train)
print(grid_search.best_params_)
```

### Random Search
```python
from sklearn.model_selection import RandomizedSearchCV

param_distributions = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(3, 20)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_distributions,
    n_iter=50,
    cv=5
)
```

---

## Pipelines

### Pipeline Básico
```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

### Pipeline com Preprocessing
```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Separar colunas numéricas e categóricas
numeric_features = ['age', 'income']
categorical_features = ['gender', 'city']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(), categorical_features)
])

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])
```

---

## Metrics

### Classificação
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report
)

# Métricas
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')

# Classification report
print(classification_report(y_true, y_pred))

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
```

### Regressão
```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error,
    r2_score
)

mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
```

---

## Aprendizado Não-Supervisionado

### Clustering
```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

# K-Means
kmeans = KMeans(n_clusters=3)
labels = kmeans.fit_predict(X)

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)
```

### Dimensionality Reduction
```python
from sklearn.decomposition import PCA, TruncatedSVD

# PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Variância explicada
print(pca.explained_variance_ratio_)
```

---

## Best Practices

### 1. Sempre Use Cross-Validation
```python
# ERRADO
model.fit(X, y)
model.score(X, y)  # Otimista!

# CORRETO
scores = cross_val_score(model, X, y, cv=5)
print(scores.mean())
```

### 2. Separe Test Set Final
```python
# Primeiro: train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Depois: CV no train set
scores = cross_val_score(model, X_train, y_train, cv=5)

# Final: avaliar no test set
model.fit(X_train, y_train)
test_score = model.score(X_test, y_test)
```

### 3. Use Pipelines
```python
# ERRADO: data leakage
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)

# CORRETO: pipeline evita leakage
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
scores = cross_val_score(pipeline, X, y, cv=5)
```

### 4. Stratify para Classes Desbalanceadas
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y
)
```

---

## Conceitos-Chave

### Fit vs Transform
- **fit()**: Aprende parâmetros dos dados
- **transform()**: Aplica transformação
- **fit_transform()**: Ambos (mais eficiente)

### Estimator API
- Todos modelos seguem `fit(X, y)` e `predict(X)`
- Hiperparâmetros no construtor
- Parâmetros aprendidos acessíveis após fit

### Pipeline Benefits
- Evita data leakage
- Reprodutibilidade
- Fácil grid search em todo pipeline

---

## Status
- [x] Conceitos consolidados
- [ ] Exemplos práticos

---

## Próximos Passos
1. Praticar com datasets reais
2. Implementar pipelines complexos
3. Comparar modelos com GridSearchCV

---

*Fonte consolidada em: 2026-03-10*