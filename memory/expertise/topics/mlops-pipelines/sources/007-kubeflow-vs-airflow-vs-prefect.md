# MLOps Orchestration Showdown: Kubeflow vs Airflow vs Prefect

**Fonte:** https://kanerika.com/blogs/mlops-orchestration/
**Autor:** Kanerika
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Comparação detalhada das três ferramentas de orquestração ML mais populares. Foca em TCO real, integração CI/CD, experiência do desenvolvedor, e framework de decisão baseado em contexto organizacional.

---

## 🎯 TL;DR

| Ferramenta | Melhor Para |
|------------|-------------|
| **Airflow** | Times de data engineering com expertise existente, scheduling complexo |
| **Kubeflow** | ML-heavy teams com DevOps forte, distributed training em escala |
| **Prefect** | Python-first ML teams, velocidade de desenvolvimento, sem Kubernetes |

---

## 📊 Feature Comparison

| Dimensão | Airflow | Kubeflow | Prefect |
|----------|---------|----------|---------|
| **Pipeline Model** | Static DAG (asset-aware 3.0) | Static (K8s pods) | Dynamic Flows |
| **ML-Native** | Não (integrations required) | Sim (Katib, KServe built-in) | Parcial (community) |
| **Kubernetes Required** | Não (optional executor) | Sim — hard requirement | Não |
| **Observability** | Médio (log drilling) | Baixo (extra tooling) | Alto (built-in, real-time) |
| **Local Testability** | Médio (TaskFlow API) | Baixo (Kind/Minikube) | Alto (pure Python, pytest) |
| **Pipeline Versioning** | Git-based (informal) | Built-in version registry | Deployment-based |
| **Learning Curve** | Alto | Muito Alto | Baixo-Médio |
| **Scale Ceiling** | Alto | Muito Alto | Alto |
| **Self-Host Base Cost** | Baixo | Médio-Alto | Baixo |
| **Managed Option** | MWAA, Composer, Astronomer | Limitado | Prefect Cloud |
| **Community Size** | Maior (37K+ stars) | Médio (14K+, CNCF) | Growing (16K+) |

---

## 🔧 Apache Airflow: The Data Engineering Incumbent

### Origem
- Nascido no Airbnb (2014), Apache top-level (2016)
- Core: DAGs como Python code, scheduling complexo

### Airflow 3.0 (2024)
- Asset-aware scheduling (DAGs triggered by data changes)
- UI overhauled
- Scheduler performance improved
- Event-driven triggers first-class

### Ideal Para
- Times de data engineering com expertise existente
- ETL + ML workloads sob mesmo scheduling framework
- Complex scheduling needs

---

## 🔧 Kubeflow: The Kubernetes-Native ML Platform

### Origem
- Google (2018), CNCF project
- Full ML platform: pipelines, notebooks, serving, hyperparameter tuning

### Kubeflow Pipelines v2
- Python SDK melhorado
- Artifact lineage tracking
- Integration com ecosystem

### Ideal Para
- ML-heavy teams com DevOps forte
- Distributed training em grande escala
- Kubernetes já em produção

### Tradeoffs
- Kubernetes requirement = high operational overhead
- Container build cycle slows CI/CD
- Painful local development (Kind/Minikube required)

---

## 🔧 Prefect: The Python-First Modern Option

### Abordagem
- Flows e tasks com dynamic execution
- Workflows criados/modificados at runtime

### Prefect 3.0
- Autonomous task execution
- Server performance improvements
- Better event-driven capabilities

### Ideal Para
- Python-first ML engineering teams
- Velocidade de desenvolvimento
- Sem Kubernetes para começar

### Vantagens
- Local testability: pytest sem infra
- Built-in observability
- Simple CI/CD: pytest + prefect deploy
- Dynamic flows adapt to data conditions

---

## 🔄 Static vs Dynamic Execution

| Ferramenta | Tipo | Limitação |
|------------|------|-----------|
| Airflow | Static DAG | Parse-time structure, runtime branching limits |
| Kubeflow | Static (YAML/JSON) | Compiled before execution |
| Prefect | Dynamic | Tasks created at runtime based on data |

**Importante:** Para pipelines que adaptam a dados (variable training subsets, conditional preprocessing), dynamic execution matters.

---

## 📈 CI/CD Integration

| Dimensão | Airflow | Kubeflow | Prefect |
|----------|---------|----------|---------|
| **Local Test Command** | pytest with DagBag | Kind/Minikube required | pytest (pure Python) |
| **Container Build Required** | Não (DAG changes) | Sim (every component) | Não (flow changes) |
| **Deployment Mechanism** | S3 sync, Astro deploy | KFP SDK upload + image push | prefect deploy |
| **CI Step Complexity** | Médio | Alto (build→push→compile→upload) | Baixo |

**Kubeflow CI/CD Pain:** Mudar um import = rebuild + push Docker image

---

## 🛠️ Ecosystem Integration

| Integração | Airflow | Kubeflow | Prefect |
|------------|---------|----------|---------|
| MLflow | Provider package | External server | Community package |
| W&B | Custom operator | Python SDK in components | Community collection |
| Feature Stores | Python SDK in tasks | Python SDK in components | Python SDK in tasks |
| SageMaker | First-class (AWS-maintained) | Via bridge | prefect-aws |
| Vertex AI | First-class (Google-maintained) | Native | prefect-gcp |
| Azure ML | Provider package | Via AKS | prefect-azure |

**Nota:** Airflow providers para cloud ML services são mantidos pelos vendors (AWS, Google), não community.

---

## 💡 Insights Principais

1. **Orchestration decision é organizacional, não apenas técnico**
2. **Kubeflow scale ceiling é o maior, mas floor também**
3. **Prefect wins em developer experience**
4. **Airflow 3.0 é mais moderno que artigos antigos sugerem**
5. **Container build cycle do Kubeflow é fricção real em CI/CD**
6. **None has built-in model registry** - todos usam MLflow externo

---

## 🎯 Decision Framework

| Se você tem... | Escolha |
|----------------|---------|
| Data engineering team, Airflow expertise, complex scheduling | **Airflow** |
| ML-heavy team, DevOps strong, distributed training at scale | **Kubeflow** |
| Python-first team, speed priority, no Kubernetes mandate | **Prefect** |

---

## 📝 Tags

`#orchestration` `#kubeflow` `#airflow` `#prefect` `#mlops` `#comparison` `#ci-cd`