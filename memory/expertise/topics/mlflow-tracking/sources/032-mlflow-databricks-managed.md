# MLflow on Databricks - Managed MLflow Guide

**Fonte:** GUIDE-005 - MLflow on Databricks: Benefits, Capabilities & Quick Tutorial  
**URL:** https://lakefs.io/blog/databricks-mlflow/  
**Tipo:** Blog/Guia  
**Data:** Fevereiro 2025  
**Status:** completed

---

## Resumo

Guia completo sobre MLflow gerenciado no Databricks: componentes, recursos adicionais, tutorial de setup, Model Registry com Unity Catalog, Model Serving.

---

## MLflow Components Overview

| Component | Function |
|-----------|----------|
| **Tracking** | Record and compare parameters and outcomes from experiments |
| **Models** | Manage and deploy models from various ML libraries |
| **Projects** | Package ML code in reusable, reproducible format |
| **Model Registry** | Centralized model store with versioning, stage transitions, annotations |
| **Model Serving** | Host MLflow models as REST endpoints |

---

## Managed MLflow on Databricks

### What Databricks Adds
- **Corporate security measures**
- **High availability**
- **Workspace features**: experiment/run management, notebook revision recording
- **Unity Catalog**: centralized model governance
- **Mosaic AI Model Serving**: optimized inference

### MLflow APIs Compatibility
- APIs identical to open-source version
- Same code runs on Databricks or self-hosted infrastructure

---

## Setup by Cloud Provider

- **AWS**: https://docs.databricks.com/en/mlflow/quick-start.html
- **Azure**: https://learn.microsoft.com/en-us/azure/databricks/mlflow/
- **GCP**: https://docs.gcp.databricks.com/en/mlflow/index.html

### Community Edition
- Fully managed Databricks platform (free)
- Most MLflow features available
- **Limitation**: Cannot create serving endpoints

---

## Model Registry on Databricks

### Unity Catalog Model Registry
- Centralized model governance
- Cross-workspace access
- Lineage tracking
- Deployment integration

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Model** | An MLflow Model recorded from an experiment |
| **Registered model** | Model registered with Model Registry; unique name, versions, lineage, metadata |
| **Model version** | Version assigned to each model (Version 1, 2, 3...) |
| **Model alias** | Mutable named reference to specific version (e.g., "champion") |
| **Model stage** | None, Staging, Production, Archived (Workspace Model Registry only) |
| **Description** | Annotations about algorithm, dataset, technique |

---

## Model Deployment Targets

### MLflow Supported Deployment Targets
- **Local**: `mlflow models serve`
- **Docker**: Container-based deployment
- **Azure ML**: Microsoft Azure ML integration
- **Amazon SageMaker**: AWS integration
- **Kubernetes**: Seldon Core, KServe (formerly KFServing)
- **Apache Spark**: Batch inference
- **Ray Serve**: Ray integration

### Mosaic AI Model Serving (Databricks)
- Uniform interface for deploying, managing, querying AI models
- REST API for each model
- **Custom models**: scikit-learn, XGBoost, PyTorch, Hugging Face
- **Foundation Model APIs**: Llama-2-70B-chat, BGE-Large, Mistral-7B (pay-per-token)
- **External models**: OpenAI GPT-4, Anthropic Claude (central management)

---

## Key Features

### Experiment Tracking
- Automatic tracking of parameters, metrics, code, models
- Secure sharing and comparison of results
- Integration with Databricks Notebooks

### Model Management
- Single location to discover and share models
- Collaboration on transitions to production
- Approval and governance workflows
- Write-Audit-Publish pipelines

### Model Deployment
- Batch inference on Apache Spark
- REST APIs with Docker/Azure ML/SageMaker integration
- Auto-managed clusters that scale based on requirements

---

## Model Registry Workflow

1. **Register Model**: Log model from experiment
2. **Version**: Each new model → new version
3. **Alias**: Set aliases like "champion" for production
4. **Transition**: Move between stages (if using Workspace Registry)
5. **Deploy**: Create serving endpoint
6. **Monitor**: Track performance and feedback

---

## Example Code

### Registering and Serving

```python
import mlflow
from mlflow.tracking import MlflowClient

# Log and register model
with mlflow.start_run():
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="my-classifier"
    )

# Set alias for production
client = MlflowClient()
client.set_registered_model_alias(
    name="my-classifier",
    alias="champion",
    version="1"
)

# Load model by alias
model = mlflow.pyfunc.load_model("models:/my-classifier@champion")
```

---

## Concepts Adicionados

- Unity Catalog Model Registry
- Mosaic AI Model Serving
- Foundation Model APIs (Llama, BGE, Mistral)
- External models (OpenAI, Anthropic)
- Pay-per-token pricing model
- Cross-workspace model access
- Model alias vs Model stage
- Write-Audit-Publish pipelines

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 20 min