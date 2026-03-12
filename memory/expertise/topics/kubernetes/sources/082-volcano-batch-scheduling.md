# Volcano - High-Performance Batch Scheduling

**Fonte:** https://volcano.sh/en/docs/
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

Volcano é sistema cloud-native para workloads de alta performance. Primeiro projeto oficial de CNCF para container batch scheduling. Suporta Spark, TensorFlow, PyTorch, Flink, Ray e mais.

---

## O que é Volcano

CNCF's primeiro e único projeto oficial de container batch scheduling.

### Frameworks Suportados
| Framework | Status |
|-----------|--------|
| Spark | ✅ |
| TensorFlow | ✅ |
| PyTorch | ✅ |
| Flink | ✅ |
| Argo | ✅ |
| MindSpore | ✅ |
| PaddlePaddle | ✅ |
| Ray | ✅ |

### Scheduling Capabilities
- Heterogeneous device scheduling
- Network topology-aware scheduling
- Multi-cluster scheduling
- Online-offline colocation

---

## Por que Volcano

### Requisitos Comuns
1. Suporte para diversos scheduling algorithms
2. Scheduling mais eficiente
3. Suporte não-intrusivo para frameworks mainstream
4. Suporte para multi-architecture computing

### Design Philosophy
Herda design de Kubernetes APIs, permitindo rodar facilmente aplicações de high-performance computing em Kubernetes.

---

## Features

### 1. Unified Scheduling
- Support native Kubernetes workload scheduling
- Complete support para PyTorch, TensorFlow, Spark, Flink, Ray via VolcanoJob
- Unified scheduling para online microservices + offline batch jobs

### 2. Rich Scheduling Policies

| Policy | Description |
|--------|-------------|
| **Gang Scheduling** | All tasks start simultaneously |
| **Binpack Scheduling** | Compact allocation, optimize utilization |
| **Heterogeneous Device** | GPU sharing, CUDA, MIG modes, NPU |
| **Proportion/Capacity** | Quota-based sharing, preemption, reclaim |
| **NodeGroup Scheduling** | Queue-node group binding |
| **DRF Scheduling** | Fair scheduling multi-dimensional |
| **SLA Scheduling** | Quality of service guarantee |
| **Task-topology** | Topology-aware for communication-intensive |
| **NUMA Aware** | Optimize for multi-core processors |

### 3. Queue Resource Management
- Multi-dimensional resource quota (CPU, Memory, GPU)
- Multi-level queue structure
- Resource borrowing, reclaiming, preemption
- Multi-tenant isolation

### 4. Multi-Architecture Computing
| Architecture | Support |
|--------------|---------|
| x86 | ✅ |
| Arm | ✅ |
| Kunpeng | ✅ |
| Ascend | ✅ |

### 5. GPU Virtualization
| Technology | Description |
|------------|-------------|
| **Dynamic MIG** | Dynamic partitioning of NVIDIA MIG |
| **vCUDA** | Software-level GPU virtualization |
| **Fine-Grained Control** | Dedicated memory/compute per instance |
| **Multi-Container Sharing** | Multiple containers share single GPU |
| **Unified Monitoring** | Metrics for all GPU instances |

### 6. Network Topology-Aware Scheduling
- Considera network bandwidth entre nodes
- Otimiza data transmission para distributed training
- Reduz communication overhead

### 7. Online-Offline Colocation
- Enhance resource utilization
- QoS guarantee para online workloads
- Dynamic resource overcommitment
- CPU burst, resource isolation

### 8. Multi-Cluster Scheduling
- Cross-cluster job scheduling
- Larger-scale resource pool management
- Load balancing

### 9. Descheduling
- Dynamic descheduling
- Optimize cluster load distribution
- Improve stability

### 10. Monitoring & Observability
- Complete logging system
- Rich monitoring metrics
- Dashboard UI

---

## Ecosystem

Volcano é de facto standard para batch computing:

### Supported Frameworks
- Spark, TensorFlow, PyTorch
- Flink, Argo, Ray
- MindSpore, PaddlePaddle
- OpenMPI, Horovod, MXNet
- Kubeflow, KubeGene, Cromwell

### Industry Adoption
AI e Big Data em:
- Distributed training
- Data analysis tasks
- Resource utilization systems

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              Volcano Scheduler                      │
│  ┌─────────────────────────────────────────────┐  │
│  │           Scheduling Actions                  │  │
│  │  Enqueue → Allocate → Backfill → Preempt    │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐  │
│  │           Scheduling Plugins                │  │
│  │  Gang | DRF | Binpack | Proportion | SLA   │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                     │
│  ┌──────────────┐  ┌──────────────┐              │
│  │  Queue A     │  │  Queue B     │              │
│  │  (Team 1)    │  │  (Team 2)    │              │
│  └──────────────┘  └──────────────┘              │
│  ┌──────────────────────────────────────────┐    │
│  │           VolcanoJobs                     │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐       │    │
│  │  │ Job 1  │ │ Job 2  │ │ Job 3  │       │    │
│  │  │(Gang)  │ │(Spark) │ │(PyTorch)│      │    │
│  │  └────────┘ └────────┘ └────────┘       │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## Gang Scheduling

Conceito central do Volcano:

```yaml
apiVersion: batch.volcano.sh/v1alpha1
kind: Job
metadata:
  name: tensorflow-job
spec:
  minAvailable: 3  # All 3 pods must be ready
  tasks:
  - replicas: 3
    name: worker
    template:
      spec:
        containers:
        - name: tensorflow
          image: tensorflow/tensorflow:latest
```

**Benefício:** Distributed training funciona apenas quando todas tasks estão rodando simultaneamente.

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Gang Scheduling | All tasks start simultaneously |
| Binpack | Compact allocation |
| DRF | Dominant Resource Fairness |
| vCUDA | GPU virtualization at software level |
| MIG | Multi-Instance GPU partitioning |
| Topology-Aware | Optimize for network/data center topology |
| NUMA Aware | Optimize for multi-core memory access |

---

## Referências

- Volcano GitHub: https://github.com/volcano-sh/volcano
- Volcano Dashboard: https://github.com/volcano-sh/dashboard
- Volcano Global: https://github.com/volcano-sh/volcano-global
- GPU Virtualization: https://volcano.sh/en/docs/gpu_virtualization/