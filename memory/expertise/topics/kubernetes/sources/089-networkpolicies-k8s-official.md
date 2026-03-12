# NetworkPolicies - Kubernetes Official Documentation

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/services-networking/network-policies/
**Data:** Janeiro 2026
**Tópico:** NetworkPolicies, Security, Isolation, Traffic Control
**Status:** Lido

---

## Resumo Executivo

Documentação oficial de NetworkPolicies, cobrindo conceitos de isolamento, regras de ingress/egress, seletores, políticas default e comportamento.

---

## O que são NetworkPolicies

### Definição
- Especificam regras para controle de tráfico
- OSI Layer 3-4 (IP/porta)
- Aplicação-centric: definem como Pods podem comunicar

### Pré-requisitos
- Network plugin que suporte NetworkPolicy
- CNI: Calico, Cilium, Weave Net, etc.
- NetworkPolicy sem controller = sem efeito

---

## Isolamento de Pods

### Conceitos
- **Non-isolated**: Nenhuma NetworkPolicy aplica ao Pod
- **Isolated**: Pelo menos uma NetworkPolicy aplica ao Pod

### Isolamento de Egress
- Default: Pod não-isolado para egress (toda saída permitida)
- Isolated: Apenas conexões permitidas pelas policies

### Isolamento de Ingress
- Default: Pod não-isolado para ingress (toda entrada permitida)
- Isolated: Apenas conexões permitidas pelas policies

### Comportamento Aditivo
- NetworkPolicies não conflitam
- União de todas policies aplicáveis
- Ordem não importa

---

## NetworkPolicy Resource

### Exemplo Completo
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

### Campos Obrigatórios
- apiVersion
- kind
- metadata
- spec

### spec.podSelector
- Seleciona Pods aos quais a policy aplica
- Label selector
- Empty selector = todos os Pods do namespace

### spec.policyTypes
- Lista: Ingress, Egress, ou ambos
- Indica quais direções a policy afeta

### spec.ingress
- Lista de regras de entrada permitidas
- Cada regra: `from` + `ports`

### spec.egress
- Lista de regras de saída permitidas
- Cada regra: `to` + `ports`

---

## Selectors

### Tipos de Seletores

| Seletor | Descrição |
|---------|-----------|
| **podSelector** | Pods no mesmo namespace |
| **namespaceSelector** | Todos os Pods em namespaces selecionados |
| **podSelector + namespaceSelector** | Pods específicos em namespaces específicos |
| **ipBlock** | CIDR ranges (IPs externos ao cluster) |

### Atenção: Sintaxe Correta
```yaml
# AND: Pods com role=client E namespaces com user=alice
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        user: alice
    podSelector:
      matchLabels:
        role: client

# OR: Pods com role=client OU namespaces com user=alice
ingress:
- from:
  - namespaceSelector:
      matchLabels:
        user: alice
  - podSelector:
      matchLabels:
        role: client
```

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

### Default Allow All Ingress
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

### Default Allow All Egress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
spec:
  podSelector: {}
  egress:
  - {}
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

---

## Filtragem de Tráfego

### Layer 4
- TCP, UDP, SCTP
- Comportamento garantido
- Outros protocolos: comportamento indefinido

### Port Range (v1.25+)
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: multi-port-egress
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 32000
      endPort: 32768
```

---

## Comportamento de Conexões

### Bidirecional
- Conexão precisa ser permitida por AMBOS os lados
- Egress do source + Ingress do destination
- Se qualquer lado não permitir = conexão negada

### Reply Traffic
- Tráfego de resposta é implicitamente permitido
- Não precisa de regra explícita para return traffic

### Node Traffic
- Traffic to/from node é sempre permitido
- Independentemente de IP do Pod ou node

---

## Insights para Kubernetes

1. **CNI obrigatório**: NetworkPolicy sem plugin = sem efeito
2. **Policies são aditivas**: União de todas aplicáveis
3. **Default deny é boa prática**: Isolar antes de permitir
4. **Reply traffic implícito**: Não precisa de regra para retorno
5. **Layer 4 apenas**: TCP/UDP/SCTP garantidos

---

## Palavras-Chave
`networkpolicies` `security` `isolation` `traffic-control` `ingress` `egress` `kubernetes`