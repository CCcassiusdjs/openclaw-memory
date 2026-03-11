# Kubernetes NetworkPolicies (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/services-networking/network-policies/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

NetworkPolicies controlam fluxo de tráfego no nível IP/porta (OSI layer 3-4), especificando regras para comunicação entre Pods e o mundo externo.

---

## Pré-requisitos

⚠️ **O cluster DEVE usar um CNI plugin que suporte NetworkPolicy.**
- Calico ✓
- Cilium ✓
- Weave ✓
- Flannel (limitado)
- Criar NetworkPolicy sem suporte = sem efeito

---

## Tipos de Isolamento

### Isolamento de Egress
- Por padrão: Pod é **não-isolado** para egress (toda saída permitida)
- Isolado quando: NetworkPolicy seleciona o Pod e tem `Egress` em policyTypes

### Isolamento de Ingress
- Por padrão: Pod é **não-isolado** para ingress (toda entrada permitida)
- Isolado quando: NetworkPolicy seleciona o Pod e tem `Ingress` em policyTypes

### Comportamento Aditivo
- NetworkPolicies são **aditivas** (não conflitam)
- Conexões permitidas = união de todas as políticas aplicáveis

---

## NetworkPolicy Resource

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

### Campos

| Campo | Descrição |
|-------|-----------|
| **podSelector** | Seleciona Pods (vazio = todos no namespace) |
| **policyTypes** | Ingress, Egress, ou ambos |
| **ingress** | Regras de entrada |
| **egress** | Regras de saída |

---

## Selectors

### podSelector
```yaml
from:
- podSelector:
    matchLabels:
      role: frontend
```
- Seleciona Pods no **mesmo namespace**
- Regras aplicam ao namespace da NetworkPolicy

### namespaceSelector
```yaml
from:
- namespaceSelector:
    matchLabels:
      project: myproject
```
- Seleciona todos os Pods em namespaces com o label

### namespaceSelector + podSelector
```yaml
from:
- namespaceSelector:
    matchLabels:
      user: alice
  podSelector:
    matchLabels:
      role: client
```
- Seleciona Pods específicos em namespaces específicos
- **Ambos devem match** (AND lógico)

### ipBlock
```yaml
from:
- ipBlock:
    cidr: 172.17.0.0/16
    except:
    - 172.17.1.0/24
```
- IPs externos (não Pods)
- `except` para excluir ranges

---

## Políticas Default

### Default Deny All Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

### Default Deny All Egress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {}
  policyTypes:
  - Egress
```

### Default Deny All
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow All Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  ingress:
  - {}
  policyTypes:
  - Ingress
```

---

## Port Ranges

### Múltiplas Portas
```yaml
ports:
- protocol: TCP
  port: 32000
  endPort: 32768
```

**Restrições:**
- `endPort` ≥ `port`
- `endPort` requer `port`
- Ambos devem ser numéricos

---

## Exemplos Práticos

### Permitir tráfego de frontend para backend
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

### Permitir DNS egress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

### Permitir tráfego de namespaces específicos
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-namespaces
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchExpressions:
        - key: namespace
          operator: In
          values: ["frontend", "backend"]
```

---

## Limitações

NetworkPolicy **NÃO suporta**:
- Forçar tráfego através de gateway (use Service Mesh)
- TLS/SSL (use Service Mesh ou Ingress)
- Políticas específicas de node (use CIDR)
- Targeting services por nome (use Pod labels)
- Deny rules explícitas (modelo é allow-only)
- Logging de eventos de segurança
- Prevenir loopback ou tráfego do host

---

## hostNetwork Pods

Comportamento indefinido para Pods com `hostNetwork: true`:
1. Plugin pode distinguir tráfego e aplicar políticas
2. Plugin pode ignorar e tratar como tráfego do node

**Alternativa:** Usar `ipBlock` para permitir tráfego de nodes.

---

## Protocolos Suportados

- **TCP**: Suportado
- **UDP**: Suportado
- **SCTP**: Suportado (requer CNI compatível)

**Outros protocolos (ICMP, ARP):** Comportamento indefinido.

---

## Conceitos-Chave

1. **Ingress**: Tráfego entrando no Pod
2. **Egress**: Tráfego saindo do Pod
3. **podSelector**: Seleciona Pods no mesmo namespace
4. **namespaceSelector**: Seleciona Pods em outros namespaces
5. **ipBlock**: Seleciona IPs externos

---

## Best Practices

1. **Default Deny**: Começar com deny all, depois permitir
2. **Namespace Isolation**: Usar namespaceSelector
3. **DNS Egress**: Sempre permitir DNS
4. **Port Specificity**: Especificar portas quando possível
5. **Testing**: Testar políticas antes de produção

---

## Próximos Passos de Estudo

- [ ] Calico Network Policies (extended)
- [ ] Cilium Network Policies (L7)
- [ ] Policy visualization tools
- [ ] Multi-tenant network isolation

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Network Policy Recipes: https://github.com/ahmetb/kubernetes-network-policy-recipes
- Declare Network Policy: https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/