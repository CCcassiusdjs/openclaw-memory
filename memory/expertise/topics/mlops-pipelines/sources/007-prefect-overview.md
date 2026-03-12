# Prefect Orchestration Engine - Resumo

**Fonte:** https://docs.prefect.io/latest/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é Prefect?

Prefect é um **open-source orchestration engine** que transforma Python functions em **production-grade data pipelines**:
- Workflows em Python puro (sem DSLs ou YAML)
- Roda em qualquer lugar que rode Python

## 🔧 Features Essenciais

| Feature | Descrição |
|---------|-----------|
| **Pythonic** | Workflows em Python nativo, type hints, async/await |
| **State & Recovery** | State management, resume interrupted runs, cache |
| **Flexible Execution** | Local → containers → Kubernetes → cloud |
| **Event-Driven** | Schedules, external events, API triggers |
| **Dynamic Runtime** | Tasks criadas dinamicamente baseadas em dados |
| **Modern UI** | Real-time monitoring, logging, DAG visualization |
| **CI/CD First** | Test e simulate como Python normal |

## 📋 Core Concepts

### Flows
```python
from prefect import flow

@flow
def my_workflow():
    # Workflow logic
    pass
```

### Tasks
```python
from prefect import task

@task
def my_task():
    # Task logic
    pass
```

### Deployments
- Run flows on schedule
- Deploy to specific infrastructure
- Manage via CLI or UI

## 🚀 Quickstart

### Install
```bash
pip install prefect
prefect server start
```

### Create Flow
```python
from prefect import flow, task

@task
def extract():
    return [1, 2, 3]

@task
def transform(data):
    return [x * 2 for x in data]

@flow
def etl_pipeline():
    data = extract()
    result = transform(data)
    return result

if __name__ == "__main__":
    etl_pipeline()
```

## 🤖 AI Assistants e MCP

Prefect MCP Server para conectar:
- Claude Code
- Cursor
- Codex CLI
- Gemini CLI

Capabilities:
- Inspect deployments
- Flow runs
- Task runs
- Logs
- Built-in docs search

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Flow** | Workflow container decorado com @flow |
| **Task** | Unidade de trabalho decorada com @task |
| **Deployment** | Flow configurado para rodar em infra específica |
| **State** | Success, failure, retry, running |
| **MCP Server** | Model Context Protocol para AI assistants |

## 🔄 Comparação com Airflow

| Aspecto | Airflow | Prefect |
|---------|---------|---------|
| **DSL** | Python + DSL | Pure Python |
| **State Management** | Manual | Automático |
| **Local Dev** | Complexo | Simples |
| **Dynamic Tasks** | Limitado | Nativo |
| **UI** | Clássica | Moderna |

## 🔗 Referências Cruzadas

- Alternativa a: Airflow (006), Dagster
- Complementa: Kubeflow Pipelines (039-040)
- Relacionado a: MLflow (016-020)

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (pipeline orchestration modern)