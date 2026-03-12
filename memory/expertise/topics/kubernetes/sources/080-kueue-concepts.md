# Kueue Core Concepts

**Fonte:** https://kueue.sigs.k8s.io/docs/concepts/
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

Documentação oficial dos conceitos core do Kueue: APIs, glossário e abstrações para gerenciamento de quotas e workloads.

---

## APIs Principais

### ResourceFlavor
Objeto que define recursos disponíveis no cluster. Tipicamente associado a características de um grupo de Nodes.

**Características:**
- Availability
- Pricing
- Architecture
- Models (GPU types)

### ClusterQueue
Cluster-scoped resource que governa um pool de recursos.

**Define:**
- Usage limits
- Fair Sharing rules
- Quota management

### LocalQueue
Namespace-scoped resource que agrupa workloads relacionados de um único tenant.

### Workload
Aplicação que roda até completar. Unidade de admissão no Kueue.

### WorkloadPriorityClass
Define priority class para workload, independente de pod priority.

**Uso:** Queueing e preemption de Workloads

### AdmissionCheck
Mecanismo para componentes influenciarem timing de admissão de workloads.

### Topology
Cluster-scoped resource que representa hierarquia de nodes em um data center.

**Níveis:** Blocks, racks, etc.

**Referenciado por:** ResourceFlavor para Topology Aware Scheduling

---

## Glossário

### Quota Reservation
Processo onde Kueue scheduler locka recursos necessários por workload dentro de ClusterQueues ResourceGroups.

**Também chamado:** workload scheduling, job scheduling

### Admission
Processo de permitir Workload iniciar (Pods serem criados).

**Condições para admissão:**
1. Quota Reservation condition presente
2. Node capacity permite rodar (com Topology-Aware Scheduling)
3. AdmissionCheckStates em Ready state (se aplicável)

### Cohort
Grupo de ClusterQueues que podem emprestar quota não utilizada entre si.

### Queueing
Estado de Workload desde criação até admissão em ClusterQueue.

**Competição:** Baseada em Fair Sharing rules

### Preemption
Processo de evict um ou mais Workloads admitidos para acomodar outro Workload.

**Causas:**
- Lower priority
- Borrowing resources now needed by owning ClusterQueue

### Fair Sharing
Mecanismos para compartilhar quota entre tenants de forma justa.

### Elastic Workloads
Workload types que suportam scaling dinâmico.

---

## Arquitetura de Conceitos

```
┌─────────────────────────────────────────────────────┐
│                    Cohort                           │
│  ┌───────────────────────────────────────────────┐│
│  │              ClusterQueue A                    ││
│  │  ┌─────────────────────────────────────────┐ ││
│  │  │          ResourceGroups                   │ ││
│  │  │  ┌────────────┐  ┌────────────┐         │ ││
│  │  │  │ResourceFlavor│ │ResourceFlavor│        │ ││
│  │  │  │    A        │  │    B       │         │ ││
│  │  │  └────────────┘  └────────────┘         │ ││
│  │  └─────────────────────────────────────────┘ ││
│  └───────────────────────────────────────────────┘│
│  ┌───────────────────────────────────────────────┐│
│  │              ClusterQueue B                    ││
│  │              (can borrow from A)               ││
│  └───────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│                   Namespaces                        │
│  ┌─────────────────┐  ┌─────────────────┐         │
│  │   LocalQueue    │  │   LocalQueue    │         │
│  │   (Team A)      │  │   (Team B)      │         │
│  └─────────────────┘  └─────────────────┘         │
│  ┌─────────────────────────────────────────────┐  │
│  │              Workloads                       │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐       │  │
│  │  │ Job 1   │ │ Job 2   │ │ Job 3   │       │  │
│  │  └─────────┘ └─────────┘ └─────────┘       │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Key Concepts Summary

| Conceito | Tipo | Função |
|----------|------|--------|
| ResourceFlavor | Cluster-scoped | Define recursos disponíveis |
| ClusterQueue | Cluster-scoped | Governs resource pool, quotas |
| LocalQueue | Namespace-scoped | Groups related workloads |
| Workload | Unit | Application to completion |
| WorkloadPriorityClass | Priority | Independent from pod priority |
| AdmissionCheck | Mechanism | Influence admission timing |
| Topology | Cluster-scoped | Hierarchical node structure |

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Quota Reservation | Lock resources for workload |
| Admission | Allow workload to start |
| Cohort | ClusterQueues sharing quota |
| Preemption | Evict workloads for higher priority |
| Fair Sharing | Equitable quota distribution |

---

## Referências

- ResourceFlavor: https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/
- ClusterQueue: https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/
- LocalQueue: https://kueue.sigs.k8s.io/docs/concepts/local_queue/
- Workload: https://kueue.sigs.k8s.io/docs/concepts/workload/