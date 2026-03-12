# Apache Airflow Overview - Resumo

**Fonte:** https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é Airflow?

Airflow é uma plataforma para **build and run workflows**:
- Workflows como **DAGs** (Directed Acyclic Graphs)
- Contém **Tasks** individuais com dependências e data flows

Airflow é **agnostico** - pode orquestrar qualquer coisa.

## 🏗️ Arquitetura

### Componentes Obrigatórios

| Componente | Função |
|------------|--------|
| **Scheduler** | Trigger workflows, submit tasks ao executor |
| **DAG Processor** | Parse DAG files, serializa para metadata DB |
| **Webserver** | UI para inspecionar, trigger, debug DAGs/tasks |
| **DAG Files** | Pasta de arquivos DAG lidos pelo scheduler |
| **Metadata DB** | PostgreSQL ou MySQL para state de tasks/DAGs |

### Componentes Opcionais

| Componente | Função |
|------------|--------|
| **Worker** | Executa tasks (CeleryExecutor, KubernetesExecutor) |
| **Triggerer** | Executa deferred tasks em asyncio event loop |
| **Plugins** | Extende funcionalidade do Airflow |

## 🔄 Executors

| Executor | Descrição |
|----------|-----------|
| **LocalExecutor** | Scheduler e workers no mesmo processo |
| **CeleryExecutor** | Workers distribuídos |
| **KubernetesExecutor** | Tasks como PODs no Kubernetes |

## 📋 DAGs e Tasks

### DAG (Directed Acyclic Graph)
- Define dependências entre tasks
- Especifica ordem de execução
- Python code para definir

### Task
- Unidade de trabalho
- Pode ser: fetch data, run analysis, trigger systems
- Usa **Operators** para definir o que fazer

## 🛡️ Security Model

### User Roles
| Role | Responsabilidade |
|------|------------------|
| **Deployment Manager** | Instala e configura Airflow |
| **DAG Author** | Escreve DAGs |
| **Operations User** | Triggers DAGs/tasks, monitora execução |

### Security Perimeters
- Componentes podem rodar em máquinas diferentes
- Isolamento entre scheduler, workers, DAG processor
- Controle de acesso diferente por componente

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **DAG** | Directed Acyclic Graph - estrutura do workflow |
| **Task** | Unidade de trabalho individual |
| **Operator** | Define o que a task faz |
| **Executor** | Componente que executa tasks |
| **Scheduler** | Orquestra execução |
| **Webserver** | Interface de visualização |
| **Metadata DB** | Armazena estado |

## 🔗 Deployments

### Basic (Single Machine)
- LocalExecutor
- Scheduler + workers no mesmo processo
- Sem triggerer (sem task deferral)

### Distributed
- Componentes distribuídos em múltiplas máquinas
- Roles separados
- Security perimeters entre componentes

## 🔗 Referências Cruzadas

- Alternativa a: Prefect, Dagster
- Complementa: Kubeflow Pipelines (039-040)
- Relacionado a: Pipeline Orchestration

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (pipeline orchestration popular)