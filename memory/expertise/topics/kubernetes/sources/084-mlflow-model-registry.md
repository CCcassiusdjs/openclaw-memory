# MLflow Model Registry - Complete Guide

**Fonte:** https://mlflow.org/docs/latest/model-registry/
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

MLflow Model Registry é um componente para versionamento, organização e deployment de modelos ML. Permite gerenciar lifecycle completo com aliases, tags, estágios e versionamento.

---

## O que é Model Registry

Serviço que permite:
- Versionar modelos
- Compartilhar modelos entre times
- Anotar modelos com metadata
- Gerenciar estágios (staging, production, archived)

### Componentes Principais

| Componente | Função |
|------------|--------|
| **Centralized Model Store** | Store único para modelos |
| **APIs** | CRUD programático de modelos |
| **GUI** | Interface visual para gestão |

### MLflow Components

| Component | Description |
|-----------|-------------|
| **MLflow Tracking** | Track experiments (code, data, setup, outcomes) |
| **MLflow Projects** | Package code for reproducibility |
| **MLflow Models** | Deploy models to serving environments |
| **Model Registry** | Store, annotate, find, manage models |

---

## Use Cases

1. Monitorar múltiplas iterações de modelos
2. Track qual versão está em cada ambiente
3. Avaliar performance de modelos ao longo do tempo
4. Streamlinar deployment para staging/production

---

## Key Concepts

### Registered Model
- Nome único
- Tags, aliases, versões, metadata

### Model Version
- Versão numerada (1, 2, 3...)
- Tags por versão (ex: `pre_deploy_checks: "PASSED"`)
- Linhagem: experiment e run que gerou

### Model Aliases
- Referência nomeada para versão específica
- Mutable (pode ser reatribuído)
- Útil para deployment

```python
# Champion alias example
models:/MyModel@champion  # Points to version currently in production
```

### Model Tags
- Key-value pairs
- Organizar e categorizar modelos
- Ex: `task: "classification"`, `framework: "sklearn"`

---

## UI Workflow

### Register a Model
1. Open MLflow Run details page
2. Select model folder in Artifacts
3. Click "Register Model"
4. Choose "Create New Model" or existing model

### Find Registered Models
- Registered Models page
- Artifacts section → model folder → model version link

### Deploy and Organize
- Set aliases para deployment
- Add tags para organização
- View version details (signature, source run, timestamp)

---

## API Workflow

### Method 1: log_model()
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor

with mlflow.start_run() as run:
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    # Log and register in one step
    mlflow.sklearn.log_model(
        sk_model=model,
        name="sklearn-model",
        registered_model_name="my-random-forest"
    )
```

### Method 2: register_model()
```python
import mlflow

# Register after run completes
result = mlflow.register_model(
    "runs:/d16076a3ec534311817565e6527539c0/sklearn-model",
    "my-random-forest"
)
```

### Method 3: create_registered_model()
```python
from mlflow import MlflowClient

client = MlflowClient()

# Create empty registered model
client.create_registered_model("my-random-forest")

# Create version
client.create_model_version(
    name="my-random-forest",
    source="mlruns/0/d1607.../artifacts/sklearn-model",
    run_id="d16076a3ec534311817565e6527539c0"
)
```

---

## Aliases and Tags

### Set Aliases
```python
from mlflow import MlflowClient

client = MlflowClient()

# Create "champion" alias for version 1
client.set_registered_model_alias("my-model", "champion", 1)

# Reassign alias to version 2
client.set_registered_model_alias("my-model", "champion", 2)

# Get model by alias
model_version = client.get_model_version_by_alias("my-model", "champion")

# Delete alias
client.delete_registered_model_alias("my-model", "champion")
```

### Set Tags
```python
# Set model version tag
client.set_model_version_tag("my-model", "1", "validation_status", "passed")

# Delete tag
client.delete_model_version_tag("my-model", "1", "validation_status")
```

---

## Databricks Unity Catalog

### Setup
```python
import mlflow
import os

mlflow.set_registry_uri("databricks-uc")
os.environ["DATABRICKS_HOST"] = "<your-databricks-uri>"
os.environ["DATABRICKS_TOKEN"] = "<your-token>"
```

### Migrate from Workspace to UC
```python
from mlflow import MlflowClient

client = MlflowClient(registry_uri="databricks")
src_model_uri = "models:/my_wmr_model/1"

# Copy to Unity Catalog
uc_migrated_copy = client.copy_model_version(
    src_model_uri,
    "mycatalog.myschema.my_uc_model"
)
```

---

## Model Loading

### Load by Version
```python
import mlflow

model = mlflow.pyfunc.load_model("models:/my-model/1")
predictions = model.predict(X_test)
```

### Load by Alias
```python
model = mlflow.pyfunc.load_model("models:/my-model@champion")
```

---

## Best Practices

### 1. Model Staging
- Use staging environment before production
- Test e ajuste antes de ir live
- Remove errors e potenciais falhas

### 2. Centralize Experiment Tracking
- Um tracking server para toda organização
- Facilita colaboração e auditoria

### 3. Use Aliases for Deployment
- Champion para production
- Challenger para candidatos
- Archivist para modelos antigos

### 4. Implement CI/CD
- Registre modelos automaticamente
- Promote através de environments
- Use tags para status de validação

### 5. Model Lineage
- Track experiment e run que gerou
- Documente dataset usado
- Descreva algoritmo e hyperparameters

---

## Environment Promotion

```
┌─────────────────────────────────────────────────────┐
│                    Dev Environment                  │
│  ┌─────────────────────────────────────────────┐  │
│  │              Experiment Runs                  │  │
│  │         models:/my-model/versions/1-10      │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      ↓ Promote
┌─────────────────────────────────────────────────────┐
│                  Staging Environment                │
│  ┌─────────────────────────────────────────────┐  │
│  │              Validation Tests                │  │
│  │         models:/my-model@staging            │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      ↓ Promote
┌─────────────────────────────────────────────────────┐
│                 Production Environment              │
│  ┌─────────────────────────────────────────────┐  │
│  │              Serving Models                  │  │
│  │         models:/my-model@champion           │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Version control scaling | Use lakeFS for large datasets |
| Data schema changes | Document transformations |
| Tool integration | MLflow integrates with CI/CD |
| Automation | Use MLflow APIs for pipeline integration |

---

## Comparison with Alternatives

| Feature | MLflow Registry | DVC | Weights & Biases |
|---------|-----------------|-----|------------------|
| Versioning | ✅ | ✅ | ✅ |
| Stages | ✅ | ❌ | ✅ |
| Aliases | ✅ | ❌ | ✅ |
| Lineage | ✅ | ✅ | ✅ |
| Open Source | ✅ | ✅ | Partial |

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Registered Model | Container para versões de um modelo |
| Model Version | Versão numerada de um modelo |
| Model Alias | Referência nomeada (ex: champion) |
| Model Tag | Key-value pair para metadata |
| Model Lineage | Experiment/run que gerou o modelo |
| Staging | Ambiente de teste antes de production |

---

## Referências

- MLflow Model Registry: https://mlflow.org/docs/latest/model-registry/
- Workflow Guide: https://mlflow.org/docs/latest/ml/model-registry/workflow/
- API Reference: https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html