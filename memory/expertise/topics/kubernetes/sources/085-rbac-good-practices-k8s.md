# RBAC Good Practices - Kubernetes Official

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/security/rbac-good-practices/
**Data:** Janeiro 2026
**Tópico:** RBAC Security, Least Privilege, Service Accounts, Privilege Escalation
**Status:** Lido

---

## Resumo Executivo

Melhores práticas oficiais para design de RBAC em Kubernetes, cobrindo princípios de least privilege, minimização de tokens privilegiados, hardening, e riscos de escalação de privilégios.

---

## Princípios Gerais

### Least Privilege
- Atribuir permissões mínimas necessárias
- Usar RoleBindings (namespace) em vez de ClusterRoleBindings
- Evitar wildcard permissions (especialmente `*`)
- Não usar `cluster-admin` exceto quando necessário
- Evitar adicionar usuários ao grupo `system:masters`

### Minimizar Distribuição de Tokens Privilegiados
- Pods não devem ter service accounts com permissões elevadas
- Limitar nodes que rodam pods poderosos
- Usar Taints/Tolerations e PodAntiAffinity para isolar
- Separar workloads por nível de confiança

### Hardening
- Revisar bindings para `system:unauthenticated` (remover se possível)
- Evitar auto-mount de tokens: `automountServiceAccountToken: false`
- Aplicar Pod Security Standards (Baseline/Restricted)

### Revisão Periódica
- Revisar RBAC regularmente para entradas redundantes
- Atenção a usuários deletados (herança de direitos)
- Verificar possíveis caminhos de escalação

---

## Riscos de Escalação de Privilégios

### 1. Listar Secrets
- `get` access lê conteúdo
- `list` e `watch` também revelam conteúdo
- Resposta de `kubectl get secrets -A -o yaml` inclui dados

### 2. Criação de Workloads
- Criar Pods/Deployments concede acesso a:
  - Secrets do namespace
  - ConfigMaps
  - PersistentVolumes montáveis
- Pods podem usar qualquer ServiceAccount do namespace
- Pods privilegiados podem acessar nodes

### 3. Criação de PersistentVolumes
- Permite criar `hostPath` volumes
- Acesso ao filesystem do node
- Escalação para credenciais de sistema

### 4. Acesso ao nodes/proxy
- Acesso à API do Kubelet
- Execução de comandos em todos pods do node
- Bypass de audit e admission control

### 5. Verbos Perigosos

| Verbo | Risco |
|-------|-------|
| `escalate` | Criar roles com mais permissões que o próprio |
| `bind` | Criar bindings para roles que não possui |
| `impersonate` | Assumir identidade de outros usuários |

### 6. CSRs e Certificados
- `create` em CSRs + `update` em `certificatesigningrequests/approval`
- Permite criar certificados client arbitrários
- Possível escalação para system components

### 7. Token Request
- `create` em `serviceaccounts/token`
- Emite tokens para service accounts existentes

### 8. Admission Webhooks
- Controle sobre `validatingwebhookconfigurations`
- Controle sobre `mutatingwebhookconfigurations`
- Pode ler/mutar qualquer objeto admitido

### 9. Modificação de Namespaces
- `patch` em Namespace objects
- Mudar labels pode afetar Pod Security Admission
- Pode afetar NetworkPolicies indiretamente

---

## Riscos de Negação de Serviço

### Criação de Objetos
- Objetos grandes podem causar OOM no etcd
- Multi-tenant clusters são vulneráveis
- Mitigação: Resource Quotas para limitar quantidade

---

## Best Practices Resumidas

### Para Usuários
```yaml
# Use RoleBinding (namespace-scoped)
kind: RoleBinding
# Não ClusterRoleBinding

# Evite wildcards
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]  # Não use ["*"]

# Use nomes específicos
resourceNames: ["my-pod"]  # Restringe a recursos específicos
```

### Para Service Accounts
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-sa
automountServiceAccountToken: false  # Não montar por padrão
```

### Para Pods
```yaml
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: my-sa
  automountServiceAccountToken: false  # Sobrescreve SA default
  containers:
  - name: app
    # ...
```

### Namespace Isolation
```yaml
# Use namespaces para separar níveis de confiança
apiVersion: v1
kind: Namespace
metadata:
  name: trusted-workloads
  labels:
    pod-security.kubernetes.io/enforce: restricted
```

---

## Insights para Kubernetes

1. **RBAC é crítico**: Principal controle de segurança
2. **Least privilege obrigatório**: Permissões mínimas necessárias
3. **Namespace boundaries**: Use namespaces para isolar
4. **Verbs perigosos**: `escalate`, `bind`, `impersonate` requerem cuidado
5. **Revisão contínua**: RBAC deve ser auditado regularmente

---

## Palavras-Chave
`rbac` `security` `least-privilege` `service-accounts` `privilege-escalation` `kubernetes` `hardening`