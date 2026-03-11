# OWASP Kubernetes Security Cheat Sheet

**Source:** https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html
**Type:** OWASP Guide
**Category:** Security
**Read:** 2026-03-11

---

## Resumo

### Estrutura do Cheat Sheet

```
┌─────────────────────────────────────────────────────────────┐
│              KUBERNETES SECURITY LAYERS                      │
│                                                             │
│  1. HOST SECURITY                                           │
│     - OS hardening                                          │
│     - Patch management                                      │
│     - Firewall rules                                        │
│                                                             │
│  2. COMPONENT SECURITY                                      │
│     - Dashboard                                             │
│     - etcd                                                  │
│     - API access                                            │
│     - RBAC                                                  │
│                                                             │
│  3. BUILD PHASE                                             │
│     - Image security                                        │
│     - Base images                                           │
│                                                             │
│  4. DEPLOY PHASE                                            │
│     - Admission controllers                                 │
│     - Pod security                                          │
│                                                             │
│  5. RUNTIME PHASE                                           │
│     - Network policies                                      │
│     - Service mesh                                          │
│     - Monitoring                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Section 1: Host Security

### Deployment Options
| Option | Considerations |
|--------|----------------|
| Bare metal | Full control, more responsibility |
| On-premise VMs | Balance of control/convenience |
| Managed Cloud | Less control, shared responsibility |

### Hardening Checklist
- [ ] Latest OS version
- [ ] OS hardening (CIS benchmarks)
- [ ] Patch management system
- [ ] Configuration management
- [ ] Firewall rules
- [ ] Datacenter security measures

### Updating Kubernetes
- **Always run latest stable version**
- Kubernetes mantém 3 release branches
- Patch releases regulares + urgent releases
- Use rolling updates for minimal disruption

---

## Section 2: Component Security

### Kubernetes Dashboard Security

**Risco Real:** Tesla hack via poorly configured dashboard

**Mitigations:**
1. **NÃO** expor dashboard publicamente
2. Habilitar RBAC
3. Service account com privilégios mínimos
4. Per-user permissions
5. Network policies para bloquear requests internos
6. Verificar RoleBindings para cluster-admin
7. Deploy com reverse proxy + MFA

### etcd Security (CRÍTICO)

**Por que é crítico:**
- Armazena TODOS os dados do cluster
- Write access = root no cluster
- Read access = easy privilege escalation

**Recomendações:**
1. **Isolar atrás de firewall** (apenas API server acessa)
2. **Mutual TLS** para autenticação
3. **CA separado** para etcd
4. **Backup regular**
5. Instância separada para componentes adicionais

### Network Ports

#### Control Plane
| Port | Component |
|------|-----------|
| 6443 | API Server |
| 2379-2380 | etcd |
| 10250 | Kubelet API |
| 10259 | kube-scheduler |
| 10257 | kube-controller-manager |
| 10255 | Read-Only Kubelet |

#### Worker Nodes
| Port | Component |
|------|-----------|
| 10248 | Kubelet Healthz |
| 10249 | Kube-proxy Metrics |
| 10250 | Kubelet API |
| 10255 | Read-Only Kubelet |
| 10256 | Kube-proxy Healthz |
| 30000-32767 | NodePort Services |

### API Authentication

#### External (RECOMMENDED)
| Method | Use Case |
|--------|----------|
| **OIDC** | Enterprise SSO, short-lived tokens |
| **Cloud IAM** | GKE, EKS, AKS managed |
| **Impersonation** | Auth proxy without API config access |

#### Internal (NOT RECOMMENDED)
| Method | Why Not Recommended |
|--------|---------------------|
| Static Token File | Tokens never expire, plain text |
| Bootstrap Tokens | Limited scope, bootstrap only |
| Client Certificates | No revocation, management overhead |
| Service Account Tokens | Long-lived by default |

### RBAC Best Practices

1. **Least Privilege**: Start with nothing, add as needed
2. **Namespaced Roles**: Prefer Role over ClusterRole
3. **Groups over Users**: Easier management
4. **Avoid Wildcards**: Be explicit
5. **Regular Audit**: Review bindings periodically

---

## Section 3: Build Phase

### Image Security

| Practice | Description |
|----------|-------------|
| Minimal base images | Alpine, distroless |
| No unnecessary packages | Reduce attack surface |
| Run as unprivileged | Non-root user |
| Pin by SHA256 | Reproducible builds |
| Sign images | Verify provenance |
| Scan regularly | Vulnerability management |

### Image Best Practices

```dockerfile
# BAD
FROM ubuntu:latest
USER root

# GOOD
FROM alpine:3.19@sha256:abc123...
USER nonroot
RUN addgroup -S app && adduser -S app -G app
```

---

## Section 4: Deploy Phase

### Admission Controllers

| Controller | Purpose |
|-------------|---------|
| **PodSecurity** | Enforce Pod Security Standards |
| **LimitRanger** | Resource limits |
| **ResourceQuota** | Namespace quotas |
| **ImagePolicyWebhook** | External image validation |
| **ValidatingAdmissionWebhook** | Custom validation |

### Pod Security

1. **Pod Security Standards**: Enforce restricted policy
2. **Security Context**: Drop capabilities, run as non-root
3. **Resource Limits**: Prevent DoS
4. **Readiness/Liveness Probes**: Health checks

---

## Section 5: Runtime Phase

### Network Policies

```yaml
# Default deny all
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Service Mesh Benefits
- mTLS automático
- Observabilidade
- Traffic management
- Security policies

### Monitoring
- Audit logs
- Prometheus metrics
- Falco for runtime security
- Network flow logs

---

## Conceitos-Chave

1. **Defense in Depth**: Múltiplas camadas
2. **Zero Trust**: Verify everything
3. **Least Privilege**: Minimal permissions
4. **External Auth**: OIDC/IAM over internal
5. **etcd Critical**: Most sensitive component
6. **Dashboard Risk**: Known attack vector
7. **Image Security**: First line of defense

---

## Critical Points

1. **etcd = Root**: Acesso ao etcd = root no cluster
2. **Dashboard**: Tesla hack via exposed dashboard
3. **API Ports**: 6443, 10250, 2379-2380 são críticos
4. **Internal Auth**: Use OIDC/Cloud IAM, avoid static tokens
5. **Images**: Pin by SHA256, scan regularly, run as non-root