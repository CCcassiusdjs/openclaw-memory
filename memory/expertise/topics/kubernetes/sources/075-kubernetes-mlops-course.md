# Kubernetes for MLOps - Chicago Data Science

**Fonte:** https://chicagodatascience.github.io/MLOps/lecture4/kubernetes/
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## Resumo

Tutorial prático de Kubernetes para MLOps: conceitos fundamentais, instalação (kubectl, minikube) e deploy de uma aplicação Flask (Weather Service).

---

## Conceitos Fundamentais

### O que é Kubernetes?
- Open-source system for automating deployment, scaling, management
- Open-sourced by Google (predecessor: Borg)
- Container orchestration for large complex systems
- Agnostic to which computer runs which container

### Arquitetura
```
┌─────────────────────────────────────────────────┐
│                   CLUSTER                       │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐         ┌─────────────────┐   │
│  │    MASTER   │ ←─────→ │     NODES       │   │
│  │ (coordinator)│         │  (workers/VMs)  │   │
│  └─────────────┘         └─────────────────┘   │
│                                │               │
│                                ▼               │
│                         ┌─────────────┐        │
│                         │   Kubelet   │        │
│                         │  + Docker   │        │
│                         └─────────────┘        │
└─────────────────────────────────────────────────┘
```

### Cluster Resources
| Resource | Função |
|----------|--------|
| **Master** | Coordinator of the cluster |
| **Nodes** | Workers (VMs/computers) that run containers |
| **Kubelet** | Node agent, communicates with master |
| **Docker daemon** | Pulls and runs containers |

---

## Key Concepts

### Deployment
- Set of instructions to K8s to set up application
- Containers mapped to individual nodes
- Deployment Controller monitors instances (self-healing)

### Nodes and Pods
| Concept | Description |
|---------|-------------|
| **Pod** | Collection of containers sharing storage/network |
| **Node** | VM/machine running multiple pods |
| **Container** | Single application (encapsulated in pod) |

**Pod shared resources:**
- Storage
- Networking and IP address

**Key insight:** Pods are created/destroyed, not individual containers

### Services
- Abstraction layer defining logical set of Pods
- External traffic exposure
- Load balancing
- Service discovery

**NodePort example:**
```yaml
# Exposes pods on same port of each selected node using NAT
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
```

### Scaling and Updates
- **Scaling:** Add/remove replicas dynamically
- **Rolling Updates:** Zero-downtime deployments

---

## Installation Guide

### Tools Required
| Tool | Purpose |
|------|---------|
| **kubectl** | CLI to talk to K8s server |
| **minikube** | Single-node K8s cluster locally |
| **VirtualBox** | VM for running minikube |
| **Docker** | Container runtime |

### kubectl Installation (macOS)
```bash
# Download
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl"

# Make executable
chmod +x kubectl
mv kubectl ~/Library/local/bin/

# Verify
kubectl version --client
```

### minikube Installation
```bash
# Check virtualization support
sysctl -a | grep -E --color 'machdep.cpu.features|VMX'

# Download
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64

# Install
chmod +x minikube
mv minikube ~/Library/local/bin/

# Start cluster
minikube start
```

---

## Weather Service App Tutorial

### Deploy Sequence
```
1. Build Docker image
   ↓
2. Push to minikube registry
   ↓
3. Create Deployment YAML
   ↓
4. Apply deployment
   ↓
5. Expose Service
```

### Key Commands
```bash
# Check status
minikube status
kubectl get nodes
kubectl get all

# Use minikube Docker registry
eval $(minikube -p minikube docker-env)

# Build image
docker build -t weather-service-k8s/latest .

# Create deployment
kubectl create deployment weather-minikube --image=weather-service-k8s:latest -o yaml --dry-run=client

# Apply deployment
kubectl apply -f weather_minikube.yaml
```

### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: weather-minikube
  name: weather-minikube
spec:
  replicas: 1
  selector:
    matchLabels:
      app: weather-minikube
  template:
    metadata:
      labels:
        app: weather-minikube
    spec:
      containers:
      - image: weather-service-k8s/latest:latest
        name: weather-service-k8s
        imagePullPolicy: Never
```

---

## Insights

### When to Use Kubernetes?
> "Unless we have a truly massive or complex system, we probably don't need Kubernetes."

- Use for: Large/complex systems
- Consider alternatives for: Smaller workloads (managed solutions)

### Development Workflow
```
Local Development (minikube)
    ↓
Testing
    ↓
Production Cluster
```

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Master-Node Architecture | Master coordinates, Nodes run workloads |
| Pods | Smallest deployable units (container groups) |
| Services | Abstraction for pod access and load balancing |
| Deployment | Desired state specification |
| minikube | Local single-node cluster for development |

---

## Referências

- Kubernetes Basics: https://kubernetes.io/docs/tutorials/kubernetes-basics/
- kubectl Install: https://kubernetes.io/docs/tasks/tools/install-kubectl/
- minikube Install: https://kubernetes.io/docs/tasks/tools/install-minikube/