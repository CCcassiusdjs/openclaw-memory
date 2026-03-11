# Resilience Evaluation of Kubernetes in Cloud-Edge Environments via Failure Injection

**Source:** arXiv:2507.16109  
**Type:** Academic Research Paper  
**URL:** https://arxiv.org/abs/2507.16109  
**Date:** July 2025  
**Author:** Zihao Chen  
**Status:** Completed

---

## Summary

This paper presents a **novel resilience evaluation framework** for Kubernetes in hybrid cloud-edge environments. It integrates fault injection tools with automated workload generation to systematically assess system resilience under realistic failure conditions.

---

## Key Findings

### Resilience Comparison

| Environment | Strength | Improvement |
|-------------|----------|-------------|
| **Cloud-Edge** | Response stability under network delay/partition | 80% superior |
| **Cloud-only** | Resilience under bandwidth limitations | 47% better |

### Dataset Created

- **Size:** 30+ GB of performance data
- **Scenarios:** 11,965 fault injection scenarios
- **Metrics:** Response times, failure rates, error patterns

### Fault Types Tested

| Level | Failure Types |
|-------|---------------|
| **Node-level** | Node failures, resource exhaustion |
| **Pod-level** | Container crashes, OOM kills |
| **Network** | Delays, partitions, bandwidth limits |

---

## Methodology

### Fault Injection Tools Used
- **Chaos Mesh** - CNCF chaos engineering platform
- **Gremlin** - Commercial chaos engineering tool
- **ChaosBlade** - Alibaba's chaos engineering tool

### Workload Generation
- Automated traffic simulation
- Realistic failure scenarios
- Cloud and cloud-edge environments

---

## Concepts Learned

| Concept | Description |
|---------|-------------|
| **Resilience Evaluation** | Systematic assessment of system recovery from failures |
| **Fault Injection** | Deliberately introducing failures to test resilience |
| **Chaos Engineering** | Discipline of experimenting on distributed systems |
| **Cloud-Edge Hybrid** | Architecture combining cloud and edge computing |
| **Network Partition** | Failure scenario where network connectivity is lost |
| **Response Stability** | Ability to maintain consistent response times under failures |

---

## Fault Injection Framework

```
┌─────────────────────────────────────┐
│     Resilience Evaluation Framework   │
├─────────────────────────────────────┤
│  Fault Injection Tools:              │
│  • Chaos Mesh                        │
│  • Gremlin                           │
│  • ChaosBlade                        │
├─────────────────────────────────────┤
│  Workload Generation:                │
│  • Automated traffic simulation      │
│  • Realistic failure scenarios       │
├─────────────────────────────────────┤
│  Target Environments:                │
│  • Cloud-only                        │
│  • Cloud-Edge hybrid                │
└─────────────────────────────────────┘
```

---

## Key Insights for Practice

| Failure Type | Best Environment | Guidance |
|--------------|------------------|----------|
| Network delay | Cloud-Edge | 80% better response stability |
| Network partition | Cloud-Edge | Superior handling |
| Bandwidth limitation | Cloud-only | 47% better resilience |
| Node failure | Depends on architecture | Consider replication strategy |

---

## Research Contributions

1. **First comprehensive resilience dataset** for hybrid cloud-edge Kubernetes
2. **Novel evaluation framework** integrating multiple chaos tools
3. **Quantitative guidance** for architectural decisions
4. **30+ GB performance data** from 11,965 scenarios

---

## Cross-References

- **Edge computing** → Source 005 (Lightweight K8s)
- **Chaos engineering** → Sources 038-039 (Architecture reliability)
- **Network failures** → Sources 047-053 (CNI/Networking)

---

*Read date: 2026-03-11*