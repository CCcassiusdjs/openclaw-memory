# Kubernetes DaemonSets - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/controllers/daemonset/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

DaemonSets garantem que todos (ou alguns) Nodes executem uma cópia de um Pod. Útil para facilities node-local como logging, monitoring, e networking.

## What is a DaemonSet?

### Definition
- Ensures a Pod copy runs on all (or some) nodes
- Automatically adds Pods to new nodes
- Garbage collects Pods when nodes removed
- Deleting DaemonSet cleans up created Pods

### Typical Use Cases
1. Cluster storage daemon on every node
2. Log collection daemon on every node
3. Node monitoring daemon on every node
4. Network plugin components

## DaemonSet Spec

### Required Fields
- `apiVersion`: apps/v1
- `kind`: DaemonSet
- `metadata`: name, labels
- `spec`: selector, template

### Example
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      # Allow running on control plane nodes
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: quay.io/fluentd_elasticsearch/fluentd:v5.0.1
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

## Pod Template

### Key Requirements
- Must specify appropriate labels
- Labels must match selector
- RestartPolicy must be Always (or unspecified)
- Selector cannot be changed after creation

## Running on Selected Nodes

### Node Selector
- Use `.spec.template.spec.nodeSelector`
- Creates Pods only on matching nodes

### Node Affinity
- Use `.spec.template.spec.affinity`
- More flexible node selection

### Default Behavior
- If neither specified, runs on all nodes

## How Daemon Pods are Scheduled

### Scheduling Process
1. DaemonSet controller creates Pod for each eligible node
2. Adds nodeAffinity to match target host
3. Default scheduler binds Pod to target host
4. If Pod doesn't fit, may preempt existing Pods

### Priority
- Set `.spec.template.spec.priorityClassName` for higher priority
- Ensures DaemonSet Pods can preempt others

## Taints and Tolerations

### Automatic Tolerations

| Toleration Key | Effect | Details |
|----------------|--------|---------|
| node.kubernetes.io/not-ready | NoExecute | Pods run on unhealthy nodes |
| node.kubernetes.io/unreachable | NoExecute | Pods run on unreachable nodes |
| node.kubernetes.io/disk-pressure | NoSchedule | Pods run on disk-pressure nodes |
| node.kubernetes.io/memory-pressure | NoSchedule | Pods run on memory-pressure nodes |
| node.kubernetes.io/pid-pressure | NoSchedule | Pods run on PID-pressure nodes |
| node.kubernetes.io/unschedulable | NoSchedule | Pods run on unschedulable nodes |
| node.kubernetes.io/network-unavailable | NoSchedule | Pods run on network-unavailable nodes (hostNetwork only) |

### Why Tolerations Matter
- DaemonSet Pods can run on nodes not ready
- Critical for cluster bootstrapping (e.g., network plugin)
- Prevents deadlock: node not ready because network plugin not running

## Communicating with Daemon Pods

### Patterns
1. **Push** - Pods send data to external service (no clients)
2. **NodeIP + Known Port** - Use hostPort, clients know node IPs
3. **DNS** - Headless service with same selector, discover via endpoints
4. **Service** - Service with same selector, random node selection

## Updating a DaemonSet

### Rolling Update
- Modify Pod template to trigger update
- Controlled by updateStrategy
- Can use `OnDelete` or `RollingUpdate`

### OnDelete Strategy
- Pods not updated automatically
- Manual deletion triggers recreation

### RollingUpdate Strategy
- Automatic updates
- Controlled by `maxUnavailable` parameter

## Alternatives to DaemonSet

### Init Scripts
- Running daemons directly on node (systemd, upstart)
- Advantages: monitoring, unified config, resource limits

### Bare Pods
- Create Pods directly on specific nodes
- DaemonSet is better: handles node failure, maintenance

### Static Pods
- Written to directory watched by kubelet
- Not managed by API server
- Useful for control plane bootstrapping
- May be deprecated in future

### Deployments
- For stateless services where scaling > node placement
- DaemonSet: Pod MUST run on specific nodes
- Deployment: Pod placement is flexible

## Key Takeaways

1. DaemonSet ensures one Pod per node (or subset)
2. Automatic tolerations for node problems
3. Use for node-level infrastructure (logging, monitoring, networking)
4. Can select specific nodes via nodeSelector/affinity
5. Two update strategies: OnDelete, RollingUpdate
6. Prefer DaemonSet over static Pods or bare Pods

## Personal Notes

DaemonSets são críticos para cluster infrastructure. A feature de automatic tolerations é importante para entender porque network plugins podem rodar em nodes not ready.

Para CKA/CKAD:
- DaemonSet = one Pod per node
- Use tolerations for control plane nodes
- Use priorityClassName for critical DaemonSets
- Update strategies: OnDelete vs RollingUpdate

A diferença para Deployments: DaemonSet controla onde Pod roda, Deployment controla quantas réplicas.