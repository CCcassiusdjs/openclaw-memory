# Kubernetes Service Accounts (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/security/service-accounts/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

ServiceAccounts fornecem identidade não-humana para Pods, system components, e entidades externas interagindo com o cluster Kubernetes.

---

## O que são Service Accounts?

### Definição
- Contas não-humanas para identidade no cluster
- Aplicações, system components, e entidades externas
- Usados para autenticação com API server
- Implementação de políticas de segurança baseadas em identidade

### Propriedades
- **Namespaced**: Cada SA vinculado a um namespace
- **Lightweight**: Criados rapidamente
- **Portable**: Fáceis de incluir em configurações

### Diferença de User Accounts
| Característica | ServiceAccount | User |
|---------------|----------------|------|
| Localização | Kubernetes API | Externo |
| Access Control | Kubernetes RBAC | IAM externo |
| Uso pretendido | Workloads, automação | Pessoas |

---

## Default Service Accounts

- Todo namespace tem um SA `default`
- Criado automaticamente pelo control plane
- Sem permissões por padrão (exceto API discovery)
- Se deletado, é recriado automaticamente
- Pods sem SA especificado usam o SA `default` do namespace

---

## Casos de Uso

### Comunicação com API Server
- Ler Secrets
- Cross-namespace access (Jobs, Leases)
- Listar recursos em outros namespaces

### Serviços Externos
- Autenticação com APIs cloud
- CI/CD pipelines
- Private image registries (imagePullSecret)

### Software de Terceiros
- Security tools
- Service mesh grouping
- Observabilidade

---

## Como Usar

### 1. Criar ServiceAccount
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-serviceaccount
  namespace: my-namespace
```

### 2. Conceder Permissões (RBAC)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: my-namespace
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: my-namespace
subjects:
- kind: ServiceAccount
  name: my-serviceaccount
roleRef:
  kind: Role
  name: pod-reader
```

### 3. Atribuir ao Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  serviceAccountName: my-serviceaccount
  containers:
  - name: app
    image: myapp:latest
```

---

## Cross-Namespace Access

Para permitir SA de um namespace acessar recursos de outro:

1. Criar Role no namespace target
2. Criar RoleBinding no namespace target
3. Vincular Role ao SA do namespace source

```yaml
# Role no namespace maintenance
kind: Role
metadata:
  name: job-reader
  namespace: maintenance
rules:
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding no namespace maintenance
kind: RoleBinding
metadata:
  name: read-jobs
  namespace: maintenance
subjects:
- kind: ServiceAccount
  name: my-sa
  namespace: dev
roleRef:
  kind: Role
  name: job-reader
```

---

## Tokens de Service Account

### TokenRequest API (Recomendado)
- Tokens de curta duração
- Automaticamente rotacionados
- Bound ao lifecycle do Pod
- Projected volume

```yaml
volumes:
- name: token
  projected:
  sources:
  - serviceAccountToken:
      path: token
      audience: api
      expirationSeconds: 3600
```

### Token Volume Projection
- Configurado no Pod spec
- Kubelet adiciona token automaticamente
- Rotação antes da expiração

### Legacy Token Secrets (NÃO recomendado)
- Tokens estáticos em Secrets
- Não expiram
- Não rotacionam
- Risco de segurança

---

## Autenticação de Tokens

### Validação pelo API Server
1. Verifica assinatura do token
2. Verifica se expirou
3. Verifica se object references são válidos
4. Verifica audience claims

### Bound Tokens (TokenRequest)
- Vinculados ao lifecycle do objeto (Pod, Secret)
- Invalidados quando objeto é deletado
- TokenReview detecta invalidação imediatamente

### OIDC Validation (Alternativa)
- Tokens válidos até expiração
- Não detecta invalidação de objetos
- Menos seguro que TokenReview

---

## Desabilitando Auto-Mount

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  automountServiceAccountToken: false
  containers:
  - name: app
    image: myapp
```

**Benefícios:**
- Reduz risco de exposição
- Principio do menor privilégio
- Segurança defense in depth

---

## Alternatives to Service Accounts

### SPIFFE/SPIRE
- X.509 certificates para Pods
- Identity federation
- No secrets management

### Service Mesh (Istio)
- mTLS automático
- Certificate rotation
- Workload identity

### OIDC Tokens
- External identity provider
- Short-lived tokens
- Cloud IAM integration

---

## Conceitos-Chave

1. **ServiceAccount**: Identidade não-humana no cluster
2. **Default SA**: Criado automaticamente em cada namespace
3. **TokenRequest API**: Tokens de curta duração (recomendado)
4. **Bound Tokens**: Vinculados ao lifecycle de objetos
5. **Cross-namespace**: RBAC permite acesso entre namespaces

---

## Best Practices

1. **One SA per workload**: Isolamento de identidade
2. **Least privilege**: RBAC mínimo necessário
3. **Short-lived tokens**: Usar TokenRequest API
4. **Disable auto-mount**: Quando não necessário
5. **Audit**: Revisar SAs e bindings regularmente

---

## Próximos Passos de Estudo

- [ ] TokenRequest API em detalhes
- [ ] SPIFFE CSI driver
- [ ] Workload Identity (cloud)
- [ ] Service mesh identity

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/security/service-accounts/
- RBAC: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- TokenRequest: https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/token-request-v1/