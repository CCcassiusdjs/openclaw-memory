# Kubernetes Nodes - Official Documentation

**Source:** kubernetes.io/docs/concepts/architecture/nodes/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Documentação oficial sobre Nodes Kubernetes. Um Node é uma máquina (virtual ou física) que executa Pods. Cada Node contém os serviços necessários para rodar containers.

## Node Management

### Adding Nodes
1. **Self-registration** (default): kubelet registers to API server
2. **Manual addition**: User creates Node object manually

### Self-Registration
- `--register-node=true` (default)
- `--kubeconfig`: credentials path
- `--cloud-provider`: cloud metadata
- `--register-with-taints`: register with taints
- `--node-ip`: IP addresses for node
- `--node-labels`: labels on registration
- `--node-status-update-frequency`: heartbeat interval

### Manual Administration
- Create Node objects via kubectl
- Set `--register-node=false`
- Can modify Node objects regardless

### Node Roles
- Set via `node-role.kubernetes.io/<role>` labels
- Value is ignored by Kubernetes (use convention)
- Example: `node-role.kubernetes.io/control-plane: control-plane`

## Node Status

### Components
- **Addresses**: Hostname, ExternalIP, InternalIP
- **Conditions**: Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable
- **Capacity and Allocatable**: CPU, memory, storage
- **Info**: Kernel, OS, kubelet version, container runtime

### Conditions

| Condition | Description |
|-----------|-------------|
| Ready | Node healthy and schedulable |
| MemoryPressure | Node memory low |
| DiskPressure | Disk space low |
| PIDPressure | Too many processes |
| NetworkUnavailable | Network not configured |

## Node Heartbeats

### Two Forms
1. **Node status updates**: Updates to `.status`
2. **Lease objects**: `kube-node-lease` namespace

### Purpose
- Determine node availability
- Take action on failures
- Control plane checks node health

## Node Controller

### Roles
1. Assign CIDR block to nodes (if enabled)
2. Sync node list with cloud provider
3. Monitor node health

### Health Monitoring
- Updates Ready condition
- Sets to Unknown if unreachable
- Triggers API-initiated eviction

### Eviction Behavior
- Default: 5 minutes before eviction
- Rate limit: 0.1 per second (1 node per 10 seconds)
- Per-zone handling for availability zones

### Rate Limits
- `--node-eviction-rate`: 0.1 (default)
- `--unhealthy-zone-threshold`: 0.55 (55%)
- `--large-cluster-size-threshold`: 50 nodes
- `--secondary-node-eviction-rate`: 0.01

## Node Controller Actions

1. Node unreachable → Ready=Unknown
2. After timeout → Evict pods
3. If zone unhealthy → Reduce eviction rate
4. If small cluster → Stop evictions
5. If all zones down → No evictions

## Resource Capacity Tracking

- Nodes report capacity during registration
- Scheduler ensures enough resources for Pods
- Sum of requests < Node capacity
- Excludes non-kubelet containers

## Node Topology

- TopologyManager for resource alignment
- Helps with NUMA, device assignment
- Feature stable since v1.27

## Key Takeaways

1. Nodes can self-register or be manual
2. Node status includes addresses, conditions, capacity
3. Heartbeats use status updates and Lease objects
4. Node controller monitors health and evicts pods
5. Eviction rate limits prevent cascade failures
6. Zone-aware behavior for multi-zone clusters

## Personal Notes

Nodes são a unidade básica de compute no Kubernetes. O Node Controller é crítico para alta disponibilidade.

Para CKA/CKAD:
- kubectl cordon: mark unschedulable
- kubectl drain: evict pods safely
- kubectl uncordon: mark schedulable
- Conditions: Ready, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable

A feature de Zone-aware eviction é importante para entender comportamento em cloud multi-zone. DaemonSets toleram nodes unschedulable por design.