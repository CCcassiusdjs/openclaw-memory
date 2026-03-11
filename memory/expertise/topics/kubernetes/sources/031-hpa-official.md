# Kubernetes HorizontalPodAutoscaler (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

HorizontalPodAutoscaler (HPA) escala automaticamente o número de Pods em um workload baseado em métricas observadas (CPU, memória, custom).

---

## O que é HPA?

### Definição
- Recurso que escala réplicas de Pods automaticamente
- Baseado em métricas (CPU, memória, custom)
- Parte da API autoscaling/v2
- Controlado pelo controller manager

### Funcionamento
```
Metrics Server → HPA Controller → Scale Target
     ↑                ↓
   Metrics      Scale Decision
```

---

## Como Funciona

### Loop de Controle
1. HPA controller verifica métricas periodicamente
2. Calcula réplicas desejadas baseado em target
3. Atualiza ScaleTarget (Deployment, StatefulSet)
4. ScaleTarget cria/deleta Pods

### Fórmula de Escala
```
desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]
```

**Exemplo:**
- Target: 50% CPU
- Current: 100% CPU
- Current Replicas: 2
- Desired: ceil[2 * (100/50)] = 4

---

## Métricas Suportadas

### Resource Metrics
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apc
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apc
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### Container Resource Metrics (v1.27+)
```yaml
metrics:
- type: ContainerResource
  containerResource:
    name: cpu
    container: application
    target:
      type: Utilization
      averageUtilization: 60
```

### Pod Metrics (Custom)
```yaml
metrics:
- type: Pods
  pods:
    metric:
      name: packets-per-second
    target:
      type: AverageValue
      averageValue: 1k
```

### Object Metrics (External)
```yaml
metrics:
- type: Object
  object:
    metric:
      name: requests-per-second
    describedObject:
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      name: main-route
    target:
      type: AverageValue
      averageValue: 500
```

### External Metrics
```yaml
metrics:
- type: External
  external:
    metric:
      name: queue_messages_ready
      selector:
        matchLabels:
          queue: "worker_tasks"
    target:
      type: AverageValue
      averageValue: 30
```

---

## Comportamento de Escala

### Scale Up
- Rápido por padrão
- Pode configurar stabilization window
- Permite múltiplos scale events em janela curta

### Scale Down
- Conservador por padrão
- Stabilization window de 5 minutos
- Apenas um scale event por janela

### Configuration
```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60
    - type: Pods
      value: 4
      periodSeconds: 60
    selectPolicy: Min  # Escolhe a política mais conservadora
  scaleUp:
    stabilizationWindowSeconds: 0
    policies:
    - type: Percent
      value: 100
      periodSeconds: 15
    - type: Pods
      value: 4
      periodSeconds: 15
    selectPolicy: Max
```

---

## Default Behavior

### Sem behavior definido:
- **Scale Up**: 
  - Dobra réplicas (100%)
  - Período: 15s
  - Múltiplos events permitidos
  
- **Scale Down**:
  - 100% dos pods atuais
  - Período: 15s
  - Apenas um event por stabilization window (5min)

---

## Requisitos

### Metrics Server
```bash
# Instalar Metrics Server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Custom Metrics (opcional)
- Instalar adapter custom metrics
- Prometheus Adapter
- Google Cloud Monitoring

---

## Limitações

### VPA Conflict
- HPA e VPA podem conflitar
- Usar um ou outro, ou usar com cuidado
- VPA para memory, HPA para CPU é possível

### Scale From Zero
- HPA não pode escalar de 0 para N
- Precisa de pelo menos 1 réplica ativa
- KEDA pode escalar de 0

### Metric Availability
- Se métricas não disponíveis, HPA não age
- Configurar fallback se necessário

---

## Status e Debugging

### Verificar HPA
```bash
kubectl get hpa
kubectl describe hpa <name>
```

### Condições

| Condição | Status | Descrição |
|----------|--------|-----------|
| AbleToScale | True | HPA pode obter métricas e escalar |
| ScalingActive | True | HPA está processando métricas |
| ScalingLimited | False | Não atingiu limites |

### Eventos Comuns
```
Normal  SuccessfulRescale  New size: 4
Warning FailedGetMetric      unable to get metric
Warning FailedComputeMetrics unable to compute desired replicas
```

---

## Multiple Metrics

HPA pode usar múltiplas métricas:
```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 50
- type: Pods
  pods:
    metric:
      name: http_requests_per_second
    target:
      type: AverageValue
      averageValue: 100
```

**Comportamento:** Usa a métrica que resulta em MAIS réplicas.

---

## Conceitos-Chave

1. **HPA Controller**: Control loop que ajusta réplicas
2. **Metrics Server**: Fonte de métricas de recurso
3. **Scale Target**: Deployment, StatefulSet, ReplicaSet
4. **Stabilization Window**: Delay para evitar flapping
5. **Scaling Policies**: Regras de scale up/down

---

## Best Practices

1. **Resource Requests**: Sempre definir requests para HPA
2. **Min/Max**: Definir limites razoáveis
3. **Metrics**: Usar métricas relevantes para workload
4. **Testing**: Testar comportamento em staging
5. **Monitoring**: Alertar quando próximo de limites

---

## Próximos Passos de Estudo

- [ ] VerticalPodAutoscaler (VPA)
- [ ] Custom Metrics Adapter
- [ ] KEDA para scale to zero
- [ ] HPA com múltiplas métricas

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- Metrics Server: https://github.com/kubernetes-sigs/metrics-server
- VPA: https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler