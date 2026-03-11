# Distributed Training with Kubeflow Training Operator

**Fonte:** https://www.kubeflow.org/docs/components/trainer/legacy-v1/reference/distributed-training/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

O Training Operator do Kubeflow suporta distributed training para PyTorch e TensorFlow, criando pods Kubernetes com environment variables corretas para cada framework.

## Distributed Training para PyTorch

### Arquitetura
```
Training Operator → PyTorchJob → Workers (pods)
                                      ↓
                              torchrun CLI
                                      ↓
                           Ring All-Reduce Algorithm
```

### Como Funciona
1. **User escreve código**: Usa PyTorch Distributed APIs nativas
2. **User cria PyTorchJob**: Define número de workers e GPUs
3. **Training Operator cria pods**: Com environment variables para torchrun
4. **Gradients sincronizados**: Ring all-reduce entre workers
5. **Model treinado**: Todos os workers contribuem

### Estratégias Suportadas
- **PyTorch FSDP**: Fully Sharded Data Parallel
- **DDP**: Distributed Data Parallel
- **Ring All-Reduce**: Sincronização eficiente de gradients

### torchrun
- CLI do PyTorch para distributed training
- Environment variables configuradas pelo Training Operator
- Gerencia workers automaticamente

## Distributed Training para TensorFlow

### Arquitetura
```
Training Operator → TFJob → Parameter Servers + Workers
                                ↓
                        TF_CONFIG environment variable
                                ↓
                        Distributed Training
```

### Como Funciona
1. **User escreve código**: Usa TensorFlow Distributed APIs nativas
2. **User cria TFJob**: Define número de PSs, workers, GPUs
3. **Training Operator cria pods**: Com TF_CONFIG environment variable
4. **PS distribui dados**: Para cada worker
5. **Workers treinam**: E enviam gradients ao PS
6. **PS atualiza pesos**: Average de gradients

### Estratégias Suportadas
- **Parameter Server Strategy**: PS + workers
- **MirroredStrategy**: Single-machine multi-GPU
- **MultiWorkerMirroredStrategy**: Multi-machine
- **TPUStrategy**: Para TPUs

## TF_CONFIG Environment Variable

```json
{
  "cluster": {
    "worker": ["worker1:port", "worker2:port"],
    "ps": ["ps0:port"]
  },
  "task": {
    "type": "worker",
    "index": 0
  }
}
```

## Comparação PyTorch vs TensorFlow

| Aspecto | PyTorch | TensorFlow |
|---------|---------|------------|
| **Estratégia Principal** | Ring All-Reduce | Parameter Server |
| **CLI** | torchrun | TF_CONFIG |
| **Modelo** | Workers sincronizam diretamente | PS centralizado |
| **Escalabilidade** | Better para small-medium | Better para large-scale |
| **Gradient Sync** | All-reduce entre workers | PS averaging |

## Principais Conceitos

### PyTorchJob CRD
```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
          - name: pytorch
            resources:
              limits:
                nvidia.com/gpu: 4
    Worker:
      replicas: 3
```

### TFJob CRD
```yaml
apiVersion: kubeflow.org/v1
kind: TFJob
spec:
  tfReplicaSpecs:
    PS:
      replicas: 1
    Worker:
      replicas: 4
```

## Insights

- Training Operator abstrai complexidade de distributed training
- PyTorch usa ring all-reduce (workers se comunicam diretamente)
- TensorFlow usa parameter server (PS centralizado)
- Environment variables são configuradas automaticamente
- Suporte a múltiplas estratégias de distribuição por framework