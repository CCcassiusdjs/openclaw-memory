# How to Schedule GPU Workloads in Kubernetes

**Fonte:** OneUptime Blog - https://oneuptime.com/blog/post/2026-01-19-kubernetes-gpu-workload-scheduling/view
**Data:** Janeiro 2026
**Tópico:** GPU Scheduling, NVIDIA Device Plugin, MIG, Time-Slicing
**Status:** Lido

---

## Resumo Executivo

Guia abrangente para scheduling de workloads GPU em Kubernetes, cobrindo desde configuração básica (device plugin) até features avançadas (MIG, time-slicing, monitoring com DCGM).

---

## Arquitetura GPU em Kubernetes

```
┌─────────────────────────────────────────────────┐
│            Kubernetes Cluster                    │
│  ┌───────────────────────────────────────────┐  │
│  │ Control Plane                              │  │
│  │ ┌───────────┐ ┌───────────┐               │  │
│  │ │ Scheduler │ │ API Server│               │  │
│  │ └───────────┘ └───────────┘               │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │ GPU Node                                    │  │
│  │ ┌─────────┐ ┌────────────────┐           │  │
│  │ │ Kubelet │ │ Device Plugin  │           │  │
│  │ └─────────┘ └────────────────┘           │  │
│  │ ┌─────────────────────────────────────┐   │  │
│  │ │ NVIDIA Driver │ GPU 0 │ GPU 1 │     │   │  │
│  │ └─────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Componentes
| Componente | Função |
|------------|--------|
| **NVIDIA Driver** | Interface de hardware |
| **Device Plugin** | Expõe GPUs ao Kubernetes |
| **Container Runtime** | GPU passthrough |
| **Scheduler** | Aloca GPUs para pods |

---

## Pré-requisitos

### Node Setup
```bash
# Verificar driver NVIDIA
nvidia-smi

# Versão do driver
cat /proc/driver/nvidia/version

# Versão CUDA
nvcc --version
```

### NVIDIA Container Toolkit
```bash
# Adicionar repositório
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Instalar toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configurar containerd
sudo nvidia-ctk runtime configure --runtime=containerd
sudo systemctl restart containerd
```

---

## NVIDIA Device Plugin

### Instalação via Helm
```bash
helm repo add nvdp https://nvidia.github.io/k8s-device-plugin
helm repo update

helm install nvidia-device-plugin nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --create-namespace \
  --set gfd.enabled=true
```

### DaemonSet Manual
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nvidia-device-plugin-daemonset
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: nvidia-device-plugin-ds
  template:
    spec:
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
      containers:
      - name: nvidia-device-plugin-ctr
        image: nvcr.io/nvidia/k8s-device-plugin:v0.14.3
        volumeMounts:
        - name: device-plugin
          mountPath: /var/lib/kubelet/device-plugins
      nodeSelector:
        accelerator: nvidia-gpu
```

### Verificação
```bash
# Verificar pods do device plugin
kubectl get pods -n kube-system -l name=nvidia-device-plugin-ds

# Verificar GPUs anunciadas
kubectl get nodes -o json | jq '.items[].status.capacity["nvidia.com/gpu"]'

# Capacidade detalhada
kubectl describe node <gpu-node-name> | grep -A 10 "Capacity:"
```

---

## Pods com GPU

### GPU Simples
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: cuda-container
    image: nvcr.io/nvidia/cuda:12.2.0-base-ubuntu22.04
    command: ["nvidia-smi", "-L"]
    resources:
      limits:
        nvidia.com/gpu: 1
  restartPolicy: Never
```

### Multi-GPU
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-gpu-pod
spec:
  containers:
  - name: cuda-container
    image: nvcr.io/nvidia/cuda:12.2.0-base-ubuntu22.04
    command: ["sleep", "infinity"]
    resources:
      limits:
        nvidia.com/gpu: 4  # 4 GPUs
```

---

## Patterns de Deployment

### ML Training Job
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pytorch-training
spec:
  parallelism: 1
  completions: 1
  template:
    spec:
      containers:
      - name: pytorch
        image: pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
        command:
        - python
        - -c
        - |
          import torch
          print(f"CUDA available: {torch.cuda.is_available()}")
          print(f"GPU count: {torch.cuda.device_count()}")
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: 32Gi
            cpu: "8"
        volumeMounts:
        - name: shm
          mountPath: /dev/shm
      volumes:
      - name: shm
        emptyDir:
          medium: Memory
          sizeLimit: 16Gi
      restartPolicy: Never
```

### Inference Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-inference
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ml-inference
  template:
    spec:
      containers:
      - name: inference
        image: myregistry/ml-inference:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          limits:
            nvidia.com/gpu: 1
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: kubernetes.io/hostname
        whenUnsatisfiable: ScheduleAnyway
```

---

## GPU Time-Slicing

### Configuração
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: time-slicing-config
  namespace: nvidia-device-plugin
data:
  any: |-
    version: v1
    sharing:
      timeSlicing:
        renameByDefault: false
        resources:
        - name: nvidia.com/gpu
          replicas: 4  # 4 pods podem compartilhar cada GPU
```

### Deploy com Time-Slicing
```bash
helm upgrade nvidia-device-plugin nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --set config.name=time-slicing-config \
  --set gfd.enabled=true
```

---

## Multi-Instance GPU (MIG)

### Habilitar MIG Mode
```bash
# No node GPU (requer reload do driver)
sudo nvidia-smi -i 0 -mig 1
sudo reboot

# Criar instâncias MIG (A100 exemplo)
# 7 x 1g.5gb instances
sudo nvidia-smi mig -i 0 -cgi 19,19,19,19,19,19,19 -C

# Ou 2 x 3g.20gb + 1 x 1g.5gb
sudo nvidia-smi mig -i 0 -cgi 9,9,19 -C
```

### ConfigMap MIG
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mig-config
  namespace: nvidia-device-plugin
data:
  config.yaml: |
    version: v1
    flags:
      migStrategy: single  # ou "mixed"
    sharing:
      mig:
        resources:
        - name: nvidia.com/mig-1g.5gb
          rename: nvidia.com/gpu-1g5gb
        - name: nvidia.com/mig-3g.20gb
          rename: nvidia.com/gpu-3g20gb
```

### Pod com MIG
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mig-pod
spec:
  containers:
  - name: cuda-container
    image: nvcr.io/nvidia/cuda:12.2.0-base-ubuntu22.04
    command: ["nvidia-smi"]
    resources:
      limits:
        nvidia.com/mig-1g.5gb: 1
```

---

## Node Selection

### GPU Type Específico
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: a100-pod
spec:
  nodeSelector:
    nvidia.com/gpu.product: NVIDIA-A100-SXM4-40GB
  containers:
  - name: cuda
    image: nvcr.io/nvidia/cuda:12.2.0-base-ubuntu22.04
    resources:
      limits:
        nvidia.com/gpu: 1
```

### Node Affinity para GPU
```yaml
apiVersion: v1
kind: Pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nvidia.com/gpu.memory
            operator: Gt
            values: ["16000"]  # >16GB VRAM
          - key: nvidia.com/gpu.compute.major
            operator: Gt
            values: ["7"]  # Compute capability 8.0+
```

### GPU Feature Discovery Labels
```yaml
# Labels comuns disponibilizados
nvidia.com/cuda.driver.major
nvidia.com/cuda.driver.minor
nvidia.com/cuda.runtime.major
nvidia.com/cuda.runtime.minor
nvidia.com/gpu.compute.major
nvidia.com/gpu.compute.minor
nvidia.com/gpu.count
nvidia.com/gpu.family
nvidia.com/gpu.machine
nvidia.com/gpu.memory
nvidia.com/gpu.product
```

---

## Monitoramento GPU

### DCGM Exporter DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: dcgm-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: dcgm-exporter
  template:
    spec:
      containers:
      - name: dcgm-exporter
        image: nvcr.io/nvidia/k8s/dcgm-exporter:3.3.0-3.2.0-ubuntu22.04
        ports:
        - containerPort: 9400
          name: metrics
      nodeSelector:
        nvidia.com/gpu: "true"
```

### Prometheus ServiceMonitor
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: dcgm-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: dcgm-exporter
  endpoints:
  - port: metrics
    interval: 15s
```

### Alertas GPU
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: gpu-alerts
spec:
  groups:
  - name: gpu
    rules:
    - alert: GPUHighMemoryUsage
      expr: DCGM_FI_DEV_FB_USED / DCGM_FI_DEV_FB_FREE > 0.9
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "GPU memory usage is high"

    - alert: GPUHighTemperature
      expr: DCGM_FI_DEV_GPU_TEMP > 85
      for: 5m
      labels:
        severity: critical
```

---

## Best Practices

### Resource Management
```yaml
# Sempre definir memory limits junto com GPU
resources:
  limits:
    nvidia.com/gpu: 1
    memory: 32Gi
  requests:
    memory: 16Gi
    cpu: "4"
```

### Shared Memory para DL
```yaml
# DataLoader workers precisam de shared memory
volumes:
- name: shm
  emptyDir:
    medium: Memory
    sizeLimit: 16Gi
volumeMounts:
- name: shm
  mountPath: /dev/shm
```

### Taints e Tolerations
```bash
# Taint GPU nodes
kubectl taint nodes gpu-node-1 nvidia.com/gpu=true:NoSchedule
```

```yaml
# Apenas pods GPU podem schedulear
tolerations:
- key: nvidia.com/gpu
  operator: Exists
  effect: NoSchedule
```

---

## Resumo de Features

| Feature | Use Case | Complexidade |
|---------|----------|--------------|
| **Single GPU** | Basic ML workloads | Baixa |
| **Multi-GPU** | Distributed training | Média |
| **Time-Slicing** | GPU sharing para inference | Média |
| **MIG** | Memory isolation | Alta |

---

## Insights para Kubernetes

1. **Device Plugin é obrigatório**: Sem ele, Kubernetes não vê GPUs
2. **Shared memory é crítico**: PyTorch/DataLoaders precisam de /dev/shm
3. **Taints isolam GPU nodes**: Evita pods não-GPU em nodes caros
4. **DCGM para monitoramento**: Métricas essenciais de GPU
5. **MIG para A100/H100**: Isolamento forte em GPUs enterprise

---

## Palavras-Chave
`gpu-scheduling` `nvidia-device-plugin` `mig` `time-slicing` `dcgm` `gpu-monitoring` `kubernetes`