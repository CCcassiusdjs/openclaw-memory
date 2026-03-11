# Kubernetes Autoscaling Workloads - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/autoscaling/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Kubernetes suporta múltiplas estratégias de autoscaling: horizontal (HPA), vertical (VPA), baseado em cluster size, baseado em eventos (KEDA), e baseado em schedules.

## Scaling Strategies

### Horizontal Scaling
- Add or remove Pod replicas
- HPA (HorizontalPodAutoscaler)
- Automatic based on metrics

### Vertical Scaling
- Adjust CPU/memory for running Pods
- VPA (VerticalPodAutoscaler)
- Add-on (not built-in)

## Manual Scaling

### Horizontal
```bash
kubectl scale deployment/my-app --replicas=5
```

### Vertical
```bash
kubectl patch deployment my-app --type=json -p='[
  {"op": "replace", "path": "/spec/template/spec/containers/0/resources/requests/cpu", "value":"500m"}
]'
```

## Automatic Scaling

### HorizontalPodAutoscaler (HPA)
- Built-in controller
- Scales based on CPU, memory, or custom metrics
- Requires Metrics Server
- Stable API: autoscaling/v2

### VerticalPodAutoscaler (VPA)
- Add-on component (not built-in)
- Scales resource requests/limits
- Requires Metrics Server
- Stable since v1.25
- In-place resize: v1.35 stable

### Cluster Proportional Autoscaler
- Scales based on cluster size
- For cluster-dns, system components
- Horizontal: more replicas
- Vertical: more resources per replica

### Event-Driven Autoscaling (KEDA)
- CNCF graduated project
- Scales based on event count
- Queue depth, message count
- Many event source adapters

### Schedule-Based Scaling
- KEDA + Cron scaler
- Scale down during off-peak
- Define schedules and timezones

## Comparison

| Feature | HPA | VPA | Cluster Proportional | KEDA |
|---------|-----|-----|---------------------|------|
| Built-in | Yes | No | No | No |
| Metric type | CPU/memory/custom | CPU/memory | Node/Core count | Events |
| Scaling | Horizontal | Vertical | Horizontal | Horizontal |
| Use case | Web apps | Right-sizing | DNS, system | Queues, streams |

## Key Takeaways

1. Horizontal scaling = add Pods, Vertical scaling = add resources
2. HPA is built-in, VPA is an add-on
3. Cluster Proportional scales with cluster size
4. KEDA for event-driven scaling
5. Schedule-based scaling with KEDA Cron scaler
6. Metrics Server required for HPA and VPA

## Personal Notes

Escolha do autoscaling depende do workload:
- HPA: web apps, APIs, stateless
- VPA: apps que precisam de right-sizing
- KEDA: event-driven, queues, streams
- Cluster Proportional: DNS, monitoring, ingress

Para CKA/CKAD:
- HPA: built-in, autoscaling/v2
- VPA: add-on, requires Metrics Server
- kubectl scale: manual horizontal
- kubectl patch: manual vertical

A feature de in-place resize (v1.35) é importante para VPA - evita restart de pods.