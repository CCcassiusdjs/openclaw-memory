# Kubernetes Garbage Collection (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/architecture/garbage-collection/
**Tipo:** Official Documentation
**Prioridade:** Média
**Data:** 2026-03-11

## Resumo Executivo

Garbage collection é o mecanismo do Kubernetes para limpar recursos não utilizados automaticamente, incluindo Pods terminados, containers antigos e objetos órfãos.

---

## O que é Garbage Collection?

### Definição
- Mecanismo de limpeza automática
- Gerencia lifecycle de recursos
- Remove objetos sem owner references
- Limpa containers e imagens não utilizados

### Recursos Gerenciados
- Terminated Pods
- Completed Jobs
- Objects sem owner references
- Unused containers e images
- Dynamically provisioned PVs
- Expired CSRs
- Node Lease objects

---

## Owners and Dependents

### Conceito
Objetos Kubernetes podem ter **owner references** que estabelecem relações de dependência:

```yaml
metadata:
  ownerReferences:
  - apiVersion: apps/v1
    kind: ReplicaSet
    name: my-rs
    uid: abc-123
    blockOwnerDeletion: true
```

### Comportamento
- Dependents são deletados quando owner é deletado
- Labels vs Owner References: Labels para seleção, Owner References para ownership

### Cross-Namespace References
- **NÃO permitidas** por design
- Namespaced dependents podem ter cluster-scoped owners
- Namespaced owners devem estar no mesmo namespace do dependent

---

## Cascading Deletion

### Tipos

#### Foreground Cascading Deletion
1. Owner entra em "deletion in progress"
2. `metadata.deletionTimestamp` setado
3. `metadata.finalizers` setado para `foregroundDeletion`
4. Controller deleta dependents primeiro
5. Controller deleta owner

```bash
kubectl delete rs my-rs --cascade=foreground
```

#### Background Cascading Deletion (Default)
1. API server deleta owner imediatamente
2. Garbage collector deleta dependents em background

```bash
kubectl delete rs my-rs --cascade=background
```

#### Orphan Deletion
1. Owner deletado
2. Dependents mantidos (órfãos)

```bash
kubectl delete rs my-rs --cascade=orphan
```

---

## Finalizers

### O que são
- Mecanismo para prevenir deleção até cleanup completar
- Adicionados em `metadata.finalizers`

### Exemplos
- `foregroundDeletion`: Aguarda dependents
- `kubernetes.io/pv-protection`: Aguarda PVC release
- `kubernetes.io/pvc-protection`: Aguarda Pod unmount

---

## Container e Image Garbage Collection

### Kubelet GC
- **Containers**: A cada 1 minuto
- **Images**: A cada 5 minutos

### Image Manager
Gerencia lifecycle de imagens com thresholds de disco:

```yaml
# KubeletConfiguration
imageMinimumGCAge: 2m
imageMaximumGCAge: 12h
imageGCHighThresholdPercent: 85
imageGCLowThresholdPercent: 80
```

### Comportamento
1. Quando disco > HighThresholdPercent: GC trigger
2. Deleta imagens mais antigas primeiro
3. Para quando disco < LowThresholdPercent

### Maximum GC Age
```yaml
imageMaximumGCAge: 12h45m  # Máximo tempo sem uso
```

⚠️ **Nota:** Reset no restart do kubelet

---

## Container Garbage Collection

### Parâmetros
| Parâmetro | Descrição |
|-----------|-----------|
| `MinAge` | Idade mínima para GC |
| `MaxPerPodContainer` | Max containers mortos por Pod |
| `MaxContainers` | Max containers mortos no cluster |

### Comportamento
1. Remove containers unidentified/deleted
2. Começa pelos mais antigos
3. Ajusta conflitos entre MaxPerPodContainer e MaxContainers

---

## TTL After Finished (Jobs)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
spec:
  ttlSecondsAfterFinished: 100
```

- Remove Jobs completados após TTL
- Reduz necessidade de GC manual

---

## Configurando Garbage Collection

### Cascading Deletion
```yaml
# No owner object
metadata:
  finalizers:
  - foregroundDeletion
```

### Container/Image GC
```yaml
# KubeletConfiguration
evictionSoft:
  memory.available: "500Mi"
  nodefs.available: "10%"
evictionHard:
  memory.available: "200Mi"
  nodefs.available: "5%"
```

---

## Conceitos-Chave

1. **Owner References**: Relação de dependência
2. **Cascading Deletion**: Foreground, Background, Orphan
3. **Finalizers**: Previnem deleção até cleanup
4. **Kubelet GC**: Containers e imagens
5. **TTL Controller**: Jobs cleanup

---

## Best Practices

1. **Não usar ferramentas externas**: Podem quebrar kubelet GC
2. **Configurar TTL**: Para Jobs
3. **Monitorar disco**: Para image GC
4. **Usar owner references**: Para cascade correto
5. **Finalizers**: Para cleanup customizado

---

## Próximos Passos de Estudo

- [ ] Custom Finalizers
- [ ] Eviction API
- [ ] Resource Quotas e GC
- [ ] Third-party GC controllers

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/architecture/garbage-collection/
- Owners and Dependents: https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/
- Finalizers: https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
- TTL After Finished: https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/