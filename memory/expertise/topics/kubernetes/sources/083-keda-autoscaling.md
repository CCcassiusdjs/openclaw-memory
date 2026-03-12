# KEDA - Kubernetes Event-Driven Autoscaling

**Fonte:** https://keda.sh/
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

KEDA é um componente Kubernetes Event-Driven Autoscaler. Permite escalar containers baseado em eventos, de 0 a N instâncias, sem duplicar funcionalidade do HPA.

---

## O que é KEDA

Kubernetes-based Event Driven Autoscaler que:
- Escala containers baseado em número de eventos
- Single-purpose, lightweight component
- Works alongside standard Kubernetes components
- Não sobrescreve nem duplica HPA

### Key Features
| Feature | Descrição |
|---------|-----------|
| **Event-driven** | Escala baseado em eventos, não CPU/memory |
| **Scale to/from zero** | 0 to N instances |
| **Built-in Scalers** | 70+ event sources |
| **Multiple Workload Types** | Deployments, Jobs, StatefulSets, custom resources |
| **Vendor-Agnostic** | Multi-cloud support |

---

## Built-in Scalers (70+)

### Message Queues
- Apache Kafka
- RabbitMQ
- Azure Service Bus
- AWS SQS
- Google Pub/Sub
- NATS
- Redis Streams

### Databases
- PostgreSQL
- MongoDB
- MySQL
- Cassandra
- Elasticsearch

### Monitoring
- Prometheus
- Datadog
- Dynatrace
- New Relic
- Splunk

### Cloud Services
- Azure Blob Storage
- AWS DynamoDB
- GCP Pub/Sub
- Azure Pipelines

### Event Sources
- Cron (time-based)
- CPU/Memory (standard HPA)
- External (custom scalers)
- External Push (push-based)

---

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│              KEDA Components                        │
│  ┌─────────────────────────────────────────────┐  │
│  │           KEDA Operator                      │  │
│  │  ┌─────────────┐  ┌─────────────┐          │  │
│  │  │  Scaler     │  │  HPA        │          │  │
│  │  │  (Metrics)  │  │  Controller │          │  │
│  │  └─────────────┘  └─────────────┘          │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│              Event Sources                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  Kafka   │ │ RabbitMQ │ │  Redis  │           │
│  └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │Prometheus│ │ Datadog  │ │   SQL   │           │
│  └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│              Workloads                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │Deployment│ │   Job    │ │StatefulSet│          │
│  └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────┘
```

---

## ScaledObject Example

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: kafka-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicaCount: 0
  maxReplicaCount: 10
  cooldownPeriod: 30
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka.svc:9092
      consumerGroup: my-group
      topic: orders
      lagThreshold: "10"
```

---

## ScaledJob Example

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledJob
metadata:
  name: queue-processor
spec:
  jobTargetRef:
    template:
      spec:
        containers:
        - name: processor
          image: my-processor:latest
        restartPolicy: Never
  triggers:
  - type: rabbitmq
    metadata:
      host: rabbitmq.svc
      queueName: jobs
      queueLength: "5"
```

---

## Key Concepts

### ScaledObject
- Escala Deployments, StatefulSets, Custom Resources
- Cria HPA automaticamente
- Scale to zero quando não há eventos

### ScaledJob
- Cria Kubernetes Jobs baseado em eventos
- Ideal para batch processing
- Cada evento pode criar um Job

### Triggers
- Definem quando escalar
- Múltiplos triggers por ScaledObject
- AND logic para múltiplos triggers

### Cooldown Period
- Tempo antes de scale down
- Default: 300 segundos
- Evita thrashing

---

## Benefits

| Benefício | Descrição |
|-----------|-----------|
| **Scale to Zero** | Economia de recursos quando idle |
| **Event-Driven** | Escala baseado em demanda real |
| **No Code Changes** | Funciona com qualquer container |
| **Multi-Source** | 70+ built-in scalers |
| **Extensible** | Custom scalers via External |

---

## Use Cases

### 1. Message Queue Processing
```
Kafka → KEDA → Scale consumers based on lag
```

### 2. Batch Processing
```
RabbitMQ → KEDA → Create Jobs for each message
```

### 3. Cost Optimization
```
Cron → Scale down dev environments at night
```

### 4. ML Inference
```
Prometheus → Scale inference pods based on request rate
```

---

## Integration with ML/AI

| Use Case | Scaler | Benefit |
|----------|--------|---------|
| Model Serving | Prometheus | Scale based on latency |
| Data Pipeline | Kafka | Scale based on queue depth |
| Batch Training | Azure Pipelines | Scale based on queue |
| Feature Store | Redis | Scale based on cache hit rate |

---

## Comparison with HPA

| Feature | HPA | KEDA |
|---------|-----|------|
| Metrics | CPU, Memory, Custom | 70+ event sources |
| Scale to Zero | No | Yes |
| Event-Driven | Limited | Native |
| Jobs Support | No | Yes (ScaledJob) |
| External Triggers | Custom Metrics API | Built-in scalers |

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| ScaledObject | CRD para escalar Deployments/StatefulSets |
| ScaledJob | CRD para criar Jobs baseado em eventos |
| Trigger | Condição para escalar |
| Cooldown Period | Tempo antes de scale down |
| Scale to Zero | Reduzir para 0 réplicas quando idle |

---

## Referências

- KEDA Documentation: https://keda.sh/docs/
- Scalers List: https://keda.sh/docs/2.19/scalers/
- GitHub: https://github.com/kedacore/keda