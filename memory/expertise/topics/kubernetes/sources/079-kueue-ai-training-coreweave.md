# Kueue: Kubernetes-Native AI Workload Scheduling

**Fonte:** CoreWeave Blog - https://www.coreweave.com/blog/kueue-a-kubernetes-native-system-for-ai-training-workloads
**Data:** 2024-2025
**Tópico:** Kueue, Batch Scheduling, Gang Scheduling, Resource Management
**Status:** Lido

---

## Resumo Executivo

Kueue é um sistema open-source para Kubernetes que adiciona capacidades de job queueing essenciais para workloads de AI/ML, incluindo scheduling "all-or-nothing" e gestão de quotas multi-tenant.

---

## O Problema do Kubernetes Tradicional

### Workloads Tradicionais vs AI/ML
| Aspecto | Tradicional | AI/ML |
|---------|-------------|-------|
| **State** | Stateless, ephemeral | Stateful, long-running |
| **Scaling** | Auto-scaling nodes | Fixed/reserved GPU capacity |
| **Scheduling** | Pods individuais | "All-at-once" requirement |
| **Elasticidade** | Alta | Baixa (GPU capacity limitada) |

### Desafios de AI Workloads
1. **GPU nodes são inelásticos**: Capacidade limitada, mesmo em cloud
2. **Compute mínimo na inicialização**: Não podem começar com pods parciais
3. **All-at-once semantics**: Todos pods precisam rodar simultaneamente

---

## O que é Kueue

### Definição
- **Open-source project**: Adiciona job queueing ao Kubernetes
- **CNCF**: Parte do ecossistema Kubernetes
- **Foco**: Batch AI/ML workloads

### Conceitos Principais

#### 1. All-or-Nothing Scheduling
- Jobs permanecem em queue até compute suficiente
- Gang scheduling: todos pods iniciam simultaneamente
- Evita scheduling parcial que desperdiça recursos

#### 2. ResourceFlavor
- Formalização de tipos de hardware
- Exemplo: CPU nodes, GPU nodes, GPUs com InfiniBand
- Substitui taints/tolerations complexos

#### 3. ClusterQueue e LocalQueue
- **ClusterQueue**: Quota global, cluster-wide
- **LocalQueue**: Queue por namespace/time
- Permite gestão multi-tenant

---

## Arquitetura Kueue

```
┌─────────────────────────────────────────────────┐
│            Kueue Components                     │
│  ┌───────────────┐ ┌───────────────┐           │
│  │ ClusterQueue  │ │ LocalQueue    │           │
│  │ (Quota)       │ │ (Per-team)    │           │
│  └───────────────┘ └───────────────┘           │
│  ┌───────────────┐ ┌───────────────┐           │
│  │ ResourceFlavor│ │ Workload      │           │
│  │ (Hardware)    │ │ (Job)         │           │
│  └───────────────┘ └───────────────┘           │
├─────────────────────────────────────────────────┤
│            Kubernetes Integration               │
│  ┌───────────────┐ ┌───────────────┐           │
│  │ Job CRDs      │ │ Scheduler     │           │
│  │ (PyTorchJob)  │ │ Integration   │           │
│  └───────────────┘ └───────────────┘           │
├─────────────────────────────────────────────────┤
│            CoreWeave CKS                        │
│  (Managed Kubernetes with GPU nodes)           │
└─────────────────────────────────────────────────┘
```

---

## Benefícios do Kueue

### 1. All-or-Nothing Scheduling
- Jobs só iniciam quando há recursos para todos pods
- Evita deadlocks e desperdício de GPU
- Gang scheduling nativo

### 2. ResourceFlavor
- Formaliza tipos de hardware
- Exemplos:
  - `cpu-flavor`: CPU-only nodes
  - `gpu-flavor`: GPU nodes
  - `gpu-ib-flavor`: GPU + InfiniBand

### 3. Multi-Tenant Resource Sharing
- ClusterQueue: Quota por time
- ResourceFlavor: Tipos de hardware
- Preemption: Workloads de alta prioridade podem preemptar
- Quota borrowing: Times podem emprestar recursos não usados

### Exemplo de Quota
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: research-team
spec:
  namespaceSelector:
    matchLabels:
      team: research
  resources:
  - name: nvidia.com/gpu
    flavors:
    - name: gpu-ib-flavor
      quota:
        min: 8
        max: 16
```

---

## Kueue vs Kubernetes Scheduler Nativo

| Feature | K8s Scheduler | Kueue |
|---------|---------------|-------|
| **Scheduling** | Pod-by-pod | Workload-level |
| **All-or-nothing** | Não | Sim |
| **Resource Flavors** | Labels/taints | ResourceFlavor CRD |
| **Quota Management** | ResourceQuota | ClusterQueue |
| **Preemption** | PriorityClass | Workload-level |
| **Borrowing** | Não | Sim |

---

## Casos de Uso

### 1. ML Training
- PyTorchJob, TFJob
- Distributed training
- All workers need to start together

### 2. Batch Inference
- Batch processing
- Queue until resources available

### 3. Multi-Team Clusters
- Research team: InfiniBand GPUs
- Production team: Standard GPUs
- Fair sharing via quotas

---

## Integração com CKS (CoreWeave Kubernetes Service)

### Features
- Helm Chart para instalação
- Prometheus metrics integrados
- Grafana dashboard customizado
- Documentação completa

### Monitoring
- Kueue emite métricas Prometheus
- Dashboards para troubleshooting
- Métricas de queue depth, admission, preemption

---

## Exemplos de Configuração

### LocalQueue
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: training-queue
  namespace: ml-team
spec:
  clusterQueue: research-team
```

### Workload
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  name: training-workload
spec:
  queueName: training-queue
  podSets:
  - name: workers
    count: 4
    template:
      spec:
        containers:
        - name: pytorch
          image: pytorch/pytorch:latest
          resources:
            requests:
              nvidia.com/gpu: 1
```

---

## Preemption e Borrowing

### Preemption
- Workloads de alta prioridade podem preemptar lower priority
- Todos pods do workload são evicted juntos (all-or-nothing)
- Mantém semântica de scheduling correto

### Borrowing
- Times podem usar recursos não utilizados de outras queues
- Recursos retornam ao owner quando requisitados
- Maximiza utilização do cluster

---

## Insights para Kubernetes

1. **Kueue é essencial para AI/ML**: Scheduler nativo não foi feito para batch jobs
2. **ResourceFlavor simplifica**: Substitui complexidade de taints/tolerations
3. **Quota borrowing é poderoso**: Maximiza utilização sem desperdício
4. **All-or-nothing é crítico**: Jobs parcialmente scheduleados = deadlock
5. **Integração CNCF**: Ecossistema crescente, bem mantido

---

## Palavras-Chave
`kueue` `batch-scheduling` `gang-scheduling` `resource-management` `ai-workloads` `multi-tenancy` `kubernetes`