# Docker Swarm Secrets

**Fonte:** https://docs.docker.com/engine/swarm/secrets/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## O que são Secrets

Secrets = dados sensíveis gerenciados pelo Docker Swarm:
- Senhas
- Chaves SSH
- Certificados TLS
- Tokens de API
- Strings ou binários (até 500 KB)

**Características:**
- Criptografados em trânsito e em repouso
- Acessíveis apenas a serviços autorizados
- Montados em RAM (não em disco)
- Removidos quando container para

---

## Como Funciona

1. Secret criado via `docker secret create`
2. Enviado ao Swarm Manager via TLS
3. Armazenado no Raft log (criptografado)
4. Replicado para outros managers
5. Montado no container quando serviço autorizado

**Localização no container:**
- Linux: `/run/secrets/<secret_name>`
- Windows: `C:\ProgramData\Docker\secrets`

---

## Comandos Principais

### Criar Secret
```bash
# De arquivo
docker secret create my_secret ./secret.txt

# De stdin
printf "my_password" | docker secret create my_secret -

# De string
echo "my_password" | docker secret create my_secret -
```

### Listar Secrets
```bash
docker secret ls
```

### Inspecionar Secret
```bash
docker secret inspect my_secret
```

### Remover Secret
```bash
docker secret rm my_secret
# Nota: Não pode remover se serviço está usando
```

### Usar Secret em Serviço
```bash
# Criar serviço com secret
docker service create \
  --name my_app \
  --secret my_secret \
  nginx:alpine

# Com target customizado
docker service create \
  --name my_app \
  --secret source=my_secret,target=/etc/my_secret \
  nginx:alpine
```

### Adicionar/Remover Secret de Serviço Existente
```bash
# Adicionar
docker service update --secret-add my_secret my_app

# Remover
docker service update --secret-rm my_secret my_app
```

---

## Docker Compose

```yaml
version: "3.8"

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Criado fora do Compose

services:
  app:
    image: my_app:latest
    secrets:
      - db_password
      - source: api_key
        target: /etc/api_key
        uid: "1000"
        gid: "1000"
        mode: 0400
```

---

## Rotação de Secrets

1. Criar novo secret com versão:
```bash
docker secret create db_password_v2 ./new_password.txt
```

2. Atualizar serviço:
```bash
docker service update \
  --secret-rm db_password \
  --secret-add source=db_password_v2,target=db_password \
  my_app
```

3. Remover old secret:
```bash
docker secret rm db_password
```

---

## Suporte Windows

**Diferenças:**
- Secrets em disco (não RAM) - removidos ao parar
- Recomendado BitLocker no host
- Sem suporte a UID/GID/mode
- Acesso: admins e system only

---

## Best Practices

### 1. Versionar Secrets
```bash
db_password_v1
db_password_v2
db_password_v3
```

### 2. Não Commitar Secrets
- Usar `.dockerignore` para arquivos de secret
- Usar `external: true` no Compose

### 3. Rotação Regular
- Trocar secrets periodicamente
- Automatizar rotação em CI/CD

### 4. Nomes Descritivos
```bash
prod_db_password
staging_api_key
dev_jwt_secret
```

### 5. Limpar Secrets Não Usados
```bash
docker secret ls
docker secret rm old_secret
```

---

## Limitações

- **Apenas Swarm Services** - Não funciona em containers standalone
- **Tamanho máximo: 500 KB**
- **Não pode atualizar** - Criar novo e trocar
- **Não pode remover se em uso** - Remover do serviço primeiro

---

## Comparação: Secrets vs Configs vs Environment Variables

| Característica | Secrets | Configs | Env Vars |
|----------------|---------|---------|----------|
| Criptografado | Sim | Não | Não |
| Em memória | Sim | Não (disco) | Depende |
| Swarm only | Sim | Sim | Não |
| Tamanho max | 500 KB | Não definido | ~128 KB |
| Rotação | Manual | Manual | Manual |
| Audit trail | Sim | Sim | Não |

---

## Próximos Passos
- [ ] Implementar secrets em produção
- [ ] Automatizar rotação
- [ ] Migrar env vars para secrets