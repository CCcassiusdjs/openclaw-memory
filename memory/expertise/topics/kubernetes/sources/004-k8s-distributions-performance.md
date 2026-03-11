# Kubernetes in Action: Performance of Kubernetes Distributions in the Cloud

**Source:** arXiv:2403.01429v1  
**Type:** Academic Research Paper  
**URL:** https://arxiv.org/html/2403.01429v1  
**Date:** March 2024  
**Author:** Ehsan Ataie (University of Mazandaran)  
**Status:** Completed

---

## Summary

This paper investigates the **performance of four Kubernetes distributions** (Kubeadm, K3s, MicroK8s, K0s) when running **OpenFaaS** serverless workloads on CloudLab. It also compares **two Xen virtualization modes** (HVM vs PV) and **two container runtimes** (Docker vs Containerd).

---

## Key Findings

### Kubernetes Distributions Compared

| Distribution | Type | Characteristics |
|--------------|------|-----------------|
| **Kubeadm** | Standard | Official upstream Kubernetes |
| **K3s** | Lightweight | Rancher, single binary |
| **MicroK8s** | Lightweight | Canonical, snap-based |
| **K0s** | Lightweight | Mirantis, single binary |

### Related Work Findings (from literature)

| Study | Findings |
|-------|----------|
| **Koziolek et al.** | K3s and K0s showed highest control plane throughput; MicroShift highest data plane throughput |
| **Kjorveziroski et al.** | K3s and MicroK8s performed better than Kubespray (reduced deployment time/complexity) |
| **Costa et al.** | Detected memory leaks in K3s persisting beyond cluster halts (software aging) |

### Container Runtime Comparison

| Runtime | Architecture | Notes |
|---------|--------------|-------|
| **Docker** | dockerd + containerd | More components, higher overhead |
| **Containerd** | Direct daemon | Simpler, lower overhead |

### Virtualization Modes (Xen)

| Mode | Description |
|------|-------------|
| **HVM** | Hardware Virtual Machine - guest OS unaware of virtualization |
| **PV** | Paravirtualization - guest OS modified for virtualization, better performance |

---

## Methodology

1. **Hypervisor comparison**: Xen HVM vs PV on CloudLab
2. **Container runtime comparison**: Docker vs Containerd
3. **Disk performance**: Sysbench + MySQL (disk-intensive)
4. **CPU performance**: OpenFaaS (compute-intensive)
5. **Distribution comparison**: Kubeadm, K3s, MicroK8s, K0s

**Metrics measured:**
- Request rate
- CPU utilization
- Scaling behavior

---

## Concepts Learned

| Concept | Description |
|---------|-------------|
| **K8s Distributions** | Multiple implementations: Kubeadm, K3s, MicroK8s, K0s |
| **HVM vs PV** | Hardware Virtual Machine vs Paravirtualization |
| **Containerd vs Docker** | Runtime architecture differences |
| **OpenFaaS** | Popular FaaS platform (24.3k GitHub stars) |
| **Serverless on K8s** | Function-as-a-Service on Kubernetes |
| **Software Aging** | Memory leaks persisting beyond cluster halts |
| **Control Plane Throughput** | K8s API/scheduler performance metric |
| **Data Plane Throughput** | Workload performance metric |

---

## FaaS Platforms Mentioned

- **OpenFaaS** - Most popular (24.3k stars)
- **Knative** - Google's serverless platform
- **Apache OpenWhisk** - Apache serverless
- **Fission** - K8s-native serverless
- **Nuclio** - High-performance serverless
- **Kubeless** - Kubernetes-native FaaS

---

## Performance Implications

- **Lightweight distributions** (K3s, MicroK8s, K0s) often outperform standard Kubespray
- **Containerd** preferred over Docker for production (lower overhead)
- **PV mode** can provide better performance than HVM
- **Software aging** requires monitoring in long-running clusters

---

## Cross-References

- **Lightweight K8s** → Source 005 (Comparative Analysis)
- **Container runtimes** → Sources 041-046 (Container Security)
- **Performance monitoring** → Sources 038-039 (Architecture)

---

*Read date: 2026-03-11*