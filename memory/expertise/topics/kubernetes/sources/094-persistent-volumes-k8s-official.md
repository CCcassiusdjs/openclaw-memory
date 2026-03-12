# Persistent Volumes - Kubernetes Official

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/storage/persistent-volumes/
**Data:** Janeiro 2026
**Tópico:** PersistentVolumes, PersistentVolumeClaims, StorageClasses, Dynamic Provisioning
**Status:** Lido

---

## Resumo Executivo

Documentação oficial de PersistentVolumes, cobrindo PV, PVC, lifecycle, provisioning, binding, reclaiming e access modes.

---

## Introdução

### Conceitos
- **PersistentVolume (PV)**: Pedaço de storage no cluster provisionado por admin ou dinamicamente via StorageClasses
- **PersistentVolumeClaim (PVC)**: Requisição de storage por usuário
- **Lifecycle independente**: PVs sobrevivem a Pods

### Analogia
- Pods consomem recursos de Node
- PVCs consomem recursos de PV
- Similar a CPU/Memory requests, mas para storage

---

## Lifecycle de Volume e Claim

### Provisioning

#### Static
- Admin cria PVs manualmente
- PVs existem na API disponíveis para uso

#### Dynamic
- Cluster provisiona volume automaticamente para PVC
- Baseado em StorageClass
- PVC deve especificar StorageClass
- PVC com StorageClass "" desabilita dynamic provisioning

### Binding
- Control loop observa PVCs e encontra PVs matching
- PVC sem PV matching permanece unbound
- Binding é one-to-one (PVC ↔ PV)
- PVC recebe pelo menos o que pediu (pode receber mais)

### Using
- Pods usam PVC como volume
- Cluster monta PV no Pod
- User especifica access mode desejado

### Storage Object in Use Protection
- PVC em uso por Pod não é deletado imediatamente
- PV bound a PVC não é deletado imediatamente
- Finalizer `kubernetes.io/pvc-protection` e `kubernetes.io/pv-protection`
- Status `Terminating` até não estar mais em uso

### Reclaiming

#### Retain
- Manual reclamation
- PV existe mas está "released"
- Admin deve limpar dados manualmente
- Passos: deletar PV, limpar dados, recriar PV

#### Delete
- Deleta PV e storage asset associado
- Default para StorageClass
- Dinamicamente provisionados herdam reclaim policy do StorageClass

#### Recycle (Deprecated)
- Executa `rm -rf /thevolume/*`
- Torna volume disponível novamente
- Use dynamic provisioning em vez disso

---

## Access Modes

### Modos Suportados

| Modo | Abreviação | Descrição |
|------|------------|-----------|
| **ReadWriteOnce** | RWO | Um node pode montar read/write |
| **ReadOnlyMany** | ROX | Múltiplos nodes podem montar read-only |
| **ReadWriteMany** | RWX | Múltiplos nodes podem montar read/write |
| **ReadWriteOncePod** | RWOP | Um Pod pode montar read/write |

### Observação
- Modos dependem do volume plugin
- Nem todos plugins suportam todos os modos
- Verificar documentação do storage provider

---

## Volume Modes

### Filesystem (Default)
- Volume montado como filesystem
- Diretório no Pod

### Block
- Volume montado como dispositivo de bloco
- Útil para databases, storage próprio

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-pvc
spec:
  volumeMode: Block
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

---

## Classes de Storage

### StorageClass
- Define tipo de storage (fast, slow, etc.)
- Provisioner dinâmico
- Parâmetros específicos do provider

### VolumeAttributesClass (v1.29+)
- Permite modificar atributos do volume
- Expande, muda IOPS, etc.

---

## Exemplos

### PersistentVolume Estático
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    server: 192.168.1.100
    path: /export/data
```

### PersistentVolumeClaim
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-app
spec:
  accessModes:
  - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 5Gi
  storageClassName: fast-ssd
```

### Pod usando PVC
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: pvc-app
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: data
      mountPath: /data
```

---

## Pré-binding

### Reservar PV Específico
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
spec:
  storageClassName: ""
  volumeName: foo-pv  # Pre-bind
```

### Reservar PV para PVC
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo
```

---

## Finalizers de PV

### kubernetes.io/pv-protection
- Impede deleção de PV enquanto está bound

### kubernetes.io/pv-controller
- Para in-tree volumes dinamicamente provisionados
- Garante deleção do storage backend antes do PV object

### external-provisioner.volume.kubernetes.io/finalizer
- Para CSI volumes
- Garante deleção do storage backend antes do PV object

---

## Insights para Kubernetes

1. **PV lifecycle independente**: Sobrevive a Pods
2. **Dynamic provisioning via StorageClass**: Automatiza criação
3. **Reclaim policy importa**: Delete vs Retain vs Recycle
4. **Access modes dependem do plugin**: Verificar provider
5. **Finalizers protegem**: PV/PVC não são deletados em uso

---

## Palavras-Chave
`persistent-volumes` `pvc` `storage` `dynamic-provisioning` `storageclass` `kubernetes`