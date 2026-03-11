# Kubernetes RBAC - Official Documentation

**Source:** kubernetes.io/docs/reference/access-authn-authz/rbac/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

RBAC (Role-Based Access Control) regula acesso a recursos do Kubernetes baseado em roles de usuários. Usa a API group `rbac.authorization.k8s.io` para autorização dinâmica via Kubernetes API.

## API Objects

### Four Types of RBAC Objects

| Object | Scope | Description |
|--------|-------|-------------|
| Role | Namespace | Permissões dentro de um namespace |
| ClusterRole | Cluster-wide | Permissões cluster-wide |
| RoleBinding | Namespace | Vincula Role a usuários no namespace |
| ClusterRoleBinding | Cluster-wide | Vincula ClusterRole a usuários cluster-wide |

## Role and ClusterRole

### Role Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]  # Core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### ClusterRole Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### When to Use Each

**Role:**
- Permissions within a single namespace

**ClusterRole:**
- Cluster-scoped resources (nodes)
- Non-resource endpoints (/healthz)
- Namespaced resources across all namespaces

## RoleBinding and ClusterRoleBinding

### RoleBinding Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### RoleBinding with ClusterRole
- RoleBinding can reference a ClusterRole
- Permissions are scoped to the RoleBinding's namespace
- Useful for reusable role definitions

### ClusterRoleBinding Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: manager
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

## Referring to Resources

### Resource Names
- Use `resourceNames` to restrict to specific resource instances
- Only works for get, update, delete (not list/watch)

```yaml
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["my-configmap"]
  verbs: ["update", "get"]
```

### Subresources
```yaml
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]
```

### Wildcards
```yaml
rules:
- apiGroups: ["example.com"]
  resources: ["*"]
  verbs: ["*"]
```

**Warning:** Wildcards grant access to future resources too.

## Aggregated ClusterRoles

### Purpose
- Combine multiple ClusterRoles into one
- Controller merges rules from matching ClusterRoles

### Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: []  # Controller fills this
```

## Privilege Escalation Prevention

### Key Rule
- Cannot create binding to role with more permissions than you have
- Cannot grant permissions you don't possess

### Implication
- Users with binding creation rights cannot escalate their own permissions

## Key Takeaways

1. RBAC has 4 objects: Role, ClusterRole, RoleBinding, ClusterRoleBinding
2. Role/RoleBinding are namespace-scoped
3. ClusterRole/ClusterRoleBinding are cluster-wide
4. RoleBinding can reference ClusterRole (scoped to namespace)
5. Permissions are additive only (no deny rules)
6. Aggregated ClusterRoles enable reusable role composition
7. Privilege escalation is prevented by design

## Personal Notes

RBAC é fundamental para segurança Kubernetes. A distinção entre Role/RoleBinding e ClusterRole/ClusterRoleBinding é essencial.

Para CKA/CKAD:
- Role: namespace-scoped permissions
- ClusterRole: cluster-wide permissions
- RoleBinding: binds Role to users in namespace
- ClusterRoleBinding: binds ClusterRole to users cluster-wide

A feature de Aggregated ClusterRoles é poderosa para composição de roles reutilizáveis. O roleRef é imutável - para mudar, deve deletar e recriar o binding.