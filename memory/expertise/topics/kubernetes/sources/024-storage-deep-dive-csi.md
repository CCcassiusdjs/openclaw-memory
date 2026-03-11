# Kubernetes Storage Deep Dive: PVs and CSI

**Fonte:** https://medium.com/@arjun0451/kubernetes-storage-deep-dive-persistent-volumes-and-csi-drivers-explained-6ba9f36c7ad7
**Tipo:** Technical Article
**Prioridade:** Média
**Data:** 2026-03-11

## Resumo Executivo

Guia prático sobre o lifecycle de Persistent Volumes e interação com CSI drivers, incluindo troubleshooting de problemas reais.

---

## Core Concepts

### Persistent Volumes (PVs)
- Abstrações Kubernetes para storage
- Decoupling do lifecycle de Pods
- Dynamic ou static provisioning

### Persistent Volume Claims (PVCs)
- Requisições de storage por Pods
- Vinculados a PVs por capacity e access modes

### CSI Drivers
- Plugins para provisionamento e gestão de storage
- Interface entre Kubernetes e storage backends externos

### StorageClass
- Blueprint para criação dinâmica de PVs
- Define storage type, size, access modes

---

## Workflow Detalhado

### 1. Volume Provisioning
1. Pod cria PVC especificando requisitos
2. Kubernetes usa StorageClass para provisioning
3. CSI driver comunica com storage backend
4. PV criado e vinculado ao PVC

### 2. Volume Attachment
1. Pod agendado em node
2. CSI Node Plugin anexa volume ao node
3. Volume montado no Pod

### 3. Volume Usage
- Pods executam I/O via CSI Node Plugin
- Operações passadas ao storage backend

### 4. Volume Detachment
- Volume desanexado do node ao terminar Pod
- Volume preservado para re-uso

### 5. Rescheduling
- Pod terminado no node original
- Volume desanexado pelo CSI Node Plugin
- Pod re-agendado em novo node
- Volume anexado ao novo node

---

## Real-World Insights

### CSI Driver DaemonSet Issues
- Se CSI Node Plugin DaemonSet tem problemas (ex: ImagePullBackOff)
- Pods **continuam** a usar volumes já anexados
- CSI driver não é necessário para runtime I/O

### Error Handling
- PVC permanece **Pending** se provisioning falha
- Pods dependentes não iniciam até PVC resolver

---

## FAQ Prático

### CSI Driver causa lentidão?
**Não.** Lentidão geralmente causada por:
- Storage backend issues (disks overloaded)
- StorageClass mal configurado
- Network bottlenecks (latência nodes ↔ backend)

### Se CSI driver Pods não rodam?
- **Pods existentes**: Continuam normais
- **Pods novos**: Falham ao iniciar (volume operations)

### Volume file/data missing?
- Pods encontram read/write errors
- Usar `kubectl describe pvc` e eventos

### Delete PV manualmente?
**Não recomendado.** Usar:
```bash
kubectl delete pvc <name>
```

### Dynamic resize de PV?
**Sim**, se:
- Storage backend suporta
- CSI driver suporta
- StorageClass tem `allowVolumeExpansion: true`

### Force delete Pod com mounted volume?
**Problema:** Volume pode ficar em estado attached
- Outros Pods não podem usar até detach manual

**Melhor prática:** Sempre graceful termination

### Delete PVC com Pod running?
**Problema:** Comportamento undefined
- Reclaim policy Delete pode causar data loss

**Melhor prática:** Deletar Pod antes do PVC

---

## Comandos Úteis

```bash
# Verificar eventos
kubectl get events -n <namespace>

# Descrever PVC
kubectl describe pvc -n <namespace>

# Descrever PV
kubectl describe pv

# Verificar StorageClass
kubectl get storageclass
kubectl describe storageclass <name>
```

---

## Conceitos-Chave

1. **CSI Driver Role**: Provisioning, attachment, detachment
2. **Runtime I/O**: Não requer CSI driver ativo
3. **PVC Pending**: Provisioning falhou
4. **Volume State**: Attached vs detached

---

## Próximos Passos de Estudo

- [ ] Volume Snapshots
- [ ] CSI Driver development
- [ ] Storage Performance Tuning
- [ ] Multi-attach scenarios

---

## Referências

- Article: https://medium.com/@arjun0451/kubernetes-storage-deep-dive-persistent-volumes-and-csi-drivers-explained-6ba9f36c7ad7
- CSI Spec: https://github.com/container-storage-interface/spec