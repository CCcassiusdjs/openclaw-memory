# Deploy ML Model on Kubernetes with KServe

**Fonte:** https://devopscube.com/deploy-ml-model-kubernetes-kserve/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Guia passo-a-passo para deploy de modelos ML em Kubernetes usando KServe, cobrindo instalação, configuração e inferência.

## O que é KServe?

KServe é uma ferramenta open-source para serving de modelos ML em Kubernetes, simplificando o deploy de modelos para inferência.

### Modos de Deploy
| Modo | Descrição | Uso |
|------|-----------|-----|
| **Knative** | Default, requer Knative components | Advanced setups |
| **RawDeployment** | Simple setup | Produção simples |

Este guia usa **RawDeployment mode**.

## Workflow KServe

```
User → InferenceService → Controller → Deployment + Service + HPA
                                              ↓
                                      Model Server Pod
                                              ↓
                                      PVC/Storage → model.pkl
```

### Fluxo
1. Controller monitora InferenceService resources
2. Cria: Deployment, Service, HPA automaticamente
3. Pod pulls model server image (sklearnserver)
4. Pod acessa model.pkl via PVC
5. Endpoint exposto para predictions

## Storage Options

| Opção | Descrição |
|-------|-----------|
| **Object Storage** | AWS S3, Azure Blob Storage |
| **Container Image** | Modelo empacotado em imagem |
| **Persistent Volume** | PVC no cluster (usado neste guia) |

## Setup

### Pré-requisitos
- Kubernetes Cluster
- kubectl
- Docker
- Helm

### Instalação

```bash
# 1. Cert Manager (TLS)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.0/cert-manager.yaml

# 2. KServe CRDs
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version v0.16.0 -n kserve --create-namespace

# 3. KServe Controller
helm install kserve oci://ghcr.io/kserve/charts/kserve \
  --version v0.16.0 \
  --set kserve.controller.deploymentMode=Standard \
  -n kserve
```

### Verificação
```bash
kubectl get crds | grep kserve
kubectl get po -n kserve
# NAME                                    READY   STATUS
# kserve-controller-manager-xxx           2/2     Running
```

## Deploy do Modelo

### Estrutura do Projeto
```
predictor-model/
├── Dockerfile
├── inference.yaml
├── job.yaml
└── model/
    └── model.pkl
```

### Modelo Exemplo
- scikit-learn text classification
- Labels: 0 (Animals), 1 (Birds), 2 (Plants)
- Input: word → Output: category

### Dockerfile
```dockerfile
FROM alpine:latest
WORKDIR /app
COPY model/ ./model/
```

### Job para Copiar Modelo
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: predictor-model-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: batch/v1
kind: Job
metadata:
  name: predictor-model-copy-job
spec:
  ttlSecondsAfterFinished: 10
  backoffLimit: 1
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: model-writer
        image: devopscube/predictor-model:1.0
        command: ["/bin/sh", "-c"]
        args:
        - |
          cp -r /app/model/* /mnt/models/;
        volumeMounts:
        - name: model-storage
          mountPath: /mnt/models
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: predictor-model-pvc
```

### InferenceService
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: model
spec:
  predictor:
    sklearn:
      storageUri: pvc://predictor-model-pvc
      resources:
        requests:
          cpu: 500m
          memory: 1Gi
```

## Testando Inferência

### Port Forward
```bash
kubectl port-forward service/model-predictor 8000:80
```

### Request
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      "sparrow",
      "elephant",
      "sunflower"
    ]
  }' \
  "http://localhost:8000/v1/models/model:predict"
```

### Response
```json
{
  "predictions": [1, 0, 2]
}
// 0=Animal, 1=Bird, 2=Plant
```

## Endpoint Interno

```
http://model-predictor.default.svc.cluster.local/v1/models/model:predict

- model-predictor.default.svc.cluster.local → DNS interno
- v1/models/ → API version
- model → Nome do InferenceService
- predict → Endpoint padrão
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Pod Pending | Verificar PVC, storage class, node resources |
| PVC não bound | Verificar storage class e provisioning |
| Memory insuficiente | Garantir 1GB+ disponível |

## Frameworks Suportados

- scikit-learn
- TensorFlow
- PyTorch
- XGBoost
- ONNX

## Insights

- KServe simplifica deploy de modelos em K8s
- RawDeployment é mais simples para começar
- PVC storage funciona bem para modelos pequenos
- Para produção, usar object storage (S3, Azure Blob)
- KServe cria automaticamente Deployment, Service, HPA
- Model server images são pré-built por framework