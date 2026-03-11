# MLflow Autologging - Guia Completo

**Fonte:** DOC-014 - MLflow Automatic Logging  
**URL:** https://mlflow.org/docs/latest/ml/tracking/autolog/  
**Tipo:** Documentação Oficial  
**Data:** 2025  
**Status:** completed

---

## Resumo

Documentação oficial de autologging do MLflow: bibliotecas suportadas, customização, habilitar/desabilitar por biblioteca, métricas e parâmetros capturados.

---

## Getting Started

```python
import mlflow

mlflow.autolog()

with mlflow.start_run():
    # your training code goes here
    ...
```

### Automatic Capture
- **Metrics** - pre-selected based on library
- **Parameters** - hyperparams + default values
- **Model Signature** - input/output schema
- **Artifacts** - model checkpoints
- **Dataset** - dataset object used for training

---

## Basic Example (scikit-learn)

```python
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor

mlflow.autolog()

db = load_diabetes()
X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
# MLflow triggers logging automatically upon model fitting
rf.fit(X_train, y_train)
```

---

## Customize Autologging

```python
import mlflow

mlflow.autolog(
    log_model_signatures=False,
    extra_tags={"YOUR_TAG": "VALUE"},
)
```

---

## Enable/Disable by Library

```python
import mlflow

# Option 1: Enable only for PyTorch
mlflow.pytorch.autolog()

# Option 2: Disable sklearn, enable others
mlflow.sklearn.autolog(disable=True)
mlflow.autolog()
```

---

## Supported Libraries

### Keras/TensorFlow

```python
mlflow.tensorflow.autolog()
# or mlflow.autolog()
```

| Captured | Details |
|----------|---------|
| Metrics | Training loss, validation loss, user-specified |
| Parameters | fit() params, optimizer name, learning rate |
| Artifacts | Model summary, MLflow Model, TensorBoard logs |

**EarlyStopping**: Automatically logs stopped_epoch, restored_epoch, restore_best_weight

---

### LightGBM

```python
mlflow.lightgbm.autolog()
```

| Captured | Details |
|----------|---------|
| Metrics | User-specified metrics |
| Parameters | lightgbm.train parameters |
| Artifacts | MLflow Model, feature importance, input example |

**Early Stopping**: Logs metrics at best iteration

---

### PySpark ML

```python
mlflow.pyspark.ml.autolog()
```

| Captured | Details |
|----------|---------|
| Metrics | Post-training metrics from Evaluator.evaluate() |
| Parameters | Estimator.fit parameters |
| Artifacts | MLflow Model, metric_info.json |

---

### PyTorch (Lightning)

```python
mlflow.pytorch.autolog()
```

**Note**: Currently supports only PyTorch Lightning models.

| Captured | Details |
|----------|---------|
| Metrics | Training loss, validation loss, accuracy |
| Parameters | fit() params, optimizer name, learning rate |
| Artifacts | Model summary, MLflow Model, best checkpoint |

**Early Stopping**: Logs best model checkpoint if stopped early

---

### Scikit-learn

```python
mlflow.sklearn.autolog()
```

Supported:
- Estimators (LinearRegression, RandomForest, etc.)
- Meta-estimators (GridSearchCV, Pipeline, etc.)

| Captured | Details |
|----------|---------|
| Metrics | Training and validation metrics |
| Parameters | All estimator parameters |
| Artifacts | MLflow Model, confusion matrix, feature importance |

---

### XGBoost

```python
mlflow.xgboost.autolog()
```

| Captured | Details |
|----------|---------|
| Metrics | Training/validation metrics at each iteration |
| Parameters | XGBoost training parameters |
| Artifacts | MLflow Model, feature importance |

---

### Statsmodels

```python
mlflow.statsmodels.autolog()
```

| Captured | Details |
|----------|---------|
| Metrics | AIC, BIC, log-likelihood, R-squared |
| Parameters | Model parameters |
| Artifacts | MLflow Model, summary plots |

---

## Run Management

### No Active Run Exists
- MLflow automatically creates a run
- Run ends automatically when training completes

### Run Already Exists
- MLflow logs to existing run
- Does NOT end run automatically
- Must manually end if needed

---

## Full List of Supported Libraries

| Library | Autolog Call |
|---------|--------------|
| TensorFlow/Keras | `mlflow.tensorflow.autolog()` |
| LightGBM | `mlflow.lightgbm.autolog()` |
| Paddle | `mlflow.paddle.autolog()` |
| PySpark ML | `mlflow.pyspark.ml.autolog()` |
| PyTorch Lightning | `mlflow.pytorch.autolog()` |
| Scikit-learn | `mlflow.sklearn.autolog()` |
| Spark | `mlflow.spark.autolog()` |
| Statsmodels | `mlflow.statsmodels.autolog()` |
| XGBoost | `mlflow.xgboost.autolog()` |

---

## Concepts Adicionados

- Library-specific autolog calls
- Disable autolog per library
- EarlyStopping metric capture
- Automatic run creation/end behavior
- Model signatures from autolog
- Dataset logging support

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 15 min