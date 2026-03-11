# Kubernetes Security Concepts

**Source:** https://kubernetes.io/docs/concepts/security/
**Type:** Official Documentation
**Category:** Security
**Read:** 2026-03-11

---

## Resumo

### Camadas de Segurança Kubernetes

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD PROVIDER SECURITY                   │
│  (IaaS: AWS, GCP, Azure, etc.)                              │
├─────────────────────────────────────────────────────────────┤
│                    CLUSTER SECURITY                          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐  │
│  │ Control Plane   │ │ Node Security   │ │ Addons        │  │
│  │ Protection      │ │ (kubelet, etc)  │ │ Security      │  │
│  └─────────────────┘ └─────────────────┘ └───────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    WORKLOAD SECURITY                          │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐  │
│  │ Pod Security    │ │ Network Policy  │ │ RuntimeClass  │  │
│  │ Standards       │ │ (Isolation)     │ │ (Custom)      │  │
│  └─────────────────┘ └─────────────────┘ └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Control Plane Protection

| Mecanismo | Descrição |
|-----------|-----------|
| **API Access Control** | RBAC, ABAC, Node authorizer |
| **TLS** | Criptografia in-transit (obrigatório) |
| **Encryption at Rest** | Opcional para dados no etcd |
| **Admission Controllers** | Interceptam e validam/mutam requests |

### Secrets

- **Secret API**: Armazena valores confidenciais
- **Tipos**: Opaque, kubernetes.io/service-account-token, kubernetes.io/dockerconfigjson, etc.
- **Cuidado**: Secrets são encoded, não encrypted por default

### Workload Protection

| Mecanismo | Função |
|-----------|--------|
| **Pod Security Standards** | Privileged, Baseline, Restricted |
| **Pod Security Admission** | Enforça PSS via labels |
| **RuntimeClass** | Custom isolation (gVisor, Kata, etc.) |
| **Network Policies** | Firewall entre Pods e rede externa |

### Admission Control

- **Validating Webhooks**: Apenas validam
- **Mutating Webhooks**: Podem modificar requests
- **Good Practices**: Evitar breaking changes em versões

### Auditing

- **Audit Logging**: Registro cronológico de ações
- **Fontes**: Users, applications, control plane
- **Use Cases**: Forensics, compliance, debugging

---

## Security Mechanisms

### 1. Controlling Access to API

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐
│  User    │───▶│ Authentication│───▶│ Authorization │───▶│ Admission │
│ Request  │    │   (who)       │    │   (can do?)  │    │ (modify)  │
└──────────┘    └──────────────┘    └──────────────┘    └───────────┘
```

### 2. RBAC (Role-Based Access Control)

| Tipo | Escopo |
|------|--------|
| **Role** | Namespace |
| **ClusterRole** | Cluster-wide |
| **RoleBinding** | Liga Role a sujeitos (namespace) |
| **ClusterRoleBinding** | Liga ClusterRole a sujeitos (cluster) |

### 3. Network Policies

```yaml
# Exemplo: Isolamento de Pod
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      role: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: database
    ports:
    - protocol: TCP
      port: 5432
```

---

## Security Checklist Items

### Control Plane
- [ ] TLS configurado para todas as comunicações
- [ ] Encryption at rest habilitado para Secrets
- [ ] Audit logging habilitado
- [ ] RBAC configurado (least privilege)
- [ ] API access restrito

### Nodes
- [ ] kubelet com credenciais limitadas
- [ ] Container runtime seguro (containerd/CRI-O)
- [ ] Network policies implementadas
- [ ] Node isolation configurada

### Workloads
- [ ] Pod Security Standards enforced
- [ ] Secrets montados como volumes (não env vars)
- [ ] Resource limits definidos
- [ ] Network policies aplicadas
- [ ] RuntimeClass para isolamento adicional

---

## Conceitos-Chave

1. **Defense in Depth**: Múltiplas camadas de segurança
2. **Least Privilege**: Conceder apenas o necessário
3. **Network Policies**: Default é ALLOW, explicit DENY
4. **Secrets não são seguros por default**: Precisam de encryption at rest
5. **Audit é crítico**: Para forensics e compliance

---

## Links para Aprofundar
- `/docs/concepts/security/pod-security-standards/`
- `/docs/concepts/security/rbac-good-practices/`
- `/docs/concepts/security/security-checklist/`
- `/docs/concepts/security/secrets-good-practices/`