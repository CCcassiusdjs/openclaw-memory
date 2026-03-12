# CI/CD for Machine Learning in 2024: Best Practices & Tips - Resumo

**Fonte:** https://www.qwak.com/post/ci-cd-pipelines-for-machine-learning
**Tipo:** Guide
**Data:** 2026-03-12

---

## 🎯 Por que CI/CD para ML?

### Motivação Principal
ML models sofrem de **degradação** - necessitam retraining regular com novos dados e redeployment.

### Diferenças do CI/CD Tradicional

| Software Tradicional | Machine Learning |
|---------------------|------------------|
| Code-focused | Code + Data + Model |
| Linear paths | Exploratory, non-linear |
| Build once, deploy | Retrain regularly |
| Version control = code | Version control = code + data + artifacts |

## 📋 ML Lifecycle e CI/CD

### 1. Model Development (Experimentation Phase)
- Exploratory field, creative process
- Prototyping and iterating over models
- Goal: Identify promising models for deployment
- **NOT automation-focused** - human experimentation

### 2. Model Integration and Training (Build Phase)
| Step | Ação |
|------|------|
| Code tested | Unit tests, linting, vulnerability checks |
| Container images built | Packaging for training and serving |
| Model trained | With latest data |
| Artifacts stored | Model Registry + Container Registry |

### 3. Deployment Phase
- **Immutable process** - same steps from start to finish
- No side effects that complicate troubleshooting
- Eliminates "works on my laptop" issues

## 🔄 ML CI/CD Pipeline Flow

```
Code/Data Update → Integration Pipeline:
  ├── Unit testing
  ├── Linting
  ├── Vulnerability checks
  ├── Packaging (container images)
  └── Staging deployment

→ Deployment Pipeline:
  ├── End-to-end testing
  ├── Model testing (known input/output)
  ├── Load testing
  └── Production deployment (canary/blue-green)
```

## 🔧 Pipeline Components

### Integration Pipeline
- Building
- Testing
- Packaging

### Deployment Pipeline
- Staging deployment
- End-to-end testing
- Production deployment
- Canary releases

## 💡 Conceitos-Chave

1. **Immutable process** - Same steps, no side effects
2. **Code + Data + Model** - Three dimensions vs traditional Code-only
3. **Model Registry** - Central storage for trained models
4. **Container Registry** - Storage for container images
5. **Canary release** - Gradual rollout strategy
6. **Model degradation** - Necessity for retraining cycles

## 📊 Model Registry Integration

```python
# Example: Registering model during training
mlflow.sklearn.log_model(
    sk_model=model,
    name="sklearn-model",
    signature=signature,
    registered_model_name="sk-learn-random-forest-reg-model",
)
```

## 🔗 Referências Cruzadas

- Complementa: MLOps Principles (002)
- Relacionado a: MLflow Model Registry (016-020)
- Pré-requisito para: Kubeflow Pipelines (039-043)

---

**Conceitos aprendidos:** 8
**Relevância:** Alta (CI/CD específico para ML)