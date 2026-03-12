# MLOps on Kubernetes - DataCamp

**Fonte:** https://campus.datacamp.com/courses/introduction-to-kubernetes/data-engineering-and-mlops?ex=8
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## Resumo

Visão geral de como MLOps e Kubernetes trabalham juntos. Explica o paradigma MLOps e como Kubeflow facilita o deployment de ML workflows.

---

## Conceitos Principais

### O que é MLOps?
- Paradigma para deploy e manutenção de ML models em produção
- Best-practice workflows com foco em continuous development
- Inspirado por DevOps: development, deployment, operations
- Modelos desenvolvidos/testados em sistemas isolados → deploy para produção
- Continuous monitoring, accuracy measurement, retraining triggers

### Fluxo MLOps
```
Development (Isolated Systems)
    ↓
Testing (Isolated Systems)
    ↓
Production Deployment
    ↓
Continuous Monitoring
    ↓
Accuracy Measurement
    ↓
Retraining (when needed)
```

### MLOps + Kubernetes Mapping
| MLOps Requirement | Kubernetes Solution |
|-------------------|---------------------|
| Sistemas experimentais isolados | Pods + Storage |
| Monitoring de modelos | Pod lifecycle + deployed images |
| Trabalho síncrono em equipe | Arquitetura colaborativa |

### Frameworks para MLOps
- **MLflow:** Open-source platform for ML lifecycle
- **Kubeflow:** Kubernetes-native ML platform

---

## Kubeflow Overview

### Propósito
- Deployment simples de ML workflows em Kubernetes
- Cobre cada step do ML model lifecycle:
  - Data gathering
  - Data wrangling
  - Model training
  - Model testing
  - Deployment

### Arquitetura
- **Componentes independentes:** Cada step é um componente separado
- **Máxima flexibilidade:** Workflows customizados
- **Python SDK:** Interage com Kubernetes API diretamente
- **No kubectl necessário:** Python é suficiente

### Componentes Principais
1. **Notebooks:** Jupyter notebooks no cluster
2. **Pipelines:** Orquestração de workflows
3. **Katib:** AutoML e hyperparameter tuning
4. **Training Operators:** TFJob, PyTorchJob, etc.
5. **Serving:** Model deployment

---

## Insights

### Vantagens do Kubeflow
- **Abstraction:** Python interface instead of kubectl
- **Modularity:** Components work independently
- **Flexibility:** Create any workflow type
- **Native:** Built specifically for Kubernetes

### Team Collaboration
- Data scientists, data engineers, IT teams
- Synchronous work on deployed models
- Accuracy improvements together

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| MLOps Paradigm | Deploy + maintain ML models in production |
| Isolated Systems | Dev/test environments via Pods |
| Kubeflow Python SDK | Direct Kubernetes API interaction |
| Continuous Monitoring | Model accuracy measurement |
| Team Synchronization | Collaborative model improvement |

---

## Referências

- MLflow: https://mlflow.org/
- Kubeflow: https://www.kubeflow.org/