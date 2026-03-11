# MLflow Production-Ready ML Workflows - Guia Prático

**Fonte:** GUIDE-006 - A Practical Guide to MLflow: From Chaos to Production-Ready ML Workflows  
**URL:** https://medium.com/@omari.james.data/a-practical-guide-to-mlflow-from-chaos-to-production-ready-ml-workflows-3fa37bd95ef9  
**Tipo:** Tutorial/Artigo  
**Data:** Agosto 2025  
**Status:** completed

---

## Resumo

Guia prático introdutório sobre MLflow: conceitos core (Tracking, Runs, Experiments, Artifacts), autologging, Model Registry, deployment, model flavors, custom models.

---

## Core Concepts

### Tracking UI
- Visual hub for exploring logged data
- Compare runs by metrics/parameters
- Search by metric threshold or parameter values
- Download artifacts (models, datasets)

### Runs
- Each execution of a Python file that trains a model
- Records: metrics, parameters, tags, artifacts
- Default: logs locally to `mlruns/` directory
- Use `mlflow.set_tracking_uri()` to configure location

### Experiments
- Groupings of related runs for comparison
- Created for specific project or hypothesis

### Artifacts
- Large output files: model weights, images, data files
- Stored in run's artifact store

### Logging Options
1. **Manual logging**: specific log statements
2. **Autologging**: automatic without explicit statements

### Model Registry
- Single, central place to store all models
- Unique name for each model
- Versioning automatic (next version number)
- Links to run that produced them
- Promotion to stages for deployment

---

## Deployment

### MLflow Deployment Toolset
- Ensures deployment environment mirrors training environment
- Container packages model + code + configurations
- Deployment targets: local, cloud services, Kubernetes

### MLflow Models
- Not just binary file with learned parameters
- **Comprehensive package**: everything needed to reproduce predictions
- Directory with model, metadata, dependencies, inference schema
- Docker containers for packaging

### Model Flavors
- Set of rules for MLflow to interact with models
- **What they do**:
  - Model Packaging: save with dependencies, requirements, metadata
  - Standard Interface: consistent interaction across frameworks
- Supported: scikit-learn, TensorFlow, PyTorch, etc.

### Custom Models
- For unsupported frameworks or custom behavior
- Uses Python function (pyfunc) flavor
- Loaded as `mlflow.pyfunc.PythonModel` with `predict` method

---

## Code Example Setup

### Running MLflow Server

```bash
mlflow server --host 127.0.0.1 --port 5000
# Open browser: http://127.0.0.1:5000
```

### Dependencies

```bash
pip install mlflow=='3.1.4' \
  numpy=="1.26.4" \
  pandas=="2.3.1" \
  pyarrow==14.0.2 \
  python-dotenv==1.1.1 \
  scikit-learn==1.7.0 \
  seaborn==0.13.2
```

### Tracking Code Pattern

```python
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

# Set tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Create/get experiment
mlflow.set_experiment("my-experiment")

# Start run
with mlflow.start_run(run_name="my-run"):
    # Train model
    model.fit(X_train, y_train)
    
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model with signature
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        signature=signature,
        registered_model_name="my-classifier"
    )
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Tracking UI | Visual interface for runs |
| Run | Single execution with metrics/params |
| Experiment | Group of related runs |
| Artifact | Large output files |
| Logging | Manual vs Autologging |
| Model Registry | Central model store with versioning |
| Model Flavor | Standard interface for frameworks |
| Custom Model | pyfunc-based custom models |

---

## Concepts Adicionados

- MLflow server command line setup
- pyfunc flavor for custom models
- Standard deployment toolset pattern
- Model Registry versioning workflow
- Artifacts vs Metrics distinction
- Experiment organization patterns

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 15 min