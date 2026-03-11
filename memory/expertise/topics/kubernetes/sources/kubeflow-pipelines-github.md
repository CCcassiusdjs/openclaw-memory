# Kubeflow Pipelines: GitHub Overview

**Fonte:** https://github.com/kubeflow/pipelines  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Kubeflow Pipelines é um toolkit ML dedicado a tornar deployments de ML workflows em Kubernetes simples, portáteis e escaláveis.

## Objetivos

| Objetivo | Descrição |
|----------|-----------|
| **End to end orchestration** | Simplificar orquestração de pipelines ML |
| **Easy experimentation** | Gerenciar trials/experiments facilmente |
| **Easy re-use** | Re-utilizar componentes e pipelines |

## Arquitetura

```
Kubeflow Pipelines SDK → API Server → Argo Workflows → Kubernetes
```

### Dependências
| Componente | Versão |
|------------|--------|
| Argo Workflows | v3.5, v3.6, v3.7 |
| MySQL | v8 |

## Instalação

### Opção 1: Kubeflow Platform
- Instalar como parte da plataforma completa
- Todos os componentes integrados

### Opção 2: Standalone Service
- Deploy apenas Pipelines
- Para uso independente

### Container Runtime
- Docker deprecated no Kubernetes 1.20+
- Emissary Executor é o default desde KFP 1.8
- Container runtime agnostic (funciona com qualquer runtime)

## Kubeflow Pipelines SDK

### Python SDK
```python
import kfp

@kfp.dsl.pipeline(name='My Pipeline')
def my_pipeline():
    step1 = component1()
    step2 = component2(input=step1.output)
```

### Features
- Python DSL para definir pipelines
- Componentes reutilizáveis
- Type checking
- Output/input passing
- Caching

## Componentes

### Pipelines
- Workflows end-to-end
- Definidos em Python ou YAML
- Versionados
- Compartilháveis

### Components
- Unidades de processamento
- Container-based
- Inputs e outputs tipados
- Reutilizáveis entre pipelines

### Experiments
- Agrupamento de runs
- Comparação de trials
- Tracking de métricas

### Runs
- Execução de um pipeline
- Logs e artifacts
- Visualização

## Recursos

### Documentação
- [Pipelines Overview](https://www.kubeflow.org/docs/components/pipelines/overview/)
- [API Spec](https://www.kubeflow.org/docs/components/pipelines/reference/api/kubeflow-pipeline-api-spec/)
- [Python SDK Reference](https://kubeflow-pipelines.readthedocs.io/en/stable/)

### Tutoriais
- From Raw Data to Model Serving (Blueprint)
- Getting Started with Kubeflow Pipelines (Google Cloud)
- How to Create and Deploy ML Pipeline (3 parts)

## Comunidade

### Canais
- **Community Meeting**: Every other Wed 10-11AM PST
- **Slack**: #kubeflow-pipelines on CNCF Slack
- **Meeting Notes**: bit.ly/kfp-meeting-notes

### Contribuição
- CONTRIBUTING.md para guidelines
- developer_guide.md para build from source
- just command runner para conveniência

## Argo Workflows Integration

Kubeflow Pipelines usa Argo Workflows por baixo dos panos:
- Orquestração de Kubernetes resources
- DAG execution
- Retry logic
- Parallel execution
- Argo community muito colaborativa

## Insights

- KFP abstrai complexidade de Argo Workflows
- Python SDK é a forma principal de definir pipelines
- Componentes são container-based (portabilidade)
- Emissary Executor resolve problemas com container runtime
- Integração tight com resto do Kubeflow ecosystem
- Comunidade ativa com meetings regulares