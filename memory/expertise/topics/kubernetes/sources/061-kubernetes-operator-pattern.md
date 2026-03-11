# Kubernetes Operator Pattern - Official Documentation

**Source:** kubernetes.io/docs/concepts/extend-kubernetes/operator/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Operators são extensões de software que usam custom resources para gerenciar aplicações e seus componentes. Seguem princípios do Kubernetes, notadamente o control loop.

## Motivation

### Purpose
- Capture knowledge of human operators
- Automate tasks beyond what Kubernetes provides
- Manage specific applications with domain knowledge

### What Operators Do
- Deploy applications on demand
- Take and restore backups
- Handle upgrades (code + schema)
- Publish services for discovery
- Simulate failures for testing
- Handle leader election

## How Operators Work

### Components
1. **Custom Resource Definition (CRD)**: Defines the resource type
2. **Controller**: Watches CRD instances and takes action
3. **Custom Logic**: Application-specific automation

### Control Loop
1. Watch for CRD changes
2. Compare current state vs desired state
3. Take action to reconcile
4. Update status

## Example: SampleDB Operator

### Custom Resource
```yaml
apiVersion: example.com/v1
kind: SampleDB
metadata:
  name: my-database
spec:
  version: "15.0"
  storage: 100Gi
```

### What Operator Does
- Creates StatefulSet for database
- Creates PersistentVolumeClaim for storage
- Creates Job for initial configuration
- Handles backups (periodic)
- Handles upgrades (version changes)
- Takes snapshots before deletion

## Deploying Operators

### Common Pattern
- Deploy CRD + Controller as Deployment
- Controller runs outside control plane
- Uses service account with appropriate RBAC

### Installation Methods
- OperatorHub.io (catalog)
- Manual YAML manifests
- OLM (Operator Lifecycle Manager)

## Writing Your Own Operator

### SDKs and Frameworks
- **Kubebuilder**: Go-based SDK
- **Operator Framework**: Go SDK with metrics
- **Java Operator SDK**: Java-based
- **Kopf**: Python-based
- **Kube-rs**: Rust-based
- **KubeOps**: .NET-based
- **Mast**: General framework

### Key Concepts
1. **Reconcile Loop**: Core pattern for all operators
2. **Event Handling**: Respond to CRUD events
3. **Child Resources**: Manage dependent resources
4. **Status Updates**: Report current state

## Operator Maturity Model

### Level 1: Install
- Basic installation
- Configurable

### Level 2: Upgrade
- Seamless upgrades
- Version management

### Level 3: Backup/Restore
- Full lifecycle management
- Data protection

### Level 4: Deep Insights
- Metrics and alerts
- Monitoring integration

### Level 5: Auto-pilot
- Horizontal/vertical scaling
- Auto-tuning
- Exception handling

## Key Takeaways

1. Operators extend Kubernetes with application-specific automation
2. Combine CRD + Controller for declarative management
3. Capture operational knowledge in code
4. Follow control loop pattern
5. Multiple SDKs available for different languages
6. Maturity model guides development

## Personal Notes

Operators são a forma padrão de estender Kubernetes para aplicações complexas. O padrão de control loop é fundamental.

Para CKA/CKAD:
- Operator = CRD + Controller
- Reconcile loop: watch, compare, act, update
- Use OperatorHub for existing operators
- Kubebuilder is most common Go SDK

O Operator White Paper da CNCF é referência importante para design de operators. A feature de auto-pilot (level 5) é o objetivo final para automation completa.