# OWASP Kubernetes Top 10 (2025)

**Fonte:** https://owasp.org/www-project-kubernetes-top-ten/
**Tipo:** Security Framework
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

O OWASP Kubernetes Top 10 é uma lista priorizada dos riscos mais críticos em ambientes Kubernetes, ajudando profissionais de segurança, administradores e desenvolvedores a priorizar esforços de segurança.

---

## Top 10 Riscos Kubernetes (2025)

### K01: Insecure Workload Configurations
Configurações inseguras de workloads são a principal ameaça. Inclui:
- Containers rodando como root
- Capabilities Linux excessivas
- Mounts sensíveis (hostPath, Docker socket)
- Variáveis de ambiente com secrets

### K02: Overly Permissive Authorization Configurations
RBAC mal configurado:
- Roles com permissões excessivas
- Service accounts com privilégios de cluster-admin
- Bindings mal definidos

### K03: Secrets Management Failures
Falhas no gerenciamento de secrets:
- Secrets em texto claro no etcd
- Secrets versionados em Git
- Falta de rotação de secrets
- Uso de secrets como variáveis de ambiente

### K04: Lack Of Cluster Level Policy Enforcement
Ausência de políticas de segurança cluster-wide:
- Sem Pod Security Standards
- Sem OPA/Gatekeeper
- Sem limites de recursos

### K05: Missing Network Segmentation Controls
Falta de segmentação de rede:
- Network Policies inexistentes
- Pods podendo se comunicar livremente
- Exposição desnecessária de serviços

### K06: Overly Exposed Kubernetes Components
Componentes expostos indevidamente:
- API Server exposto publicamente
- etcd acessível externamente
- Kubelet API sem autenticação
- Dashboard exposto sem auth

### K07: Misconfigured And Vulnerable Cluster Components
Componentes mal configurados ou vulneráveis:
- Versões desatualizadas
- Configurações inseguras padrão
- Binários com vulnerabilidades

### K08: Cluster To Cloud Lateral Movement
Movimento lateral cluster→cloud:
- IAM roles excessivos
- Cloud metadata exposure
- Service account tokens vazados

### K09: Broken Authentication Mechanisms
Mecanismos de autenticação quebrados:
- Certificados estáticos
- Tokens de longa duração
- Ausência de MFA
- Anonymous access habilitado

### K10: Inadequate Logging And Monitoring
Logging e monitoramento inadequados:
- Audit logs desabilitados
- Logs não centralizados
- Falta de alertas de segurança
- Sem detecção de anomalias

---

## Comparação com 2022

A versão 2025 reorganizou prioridades:
- **Supply Chain (K02 em 2022)** → Movido para K07
- **Secrets Management (K08 em 2022)** → Subiu para K03
- **Policy Enforcement** → Mais enfatizado

---

## Conceitos-Chave

1. **Defense in Depth**: Múltiplas camadas de segurança
2. **Least Privilege**: Princípio do menor privilégio
3. **Zero Trust**: Não confiar em nada por padrão
4. **Secure by Default**: Configurações seguras como padrão

---

## Mitigações Recomendadas

### Para Cada Risco:
- **K01**: Pod Security Standards + Security Context
- **K02**: RBAC least privilege + audit
- **K03**: External secrets (Vault) + encryption at rest
- **K04**: OPA/Gatekeeper + PSP/PSS
- **K05**: Network Policies + CNI com policy enforcement
- **K06**: Firewall + auth em todos os componentes
- **K07**: Patch management + scanner de vulnerabilidades
- **K08**: IAM roles restritos + node isolation
- **K09**: OIDC + MFA + short-lived tokens
- **K10**: Audit logging + SIEM + alertas

---

## Próximos Passos de Estudo

- [ ] Deep dive em cada K01-K10
- [ ] Estudar Pod Security Standards
- [ ] Praticar Network Policies
- [ ] Implementar OPA Gatekeeper
- [ ] Configurar audit logging avançado

---

## Referências

- OWASP Kubernetes Top 10: https://owasp.org/www-project-kubernetes-top-ten/
- GitHub: https://github.com/OWASP/www-project-kubernetes-top-ten