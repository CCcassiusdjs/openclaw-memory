# PV vs StatefulSets Comparison

**Fonte:** https://medium.com/@platform.engineers/kubernetes-storage-comparing-persistent-volumes-and-statefulsets-fe103be137d2
**Tipo:** Artigo
**Data:** 2026-03-12

---

## Resumo

Comparação entre Persistent Volumes (PVs) e StatefulSets no Kubernetes. Explica quando usar cada um para gerenciamento de storage.

---

## Persistent Volumes (PVs)

Recurso de storage que pode ser provisionado independentemente dos Pods.

### Características
- Backed por dispositivos físicos (HDD, SSD, NAS)
- Dados persistem mesmo se Pod for deletado
- Cluster-wide resource
- Gerenciado por cluster administrator

### Exemplo
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  local:
    path: /mnt/data
  storageClassName: local-storage
```

---

## StatefulSets

Workload para gerenciar aplicações stateful.

### Características
- Cada réplica tem identidade única
- Dados persistem across deployments
- Namespace-scoped
- Usa PersistentVolumeClaims (PVCs) para storage

### Exemplo
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-statefulset
spec:
  selector:
    matchLabels:
      app: my-app
  serviceName: my-service
  replicas: 3
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-container
        image: my-image
        volumeMounts:
        - name: data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 5Gi
```

---

## Key Differences

| Aspecto | Persistent Volumes | StatefulSets |
|---------|-------------------|--------------|
| **Purpose** | Manage storage resources | Manage stateful applications |
| **Scope** | Cluster-wide | Namespace-scoped |
| **Management** | Cluster admin | Uses PVCs to request storage |
| **Scaling** | Not inherently supported | Supports scaling with unique identity |
| **Data Persistence** | Yes | Yes + across deployments |

---

## Use Cases

### Database Storage
- **PV:** Database not part of stateful application
- **StatefulSet:** Database part of stateful application (replicated)

### File Storage
- **PV:** Files not specific to particular application
- **StatefulSet:** Files specific to particular application

---

## Comparison Table

```
┌─────────────────────────────────────────────────────┐
│            Persistent Volume                        │
│  ┌─────────────────────────────────────────────┐   │
│  │  Storage Resource (cluster-wide)            │   │
│  │  - Managed by admin                         │   │
│  │  - Independent of Pods                       │   │
│  │  - No identity concept                       │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│            StatefulSet                              │
│  ┌─────────────────────────────────────────────┐   │
│  │  Workload Controller (namespace-scoped)    │   │
│  │  - Uses PVCs for storage                    │   │
│  │  - Unique identity per replica              │   │
│  │  - Stable network identity                  │   │
│  │  - Ordered deployment/scaling               │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| PersistentVolume | Storage resource cluster-wide |
| PersistentVolumeClaim | Request for storage by Pod |
| StatefulSet | Controller para apps stateful |
| volumeClaimTemplates | PVCs criados automaticamente pelo StatefulSet |
| Unique Identity | Cada Pod tem nome estável (pod-0, pod-1, etc.) |

---

## Referências

- Kubernetes PV Docs: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- StatefulSet Docs: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/