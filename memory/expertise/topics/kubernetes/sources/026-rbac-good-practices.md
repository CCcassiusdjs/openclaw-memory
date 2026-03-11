# Kubernetes RBAC Good Practices (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/security/rbac-good-practices/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Boas práticas de segurança para RBAC em Kubernetes, focando em least privilege e prevenção de privilege escalation.

---

## General Good Practice

### Least Privilege (Princípio Básico)
- Atribuir apenas permissões explicitamente necessárias
- Usar RoleBindings (namespace) vs ClusterRoleBindings (cluster)
- Evitar wildcards (`*`)
- Não usar `cluster-admin` exceto quando necessário

### Minimizar Distribuição de Tokens Privilegiados
- Limitar número de nodes rodando pods privilegiados
- Usar Taints/Tolerations para isolamento
- NodeAffinity para separar workloads
- Evitar rodar pods privilegiados junto com não-confiáveis

### Hardening

**Revisar defaults:**
- Remover bindings para `system:unauthenticated`
- Desabilitar auto-mount de tokens: `automountServiceAccountToken: false`

### Periodic Review
- Revisar RBAC regularmente
- Remover entradas redundantes
- Verificar privilege escalations

---

## Privilege Escalation Risks

### Listing Secrets
⚠️ **CUIDADO:** `list` e `watch` em Secrets permitem ler conteúdo!

```yaml
# ISSO EXPÕE CONTEÚDO DE SECRETS
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["list", "watch"]  # Equivalente a "get" para conteúdo
```

**Recomendação:** Apenas `get` em Secrets específicos.

### Workload Creation
Permissão de criar Pods/workloads implica acesso a:
- Secrets no namespace
- ConfigMaps
- PersistentVolumes
- ServiceAccount tokens de qualquer SA no namespace

**Risco:** Pods privilegiados podem escalar para node access.

**Mitigação:**
- Enforced Pod Security Standards (Baseline/Restricted)
- Namespace isolation
- Trust boundaries

### Persistent Volume Creation
⚠️ **CRÍTICO:** Criar PVs permite criar `hostPath` volumes = host filesystem access!

**Risco:** Escape de container, leitura de dados de outros containers, abuso de credenciais de sistema.

**Mitigação:**
- Apenas usuários confiáveis podem criar PVs
- Usar PVCs (PersistentVolumeClaims) para workloads

### Access to Nodes/Proxy Subresource
```yaml
rules:
- apiGroups: [""]
  resources: ["nodes/proxy"]
  verbs: ["get"]  # NÃO É READ-ONLY!
```

**Risco:** Acesso ao Kubelet API = command execution em todos os Pods do node.

**Bypass:** Audit logging e admission control.

### Escalate Verb
```yaml
rules:
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["roles", "clusterroles"]
  verbs: ["create", "escalate"]
```

**Risco:** Permite criar roles com mais permissões que o usuário possui.

### Bind Verb
```yaml
rules:
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["rolebindings", "clusterrolebindings"]
  verbs: ["create", "bind"]
```

**Risco:** Permite criar bindings para roles que o usuário não possui.

### Impersonate Verb
```yaml
rules:
- apiGroups: [""]
  resources: ["users", "groups", "serviceaccounts"]
  verbs: ["impersonate"]
```

**Risco:** Permite assumir identidade de outros usuários.

### CSRs and Certificate Issuing
```yaml
rules:
- apiGroups: ["certificates.k8s.io"]
  resources: ["certificatesigningrequests"]
  verbs: ["create"]
- apiGroups: ["certificates.k8s.io"]
  resources: ["certificatesigningrequests/approval"]
  verbs: ["update"]
```

**Risco:** Criar client certificates = nova identidade no cluster.

### Token Request
```yaml
rules:
- apiGroups: [""]
  resources: ["serviceaccounts/token"]
  verbs: ["create"]
```

**Risco:** Emitir tokens para SAs existentes.

### Control Admission Webhooks
```yaml
rules:
- apiGroups: ["admissionregistration.k8s.io"]
  resources: ["validatingwebhookconfigurations", "mutatingwebhookconfigurations"]
  verbs: ["*"]
```

**Risco:** Controlar webhooks = ler/modificar qualquer objeto admitido.

### Namespace Modification
```yaml
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["patch"]
```

**Risco:** Modificar labels pode:
- Contornar Pod Security Admission
- Contornar Network Policies

---

## Denial of Service Risks

### Object Creation DoS
- Criar objetos grandes/númerosos pode causar OOM no etcd
- Mais crítico em clusters multi-tenant

**Mitigação:**
- Resource Quotas (object count quota)
- LimitRanges

---

## Risk Summary Table

| Permissão | Risco | Mitigação |
|-----------|-------|-----------|
| `secrets list/watch` | Ler todos secrets | Apenas `get` em secrets específicos |
| `pods create` | Acessar secrets, SAs | PSS Baseline/Restricted |
| `persistentvolumes create` | Host filesystem access | Apenas admins criam PVs |
| `nodes/proxy get` | Command execution | Não conceder |
| `roles create + escalate` | Privilege escalation | Não conceder escalate verb |
| `rolebindings create + bind` | Bind any role | Não conceder bind verb |
| `users impersonate` | Assume identity | Restrito a admins |
| `certificatesigningrequests create/update` | Issue certificates | Apenas CAs controlados |
| `serviceaccounts/token create` | Issue SA tokens | Restrito |
| `webhook configurations *` | Read/modify all objects | Apenas admins |
| `namespaces patch` | Bypass PSS/NetworkPolicy | Não conceder |

---

## Conceitos-Chave

1. **Least Privilege**: Apenas permissões necessárias
2. **Privilege Escalation**: Verbos que permitem escalar
3. **Boundaries**: Namespaces são fronteiras de confiança
4. **Periodic Review**: RBAC muda, revisar regularmente
5. **Defense in Depth**: Múltiplas camadas de proteção

---

## Próximos Passos de Estudo

- [ ] RBAC audit logging
- [ ] Impersonation para debugging
- [ ] External auth webhooks
- [ ] Pod Security Standards enforcement
- [ ] Resource Quotas para DoS prevention

---

## Referências

- Kubernetes RBAC Good Practices: https://kubernetes.io/docs/concepts/security/rbac-good-practices/
- RBAC Documentation: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/