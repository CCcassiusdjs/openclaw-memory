# Kubernetes RBAC Authorization (Official Docs)

**Fonte:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

RBAC (Role-Based Access Control) é o método padrão de autorização em Kubernetes, usando a API rbac.authorization.k8s.io para controlar acesso baseado em roles e bindings.

---

## Habilitando RBAC

```bash
# Via AuthorizationConfiguration
kube-apiserver --authorization-config=/path/to/config.yaml

# Via flag legacy
kube-apiserver --authorization-mode=Node,RBAC
```

---

## API Objects

### Role e ClusterRole
- **Role**: Permissões dentro de um namespace
- **ClusterRole**: Permissões cluster-wide

**Uso de ClusterRole:**
- Permissões em recursos cluster-scoped (nodes)
- Permissões em recursos non-resource (/healthz)
- Permissões em todos os namespaces

### RoleBinding e ClusterRoleBinding
- Vincula roles a subjects (users, groups, service accounts)
- **RoleBinding**: Namespace-specific
- **ClusterRoleBinding**: Cluster-wide

---

## Exemplos

### Role (namespace-scoped)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # core API
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### ClusterRole
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

### RoleBinding
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

### ClusterRoleBinding
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

---

## Regras de Binding

1. **roleRef é imutável** - Não pode ser alterado após criação
2. Para mudar roleRef: deletar binding e recriar
3. RoleBinding pode referenciar ClusterRole (namespace-scoped binding)
4. ClusterRoleBinding aplica ClusterRole em todos namespaces

---

## Referenciando Recursos

### Recursos e Subrecursos
```yaml
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]
```

### Por Nome
```yaml
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["my-configmap"]
  verbs: ["update", "get"]
```

### Wildcards
```yaml
rules:
- apiGroups: ["example.com"]
  resources: ["*"]
  verbs: ["*"]
```

⚠️ **Cuidado:** Wildcards podem conceder acesso excessivo.

---

## Aggregated ClusterRoles

Combina múltiplos ClusterRoles em um:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: [] # Preenchido automaticamente
```

**Benefício:** Adicionar regras para custom resources automaticamente.

---

## Default Roles e Bindings

### User-Facing Roles

| Role | Descrição |
|------|-----------|
| **cluster-admin** | Super-user, full access |
| **admin** | Admin namespace-scoped |
| **edit** | Read/write namespace-scoped |
| **view** | Read-only namespace-scoped |

### Component Roles

| Role | Binding | Descrição |
|------|---------|-----------|
| **system:kube-scheduler** | system:kube-scheduler | Scheduler resources |
| **system:kube-controller-manager** | system:kube-controller-manager | Controller resources |
| **system:node** | None (deprecated) | Kubelet resources |
| **system:node-proxier** | system:kube-proxy | Kube-proxy resources |

### API Discovery Roles

| Role | Binding | Descrição |
|------|---------|-----------|
| **system:basic-user** | system:authenticated | Basic user info |
| **system:discovery** | system:authenticated | API discovery |
| **system:public-info-viewer** | all users | Non-sensitive cluster info |

---

## Subjects

### Users
```yaml
subjects:
- kind: User
  name: "alice@example.com"
  apiGroup: rbac.authorization.k8s.io
```

### Groups
```yaml
subjects:
- kind: Group
  name: "frontend-admins"
  apiGroup: rbac.authorization.k8s.io
```

### Service Accounts
```yaml
# Service account específico
subjects:
- kind: ServiceAccount
  name: default
  namespace: kube-system

# Todos service accounts de um namespace
subjects:
- kind: Group
  name: system:serviceaccounts:qa
  apiGroup: rbac.authorization.k8s.io

# Todos service accounts do cluster
subjects:
- kind: Group
  name: system:serviceaccounts
  apiGroup: rbac.authorization.k8s.io
```

---

## Prefixos Reservados

- `system:` - Reservado para Kubernetes
- `system:serviceaccount:` - Prefixo para SA usernames
- `system:serviceaccounts:` - Prefixo para SA groups

**Não criar** users/groups com prefixo `system:`.

---

## Conceitos-Chave

1. **Role**: Namespace-scoped permissions
2. **ClusterRole**: Cluster-wide permissions (ou cross-namespace)
3. **RoleBinding**: Liga Role a subjects (namespace)
4. **ClusterRoleBinding**: Liga ClusterRole a subjects (cluster)
5. **Aggregation**: Combina roles automaticamente

---

## Best Practices

1. **Least Privilege**: Conceder apenas permissões necessárias
2. **Namespace Isolation**: Usar Role quando possível
3. **Service Accounts**: Um SA por workload
4. **Avoid Wildcards**: Usar recursos/verbs específicos
5. **Audit**: Revisar bindings regularmente

---

## Próximos Passos de Estudo

- [ ] Service Account tokens
- [ ] Impersonation
- [ ] Admission Controllers
- [ ] Audit logging
- [ ] Pod Security Standards integration

---

## Referências

- Kubernetes RBAC: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- RBAC Good Practices: https://kubernetes.io/docs/concepts/security/rbac-good-practices/
- Service Accounts: https://kubernetes.io/docs/concepts/security/service-accounts/