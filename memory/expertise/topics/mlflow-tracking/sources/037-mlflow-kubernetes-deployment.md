# MLflow Kubernetes Deployment - Guia

**Fonte:** DOC-012 - Deploy MLflow Model to Kubernetes  
**URL:** https://mlflow.org/docs/latest/ml/deployment/deploy-model-to-kubernetes/  
**Tipo:** Documentação Oficial  
**Data:** 2025  
**Status:** completed

---

## Resumo

Documentação oficial de deployment Kubernetes: MLServer vs FastAPI, Docker image building, integração com KServe e Seldon Core.

---

## MLServer vs FastAPI

### FastAPI (Default)
- Standard ASGI web framework
- Simple local deployment
- **Limitation**: No native horizontal scaling
- Not ideal for production at scale

### MLServer
- Core Python inference server
- Used in Kubernetes-native frameworks:
  - **Seldon Core**
  - **KServe** (formerly KFServing)
- Better for production ML use cases
- Supports scalability and reliability

---

## Building Docker Image

### CLI Command

```bash
mlflow models build-docker \
  -m runs:/<run_id>/model \
  -n <image_name> \
  --enable-mlserver
```

### Python API

```python
import mlflow.models

mlflow.models.build_docker(
    model_uri="runs:/<run_id>/model",
    image_name="<image_name>",
    enable_mlserver=True
)
```

### Options
- Remove `--enable-mlserver` for FastAPI server
- Use `--install-java` for Java model flavor (Spark)
- Docker image spec changed since MLflow 2.10.1 (smaller, faster)

---

## Deployment Steps

### Partner Documentation

1. **KServe InferenceService**
   - https://kserve.github.io/website/latest/modelserving/v1beta1/mlflow/v2
   - Serverless inference on Kubernetes
   - Auto-scaling, rolling updates

2. **Seldon Core**
   - https://docs.seldon.ai/seldon-core-2/user-guide/examples/model-zoo#mlflow-wine-model
   - Kubernetes-native ML serving
   - Advanced orchestration

---

## Tutorial Resources

- End-to-end tutorials available
- Environment setup
- Model training
- Kubernetes deployment

---

## Docker Image Changes (MLflow 2.10.1+)

| Change | Impact |
|--------|--------|
| Reduced image size | Faster builds and deploys |
| Improved performance | Better inference throughput |
| Java removed by default | Smaller image; use `--install-java` for Spark |

---

## Concepts Adicionados

- MLServer for production ML serving
- KServe InferenceService integration
- Seldon Core integration
- Docker image optimization (2.10.1+)
- Java installation flag for Spark models

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 10 min