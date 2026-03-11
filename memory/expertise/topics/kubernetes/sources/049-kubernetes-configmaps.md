# Kubernetes ConfigMaps - Official Documentation

**Source:** kubernetes.io/docs/concepts/configuration/configmap/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

ConfigMaps são objetos API para armazenar dados não-confidenciais em pares chave-valor. Pods podem consumir ConfigMaps como variáveis de ambiente, argumentos de linha de comando, ou arquivos de configuração em volumes.

## Motivation

- Decouple environment-specific configuration from container images
- Enable portable applications across environments
- Same container image for development and production
- Configuration via environment variable (e.g., DATABASE_HOST)

## ConfigMap Object

### Key Fields
- `data`: UTF-8 strings (key-value pairs)
- `binaryData`: base64-encoded binary data
- `immutable`: Set to `true` for immutable ConfigMaps (v1.21+)

### Constraints
- Name must be valid DNS subdomain name
- Max size: 1 MiB
- Keys: alphanumeric, `-`, `_`, `.`
- Keys in `data` and `binaryData` must not overlap

### Example
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  # Property-like keys
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"
  
  # File-like keys
  game.properties: |
    enemy.types=aliens,monsters
    player.maximum-lives=5
  user-interface.properties: |
    color.good=purple
    color.bad=yellow
```

## Using ConfigMaps

### Four Methods
1. **Container command/args** - Use values in command line
2. **Environment variables** - Inject as env vars
3. **Volume files** - Mount as read-only files
4. **Kubernetes API** - Read directly from API

### As Environment Variables
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-configmap
spec:
  containers:
  - name: app
    image: nginx
    envFrom:
    - configMapRef:
        name: myconfigmap
```

### Single Key Reference
```yaml
env:
- name: CONFIGMAP_USERNAME
  valueFrom:
    configMapKeyRef:
      name: myconfigmap
      key: username
```

### As Volume Mount
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    configMap:
      name: myconfigmap
```

## Mounted ConfigMaps Are Updated Automatically

### Update Behavior
- When ConfigMap updated, projected keys are eventually updated
- kubelet checks on every periodic sync
- kubelet uses local cache for current value
- Total delay: kubelet sync period + cache propagation delay

### Important Notes
- ConfigMaps consumed as env vars are NOT updated automatically (require pod restart)
- Containers using `subPath` volume mount will NOT receive updates

## Immutable ConfigMaps

### Benefits
1. Protects from accidental/unwanted updates
2. Improves performance (reduces kube-apiserver load)
3. Closes watches for immutable ConfigMaps

### Creation
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  key1: value1
immutable: true
```

### Constraints
- Cannot revert to mutable
- Cannot modify data or binaryData fields
- Must delete and recreate to change

## Key Takeaways

1. ConfigMaps store non-confidential configuration data
2. Four consumption methods: env vars, command args, volumes, API
3. Max size: 1 MiB
4. Mounted ConfigMaps are updated automatically (env vars are not)
5. Immutable ConfigMaps improve performance
6. Use Secrets for confidential data

## Personal Notes

ConfigMaps são fundamentais para configuração de aplicações. A distinção entre data (strings) e binaryData (base64) é importante.

Para CKA/CKAD:
- envFrom: all keys as env vars
- valueFrom.configMapKeyRef: single key
- Volume mount: each key becomes a file
- subPath: prevents automatic updates

A feature de immutable ConfigMaps é valiosa para clusters grandes - reduz carga no API server.