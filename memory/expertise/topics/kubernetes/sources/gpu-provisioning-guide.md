# GPU Provisioning and Management in Kubernetes: Ultimate Guide

**Fonte:** https://sealos.io/blog/the-ultimate-guide-to-gpu-provisioning-and-management-in-kubernetes/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Guia completo sobre provisionamento e gerenciamento de GPUs em Kubernetes, cobrindo desde setup básico até operações avançadas como MIG e time-slicing.

## Conceitos Fundamentais

### GPUs como Extended Resources
- **Extended resources**: Dispositivos expostos via device plugin (nvidia.com/gpu)
- **Device plugin**: DaemonSet que anuncia dispositivos ao kubelet
- **Runtime support**: NVIDIA Container Toolkit necessário
- **Drivers**: Driver NVIDIA no node; CUDA libraries no container

### Por que Kubernetes para GPU?
- **Unified Platform**: Training, inference, ETL, batch em uma plataforma
- **Automation**: Autoscaling, rolling upgrades, job queues
- **Cost Efficiency**: Bin-packing, time-slicing, MIG, quotas
- **Multi-tenancy**: Namespaces, quotas, policies
- **Portability**: Hybrid e multi-cloud

## Setup e Configuração

### NVIDIA Device Plugin
```yaml
# Pod com GPU request
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: gpu-container
    image: nvidia/cuda:12.0-base
    resources:
      limits:
        nvidia.com/gpu: 1
  runtimeClassName: nvidia
```

### NVIDIA GPU Operator
- Gerencia: drivers, container toolkit, device plugin, DCGM
- Instalação via Helm:
```bash
helm install gpu-operator nvidia/gpu-operator -n gpu-operator
```

### Node Requirements
1. NVIDIA driver instalado
2. Container runtime com NVIDIA support
3. Kubernetes version compatível
4. GPU Operator recomendado

## Scheduling e Isolamento

### Taints e Tolerations
```bash
# Taint GPU nodes
kubectl taint nodes gpu=true:NoSchedule
```
```yaml
# Pod com toleration
spec:
  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"
```

### Node Affinity
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nvidia.com/gpu.product
            operator: In
            values: ["A100"]
```

### Resource-Aware Scheduling
- **PriorityClasses**: Pods críticos preempt jobs de baixa prioridade
- **Topology Manager**: Alinha CPU, memory, devices em NUMA node
- **Gang Scheduling**: Kueue ou Volcano para jobs multi-GPU

## GPU Sharing Strategies

### 1. Time-Slicing (Soft Sharing)
```yaml
# ConfigMap para time-slicing
apiVersion: v1
kind: ConfigMap
data:
  config.yaml: |
    version: v1
    flags:
      migStrategy: none
    sharing:
      timeSlices:
        renameByDefault: false
        resources:
        - name: nvidia.com/gpu
          replicas: 4
```
- **Pros**: Simples, bom para inference leve
- **Cons**: Performance não isolada

### 2. MIG (Multi-Instance GPU)
```yaml
# MIG profile
resources:
  limits:
    nvidia.com/mig-1g.10gb: 1
```
- **Pros**: Isolamento forte, performance previsível
- **Cons**: Particionamento estático

### 3. MPS e vGPU
- **MPS**: Melhora throughput para jobs pequenos (não é isolamento estrito)
- **vGPU**: Virtualização para ambientes especializados

## Multi-Tenancy

### Resource Quotas
```yaml
apiVersion: v1
kind: ResourceQuota
spec:
  hard:
    limits.nvidia.com/gpu: "10"
    requests.nvidia.com/gpu: "10"
```

### PriorityClasses
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
preemptionPolicy: PreemptLowerPriority
```

## Autoscaling

### Cluster Autoscaler
- Node pool dedicado para GPUs
- Scale-up policies configurados
- Taints para não-trigger de scale-up não-GPU

### HPA com GPU Metrics
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  metrics:
  - type: Pods
    pods:
      metric:
        name: dcgm_gpu_utilization
      target:
        type: AverageValue
        averageValue: "80"
```

## Monitoring

### DCGM Exporter
- Métricas: utilization, memory, temperature, power
- Integração: Prometheus + Grafana

### PromQL Examples
```promql
# GPU utilization per pod
avg by (pod) (dcgm_gpu_utilization)

# Memory usage
dcgm_fb_used_bytes / dcgm_fb_total_bytes

# Power draw
avg by (instance) (dcgm_power_usage_watts)
```

## Storage e I/O

- **Fast storage**: NVMe local SSDs
- **Caching**: Alluxio, object store caching
- **GPUDirect Storage (GDS)**: Bypass CPU para I/O

## Best Practices

### Runtime
- Usar RuntimeClass NVIDIA
- Evitar privileged containers
- Evitar hostPath para /dev/nvidia*

### Security
- Pod Security Admission (baseline/restricted)
- NetworkPolicies para isolamento
- Secrets para credentials
- Egress governance para compliance

### Performance Tuning
1. **Topology Manager**: `topologyManagerPolicy=single-numa-node`
2. **CPU Manager**: `static` policy para CPU pinning
3. **MIG** para isolamento multi-tenant
4. **MPS** para throughput optimization
5. **Model Serving**: Triton, TensorRT

## Common Pitfalls

1. **CUDA/driver mismatch**: Verificar compatibilidade
2. **Missing runtimeClassName**: Pods não veem GPUs
3. **Overcommitting sem planejamento**: Latência imprevisível
4. **Ignorando topology/NUMA**: Jitter e performance issues
5. **Single-tenancy mindset**: Sem quotas = starvation

## Insights

- GPUs são recursos caros que requerem gerenciamento cuidadoso
- Time-slicing para workloads leves, MIG para isolamento forte
- Monitoring é crítico (DCGM + Prometheus)
- Multi-tenancy requer quotas, priority classes, e policies
- Platforms como Sealos simplificam setup e gestão