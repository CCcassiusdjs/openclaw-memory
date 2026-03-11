# Build Secrets - Documentação Oficial

**Fonte:** https://docs.docker.com/build/building/secrets/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## O que são Build Secrets

Informações sensíveis (senhas, API tokens) consumidas durante o build. **NÃO use build args ou env vars** - eles persistem na imagem!

---

## Tipos de Build Secrets

| Tipo | Uso |
|------|-----|
| **Secret mounts** | Arquivos ou env vars para build |
| **SSH mounts** | SSH sockets ou chaves para git clone |
| **Git auth** | Autenticação para contextos remotos |

---

## Por que não usar ARG/ENV?

```dockerfile
# ❌ ERRADO - Secret persiste na imagem
ARG API_TOKEN
RUN curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com

# ✅ CORRETO - Secret não persiste
RUN --mount=type=secret,id=api_token \
    curl -H "Authorization: Bearer $(cat /run/secrets/api_token)" https://api.example.com
```

---

## Secret Mounts

### Passar Secret no Build

**CLI:**
```bash
docker build --secret id=aws,src=$HOME/.aws/credentials .
```

**Bake:**
```hcl
variable "HOME" {
  default = null
}

target "default" {
  secret = [
    "id=aws,src=${HOME}/.aws/credentials"
  ]
}
```

### Consumir no Dockerfile

**Default (arquivo):**
```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp s3://bucket/file .
```

**Target customizado:**
```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp s3://bucket/file .
```

**Como environment variable:**
```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    aws s3 cp s3://bucket/file .
```

**Arquivo E environment variable:**
```dockerfile
RUN --mount=type=secret,id=token,target=/run/secrets/token,env=TOKEN \
    curl -H "Authorization: Bearer $TOKEN" https://api.example.com
```

---

## Sources de Secrets

### Arquivo
```bash
docker build --secret id=aws,src=$HOME/.aws/credentials .
```

### Environment Variable
```bash
# Detectado automaticamente
docker build --secret id=kube,env=KUBECONFIG .

# Variável com mesmo nome
export API_TOKEN=xxx
docker build --secret id=API_TOKEN .
# Monta em /run/secrets/API_TOKEN
```

---

## SSH Mounts

Para clonar repositórios privados via SSH.

### Passar SSH
```bash
docker buildx build --ssh default .
```

### Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine

# Clona repo privado
ADD git@github.com:me/myprivaterepo.git /src/

# Ou com SSH mount explícito
RUN --mount=type=ssh \
    git clone git@github.com:me/myprivaterepo.git /src
```

---

## Git Authentication para Remote Contexts

### Problema
```bash
docker build https://gitlab.com/example/todo-app.git
# ERROR: could not read Username for 'https://gitlab.com'
```

### Solução: GIT_AUTH_TOKEN
```bash
GIT_AUTH_TOKEN=$(cat gitlab-token.txt) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://gitlab.com/example/todo-app.git
```

### GIT_AUTH_HEADER (Basic Auth)
```bash
export GIT_AUTH_TOKEN=$(cat gitlab-token.txt)
export GIT_AUTH_HEADER=basic

docker build \
  --secret id=GIT_AUTH_TOKEN \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

### Multiple Hosts
```bash
export GITLAB_TOKEN=$(cat gitlab-token.txt)
export GERRIT_TOKEN=$(cat gerrit-username-password.txt)
export GERRIT_SCHEME=basic

docker build \
  --secret id=GIT_AUTH_TOKEN.gitlab.com,env=GITLAB_TOKEN \
  --secret id=GIT_AUTH_TOKEN.gerrit.internal.example,env=GERRIT_TOKEN \
  --secret id=GIT_AUTH_HEADER.gerrit.internal.example,env=GERRIT_SCHEME \
  https://gitlab.com/example/todo-app.git
```

---

## Authentication Schemes

| Scheme | Header |
|--------|--------|
| **Bearer** (default) | `Authorization: Bearer <token>` |
| **Basic** | `Authorization: Basic <base64(user:pass)>` |

---

## Conceitos Aprendidos

1. **Secrets não persistem** - Montados temporariamente
2. **Não usar ARG/ENV** - Persistem na imagem
3. **Sources** - Arquivo ou environment variable
4. **Target** - Pode ser arquivo ou env var ou ambos
5. **SSH mounts** - Para git clone privado
6. **GIT_AUTH_TOKEN** - Para contexts remotos privados

---

## Best Practices

1. **Use secrets para tokens/senhas** - Nunca ARG/ENV
2. **SSH mounts para git** - Mais seguro que tokens
3. **Per-host authentication** - Tokens diferentes para hosts
4. **Non-blocking** - Para builds com muitos logs

---

## Aplicações Práticas

1. **Private package registries** - npm, PyPI privados
2. **Cloud APIs** - AWS, GCP, Azure durante build
3. **Git clone** - Repositórios privados
4. **Certificate access** - Certificados durante build

---

## Referências Cruzadas

- Ver: `024-docker-build-secrets.md`
- Ver: `003-docker-security-overview.md`
- Relacionado: SSH mounts, GIT_AUTH_TOKEN