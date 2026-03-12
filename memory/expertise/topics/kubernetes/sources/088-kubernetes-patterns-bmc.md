# 3 Kubernetes Patterns for Cloud Native Applications

**Fonte:** https://www.bmc.com/blogs/kubernetes-patterns/
**Tipo:** Artigo
**Data:** 2026-03-12

---

## Resumo

Três padrões fundamentais para aplicações cloud-native em Kubernetes: Foundational Pattern, Behavioral Pattern e Structural Pattern.

---

## Overview

Cloud-native applications devem ser:
- Scalable
- Elastic
- Reliable
- Predictable

---

## 1. Foundational Pattern

Fundamental para rodar qualquer container-based application em Kubernetes.

### 5 Key Areas

| Area | Description |
|------|-------------|
| **Predictable Demand** | Resource profile + runtime dependencies |
| **Declarative Deployment** | Automation with Deployment workload |
| **Health Probe** | Liveness + Readiness probes |
| **Managed Lifecycle** | React to lifecycle events |
| **Automated Placement** | Scheduler + affinity rules |

### Predictable Demands

Entender:
- **Runtime dependencies:** PV, ConfigMap, Secrets
- **Resource profile:** CPU (compressible), Memory (incompressible)

### Declarative Deployment

- Deployments para Pods e ReplicaSets
- Containers devem honrar sigterm
- Health-check endpoints para status

### Health Probe

| Probe | Behavior on Failure |
|-------|---------------------|
| **Liveness** | Container terminated |
| **Readiness** | Container removed from service |

### Managed Lifecycle

| Hook | Description |
|------|-------------|
| **PostStart** | Blocking call when container created |
| **PreStop** | Blocking call before termination |
| **SIGTERM** | Graceful shutdown signal |
| **SIGKILL** | Force kill (after 30s) |

### Automated Placement

Considerations:
- Available node resources
- Container resource demands
- Placement policies
- Node affinity, pod affinity/anti-affinity
- Taints and tolerations

---

## 2. Behavioral Pattern

Focado em pod management primitives e seus comportamentos.

### Concepts

| Concept | Description |
|---------|-------------|
| **Batch Job** | Short-lived pods until completion |
| **Periodic Job** | CronJob - time/event based execution |
| **Daemon Service** | DaemonSet - one pod per node |
| **Stateful Service** | StatefulSet - persistent identity, storage |
| **Self-awareness** | Downward API - metadata injection |

### Batch Job
- Run tasks until completion
- Don't restart after completion
- Useful for finite tasks

### Periodic Job (CronJob)
- Similar to Unix crontab
- Highly available
- Time or event-based execution

### Daemon Service (DaemonSet)
- One pod per node
- Useful for logging, monitoring
- Example: fluentd for log collection

### Stateful Service (StatefulSet)
- Persistent identity
- Persistent storage
- Ordered scaling
- Stable network identity

### Self-awareness (Downward API)
- Metadata injection into containers
- Environment variables or files
- Example: POD_IP, POD_NAME

---

## 3. Structural Pattern

Organiza containers em pods seguindo single responsibility model.

### Single Responsibility
- Cada container deve fazer UMA task
- Múltiplas tasks = múltiplos containers

### Container Patterns

| Pattern | Purpose |
|---------|---------|
| **Init Containers** | Initialization before app starts |
| **Sidecar** | Extend functionality without changing container |
| **Adapter** | Unified interface for heterogeneous containers |
| **Ambassador** | Proxy for external services |

### Init Containers

```yaml
spec:
  initContainers:
  - name: init-db
    image: busybox
    command: ["sh", "-c", "setup-database.sh"]
  containers:
  - name: app
    image: my-app
```

**Características:**
- Run sequentially
- Block until completion
- No readiness check
- Used for initialization tasks

### Sidecar Pattern

```
┌─────────────────────────────────────┐
│              Pod                     │
│  ┌─────────────────────────────────┐│
│  │  Main Container (HTTP Server)  ││
│  │  - Serve content               ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  Sidecar (Content Sync)        ││
│  │  - Pull from S3/Git            ││
│  │  - Update shared volume        ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Benefícios:**
- Extend functionality
- Single-purpose containers
- Cooperate closely
- No container modification needed

### Adapter Pattern

```
┌─────────────────────────────────────┐
│              Pod                     │
│  ┌─────────────────────────────────┐│
│  │  App Container 1 (Python)      ││
│  │  - Logs in Python format       ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  App Container 2 (Java)        ││
│  │  - Logs in Java format          ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  Adapter Container              ││
│  │  - Parse all logs               ││
│  │  - Output unified format        ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Uso:** Unified interface para third-party tools

### Ambassador Pattern

```
┌─────────────────────────────────────┐
│              Pod                     │
│  ┌─────────────────────────────────┐│
│  │  Main Container (Application)   ││
│  │  - Business logic               ││
│  │  - Sends to localhost:6379     ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  Ambassador Container            ││
│  │  - Redis proxy                  ││
│  │  - Forwards to Redis cluster    ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
         │
         ▼
   External Redis
```

**Benefícios:**
- Main app unaware of external service
- Ambassador handles connection
- Easy to change external service

---

## Pattern Selection Guide

| Use Case | Pattern |
|----------|----------|
| Database initialization | Init Container |
| Log collection | Sidecar |
| Metrics normalization | Adapter |
| External DB connection | Ambassador |
| Run on every node | DaemonSet |
| Maintain state | StatefulSet |
| Scheduled tasks | CronJob |

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Predictable Demand | Resource profile + dependencies |
| Health Probe | Liveness + Readiness checks |
| Init Container | Pre-startup initialization |
| Sidecar | Extend main container |
| Adapter | Normalize interfaces |
| Ambassador | Proxy external services |
| Downward API | Pod metadata injection |

---

## Referências

- Kubernetes Patterns Book: https://k8spatterns.com/
- Kubernetes Guide (BMC): https://www.bmc.com/blogs/what-is-kubernetes/
- Twelve Factor App: https://www.bmc.com/blogs/twelve-factor-app/