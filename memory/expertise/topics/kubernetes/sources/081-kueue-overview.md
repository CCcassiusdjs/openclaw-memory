# Kueue Overview

**Fonte:** https://kueue.sigs.k8s.io/docs/overview/
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

Visão geral do Kueue: sistema Kubernetes-native para gerenciamento de quotas e jobs. Decide quando jobs devem esperar, iniciar ou ser preemptados.

---

## Por que usar Kueue

Instala em cluster Kubernetes vanilla. Não substitui componentes existentes.

### Compatibilidade
- Compute resources elásticos (scale up/down)
- Compute resources heterogêneos (arquitetura, availability, preço)

### APIs permitem expressar
- Quotas e políticas para Fair Sharing
- Resource fungibility: usar flavor diferente se um estiver full

### Princípio de Design
Evitar duplicar funcionalidade madura:
- **Autoscaling:** cluster-autoscaler
- **Pod-to-node scheduling:** kube-scheduler
- **Job lifecycle:** kube-controller-manager
- **Advanced admission control:** gatekeeper

---

## Features Overview

### Job Management
- Queueing baseado em priorities
- Estratégias: StrictFIFO, BestEffortFIFO

### Advanced Resource Management
- Resource flavor fungibility
- Fair Sharing
- Cohorts
- Preemption com múltiplas políticas

### Integrations
| Job Type | Support |
|----------|---------|
| BatchJob | ✅ |
| Kubeflow training jobs | ✅ |
| RayJob | ✅ |
| RayCluster | ✅ |
| JobSet | ✅ |
| AppWrappers | ✅ |
| Plain Pod / Pod Groups | ✅ |
| Deployment | ✅ |
| StatefulSet | ✅ |
| LeaderWorkerSet | ✅ |

### System Insight
- Prometheus metrics
- On-demand visibility para pending workloads

### AdmissionChecks
- Mecanismo para influenciar admissão
- Integration com cluster-autoscaler provisioningRequest

### All-or-Nothing
- Timeout-based implementation
- Wait for all pods ready

### Partial Admission
- Rodar job com parallelism reduzido
- Dynamic reclaim de quota quando pods completam

### Mixing Training + Inference
- Batch workloads + serving workloads (Deployments, StatefulSets)

### Multi-Cluster
- **MultiKueue:** dispatch para outros clusters
- Search capacity off-main cluster

### Topology-Aware Scheduling
- Otimiza pod-pod communication throughput
- Data-center topology aware

---

## Job-Integrated Features Matrix

| Feature | BatchJob | JobSet | PytorchJob | TFJob | TrainJob | RayJob | Deployment |
|---------|----------|--------|------------|-------|----------|--------|------------|
| Dynamic Reclaim | ✅ | ✅ | ✅ | ✅ | | | |
| MultiKueue | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PartialAdmission | ✅ | | | | | | |
| Workload Priority | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| FlavorFungibility | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| ProvisioningACC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Fair Sharing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Topology Aware | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## High-Level Operation

```
┌─────────────────────────────────────────────────────┐
│                   User Submits Job                  │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│              Kueue Webhook (set suspend=true)       │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│                LocalQueue (namespaced)              │
│                 Groups related workloads             │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│            ClusterQueue (cluster-scoped)            │
│         Quota management, Fair Sharing              │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│               Quota Reservation                     │
│         Lock resources for workload                 │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│               Admission Check                        │
│         Verify AdmissionChecks ready                │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│               Workload Admitted                      │
│         Pods created (suspend=false)                 │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│               kube-scheduler                         │
│         Pods scheduled to nodes                      │
└─────────────────────────────────────────────────────┘
```

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| StrictFIFO | Queueing com ordem estrita |
| BestEffortFIFO | Queueing com flexibilidade |
| Resource Fungibility | Usar flavor alternativo |
| MultiKueue | Multi-cluster job dispatching |
| ProvisioningRequest | Integration com cluster-autoscaler |
| Partial Admission | Rodar com parallelism reduzido |

---

## Referências

- Concepts: https://kueue.sigs.k8s.io/docs/concepts/
- Tasks: https://kueue.sigs.k8s.io/docs/tasks/
- Metrics: https://kueue.sigs.k8s.io/docs/reference/metrics/