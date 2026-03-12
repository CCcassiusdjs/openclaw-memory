# Orchestration Showdown: Dagster vs Prefect vs Airflow - Resumo

**Fonte:** https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow
**Tipo:** Comparison Guide
**Data:** 2026-03-12

---

## 🎯 Visão Geral

Comparação de ferramentas de **data orchestration** para ML pipelines:
- **Airflow** - Battle-tested, Apache Foundation
- **Dagster** - Asset-centric, data-first approach
- **Prefect** - Lightweight, Pythonic, rapid iteration

**Updated:** November 2025 (Airflow 3.0, Dagster GA Components, Prefect serverless)

## 📋 O que são Orchestration Tools?

**Orchestration tools** = Condutores do ambiente tech:
- **Deployment** - Automatizar rollout de apps e modelos
- **Scaling** - Ajustar recursos para demanda
- **Workflow Automation** - CI/CD pipelines, ML training jobs

### Por que importam?
- **Efficiency** - Automatizar tarefas repetitivas
- **Consistency** - Padronizar deployments
- **Scaling** - Handle heavy lifting de scaling

## 🔄 Apache Airflow

### O que é
Workflow orchestration tool para distributed applications:
- Jobs via **DAGs** (Directed Acyclic Graphs)
- Rich UI para visualização
- Task monitoring e logs

### Features

| Feature | Descrição |
|---------|-----------|
| **Dynamic Workflows** | DAGs para dependências complexas |
| **Community Support** | Apache Foundation backing |
| **Rich Operator Library** | Pre-built operators para databases, cloud, APIs |
| **Scalability** | LocalExecutor, CeleryExecutor, KubernetesExecutor |
| **Logging & Alerting** | Built-in logging e notifications |

### Benefícios
- Battle-tested (10+ anos)
- Apache Foundation backing
- Milhares de companies usando

## 🏗️ Dagster

### Abordagem
**Asset-centric approach** - foco em data products e lineage:
- Pipelines around **data they produce**
- Data semantics integradas
- Components framework (GA Oct 2025)

### Features
- **Software-defined assets** - Data assets como first-class citizens
- **Lineage tracking** - Built-in data lineage
- **Opinionated** - Mais estrutura, mais data-centric
- **ML integration** - Natural fit para ML pipelines

## 🚀 Prefect

### Abordagem
**Lightweight, Pythonic** - workflows via Python functions e DAGs:
- Flexible e decoupled
- Rapid iteration capabilities
- Ideal para experimentation
- Serverless offerings (2025)

### Features
- **Task-oriented** - Workflows via Python functions
- **Lightweight setup** - Minimal initial configuration
- **Python-native** - Type hints, async/await
- **Modern UI** - Real-time monitoring
- **Serverless** - Cloud-native execution

## 📊 Comparison Matrix

| Aspecto | Airflow | Dagster | Prefect |
|---------|---------|---------|---------|
| **Approach** | Task-oriented | Asset-centric | Task-oriented |
| **Setup** | Complex | Moderate | Lightweight |
| **MLOps Support** | Airflow 3.0 (30% users) | Native ML focus | Fast iteration |
| **Learning Curve** | Steeper | Moderate | Gentle |
| **Community** | Largest | Growing | Growing |
| **Production Ready** | Battle-tested | Modern | Modern |

## 💡 When to Use Each

### Airflow
- ✅ Large-scale production workloads
- ✅ Existing Apache ecosystem
- ✅ Need extensive operator library
- ✅ Team experience with DAGs

### Dagster
- ✅ ML/data-first pipelines
- ✅ Need built-in lineage tracking
- ✅ Asset-centric workflows
- ✅ Data governance requirements

### Prefect
- ✅ ML experimentation
- ✅ Fast-moving data science teams
- ✅ Python-native workflows
- ✅ Minimal setup needs

## 🔗 Referências Cruzadas

- Complementa: Airflow Overview (006)
- Relacionado a: Prefect Overview (007)
- Pré-requisito para: Pipeline Orchestration Decision

---

**Conceitos aprendidos:** 15
**Relevância:** Alta (orchestration tools comparison)