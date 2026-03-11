# Kubernetes Service Accounts Administration - Official Documentation

**Source:** kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

ServiceAccounts fornecem identidade para processos que rodam em Pods. Permitem autenticação ao API server. Tokens podem ser bound a objetos API para limitar validade.

## User Accounts vs Service Accounts

| Aspect | User Account | Service Account |
|--------|--------------|-----------------|
| Purpose | Humans | Application processes |
| Scope | Cluster-wide | Namespaced |
| Creation | Complex business process | Lightweight, on-demand |
| Auditing | Different requirements | Different requirements |

### Key Differences
- User accounts are global (unique across cluster)
- Service accounts are namespaced (same name in different namespaces)
- Service accounts follow principle of least privilege
- Configuration bundles can include service account definitions

## Bound Service Account Tokens

### Purpose
- Tie token validity to API object existence
- Auto-revoke when object deleted

### Supported Object Types
1. **Pod**: Most common, used for projected volume mounts
2. **Secret**: Can revoke by deleting Secret
3. **Node**: Auto-revoke when Node deleted (GA in v1.33+)

### Token Binding
- Object's metadata.name and metadata.uid stored in JWT
- API server verifies these claims on authentication
- If object deleted or pending deletion > 60s: authentication fails

### JWT Structure
```json
{
  "kubernetes.io": {
    "namespace": "my-namespace",
    "node": {
      "name": "my-node",
      "uid": "..."
    },
    "pod": {
      "name": "my-pod",
      "uid": "..."
    },
    "serviceaccount": {
      "name": "my-serviceaccount",
      "uid": "..."
    }
  }
}
```

### Node Information in Tokens (v1.32+)
- Pod-bound tokens include node name and UID
- Not verified by API server
- Useful for integrators (no need to fetch Pod/Node objects)

## TokenRequest API

### Modern Approach
- Short-lived tokens (default: 1 hour)
- Bound to Pod, Secret, or Node
- Automatically refreshed by kubelet
- Projected volume mechanism

### Creating Bound Tokens
```bash
kubectl create token my-sa --bound-object-kind="Pod" --bound-object-name="test-pod"
```

### TokenReview API
- Verify and extract private claims
- Check if bound object still exists
- Offline validation possible with JWT validator

## Projected Volume Mechanism

### Default Behavior (v1.22+)
- ServiceAccount admission controller adds projected volume
- Contains: token, CA cert, namespace

### Example Volume
```yaml
volumes:
- name: kube-api-access-<suffix>
  projected:
    sources:
    - serviceAccountToken:
        path: token
    - configMap:
        items:
        - key: ca.crt
          path: ca.crt
        name: kube-root-ca.crt
    - downwardAPI:
        items:
        - fieldRef:
            apiVersion: v1
            fieldPath: metadata.namespace
          path: namespace
```

### Token Refresh
- Kubelet fetches time-bound tokens
- Default lifespan: 1 hour
- Refreshed before expiry
- Invalidated when Pod deleted

## Manual Secret Management

### Legacy Mechanism
- Before v1.22: auto-created token Secrets
- Long-lived tokens (no expiry)
- Mounted into Pods

### Current Recommendation
- Use TokenRequest API for short-lived tokens
- Manual Secrets for never-expire tokens only

### Auto-generated Legacy Token Cleanup (v1.29+)
- Unused tokens marked invalid after 1 year
- Purged after another year
- Legacy tokens tracked via `kubernetes.io/legacy-token-last-used` label

## Key Takeaways

1. ServiceAccounts provide identity for Pods
2. User accounts = humans, Service accounts = applications
3. Bound tokens tied to Pod/Secret/Node existence
4. TokenRequest API for short-lived tokens (recommended)
5. Projected volume is default mechanism (v1.22+)
6. Manual Secrets for long-lived tokens (use carefully)
7. Legacy tokens cleaned up if unused (v1.29+)

## Personal Notes

ServiceAccounts são fundamentais para segurança de workloads. A feature de bound tokens é importante para rotação automática.

Para CKA/CKAD:
- TokenRequest API: short-lived, bound tokens
- Projected volume: default mechanism for Pod tokens
- Manual Secret: long-lived, use with caution
- TokenReview: verify and extract claims

A cleanup de legacy tokens (v1.29+) é importante para segurança - tokens não usados são automaticamente invalidados. Para produção, sempre usar projected volumes ao invés de Secrets.