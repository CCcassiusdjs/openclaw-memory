# Kubernetes Network Policies - Official Documentation

**Source:** kubernetes.io/docs/concepts/services-networking/network-policies/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

NetworkPolicies controlam o fluxo de tráfego no nível IP/porta (OSI layer 3/4). Permitem especificar regras de comunicação entre Pods e com o mundo externo. Requerem CNI plugin que suporte NetworkPolicy.

## How Network Policies Work

### Prerequisites
- Network plugin must support NetworkPolicy
- Creating policy without supporting plugin has no effect

### Two Types of Isolation

#### Egress Isolation
- Default: pod is non-isolated (all outbound allowed)
- Isolated if NetworkPolicy selects pod with Egress in policyTypes
- Only allowed connections are those in egress rules

#### Ingress Isolation
- Default: pod is non-isolated (all inbound allowed)
- Isolated if NetworkPolicy selects pod with Ingress in policyTypes
- Only allowed connections are those in ingress rules + node traffic

### Additive Nature
- Policies don't conflict
- Multiple policies combine additively
- Union of all applicable policies = allowed connections

### Bidirectional Requirement
- Source pod egress policy must allow connection
- Destination pod ingress policy must allow connection
- If either denies, connection fails

## NetworkPolicy Resource

### Example
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

### Key Fields
- `podSelector`: selects pods the policy applies to
- `policyTypes`: Ingress, Egress, or both
- `ingress`: allowed inbound rules
- `egress`: allowed outbound rules

## Selectors

### Four Types

#### podSelector
- Selects Pods in same namespace
- Allows traffic from/to selected Pods

#### namespaceSelector
- Selects entire namespaces
- All Pods in selected namespaces

#### namespaceSelector AND podSelector
- Selects Pods in particular namespaces
- Both must match (AND logic)

```yaml
from:
- namespaceSelector:
    matchLabels:
      user: alice
  podSelector:
    matchLabels:
      role: client
```

#### ipBlock
- Selects IP CIDR ranges
- Should be cluster-external IPs
- Pod IPs are ephemeral and unpredictable

### OR vs AND Logic
```yaml
# AND (single entry)
from:
- namespaceSelector:
    matchLabels:
      user: alice
  podSelector:
    matchLabels:
      role: client
# Matches: pods with role=client in namespaces with user=alice

# OR (multiple entries)
from:
- namespaceSelector:
    matchLabels:
      user: alice
- podSelector:
    matchLabels:
      role: client
# Matches: pods in namespaces with user=alice OR pods with role=client in same namespace
```

## Default Policies

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

## Port Ranges (v1.25+)

```yaml
ports:
- protocol: TCP
  port: 32000
  endPort: 32768
```

## Network Traffic Filtering

### Layer 4 Only
- TCP, UDP, SCTP (if supported)
- Other protocols (ICMP, ARP) behavior varies by plugin

### Limitations
- Deny all only guarantees TCP/UDP/SCTP
- ICMP may or may not be blocked
- Behavior depends on CNI plugin

## Key Takeaways

1. NetworkPolicy controls layer 3/4 traffic
2. Default: all traffic allowed
3. Isolation is additive (union of all policies)
4. Both directions must allow connection
5. Four selector types: pod, namespace, both, ipBlock
6. Default deny is a common pattern
7. Requires CNI plugin support

## Personal Notes

NetworkPolicies são essenciais para segurança em ambientes multi-tenant. O padrão "default deny" é best practice.

Para CKA/CKAD:
- podSelector: same namespace
- namespaceSelector: entire namespaces
- ipBlock: external IPs only
- Default deny: empty rules in policyTypes

A feature de port ranges é útil para aplicações que usam range de portas. A distinção entre AND (single entry) e OR (multiple entries) é crítica para políticas corretas.