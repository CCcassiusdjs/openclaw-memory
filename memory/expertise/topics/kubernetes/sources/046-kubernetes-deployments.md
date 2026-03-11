# Kubernetes Deployments - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/controllers/deployment/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Deployments gerenciam um conjunto de Pods para rodar aplicações stateless. Fornece atualizações declarativas para Pods e ReplicaSets.

## What is a Deployment?

### Definition
- Manages stateless application workloads
- Provides declarative updates for Pods and ReplicaSets
- Controller changes actual state to desired state at controlled rate

### Key Concept
- Describe desired state in Deployment
- Deployment controller manages the transition
- Creates/updates ReplicaSets as needed

## Use Cases

1. **Rollout** - Create Deployment to rollout ReplicaSet
2. **Update** - Declare new state via PodTemplateSpec update
3. **Rollback** - Rollback to earlier revision if unstable
4. **Scale** - Scale up/down for load changes
5. **Pause/Resume** - Apply multiple fixes, then resume
6. **Status** - Use Deployment status as rollout indicator

## Creating a Deployment

### Example
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

### Key Fields
- `.metadata.name` - Deployment name (basis for ReplicaSet/Pod names)
- `.spec.replicas` - Number of Pod replicas
- `.spec.selector` - How to find Pods to manage
- `.spec.template` - Pod template specification

## Updating a Deployment

### Rolling Update Strategy
- Creates new ReplicaSet for updated template
- Gradually scales up new ReplicaSet
- Gradually scales down old ReplicaSet
- Ensures Pods replaced at controlled rate

### Default Limits
- **maxUnavailable**: 25% of desired Pods can be down
- **maxSurge**: 25% extra Pods can be created above desired

### Rollout Trigger
- Only Pod template changes trigger rollout
- Scaling does NOT trigger rollout

## Pod-Template-Hash Label

### Purpose
- Added by Deployment controller to every ReplicaSet
- Ensures child ReplicaSets don't overlap
- Hash generated from PodTemplate

### Important
- **Do NOT change this label**
- It's managed by the controller

## Key Takeaways

1. Deployment manages stateless workloads
2. Creates/manages ReplicaSets automatically
3. Rolling updates are the default strategy
4. Rollout only triggered by Pod template changes
5. maxUnavailable and maxSurge control rollout pace
6. Revision history enables rollback

## Personal Notes

Deployments são o workload mais comum para stateless apps. O conceito de rollout é essencial para entender atualizações zero-downtime.

Para CKA/CKAD:
- `kubectl rollout status deployment/<name>` - check rollout
- `kubectl rollout undo deployment/<name>` - rollback
- `kubectl scale deployment/<name> --replicas=N` - scale
- `kubectl set image deployment/<name> container=image` - update image

A distinction entre Deployment e ReplicaSet é importante - Deployment cria ReplicaSets automaticamente e gerencia o ciclo de vida.