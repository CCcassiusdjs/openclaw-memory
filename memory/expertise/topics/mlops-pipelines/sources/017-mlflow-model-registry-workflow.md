# MLflow Model Registry Workflow - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/model-registry/workflow/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 📋 Visão Geral

Model Registry é o componente central para gerenciar MLflow models:
- Registrar models
- Gerenciar versions
- Aplicar aliases e tags
- Organizar models para deployment

## ⚠️ Pré-requisito

**Database-backed backend store** é necessário para acessar Model Registry via UI ou API.

## 🖥️ UI Workflow

### Registrar um Model

1. Abrir Run details page → Artifacts section
2. Selecionar model folder
3. Clicar "Register Model"
4. Escolher:
   - "Create New Model" → Novo registered model (Version 1)
   - Existing model → Nova version

### Encontrar Registered Models

| Método | Caminho |
|--------|---------|
| **Registered Models page** | Lista todos models + versions |
| **Artifacts → Model folder** | Link para version específica |

### Deploy e Organize Models

**Aliases e Tags** para organizar:
- Adicionar/editar aliases
- Adicionar/editar tags
- View details (signature, source run, timestamp)

## 🔧 API Workflow

### Método 1: log_model() com registered_model_name

```python
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

with mlflow.start_run() as run:
    X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    params = {"max_depth": 2, "random_state": 42}
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)

    # Log parameters and metrics
    mlflow.log_params(params)
    mlflow.log_metrics({"mse": mean_squared_error(y_test, y_pred)})

    # Log and register model
    mlflow.sklearn.log_model(
        sk_model=model,
        name="sklearn-model",
        signature=signature,
        registered_model_name="sk-learn-random-forest-reg-model",
    )
```

**Comportamento:**
- Se model não existe → Cria new model + Version 1
- Se model existe → Cria new version

### Método 2: register_model() após runs

```python
result = mlflow.register_model(
    "runs:/d16076a3ec534311817565e6527539c0/sklearn-model",
    "sk-learn-random-forest-reg"
)
```

**Retorna:** ModelVersion MLflow object

### Método 3: create_registered_model() + create_model_version()

```python
from mlflow import MlflowClient

client = MlflowClient()

# Create empty registered model
client.create_registered_model("sk-learn-random-forest-reg-model")

# Create version
result = client.create_model_version(
    name="sk-learn-random-forest-reg-model",
    source="mlruns/0/d16076a3ec534311817565e6527539c0/artifacts/sklearn-model",
    run_id="d16076a3ec534311817565e6527539c0",
)
```

**Nota:** `create_registered_model()` lança `MLflowException` se nome já existir.

## 🔗 Databricks Unity Catalog Integration

### Configuração

```python
# Set registry URI
mlflow.set_registry_uri("databricks-uc")

# Environment variables needed
# DATABRICKS_HOST
# DATABRICKS_TOKEN
# OR
# DATABRICKS_HOST, DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET (OAuth)
# OR
# Use ~/.databrickscfg profile:
# mlflow.set_registry_uri("databricks-uc://{profile}")
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Registered Model** | Container para todas versions de um model |
| **Model Version** | Versão específica de um registered model |
| **Alias** | Named reference para uma version (ex: "champion", "challenger") |
| **Tag** | Metadata key-value para organizar models |
| **Signature** | Input/output schema do model |
| **Source Run** | MLflow run que gerou o model |

## 🔄 Workflow de Registro

```
Training Run → log_model() → Model Artifact → Register Model → 
  ├── Create New Model (Version 1)
  └── Add to Existing Model (New Version)
```

## 🔗 Referências Cruzadas

- Pré-requisito: MLflow Model Registry (016)
- Relacionado a: MLflow Tracking (031-034)
- Complementa: CI/CD for ML (011-015)

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (workflow prático do MLflow Registry)