# Kubernetes Security Checklist

**Source:** https://kubernetes.io/docs/concepts/security/security-checklist/
**Type:** Official Documentation
**Category:** Security
**Read:** 2026-03-11

---

## Resumo

### Checklist de Segurança Kubernetes

#### Autenticação e Autorização
| Item | Status |
|------|--------|
| system:masters não usado após bootstrapping | ⬜ |
| kube-controller-manager com --use-service-account-credentials | ⬜ |
| Certificado raiz protegido | ⬜ |
| Certificados com expiração ≤ 3 anos | ⬜ |
| Revisão periódica de acesso (≤ 24 meses) | ⬜ |

#### Network Security
| Item | Status |
|------|--------|
| CNI plugins suportam Network Policies | ⬜ |
| Ingress/egress policies em todos os workloads | ⬜ |
| Default deny-all network policies | ⬜ |
| Service mesh para encrypt in-transit (opcional) | ⬜ |
| API/kubelet/etcd NÃO expostos publicamente | ⬜ |
| Cloud metadata API filtrado | ⬜ |
| LoadBalancer/ExternalIPs restritos | ⬜ |

#### Pod Security
| Item | Status |
|------|--------|
| RBAC para workloads apenas se necessário | ⬜ |
| Pod Security Standards aplicado | ⬜ |
| Memory limit configurado | ⬜ |
| CPU limit em workloads sensíveis | ⬜ |
| Seccomp habilitado | ⬜ |
| AppArmor/SELinux habilitado | ⬜ |

#### Logs and Auditing
| Item | Status |
|------|--------|
| Audit logs protegidos | ⬜ |

#### Pod Placement
| Item | Status |
|------|--------|
| Pods em nodes conforme sensibilidade | ⬜ |
| Apps sensíveis em nodes isolados | ⬜ |
| RuntimeClass para sandbox (opcional) | ⬜ |

#### Secrets
| Item | Status |
|------|--------|
| ConfigMaps NÃO usados para dados confidenciais | ⬜ |
| Encryption at rest configurado | ⬜ |
| Third-party secrets injection (opcional) | ⬜ |
| Service account tokens não montados desnecessariamente | ⬜ |
| Bound service account tokens em uso | ⬜ |

#### Images
| Item | Status |
|------|--------|
| Minimizar conteúdo desnecessário | ⬜ |
| Containers rodam como unprivileged | ⬜ |
| Images referenciadas por SHA256 | ⬜ |
| Image scanning regular | ⬜ |

---

## Detalhes Importantes

### RBAC Limitations
RBAC não é granular o suficiente para autorização em nível de Pod:
- `create on Pods` não limita o que pode ser especificado no PodSpec
- Admission controllers necessários para controle fino

### Pod Security Standards
| Policy | Descrição |
|--------|-----------|
| **Privileged** | Sem restrições |
| **Baseline** | Minimamente restritivo |
| **Restricted** | Altamente restritivo |

### Pod Security Admission
Modos de operação:
- **warn**: Avisa violações
- **audit**: Registra violações
- **enforce**: Bloqueia violações

### Network Policies
Recomendado: Default deny-all em cada namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}  # Todos os pods
  policyTypes:
  - Ingress
  - Egress
```

### Seccomp
- Secure computing mode (desde kernel 2.6.12)
- Restringe syscalls disponíveis
- RuntimeDefault profile disponível desde K8s 1.27
- Security Profiles Operator para gerenciamento

### AppArmor vs SELinux
| Feature | AppArmor | SELinux |
|---------|----------|---------|
| Facilidade | Mais simples | Mais complexo |
| Profiles | Por container | Labels |
| Modo | Enforcing/Complain | Enforcing |

### Secrets Best Practices
1. **Nunca** usar ConfigMaps para dados confidenciais
2. Encryption at rest obrigatório
3. Montar como volumes (não env vars)
4. Usar emptyDir.medium para tmpfs
5. Secrets Store CSI Driver para third-party

---

## Conceitos-Chave

1. **Defense in Depth**: Múltiplas camadas de segurança
2. **Least Privilege**: Apenas o necessário
3. **Default Deny**: Network policies deny-all por default
4. **Pod Security Standards**: Três níveis de restrição
5. **Audit Everything**: Logs protegidos e acessíveis