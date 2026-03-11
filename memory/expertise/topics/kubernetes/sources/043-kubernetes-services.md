# Kubernetes Services - Official Documentation

**Source:** kubernetes.io/docs/concepts/services-networking/service/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Documentação oficial sobre Services Kubernetes. Um Service é uma abstração que expõe aplicações de rede rodando como Pods no cluster.

## What is a Service?

### Purpose
- Expose network applications running as Pods
- Provide stable endpoint for dynamic Pod sets
- Enable service discovery without application modification

### Problem Solved
- Pods are ephemeral (created/destroyed dynamically)
- Each Pod gets its own IP address
- Pod IPs change over time
- Frontends need to find backends reliably

## Service API

### Core Concept
- Abstraction to expose groups of Pods over network
- Logical set of endpoints (usually Pods)
- Policy for making Pods accessible

### Definition Example
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
```

## Service Types

### ClusterIP (Default)
- Internal cluster access only
- Virtual IP assigned by Kubernetes
- Used for internal services

### NodePort
- Exposes service on each node's IP
- Port range: 30000-32767 (default)
- External access via node IP + port

### LoadBalancer
- Provisions external load balancer
- Cloud provider integration required
- External IP assigned automatically

### ExternalName
- Maps to DNS name
- No proxying, just DNS CNAME
- For external services

## Key Concepts

### Selectors
- Define which Pods belong to Service
- Label-based matching
- Controller continuously scans for matching Pods

### Endpoints
- Service targets Pods via EndpointSlices
- EndpointSlice API is stable (v1.21+)
- Legacy Endpoints API deprecated (v1.33)

### Port Configuration
- `port`: Service port
- `targetPort`: Container port (can be name or number)
- `protocol`: TCP (default), UDP, SCTP

## Services Without Selectors

### Use Cases
- External database cluster
- Service in different namespace/cluster
- Migration workload (partial backends)

### Implementation
- Define Service without selector
- Manually create EndpointSlice
- Link via kubernetes.io/service-name label

## Cloud-Native Service Discovery

### API-Based Discovery
- Query API server for EndpointSlices
- Kubernetes updates when Pods change

### Non-Native Applications
- Network port or load balancer
- Service discovery mechanisms provided

## Key Takeaways

1. Services abstract Pod networking complexity
2. ClusterIP is default type (internal only)
3. EndpointSlice API is preferred over Endpoints
4. Services without selectors enable hybrid deployments
5. Port names allow flexible configuration

## Personal Notes

Services são fundamentais para entender networking Kubernetes. A distinção entre ClusterIP, NodePort, LoadBalancer é essencial para CKA/CKAD.

Para certificação, memorizar:
- ClusterIP: internal only
- NodePort: 30000-32767 range
- LoadBalancer: requires cloud provider
- ExternalName: DNS mapping only

A feature de EndpointSlice é importante - substitui o antigo Endpoints API e suporta dual-stack clusters.