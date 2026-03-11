# MLflow Model Deployment - Guia Completo

**Fonte:** GUIDE-003 - How to Deploy Models with MLflow  
**URL:** https://oneuptime.com/blog/post/2026-01-27-mlflow-model-deployment/view  
**Tipo:** Tutorial/Guia  
**Data:** Janeiro 2026  
**Status:** completed

---

## Resumo

Guia completo de deployment de modelos com MLflow: registro no Model Registry, transição de stages, loading por stage, formato MLmodel, serving local com REST API.

---

## Model Registry Basics

### Registering a Model

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = accuracy_score(y_test, model.predict(X_test))
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("n_estimators", 100)
    
    # Log and register in single step
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="iris-classifier"
    )
```

### Querying the Registry

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()

# List all registered models
for model in client.search_registered_models():
    print(f"Model: {model.name}")
    print(f"Latest versions: {[v.version for v in model.latest_versions]}")

# List all versions of a model
for version in client.search_model_versions("name='iris-classifier'"):
    print(f"Version {version.version}:")
    print(f"  Stage: {version.current_stage}")
    print(f"  Run ID: {version.run_id}")
```

---

## Model Stage Transitions

### Built-in Stages
- None (initial)
- Staging (testing)
- Production (live)
- Archived (deprecated)

### Transitioning Stages

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()

# Transition to Staging
client.transition_model_version_stage(
    name="iris-classifier",
    version=1,
    stage="Staging",
    archive_existing_versions=True  # Clean up old staging versions
)

# After validation, promote to Production
client.transition_model_version_stage(
    name="iris-classifier",
    version=1,
    stage="Production",
    archive_existing_versions=True  # Archive previous production
)

# Add description
client.update_model_version(
    name="iris-classifier",
    version=1,
    description="Production model deployed after validation. Accuracy: 96.7%"
)

# Add tags
client.set_model_version_tag(
    name="iris-classifier",
    version=1,
    key="validation_status",
    value="passed"
)
```

### Loading Models by Stage

```python
import mlflow.pyfunc

model_name = "iris-classifier"

# Load Production model (always latest)
production_model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/Production"
)

# Load Staging model
staging_model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/Staging"
)

# Load specific version
specific_version = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/1"
)
```

---

## MLflow Models Format

### Model Signature

```python
from mlflow.models.signature import infer_signature, ModelSignature
from mlflow.types.schema import Schema, ColSpec
import pandas as pd
import numpy as np

# Method 1: Infer signature automatically
signature = infer_signature(X_train, predictions)

# Method 2: Define explicitly
explicit_signature = ModelSignature(
    inputs=Schema([
        ColSpec("double", "feature_1"),
        ColSpec("double", "feature_2")
    ]),
    outputs=Schema([ColSpec("double")])
)

# Log with signature and input example
with mlflow.start_run():
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        signature=signature,
        input_example=X_numeric.head(2),
        registered_model_name="price-predictor"
    )
```

### MLmodel File Structure

```yaml
artifact_path: model
flavors:
  python_function:
    env:
      conda: conda.yaml
      virtualenv: python_env.yaml
    loader_module: mlflow.sklearn
    model_path: model.pkl
    predict_fn: predict
    python_version: 3.10.12
  sklearn:
    pickled_model: model.pkl
    serialization_format: cloudpickle
    sklearn_version: 1.3.0
mlflow_version: 2.9.0
model_size_bytes: 125432
run_id: 1234567890abcdef
signature:
  inputs: '[{"type": "double", "name": "feature_1"}, {"type": "double", "name": "feature_2"}]'
  outputs: '[{"type": "double"}]'
```

---

## Local Model Serving

### Starting the Server

```bash
# Serve from Model Registry (Production)
mlflow models serve \
  --model-uri "models:/iris-classifier/Production" \
  --host 0.0.0.0 \
  --port 5001 \
  --env-manager=local

# Serve specific version
mlflow models serve \
  --model-uri "models:/iris-classifier/1" \
  --host 0.0.0.0 \
  --port 5001

# Serve from run (testing)
mlflow models serve \
  --model-uri "runs:/abc123def456/model" \
  --host 0.0.0.0 \
  --port 5001

# Multiple workers for higher throughput
mlflow models serve \
  --model-uri "models:/iris-classifier/Production" \
  --workers 4
```

### Making Predictions via REST API

```python
import requests
import json

MODEL_SERVER_URL = "http://localhost:5001/invocations"

# Method 1: Split-orient format
payload_split = {
    "dataframe_split": {
        "columns": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
        "data": [[5.1, 3.5, 1.4, 0.2], [6.2, 2.9, 4.3, 1.3]]
    }
}

response = requests.post(
    MODEL_SERVER_URL,
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload_split)
)
predictions = response.json()
```

---

## Key Concepts

- `mlflow.sklearn.log_model()` with `registered_model_name` → register in one step
- `client.search_registered_models()` → list all models
- `client.search_model_versions("name='X'")` → list versions
- `transition_model_version_stage()` → promote/demote
- `archive_existing_versions=True` → clean up old versions automatically
- `models:/name/Stage` URI → load by stage
- `models:/name/version` URI → load by version
- MLmodel YAML describes flavors, env, signature
- `mlflow models serve` → Gunicorn REST API

---

## Concepts Adicionados

- Stage transitions (None → Staging → Production → Archived)
- archive_existing_versions pattern
- Model signature (inferred vs explicit)
- Input examples for testing
- MLmodel YAML format
- REST API serving with split-orient format
- Multi-worker serving for throughput

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 25 min