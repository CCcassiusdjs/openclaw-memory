# Kubernetes Custom Resources - Official Documentation

**Source:** kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Custom Resources são extensões da Kubernetes API. Permitem definir novos tipos de recursos além dos built-in como Pods e Services.

## Custom Resources vs Built-in Resources

### Custom Resource
- Extension of Kubernetes API
- Not available in default installation
- Created dynamically in running cluster
- Accessed via kubectl like built-in resources

### Built-in Resource
- Part of core Kubernetes
- Pods, Services, Deployments, etc.
- Always available

## Custom Controllers

### Purpose
- Custom resources alone only store/retrieve data
- Custom controller + custom resource = declarative API
- Controller enforces desired state

### Operator Pattern
- Combines custom resources and custom controllers
- Encodes domain knowledge
- Extends Kubernetes API

## When to Use Custom Resources

### Use Custom Resources If:
- API is declarative (small objects, CRUD operations)
- Want kubectl support
- Want Kubernetes UI visibility
- Developing new API
- Resources are cluster/namespace scoped
- Want to reuse Kubernetes API features

### Use Stand-alone API If:
- API is not declarative (RPC, transactions)
- kubectl support not required
- Already have working API program
- Need specific REST paths
- Storing large amounts of data
- High bandwidth access needed

## ConfigMap vs Custom Resource

### Use ConfigMap If:
- Existing configuration file format (mysql.cnf, pom.xml)
- Entire config in one key
- Main use is Pod consumption
- Consumers prefer file/env var access
- Want rolling updates via Deployment

### Use Custom Resource If:
- Want kubectl and client library support
- Want automation watching for updates
- Want .spec, .status, .metadata conventions
- Object abstracts controlled resources

## Adding Custom Resources

### Two Methods

#### 1. CustomResourceDefinition (CRD)
- Simple, no programming required
- Created via YAML
- Handled by main API server

#### 2. API Aggregation
- Requires programming
- Write and deploy custom API server
- More control over behavior
- Custom storage layer

### Comparison

| Feature | CRD | Aggregated API |
|---------|-----|----------------|
| Programming required | No | Yes |
| Additional service | No | Yes |
| Ongoing support | Auto via K8s | Manual updates |
| Multi-versioning | Limited | Full |
| Custom storage | No | Yes |
| Custom business logic | Webhooks | Native |
| Subresources | Yes (scale, status) | Yes (all) |

## CRD Features

### Validation
- OpenAPI v3.0 validation
- ValidatingAdmissionWebhook
- CRDValidationRatcheting

### Defaulting
- OpenAPI default keyword
- MutatingAdmissionWebhook

### Multi-versioning
- Serve same object through multiple API versions
- Conversion webhook for version conversion

### Subresources
- `/scale` - Integration with HPA
- `/status` - Separate spec/status access

## Key Takeaways

1. CRDs extend Kubernetes API without programming
2. API Aggregation offers more flexibility but requires code
3. Use ConfigMap for application config, CRD for Kubernetes integration
4. Custom controllers enable declarative APIs
5. Operator pattern = CRD + custom controller
6. CRDs are easier, Aggregation is more flexible

## Personal Notes

CRDs são a forma mais comum de estender Kubernetes. O Operator pattern é poderoso para automatizar aplicações complexas.

Para CKA/CKAD:
- CRD: define schema via YAML
- CR: instance of CRD
- Controller: watches and reconciles
- Use ConfigMap for config, CRD for extensions

A distinction entre declarative e imperative API é importante - CRDs funcionam melhor com modelo declarativo. O Operator pattern é amplamente usado para databases, monitoring, etc.