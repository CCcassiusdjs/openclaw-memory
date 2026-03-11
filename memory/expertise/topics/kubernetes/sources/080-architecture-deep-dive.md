# Kubernetes Architecture Deep Dive

**Source:** https://devopscube.com/kubernetes-architecture-explained/
**Type:** Tutorial/Blog
**Category:** Architecture
**Read:** 2026-03-11

---

## Resumo

### Kubernetes Cluster Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                         │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  CONTROL PLANE                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │ │
│  │  │ kube-apiserver│  │    etcd      │  │kube-scheduler│  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │ │
│  │  ┌──────────────────────┐  ┌──────────────────────────┐│ │
│  │  │kube-controller-manager│ │cloud-controller-manager ││ │
│  │  └──────────────────────┘  └──────────────────────────┘│ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                               │
│  ┌───────────────────────────┼───────────────────────────┐  │
│  │        WORKER NODES      │                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │   Node 1    │  │   Node 2    │  │   Node N    │   │  │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │   │  │
│  │  │ │ kubelet │ │  │ │ kubelet │ │  │ │ kubelet │ │   │  │
│  │  │ ├─────────┤ │  │ ├─────────┤ │  │ ├─────────┤ │   │  │
│  │  │ │kube-proxy│ │  │ │kube-proxy│ │  │ │kube-proxy│ │   │  │
│  │  │ ├─────────┤ │  │ ├─────────┤ │  │ ├─────────┤ │   │  │
│  │  │ │Container│ │  │ │Container│ │  │ │Container│ │   │  │
│  │  │ │ Runtime │ │  │ │ Runtime │ │  │ │ Runtime │ │   │  │
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │   │  │
│  │  │   [Pods]    │  │   [Pods]    │  │   [Pods]    │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Control Plane Components

### 1. kube-apiserver

**Função:** Hub central do cluster, expõe Kubernetes API

**Responsabilidades:**
| Função | Descrição |
|--------|-----------|
| API Management | Expõe endpoints, versionamento |
| Authentication | Client certificates, bearer tokens, HTTP Basic |
| Authorization | ABAC, RBAC evaluation |
| Admission Control | Validation e Mutation controllers |
| Aggregation Layer | Extensões customizadas |
| Watch API | Real-time notifications |

**Características:**
- Highly scalable
- Handle large number of concurrent requests
- All communication over TLS
- Only connects to etcd directly

### 2. etcd

**Função:** Brain do cluster, backend storage

**Características:**
- Strongly consistent (CAP: CP)
- Distributed key-value store
- Raft consensus algorithm
- Leader-member fashion for HA
- Built on BoltDB

**Fault Tolerance:**
| Nodes | Tolerates |
|-------|-----------|
| 3 | 1 failure |
| 5 | 2 failures |
| 7 | 3 failures |

**Formula:** `fault tolerance = (n - 1) / 2`

**Storage Path:** `/registry/<resource>/<namespace>/<name>`
Exemplo: `/registry/pods/default/nginx`

### 3. kube-scheduler

**Função:** Scheduling de Pods em worker nodes

**Processo:**
```
1. Filtering: Encontra nodes elegíveis
   - Resource availability
   - Affinity/anti-affinity
   - Taints/tolerations
   - PV requirements

2. Scoring: Ranking dos nodes elegíveis
   - Multiple scheduling plugins
   - Highest score wins
   - Random se empate

3. Binding: Aplica decisão ao cluster
```

**Configuração:**
- `percentageOfNodesToScore`: Default 50%
- Large clusters: Default 5%
- Custom schedulers supported
- Pluggable scheduling framework

**DRA (Dynamic Resource Allocation):**
- Stable since v1.34
- Hardware-aware scheduling
- Útil para GPUs, FPGAs, smart NICs
- AI/ML workloads benefit

### 4. kube-controller-manager

**Função:** Gerencia todos os controllers

**Controllers Built-in:**
- Deployment controller
- Replicaset controller
- DaemonSet controller
- Job controller
- CronJob controller
- Endpoints controller
- Namespace controller
- Service accounts controller
- Node controller

**Conceito:** Control loop = watch actual vs desired state

### 5. cloud-controller-manager (CCM)

**Função:** Bridge entre cloud APIs e Kubernetes

**Controllers:**
| Controller | Função |
|------------|--------|
| Node controller | Atualiza info de nodes via cloud API |
| Route controller | Configura rotas na cloud |
| Service controller | Provisiona Load Balancers |
| Volume controller | Provisiona storage |

---

## Worker Node Components

### 1. kubelet

**Função:** Agente em cada node, garante containers rodando

**Responsabilidades:**
- Watch API server for Pod assignments
- Report node status
- Execute health checks
- Manage container lifecycle

### 2. kube-proxy

**Função:** Network proxy, implementa Services

**Modos:**
- iptables mode (default)
- IPVS mode (better performance)
- Userspace mode (deprecated)

### 3. Container Runtime

**Função:** Executa containers

**Opções:**
- containerd
- CRI-O
- Qualquer CRI-compliant runtime

---

## Fluxo de Comunicação

```
kubectl ────▶ API Server ────▶ etcd
                 │
                 ▼
           Scheduler (watch)
                 │
                 ▼
           Binding Event
                 │
                 ▼
             kubelet (watch)
                 │
                 ▼
         Container Runtime
                 │
                 ▼
              [Pods]
```

---

## Conceitos-Chave

1. **Distributed System**: Múltiplos componentes em rede
2. **Control Plane**: Orchestration e desired state
3. **Worker Nodes**: Execução de containers
4. **etcd = Single Source of Truth**: Backup crítico
5. **Scheduler**: Filtering + Scoring
6. **Controller Manager**: Reconciliation loops
7. **Watch-based Communication**: Real-time updates