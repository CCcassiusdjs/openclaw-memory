# Implementing Kubernetes RBAC - Best Practices

**Fonte:** https://trilio.io/kubernetes-best-practices/kubernetes-rbac/
**Tipo:** Guia
**Data:** 2026-03-12

---

## Resumo

Guia completo de implementação de RBAC no Kubernetes: Roles, ClusterRoles, RoleBindings, ClusterRoleBindings, ServiceAccounts e exemplos práticos.

---

## Componentes RBAC

### Roles e ClusterRoles

| Componente | Escopo | Uso |
|------------|-------|-----|
| **Role** | Namespace | Permissões dentro de um namespace |
| **ClusterRole** | Cluster-wide | Permissões em todos os namespaces + recursos cluster-level |

### Role YAML Example
```yaml
# Role for pod viewing in development namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: pod-viewer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### ClusterRole YAML Example
```yaml
# ClusterRole for monitoring across all namespaces
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: metrics-collector
rules:
- apiGroups: [""]
  resources: ["pods", "nodes"]
  verbs: ["get", "list"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods", "nodes"]
  verbs: ["get", "list"]
```

---

## RoleBindings e ClusterRoleBindings

| Binding | Escopo | Função |
|---------|--------|--------|
| **RoleBinding** | Namespace | Conecta Role a subjects dentro de um namespace |
| **ClusterRoleBinding** | Cluster-wide | Conecta ClusterRole a subjects em todo o cluster |

### RoleBinding Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-pod-viewers
  namespace: development
subjects:
- kind: Group
  name: dev-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-viewer
  apiGroup: rbac.authorization.k8s.io
```

---

## Subjects: Users, Groups, ServiceAccounts

| Subject | Descrição |
|---------|-----------|
| **Users** | Humanos autenticados via X.509 certificates ou external IdP |
| **Groups** | Grupos de users para easier permission management |
| **ServiceAccounts** | Kubernetes objects que fornecem identidade para pods |

### ServiceAccount Example
```yaml
# ServiceAccount for an application
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service
  namespace: development
---
# RoleBinding for the ServiceAccount
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-service-binding
  namespace: development
subjects:
- kind: ServiceAccount
  name: app-service
  namespace: development
roleRef:
  kind: Role
  name: pod-viewer
  apiGroup: rbac.authorization.k8s.io
```

---

## RBAC Evaluation Flow

```
Request → API Server
           ↓
       Authentication (who?)
           ↓
       Authorization (RBAC) ← Roles, Bindings
           ↓
       Admission Control
           ↓
       Execute Action
```

---

## Hands-on Demo

### Step 1: Create Namespaces
```bash
kubectl create namespace dev
kubectl create namespace ops
```

### Step 2: Create ServiceAccounts
```yaml
# service-accounts.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dev-sa
  namespace: dev
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ops-sa
  namespace: ops
```

### Step 3: Define Roles
```yaml
# roles.yaml

# Developer Role - Namespace specific
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
  namespace: dev
rules:
# Allow developers to manage deployments and services
- apiGroups: ["", "apps"]
  resources: ["pods", "pods/log", "deployments", "services"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
# Limited access to pod execution and configs
- apiGroups: [""]
  resources: ["pods/exec", "configmaps"]
  verbs: ["create", "get"]
---
# Operations Role - Cluster-scoped resources
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ops-admin
rules:
# Cluster-level read access for ops team
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
# Namespace-scoped resources
- apiGroups: [""]
  resources: ["namespaces", "pods", "services", "pods/log"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "daemonsets", "statefulsets"]
  verbs: ["get", "list", "watch"]
```

### Step 4: Create RoleBindings
```yaml
# role-bindings.yaml

# Developer RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-binding
  namespace: dev
subjects:
- kind: ServiceAccount
  name: dev-sa
  namespace: dev
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
---
# Operations ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ops-binding
subjects:
- kind: ServiceAccount
  name: ops-sa
  namespace: ops
roleRef:
  kind: ClusterRole
  name: ops-admin
  apiGroup: rbac.authorization.k8s.io
```

### Step 5: Test Permissions
```bash
# Test developer permissions
kubectl auth can-i list pods --as=system:serviceaccount:dev:dev-sa -n dev
# Expected: yes

kubectl auth can-i create deployments --as=system:serviceaccount:dev:dev-sa -n dev
# Expected: yes

kubectl auth can-i list nodes --as=system:serviceaccount:dev:dev-sa
# Expected: no

# Test operations permissions
kubectl auth can-i list pods --as=system:serviceaccount:ops:ops-sa --all-namespaces
# Expected: yes

kubectl auth can-i create deployments --as=system:serviceaccount:ops:ops-sa -n dev
# Expected: no
```

---

## RBAC and Backup Operations

### Considerations
- Backup operators need specific, limited RBAC permissions
- Restore operations must maintain security context
- Backup data requires proper access controls
- Regular validation of permissions

### Trilio Integration
- Operates within RBAC boundaries
- Captures application data + security contexts
- Maintains security posture on restore

---

## OpenShift RBAC

### Default Cluster Roles

| Role | Description |
|------|-------------|
| **admin** | Project manager, view/modify any resource except quota |
| **basic-user** | Basic info about projects and users |
| **cluster-admin** | Super-user, full control |
| **cluster-status** | Basic cluster status info |
| **cluster-reader** | View most objects, no modifications |
| **edit** | Modify most objects, no roles/bindings |
| **self-provisioner** | Create own projects |
| **view** | View most objects, no modifications |

### Additional Features
- Security Context Constraints (SCCs)
- Preconfigured cluster roles
- Extended beyond standard Kubernetes RBAC

---

## Best Practices

| Prática | Descrição |
|---------|-----------|
| **Least Privilege** | Grant minimum permissions needed |
| **Use ServiceAccounts** | For pods, not user accounts |
| **Namespace Isolation** | Use Roles for namespace-scoped access |
| **Regular Audits** | Review bindings periodically |
| **Avoid Wildcards** | Don't use `*` in production |

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Role | Permissões namespace-scoped |
| ClusterRole | Permissões cluster-wide |
| RoleBinding | Conecta Role a subjects |
| ClusterRoleBinding | Conecta ClusterRole a subjects |
| ServiceAccount | Identidade para pods |
| Least Privilege | Conceder mínimo necessário |

---

## Referências

- Kubernetes RBAC Docs: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- RBAC Good Practices: https://kubernetes.io/docs/concepts/security/rbac-good-practices/
- OpenShift RBAC: https://docs.openshift.com/container-platform/4.17/authentication/using-rbac.html