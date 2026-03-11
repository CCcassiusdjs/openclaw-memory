# Kubernetes Secrets (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/configuration/secret/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Secrets armazenam dados sensíveis (passwords, tokens, keys) de forma segura, permitindo que aplicações consumam credenciais sem hardcoded values.

---

## ⚠️ Nota de Segurança

**Por padrão, Secrets NÃO são criptografados no etcd.**

### Passos Obrigatórios:
1. Habilitar Encryption at Rest
2. Configurar RBAC com least-privilege
3. Restringir acesso a containers específicos
4. Considerar external secret stores

---

## O que são Secrets?

### Definição
- API object para dados sensíveis
- Similar a ConfigMaps, mas para confidencial
- Armazena passwords, tokens, SSH keys, TLS certs
- Máximo 1 MiB

### Vantagens
- Decouple secrets de container images
- Evita hardcoded secrets
- Pode montar como volumes ou env vars
- Rotação sem rebuild de images

---

## Tipos de Secrets

### Opaque (Default)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: c2VjcmV0
```

### kubernetes.io/service-account-token
- Tokens para ServiceAccounts
- Legacy (v1.22+)
- Use TokenRequest API para novos tokens

### kubernetes.io/dockerconfigjson
- Credenciais para registries privados
```bash
kubectl create secret docker-registry my-registry \
  --docker-email=user@example.com \
  --docker-username=user \
  --docker-password=password \
  --docker-server=my-registry.example:5000
```

### kubernetes.io/basic-auth
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: t0p-Secret
```

### kubernetes.io/ssh-auth
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ssh-auth
type: kubernetes.io/ssh-auth
data:
  ssh-privatekey: <base64-encoded-key>
```

### kubernetes.io/tls
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
```

### bootstrap.kubernetes.io/token
- Tokens para node bootstrap
- Formato: bootstrap-token-<token-id>

---

## Criando Secrets

### Imperativo
```bash
# From literal
kubectl create secret generic my-secret --from-literal=username=admin --from-literal=password=secret

# From file
kubectl create secret generic my-secret --from-file=username.txt --from-file=password.txt

# TLS secret
kubectl create secret tls my-tls --cert=path/to/cert --key=path/to/key
```

### Declarativo (YAML)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
stringData:  # Sem base64
  username: admin
  password: secret
```

**Nota:** stringData é mais conveniente, mas data (base64) é recomendado para produção.

---

## Consumindo Secrets

### 1. Environment Variables
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

### 2. Volume Mount
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
```

### 3. imagePullSecrets (Registries)
```yaml
apiVersion: v1
kind: Pod
spec:
  imagePullSecrets:
  - name: my-registry-secret
  containers:
  - name: app
    image: my-registry.example/app:latest
```

---

## Immutable Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
immutable: true
data:
  key: value
```

### Benefícios
- Protege contra updates acidentais
- Melhora performance do kube-apiserver
- Kubelet não precisa watch para updates

---

## Secret Updates

### Volumes
- Atualizados automaticamente
- Kubelet periodicamente sincroniza
- Pod pode não ver update imediatamente

### Environment Variables
- **NÃO atualizados automaticamente**
- Requer restart do Pod

### SubPath
- SubPath mounts **não recebem** updates automáticos

---

## Alternatives to Secrets

### Service Account Tokens (Recomendado)
- Tokens de curta duração
- TokenRequest API
- Automaticamente rotacionados

### External Secret Stores
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- GCP Secret Manager

### Secrets Store CSI Driver
```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-secrets
spec:
  provider: vault
  parameters:
    roleName: "my-role"
    objects: |
      - objectName: "db-password"
        secretPath: "secret/data/db"
        secretKey: "password"
```

---

## Security Best Practices

1. **Enable Encryption at Rest**
   ```yaml
   # /etc/kubernetes/encryption-config.yaml
   apiVersion: apiserver.config.k8s.io/v1
   kind: EncryptionConfiguration
   resources:
   - providers:
     - aescbc:
         keys:
         - name: key1
           secret: <base64-encoded-key>
   ```

2. **Limit RBAC Access**
   - Least privilege para Secrets
   - Namespace-scoped Roles
   - Não dar list/watch para secrets

3. **Use External Secrets**
   - HashiCorp Vault
   - Secrets Store CSI Driver

4. **Short-lived Tokens**
   - TokenRequest API
   - Bound Service Account Tokens

5. **Audit Logging**
   - Habilitar audit logs
   - Monitorar access a Secrets

---

## Conceitos-Chave

1. **Secret Types**: Opaque, TLS, dockerconfigjson, etc.
2. **Base64 Encoding**: Não é encryption!
3. **Encryption at Rest**: Habilitar para segurança
4. **Immutable**: Secrets que não mudam
5. **External Secrets**: Vault, cloud providers

---

## Tabela de Tipos

| Tipo | Uso | Keys Obrigatórias |
|------|-----|------------------|
| Opaque | Generic secrets | Nenhuma |
| service-account-token | SA tokens | token |
| dockerconfigjson | Registry auth | .dockerconfigjson |
| basic-auth | Basic auth | username, password |
| ssh-auth | SSH keys | ssh-privatekey |
| tls | TLS certs | tls.crt, tls.key |
| bootstrap-token | Node bootstrap | token-id, token-secret |

---

## Próximos Passos de Estudo

- [ ] External Secrets Operator
- [ ] Vault integration
- [ ] Secrets Store CSI Driver
- [ ] Encryption at Rest configuration
- [ ] Secret rotation strategies

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/configuration/secret/
- Good Practices: https://kubernetes.io/docs/concepts/security/secrets-good-practices/
- Secrets Store CSI: https://secrets-store-csi-driver.sigs.k8s.io/