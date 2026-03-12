# Kueue Integration with Kubeflow TrainJob

**Fonte:** https://kueue.sigs.k8s.io/docs/tasks/run/trainjobs/
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

Guia de integração entre Kueue e Kubeflow Trainer v2 para scheduling e resource management de TrainJobs. Mostra como usar ClusterTrainingRuntime e TrainingRuntime.

---

## Visão Geral

Kubeflow Trainer v2 introduz TrainJob API que funciona com Kueue para:
- Batch scheduling
- Resource management
- Quota management
- Priority scheduling

### Tipos de Runtime

| Tipo | Escopo | Uso |
|------|--------|-----|
| **ClusterTrainingRuntime** | Cluster-scoped | Common patterns, all namespaces |
| **TrainingRuntime** | Namespace-scoped | Team-specific configurations |

---

## TrainJob Definition

### Queue Selection
```yaml
metadata:
  labels:
    kueue.x-k8s.io/queue-name: user-queue
```

### Suspend Field
Kueue seta `suspend: true` via webhook e unsuspend quando admitido:
```yaml
spec:
  suspend: true
```

---

## ClusterTrainingRuntime Example

### Runtime Definition
```yaml
apiVersion: trainer.kubeflow.org/v1alpha1
kind: ClusterTrainingRuntime
metadata:
  name: torch-distributed
  labels:
    trainer.kubeflow.org/framework: torch
spec:
  mlPolicy:
    numNodes: 1
    torch:
      numProcPerNode: auto
  template:
    spec:
      replicatedJobs:
      - name: node
        template:
          spec:
            containers:
            - name: node
              image: pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime
```

### TrainJob with ClusterTrainingRuntime
```yaml
apiVersion: trainer.kubeflow.org/v1alpha1
kind: TrainJob
metadata:
  name: pytorch-distributed
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  runtimeRef:
    name: torch-distributed
    kind: ClusterTrainingRuntime
  trainer:
    numNodes: 2
    resourcesPerNode:
      requests:
        cpu: "4"
        memory: "8Gi"
        nvidia.com/gpu: "1"
```

---

## TrainingRuntime (Namespace-scoped)

### Runtime Definition
```yaml
apiVersion: trainer.kubeflow.org/v1alpha1
kind: TrainingRuntime
metadata:
  name: torch-custom
  namespace: team-a
spec:
  mlPolicy:
    numNodes: 1
    torch:
      numProcPerNode: auto
  template:
    spec:
      replicatedJobs:
      - name: node
        template:
          spec:
            containers:
            - name: trainer
              image: pytorch/pytorch:2.7.1-cuda12.8-cudnn9-runtime
              env:
              - name: CUSTOM_ENV
                value: "team-a-value"
```

### TrainJob with TrainingRuntime
```yaml
apiVersion: trainer.kubeflow.org/v1alpha1
kind: TrainJob
metadata:
  name: pytorch-custom
  namespace: team-a
  labels:
    kueue.x-k8s.io/queue-name: team-a-queue
spec:
  runtimeRef:
    name: torch-custom
    kind: TrainingRuntime
    apiGroup: trainer.kubeflow.org
  trainer:
    image: docker.io/team-a/custom-training:latest
    numNodes: 1
    resourcesPerNode:
      requests:
        cpu: "2"
        memory: "4Gi"
```

---

## Workload Priority

TrainJobs usam o mesmo mecanismo de priority via label:
```yaml
kueue.x-k8s.io/priority-class: high-priority
```

---

## LLM Fine-Tuning with Kueue

### Supported Frameworks
- **TorchTune:** Llama-3.2-1B, Qwen2.5-1.5B
- **DeepSpeed:** T5 Fine-Tuning

### Adding Kueue Label
```yaml
metadata:
  labels:
    kueue.x-k8s.io/queue-name: gpu-queue
spec:
  runtimeRef:
    name: torchtune-llama3.2-1b
    kind: ClusterTrainingRuntime
```

---

## Best Practices

| Prática | Descrição |
|---------|-----------|
| **ClusterTrainingRuntimes** | Use para padrões comuns |
| **TrainingRuntimes** | Use para necessidades específicas por time |
| **Resource Requests** | Match com ResourceFlavor do ClusterQueue |
| **Monitor Quota** | Use `kubectl get clusterqueue` |
| **Priority Classes** | Priorize workloads críticos |
| **Test Small** | Teste com recursos mínimos antes de escalar |

---

## Troubleshooting Commands

```bash
# List ClusterTrainingRuntimes
kubectl get clustertrainingruntime

# List TrainingRuntimes per namespace
kubectl get trainingruntime -n <namespace>
```

---

## Key Points

- **Queue Label:** Único Kueue-specific addition necessário
- **RuntimeRef:** Aponta para ClusterTrainingRuntime ou TrainingRuntime
- **Lifecycle:** Kueue gerencia admissão baseado em quota
- **Custom Code:** Veja Kubeflow Trainer examples

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| ClusterTrainingRuntime | Runtime cluster-scoped para padrões comuns |
| TrainingRuntime | Runtime namespace-scoped para customizações |
| kueue.x-k8s.io/queue-name | Label para Kueue scheduling |
| suspend: true | Campo setado por Kueue webhook |
| resourcesPerNode | CPU, memory, GPU requests por node |

---

## Referências

- Kubeflow Trainer: https://www.kubeflow.org/docs/components/trainer/
- Kubeflow Runtime Guide: https://www.kubeflow.org/docs/components/trainer/operator-guides/runtime/
- TorchTune Examples: https://github.com/kubeflow/trainer/tree/master/examples/torchtune/
- DeepSpeed Examples: https://github.com/kubeflow/trainer/tree/master/examples/deepspeed/