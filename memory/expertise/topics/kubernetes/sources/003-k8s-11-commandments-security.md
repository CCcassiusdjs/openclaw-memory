# XI Commandments of Kubernetes Security: A Systematization of Knowledge

**Source:** arXiv:2006.15275  
**Type:** Academic Research Paper  
**URL:** https://arxiv.org/abs/2006.15275  
**Date:** June 2020  
**Author:** Akond Rahman PhD  
**Status:** Completed

---

## Summary

This paper systematizes knowledge about Kubernetes security practices through **qualitative analysis of 104 Internet artifacts** (blog posts, documentation, grey literature). The goal is to help practitioners secure Kubernetes installations by identifying **11 key security practices** (the "XI Commandments").

---

## Key Findings

### The 11 Kubernetes Security Commandments

1. **Implement RBAC Authorization** - Role-Based Access Control for least privilege
2. **Apply Security Patches** - Keep Kubernetes components updated
3. **Implement Pod Security Policies** - Control pod capabilities
4. **Implement Network Security Policies** - Restrict pod-to-pod communication
5. **Secure Container Images** - Use minimal, trusted base images
6. **Limit Container Privileges** - Avoid privileged containers
7. **Use Namespaces for Isolation** - Logical separation of workloads
8. **Secure Secrets Management** - Properly manage sensitive data
9. **Enable Audit Logging** - Track cluster activities
10. **Implement Resource Limits** - Prevent resource exhaustion
11. **Monitor and Alert** - Continuous observability

---

## Methodology

- **Source Material:** 104 Internet artifacts analyzed
- **Approach:** Qualitative analysis (systematization of knowledge)
- **Focus:** Grey literature + practitioner practices
- **Goal:** Synthesize actionable security practices

---

## Security Concepts Learned

| Concept | Description |
|---------|-------------|
| **RBAC** | Role-Based Access Control for fine-grained permissions |
| **Least Privilege** | Grant only necessary permissions |
| **Pod Security Policies** | Control what pods can do |
| **Network Policies** | Restrict inter-pod communication |
| **Container Isolation** | Logical separation via namespaces |
| **Secrets Management** | Secure handling of credentials |
| **Audit Logging** | Activity tracking for compliance |
| **Resource Quotas** | Prevent noisy neighbor issues |
| **Privileged Containers** | Containers with host-level access (avoid) |

---

## Real-World Security Incidents

- **Tesla (2018)** - Kubernetes cluster compromised, used for crypto mining
- Demonstrates real-world impact of security gaps

---

## Organizations Using Kubernetes

- IBM
- Capital One
- Adidas

Benefits reported: **increased deployment frequency**

---

## Implications for Practice

| Area | Recommendation |
|------|---------------|
| **Access Control** | Implement RBAC with least privilege |
| **Updates** | Regular security patching |
| **Network** | Apply network policies |
| **Pods** | Use Pod Security Policies |
| **Images** | Minimal, trusted base images |
| **Secrets** | External secrets management |
| **Observability** | Audit logging + monitoring |

---

## Cross-References

- **RBAC deep dive** → Sources 018-019, 061-066
- **Container security** → Sources 041-046
- **Network policies** → Sources 047-053
- **Security best practices** → Sources 004-040

---

*Read date: 2026-03-11*