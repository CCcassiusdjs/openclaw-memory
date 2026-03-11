# Kubernetes API - Official Documentation

**Source:** kubernetes.io/docs/concepts/overview/kubernetes-api/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

A Kubernetes API é o ponto central de comunicação do cluster. Toda interação passa pelo API Server via HTTP API RESTful.

## API Server Role

- Core of control plane
- Exposes HTTP API
- Handles queries and manipulation of objects
- All components communicate via API

## Access Methods

1. **kubectl** - CLI tool
2. **kubeadm** - Cluster admin
3. **Client libraries** - Go, Python, Java, etc.
4. **Direct REST calls** - HTTP requests

## API Specifications

### Discovery API
- Lists all group versions and resources
- Aggregated (v2) or unaggregated format
- `/api` and `/apis` endpoints

### Aggregated Discovery (Preferred)
- Two endpoints only: `/api` and `/apis`
- Reduces requests significantly
- Supports ETag and protobuf
- Uses Accept header: `application/json;v=v2;g=apidiscovery.k8s.io`

### Unaggregated Discovery
- Separate endpoint per group version
- `/apis/<group>/<version>`
- Used by kubectl for resource lists

## OpenAPI Interface

### OpenAPI V2
- Endpoint: `/openapi/v2`
- Accept headers for format
- Some fields dropped (default, nullable, oneOf)

### OpenAPI V3 (Preferred)
- Stable since v1.27
- More comprehensive representation
- Per group version: `/openapi/v3/apis/<group>/<version>?hash=<hash>`
- Immutable URLs for caching
- HTTP cache headers set (1 year expiry)

## Persistence

- Objects stored in etcd
- Serialized state
- API server handles all reads/writes

## API Groups and Versioning

### API Groups
- Group related resources together
- Can be enabled/disabled
- Example: `rbac.authorization.k8s.io`

### API Versions
- Version at API level (not resource/field)
- Multiple versions for same resource
- API server handles conversion transparently

### Version Levels
- **v1**: GA (General Availability)
- **v1beta1**: Beta
- **v1alpha1**: Alpha

### Versioning Guarantees
- GA APIs: maintained for compatibility
- Beta APIs: data preserved via GA
- Alpha APIs: may change incompatibly

## API Changes

### Compatibility
- New resources/fields: added frequently
- Removed fields: follow deprecation policy
- GA APIs: strong compatibility commitment

### Deprecation Policy
- Beta APIs: transition before removal
- Alpha APIs: check release notes
- Data preserved across versions

## API Extension

### Custom Resources
- Define new resource types
- Declarative API definition
- CRDs (CustomResourceDefinitions)

### Aggregation Layer
- Extend API with external APIs
- API aggregation servers
- Custom API servers

## Key Takeaways

1. API Server is central communication hub
2. Access via kubectl, client libraries, or REST
3. Discovery API lists all resources
4. OpenAPI v3 is preferred (more complete)
5. API groups organize resources
6. API versioning ensures compatibility
7. Extensions via CRDs or aggregation layer

## Personal Notes

A Kubernetes API é a espinha dorsal do cluster. Tudo passa pelo API Server.

Para CKA/CKAD:
- API groups: core (v1) and named (e.g., rbac.authorization.k8s.io)
- API versions: v1 (GA), v1beta1 (beta), v1alpha1 (alpha)
- Discovery: `/api` and `/apis` endpoints
- OpenAPI v3 preferred over v2

A feature de aggregated discovery é importante para performance - reduz número de requests. A garantia de compatibilidade para GA APIs é fundamental para upgrade planning.