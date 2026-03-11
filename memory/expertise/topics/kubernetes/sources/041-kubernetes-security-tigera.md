# Kubernetes Security: 8 Best Practices to Secure Your Cluster (Tigera)

**Source:** tigera.io/learn/guides/kubernetes-security/
**Type:** Security Guide
**Priority:** High
**Date:** 2026

---

## Summary

Guia abrangente de segurança Kubernetes cobrindo 8 melhores práticas organizadas em três fases: build, deploy e runtime. Inclui estatísticas de mercado e fundamentos de segurança.

## Kubernetes Security Landscape

### Market Statistics (CNCF Survey)
- 93% of organizations using or planning containers in production
- 96% using or evaluating Kubernetes
- 28% have more than 11 production clusters

### Security Incidents (Red Hat Survey)
- 55% delayed releases due to security issues
- 94% experienced at least one security incident in past year
- 59% say security is biggest concern

## 8 Kubernetes Security Best Practices

### Build-Time Security

#### 1. Image Scanning
- Verify container images are free of vulnerabilities
- Scan base images and all packages against CVE database
- Check for vulnerabilities at all CI/CD stages
- Control access to image registries

#### 2. Host Operating System Hardening
- Use minimal required privileges on host
- Use hardened host OS
- Restrict system calls and filesystem access
- Strong isolation between processes
- Prevent privilege escalation attacks

#### 3. Minimizing Attack Surface
- Use minimal base images
- Consider `FROM scratch` for minimal containers
- Use distroless or Alpine images
- Include only necessary packages

### Deploy-Time Security

#### 4. Harden Kubernetes Clusters
- Review cluster configuration against best practices
- Use tools like kube-bench for CIS compliance
- Build trust models for each component
- Use label taxonomies and governance
- Set up RBAC aligned with threat model
- Secure etcd and API server with TLS

#### 5. Integrating Security Tools
- Integrate clusters with existing security toolset
- Feed IP addresses and ports to perimeter security
- Use cloud provider security groups
- Align security groups with Kubernetes architecture

### Runtime Security

#### 6. Network Security Controls
- Security controls must be pod-aware, not just node-level
- Build network security into workload definitions
- Use Kubernetes-native network policy (Calico, Weavenet, Antrea)
- Use Kubernetes-native proxy (Envoy) for layer 7 policy
- Security definitions must be portable across environments

#### 7. Enterprise Security Controls
- Encrypt data in transit (TLS, mTLS, WireGuard VPN)
- Automate compliance reports (PCI, HIPAA, GDPR, SOC2)
- Aim for continuous compliance
- Use Kubernetes-native automation for remediation

#### 8. Threat Defense
- Intrusion detection: analyze data, identify anomalies
- Intrusion prevention: block malicious activity
- Aggregate by pods (not 5-tuple)
- Leverage machine learning for anomaly detection
- Use threat intelligence databases

## Main Security Issues

### Compromised Images
- Implement strong governance policies
- Use pre-approved secure base images
- Regular vulnerability scanning
- Standardize allowed registries

### Compromised Containers/Malicious Traffic
- Implement network policies
- Limit communication to minimum necessary
- Cover north-south and east-west traffic
- Auto-adjust policies for productivity

### Lack of Visibility
- Track large number of containers
- Handle distributed, dynamic workloads
- Multi-cloud visibility challenges
- Need consistent visibility across environments

## Key Takeaways

1. Security must span build, deploy, and runtime phases
2. Traditional security tools are insufficient for Kubernetes
3. Network policies must be pod-aware and portable
4. Continuous monitoring and remediation are essential
5. Compliance automation reduces manual effort

## Personal Notes

Este guia é excelente para entender a abordagem defense-in-depth. A divisão em build/deploy/runtime ajuda a organizar a implementação. A estatística de 94% com incidentes é alarmante - reforça a importância de segurança proativa.

Para implementação prática, focar em:
1. Image scanning no CI/CD
2. kube-bench para hardening
3. Network policies com Calico
4. mTLS com service mesh (Istio/Linkerd)