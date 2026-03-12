# Horizontal Pod Autoscaler with Custom Metrics - Guide

**Fonte:** Overcast Blog - https://overcast.blog/horizontal-pod-autoscaler-hpa-with-custom-metrics-a-guide-0fd5cf0f80b8
**Data:** Março 2024
**Tópico:** HPA, Custom Metrics, Prometheus Adapter, External Metrics
**Status:** Lido

---

## Resumo Executivo

Guia completo de HPA com métricas customizadas, cobrindo categorias (Pod, External), setup com Prometheus Adapter, e exemplos práticos de scaling baseado em métricas específicas da aplicação.

---

## Por que Custom Metrics

### Limitações de CPU/Memory
- Aplicações complexas podem não ter correlação direta com CPU/memória
- Performance bottleneck pode ser network latency, I/O throughput
- Scaling baseado em CPU/memória pode levar a under/over-provisioning

### Benefícios de Custom Metrics
- Scaling baseado em métricas específicas da aplicação
- Melhor alinhamento com performance real
- Decisões mais precisas e responsivas

---

## Categorias de Custom Metrics

### Pod Metrics
- Derivados dos próprios Pods
- Exemplos:
  - Active sessions
  - Transaction rate
  - Custom application counters
- Decisões acopladas à performance interna

### External Metrics
- Dados de serviços/sistemas externos
- Exemplos:
  - Message queue depth (SQS, RabbitMQ)
  - Traffic metrics de load balancer
  - Business metrics (orders/second)
- Permite scaling proativo baseado em demanda externa

---

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│            HorizontalPodAutoscaler                   │
│  (Escala baseado em métricas)                       │
├─────────────────────────────────────────────────────┤
│            Custom Metrics API                        │
│  (custom.metrics.k8s.io)                            │
├─────────────────────────────────────────────────────┤
│            Metrics Adapter                          │
│  ┌───────────────┐ ┌───────────────┐               │
│  │ Prometheus    │ │ Kube Metrics  │               │
│  │ Adapter       │ │ Adapter       │               │
│  └───────────────┘ └───────────────┘               │
├─────────────────────────────────────────────────────┤
│            Metrics Source                           │
│  ┌───────────────┐ ┌───────────────┐               │
│  │ Prometheus    │ │ External API  │               │
│  │ Server        │ │ (Queue, etc)  │               │
│  └───────────────┘ └───────────────┘               │
├─────────────────────────────────────────────────────┤
│            Application Pods                          │
│  (Export metrics)                                  │
└─────────────────────────────────────────────────────┘
```

---

## Pré-requisitos

### 1. Kubernetes Cluster
- Versão 1.23+
- Minikube, Kind, GKE, EKS, AKS

### 2. Metrics Server
```bash
# Deploy
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verificar
kubectl get deployment metrics-server -n kube-system
```

### 3. Custom Metrics API
- Prometheus Adapter, ou
- Kube Metrics Adapter, ou
- Implementação customizada

---

## Setup com Prometheus

### Deploy Prometheus Adapter
```bash
kubectl apply -f https://raw.githubusercontent.com/DirectXMan12/k8s-prometheus-adapter/master/deploy/manifests/custom-metrics-apiserver-deployment.yaml
```

### Configurar Metrics
- Expor métricas da aplicação com labels adequados
- Configurar recording rules no Prometheus
- ServiceMonitor para scrape

### Verificar Custom Metrics
```bash
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq .
```

---

## Configurar HPA com Custom Metrics

### Exemplo: Queue Length
```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: my-application-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-application
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: External
    external:
      metric:
        name: my_queue_length
        selector:
          matchLabels:
            queue: "jobs"
      target:
        type: Value
        value: 10
```

### Exemplo: Requests per Second
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: 1000
```

### Exemplo: Múltiplas Métricas
```yaml
metrics:
# CPU
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70

# Memória
- type: Resource
  resource:
    name: memory
    target:
      type: AverageValue
      averageValue: 500Mi

# Custom: Request latency
- type: Pods
  pods:
    metric:
      name: http_request_duration_seconds
    target:
      type: AverageValue
      averageValue: 100ms

# External: Queue depth
- type: External
  external:
    metric:
      name: rabbitmq_queue_messages_ready
      selector:
        matchLabels:
          queue: "tasks"
    target:
      type: AverageValue
      averageValue: 50
```

---

## Tipos de Target

### Value
- Compara valor diretamente com target
- Útil para external metrics

### AverageValue
- Divide valor pelo número de Pods
- Mais comum para Pod metrics

### Utilization
- Percentagem do recurso solicitado
- Apenas para Resource metrics (CPU, memória)

---

## Comportamento de Scaling

### Scale Up
- Imediato quando métrica excede target
- `desiredReplicas = ceil[currentReplicas * (currentValue / targetValue)]`

### Scale Down
- Gradual com stabilization window
- Default: 5 minutos
- Configurável via behavior:

```yaml
behavior:
  scaleDown:
    stabilizationWindowSeconds: 300
    policies:
    - type: Percent
      value: 10
      periodSeconds: 60
```

### Múltiplas Métricas
- HPA calcula réplicas desejadas para cada métrica
- Usa o **maior valor** de réplicas
- Garante que todos targets sejam atendidos

---

## Monitoramento e Troubleshooting

### Verificar HPA
```bash
# Status
kubectl get hpa

# Detalhes
kubectl describe hpa my-application-hpa
```

### Status Interpretation
| Status | Significado |
|--------|-------------|
| `<metric>/target` | Current/target value |
| `MINPODS/MAXPODS` | Limites configurados |
| `REPLICAS` | Réplicas atuais |
| `Events` | Histórico de scaling |

### Problemas Comuns
| Problema | Causa | Solução |
|-----------|-------|---------|
| `unable to get metric` | Metric não disponível | Verificar adapter |
| `the HPA was unable to compute` | Dados insuficientes | Aguardar métricas |
| `missing request for cpu` | Requests não definidos | Adicionar resources |

---

## Best Practices

### 1. Definir Resources Requests
```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

### 2. Usar Métricas Relevantes
- CPU: Workloads CPU-bound
- Queue depth: Workers de processamento
- Requests/sec: Web APIs
- Latency: Aplicações sensíveis a performance

### 3. Configurar Limits Adequados
- minReplicas: Mínimo para HA (2+)
- maxReplicas: Limite de custo/capacidade

### 4. Testar Carga
- Load testing para validar behavior
- Ajustar targets conforme observação

---

## Insights para Kubernetes

1. **Custom metrics = melhor alinhamento**: Métricas específicas refletem performance real
2. **Adapter é obrigatório**: Prometheus Adapter é solução mais comum
3. **Múltiplas métricas = max**: HPA escolhe réplica mais alta
4. **Stabilization window**: Scale down é gradual por design
5. **Requests são obrigatórios**: Para Utilization targets

---

## Palavras-Chave
`hpa` `custom-metrics` `prometheus-adapter` `autoscaling` `external-metrics` `pod-metrics` `kubernetes`