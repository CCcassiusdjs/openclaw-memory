# Kubernetes Taints and Tolerations - Official Documentation

**Source:** kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Taints e Tolerations controlam onde Pods podem ser agendados. Taints são aplicados a Nodes para repelir Pods, Tolerations são aplicados a Pods para permitir agendamento em Nodes com Taints.

## Concepts

### Taint
- Applied to nodes
- Repels pods without matching toleration
- Format: `key=value:effect`

### Toleration
- Applied to pods
- Allows scheduling on tainted nodes
- Format: key, operator, value, effect

## Creating Taints and Tolerations

### Add Taint to Node
```bash
kubectl taint nodes node1 key1=value1:NoSchedule
```

### Remove Taint
```bash
kubectl taint nodes node1 key1=value1:NoSchedule-
```

### Pod Toleration
```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
```

## Toleration Matching Rules

A toleration "matches" a taint if:
1. Keys are the same
2. Effects are the same
3. One of:
   - Operator is Exists (no value needed)
   - Operator is Equal and values match

### Special Cases
- Empty key + Exists operator: matches all keys
- Empty effect: matches all effects with matching key

## Taint Effects

| Effect | Behavior |
|--------|----------|
| NoExecute | Evicts running pods without toleration; prevents new scheduling |
| NoSchedule | Prevents scheduling (soft block) |
| PreferNoSchedule | Tries to avoid scheduling (preference) |

### NoExecute Details
- Pods without toleration: evicted immediately
- Pods with toleration (no seconds): stay forever
- Pods with tolerationSeconds: evicted after specified time

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
  tolerationSeconds: 3600
```

## Multiple Taints and Tolerations

Kubernetes processes multiple taints like a filter:
1. Start with all node taints
2. Ignore taints with matching tolerations
3. Apply effects of remaining taints

### Logic
- If any un-ignored taint has NoSchedule → no scheduling
- If any un-ignored taint has PreferNoSchedule → try to avoid
- If any un-ignored taint has NoExecute → evict

## Numeric Comparison Operators (v1.35 alpha)

### Gt and Lt Operators
- Gt: taint value > toleration value
- Lt: taint value < toleration value

### Use Case
- Threshold-based scheduling
- SLA tier matching
- Reliability level matching

### Example
```bash
# Node taint
kubectl taint nodes node1 servicelevel=950:NoSchedule

# Pod toleration (Gt: 950 > 900)
tolerations:
- key: "servicelevel"
  operator: "Gt"
  value: "900"
  effect: "NoSchedule"
```

## Built-in Node Taints

| Taint | Condition |
|-------|-----------|
| node.kubernetes.io/not-ready | Node Ready=False |
| node.kubernetes.io/unreachable | Node Ready=Unknown |
| node.kubernetes.io/memory-pressure | Memory pressure |
| node.kubernetes.io/disk-pressure | Disk pressure |
| node.kubernetes.io/pid-pressure | PID pressure |
| node.kubernetes.io/network-unavailable | Network unavailable |
| node.kubernetes.io/unschedulable | Node unschedulable |

## Use Cases

### 1. Dedicated Nodes
- Taint nodes with dedicated=groupName:NoSchedule
- Add toleration to authorized pods

### 2. Special Hardware
- Taint GPU nodes with special=true:NoSchedule
- Only pods needing GPU have toleration

### 3. Taint-based Evictions
- Node problems trigger automatic taints
- Pods can specify tolerationSeconds for graceful eviction

## Key Takeaways

1. Taints repel pods, tolerations allow scheduling
2. Three effects: NoExecute, NoSchedule, PreferNoSchedule
3. Multiple taints processed like filter
4. Built-in taints for node problems
5. tolerationSeconds for graceful eviction
6. Numeric operators (Gt/Lt) for threshold-based scheduling

## Personal Notes

Taints and Tolerations são fundamentais para controle de agendamento. A combinação com Node Affinity é poderosa.

Para CKA/CKAD:
- kubectl taint nodes <node> key=value:effect
- NoExecute: evicts pods, NoSchedule: prevents scheduling
- tolerationSeconds: graceful eviction time
- Built-in taints: not-ready, unreachable, memory-pressure, etc.

A feature de numeric operators é nova (v1.35 alpha) e útil para SLA-based scheduling. DaemonSets automaticamente toleram todos os taints por isso rodam em todos os nodes.