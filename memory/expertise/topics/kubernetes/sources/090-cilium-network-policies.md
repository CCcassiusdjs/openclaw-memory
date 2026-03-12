# Cilium Network Policies Overview

**Fonte:** Cilium Docs - https://docs.cilium.io/en/stable/security/policy/index.html
**Data:** 2025-2026
**Tópico:** Cilium Network Policies, L7 Filtering, HTTP/Kafka Policies, Security Identity
**Status:** Lido

---

## Resumo Executivo

Visão geral das políticas de rede do Cilium, incluindo Kubernetes NetworkPolicy, CiliumNetworkPolicy, CiliumClusterwideNetworkPolicy e recursos avançados como L7 filtering.

---

## Métodos de Configuração

### Recursos Kubernetes
- **NetworkPolicy**: Standard Kubernetes policy
- **CiliumNetworkPolicy**: Namespaced Cilium policy
- **CiliumClusterwideNetworkPolicy**: Cluster-wide Cilium policy

### Importação Direta (Deprecado)
- CLI ou API do agent
- Não distribui automaticamente para todos os agents
- Será removido em v1.19

---

## Policy Enforcement Modes

### Endpoint Default Policy
- Política padrão para endpoints
- Aplicada quando nenhuma policy específica existe

### Policy Deny Response Handling
- Como Cilium responde a tráfego negado
- Pode retornar ICMP ou simplesmente drop

---

## Rule Basics

### Endpoint Selector
- Seleciona endpoints (Pods, nodes, etc.)
- Label-based matching
- Similar ao podSelector do Kubernetes

### Node Selector
- Seleciona nodes específicos
- Para políticas de node-level

---

## Layer 3 Examples

### Endpoints Based
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-frontend
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
```

### Services Based
- Policies baseadas em serviços Kubernetes
- Seleciona Pods de um Service

### Entities Based
- Entidades especiais: world, cluster, host, etc.
- `entity: world` = todo tráfego externo
- `entity: cluster` = tráfego dentro do cluster

### Node Based
- Seleciona nodes específicos
- Útil para tráfego node-to-pod

### IP/CIDR Based
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-external
spec:
  endpointSelector:
    matchLabels:
      app: backend
  ingress:
  - fromCIDR:
    - 192.168.1.0/24
```

### DNS Based
- Policies baseadas em FQDN
- Resolve IPs dinamicamente
- Exemplo: permitir acesso a `api.example.com`

---

## Layer 4 Examples

### Limit Ingress/Egress Ports
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-port-80
spec:
  endpointSelector:
    matchLabels:
      app: web
  ingress:
  - toPorts:
    - ports:
      - port: "80"
        protocol: TCP
```

### Limit ICMP/ICMPv6 Types
- Controle de mensagens ICMP
- Exemplo: permitir ping, bloquear outros

### Limit TLS SNI
- Filtragem baseada em Server Name Indication
- Controle de conexões TLS por hostname

---

## Layer 7 Examples

### HTTP Filtering
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-http-path
spec:
  endpointSelector:
    matchLabels:
      app: web
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: frontend
    toPorts:
    - ports:
      - port: "80"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/api/.*"
```

### Kafka (Beta)
- Filtragem de tópicos Kafka
- Controle de producers/consumers

### DNS Policy e IP Discovery
- Políticas de DNS para resolver FQDNs
- IP discovery automático

---

## Deny Policies

### Política de Negação
```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: deny-external
spec:
  endpointSelector:
    matchLabels:
      app: internal
  ingressDeny:
  - fromCIDR:
    - 0.0.0.0/0
```

- Permite negar tráfego explicitamente
- Útil para default deny + exceptions

---

## Host Policies

### Host-level Security
- Aplica ao node, não ao Pod
- Controle de tráfego node-to-node
- Proteção do próprio node

### Exemplo
```yaml
apiVersion: cilium.io/v2
kind: CiliumClusterwideNetworkPolicy
metadata:
  name: host-policy
spec:
  nodeSelector:
    matchLabels: {}
  ingress:
  - fromEntities:
    - cluster
```

---

## Kubernetes Constructs

### Namespaces
- CiliumNetworkPolicy: Namespace-scoped
- CiliumClusterwideNetworkPolicy: Cluster-scoped
- Selector pode especificar namespace

### Known Pitfalls
- Namespace matching com labels requer configuração
- Pod IPs são efêmeros (usar selectors)
- Service IPs podem mudar

---

## Endpoint Lifecycle

### Init Identity
- Identity inicial durante inicialização
- Sem regras até endpoint estar ready

### Lockdown Mode
- Modo restrito durante inicialização
- Nenhum tráfego permitido até policies aplicadas

---

## Troubleshooting

### Policy Rule to Endpoint Mapping
```bash
cilium policy get
cilium endpoint list
cilium policy trace <source> <destination>
```

### Troubleshooting toFQDNs Rules
- Verificar DNS resolution
- Validar IPs resolvidos
- Checar TTL

---

## Differences from Kubernetes NetworkPolicies

| Feature | K8s NetworkPolicy | Cilium |
|---------|-------------------|--------|
| **Layer** | L3/L4 | L3/L4/L7 |
| **HTTP filtering** | Não | Sim |
| **DNS-based** | Não | Sim |
| **Deny rules** | Não | Sim |
| **Cluster-wide** | Não | Sim |
| **Entity-based** | Não | Sim |

---

## Insights para Kubernetes

1. **L7 filtering é poderoso**: HTTP, Kafka, DNS filtering
2. **CiliumClusterwideNetworkPolicy**: Cluster-scoped policies
3. **FQDN policies**: Resolve DNS dinamicamente
4. **Deny rules explícitas**: Mais controle que K8s padrão
5. **Host policies**: Proteção node-level

---

## Palavras-Chave
`cilium` `network-policies` `l7-filtering` `security` `http-filtering` `dns-policy` `kubernetes`