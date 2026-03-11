# Kubernetes Garbage Collection - Official Documentation

**Source:** kubernetes.io/docs/concepts/architecture/garbage-collection/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Garbage Collection é o mecanismo do Kubernetes para limpar recursos do cluster. Remove Pods terminados, Jobs completos, containers não utilizados, e imagens antigas.

## What Garbage Collection Cleans

1. **Terminated Pods**
2. **Completed Jobs** (with TTL)
3. **Objects without owner references**
4. **Unused containers and images**
5. **Dynamically provisioned PVs** (with Delete reclaim)
6. **Stale/expired CSRs**
7. **Deleted Nodes** (cloud controller)
8. **Node Lease objects**

## Owners and Dependents

### Owner References
- Link objects together
- Tell control plane which objects depend on others
- Enable cleanup before deletion

### Key Rules
- Cross-namespace owner references are disallowed
- Namespaced dependents can reference cluster-scoped owners
- Namespaced owners must be in same namespace as dependent

### Example
- Service creates EndpointSlice
- EndpointSlice has labels AND owner reference
- Owner reference prevents interference from other controllers

## Cascading Deletion

### Foreground Cascading Deletion
1. Owner enters "deletion in progress" state
2. API sets `metadata.deletionTimestamp`
3. API sets `metadata.finalizers=foregroundDeletion`
4. Controller deletes dependents first
5. Controller deletes owner last

### Background Cascading Deletion (Default)
1. API server deletes owner immediately
2. Garbage collector cleans up dependents in background
3. Faster but dependents may briefly remain

### Orphaned Dependents
- Dependents left behind when owner deleted
- Default: Kubernetes deletes dependents
- Override with orphan deletion policy

## Finalizers

- Prevent deletion until cleanup complete
- `metadata.finalizers` field
- Controller removes finalizer when ready
- Object deleted only when finalizers empty

## Container and Image Garbage Collection

### Kubelet Garbage Collection
- Images: every 5 minutes
- Containers: every 1 minute
- Don't use external GC tools (breaks kubelet)

### Disk Usage Limits
- `HighThresholdPercent`: triggers GC
- `LowThresholdPercent`: stops GC
- GC deletes oldest images first

### Container GC Variables
- `MinAge`: minimum age for GC
- `MaxPerPodContainer`: max dead containers per Pod
- `MaxContainers`: max total dead containers

### Image Maximum GC Age
- `imageMaximumGCAge`: max time unused
- Independent of disk usage
- Resets on kubelet restart

## Configuring Garbage Collection

### For Objects
- Cascading deletion policies
- TTL controller for Jobs
- Finalizers for custom cleanup

### For Containers/Images
- Kubelet configuration file
- KubeletConfiguration resource type

## Key Takeaways

1. GC cleans terminated Pods, completed Jobs, unused containers/images
2. Owner references link objects for cascade deletion
3. Cross-namespace owner references are disallowed
4. Two cascade modes: Foreground (dependents first) and Background (owner first)
5. Finalizers block deletion until cleanup complete
6. Kubelet GC runs every 5 min (images) and 1 min (containers)
7. Disk thresholds trigger automatic cleanup

## Personal Notes

Garbage Collection é essencial para evitar resource leaks. A distinção entre foreground e background cascade é importante.

Para CKA/CKAD:
- Foreground: dependents deleted before owner
- Background: owner deleted first (default)
- Orphan: dependents left behind
- Finalizers block deletion

A feature de TTL para Jobs é útil para cleanup automático - evita acumulação de Jobs antigos. O imageMaximumGCAge é importante para imagens que nunca são usadas mesmo com disk space disponível.