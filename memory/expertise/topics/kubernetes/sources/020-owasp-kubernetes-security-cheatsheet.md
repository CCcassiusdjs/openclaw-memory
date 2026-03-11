# OWASP Kubernetes Security Cheat Sheet

**Fonte:** https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html
**Tipo:** Security Best Practices
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Guia abrangente de segurança Kubernetes dividido em 4 fases: Host, Components, Build, Deploy e Runtime.

---

## SECTION 1: Securing Kubernetes Hosts

### Host Hardening
- Instalar última versão do OS
- Harden operating system
- Patch management
- Configuration management
- Firewall rules
- Datacenter security measures

### Atualizações Kubernetes
- **Sempre usar última versão estável**
- Kubernetes mantém 3 minor releases ativas
- Backports de security fixes
- Version skew policy aplicável
- Rolling updates para upgrades

### Release Schedule
- 3 releases mantidos
- Patch releases regulares
- Urgent releases quando necessário
- Atualização com minimal disruption

---

## SECTION 2: Securing Kubernetes Components

### Ports Críticos

**Control Plane:**
| Protocol | Port | Purpose |
|----------|------|---------|
| TCP | 6443 | API Server |
| TCP | 2379-2380 | etcd client API |
| TCP | 10250 | Kubelet API |
| TCP | 10259 | kube-scheduler |
| TCP | 10257 | kube-controller-manager |
| TCP | 10255 | Read-Only Kubelet API |

**Worker Nodes:**
| Protocol | Port | Purpose |
|----------|------|---------|
| TCP | 10248 | Kubelet Healthz |
| TCP | 10249 | Kube-proxy Metrics |
| TCP | 10250 | Kubelet API |
| TCP | 10255 | Read-Only Kubelet |
| TCP | 10256 | Kube-proxy Healthz |
| TCP | 30000-32767 | NodePort Services |

### Kubernetes Dashboard Security
⚠️ **CUIDADO:** Dashboard é comum vetor de ataque (Tesla hack)

**Recomendações:**
- Não expor sem auth adicional
- Habilitar RBAC
- Não dar privilégios altos ao service account
- Per-user permissions
- Network policies para bloquear acesso interno
- Versões < 1.8 tinham service account com cluster-admin
- Usar reverse proxy com OIDC/MFA

### etcd Security (CRÍTICO)
⚠️ **Acesso ao etcd = Root no cluster**

**Proteções:**
- TLS mutual auth (client certificates)
- Firewall isolando etcd
- Apenas API servers acessam etcd
- ACLs para subset do keyspace
- Backup regular

### API Authentication

**RECOMENDADO:**
- OpenID Connect (OIDC)
- Managed cloud IAM (GKE, EKS, AKS)
- Kubernetes Impersonation
- MFA para user access

**NÃO RECOMENDADO:**
- Static Token File (clear text tokens)
- X509 Client Certs (no revocation)
- Service Account Tokens (não para users)

### RBAC Implementation

```bash
# Habilitar RBAC
kube-apiserver --authorization-mode=Node,RBAC
```

**Conceitos:**
- Roles: conjunto de permissions
- RoleBindings: liga roles a users/groups
- ClusterRoles: cluster-wide
- Roles: namespace-scoped

**Best Practice:**
- Node + RBAC authorizers juntos
- NodeRestriction admission plugin
- Least privilege principle

### Kubelet Security
- Habilitar autenticação/autorização
- Por padrão: unauthenticated access (!!)
- Production: sempre autenticar

---

## SECTION 3: Build Phase Security

### Container Image Security

**Principles:**
- Approved/secure base image
- Scan regularmente
- Trusted registries only
- Governance policies

### Image Best Practices
- Imagens atualizadas
- Only authorized images
- CI pipeline com vulnerability scanning
- Private registry para approved images

### CI Pipeline Security
1. Build image
2. Security scan (Trivy, Grype)
3. Se OK → push to private registry
4. Se falha → block deployment

### Distroless Images
**Benefícios:**
- Menor attack surface
- Sem shell/package managers
- Menos CVEs
- Menor tamanho

**Opções:**
- GoogleContainerTools/distroless
- scratch (Go, Rust)

---

## SECTION 4: Deploy Phase Security

### Namespaces for Isolation
```bash
# Set namespace
kubectl run nginx --image=nginx --namespace=myapp
kubectl get pods --namespace=myapp

# Permanent context
kubectl config set-context --current --namespace=myapp
```

### Image Policy Webhook
**Rejeitar imagens:**
- Not scanned recently
- Base image não aprovada
- From insecure registries

### Security Context
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    readOnlyRootFilesystem: true
    capabilities:
      drop: ["ALL"]
  containers:
  - name: app
    image: app:latest
    securityContext:
      allowPrivilegeEscalation: false
```

### Pod Security Standards
**3 Profiles:**
1. **Privileged**: Unrestricted (system/infra)
2. **Baseline**: Minimal restrictions, prevent escalations
3. **Restricted**: Highly restricted (defense in depth)

**Implementação:**
- Pod Security Admission Controller
- Labels: `pod-security.kubernetes.io/<MODE>: <version>`
- Namespace level enforcement

### Container Privileges Assessment
**Principle:** Least privilege
- Only necessary capabilities
- No privileged containers (unless required)
- read-only root filesystem
- runAsNonRoot

---

## SECTION 5: Runtime Phase Security

### Continuous Monitoring
- Vulnerability scanning em produção
- First-party + third-party containers
- Open source: ThreatMapper
- SIEM integration

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Audit Logging
- API Server audit log
- Request/Response capture
- Policy violation detection
- Retention policies

### Runtime Security Tools
- Falco (runtime detection)
- Sysdig Secure
- Aqua Security
- NeuVector

---

## Checklist de Segurança

### Host Level
- [ ] OS hardened
- [ ] Firewall configurado
- [ ] Kubernetes atualizado
- [ ] Nodes isolados por função

### Control Plane
- [ ] etcd com TLS + auth
- [ ] API Server com auth/authorização
- [ ] RBAC enabled
- [ ] Dashboard secured
- [ ] Ports restritos

### Build
- [ ] Base images aprovadas
- [ ] CI scanning
- [ ] Private registry
- [ ] Distroless images

### Deploy
- [ ] Security context
- [ ] Pod Security Standards
- [ ] Network Policies
- [ ] Namespaces isolation

### Runtime
- [ ] Continuous scanning
- [ ] Audit logging
- [ ] SIEM integration
- [ ] Incident response plan

---

## Próximos Passos de Estudo

- [ ] Implementar Pod Security Standards
- [ ] Configurar Network Policies
- [ ] Setup audit logging
- [ ] Integrar Falco
- [ ] Threat modeling exercises

---

## Referências

- OWASP Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html
- Kubernetes Security: https://kubernetes.io/docs/concepts/security/
- Trivy: https://github.com/aquasecurity/trivy
- ThreatMapper: https://github.com/deepfence/ThreatMapper