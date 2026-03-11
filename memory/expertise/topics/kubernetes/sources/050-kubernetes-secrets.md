# Kubernetes Secrets - Official Documentation

**Source:** kubernetes.io/docs/concepts/configuration/secret/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Secrets armazenam dados sensíveis como senhas, tokens, ou chaves. Permitem separar informações confidenciais da especificação do Pod e imagens de container.

## Security Warning

### Default Behavior
- Secrets stored unencrypted in etcd
- Anyone with API access can retrieve/modify
- Anyone with etcd access can read
- Pod creators can read any Secret in namespace

### Required Security Steps
1. **Enable Encryption at Rest** for Secrets
2. **Enable RBAC** with least-privilege access
3. **Restrict Secret access** to specific containers
4. **Consider external Secret stores** (Vault, etc.)

## Uses for Secrets

1. **Environment variables** - Set container env vars
2. **Credentials** - SSH keys, passwords for Pods
3. **Image pull** - Private registry credentials
4. **Bootstrap tokens** - Node registration automation

## Types of Secrets

### Built-in Types

| Type | Usage |
|------|-------|
| Opaque | Arbitrary user-defined data (default) |
| kubernetes.io/service-account-token | ServiceAccount token |
| kubernetes.io/dockercfg | Serialized ~/.dockercfg |
| kubernetes.io/dockerconfigjson | Serialized ~/.docker/config.json |
| kubernetes.io/basic-auth | Basic authentication credentials |
| kubernetes.io/ssh-auth | SSH authentication credentials |
| kubernetes.io/tls | TLS client/server data |
| bootstrap.kubernetes.io/token | Bootstrap token data |

### Opaque Secrets
- Default type if not specified
- Created with: `kubectl create secret generic`
- Can contain any key-value pairs

### ServiceAccount Token Secrets
- Legacy mechanism for long-lived tokens
- **Recommended**: Use TokenRequest API for short-lived tokens
- Auto-rotating tokens via projected volume

### Docker Config Secrets
- Store registry credentials
- Type: `kubernetes.io/dockerconfigjson`
- Created with: `kubectl create secret docker-registry`

## Creating Secrets

### From Literal
```bash
kubectl create secret generic my-secret \
  --from-literal=username=admin \
  --from-literal=password='S3cr3t!'
```

### From File
```bash
kubectl create secret generic my-secret \
  --from-file=username=./username.txt \
  --from-file=password=./password.txt
```

### From YAML
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: UzNjcjN0IQ==
```

### Using stringData
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
stringData:  # Not base64 encoded (API encodes it)
  username: admin
  password: S3cr3t!
```

## Using Secrets in Pods

### As Environment Variables
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: nginx
    env:
    - name: USERNAME
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: username
```

### As Volume Mount
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secret"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: my-secret
```

## Alternatives to Secrets

1. **ServiceAccount tokens** - For in-cluster authentication
2. **External secret services** - HashiCorp Vault, AWS Secrets Manager
3. **Custom signers** - X.509 certificates
4. **Device plugins** - TPM, hardware security modules

## Key Takeaways

1. Secrets store sensitive data separately from code
2. Default storage is unencrypted - enable encryption at rest
3. RBAC should restrict access to minimum necessary
4. Multiple types available (Opaque, TLS, dockerconfigjson)
5. Can be consumed as env vars or volume mounts
6. Consider external secret stores for production

## Personal Notes

Secrets são essenciais para segurança mas requerem configuração adicional. O fato de serem base64-encoded (não encrypted) é frequentemente mal-entendido.

Para CKA/CKAD:
- Opaque é o tipo padrão
- stringData evita base64 manual
- secretKeyRef para único valor
- envFrom para todos os valores
- Volume mount: cada key vira arquivo

A feature de encryption at rest é CRÍTICA para produção - sem isso, Secrets são plaintext em etcd.