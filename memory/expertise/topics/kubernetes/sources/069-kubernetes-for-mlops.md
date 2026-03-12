# Kubernetes for MLOps - Iguazio

**Fonte:** https://www.iguazio.com/glossary/kubernetes-for-mlops/
**Tipo:** Artigo
**Data:** 2026-03-12

---

## Resumo

Visão abrangente de como Kubernetes suporta o ciclo de vida completo de ML, desde treinamento até deployment. Explica a evolução de containers, Kubeflow e práticas de MLOps.

---

## Conceitos Principais

### Evolução de Containers
```
Physical Server → VM (hypervisor) → Container (shared kernel)
```
- **VMs:** Virtualização de hardware (lento)
- **Containers:** Lightweight, portável, shared OS kernel
- **Kubernetes:** Orchestration com zero downtime

### Kubernetes Core Capabilities
- **Autoscaling:** Escala baseada em demanda
- **Failover:** Recuperação automática de falhas
- **Load Balancing:** Distribuição de tráfego
- **Deployment Patterns:** Rolling updates, rollbacks
- **Community Support:** Ecossistema maduro

### Docker para Kubernetes
```dockerfile
FROM python:3.9          # Parent image
RUN pip install flask   # Dependencies
COPY app.py /app/       # Application code
WORKDIR /app            # Working directory
CMD ["python", "app.py"] # Command
EXPOSE 3000             # Port
```

### YAML Files para Deploy
| Arquivo | Propósito |
|---------|-----------|
| configmap.yaml | Key-value configs (não-confidenciais) |
| secret.yaml | Dados sensíveis |
| deployment.yaml | Replicas, image, volumes, env, resources |
| service.yaml | Network routing |
| autoscale.yaml | HPA policies |

### Kubeflow Components
| Componente | Função |
|------------|--------|
| **Notebooks** | JupyterLab, RStudio, VS Code no cluster |
| **Pipelines** | Orquestração end-to-end de workflows |
| **Katib** | AutoML: hyperparameter tuning, NAS |
| **Model Serving** | TFServing, KFServing, Seldon, MLRun |

---

## Kubernetes no Ciclo de Vida ML

### Training Pipeline Automation
- Cada task = container com inputs/outputs definidos
- Pipeline = múltiplas tasks com specs próprias
- Hardware/software específicos por task
- **Kubeflow Pipelines** provê essa capability

### Real-Time Deployment
- Microservices deployment natural para model serving
- Framework-agnostic
- Otimização de latency e throughput

### Code Example: FastAPI Serving
```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load('model.pkl')

@app.post("/predict")
def predict(data: dict):
    return {"prediction": model.predict([data])}
```

---

## Self-Hosted vs Managed

| Opção | Prós | Contras |
|-------|------|---------|
| **Self-Hosted** | Controle total, customização | Complexo, manutenção intensiva |
| **Managed** | Menos overhead, best practices | Menos customização, custo |

**Recomendação:** Managed solutions (Iguazio, etc.) para maioria dos casos.

---

## Insights

### MLOps Problem Statement
- **Development:** Jupyter notebooks, experimental
- **Production:** Requires automation, scalability
- **Gap:** Where most ML projects fail

### Kubeflow Focus
- Principal foco: **model development**
- Model serving: integrações com TFServing, KFServing, Seldon
- Central UI: fácil adoção para practitioners

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Container Layers | Cache-friendly layering for efficiency |
| Kubeflow Notebooks | Web-based dev environment in cluster |
| Pipeline Orchestration | Containerized tasks = any ML framework |
| Managed Kubernetes | Recommended over self-hosted |

---

## Referências

- Kubernetes Architecture: https://kubernetes.io/docs/concepts/overview/components/
- Kubeflow Architecture: https://www.kubeflow.org/docs/started/architecture/
- Docker Hub: https://hub.docker.com/