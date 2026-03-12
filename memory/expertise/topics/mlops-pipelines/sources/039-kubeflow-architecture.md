# Kubeflow Architecture Overview - Resumo

**Fonte:** https://www.kubeflow.org/docs/started/architecture/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 Kubeflow Ecosystem

Kubeflow builds on **Kubernetes** as a system for deploying, scaling, and managing AI platforms.

## 🔄 AI Lifecycle Stages

| Stage | Description | Tools |
|-------|-------------|-------|
| **Data Preparation** | Ingest raw data, feature engineering, prepare training data | Spark, Dask, Flink, Ray |
| **Model Development** | Choose ML framework, develop architecture, explore pre-trained models | Notebooks, Jupyter |
| **Model Training** | Train/fine-tune on large-scale compute | Distributed training |
| **Model Optimization** | Hyperparameter tuning, AutoML, model compression | Katib |
| **Model Serving** | Online/batch inference, feature extraction | KServe, Feature Store |

## 🏗️ Kubeflow Projects Mapping

### Development Phase
| Project | Purpose |
|---------|---------|
| **Spark Operator** | Data preparation, feature engineering |
| **Notebooks** | Interactive development, experimentation |
| **Trainer** | Large-scale distributed training, LLM fine-tuning |
| **Katib** | Hyperparameter tuning, AutoML |

### Production Phase
| Project | Purpose |
|---------|---------|
| **Model Registry** | Store ML metadata, artifacts, prepare for serving |
| **KServe** | Online and batch inference |
| **Feast** | Feature store (offline + online features) |
| **Pipelines** | Build, deploy, manage AI lifecycle steps |

## 📋 Kubeflow Components

### Kubeflow Spark Operator
- Data preparation
- Feature engineering

### Kubeflow Notebooks
- Interactive data science
- Model development experimentation
- Jupyter, VS Code, RStudio support

### Kubeflow Trainer
- Large-scale distributed training
- LLM fine-tuning
- Multi-node, multi-GPU support

### Kubeflow Katib
- Hyperparameter optimization
- Neural architecture search
- Model compression

### Kubeflow Model Registry
- ML metadata storage
- Model artifacts
- Production preparation

### KServe
- Online inference
- Batch inference
- Model serving

### Feast
- Feature store
- Offline features (training)
- Online features (inference)

### Kubeflow Pipelines
- Build AI workflows
- Deploy and manage steps
- DSL for pipeline definition

## 🖥️ Kubeflow Interfaces

### Dashboard
- Central Dashboard
- Hub for AI platform and tools
- Exposes UIs of cluster components

### APIs and SDKs
| API/SDK | Purpose |
|--------|---------|
| **Pipelines API/SDK** | DSL for pipeline definition |
| **Kubeflow Python SDK** | Trainer API, TrainJobs management |
| **Katib Python SDK** | Experiments, hyperparameter tuning |

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **AI Lifecycle** | Iterative process: prep → dev → train → optimize → serve |
| **Development Phase** | Experimentation, development |
| **Production Phase** | Serving, monitoring, inference |
| **Distributed Training** | Multi-node, multi-GPU training |
| **Model Registry** | Central artifact storage |

## 🔗 Referências Cruzadas

- Complementa: MLOps Principles (002)
- Relacionado a: Feature Stores (Feast) (021)
- Pré-requisito para: Kubeflow Pipelines (039-043)

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (Kubeflow architecture overview)