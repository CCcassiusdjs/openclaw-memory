# Inside Job: Defending Kubernetes Clusters Against Network Misconfigurations

**Source:** arXiv:2506.21134  
**Type:** Academic Research Paper  
**URL:** https://arxiv.org/abs/2506.21134  
**Date:** June 2025  
**Author:** Jacopo Bufalino  
**Published:** ACM (DOI: 10.1145/3749220)  
**Status:** Completed

---

## Summary

This paper addresses a critical gap in Kubernetes security: **network configuration impact on application security**. It presents a comprehensive analysis of network misconfigurations enabling **lateral movement attacks** in Kubernetes clusters.

---

## Key Findings

### Study Scope

| Metric | Value |
|--------|-------|
| **Applications analyzed** | 287 open-source apps |
| **Organizations covered** | 6 (IT, public entities, non-profits) |
| **Misconfigurations found** | 634 |
| **Applications fixed** | 30+ (as of publication) |

### Security Impact

- Misconfigurations enable **lateral movement** within clusters
- Found issues **beyond state-of-the-art detection tools**
- Demonstrated real-world exploitation paths

---

## Methodology

1. **Analyzed 287 open-source applications**
2. **Identified network misconfigurations**
3. **Assessed lateral movement potential**
4. **Responsible disclosure** to affected organizations
5. **Proposed mitigations** for each issue

---

## Concepts Learned

| Concept | Description |
|---------|-------------|
| **Network Misconfiguration** | Improper network policies enabling attacks |
| **Lateral Movement** | Attacker moving within cluster after initial compromise |
| **NetworkPolicy Gaps** | Missing or overly permissive policies |
| **Responsible Disclosure** | Reporting vulnerabilities before publication |
| **Cluster Security Posture** | Overall security state of Kubernetes deployment |

---

## Types of Misconfigurations

| Category | Examples |
|----------|----------|
| **Missing NetworkPolicy** | No policies restricting pod-to-pod traffic |
| **Overly Permissive Policies** | Policies allowing all traffic |
| **Default Namespace Issues** | Workloads in default namespace without isolation |
| **Service Exposure** | Unnecessary external exposure |
| **Ingress Misconfigurations** | Insecure ingress rules |

---

## Lateral Movement Attack Path

```
Initial Compromise
       ↓
Reconnaissance (enabled by misconfig)
       ↓
Lateral Movement (pod-to-pod)
       ↓
Privilege Escalation
       ↓
Data Exfiltration / Cluster Takeover
```

---

## Impact

- **634 misconfigurations** identified across 287 applications
- **30+ applications** fixed with proposed mitigations
- Exposed gaps in existing security tools
- Provided actionable remediation guidance

---

## Recommendations

1. **Implement NetworkPolicy** for all namespaces
2. **Use namespace isolation** for workload separation
3. **Apply least privilege** to network policies
4. **Regular security audits** of network configurations
5. **Automated policy validation** in CI/CD

---

## Cross-References

- **Network Policies** → Sources 047-053 (CNI/Networking)
- **Security practices** → Sources 003, 002 (Security Commandments/Landscape)
- **RBAC** → Sources 061-066 (Authorization)
- **Pod Security** → Sources 015-017 (Security Concepts)

---

*Read date: 2026-03-11*