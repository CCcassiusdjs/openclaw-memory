# Kubernetes Pod Priority and Preemption - Official Documentation

**Source:** kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Pod Priority permite que Pods tenham prioridade relativa. Quando um Pod não pode ser agendado, o scheduler pode preemptar (evict) Pods de menor prioridade para abrir espaço.

## PriorityClass

### Definition
- Non-namespaced object
- Maps priority class name to integer priority value
- Higher value = higher priority

### Fields
- `value`: Integer priority (-2147483648 to 1000000000)
- `globalDefault`: Use for Pods without priorityClassName (only one can be true)
- `description`: Human-readable explanation

### Example
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "High priority for critical services."
```

### Built-in PriorityClasses
- System reserved values > 1000000000
- `system-cluster-critical`: 2000000000
- `system-node-critical`: 2000001000

## Non-preempting PriorityClass

### preemptionPolicy
- `PreemptLowerPriority` (default): Can preempt lower priority pods
- `Never`: Cannot preempt other pods

### Use Case
- High priority jobs that shouldn't disrupt running workloads
- Wait for resources to "naturally" become available
- Still scheduled ahead of lower priority pending pods

### Example
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-nonpreempting
value: 1000000
preemptionPolicy: Never
globalDefault: false
```

## Pod Priority

### Setting Priority
```yaml
apiVersion: v1
kind: Pod
spec:
  priorityClassName: high-priority
  containers:
  - name: nginx
    image: nginx
```

### Scheduling Order
- Pending pods ordered by priority
- Higher priority pods scheduled first
- If high priority pod cannot schedule, scheduler continues with lower priority

## Preemption

### How It Works
1. Pod P pending, cannot find node
2. Preemption logic triggered
3. Find node where removing lower priority pods enables P scheduling
4. Evict victims
5. Schedule P on freed node

### nominatedNodeName
- Status field showing target node for preemption
- Scheduler tracks reserved resources
- Not guaranteed (another node might become available)

### Limitations

#### Graceful Termination
- Victims get graceful termination period (default 30s)
- Time gap between preemption and scheduling
- Can set termination period to zero for faster preemption

#### PodDisruptionBudget
- Respected but not guaranteed
- If no victims found without PDB violation, preemption still happens
- PDB is best-effort, not hard constraint

#### Inter-Pod Affinity
- If pending pod has affinity to lower-priority pods
- Affinity cannot be satisfied after victims removed
- Node not considered for preemption

#### Cross-Node Preemption
- Not supported
- Pod Q on node A, pending pod P has anti-affinity with Q
- P cannot be scheduled even if Q preempted from A
- Future enhancement possibility

## Security Warning

### Risk
- Malicious user could create high-priority pods
- Would cause other pods to be evicted
- Use ResourceQuota to limit PriorityClass usage

### Mitigation
```yaml
apiVersion: v1
kind: ResourceQuota
spec:
  hard:
    pods: "10"
  scopeSelector:
    matchScopes:
    - scopeName: PriorityClass
      operator: In
      values:
      - high-priority
```

## Key Takeaways

1. PriorityClass defines priority levels for pods
2. Higher value = higher priority
3. Non-preempting priority classes don't evict running pods
4. Preemption respects PDB (best-effort)
5. Use ResourceQuota to limit high-priority access
6. System priorities reserved (> 1 billion)

## Personal Notes

Pod Priority é essencial para workloads críticos. A feature de non-preempting é útil para workloads que não devem interromper outros.

Para CKA/CKAD:
- PriorityClass: non-namespaced
- globalDefault: only one per cluster
- system-cluster-critical and system-node-critical are built-in
- Use ResourceQuota to prevent abuse

A limitação de cross-node preemption é importante entender - anti-affinity não pode ser resolvida preemptando pods em outros nodes.