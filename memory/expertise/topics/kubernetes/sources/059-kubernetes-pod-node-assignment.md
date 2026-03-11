# Kubernetes Assigning Pods to Nodes - Official Documentation

**Source:** kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Múltiplos métodos para controlar onde Pods são agendados: nodeSelector, Affinity/Anti-affinity, nodeName, e Topology Spread Constraints.

## Node Labels

### Built-in Labels
- `kubernetes.io/hostname`
- `topology.kubernetes.io/zone`
- `topology.kubernetes.io/region`
- `kubernetes.io/os`
- `kubernetes.io/arch`

### Custom Labels
- Can add arbitrary labels
- Use for workload isolation
- Choose keys kubelet cannot modify

### Node Restriction Labels
- Prefix: `node-restriction.kubernetes.io/`
- Protected by NodeRestriction admission plugin
- Prevents compromised nodes from setting labels

## nodeSelector

### Simplest Method
- Constrain Pod to nodes with matching labels
- All labels must match (AND logic)

### Example
```yaml
apiVersion: v1
kind: Pod
spec:
  nodeSelector:
    disktype: ssd
    zone: west
  containers:
  - name: nginx
    image: nginx
```

## Node Affinity

### Two Types

#### requiredDuringSchedulingIgnoredDuringExecution
- Hard requirement
- Pod won't schedule unless rule met
- Similar to nodeSelector but more expressive

#### preferredDuringSchedulingIgnoredDuringExecution
- Soft preference
- Scheduler tries to satisfy
- Pod still schedules if not met

### Example
```yaml
apiVersion: v1
kind: Pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - antarctica-east1
            - antarctica-west1
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
```

### Operators
- In: label value in list
- NotIn: label value not in list
- Exists: label key exists
- DoesNotExist: label key does not exist
- Gt: label value > integer
- Lt: label value < integer

### Weight
- Range: 1-100
- Used for scoring preferred rules
- Higher weight = higher priority

## Inter-pod Affinity and Anti-affinity

### Purpose
- Schedule based on labels of other Pods
- Not node labels
- Useful for co-location or spreading

### Types
- podAffinity: prefer to schedule with matching pods
- podAntiAffinity: prefer to avoid scheduling with matching pods

### Hard vs Soft
- requiredDuringSchedulingIgnoredDuringExecution: must match
- preferredDuringSchedulingIgnoredDuringExecution: prefer to match

### Topology Key
- Defines topology domain (node, zone, region)
- Uses node labels for domain
- Common: `kubernetes.io/hostname`, `topology.kubernetes.io/zone`

### Example: Co-locate in Same Zone
```yaml
apiVersion: v1
kind: Pod
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: database
        topologyKey: topology.kubernetes.io/zone
```

### Example: Spread Across Zones
```yaml
apiVersion: v1
kind: Pod
spec:
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: web
          topologyKey: topology.kubernetes.io/zone
```

### Performance Warning
- Inter-pod affinity requires significant processing
- Not recommended for clusters > several hundred nodes
- Nodes must be consistently labeled

## nodeName

### Direct Assignment
- Bypasses scheduler
- Pod runs on specified node
- Use for special cases only

### Example
```yaml
apiVersion: v1
kind: Pod
spec:
  nodeName: node1
  containers:
  - name: nginx
    image: nginx
```

## Pod Topology Spread Constraints

### Purpose
- Spread Pods across topology domains
- Achieve high availability
- Efficient resource utilization

### Fields
- `topologyKey`: domain (zone, node, etc.)
- `maxSkew`: allowed difference in Pod count
- `whenUnsatisfiable`: DoNotSchedule or ScheduleAnyway
- `labelSelector`: which Pods to consider

### Example
```yaml
apiVersion: v1
kind: Pod
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: web
```

## Key Takeaways

1. nodeSelector: simplest, label matching
2. Node Affinity: expressive node selection
3. Inter-pod Affinity: schedule based on other pods
4. nodeName: bypass scheduler (special cases)
5. Topology Spread: distribute across domains
6. Use node labels for isolation

## Personal Notes

Node Affinity e Inter-pod Affinity são poderosos para controle de agendamento. A combinação com Taints oferece controle total.

Para CKA/CKAD:
- nodeSelector: simple label matching
- nodeAffinity: required (hard) and preferred (soft)
- podAffinity: co-locate with matching pods
- podAntiAffinity: spread from matching pods
- topologySpreadConstraints: even distribution

A feature de Node Restriction Labels é importante para segurança - previne nodes comprometidos de atrair workloads sensíveis.