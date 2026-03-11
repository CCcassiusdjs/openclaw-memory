# Declarative Management of Kubernetes Objects - Official Documentation

**Source:** kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Gerenciamento declarativo usa arquivos de configuração e `kubectl apply` para criar, atualizar e deletar objetos Kubernetes. O estado desejado é declarado em arquivos, e o Kubernetes aplica as mudanças automaticamente.

## Three Management Approaches

| Approach | Commands | Use Case |
|----------|----------|----------|
| Imperative commands | kubectl run, kubectl expose | Quick tasks, learning |
| Imperative config | kubectl create -f, kubectl replace -f | Production config files |
| Declarative config | kubectl apply -f | Production, GitOps |

## Declarative Configuration

### Key Concepts
- **Configuration file**: YAML/JSON defining desired state
- **Live object configuration**: Current state in cluster
- **Last-applied-configuration annotation**: Tracks applied config

### Creating Objects
```bash
kubectl apply -f <directory> -R  # Recursive
kubectl diff -f <directory>       # Preview changes
```

### The Annotation
```yaml
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1",...}
```

## How Updates Work

### Field Management
1. Fields in config file: set in live object
2. Fields removed from config: cleared in live object
3. Fields not in config: preserved (manual changes)

### Example
```yaml
# Original config
spec:
  replicas: 3
  minReadySeconds: 5

# After kubectl scale --replicas=2 (imperative)
spec:
  replicas: 2  # Changed imperatively

# After update config (removed minReadySeconds)
spec:
  replicas: 2  # Preserved (not in config)
  # minReadySeconds cleared by apply
```

### Warning
Do NOT mix `kubectl apply` with `kubectl create/replace`:
- create/replace don't set last-applied-configuration
- apply cannot track changes properly

## Deleting Objects

### Method 1: kubectl delete (Recommended)
```bash
kubectl delete -f <filename>
```
- Explicit about what's deleted
- Less risk of unintended deletion

### Method 2: kubectl apply --prune
```bash
kubectl apply -f <directory> --prune -l <labels>
```
- Deletes objects not in directory
- Uses labels to identify scope
- Requires last-applied-configuration annotation

### Pruning Modes (v1.35)
- **Allowlist-based**: Alpha, usability issues
- **ApplySet-based**: Alpha, replacement for allowlist

#### ApplySet-based Pruning
```bash
kubectl apply -f <directory> --prune --applyset=<name>
```
- Uses server-side object to track membership
- More accurate and efficient
- Requires enabling ApplySet feature gate

## Best Practices

### Directory Structure
```
configs/
├── namespace.yaml
├── deployment.yaml
├── service.yaml
└── kustomization.yaml  # Optional
```

### Version Control
- Store configs in Git
- Use GitOps workflows
- Review changes before apply

### Preview Changes
```bash
kubectl diff -f <directory>
kubectl apply -f <directory> --dry-run=server
```

### Separate Environments
```
configs/
├── base/
│   └── deployment.yaml
└── overlays/
    ├── dev/
    └── prod/
```

## Key Takeaways

1. Declarative config uses `kubectl apply` to manage state
2. last-applied-configuration annotation tracks changes
3. Manual changes preserved unless in config file
4. Don't mix apply with create/replace
5. Use `kubectl delete` for explicit deletion
6. `--prune` for automatic cleanup (use carefully)
7. Preview with `kubectl diff` before applying

## Personal Notes

Declarative management é a abordagem recomendada para produção. GitOps usa este padrão.

Para CKA/CKAD:
- kubectl apply -f <directory>: apply all configs
- kubectl diff -f <directory>: preview changes
- last-applied-configuration: tracks state
- Manual changes preserved by default

A feature de ApplySet é mais confiável que allowlist pruning. Sempre use kubectl delete para evitar deleções acidentais.