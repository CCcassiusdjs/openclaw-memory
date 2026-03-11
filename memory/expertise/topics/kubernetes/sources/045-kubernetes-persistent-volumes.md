# Kubernetes Persistent Volumes - Official Documentation

**Source:** kubernetes.io/docs/concepts/storage/persistent-volumes/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Documentação oficial sobre PersistentVolumes (PV) e PersistentVolumeClaims (PVC). Abstração de storage que separa provisionamento de consumo.

## Introduction

### Problem Statement
- Storage management is distinct from compute management
- Need to abstract storage implementation from consumption
- Different storage types: NFS, iSCSI, cloud-specific

### Two API Resources

#### PersistentVolume (PV)
- Piece of storage in cluster
- Provisioned by admin or dynamically via StorageClass
- Cluster resource (like nodes)
- Lifecycle independent of Pods
- Captures implementation details (NFS, iSCSI, cloud storage)

#### PersistentVolumeClaim (PVC)
- User's request for storage
- Similar to Pod consuming node resources
- PVCs consume PV resources
- Can request specific size and access modes

## Lifecycle of a Volume and Claim

### 1. Provisioning

#### Static
- Admin creates PVs with storage details
- PVs exist in API for consumption

#### Dynamic
- No matching static PV for PVC
- Cluster provisions volume based on StorageClass
- PVC must request storage class
- Empty string "" disables dynamic provisioning

### 2. Binding
- User creates PVC with requirements
- Control loop finds matching PV
- Binds PVC to PV (one-to-one mapping)
- PVC remains unbound if no matching PV

### 3. Using
- Pods use claims as volumes
- Cluster mounts bound volume to Pod
- User specifies access mode when using claim

### 4. Storage Object in Use Protection
- PVCs in use by Pod are protected from deletion
- PVs bound to PVC are protected from deletion
- Status shows "Terating" with finalizer
- Finalizer: `kubernetes.io/pvc-protection`

### 5. Reclaiming

#### Retain
- Manual reclamation
- PV still exists after PVC deletion
- Volume is "released" but not available
- Admin must manually clean up

#### Delete
- Removes PV and associated storage asset
- Default for dynamically provisioned volumes
- Inherit reclaim policy from StorageClass

#### Recycle (Deprecated)
- Basic scrub (rm -rf /volume/*)
- Not recommended
- Use dynamic provisioning instead

## Access Modes

### ReadWriteOnce (RWO)
- Single node can mount as read-write
- Most common access mode

### ReadOnlyMany (ROX)
- Multiple nodes can mount as read-only

### ReadWriteMany (RWX)
- Multiple nodes can mount as read-write

### ReadWriteOncePod (RWO)
- Single Pod can mount as read-write
- Ensures exclusive access

## PersistentVolume Deletion Protection Finalizer

### Feature Status
- Kubernetes v1.33 [stable]
- Ensures PV deleted only after backing storage deleted

### Finalizers
- `external-provisioner.volume.kubernetes.io/finalizer` (CSI volumes)
- `kubernetes.io/pv-controller` (in-tree plugin volumes)

## Reserving a PersistentVolume

### Pre-binding
- Specify PV in PVC to bind to specific PV
- `spec.volumeName` in PVC
- Use `claimRef` in PV to reserve

### Use Case
- Ensure specific PV binds to specific PVC
- Skip normal matching criteria

## Key Takeaways

1. PV = cluster resource, PVC = user request
2. Static vs Dynamic provisioning
3. Three reclaim policies: Retain, Delete, Recycle (deprecated)
4. Access modes: RWO, ROX, RWX, RWOP
5. Protection finalizers prevent data loss
6. StorageClass enables dynamic provisioning

## Personal Notes

PV/PVC é fundamental para storage stateful. A separação entre provisionamento (admin) e consumo (user) é o conceito-chave.

Para CKA/CKAD, memorizar:
- PV: cluster resource (admin)
- PVC: request for storage (user)
- RWO: single node (most common)
- RWX: multiple nodes (requires shared storage)
- Reclaim policies: Delete (default), Retain (manual)

A feature de finalizers é importante para entender proteção de dados - garante que storage não seja deletado antes de dados serem removidos.