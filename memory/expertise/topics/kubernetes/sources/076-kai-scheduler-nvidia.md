# KAI Scheduler - GPU Scheduling for AI Workloads

**Fonte:** NVIDIA/GitHub - https://github.com/NVIDIA/KAI-Scheduler
**Data:** 2024-2025
**Tópico:** Kubernetes Scheduler, GPU Scheduling, AI Workloads, Batch Scheduling
**Status:** Lido

---

## Resumo Executivo

KAI Scheduler é um scheduler Kubernetes open-source otimizado para workloads de AI/ML, oferecendo gang scheduling, GPU sharing, topology-aware scheduling, e fair share para clusters de larga escala.

---

## O que é KAI Scheduler

### Definição
- **Kubernetes Native Scheduler**: Otimizado para GPU allocation
- **Escalabilidade**: Milhares de nodes, alto throughput
- **AI Lifecycle**: Do small interactive jobs a large training/inference

### Propósito
- Gerenciar clusters GPU de larga escala
- Alocação dinâmica de recursos GPU
- Fairness entre consumidores diferentes
- Coexistência com outros schedulers

---

## Features Principais

### Batch Scheduling (Gang Scheduling)
- Todos pods de um grupo são schedulados simultaneamente
- **All-or-nothing**: Se não há recursos para todos, nenhum é iniciado
- Ideal para distributed training

### Bin Packing & Spread Scheduling
- **Bin Packing**: Minimiza fragmentação
- **Spread**: Aumenta resiliência, distribui pods

### Workload Priority
- Priorização efetiva dentro de queues
- Separação de priority e preemptibility

### Hierarchical Queues
- Duas levels de hierarchy
- Controle organizacional flexível
- Quotas, over-quota weights, limits

### Resource Distribution
- **Dominant Resource Fairness (DRF)**: Fair share
- Resource reclamation entre queues
- Customização de quotas e limits

### Time-based Fairshare
- Uso justo ao longo do tempo
- Considera historical usage
- Time decay parameters

### Min-guaranteed-runtime
- Período sem preemption
- Workloads preemptíveis protegidos temporariamente

### Workload Consolidation
- Realocação inteligente de workloads running
- Reduz fragmentação
- Aumenta utilização do cluster

### Elastic Workloads
- Escala dinâmica dentro de min/max pods
- Adaptativo a recursos disponíveis

### Dynamic Resource Allocation (DRA)
- Vendor-specific hardware resources
- Kubernetes ResourceClaims
- Suporte a GPUs NVIDIA/AMD

### Topology-Aware Scheduling (TAS)
- Otimiza placement para arquiteturas modernas
- Scheduling hierárquico para PodGroups
- Ideal para distributed/disaggregated workloads

### Hierarchical PodGroups
- Gang scheduling otimizado
- Multi-level workloads (Dynamo/Grove)

---

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│              KAI Scheduler                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │ Queue       │ │ Workload    │ │ Preemption  │   │
│  │ Manager     │ │ Scheduler   │ │ Manager     │   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │ GPU Sharing │ │ TAS         │ │ Fairshare   │   │
│  │ Manager     │ │ Engine      │ │ Calculator  │   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
├─────────────────────────────────────────────────────┤
│              Kubernetes API Server                  │
├─────────────────────────────────────────────────────┤
│              GPU Operator (NVIDIA)                  │
├─────────────────────────────────────────────────────┤
│              Nodes with GPUs                        │
└─────────────────────────────────────────────────────┘
```

---

## Instalação

### Pré-requisitos
- Kubernetes cluster rodando
- Helm CLI instalado
- NVIDIA GPU-Operator instalado (para GPU workloads)

### Instalação via Helm

```bash
# Instalar versão específica
helm upgrade -i kai-scheduler \
  oci://ghcr.io/kai-scheduler/kai-scheduler/kai-scheduler \
  -n kai-scheduler \
  --create-namespace \
  --version <VERSION>
```

### GPU Operator < v25.10.0

```bash
# Flag adicional necessária
--set admission.gpuPodRuntimeClassName=null

# Se CDI enabled
--set binder.cdiEnabled=true
```

---

## Integrações

### KubeRay Integration
- Native scheduling para Ray workloads
- Documentação: docs.ray.io

### Grove & Dynamo
- Topology-aware scheduling
- Hierarchical PodGroups
- Disaggregated serving

---

## Casos de Uso

### 1. Large-Scale Training
- Distributed training jobs
- Multi-node, multi-GPU
- Gang scheduling necessário

### 2. Inference Serving
- Real-time inference
- Autoscaling baseado em demanda
- GPU sharing para efficiency

### 3. Interactive Development
- Notebooks em cluster
- Small jobs, recursos mínimos
- Fair share entre usuários

### 4. Batch Processing
- Data preprocessing
- Feature engineering
- Scheduled jobs

---

## Exemplos de Configuração

### Queue Hierarchy
```yaml
apiVersion: kai.scheduler/v1
kind: Queue
metadata:
  name: team-a
spec:
  resources:
    cpu: 100
    memory: 200Gi
    nvidia.com/gpu: 10
  children:
    - team-a-research
    - team-a-production
```

### Workload Submission
```yaml
apiVersion: kai.scheduler/v1
kind: Workload
metadata:
  name: training-job
spec:
  queue: team-a-research
  priority: high
  podGroups:
    - name: workers
      count: 8
      podSpec:
        containers:
        - name: trainer
          image: pytorch/pytorch:latest
          resources:
            limits:
              nvidia.com/gpu: 4
```

---

## Roadmap Recente

### v0.10.0 (Outubro 2025)
- Topology-Aware Scheduling (TAS)
- Hierarchical PodGroups
- Time-based Fairshare

### Integrações
- KubeRay (Agosto 2025)
- Grove & Dynamo (Novembro 2025)

---

## Insights para Kubernetes

1. **GPU scheduling é complexo**: Precisa de scheduler especializado
2. **Gang scheduling**: Crítico para distributed training
3. **Fair share**: Essencial em clusters multi-tenant
4. **Topology matters**: Para performance GPU (NVLink, PCIe)
5. **Open-source e ativo**: Desenvolvimento contínuo pela NVIDIA

---

## Palavras-Chave
`kai-scheduler` `gpu-scheduling` `kubernetes` `ai-workloads` `gang-scheduling` `fairshare` `topology-aware` `nvidia`