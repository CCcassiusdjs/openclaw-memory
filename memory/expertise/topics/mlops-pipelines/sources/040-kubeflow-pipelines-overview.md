# Kubeflow Pipelines Overview - Resumo

**Fonte:** https://www.kubeflow.org/docs/components/pipelines/overview/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é Kubeflow Pipelines (KFP)?

**KFP** é uma plataforma para construir e deployar **workflows ML portáteis e escaláveis** usando containers em sistemas baseados em Kubernetes.

## 📋 Capacidades do KFP

| Capacidade | Descrição |
|------------|-----------|
| **Author workflows** | Pipelines nativamente em Python |
| **Custom components** | Criar componentes ML ou usar existentes |
| **Pass artifacts** | Passar parâmetros e artefatos entre componentes |
| **Manage & track** | Visualizar pipelines, runs, experiments |
| **Efficient compute** | Paralelismo + caching |
| **Python-centric** | Minimiza necessidade de containers |
| **Cross-platform** | Portabilidade via IR YAML |

## 🔄 O que é um Pipeline?

Um **pipeline** é uma definição de workflow que compõe um ou mais **components** em um **DAG** (Directed Acyclic Graph):

| Conceito | Descrição |
|----------|-----------|
| **Pipeline** | Workflow como DAG |
| **Component** | Step do pipeline (container execution) |
| **Artifact** | Output de um componente (ML model, dataset) |
| **IR YAML** | Intermediate Representation YAML |

## 🚀 Backend Conformant

KFP pode rodar em:
- **Open source KFP backend** (Kubeflow core component)
- **Google Cloud Vertex AI Pipelines**

## 📝 Authoring Components

### KFP Python SDK
```python
from kfp import dsl

@dsl.component
def my_component(input_param: str) -> str:
    # Component logic
    return output_value

@dsl.pipeline
def my_pipeline():
    comp1 = my_component(input_param='value')
    comp2 = my_component(input_param=comp1.output)
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **DAG** | Directed Acyclic Graph - pipeline structure |
| **Component** | Single container execution |
| **IR YAML** | Intermediate Representation - portable format |
| **Backend** | KFP-conformant execution environment |
| **Artifact** | ML model, dataset, or other output |

## 🔗 Referências Cruzadas

- Complementa: Kubeflow Architecture (039)
- Pré-requisito: Kubernetes basics
- Relacionado a: MLflow Pipelines (031-034)

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (Kubeflow Pipelines overview)