# Persistent Volumes

**Source:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/
**Type:** Official Documentation
**Category:** Storage/StatefulSets
**Read:** 2026-03-11

---

## Resumo

### Conceitos Fundamentais

| Objeto | O que é | Analogia |
|--------|---------|----------|
| **PersistentVolume (PV)** | Storage no cluster | Como um Node |
| **PersistentVolumeClaim (PVC)** | Request de storage pelo usuário | Como um Pod |
| **StorageClass** | Template para provisionamento dinâmico | Como uma "classe" de storage |

### Lifecycle PV/PVC

```
Provisioning → Binding → Using → Reclaiming
    │             │         │         │
    ├─ Static     ├─ 1:1    ├─ Pod    ├─ Retain
    └─ Dynamic    └─ binds  └─ mount  ├─ Delete
                                        └─ Recycle (deprecated)
```

---

## Provisioning

### Static Provisioning
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-volume
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: slow
  hostPath:
    path: /tmp/data
```

### Dynamic Provisioning
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-claim
spec:
  storageClassName: fast  # StorageClass necessária
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

---

## Access Modes

| Modo | Sigla | Descrição |
|------|-------|-----------|
| **ReadWriteOnce** | RWO | Um node pode montar R/W |
| **ReadOnlyMany** | ROX | Múltiplos nodes podem montar R/O |
| **ReadWriteMany** | RWX | Múltiplos nodes podem montar R/W |
| **ReadWriteOncePod** | RWOP | Apenas um Pod pode montar R/W |

---

## Reclaim Policies

| Policy | Comportamento |
|--------|---------------|
| **Retain** | PV retido, dados preservados, reclamação manual |
| **Delete** | PV e storage asset deletados (default para dynamic) |
| **Recycle** | DEPRECATED - rm -rf e disponibiliza novamente |

---

## Storage Object in Use Protection

- **Finalizer**: `kubernetes.io/pvc-protection` / `kubernetes.io/pv-protection`
- **Propósito**: Impede deleção de PVC/PV em uso
- **Status**: Terminating até liberar

---

## Binding

### Como Funciona
1. Control loop vê novo PVC
2. Encontra PV compatível (se existir)
3. Faz binding 1:1 via ClaimRef
4. PVC permanece unbound se não encontrar match

### Pre-binding (Reserva)
```yaml
# PVC específico para um PV
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
spec:
  volumeName: foo-pv  # Bind específico
```

```yaml
# PV reservado para um PVC
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  claimRef:
    name: foo-pvc
    namespace: foo
```

---

## PV Deletion Protection Finalizer

| Finalizer | Quando Usado |
|-----------|--------------|
| `kubernetes.io/pv-protection` | Todos os PVs |
| `kubernetes.io/pv-controller` | In-tree dynamic provisioned |
| `external-provisioner.volume.kubernetes.io/finalizer` | CSI volumes |

**Propósito**: Garante que o storage backend é deletado antes do PV

---

## Conceitos-Chave

1. **PV é cluster resource**: Independente de Pod lifecycle
2. **PVC é namespace-scoped**: Request de usuário
3. **Binding é exclusivo**: 1:1 PV-PVC
4. **StorageClass para dynamic provisioning**: Default StorageClass admission controller
5. **Retain vs Delete**: Importante para dados críticos
6. **VolumeMode**: Filesystem (default) ou Block

---

## Diagrama de Relacionamento

```
┌─────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                          │
│                                                             │
│  ┌──────────────────┐     ┌──────────────────┐              │
│  │  StorageClass    │────▶│ Dynamic Prov.   │              │
│  │  (template)      │     │ (CSI driver)    │              │
│  └──────────────────┘     └──────────────────┘              │
│         │                         │                         │
│         ▼                         ▼                         │
│  ┌──────────────────┐     ┌──────────────────┐              │
│  │ PersistentVolume │◀───▶│ PersistentVolume │              │
│  │ (PV) - cluster   │     │ (dinamicamente   │              │
│  │     resource     │     │  provisionado)   │              │
│  └──────────────────┘     └──────────────────┘              │
│         ▲                         ▲                         │
│         │                         │                         │
│  ┌──────┴───────────────┐         │                         │
│  │ PersistentVolumeClaim│─────────┘                          │
│  │ (PVC) - namespace    │                                   │
│  └──────────────────────┘                                   │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────┐                                   │
│  │        Pod           │                                   │
│  │ (consome PVC)        │                                   │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Próximos Passos
- Estudar StatefulSets
- Ver CSI drivers específicos
- Entender volume expansion