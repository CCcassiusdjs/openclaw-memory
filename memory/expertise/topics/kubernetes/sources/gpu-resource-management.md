# Kubernetes GPU Resource Management: Best Practices

**Fonte:** https://www.perfectscale.io/blog/kubernetes-gpu  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

GPUs em Kubernetes são recursos caros e escassos. Gerenciamento eficiente é crítico para evitar desperdício e maximizar ROI.

## 8 Best Practices para GPU Management

### 1. Node Labels para GPU Types
```bash
# Label manual
kubectl label nodes node1 accelerator=nvidia-v100
kubectl label nodes node2 accelerator=intel-flex

# Node Feature Discovery (NFD) para auto-labeling
kubectl apply -k 'https://github.com/intel/intel-device-plugins-for-kubernetes/deployments/nfd'
```

**Por que**: Clusters podem ter diferentes GPUs (A100, V100, Intel Flex). Labels ajudam scheduler a colocar workloads nos nodes certos.

### 2. Resource Limits para GPU
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-enabled-pod
spec:
  containers:
  - name: gpu-container
    image: gpu-enabled-image:v1
    resources:
      limits:
        nvidia.com/gpu: 1  # Apenas em limits!
```

**Importante**: GPUs são definidas APENAS em limits, não requests. Cada pod tem GPU dedicado.

### 3. Fractional Resource Management
```yaml
# Intel GPU Plugin - fractional usage
-resource-manager enabled
-shared-dev-num 2  # 2 containers compartilham 1 GPU
```

**Benefícios**: Time-slicing, MIG permitem compartilhar GPU entre workloads leves (inference, transcoding).

### 4. Node Affinity para GPU Scheduling
```yaml
apiVersion: v1
kind: Pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: "gpu.vendor.example/installed-memory"
            operator: Gt
            values: ["40960"]  # GPU com >40GB memória
```

**Uso**: Workloads específicos em GPUs específicas (high-end vs economy).

### 5. Scheduling Strategies por Workload
- **Time-sensitive jobs**: Node selectors para high-end GPU nodes
- **Non-critical jobs**: GPUs antigas ou menos potentes
- **Batch jobs**: Gang scheduling (Kueue, Volcano) para distributed training

### 6. GPU Health Monitoring
- NVIDIA DCGM para métricas (temperatura, memória, utilization)
- Intel Level Zero API
- Alerts para issues antes que impactem aplicações

### 7. RBAC para GPU Access
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ml-project
  name: gpu-access-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create", "get", "list", "watch", "delete"]
```

**Objetivo**: Restringir GPU access a users/workloads autorizados.

### 8. Dynamic Resource Allocation (DRA) - Future
- NVIDIA DRA driver permite alocação dinâmica baseada em demanda
- Status: **Beta** (não production-ready ainda)

## Ferramentas

- **NVIDIA Device Plugin**: `nvidia.com/gpu` resource
- **Node Feature Discovery (NFD)**: Auto-labeling de hardware
- **DCGM**: Monitoring e health
- **Time-slicing**: GPU sharing para workloads leves
- **MIG (Multi-Instance GPU)**: Particionamento físico de GPU

## Custos e Eficiência

- GPUs podem representar até **75% dos custos cloud** em ambientes AI
- Idle GPUs = desperdício de dinheiro
- Overloaded GPUs = performance degradation

## Insights

- GPU management em Kubernetes requer planejamento cuidadoso
- Labels + affinity são fundamentais para scheduling correto
- Fractional resources permitem melhor utilização
- Health monitoring é crítico para production
- DRA é o futuro mas ainda em desenvolvimento