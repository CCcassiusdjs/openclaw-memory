# RBAC Authorization

**Source:** https://kubernetes.io/docs/reference/access-authn-authz/rbac/
**Type:** Official Documentation
**Category:** RBAC/Auth
**Read:** 2026-03-11

---

## Resumo

### API Objects RBAC

| Objeto | Escopo | Descrição |
|--------|--------|-----------|
| **Role** | Namespace | Permissões dentro de um namespace |
| **ClusterRole** | Cluster | Permissões cluster-wide ou cross-namespace |
| **RoleBinding** | Namespace | Liga Role/ClusterRole a sujeitos em um namespace |
| **ClusterRoleBinding** | Cluster | Liga ClusterRole a sujeitos cluster-wide |

### Role Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # Core API group
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

---

## Conceitos-Chave

### 1. Permissões Puramente Aditivas
- **Não existe "deny"** - apenas permissões positivas
- Regras são acumulativas

### 2. roleRef é Imutável
- Uma vez criado binding, não pode mudar o roleRef
- Para trocar a Role, precisa deletar e recriar o Binding
- `kubectl auth reconcile` ajuda nisso

### 3. Subresources
```yaml
# Exemplo: ler pods e logs
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]
```

### 4. resourceNames (Restrição por Nome)
```yaml
# Exemplo: apenas um ConfigMap específico
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["my-configmap"]
  verbs: ["get", "update"]
```

### 5. Wildcards
```yaml
# CUIDADO: Muito permissivo
rules:
- apiGroups: ["example.com"]
  resources: ["*"]
  verbs: ["*"]
```

### 6. Aggregated ClusterRoles
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
rules: [] # Preenchido automaticamente pelo control plane
```

---

## Subjects (Sujeitos)

| Tipo | Descrição |
|------|-----------|
| **User** | Usuário externo (gerenciado por auth provider) |
| **Group** | Grupo de usuários |
| **ServiceAccount** | Conta de serviço do Kubernetes |

---

## Default Roles (Built-in)

| Role | Escopo | Uso |
|------|--------|-----|
| **cluster-admin** | Cluster | Super-user, tudo permitido |
| **admin** | Namespace | Admin de namespace |
| **edit** | Namespace | Editar recursos (não roles) |
| **view** | Namespace | Apenas leitura |

---

## Checklist RBAC

- [ ] Usar **least privilege**
- [ ] Evitar wildcards (*)
- [ ] Namespaces para isolar ambientes
- [ ] ServiceAccounts para workloads
- [ ] Auditar bindings regularmente
- [ ] Usar grupos em vez de usuários individuais