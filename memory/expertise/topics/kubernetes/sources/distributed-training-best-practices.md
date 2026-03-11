# Distributed Training on Kubernetes: Best Practices & Implementation

**Fonte:** https://collabnix.com/distributed-training-on-kubernetes-best-practices-implementation/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Guia comprehensive para distributed training em Kubernetes, cobrindo PyTorchJob, TFJob, NCCL optimization, fault tolerance e production best practices.

## Arquitetura de Distributed Training

### Patterns

| Pattern | Descrição | Uso |
|---------|-----------|-----|
| **Data Parallelism** | Cada worker treina em data subsets diferentes | Mais comum |
| **Model Parallelism** | Partes do modelo distribuídas entre workers | Modelos grandes |
| **Hybrid Parallelism** | Combina data e model parallelism | Extreme scale |

### Componentes

```
Training Operator → PyTorchJob/TFJob CRD → Master + Workers
                                                    ↓
                                          Kubernetes Pods
                                                    ↓
                                          Distributed Training
```

## Kubeflow Training Operator

### Instalação
```bash
kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone?ref=v1.7.0"

# Verify
kubectl get pods -n kubeflow
kubectl get crd | grep kubeflow.org
```

### CRDs Criados
- PyTorchJob
- TFJob
- MXJob
- XGBoostJob
- MPIJob

## PyTorch Distributed Training

### Setup Distributed
```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

def setup_distributed():
    dist.init_process_group(
        backend='nccl',
        init_method='env://',
    )
    torch.cuda.set_device(int(os.environ['LOCAL_RANK']))
```

### DDP Training
```python
model = YourModel().cuda()
model = DDP(model, device_ids=[int(os.environ['LOCAL_RANK'])])

# Distributed sampler
train_sampler = DistributedSampler(train_dataset)
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    sampler=train_sampler,
    num_workers=4,
    pin_memory=True
)
```

### PyTorchJob YAML
```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-distributed-training
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
                nvidia.com/gpu: 1
                memory: 16Gi
    Worker:
      replicas: 3
      template:
        spec:
          containers:
          - name: pytorch
            resources:
              limits:
                nvidia.com/gpu: 1
                memory: 16Gi
```

## TensorFlow Distributed Training

### TFJob com Parameter Server
```yaml
apiVersion: kubeflow.org/v1
kind: TFJob
metadata:
  name: tensorflow-distributed-training
spec:
  tfReplicaSpecs:
    Chief:
      replicas: 1
    Worker:
      replicas: 3
    PS:
      replicas: 2
```

## Best Practices

### 1. Resource Management e GPU Scheduling
```yaml
spec:
  nodeSelector:
    accelerator: nvidia-tesla-v100
  tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
```

### 2. Network Optimization for NCCL
```yaml
env:
- name: NCCL_DEBUG
  value: "INFO"
- name: NCCL_SOCKET_IFNAME
  value: "eth0"
- name: NCCL_IB_DISABLE
  value: "0"
- name: NCCL_NET_GDR_LEVEL
  value: "5"
- name: NCCL_P2P_DISABLE
  value: "0"
```

### 3. Persistent Storage
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: training-data-pvc
spec:
  accessModes:
  - ReadWriteMany
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 500Gi
```

### 4. Monitoring
```bash
# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring

# ServiceMonitor
kubectl apply -f servicemonitor.yaml
```

### 5. Fault Tolerance e Checkpointing
```python
def save_checkpoint(model, optimizer, epoch, loss, checkpoint_dir):
    if dist.get_rank() == 0:
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.module.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
        }
        torch.save(checkpoint, f'{checkpoint_dir}/checkpoint_epoch_{epoch}.pt')

def load_checkpoint(model, optimizer, checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.module.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    return checkpoint['epoch'], checkpoint['loss']
```

## Troubleshooting

### NCCL Timeout Errors
```yaml
env:
- name: NCCL_TIMEOUT
  value: "7200"
- name: NCCL_BLOCKING_WAIT
  value: "1"
```

### OOM Errors
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
accumulation_steps = 4

for batch_idx, (data, target) in enumerate(train_loader):
    with autocast():
        output = model(data)
        loss = criterion(output, target) / accumulation_steps
    
    scaler.scale(loss).backward()
    
    if (batch_idx + 1) % accumulation_steps == 0:
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

### Pod Scheduling Issues
```bash
# Check GPU availability
kubectl describe nodes | grep -A 5 "Allocated resources"

# Verify GPU device plugin
kubectl get daemonset -n kube-system | grep nvidia

# Check node labels
kubectl get nodes --show-labels | grep gpu
```

## Performance Optimization

### Data Loading
```python
train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    sampler=train_sampler,
    num_workers=8,          # Increase for better I/O
    pin_memory=True,        # Faster GPU transfer
    persistent_workers=True, # Reuse workers
    prefetch_factor=2       # Prefetch batches
)
```

### Gradient Compression (Horovod)
```bash
# Install Horovod with NCCL
pip install horovod[pytorch]

# Run with compression
horovodrun -np 4 --compression fp16 python train.py
```

## Key Takeaways

1. **Training Operator** é padrão para distributed training em K8s
2. **NCCL** é crítico para multi-GPU performance
3. **Checkpointing** é essencial para fault tolerance
4. **Monitoring** (Prometheus/Grafana) obrigatório para production
5. **Mixed precision** economiza memória e acelera training
6. **Data loading** otimizado é crucial para GPU utilization

## Insights

- PyTorchJob/TFJob abstraem complexidade de distributed training
- NCCL configuration tem grande impacto em performance
- Fault tolerance requer checkpointing robusto
- Storage rápido (SSD, NVMe) é critical para data loading
- Pod anti-affinity melhora resiliência
- Mixed precision + gradient accumulation resolvem OOM