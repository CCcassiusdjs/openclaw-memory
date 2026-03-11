# Kubernetes Horizontal Pod Autoscaler (HPA) - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

HorizontalPodAutoscaler (HPA) atualiza automaticamente workloads (Deployment, StatefulSet) para escalar capacidade conforme demanda. Horizontal scaling = adicionar Pods, vertical scaling = adicionar recursos.

## How HPA Works

### Control Loop
- Runs in control plane
- Default interval: 15 seconds
- Queries metrics, calculates replicas, updates workload

### Scaling Algorithm
```
desiredReplicas = ceil(currentReplicas × currentMetricValue/desiredMetricValue)
```

### Example
- Current CPU: 200m, Target: 100m
- Ratio: 200/100 = 2.0
- Result: double replicas

### Tolerance
- Default: 0.1 (10%)
- Skip scaling if ratio within tolerance
- Prevents thrashing

## Metrics Types

### Resource Metrics
- CPU utilization
- Memory utilization
- Requires Metrics Server

### Custom Metrics
- Per-pod metrics
- Object metrics
- External metrics

### Pod Metrics
- Requires Metrics Server
- Uses resource requests for calculation
- Missing metrics handled conservatively

## API Object

### autoscaling/v2 (Stable)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
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

### Scale Target
- Deployment
- StatefulSet
- ReplicaSet
- Any resource with `scale` subresource

## Behavior Configuration

### Scale Down Stabilization
- Default: 5 minutes
- Highest recommendation in window chosen
- Prevents rapid scale down/up

### Scale Up
- Immediate if metrics warrant
- No stabilization delay

## Pod Readiness and Metrics

### Initialization Period
- `--horizontal-pod-autoscaler-cpu-initialization-period`: 5 minutes default
- CPU metrics ignored during startup
- Prevents misleading high CPU from warm-up

### Readiness Delay
- `--horizontal-pod-autoscaler-initial-readiness-delay`: 30 seconds default
- Pods with rapid ready/not-ready toggles ignored
- Ensures stable readiness signal

### Best Practices
- Use startupProbe for initialization phase
- Set readinessProbe with appropriate initialDelaySeconds
- Match initialization-period to app startup time

## Scaling During Rolling Update

### Deployment
- HPA manages Deployment's replicas field
- Deployment controller handles ReplicaSets
- Works seamlessly during rollout

### StatefulSet
- HPA manages StatefulSet directly
- No intermediate resource
- Pods managed directly by StatefulSet

## Key Takeaways

1. HPA scales horizontally (adds/removes Pods)
2. Control loop runs every 15 seconds (default)
3. Algorithm: desiredReplicas = current × (currentMetric/targetMetric)
4. Tolerance (10%) prevents thrashing
5. 5-minute stabilization for scale down
6. Pod readiness affects metric collection
7. Requires Metrics Server for resource metrics

## Personal Notes

HPA é essencial para escalar workloads automaticamente. A configuração correta de resource requests é crítica.

Para CKA/CKAD:
- minReplicas/maxReplicas: bounds
- scaleTargetRef: target workload
- metrics: list of metrics to track
- type: Resource, Pods, Object, External

A feature de stabilization é importante para evitar flapping. Para apps com startup lento (Java), ajustar initialization-period.