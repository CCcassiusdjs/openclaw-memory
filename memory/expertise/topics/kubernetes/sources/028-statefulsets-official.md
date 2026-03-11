# Kubernetes StatefulSets (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

StatefulSets gerenciam aplicações stateful, fornecendo identidade estável, armazenamento persistente e ordenamento de deployment.

---

## O que é StatefulSet?

### Definição
- Workload API object para aplicações stateful
- Gerencia deployment e scaling de um conjunto de Pods
- Fornece garantias de ordenação e unicidade
- Mantém identidade persistente para cada Pod

### Diferença de Deployments

| Característica | Deployment | StatefulSet |
|---------------|-----------|-------------|
| Identidade dos Pods | Intercambiáveis | Persistente |
| Ordem de criação | Paralela | Sequencial (0→N-1) |
| Ordem de exclusão | Paralela | Reversa (N-1→0) |
| Storage | Efêmero por padrão | Persistente |
| Network identity | DNS do Service | DNS individual |

---

## Casos de Uso

StatefulSets são valiosos para aplicações que requerem:
- Identificadores de rede estáveis e únicos
- Armazenamento persistente estável
- Deployment e scaling ordenados
- Rolling updates ordenados e automatizados

**Use Deployment/ReplicaSet** para workloads stateless.

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

### StatefulSet
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"
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
- Pods numerados de 0 a N-1
- Label `apps.kubernetes.io/pod-index` adicionado
- Nome: `$(statefulset name)-$(ordinal)`
- Exemplo: web-0, web-1, web-2

### Stable Network ID
- Hostname: `$(statefulset name)-$(ordinal)`
- Domínio: `$(service name).$(namespace).svc.cluster.local`
- DNS completo: `$(podname).$(governing service domain)`
- Exemplo: `web-0.nginx.default.svc.cluster.local`

### Stable Storage
- Cada Pod recebe um PVC do volumeClaimTemplate
- PVC não é deletado quando Pod é deletado
- Volume persiste entre reschedules

---

## Deployment e Scaling Guarantees

### Ordinal Ready
- Pods criados sequencialmente: 0 → N-1
- Cada Pod deve estar Running and Ready antes do próximo
- minReadySeconds considerado se definido

### Exemplo
1. web-0 criado e aguarda Ready
2. web-1 criado após web-0 Ready
3. web-2 criado após web-1 Ready

### Scaling Down
- Pods terminados em ordem reversa: N-1 → 0
- Cada Pod deve terminar antes do próximo

---

## Pod Management Policies

### OrderedReady (Default)
- Ordem estrita: 0 → N-1 para criação
- N-1 → 0 para exclusão
- Garantias de ordenamento

### Parallel
- Todos Pods criados/terminados em paralelo
- Não espera Ready ou terminated
- Útil para aplicações que não requerem ordem

---

## Update Strategies

### OnDelete
- Não atualiza Pods automaticamente
- Requer deleção manual
- Útil para updates controlados

### RollingUpdate (Default)
- Atualiza Pods automaticamente
- Ordem: N-1 → 0 (maior ordinal primeiro)
- Aguarda Pod Ready antes do próximo

### Partitioned Rolling Updates
```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 2
```
- Apenas Pods com ordinal ≥ partition são atualizados
- Útil para canary deployments
- Rollouts em fases

### Maximum Unavailable
```yaml
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 2
```
- Controla quantos Pods podem estar indisponíveis
- Padrão: 1

---

## PersistentVolumeClaim Retention

```yaml
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain  # ou Delete
    whenScaled: Delete   # ou Retain
```

| Política | Comportamento |
|----------|--------------|
| **Retain** (default) | PVCs não são deletados |
| **Delete** | PVCs são deletados após Pod terminar |

---

## Revision History

```yaml
spec:
  revisionHistoryLimit: 5  # Manter últimas 5 revisões
```

### Comandos Úteis
```bash
# Ver histórico
kubectl rollout history statefulset/webapp

# Rollback para revisão específica
kubectl rollout undo statefulset/webapp --to-revision=3

# Listar ControllerRevisions
kubectl get controllerrevisions -l app.kubernetes.io/name=webapp
```

---

## Limitações

1. **Storage**: Deve ser provisionado por PV Provisioner ou pre-provisioned
2. **Deletion**: Deletar StatefulSet não deleta PVCs
3. **Headless Service**: Obrigatório para network identity
4. **Termination**: Sem garantias de termination ordenada
5. **Rolling Updates**: Estado quebrado pode requerer intervenção manual

---

## Forced Rollback

Quando um rollout falha e o StatefulSet fica em estado quebrado:

1. Reverter o Pod template para configuração boa
2. Deletar Pods que tentaram rodar com configuração ruim
3. StatefulSet recriará Pods com configuração revertida

---

## Conceitos-Chave

1. **Sticky Identity**: Identidade persistente entre reschedules
2. **Stable Storage**: PVC por Pod, persiste após Pod deletion
3. **Ordered Deployment**: Sequencial, ordinal-based
4. **Headless Service**: DNS individual por Pod
5. **volumeClaimTemplate**: Provisionamento automático de PVCs

---

## Próximos Passos de Estudo

- [ ] StatefulSet com Service Mesh
- [ ] StatefulSet com HorizontalPodAutoscaler
- [ ] Backup e restore de StatefulSets
- [ ] Multi-zone StatefulSets

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- Tutorial: https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/