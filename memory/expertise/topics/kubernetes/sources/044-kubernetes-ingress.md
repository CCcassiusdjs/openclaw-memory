# Kubernetes Ingress - Official Documentation

**Source:** kubernetes.io/docs/concepts/services-networking/ingress/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Documentação oficial sobre Ingress Kubernetes. Ingress gerencia acesso externo aos serviços no cluster, tipicamente HTTP/HTTPS.

## What is Ingress?

### Definition
- API object managing external access to cluster services
- Typically HTTP/HTTPS
- Provides load balancing, SSL termination, name-based virtual hosting

### Important Note
- Kubernetes recommends using Gateway API instead of Ingress
- Ingress API is frozen (no further development)
- But Ingress remains generally available and supported

## Prerequisites

### Ingress Controller Required
- Ingress resource alone has no effect
- Must have an Ingress controller deployed
- Examples: nginx-ingress, Traefik, HAProxy, Istio

## Ingress Resource

### Minimal Example
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
spec:
  ingressClassName: nginx-example
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

### Required Fields
- apiVersion
- kind
- metadata
- spec

## Ingress Rules

### Components
1. **Host** (optional): e.g., foo.bar.com
2. **Paths**: e.g., /testpath
3. **Backend**: Service + port or Resource backend

### Rule Matching
- Host and path must match incoming request
- Traffic routed to listed backend
- defaultBackend handles unmatched requests

## Path Types

### ImplementationSpecific
- Matching up to IngressClass
- Can be treated as separate or same as Prefix/Exact

### Exact
- Matches URL path exactly
- Case sensitive

### Prefix
- Matches based on URL path prefix
- Split by / separator
- Case sensitive

### Examples
| Type | Path | Request | Match? |
|------|------|---------|--------|
| Prefix | / | /foo | Yes |
| Exact | /foo | /foo | Yes |
| Exact | /foo | /bar | No |
| Prefix | /foo | /foo/bar | Yes |
| Prefix | /aaa/bbb | /aaa/bbb/ccc | Yes |

## Hostname Wildcards

### Syntax
- `*.foo.com` matches single DNS label
- Exact match: `foo.bar.com`
- Wildcard: `*.foo.com`

### Matching Rules
- `*.foo.com` matches `bar.foo.com`
- `*.foo.com` does NOT match `baz.bar.foo.com`
- `*.foo.com` does NOT match `foo.com`

## IngressClass

### Purpose
- Different controllers, different configurations
- Each Ingress specifies a class
- References IngressClass resource

### Example
```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: external-lb
spec:
  controller: example.com/ingress-controller
  parameters:
    apiGroup: k8s.example.com
    kind: IngressParameters
    name: external-lb
```

### Scope
- Cluster-wide (default)
- Namespaced (set scope: Namespace)

## Key Takeaways

1. Ingress exposes HTTP/HTTPS routes to services
2. Requires Ingress Controller to function
3. Gateway API is the recommended successor
4. Path types: Exact, Prefix, ImplementationSpecific
5. Wildcards match only single DNS label
6. IngressClass enables multi-controller environments

## Personal Notes

Ingress é essencial para entender exposição de serviços HTTP/HTTPS. A transição para Gateway API é importante para acompanhar evolução.

Para CKA/CKAD, focar em:
- Path types (Exact vs Prefix)
- IngressClass configuration
- Default backend for unmatched traffic
- Hostname wildcards limitations

A separação entre Ingress resource e Ingress controller é fundamental - resource sem controller não funciona.