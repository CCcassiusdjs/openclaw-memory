# Katib: Kubernetes-Native AutoML

**Fonte:** https://www.kubeflow.org/docs/components/katib/overview/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Katib é um projeto Kubernetes-native para AutoML, suportando hyperparameter tuning, early stopping e neural architecture search (NAS).

## O que é Katib?

Katib é agnóstico a ML frameworks:
- Suporta qualquer linguagem
- TensorFlow, MXNet, PyTorch, XGBoost, e outros
- Hyperparameter tuning
- Early stopping
- Neural Architecture Search (NAS)

## Algoritmos Suportados

| Algoritmo | Tipo | Uso |
|-----------|------|-----|
| **Bayesian Optimization** | Hyperparameter | Efficient exploration |
| **Tree of Parzen Estimators (TPE)** | Hyperparameter | Sequential model-based |
| **Random Search** | Hyperparameter | Baseline, simple |
| **CMA-ES** | Hyperparameter | Evolution strategy |
| **Hyperband** | Early Stopping | Resource-efficient |
| **Efficient Neural Architecture Search (ENAS)** | NAS | Architecture optimization |
| **Differentiable Architecture Search (DARTS)** | NAS | Gradient-based |

## Por que Katib?

### 1. Distributed Training Support
- Orquestra multi-node & multi-GPU workloads
- Integração com Kubeflow Training Operator (PyTorchJob, TFJob)
- Otimiza hyperparameters para large models

### 2. Workflow Orchestration
- Argo Workflows integration
- Tekton Pipelines integration
- Advanced optimization use-cases

### 3. Extensibility & Portability
- Roda Kubernetes containers
- Qualquer ML framework
- Qualquer linguagem
- Qualquer task (desde que tenha métricas)

### 4. Algorithm Library
- Integração com Hyperopt
- Integração com Optuna
- State-of-the-art algorithms
- Custom algorithms support

## Arquitetura

```
User → Experiment CRD → Katib Controller → Suggestions → Trials
                                                            ↓
                                                    Training Jobs (PyTorchJob, TFJob, etc.)
                                                            ↓
                                                    Metrics Collection
                                                            ↓
                                                    Optimization Loop
```

### Componentes
- **Experiment**: CRD que define optimization goal
- **Suggestion**: Algoritmo que propõe hyperparameters
- **Trial**: Execução de um set de hyperparameters
- **Metrics Collector**: Coleta métricas de cada trial

## Casos de Uso

### Hyperparameter Tuning
```yaml
apiVersion: kubeflow.org/v1beta1
kind: Experiment
metadata:
  name: pytorch-hpo
spec:
  objective:
    type: maximize
    goal: 0.99
    objectiveMetricName: accuracy
  parameters:
  - name: lr
    parameterType: double
    feasibleSpace:
      min: "0.001"
      max: "0.1"
  algorithm:
    algorithmName: bayesianoptimization
```

### Early Stopping
- Interrompe trials ruins cedo
- Economiza recursos
- Algoritmos: Hyperband, Median stopping rule

### Neural Architecture Search
- Busca automática de arquiteturas
- ENAS, DARTS
- Para deep learning research

## Integrações

| Componente | Integração |
|------------|------------|
| **Training Operator** | PyTorchJob, TFJob, MPIJob |
| **Argo Workflows** | Pipeline orchestration |
| **Tekton Pipelines** | CI/CD integration |
| **Optuna** | Optimization algorithms |
| **Hyperopt** | Bayesian optimization |

## Insights

- Katib é Kubernetes-native, não requer mudanças no código
- Agnóstico a frameworks - funciona com qualquer ML framework
- Algoritmos state-of-the-art built-in
- Early stopping economiza recursos significativamente
- Custom algorithms são suportados
- Integração com Kubeflow ecosystem completa o MLOps lifecycle