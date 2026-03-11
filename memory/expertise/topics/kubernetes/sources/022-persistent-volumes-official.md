# Kubernetes Persistent Volumes (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/storage/persistent-volumes/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

PersistentVolume (PV) e PersistentVolumeClaim (PVC) são abstrações Kubernetes que separam o provisionamento de storage do consumo de storage, permitindo que stateful workloads persistam dados além do lifecycle de um Pod.

---

## Conceitos Fundamentais

### PersistentVolume (PV)
- Recurso de storage no cluster (como nodes são recursos)
- Provisionado por admin ou dinamicamente via StorageClass
- Lifecycle independente de qualquer Pod
- Plugins como Volumes, mas com lifecycle próprio

### PersistentVolumeClaim (PVC)
- Requisição de storage por usuário
- Similar a Pod (Pods consomem node resources, PVCs consomem PV resources)
- Pode especificar tamanho e access modes

---

## Lifecycle de Volume e Claim

### 1. Provisioning

**Estático:**
- Admin cria PVs manualmente
- Detalhes do storage real carregados
- Disponíveis para consumo

**Dinâmico:**
- StorageClass-based provisioning
- Cluster provisiona automaticamente para PVC
- Requer DefaultStorageClass admission controller

### 2. Binding
- Control loop observa novos PVCs
- Encontra PV correspondente (se possível)
- Vincula PVC ao PV (one-to-one mapping)
- Se não encontrar match, PVC permanece unbound

### 3. Using
- Pods usam claims como volumes
- Cluster monta o volume vinculado ao claim
- Access mode selecionado pelo usuário

### 4. Storage Object in Use Protection
- PVC em uso por Pod não é removido imediatamente
- Status: Terminating com finalizer kubernetes.io/pvc-protection
- PV vinculado também protegido

### 5. Reclaiming

**Políticas:**
- **Retain**: Reclamação manual (volume preservado)
- **Delete**: Remove PV e storage asset (padrão para dinâmico)
- **Recycle**: DEPRECATED (rm -rf básico)

---

## Volume Expansion

**Recursos suportados:**
- CSI volumes (incluindo CSI migrated)
- FlexVolume (deprecated)
- PortworxVolume (deprecated)

**Requisitos:**
- StorageClass com allowVolumeExpansion: true
- Filesystem: XFS, Ext3, Ext4

**Processo:**
1. Editar PVC com novo tamanho
2. Volume existente é redimensionado
3. Novo PV não é criado

**In-use PVC resize:**
- Resize automático quando Pod está usando
- File system expansion: online ou no restart

---

## Tipos de PersistentVolume

### Suportados (v1.35)
- **CSI** - Container Storage Interface (recomendado)
- **FC** - Fibre Channel
- **hostPath** - Single node testing only
- **iSCSI** - SCSI over IP
- **local** - Local devices
- **NFS** - Network File System

### Deprecados (usar CSI drivers)
- awsElasticBlockStore
- azureDisk, azureFile
- cinder (OpenStack)
- gcePersistentDisk
- vsphereVolume
- portworxVolume
- flexVolume

### Removidos
- cephfs, rbd (v1.31)
- glusterfs (v1.26)
- flocker, quobyte, storageos (v1.25)

---

## Access Modes

| Mode | Abbr | Description |
|------|------|-------------|
| ReadWriteOnce | RWO | Single node read-write |
| ReadOnlyMany | ROX | Many nodes read-only |
| ReadWriteMany | RWX | Many nodes read-write |
| ReadWriteOncePod | RWOP | Single Pod read-write |

**Notas:**
- Volume montado em apenas UM access mode por vez
- Access modes não garantem write protection
- RWOP é constraint (só um Pod)

---

## Volume Mode

**Filesystem (padrão):**
- Montado como diretório no Pod
- Filesystem criado se vazio

**Block:**
- Raw block device
- Sem filesystem
- Maior performance
- Aplicação deve lidar com block device

---

## Node Affinity

- Constraints sobre quais nodes podem acessar o PV
- Importante para **local** volumes
- Pods só agendados em nodes compatíveis

---

## Conceitos-Chave

1. **PV vs PVC**: Abstração storage (PV) vs requisição (PVC)
2. **StorageClass**: Blueprint para dynamic provisioning
3. **Reclaim Policy**: O que acontece quando PVC é deletado
4. **Access Mode**: Como o volume pode ser montado
5. **Volume Mode**: Filesystem vs Block

---

## Exemplos Práticos

### PV Estático
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: slow
  nfs:
    path: /tmp
    server: 172.17.0.2
```

### PVC Dinâmico
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc
spec:
  storageClassName: fast
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

---

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| PVC Pending | StorageClass incorreto | Verificar StorageClass name |
| PVC Pending | Capacidade insuficiente | Adicionar PVs ou configurar dynamic |
| Mount fail | Access mode incompatível | Verificar access modes suportados |
| Resize fail | Driver não suporta | Verificar CSI driver docs |

---

## Próximos Passos de Estudo

- [ ] CSI Driver desenvolvimento
- [ ] Volume Snapshots
- [ ] Volume Cloning
- [ ] Raw Block Volumes
- [ ] Local Persistent Volumes

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- Storage Classes: https://kubernetes.io/docs/concepts/storage/storage-classes/
- CSI Spec: https://github.com/container-storage-interface/spec