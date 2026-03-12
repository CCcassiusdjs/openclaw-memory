# The Ultimate Guide to GPU Provisioning and Management in Kubernetes

**Fonte:** Sealos Blog - https://sealos.io/blog/the-ultimate-guide-to-gpu-provisioning-and-management-in-kubernetes/
**Data:** Setembro 2025
**Tópico:** GPU Provisioning, NVIDIA GPU Operator, MIG, Time-Slicing, Multi-tenancy
**Status:** Lido

---

## Resumo Executivo

Guia completo para provisionamento e gestão de GPUs em Kubernetes, cobrindo arquitetura, device plugins, MIG, time-slicing, scheduling avançado, monitoramento, e melhores práticas operacionais.

---

## Por que Kubernetes para GPUs

### Benefícios
| Benefício | Descrição |
|-----------|-----------|
| **Unified Platform** | Treinamento, inference, ETL, batch em um platform |
| **Automation** | Autoscaling, rolling upgrades, job queues, CI/CD |
| **Cost Efficiency** | Bin-packing, sharing, quotas |
| **Multi-tenancy** | Namespaces, quotas, policies |
| **Portability** | Hybrid, multi-cloud |

### Conceitos-Chave
- **Extended resources**: GPUs expostos via device plugin (`nvidia.com/gpu`)
- **Device plugin**: DaemonSet que anuncia dispositivos ao kubelet
- **Runtime support**: NVIDIA Container Toolkit necessário
- **Drivers/libraries**: Driver no node, CUDA libraries no container

---

## NVIDIA Device Plugin

### Arquitetura
```
Kubelet ──> Device Plugin ──> NVIDIA Driver ──> GPU
   │            │
   └────────────┴──> nvidia.com/gpu resource
```

### Funções
- Roda como DaemonSet
- Registra GPUs como extended resources
- Pods requisitam via `limits.nvidia.com/gpu`
- Scheduler seleciona nodes com GPUs disponíveis

### Comportamento Importante
- Limits para `nvidia.com/gpu` são obrigatórios
- Requests devem igualar limits (se especificados)
- GPU é exclusiva por container (sem MIG/time-slicing)

---

## NVIDIA GPU Operator

### O que Gerencia
- NVIDIA drivers
- Container Toolkit
- Device Plugin
- DCGM e DCGM Exporter (monitoramento)
- Node Feature Discovery (opcional)

### Instalação via Helm
```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm install gpu-operator nvidia/gpu-operator \
  --namespace gpu-operator \
  --create-namespace
```

### Verificação
```bash
# Pods do GPU Operator
kubectl get pods -n gpu-operator

# DaemonSets
# - nvidia-device-plugin
# - nvidia-driver-daemonset
# - dcgm-exporter

# Verificar resources no node
kubectl describe node | grep -i nvidia
```

---

## GPU Sharing Strategies

### 1. Time-Slicing (Soft Sharing)
- Múltiplos pods compartilham GPU
- Performance não isolada
- Bom para: inference leve, bursty workloads

**ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
data:
  any: |-
    version: v1
    sharing:
      timeSlicing:
        renameByDefault: false
        resources:
        - name: nvidia.com/gpu
          replicas: 4  # 4 pods por GPU
```

### 2. MIG (Multi-Instance GPU)
- Partições isoladas com memoria e compute dedicados
- Isolamento forte de performance
- Requer GPUs: A100, H100
- Reconfiguração requer draining

**Exemplo A100:**
```bash
# 7 x 1g.5gb instances
sudo nvidia-smi mig -i 0 -cgi 19,19,19,19,19,19,19 -C

# Ou 2 x 3g.20gb + 1 x 1g.5gb
sudo nvidia-smi mig -i 0 -cgi 9,9,19 -C
```

**Pod com MIG:**
```yaml
resources:
  limits:
    nvidia.com/mig-1g.5gb: 1
```

### 3. MPS (Multi-Process Service)
- Melhora throughput para CUDA workloads
- Sem isolamento estrito de performance
- Bom para muitos jobs pequenos

---

## Scheduling Avançado

### Taints e Tolerations
```bash
# Taint GPU nodes (apenas pods GPU)
kubectl taint nodes gpu-node-1 nvidia.com/gpu=true:NoSchedule
```

```yaml
# Pod com toleration
tolerations:
- key: nvidia.com/gpu
  operator: Exists
  effect: NoSchedule
```

### Node Affinity
```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: nvidia.com/gpu.memory
          operator: Gt
          values: ["16000"]  # >16GB VRAM
```

### Topology Manager
- Alinha CPU, memory, device dentro de NUMA node
- Configuração no kubelet:
```bash
topologyManagerPolicy: single-numa-node
```

### Gang Scheduling
- Para distributed training
- Usa Kueue ou Volcano
- Todos pods iniciam juntos

---

## Multi-Tenancy

### Resource Quotas
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: team-a
spec:
  hard:
    limits.nvidia.com/gpu: "10"
    requests.nvidia.com/gpu: "10"
```

### Priority Classes
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
```

---

## Autoscaling

### Cluster Autoscaler
- Node pool dedicado para GPUs
- Scale-up policies para GPU pool
- Taints para que apenas GPU workloads trigger scale-up

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
        type: Utilization
        averageUtilization: 70
```

---

## Monitoramento

### DCGM Exporter
- Expõe métricas de GPU
- Integrado com Prometheus
- Métricas: utilization, memory, temperature, power

### PromQL Exemplos
```promql
# GPU utilization por pod
avg by (pod) (dcgm_gpu_utilization)

# Memory usage por GPU
dcgm_fb_used_bytes / dcgm_fb_total_bytes

# Power draw por node
avg by (instance) (dcgm_power_usage_watts)
```

### Alertas
- High memory usage (>90%)
- High temperature (>85°C)
- XID errors (hardware issues)

---

## Storage e I/O

### Best Practices
- **NVMe local SSDs**: Scratch space rápido
- **High-performance network**: Para datasets grandes
- **Data caching**: Alluxio ou object store caching
- **GPUDirect Storage (GDS)**: Bypass CPU para I/O

### PVCs para Modelos
```yaml
volumes:
- name: models
  persistentVolumeClaim:
    claimName: model-storage
    readOnly: true
```

---

## Operações

### Upgrades de Driver
- GPU Operator pode orquestrar upgrades
- Usar node draining e PDBs
- Validar compatibilidade CUDA/runtime

### Node Maintenance
```bash
kubectl drain --ignore-daemonsets --delete-emptydir-data
```

### Performance Tuning Checklist
- `topologyManagerPolicy=single-numa-node`
- `cpuManagerPolicy=static` para CPU pinning
- MIG para isolamento em inference
- MPS para throughput optimization
- Triton para serving multi-framework

---

## Casos de Uso

### Batch Training (uso sustentado)
- MIG ou GPUs dedicadas
- Performance previsível

### Online Inference (requests espiky)
- Time-slicing ou MPS
- Multiplexação alta

### Multi-tenant Platform (isolamento/SLA)
- MIG profiles + quotas por namespace
- PriorityClasses para workloads críticos

### Cost-sensitive Experimentation
- Time-slicing com quotas
- GPU node pools elásticos

---

## Problemas Comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| CUDA/driver mismatch | Versão incompatível | Verificar compatibilidade |
| Sem GPU visível | Falta runtimeClassName | Usar GPU Operator |
| Overcommit sem plano | Time-slicing sem SLO | HPA + alerts |
| Ignorando NUMA | Topology manager desabilitado | Habilitar single-numa-node |
| Single-tenancy mindset | Sem quotas | Implementar quotas + priority |

---

## Insights para Kubernetes

1. **GPU Operator simplifica**: Gerencia drivers, toolkit, device plugin
2. **Sharing é essencial**: Time-slicing e MIG para eficiência
3. **Topology matters**: NUMA alignment para latência
4. **Multi-tenancy requer planning**: Quotas, priority, taints
5. **Monitoramento é crítico**: DCGM + Prometheus + Grafana

---

## Palavras-Chave
`gpu-provisioning` `nvidia-gpu-operator` `mig` `time-slicing` `multi-tenancy` `gpu-monitoring` `kubernetes`