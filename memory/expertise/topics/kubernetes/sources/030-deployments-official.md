# Kubernetes Deployments (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Deployment gerencia um conjunto de Pods para rodar uma workload stateless, fornecendo updates declarativos para ReplicaSets.

---

## O que é Deployment?

### Definição
- Workload API object para aplicações stateless
- Gerencia ReplicaSets e Pods
- Updates declarativos com rollout controlado
- Garantias de disponibilidade durante updates

### Relação com ReplicaSets
- Deployment cria ReplicaSet
- ReplicaSet cria Pods
- Múltiplos ReplicaSets podem existir (rollout history)

---

## Casos de Uso

1. **Rollout**: Criar ReplicaSet para rodar Pods
2. **Update**: Declarar novo estado, rollout gradual
3. **Rollback**: Reverter para versão anterior
4. **Scale**: Escalar para mais/menos Pods
5. **Pause/Resume**: Pausar rollout, aplicar fixes, resumir
6. **Status**: Indicar rollout travado
7. **Cleanup**: Remover ReplicaSets antigos

---

## Exemplo de Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

---

## Campos Importantes

### replicas
- Número desejado de Pods
- Padrão: 1

### selector
- Define quais Pods o Deployment gerencia
- Deve match com template.labels

### template
- Pod template
- Deve ter labels que match com selector

---

## Rolling Update Strategy

### Padrão: RollingUpdate

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # Pods extras durante rollout
      maxUnavailable: 25%  # Pods indisponíveis durante rollout
```

### maxSurge
- Quantos Pods EXTRA podem existir durante rollout
- Pode ser número absoluto ou percentual
- Padrão: 25%

### maxUnavailable
- Quantos Pods podem estar INDISPONÍVEIS
- Pode ser número absoluto ou percentual
- Padrão: 25%

### Comportamento
- Garante pelo menos (replicas - maxUnavailable) Pods disponíveis
- Garante no máximo (replicas + maxSurge) Pods total
- Exemplo com 3 réplicas: 2-4 Pods durante rollout

---

## Criando um Deployment

```bash
# Criar
kubectl apply -f deployment.yaml

# Verificar
kubectl get deployments
kubectl rollout status deployment/nginx-deployment

# Ver ReplicaSets criados
kubectl get rs

# Ver Pods
kubectl get pods --show-labels
```

---

## Atualizando um Deployment

### Método 1: set image
```bash
kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
```

### Método 2: edit
```bash
kubectl edit deployment/nginx-deployment
```

### Método 3: apply
```bash
kubectl apply -f deployment-new.yaml
```

### Comportamento
- Novo ReplicaSet criado
- Escalado gradualmente
- ReplicaSet antigo escalado para 0
- Pod template hash label usado para tracking

---

## Rollback

### Histórico de Revisões
```bash
# Ver histórico
kubectl rollout history deployment/nginx-deployment

# Detalhes de uma revisão
kubectl rollout history deployment/nginx-deployment --revision=2
```

### Reverter
```bash
# Voltar para anterior
kubectl rollout undo deployment/nginx-deployment

# Voltar para revisão específica
kubectl rollout undo deployment/nginx-deployment --to-revision=2
```

### revisionHistoryLimit
```yaml
spec:
  revisionHistoryLimit: 10  # Manter últimas 10 revisões
```

---

## Scaling

### Manual
```bash
kubectl scale deployment/nginx-deployment --replicas=10
```

### HorizontalPodAutoscaler
```bash
kubectl autoscale deployment/nginx-deployment --min=10 --max=15 --cpu-percent=80
```

### Proportional Scaling
Durante rollout, réplicas são distribuídas proporcionalmente entre ReplicaSets ativos.

---

## Pause e Resume

```bash
# Pausar
kubectl rollout pause deployment/nginx-deployment

# Fazer múltiplas mudanças
kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
kubectl set resources deployment/nginx-deployment -c nginx --limits=cpu=200m,memory=512Mi

# Resumir (único rollout)
kubectl rollout resume deployment/nginx-deployment
```

---

## Deployment Status

### Condições

| Condição | Descrição |
|----------|-----------|
| **Available** | Mínimo de réplicas disponíveis |
| **Progressing** | Novo ReplicaSet está sendo escalado |
| **ReplicaFailure** | Falha ao criar réplicas |

### Progress Deadline
```yaml
spec:
  progressDeadlineSeconds: 600  # Timeout para rollout
```

---

## Label Selector Updates

⚠️ **CUIDADO:** Label selectors são imutáveis em apps/v1.

### Imutável após criação
- Não pode ser alterado
- Mudança de selector requer novo Deployment

---

## Pod Template Hash

### Label Adicionado Automaticamente
```
pod-template-hash: 75675f5897
```

- Hash do Pod template
- Garante ReplicaSets únicos
- Não modificar manualmente

---

## Clean Up Policy

```yaml
spec:
  revisionHistoryLimit: 5  # Manter 5 ReplicaSets antigos
```

- Default: 10
- ReplicaSets antigos são garbage collected

---

## Rollover

Quando um rollout está em progresso e uma nova update é feita:

1. Novo ReplicaSet criado
2. Deployment começa a escalar novo ReplicaSet
3. ReplicaSet anterior (em rollout) é adicionado aos "old ReplicaSets"
4. Escala para 0

### Exemplo
- 5 réplicas de nginx:1.14.2
- Update para nginx:1.16.1
- Quando 3 réplicas de 1.14.2 criadas
- Update para nginx:1.17.0
- Deployment imediatamente muda para criar 1.17.0
- Não espera 5 réplicas de 1.14.2

---

## Strategy Types

### RollingUpdate (Default)
- Gradualmente substitui Pods
- Zero downtime
- Configurável com maxSurge/maxUnavailable

### Recreate
```yaml
spec:
  strategy:
    type: Recreate
```
- Deleta TODOS Pods antes de criar novos
- Downtime durante update
- Útil quando não pode ter múltiplas versões

---

## Conceitos-Chave

1. **ReplicaSet**: Gerencia réplica de Pods (low-level)
2. **Deployment**: Gerencia ReplicaSets (high-level)
3. **RollingUpdate**: Substituição gradual de Pods
4. **Rollback**: Reverter para versão anterior
5. **Revision History**: Histórico de configurações

---

## Próximos Passos de Estudo

- [ ] Canary deployments com Deployments
- [ ] Blue-green deployments
- [ ] Deployment com HPA
- [ ] Deployment com PodDisruptionBudget
- [ ] Advanced rollout strategies

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- ReplicaSet: https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/
- Tutorial: https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/