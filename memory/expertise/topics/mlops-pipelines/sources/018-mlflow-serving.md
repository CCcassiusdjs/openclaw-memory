# MLflow Serving - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/deployment/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 Visão Geral

MLflow simplifica deployment de ML models para vários destinos:
- Local environments
- Cloud services (AWS, Azure)
- Kubernetes clusters

## 🔧 Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Effortless Deployment** | Interface simples, sem boilerplate |
| **Dependency Management** | Environment mirror training environment |
| **Packaging Models + Code** | Container com tudo necessário |
| **No Vendor Lock-in** | Standard format, unified APIs |

## 📋 Conceitos

### MLflow Model
- Standard format para empacotar modelo + metadata
- Dependencies + inference schema
- Criado via Tracking APIs ou Model Registry

### Container
- Docker container com modelo + dependências
- Deployment para vários destinos
- Environment compatibility garantida

### Deployment Target
- Destination environment
- Local, cloud (AWS, Azure), Kubernetes

## 🚀 Como Funciona

```
MLflow Model → Container/venv → Inference Server (FastAPI) → Deployment Target
```

1. Model já empacotado com dependências
2. MLflow cria container ou virtual environment
3. Inference server com REST endpoints
4. Deployment para destino escolhido

## 📊 Deployment Targets Suportados

| Target | Descrição |
|--------|-----------|
| **Local** | `mlflow models serve` - inference server local |
| **SageMaker** | AWS managed inference containers |
| **Azure ML** | Online/batch endpoints, AKS, ACI |
| **Databricks** | Managed serving at scale |
| **Kubernetes** | Seldon Core, KServe |
| **Modal** | Serverless cloud, on-demand GPU |

## 🔧 CLI Commands

### Local Deployment
```bash
mlflow models serve -m "models:/my-model/1" -p 5001
```

### SageMaker Deployment
```bash
mlflow sagemaker deploy -m "models:/my-model/1" --app-name my-app
```

### Azure ML Deployment
```python
import mlflow.azureml
mlflow.azureml.deploy(...)
```

## 💡 API References

| API | Uso |
|-----|-----|
| `mlflow.models` | Model management |
| `mlflow.deployments` | Deployment operations |
| `mlflow.sagemaker` | SageMaker specific |

## 🔗 Referências Cruzadas

- Complementa: MLflow Model Registry (016-020)
- Relacionado a: Kubernetes Deployment (039-040)
- Pré-requisito para: Production Serving

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (ML deployment prático)