# Secrets - Kubernetes Official Documentation

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/configuration/secret/
**Data:** Janeiro 2026
**Tópico:** Secrets Management, Security, Types, Best Practices
**Status:** Lido

---

## Resumo Executivo

Documentação oficial de Secrets, cobrindo tipos, uso, segurança, alternativas e melhores práticas para gerenciamento de dados sensíveis em Kubernetes.

---

## O que são Secrets

### Definição
- Objeto para armazenar dados sensíveis
- Senhas, tokens, chaves, credenciais
- Separado da especificação do Pod
- Permite evitar dados confidenciais em código/container images

### Segurança Padrão (Atenção!)
- Secrets são armazenados **não criptografados** no etcd por padrão
- Qualquer um com API access pode ler/modificar
- Qualquer um com etcd access pode ler
- Qualquer um que pode criar Pods no namespace pode ler Secrets

### Passos Mínimos de Segurança
1. Habilitar **Encryption at Rest** para Secrets
2. Configurar RBAC com least-privilege
3. Restringir acesso a containers específicos
4. Considerar **External Secret Stores** (Vault, etc.)

---

## Usos de Secrets

### Casos Comuns
- Environment variables para containers
- Credenciais SSH/senhas para Pods
- Image pull secrets para registries privados
- Bootstrap tokens para node registration

---

## Tipos de Secrets

### Built-in Types

| Tipo | Uso |
|------|-----|
| `Opaque` | Dados arbitrários (padrão) |
| `kubernetes.io/service-account-token` | Token de ServiceAccount |
| `kubernetes.io/dockercfg` | ~/.dockercfg serializado |
| `kubernetes.io/dockerconfigjson` | ~/.docker/config.json |
| `kubernetes.io/basic-auth` | Credenciais basic auth |
| `kubernetes.io/ssh-auth` | Credenciais SSH |
| `kubernetes.io/tls` | Certificados TLS |
| `bootstrap.kubernetes.io/token` | Bootstrap tokens |

### Opaque Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
```

### TLS Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS...
  tls.key: LS0tLS...
```

### Docker Config Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: eyJhdXRocyI6...
```

---

## Consumindo Secrets

### Como Environment Variables
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: app
    image: myapp
    env:
    - name: SECRET_USERNAME
      valueFrom:
        secretKeyRef:
          name: my-secret
          key: username
```

### Como Volume Mounts
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-pod
spec:
  containers:
  - name: app
    image: myapp
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secrets"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: my-secret
```

### Image Pull Secrets
```yaml
apiVersion: v1
kind: Pod
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: my-registry/myapp:v1
```

---

## Secrets Visíveis a Um Container

### Use Case: Isolamento
- Frontend container: lida com requests, NÃO vê a chave
- Signer container: vê a chave, responde a requests de signing
- Atacante precisa comprometer dois processos

### Configuração
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: frontend
    image: myapp-frontend
    # Não monta o secret
  
  - name: signer
    image: myapp-signer
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secrets"
      readOnly: true
  
  volumes:
  - name: secret-volume
    secret:
      secretName: signing-key
```

---

## Dotfiles em Secret Volumes

### Conceito
- Chaves iniciando com `.` são arquivos ocultos
- Útil para configuração "invisível"

### Exemplo
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: dotfile-secret
data:
  .secret-file: dmFsdWUtMg0KDQo=
---
apiVersion: v1
kind: Pod
metadata:
  name: secret-dotfiles-pod
spec:
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
  containers:
  - name: dotfile-test-container
    image: registry.k8s.io/busybox
    volumeMounts:
    - name: secret-volume
      readOnly: true
      mountPath: "/etc/secret-volume"
# Arquivo: /etc/secret-volume/.secret-file (oculto)
```

---

## Alternativas a Secrets

### ServiceAccount Tokens
- Usar tokens de ServiceAccount para autenticação intra-cluster
- Não precisa de Secrets adicionais

### Third-Party Tools
- Serviços externos que revelam secrets mediante autenticação
- Vault, AWS Secrets Manager, etc.

### Custom Signers
- Implementar signer X.509 customizado
- Usar CertificateSigningRequests

### Device Plugins
- Expor hardware de criptografia do node
- Trusted Platform Module (TPM)

### Operadores
- Operator que busca tokens de curta duração
- Cria Secrets baseados nesses tokens
- Pods usam tokens sem saber mecanismos

---

## Segurança de Secrets

### Informação Sensível
- Secrets são **base64 encoded**, NÃO criptografados
- `echo -n "value" | base64` é facilmente reversível
- Qualquer acesso ao Secret revela o conteúdo

### Encryption at Rest
```yaml
# EncryptionConfiguration
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-key>
  - identity: {}
```

### RBAC Restritivo
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["my-secret"]  # Apenas este secret
```

---

## ServiceAccount Token Secrets (Legacy)

### Aviso
- `kubernetes.io/service-account-token` é legado
- Tokens de longa duração, não rotacionam

### Recomendação Atual
- Usar **TokenRequest API** para tokens de curta duração
- Usar **projected volumes** para montar tokens
- Tokens são invalidados quando Pod é deletado

### TokenRequest
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    volumeMounts:
    - name: token
      mountPath: "/var/run/secrets/kubernetes.io/serviceaccount"
  volumes:
  - name: token
    projected:
    - serviceAccountToken:
        path: token
        expirationSeconds: 3600
        audience: "my-audience"
```

---

## Insights para Kubernetes

1. **Secrets não são seguros por padrão**: Precisam de configuração adicional
2. **Base64 ≠ criptografia**: Apenas encoding, não proteção
3. **Encryption at Rest é obrigatório**: Para dados sensíveis reais
4. **RBAC é crítico**: Restringir acesso com least privilege
5. **External secrets stores**: Considerar Vault, AWS Secrets Manager

---

## Palavras-Chave
`secrets` `security` `encryption-at-rest` `service-accounts` `tls` `docker-config` `kubernetes`