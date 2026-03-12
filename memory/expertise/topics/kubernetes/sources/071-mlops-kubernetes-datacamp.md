# MLOps on Kubernetes - DataCamp

**Fonte:** DataCamp - https://campus.datacamp.com/courses/introduction-to-kubernetes/data-engineering-and-mlops?ex=8
**Data:** 2024-2025
**Tópico:** MLOps, Kubernetes, Kubeflow, MLflow
**Status:** Lido

---

## Resumo Executivo

Introdução conceitual a MLOps em Kubernetes, explicando como o paradigma de DevOps aplica-se a ML e como Kubeflow e MLflow facilitam o deployment.

---

## Conceitos-Chave

### O que é MLOps

- **Machine Learning Operations**: Paradigma para deploy e manutenção de modelos ML
- **Origem**: Inspirado em DevOps (continuous development, deployment, operations)
- **Foco**: Workflows de melhores práticas com ênfase em melhoria contínua

### Ciclo de Vida MLOps

```
Development → Testing → Production → Monitoring → Retraining → ...
     ↑                                                        |
     └──────────────────────────────────────────────────────────┘
```

1. **Isolated Systems**: Desenvolvimento e teste em ambientes isolados
2. **Deployment**: Modelos promovidos a produção
3. **Monitoring**: Acurácia medida constantemente
4. **Improvement**: Retraining triggered por métricas

### Colaboração
- Data scientists
- Data engineers
- IT teams
- Trabalham sincronicamente em deployed models

---

## Kubernetes para MLOps

### Por que Kubernetes

| Requisito MLOps | Solução K8s |
|-----------------|-------------|
| Ambientes isolados | Pods + Storage |
| Monitoramento | Lifecycle de Pods |
| Colaboração em equipe | Arquitetura nativa |
| Workflows complexos | Orchestration built-in |

### Mapeamento MLOps → Kubernetes

- **Isolated experimental systems**: Pods e Storage K8s
- **Monitoring productive models**: Lifecycle de Pods e images
- **Team collaboration**: Arquitetura desde o início

---

## Frameworks para MLOps

### Kubeflow

#### Visão Geral
- Open-source para ML workflows em Kubernetes
- Cobertura completa do ciclo de vida
- Components independentes

#### Componentes Principais
- **Data gathering**: Coleta de dados
- **Data wrangling**: Limpeza e transformação
- **Model training/testing**: Treino e validação
- **Deployment**: Serving em produção

#### Features
- **Python API**: Desenvolvimento direto, sem kubectl
- **Flexibilidade**: Components work independently
- **Integration**: Kubernetes API nativo

### MLflow

#### Visão Geral
- Platform-agnostic MLOps
- Tracking de experiments
- Model registry
- Deployment tools

---

## Arquitetura Kubeflow

```
┌─────────────────────────────────────────────┐
│           Kubeflow Dashboard                 │
│  (Central UI for all components)             │
├─────────────────────────────────────────────┤
│           Kubeflow Components                │
│  ┌─────────────┐  ┌─────────────┐           │
│  │ Notebooks   │  │ Pipelines   │           │
│  │ (Jupyter)  │  │ (Argo)      │           │
│  └─────────────┘  └─────────────┘           │
│  ┌─────────────┐  ┌─────────────┐           │
│  │ Katib       │  │ TFJob       │           │
│  │ (AutoML)    │  │ (Training)  │           │
│  └─────────────┘  └─────────────┘           │
├─────────────────────────────────────────────┤
│           Kubernetes Layer                   │
│  (Orchestration, Scheduling, Storage)        │
└─────────────────────────────────────────────┘
```

---

## Comparação: Kubeflow vs MLflow

| Feature | Kubeflow | MLflow |
|---------|----------|--------|
| Kubernetes Native | ✅ | ❌ |
| Pipeline Orchestration | ✅ (Argo) | ✅ |
| Notebooks | ✅ | ❌ |
| AutoML | ✅ (Katib) | ❌ |
| Language | Python + YAML | Python |
| Scope | Full ML lifecycle | Experiment tracking |

---

## Insights para Kubernetes

1. **MLOps = DevOps para ML**: Mesmos princípios, contexto diferente
2. **Kubeflow é nativo**: Desenvolvido especificamente para K8s
3. **Python-first**: Kubeflow permite uso direto sem kubectl
4. **Ciclo completo**: Do desenvolvimento ao production
5. **Colaboração é chave**: Data scientists + engineers + IT

---

## Palavras-Chave
`mlops` `kubernetes` `kubeflow` `mlflow` `machine-learning` `devops` `pipelines` `collaboration`