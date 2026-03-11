# Kubernetes Tutorial for Beginners: Basic Concepts (Spacelift)

**Source:** spacelift.io/blog/kubernetes-tutorial
**Type:** Tutorial
**Priority:** Medium
**Date:** 2026

---

## Summary

Tutorial abrangente sobre Kubernetes fundamentals, cobrindo arquitetura, conceitos básicos, e instalação prática com K3s. Focado em iniciantes que já conhecem Docker.

## What is Kubernetes?

### Definition
- Open-source container orchestration system
- Originally developed at Google
- Now maintained by CNCF (Cloud Native Computing Foundation)
- Automates deployment, scaling, and management of containerized applications

### Key Statistics
- 80% of respondents run Kubernetes in production (CNCF 2025)
- 13% testing it
- K8s is now default platform for containerized workloads

## Kubernetes Features

### Core Capabilities
1. **Automated Rollouts/Scaling/Rollbacks**
   - Creates specified replicas
   - Distributes onto suitable hardware
   - Reschedules if node goes down
   - Scales on-demand or by CPU usage

2. **Service Discovery & Load Balancing**
   - Internal service discovery
   - Public container exposure
   - Built-in load balancing

3. **Stateless and Stateful Applications**
   - Built-in objects for stateful apps (StatefulSet)
   - Any application type supported

4. **Storage Management**
   - Consistent interface across providers
   - Cloud, network share, or local filesystem

5. **Declarative State**
   - YAML manifests for desired state
   - Automatic transition to target state

6. **Cross-Environment Support**
   - Cloud, edge, local workstation
   - Many distributions available

7. **Highly Extensible**
   - Custom object types (CRDs)
   - Custom controllers
   - Operators

## How Kubernetes Works

### Cluster Architecture
- **Cluster**: Set of nodes running containers
- **Node**: Physical machine or VM
- **Control Plane**: Coordinates cluster operations

### Control Plane Components

| Component | Description |
|-----------|-------------|
| kube-apiserver | API server - only way to interact with cluster |
| kube-controller-manager | Runs built-in controllers (event loops) |
| kube-scheduler | Assigns Pods to nodes |
| kubelet | Worker process on each node |
| kube-proxy | Configures host networking |

### Distributions Mentioned
- **Official**: kubeadm (complex setup)
- **Development**: Minikube, MicroK8s, K3s, Kind
- **Cloud Managed**: GKE, EKS, AKS

## Basic Terms and Concepts

### 1. Nodes
- Physical/virtual machines forming the cluster
- Up to 5,000 nodes supported (theoretically more)
- Each node runs kubelet and kube-proxy

### 2. Namespaces
- Resource isolation mechanism
- Avoids name collisions
- Scope for RBAC

### 3. Pods
- Fundamental compute unit
- Can contain multiple containers
- Always scheduled together
- Shared context (network, storage)

### 4. ReplicaSets
- Maintains replica count
- Automatically replaces failed Pods
- Lower-level abstraction

### 5. Deployments
- Wraps ReplicaSets
- Declarative updates
- Rollback support
- Pause/resume rollouts

### 6. Services
- Exposes Pods to network
- Stable endpoint for dynamic Pods
- Load balancing built-in

### 7. Ingresses
- External access to Services
- HTTP/HTTPS routing
- SSL termination

## Quick Start with K3s

```bash
# Install K3s
curl -sfL https://get.k3s.io | sh -

# Setup kubeconfig
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
export KUBECONFIG=~/.kube/config

# Verify
kubectl get nodes
```

## Key Takeaways

1. Kubernetes solves container orchestration at scale
2. Declarative configuration is core paradigm
3. Control plane manages cluster state
4. Multiple distributions for different use cases
5. K3s is simplest for learning/development

## Personal Notes

Este tutorial é excelente para quem já conhece Docker. A abordagem com K3s é mais simples que Minikube. A tabela de componentes do control plane é uma referência útil. A explicação de Pods vs Containers é clara.

Para certificação CKA/CKAD, vale focar nos conceitos de Services e Deployments que são bem explicados aqui.