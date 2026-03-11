# AI/ML Kubernetes Best Practices: The Essentials

**Fonte:** https://www.wiz.io/academy/ai-ml-kubernetes-best-practices  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Guia comprehensive para rodar workloads AI/ML em Kubernetes, cobrindo resource management, scaling, storage, security e observability.

## Resource Management

### GPU Allocation
- Use device plugins (NVIDIA, Intel) para expor GPUs aos pods
- Sempre definir resource requests para scheduler correto
- Label GPU nodes: `nvidia.com/gpu=true`
- Node selectors para targeting

```yaml
# Pod com GPU request
spec:
  containers:
  - name: gpu-app
    resources:
      limits:
        nvidia.com/gpu: 1
```

### CPU/Memory Sizing
- Requests e limits são obrigatórios
- Monitorar uso real com Prometheus
- Ajustar requests se >90% ou <20% utilization

### Cluster Autoscaling
- Absorver spikes de traffic/jobs
- HPA para scaling horizontal
- VPA para ajustar requests automaticamente

## Scaling Strategies

### Horizontal Pod Autoscaler (HPA)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: inference-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Batch Jobs
- Kubernetes Jobs para one-off experiments
- CronJobs para scheduled retraining
- Gerenciar recursos como qualquer pod

### Multi-Cluster
- Anthos para management console multi-cluster
- Failover entre environments
- Hybrid on-prem + cloud

## Storage & Data

### High-Performance Storage
- StorageClasses com SSD para training
- PVC com StorageClass apropriado
- Monitorar IOPS

### Data Locality
- Caching layers para remote storage
- Node-local SSD volumes
- Sidecar container para caching

```yaml
# Sidecar de cache
volumes:
- name: training-data-cache
  emptyDir: {}
```

### Backup & Versioning
- Model artifacts em object storage (S3)
- Scheduled backups
- Version tracking para rollbacks

## Security

### Fundamentals
- Scan container images (vulnerabilities)
- RBAC restritivo
- Pod Security Standards (PSS)
- Registry access control
- Stable image tags

### Model Integrity
- Monitor incoming data for anomalies
- Drift detection (Alibi Detect)
- Train only on vetted datasets
- Digital signatures (Cosign)

```bash
# Sign container image
cosign sign myregistry/model:v1
```

### Network Isolation
- NetworkPolicies para restrict comunicação
- Separar namespaces por propósito
- Zero-trust principles

```yaml
# NetworkPolicy restrictiva
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: inference
```

## Observability

### Metrics
- Prometheus para CPU, memory, GPU usage
- Grafana para dashboards
- Alerting rules para threshold violations

```yaml
# PrometheusRule para GPU alert
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
spec:
  groups:
  - name: gpu-alerts
    rules:
    - alert: HighGPUUsage
      expr: gpu_utilization > 90
      for: 5m
```

### Distributed Tracing
- OpenTelemetry para request tracing
- Correlação entre serviços
- Performance bottleneck identification

### Logging
- Centralized logging stack
- Structured logs (JSON)
- Correlation IDs

## Key Takeaways

1. **Resource Management**: Sempre definir requests/limits, usar labels, monitorar
2. **Scaling**: HPA para inference, Jobs para training, multi-cluster para resiliência
3. **Storage**: SSD StorageClasses, caching, versioning
4. **Security**: Defense in depth - RBAC, PSS, NetworkPolicies, image signing
5. **Observability**: Full stack visibility - metrics, logs, traces

## Insights

- AI/ML em Kubernetes é complexo mas manejável com boas práticas
- Security não é opcional - breaches em ML platforms são comuns
- Observabilidade é crítica para troubleshooting
- Multi-cluster strategies oferecem resiliência e cost optimization