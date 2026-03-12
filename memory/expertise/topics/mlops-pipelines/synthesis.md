# MLOps Pipelines & Automation - Síntese

**Data:** 2026-03-12
**Status:** Completo
**Fontes estudadas:** 43/44 (98%)

---

## 📚 Visão Geral

Este documento sintetiza os conceitos fundamentais de **MLOps Pipelines & Automation**, cobrindo desde princípios básicos até ferramentas avançadas para automação de ML em produção.

---

## 🎯 Conceitos Fundamentais

### MLOps Maturity Levels

| Nível | Descrição | Automação |
|-------|-----------|-----------|
| **Manual** | Processo experimental, iterativo | Jupyter Notebooks, RAD tools |
| **ML Pipeline Automation** | Treino automatizado | Continuous training, data/model validation |
| **CI/CD Pipeline Automation** | Build, test, deploy automáticos | Full automation |

### MLOps Process Phases

1. **Designing** - Business/data understanding, design da solução ML
2. **Development** - PoC, iterações de algoritmos, data/model engineering
3. **Operations** - Deploy com DevOps practices (testing, versioning, CD, monitoring)

---

## 🔧 Core Components

### MLOps Stack

| Componente | Função | Ferramentas |
|------------|--------|-------------|
| **Source Control** | Version code, data, models | Git + Git LFS/DVC |
| **Model Registry** | Store artifacts, versions, metadata | MLflow, SageMaker |
| **Feature Store** | Centralized reusable features | Feast, Tecton, Hopsworks |
| **Metadata Store** | Track experiments, datasets, runs | MLflow, Kubeflow |
| **Pipeline Orchestrator** | Automate ML tasks execution | Kubeflow, Airflow, Prefect |

---

## 🔄 Feature Stores

### Comparação de Feature Stores

| Feature Store | Tipo | Real-time | Best For |
|---------------|------|-----------|----------|
| **Feast** | Open source | ✅ | Startups, flexibility |
| **Tecton** | Enterprise | ✅ (sub-second) | Enterprise, streaming |
| **Hopsworks** | Hybrid | ✅ | Regulated industries |
| **Databricks** | Lakehouse | ✅ | Spark teams |

### Feature Store Benefits
- **Feature reuse** across models
- **Point-in-time correctness** (no data leakage)
- **Online + Offline serving**
- **Centralized management**

---

## 📊 DVC - Data Version Control

### Como Funciona
```
Large file (dataset/model) → DVC creates .dvc metafile → 
Git tracks metafile → Remote storage stores actual data
```

### Key Commands
```bash
# Initialize
dvc init

# Add data
dvc add data/dataset.csv

# Track with Git
git add data/dataset.csv.dvc

# Push to remote
dvc push
```

---

## 🔄 MLflow Components

### MLflow Ecosystem

| Componente | Função |
|------------|--------|
| **Tracking** | Log params, metrics, artifacts |
| **Model Registry** | Version models, aliases, tags |
| **Projects** | Package reproducible code |
| **Models** | Standard model format |
| **Serving** | Deploy models to production |

### Model Registry Concepts

| Conceito | Descrição |
|----------|-----------|
| **Registered Model** | Container para todas versions |
| **Model Version** | Versão específica |
| **Alias** | Named reference (ex: @champion) |
| **URI** | `models:/name/version` ou `models:/name@alias` |

---

## 🚀 Pipeline Orchestration

### Orchestration Tools Comparison

| Tool | Approach | Setup | Best For |
|------|----------|-------|----------|
| **Airflow** | Task-oriented (DAGs) | Complex | Large-scale production |
| **Prefect** | Task-oriented (Pythonic) | Lightweight | Fast iteration, experimentation |
| **Dagster** | Asset-centric | Moderate | ML/data-first, lineage |
| **Kubeflow** | K8s-native | Complex | Kubernetes environments |

### When to Use Each

| Use Case | Recommended Tool |
|----------|------------------|
| Large-scale production workloads | Airflow |
| ML/data-first pipelines | Dagster |
| ML experimentation, fast teams | Prefect |
| Kubernetes-native ML | Kubeflow |

---

## 🔁 CI/CD for ML

### Diferenças do CI/CD Tradicional

| Software Tradicional | Machine Learning |
|---------------------|------------------|
| Code-focused | Code + Data + Model |
| Linear paths | Exploratory, non-linear |
| Build once, deploy | Retrain regularly |
| Version control = code | Version control = code + data + artifacts |

### ML CI/CD Workflow
```
Code/Data Update → CI Pipeline Run → Version & Log → Compare → 
If Approved → CD Pipeline → Verify Infrastructure → Test Model → Deploy
```

---

## 📈 Monitoring

### Monitoring Layers

| Layer | Métricas |
|-------|----------|
| **Service Health** | Uptime, Memory, Latency |
| **Model Performance** | Accuracy, F1, Log Loss |
| **Data Quality** | Missing values, Schema validation |
| **Drift Detection** | Data drift, Concept drift |

### Data Drift vs Concept Drift

| Tipo | Definição | Exemplo |
|------|-----------|---------|
| **Data Drift** | Mudança na distribuição dos inputs | Mais vendas online vs física |
| **Concept Drift** | Mudança na relação input-output | Comportamento de compra diferente |
| **Prediction Drift** | Mudança na distribuição das predictions | Fraud model prevê mais fraud |

---

## 🚢 Deployment Strategies

### Comparison Matrix

| Strategy | Downtime | Rollback | Cost | Risk |
|----------|----------|----------|------|------|
| **Recreate** | Yes | Slow | Low | High |
| **Blue-Green** | No | Fast | 2x | Low |
| **Canary** | No | Fast | 1.x | Very Low |
| **A/B Testing** | No | Fast | 1.x | Low |

### When to Use Each

| Strategy | Best For |
|----------|----------|
| **Recreate** | Non-critical systems, dev/staging |
| **Blue-Green** | Zero downtime required |
| **Canary** | Risk mitigation, gradual rollout |
| **A/B Testing** | Statistical comparison, feature experiments |

---

## 🛠️ Experiment Tracking Tools

### Comparison

| Tool | Tipo | Hosting | Scalability |
|------|------|---------|-------------|
| **MLflow** | Open-source | Self-hosted | Configurable |
| **W&B** | Cloud | Managed | High |
| **Neptune** | Cloud | Managed | High |
| **Comet** | Cloud | Managed | High |

---

## 💡 Lições Aprendidas

1. **MLOps is a journey** - Não é once-and-done, evolui com maturidade
2. **Tools matter, practices more** - Ferramentas são importantes, mas práticas mais
3. **Feature Stores são críticos** - Para projetos com features compartilhados
4. **Monitoring não é opcional** - Drift acontece, detectar cedo é essencial
5. **CI/CD para ML ≠ CI/CD tradicional** - Data + Model versioning obrigatório

---

## 🔗 Referências Principais

1. MLOps Principles (ml-ops.org)
2. MLOps Best Practices (Clarifai)
3. MLflow Documentation
4. Feast Documentation
5. DVC Documentation
6. Kubeflow Documentation
7. Airflow Documentation
8. Prefect Documentation
9. Evidently AI Blog
10. MLOps Zoomcamp Course

---

**Próximos passos recomendados:**
- Implementar MLflow para tracking e model registry
- Setup DVC para data versioning
- Considerar Feature Store para projetos com features compartilhados
- Implementar monitoring com Evidently para drift detection
- CI/CD pipeline com GitHub Actions + CML para ML projects