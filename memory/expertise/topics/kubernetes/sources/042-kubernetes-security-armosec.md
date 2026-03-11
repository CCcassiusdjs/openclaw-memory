# Kubernetes Security Best Practices for Security Professionals (ArmoSec)

**Source:** armosec.io/blog/kubernetes-security-best-practices/
**Type:** Security Guide
**Priority:** High
**Date:** 2026

---

## Summary

Guia detalhado sobre segurança Kubernetes usando o modelo "4Cs": Cloud, Cluster, Container, Code. Aborda desde fundamentos até práticas avançadas de hardening.

## Understanding Kubernetes Architecture

### Core Components
- **Pod**: Set of containers (atomic deployment unit)
- **Node**: Worker or control plane machine
- **Cluster**: Collection of nodes running workloads
- **Control Plane**: API server, scheduler, controller manager

### Node Components
- kubelet
- kube-proxy
- Container runtime

## The 4Cs Security Model

### Overview
1. **Cloud/Colocated**: Infrastructure layer
2. **Cluster**: Kubernetes configuration
3. **Container**: Application packaging
4. **Code**: Application logic

## Cloud Layer Security

### 1. Prevent Unwanted Access to API Server
- Limit network layer access to API server
- Don't expose API server to open internet
- Use VPC restriction
- Use VPN or SSH bastion for external access

## Cluster Layer Security

### 2. Controlling Access to API Server

#### Authentication & Authorization Flow
1. Request authenticated
2. Request authorized
3. Admission control applied

#### TLS Requirements
- Use TLS for all API server connections
- TLS for control plane internal communication
- TLS for control plane to kubelet

#### Service Accounts
- Provide identity for Pod processes
- Critical for cluster security
- Each application should have own service account
- Avoid default service account (auto-mounted)
- Disable auto-mounting of default tokens

#### Credentials Management
- Control access to kubeconfigs and service account tokens
- Newer versions use TokenRequest API (short-lived tokens)
- Manual tokens can be created without expiration
- Kubeconfigs can be created without expiration
- Stolen credentials require cluster reinstall with new root CA

### 3. Kubernetes Secrets

#### Purpose
- Hold sensitive information (passwords, keys, tokens)
- Decouple sensitive from non-sensitive configuration
- Reduce chance of accidental exposure

#### Characteristics
- RBAC-controlled
- Namespaced objects
- Max size: 1 MB
- Stored in tmpfs on nodes (not persistent storage)
- Base64-encoded (NOT encryption)

#### Best Practice
- Enable encryption in API server configuration
- Use encryption for etcd data
- Kubernetes supports multiple encryption schemes:
  - Local key pairs
  - CSP-hosted KMS

### 4. Protect Nodes

#### CIS Benchmark Guidelines
- Enable SELinux for mandatory access controls
- Disable unnecessary services/daemons
- Configure firewall rules
- Limit kernel capabilities
- Use read-only container filesystems where possible

## Container Layer Security

### 5. Use Trusted Images
- Use images from trusted registries
- Use proper image tags (not just :latest)
- Scan images before deployment
- Use signed images

### 6. Reduce Container Attack Surface
- Use minimal base images
- Remove unnecessary packages
- Don't run as root
- Use read-only filesystems

### 7. Scan for Vulnerabilities
- Continuous vulnerability scanning
- Scan base images
- Scan application dependencies
- Integrate scanning into CI/CD

## Code Layer Security

### 8. Apply Least Privilege
- Minimal permissions for applications
- No privileged containers unless absolutely necessary
- Limit capabilities
- Use Pod Security Standards

## Key Takeaways

1. The 4Cs model provides comprehensive security coverage
2. API server is the primary entry point - secure it well
3. Secrets need encryption at rest
4. Node hardening follows CIS benchmarks
5. Service accounts should be application-specific
6. Container images must be scanned and trusted

## Personal Notes

O modelo 4Cs é uma excelente framework mental para organizar segurança Kubernetes. A ênfase em que secrets são base64-encoded (não encrypteds) é importante - muitos confundem isso.

Para CKA/CKAD, memorizar:
- Service accounts: one per application
- TLS required everywhere
- Secrets: encrypt at rest
- Node hardening: CIS benchmarks