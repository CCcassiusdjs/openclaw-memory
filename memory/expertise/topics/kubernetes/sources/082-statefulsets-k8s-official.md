# StatefulSets - Kubernetes Official Documentation

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
**Data:** Janeiro 2026
**Tópico:** StatefulSets, Persistent Storage, Network Identity
**Status:** Lido

---

## Resumo Executivo

Documentação oficial de StatefulSets, cobrindo identidade estável, armazenamento persistente, deployment ordenado, e diferenças críticas em relação a Deployments.

---

## O que é StatefulSet

### Definição
- **Workload API**: Gerencia aplicações stateful
- **Pods com identidade**: Cada Pod tem identidade persistente
- **Não intercambiáveis**: Pods são criados do mesmo spec, mas não são idênticos
- **Reagendamento**: Mantém identidade através de reschedules

### Diferença de Deployments
| Feature | Deployment | StatefulSet |
|---------|------------|-------------|
| **Pod Identity** | Random, ephemeral | Stable, persistent |
| **Storage** | Shared or ephemeral | Per-pod persistent |
| **Network** | Random DNS | Stable hostname |
| **Ordering** | Parallel | Sequential (optional) |

---

## Quando Usar

StatefulSets são valiosos para aplicações que requerem:
- Network identifiers estáveis e únicos
- Armazenamento persistente estável
- Deployment e scaling ordenados
- Rolling updates ordenados e automatizados

**Nota:** Se a aplicação não requer identificadores estáveis ou deployment ordenado, use Deployment ou ReplicaSet.

---

## Limitações

### Storage
- Deve ser provisionado por PersistentVolume Provisioner baseado no storage class
- Ou pre-provisionado por admin
- Deletar/scalar StatefulSet não deleta volumes associados (data safety)

### Service
- Requer Headless Service para network identity
- Usuário é responsável por criar o Service

### Termination
- Não garante terminação ordenada quando deletado
- Para terminação graciosa: scale down para 0 antes de deletar

### Rolling Updates
- Com `OrderedReady` (padrão): pode chegar em estado quebrado
- Pode requerer intervenção manual

---

## Componentes

### Headless Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None  # Headless
  selector:
    app: nginx
```

### StatefulSet Manifest
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"  # Headless Service
  replicas: 3
  minReadySeconds: 10
  template:
    metadata:
      labels:
        app: nginx
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: registry.k8s.io/nginx-slim:0.24
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

---

## Pod Identity

### Ordinal Index
- StatefulSet com N réplicas: Pods recebem ordinais de 0 a N-1
- Padrão: ordinais começam em 0
- Label: `apps.kubernetes.io/pod-index`

### Start Ordinal (v1.31+)
- `.spec.ordinals.start`: Define ordinal inicial
- Exemplo: `start: 1` → Pods: 1, 2, 3

### Network Identity
- **Hostname**: `$(statefulset name)-$(ordinal)`
- **DNS**: `$(podname).$(governing service domain)`
- **Exemplo**: web-0.nginx.default.svc.cluster.local

### DNS Components
| Cluster Domain | Service (ns/name) | StatefulSet | StatefulSet Domain | Pod DNS |
|----------------|-------------------|-------------|-------------------|---------|
| cluster.local | default/nginx | default/web | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local |

---

## Storage

### volumeClaimTemplates
- Cada Pod recebe um PersistentVolumeClaim por template
- PVCs não são deletados quando Pods ou StatefulSet são deletados
- Deve ser feito manualmente se necessário

### StorageClass
- Pode especificar StorageClass
- Se não especificado: usa default StorageClass
- Escolher baseado em workload:
  - **High IOPS**: Databases (gp3, io2)
  - **High Throughput**: Logs, analytics (st1, sc1)

---

## Deployment Guarantees

### Ordering
- **Deploy**: Pods criados sequencialmente (0 → N-1)
- **Delete**: Pods terminados em reverso (N-1 → 0)
- **Scaling**: Predecessor deve estar Running/Ready antes do próximo

### Example
1. web-0 criado, aguarda Running/Ready
2. web-1 criado, aguarda Running/Ready
3. web-2 criado, aguarda Running/Ready

Se web-0 falhar após web-1 estar Ready:
- web-2 não é lançado até web-0 ser re-launchado e ficar Ready

---

## Pod Management Policies

### OrderedReady (Default)
- Implementa ordering guarantees
- Deploy/delete sequencial

### Parallel
- Launch/terminate Pods em paralelo
- Não espera Ready/terminated antes de próximo
- Útil para aplicações que não precisam de ordem
- Speed up updates quando `maxUnavailable > 1`

---

## Update Strategies

### OnDelete
- Controller não atualiza Pods automaticamente
- Usuário deve deletar Pods manualmente
- Novos Pods refletem spec atualizado

### RollingUpdate
- Controller atualiza Pods automaticamente
- Ordem reversa (N-1 → 0)
- Partitions: Pode especificar qual partição atualizar

```yaml
updateStrategy:
  type: RollingUpdate
  rollingUpdate:
    partition: 2  # Apenas Pods com ordinal >= partition são atualizados
```

---

## Minimum Ready Seconds

- `.spec.minReadySeconds`: Segundos para considerar Pod disponível
- Padrão: 0 (imediatamente Ready)
- Usado para progression de rollout
- Importante para Rolling Updates

---

## Best Practices

### Headless Service
```yaml
# Obrigatório para StatefulSet
clusterIP: None
```

### Termination Grace Period
```yaml
# Nunca usar 0
terminationGracePeriodSeconds: 10
```

### Pod Anti-Affinity
```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values: [myapp]
      topologyKey: kubernetes.io/hostname
```

### StorageClass Selection
- **High IOPS**: Databases com random read/write
- **High Throughput**: Log aggregation, analytics
- **Consider**: Latência, IOPS, throughput para workload

---

## Insights para Kubernetes

1. **Headless Service é obrigatório**: Para network identity estável
2. **Volumes não são auto-deletados**: Data safety first
3. **Parallel acelera updates**: Para apps que não precisam de ordem
4. **minReadySeconds**: Importante para rollout stability
5. **Partition updates**: Útil para canary/blue-green

---

## Palavras-Chave
`statefulsets` `persistent-storage` `network-identity` `workload-api` `ordered-deployment` `volumeclaimtemplates`