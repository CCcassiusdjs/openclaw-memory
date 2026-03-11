# Comparative Analysis of Lightweight Kubernetes Distributions for Edge Computing

**Source:** arXiv:2504.03656  
**Type:** Academic Research Paper  
**URL:** https://arxiv.org/abs/2504.03656  
**Date:** March 2025  
**Authors:** Diyaz Yakubov, David Hästbacka (Tampere University)  
**Published:** ESOCC 2025 (Springer)  
**Status:** Completed

---

## Summary

This paper provides an **empirical analysis of five lightweight Kubernetes distributions** for edge computing: k0s, k3s, KubeEdge, OpenYurt, and standard Kubernetes (k8s). The study evaluates **performance and resource efficiency** using Intel NUCs and Raspberry Pi devices as testbed.

---

## Key Findings

### Distributions Compared

| Distribution | Characteristics |
|--------------|-----------------|
| **k0s** | Lightweight, single binary, by Mirantis |
| **k3s** | Lightweight, by Rancher/SUSE |
| **KubeEdge** | CNCF project, edge-focused features |
| **OpenYurt** | Alibaba, hybrid cloud-edge use cases |
| **k8s** | Standard Kubernetes (upstream) |

### Performance Results

| Distribution | Resource Usage | Throughput | Latency | Scalability |
|--------------|----------------|------------|---------|-------------|
| **k3s** | Lowest | Good | Good | High |
| **k0s** | Low | Highest | Lowest | High |
| **k8s** | Medium | High | Low | Medium |
| **OpenYurt** | Higher | Balanced | Balanced | Lower |
| **KubeEdge** | Highest | Lower | Higher | Lower |

### Key Insights

- **k3s**: Lowest resource consumption, ideal for resource-constrained edge devices
- **k0s and k8s**: Excelled in data plane throughput and latency
- **k3s and k0s**: Accomplished same workloads faster under heavy stress
- **OpenYurt**: Balanced for hybrid cloud-edge, but less resource-efficient
- **KubeEdge**: Feature-rich for edge but higher resource consumption, lower scalability

---

## Methodology

### Testbed Hardware
- Intel NUCs
- Raspberry Pi devices

### Metrics Evaluated
- CPU usage
- Memory usage
- Disk usage
- Throughput
- Latency

### Workload Scenarios
- Varying workloads
- Heavy stress scenarios
- Edge computing scenarios

---

## Concepts Learned

| Concept | Description |
|---------|-------------|
| **Lightweight K8s** | Kubernetes distributions optimized for edge/resource-constrained environments |
| **Edge Computing** | Computing at network edge, near data source |
| **Resource Efficiency** | CPU/memory/disk usage optimization |
| **Data Plane Throughput** | Workload processing capacity |
| **Control Plane Throughput** | API/scheduler performance |
| **Hybrid Cloud-Edge** | Architecture combining cloud and edge computing |

---

## Edge-Specific Considerations

- **Resource constraints**: Edge devices have limited CPU/memory
- **Network limitations**: Intermittent connectivity at edge
- **Scalability**: Ability to manage many edge nodes
- **Latency**: Response time critical for edge applications

---

## Recommendations from Paper

| Use Case | Recommended Distribution |
|----------|--------------------------|
| Resource-constrained edge | k3s |
| High throughput requirements | k0s or k8s |
| Hybrid cloud-edge | OpenYurt |
| Edge-specific features | KubeEdge (if resources available) |

---

## Cross-References

- **Lightweight K8s comparison** → Source 004 (K8s Distributions Performance)
- **Edge computing** → Source 006 (Resilience in Cloud-Edge)
- **Performance monitoring** → Sources 038-039 (Architecture)

---

*Read date: 2026-03-11*