# 4 Ways to Securely Store & Manage Secrets in Docker

**Fonte:** https://blog.gitguardian.com/how-to-handle-secrets-in-docker/
**Data:** 2026-03-11
**Status:** Lido

---

## Resumo

Quatro métodos principais para gerenciar secrets em Docker: Docker Secrets (Swarm), Docker Compose, Sidecar containers, e Mozilla SOPS.

## 4 Métodos de Gestão de Secrets

### 1. Docker Secrets + Docker Swarm

**Inicializar Swarm:**
```bash
docker swarm init
```

**Criar Secret:**
```bash
# Gerar SSH key
ssh-keygen -t rsa -b 4096 -N "" -f mykey

# Criar secret no Docker
docker secret create my_key mykey

# Remover arquivo original (segurança!)
rm mykey

# Verificar
docker secret ls
```

**Usar em Serviço:**
```bash
docker service create --name mongodb --secret my_mongodb_secret redis:latest
```

**Usar em Compose:**
```yaml
version: '3.7'
services:
  myapp:
    image: mydummyapp:latest
    secrets:
      - my_secret_key

secrets:
  my_secret_key:
    external: true
```
- Secret montado em `/run/secrets/my_secret_key`

### 2. Docker Compose (File-based)

```yaml
version: '3.7'
services:
  myapp:
    image: myapp:latest
    secrets:
      - my_secret

secrets:
  my_secret:
    file: ./my_secret.txt
```

**⚠️ Cuidado:** Não commitar arquivo de secret no repositório!

### 3. Sidecar Container (Vault)

```yaml
version: '3.7'

services:
  mongo:
    image: mongo
    volumes:
      - secrets:/run/secrets
    environment:
      MONGO_INITDB_ROOT_USERNAME_FILE: /run/secrets/mongo-root-username
      MONGO_INITDB_ROOT_PASSWORD_FILE: /run/secrets/mongo-root-password

  secrets:
    image: vault
    volumes:
      - secrets:/secrets
    command: ["vault", "server", "-dev", "-dev-root-token-id=myroot"]
    ports:
      - "8200:8200"

volumes:
  secrets:
```

**Fluxo:**
1. Sidecar (Vault) gerencia secrets
2. Volume compartilhado entre containers
3. App lê secrets do volume

### 4. Mozilla SOPS

**Descriptografar arquivo:**
```bash
sops decrypt secret.enc.json
{
  "PASSWORD_1": "SuperSecretPassword",
  "PASSWORD_2": "AnotherSecretPassword"
}
```

**Passar para Docker:**
```bash
sops exec-env secret.enc.json 'docker run --rm -it -e PASSWORD_1=$PASSWORD_1 bash -c "echo $PASSWORD_1"'
```

**Com Docker Compose:**
```yaml
services:
  env_printer:
    image: alpine
    command: ["sh", "-c", "echo The secret is: $PASSWORD_1"]
    environment:
      - PASSWORD_1
```

```bash
sops exec-env secret.enc.json 'docker compose up'
```

**Vantagem:** Variável disponível apenas para processo Docker Compose, não para shell pai.

## Docker Build Secrets (BuildKit)

**Problema:** Secrets durante build podem ser embedded em image layers

**Solução:** BuildKit `--secret` mount

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    curl -H "Authorization: Bearer $API_KEY" https://api.example.com/data
```

**Build:**
```bash
echo "your-secret-key" | docker build --secret id=api_key,src=- .
```

**Benefícios:**
- Secret disponível apenas durante build step
- Não commitado em image layers
- Combinar com multi-stage builds para isolamento

## Docker Secrets Without Swarm

### Init Container Pattern

```yaml
version: '3.8'
services:
  secret-fetcher:
    image: vault:latest
    command: |
      sh -c "vault kv get -field=password secret/myapp > /shared/password"
    volumes:
      - shared-secrets:/shared

  myapp:
    image: myapp:latest
    depends_on:
      - secret-fetcher
    volumes:
      - shared-secrets:/run/secrets
```

### Encrypted Files (age/GPG)

1. Criptografar secrets com age/GPG
2. Container descriptografa no startup
3. Chaves passadas via canal seguro

## Environment Variables: Best Practices

**Riscos:**
- Visíveis em process lists
- `docker inspect` expõe
- Logs acidentais
- Debug tools

**Quando necessário:**
```bash
# Usar secret files para popular env vars
docker run -d \
  --env-file <(sops -d secrets.env) \
  --tmpfs /tmp:noexec,nosuid,size=100m \
  myapp:latest
```

**Docker Compose:**
```yaml
services:
  webapp:
    image: webapp:latest
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**Permissões:**
- Arquivos de secret: `chmod 600` ou `400`
- Adicionar ao `.gitignore`

## Scan de Secrets em Imagens

**Problema:** Imagens base podem conter secrets hard-coded

**Solução:** Scanner de secrets

```bash
ggshield secret scan docker ubuntu:22.04
```

**Estatística (2021):** 7% das imagens no Docker Hub continham pelo menos um secret

## Comparação de Métodos

| Método | Swarm Required | Complexidade | Segurança | Best For |
|--------|---------------|--------------|-----------|----------|
| Docker Secrets | Sim | Média | Alta | Swarm clusters |
| Compose Files | Não | Baixa | Média | Dev/small apps |
| Sidecar (Vault) | Não | Alta | Muito Alta | Enterprise |
| SOPS | Não | Média | Alta | GitOps workflows |
| BuildKit Secrets | Não | Baixa | Alta | Build time |

## Conclusão

1. **Nunca hard-code secrets** em Dockerfile ou imagens
2. **Use Docker Secrets** para Swarm
3. **Use BuildKit secrets** para build time
4. **Prefira file-based mounts** sobre environment variables
5. **Scaneie imagens** para secrets expostos
6. **Considere external secret managers** para enterprise

---
*GitGuardian oferece ggshield para detectar secrets em código, imagens e IaC*