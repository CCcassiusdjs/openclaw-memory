# StatefulSets

**Source:** https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
**Type:** Official Documentation
**Category:** Storage/StatefulSets
**Read:** 2026-03-11

---

## Resumo

### O que é StatefulSet?
Workload API para gerenciar aplicações **stateful**:
- Mantém identidade persistente para cada Pod
- Garante ordem de deploy e scaling
- Provê storage estável

### Quando Usar?
StatefulSets são valiosos para aplicações que requerem:
1. **Identificadores de rede estáveis e únicos**
2. **Storage persistente estável**
3. **Deployment e scaling ordenados**
4. **Rolling updates ordenados e automatizados**

### StatefulSet vs Deployment

| Característica | Deployment | StatefulSet |
|----------------|-----------|-------------|
| Identidade Pod | Random | Ordinal (web-0, web-1) |
| Storage | Compartilhado | PVC por Pod |
| Network | Random DNS | DNS estável |
| Scaling | Paralelo | Ordenado |

---

## Componentes

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
  clusterIP: None    # Headless Service
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"    # Headless Service
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
  volumeClaimTemplates:    # PVC automático por Pod
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
- Para N réplicas: Pods nomeados de 0 a N-1
- Exemplo: web-0, web-1, web-2
- Label: `apps.kubernetes.io/pod-index`

### Stable Network ID
- Hostname: `$(statefulset name)-$(ordinal)`
- DNS: `$(podname).$(governing service domain)`
- Exemplo: `web-0.nginx.default.svc.cluster.local`

### Stable Storage
- Cada Pod recebe seu próprio PVC
- PVC criado via `volumeClaimTemplates`
- PVC **NÃO é deletado** quando Pod/StatefulSet são deletados

---

## Deployment Guarantees

### Ordinal Order
1. Deploy: Pods criados sequencialmente (0 → N-1)
2. Delete: Pods terminados em ordem reversa (N-1 → 0)
3. Scale: Predecessores devem estar Running/Ready
4. Update: Sucessores devem estar shutdown antes de atualizar

### Pod Management Policies

| Política | Comportamento |
|----------|---------------|
| **OrderedReady** (default) | Ordem estrita, um por um |
| **Parallel** | Todos em paralelo |

---

## Update Strategies

| Estratégia | Comportamento |
|------------|--------------|
| **OnDelete** | Manual - Pod atualizado quando deletado |
| **RollingUpdate** | Automático - ordem reversa (N-1 → 0) |

### RollingUpdate Options
- `partition`: Pode limitar updates (apenas Pods ≥ partition)
- `maxUnavailable`: Número máximo de Pods indisponíveis durante update

---

## Limitações

1. **Storage**: Deve ser provisionado por PV Provisioner ou pre-provisioned
2. **Volume Deletion**: Volumes não são deletados automaticamente (proteção de dados)
3. **Headless Service**: Obrigatório para network identity
4. **Termination**: Não garante ordem quando StatefulSet é deletado (scale to 0 antes)
5. **Rolling Update Bug**: Pode precisar de intervenção manual

---

## Best Practices

- Usar `ReadWriteOncePod` em produção (mais seguro que RWO)
- Configurar `terminationGracePeriodSeconds` adequadamente
- NÃO usar `pod.Spec.TerminationGracePeriodSeconds: 0`
- Criar Headless Service antes do StatefulSet
- Para ordered termination: scale to 0 antes de deletar

---

## Conceitos-Chave

1. **Sticky Identity**: Pods mantêm nome e storage através de reschedules
2. **Headless Service**: DNS estável para cada Pod
3. **volumeClaimTemplates**: PVC automático por Pod
4. **Ordered Operations**: Sequencial por default, paralelo opcional
5. **Data Safety**: Volumes não são deletados automaticamente