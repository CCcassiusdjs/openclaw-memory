# Kubernetes for MLOps - Chicago Data Science

**Fonte:** Chicago Data Science - https://chicagodatascience.github.io/MLOps/lecture4/kubernetes/
**Data:** 2024-2025
**Tópico:** Kubernetes Fundamentals, kubectl, minikube, Deployment Tutorial
**Status:** Lido

---

## Resumo Executivo

Tutorial prático de Kubernetes para MLOps, cobrindo conceitos fundamentais (nodes, pods, services, deployments) e implementação hands-on com minikube, kubectl e uma aplicação de weather service.

---

## Conceitos-Chave

### O que é Kubernetes

- **Definição**: Sistema open-source para automação de deployment, scaling e gestão de aplicações containerizadas
- **Origem**: Open-sourced pelo Google (precursor: Borg)
- **Nome curto**: K8s (K + 8 letras + s)
- **Propósito**: Orquestração de containers em clusters

### Arquitetura de Cluster

#### Master (Control Plane)
- Coordenador do cluster
- Gerencia scheduling
- API server, scheduler, controller manager, etcd

#### Nodes (Workers)
- VMs/máquinas que rodam containers
- Cada node roda:
  - **Kubelet**: Comunica com master, gerencia pods
  - **Docker/containerd**: Runtime de containers
- Pods são agendados em nodes

---

## Conceitos Fundamentais

### Deployment

- **Definição**: Set de instruções para K8s setup de aplicação
- **Function**: Mapeia containers para nodes
- **Self-healing**: Deployment Controller monitora instâncias
- **Spec**: Container images + número de réplicas

### Nodes e Pods

#### Pods
- Unidade básica do K8s
- Collection de containers relacionados
- Compartilham:
  - Storage
  - Networking (IP address)
- Pod é criado/destruído, não container individual

#### Nodes
- VM/machine no cluster
- Pode ter múltiplos pods
- Executa kubelet + container runtime

### Services

- **Abstraction layer**: Conjunto lógico de Pods
- **Features**:
  - External traffic exposure
  - Load balancing
  - Service discovery
- **NodePort**: Expõe pods em cada node via NAT
- **LoadBalancer**: Expõe externamente

### Scaling e Updating

- **Scaling**: `kubectl scale` para aumentar réplicas
- **Rolling Update**: Update gradual de versões
- **Rollback**: Retorno para versão anterior

---

## Instalação de Ferramentas

### VirtualBox
- Software para VMs
- Disponível para MacOS/Windows/Linux
- Base para minikube local

### kubectl
- CLI para interagir com K8s
- Download: https://kubernetes.io/docs/tasks/tools/install-kubectl/

```bash
# MacOS
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
mv kubectl ~/Library/local/bin/
kubectl version --client
```

### minikube
- Single-node K8s cluster local
- Cria VM na máquina local

```bash
# Verificar virtualização
sysctl -a | grep -E --color 'machdep.cpu.features|VMX'

# Instalar
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
chmod +x minikube
mv minikube ~/Library/local/bin/

# Iniciar cluster
minikube start

# Status
minikube status
```

---

## Weather Service App - Tutorial

### Setup

```bash
# Iniciar minikube
minikube start

# Verificar contexto
kubectl config current-context

# Verificar nodes
kubectl get nodes
```

### Docker Build

```bash
# Configurar docker env para minikube
eval $(minikube -p minikube docker-env)

# Build da imagem
docker build -t weather-service-k8s/latest .

# Verificar imagens
docker images
```

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: weather-minikube
  name: weather-minikube
spec:
  replicas: 1
  selector:
    matchLabels:
      app: weather-minikube
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: weather-minikube
    spec:
      containers:
      - image: weather-service-k8s/latest:latest
        name: weather-service-k8s
        resources: {}
        imagePullPolicy: Never  # Importante para imagens locais
status: {}
```

### Aplicar Deployment

```bash
# Criar deployment
kubectl apply -f weather_minikube.yaml

# Verificar pods
kubectl get all
```

---

## Fluxo de Trabalho

```
┌─────────────────────────────────────────────────┐
│  1. Develop App (Flask/FastAPI)                 │
│     → test_model.py, app.py                     │
├─────────────────────────────────────────────────┤
│  2. Containerize (Docker)                       │
│     → Dockerfile, build image                    │
├─────────────────────────────────────────────────┤
│  3. Create Cluster (minikube)                   │
│     → minikube start                             │
├─────────────────────────────────────────────────┤
│  4. Define Manifests (YAML)                     │
│     → deployment.yaml, service.yaml              │
├─────────────────────────────────────────────────┤
│  5. Deploy (kubectl)                             │
│     → kubectl apply -f deployment.yaml          │
├─────────────────────────────────────────────────┤
│  6. Expose Service                              │
│     → kubectl port-forward svc/name port:port   │
└─────────────────────────────────────────────────┘
```

---

## Comandos Úteis

### Verificação
```bash
kubectl get nodes           # Lista nodes
kubectl get pods            # Lista pods
kubectl get all             # Lista todos recursos
kubectl get services        # Lista services
kubectl describe pod <name> # Detalhes do pod
```

### Logs e Debugging
```bash
kubectl logs <pod-name>            # Logs do pod
kubectl logs <pod-name> -f         # Follow logs
kubectl exec -it <pod-name> -- sh # Shell no container
```

### Deployment
```bash
kubectl apply -f <file.yaml>       # Aplicar manifesto
kubectl delete -f <file.yaml>       # Remover recurso
kubectl scale deployment <name> --replicas=3  # Escalar
```

---

## Insights para Kubernetes

1. **Pod é a unidade básica**: Containers são encapsulados em pods
2. **imagePullPolicy: Never**: Para imagens locais em minikube
3. **Services abstraem IPs**: Pods são efêmeros, services persistem
4. **minikube docker-env**: Necessário para usar imagens locais
5. **Self-healing automático**: Deployment Controller monitora pods

---

## Palavras-Chave
`kubernetes` `kubectl` `minikube` `deployment` `pods` `services` `tutorial` `mlops`