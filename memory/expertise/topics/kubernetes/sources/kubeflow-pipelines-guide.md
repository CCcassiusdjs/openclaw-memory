# Building ML Pipelines with Kubeflow: Complete Guide

**Fonte:** https://medium.com/@saadullahkhanwarsi/building-ml-pipelines-with-kubeflow-a-complete-guide-for-mlops-7c621aee29bf  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Guia completo de Kubeflow Pipelines para MLOps, cobrindo desde instalação local até criação de pipelines ML completos.

## Por que Kubeflow?

### Problemas que Resolve
| Problema | Solução Kubeflow |
|----------|------------------|
| **Reproducibility** | Tracking automático de datasets, código, parâmetros |
| **Scalability** | Distributed training, CPU/GPU/TPU flexibility |
| **Collaboration** | Compartilhamento de experiments e pipelines |
| **Monitoring** | Performance tracking pós-deployment |
| **Versioning** | Gestão de model e data versions |

## Componentes Kubeflow

| Componente | Propósito |
|------------|-----------|
| **Kubeflow Pipelines** | Workflow orchestration, experiment tracking |
| **Jupyter Notebooks** | Interactive development |
| **Katib** | Hyperparameter tuning |
| **KFServing/KServe** | Model serving e inference |
| **Kubeflow Training** | Distributed training operators |
| **Metadata** | Artifact e lineage tracking |

## Setup Local (Kind)

### Pré-requisitos
- Docker Desktop
- macOS/Linux
- 8GB+ RAM
- Python e Kubernetes básico

### Instalação
```bash
# 1. Kind (Kubernetes in Docker)
brew install kind
kind create cluster --name kind-cluster

# 2. Helm
brew install helm

# 3. Kubeflow Pipelines
helm repo add getindata https://getindata.github.io/helm-charts/
helm install my-kubeflow-pipelines getindata/kubeflow-pipelines \
  --version 1.6.2 \
  --set platform.managedStorage.enabled=false \
  --set platform.cloud=gcp \
  --namespace kubeflow-pipelines \
  --create-namespace

# 4. Acessar UI
kubectl port-forward -n kubeflow-pipelines svc/ml-pipeline-ui 8080:80
```

## Pipeline ML Exemplo

### Arquitetura do Pipeline
1. **create-data**: Gera dataset sintético (1000 samples, 3 features)
2. **split-data**: Divide em train/test (80/20)
3. **train-model**: Aplica classificador rule-based
4. **test-model**: Calcula métricas (accuracy, precision, recall, F1)
5. **generate-report**: Gera relatório final

### YAML Structure
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: ml-pipeline-
  namespace: kubeflow-pipelines
spec:
  entrypoint: ml-pipeline
  serviceAccountName: pipeline-runner
  templates:
  - name: create-data
    container:
      image: python:3.8-slim
      command: [python3, -c]
      args:
      - |
        # Python code for data generation
        # Creates 1000 samples with 3 features
        # Label: 1 if sum(features) > 15, else 0
```

### DAG Dependencies
```yaml
- name: ml-pipeline
  dag:
    tasks:
    - name: create-data
      template: create-data
    - name: split-data
      template: split-data
      dependencies: [create-data]
    - name: train-model
      template: train-model
      dependencies: [split-data]
    - name: test-model
      template: test-model
      dependencies: [train-model]
    - name: generate-report
      template: generate-report
      dependencies: [test-model]
```

## Resultados Esperados

| Métrica | Valor Esperado |
|---------|----------------|
| **Accuracy** | ~95% |
| **Precision** | ~94% |
| **Recall** | ~96% |
| **F1-Score** | ~95% |

## Monitoring

### Dashboard Features
- Real-time logs e status updates
- Execution times para cada step
- Output metrics e visual artifacts
- DAG visualization

## Próximos Passos

### Pipelines mais Complexos
- Integrar scikit-learn ou TensorFlow
- Adicionar preprocessing, validation, monitoring
- Katib para hyperparameter tuning

### Produção
- Deploy para EKS, GKE, AKS
- CI/CD com GitHub Actions ou ArgoCD
- Model drift detection e real-time monitoring

## Troubleshooting

```bash
# Pods não iniciam
kubectl get pods -n kubeflow-pipelines
kubectl logs <pod-name> -n kubeflow-pipelines

# UI não acessível
kubectl port-forward -n kubeflow-pipelines svc/ml-pipeline-ui 8080:80

# Clean restart
kind delete cluster --name kind-cluster
kind create cluster --name kind-cluster
```

## Insights

- Kubeflow Pipelines traz estrutura e escalabilidade para ML
- DAG workflows permitem reproducibility
- Kind é ideal para desenvolvimento local
- Integração com GitOps é essencial para produção
- Monitoring e experiment tracking são built-in