# What is Kubernetes for MLOps - Iguazio

**Fonte:** https://www.iguazio.com/glossary/kubernetes-for-mlops/
**Data:** 2024-2025
**Tópico:** MLOps, Kubernetes, Kubeflow, Container Orchestration
**Status:** Lido

---

## Resumo Executivo

Visão geral abrangente de como Kubernetes suporta o ciclo de vida completo de ML, desde treinamento até deployment em produção, com foco em Kubeflow como plataforma ML nativa para Kubernetes.

---

## Conceitos-Chave

### Evolução de Deployment
1. **Servidores Dedicados**: Aplicações em hardware específico (limitado)
2. **Virtualização**: VMs para abstração, mas lentas
3. **Containers**: Leves, portáveis, compartilham kernel do OS
4. **Orquestração**: Kubernetes gerencia containers em escala

### O que é Kubernetes
- **Container Orchestration**: Gerenciamento automatizado de containers
- **Features**: Auto-scaling, failover, load balancing, zero downtime
- **Adoção**: >50% das organizações mundialmente
- **Origem**: Open-sourced pelo Google em 2014

### Docker para Kubernetes
- **Image**: Coleção de instalações, código, dependências
- **Dockerfile**: Define layers em hierarquia
- **Layers**: Inferiores mudam menos, otimizam cache
- **Container**: Imagem em execução

### Arquitetura de Deployment
```
configmap.yaml → Configurações não-confidenciais
secret.yaml → Dados sensíveis
deployment.yaml → Réplicas, imagem, volumes, env vars
service.yaml → Exposição e load balancing
autoscale.yaml → HPA para scaling
```

---

## Kubeflow: ML no Kubernetes

### O que é Kubeflow
- Plataforma ML open-source sobre Kubernetes
- Desenvolvimento e deployment de workflows ML
- **Foco principal**: Desenvolvimento de modelos

### Componentes Principais

#### 1. Kubeflow Notebooks
- JupyterLab, RStudio, VS Code (code-server)
- Rodam diretamente no cluster
- Fácil compartilhamento e escalabilidade

#### 2. Kubeflow Pipelines
- Orquestração end-to-end
- Cada step é containerizado
- Suporta qualquer framework ML

#### 3. Katib (AutoML)
- Hyperparameter tuning
- Otimização Bayesiana
- Neural Architecture Search
- Hyperband

### Model Serving
- TFServing (TensorFlow)
- KFServing
- MLRun
- Seldon

---

## Kubernetes para Pipeline de Treinamento

### Containerização de Pipelines
- Cada task é container Docker
- Inputs, lógica, outputs bem definidos
- Pipeline = múltiplas tasks
- Hardware/software específicos por task

### Benefícios
- **Escalabilidade**: Recursos sob demanda
- **Modularidade**: Tasks independentes
- **Portabilidade**: Roda em qualquer cluster
- **Reprodutibilidade**: Ambientes consistentes

### Desafios
- **Curva de aprendizado**: Íngreme para data scientists
- **Complexidade**: Configuração inicial

---

## Kubernetes para Deployment em Tempo Real

### Por que K8s para ML Serving
- **Microservices**: Deployment natural
- **Escalabilidade**: Latência e throughput otimizados
- **Abstração**: Container orchestration transparente
- **Resiliência**: Self-healing, rolling updates

### Exemplo: FastAPI para Model Serving
```python
from fastapi import FastAPI
import pickle

app = FastAPI()

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.post("/predict")
def predict(data: dict):
    return {"prediction": model.predict(data)}
```

---

## Self-Hosted vs Managed

### Recomendação
- **Self-hosted**: Apenas para requisitos extremamente customizados
- **Managed**: Preferível para maioria dos casos
- **Exemplos managed**: Iguazio, cloud providers
- **Benefícios managed**: Menos overhead, melhores práticas

---

## Comparação: Kubeflow vs Outros

| Feature | Kubeflow | MLflow | Flyte |
|---------|----------|--------|-------|
| Pipeline Orchestration | ✅ | ✅ | ✅ |
| Notebook Integration | ✅ | ❌ | ❌ |
| AutoML | ✅ (Katib) | ❌ | ❌ |
| Model Serving | ✅ | ✅ | ❌ |
| Kubernetes Native | ✅ | ❌ | ✅ |

---

## Insights para Kubernetes

1. **Kubeflow é a solução padrão** para ML em Kubernetes
2. **Containerização é fundação**: Pipelines = containers
3. **Self-hosted é difícil**: Preferir managed solutions
4. **Model serving é simples**: FastAPI + Docker + K8s
5. **MLOps = DevOps para ML**: Princípios similares

---

## Palavras-Chave
`kubernetes` `kubeflow` `mlops` `container-orchestration` `model-serving` `pipelines` `katib` `docker`