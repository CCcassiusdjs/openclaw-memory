# Kubernetes StatefulSets - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/controllers/statefulset/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

StatefulSets gerenciam aplicações stateful, mantendo identidade persistente para cada Pod. Útil para aplicações que precisam de storage persistente ou identidade de rede estável.

## What is a StatefulSet?

### Definition
- Manages deployment and scaling of Pods
- Provides ordering and uniqueness guarantees
- Maintains sticky identity for each Pod
- Pods are NOT interchangeable

### Key Difference from Deployments
- Deployments: stateless, interchangeable Pods
- StatefulSets: stateful, unique persistent identities

## Use Cases

StatefulSets are valuable for applications requiring:
1. **Stable network identifiers** - Pod hostname persists across rescheduling
2. **Stable persistent storage** - Volume persists across Pod lifetime
3. **Ordered deployment/scaling** - Sequential Pod creation/deletion
4. **Ordered rolling updates** - Controlled update sequence

## Limitations

1. Storage must be provisioned by PersistentVolume Provisioner or pre-provisioned
2. Deleting/scaling down does NOT delete volumes (data safety)
3. Requires a Headless Service for network identity
4. No guarantees on Pod termination when StatefulSet is deleted
5. Rolling updates can get into broken states requiring manual intervention

## Components

### Headless Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None  # Headless
  selector:
    app: nginx
```

### StatefulSet
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"  # Headless Service
  replicas: 3
  minReadySeconds: 10
  template:
    metadata:
      labels:
        app: nginx
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: registry.k8s.io/nginx-slim:0.24
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

## Pod Identity

### Ordinal Index
- N replicas → Pods numbered 0 to N-1
- Pod name: `$(statefulset name)-$(ordinal)`
- Example: web-0, web-1, web-2

### Stable Network ID
- Hostname pattern: `$(statefulset name)-$(ordinal)`
- Domain: `$(service name).$(namespace).svc.cluster.local`
- Full DNS: `$(podname).$(governing service domain)`

### Stable Storage
- Each Pod gets its own PersistentVolumeClaim
- VolumeClaimTemplate creates one PVC per Pod
- Volumes persist across Pod rescheduling
- Volumes NOT deleted when StatefulSet deleted

## Deployment and Scaling Guarantees

### Ordered Deployment
- Pods created sequentially: 0, 1, 2, ..., N-1
- Pod N not created until N-1 is Running and Ready

### Ordered Deletion
- Pods terminated in reverse order: N-1, N-2, ..., 0
- Pod N-1 not terminated until N is fully shutdown

### Pod Management Policies

#### OrderedReady (Default)
- Sequential creation/deletion
- Wait for each Pod to be ready before next

#### Parallel
- Create/terminate all Pods simultaneously
- No ordering guarantees
- Faster scaling and updates

## Update Strategies

### OnDelete
- Pods not updated automatically
- Must manually delete Pods to trigger recreation
- Useful for controlled rollout

### RollingUpdate (Default)
- Automatic rolling updates
- Controlled by `partition` and `maxUnavailable` parameters
- Updates from highest ordinal to lowest

## Key Takeaways

1. StatefulSets maintain unique Pod identities
2. Each Pod gets stable hostname and persistent storage
3. Ordered deployment/scaling by default
4. Requires Headless Service for network identity
5. volumeClaimTemplate creates one PVC per Pod
6. Volumes persist after StatefulSet deletion

## Personal Notes

StatefulSets são essenciais para bancos de dados e aplicações stateful. O conceito de identidade persistente é o diferencial.

Para CKA/CKAD:
- Ordinal index: web-0, web-1, web-2
- DNS: web-0.nginx.default.svc.cluster.local
- Storage: volumeClaimTemplate creates PVC per Pod
- Scaling: ordered by default, can use parallel policy

A diferença crítica é que volumes NÃO são deletados quando StatefulSet é deletado - isso é intencional para proteger dados.