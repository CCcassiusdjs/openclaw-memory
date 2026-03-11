# Manage Sensitive Data with Docker Secrets - Docker Docs

**URL:** https://docs.docker.com/engine/swarm/secrets/
**Lido em:** 2026-03-11
**Categoria:** Secrets Management
**Prioridade:** Alta

---

## Resumo

Documentação completa sobre Docker Secrets para gerenciamento de dados sensíveis em Swarm.

---

## O que são Secrets

Blob de dados sensíveis que não deve ser transmitido em clear text ou armazenado em Dockerfiles:
- Passwords
- SSH private keys
- TLS certificates
- API tokens
- Database credentials

### Características:
- **Encrypted in transit and at rest** (Raft log)
- **Only accessible** to services com acesso explícito
- **Mounted in-memory** (RAM disk)
- **Maximum size:** 500 KB

### Limitação:
- **Apenas Swarm services** (não funciona com standalone containers)

---

## Como Docker Gerencia Secrets

### Fluxo:
1. Secret criado → enviado ao manager via TLS
2. Armazenado no Raft log (encrypted)
3. Replicado para outros managers
4. Quando service acessa secret:
   - Decrypt e mount no container
   - Location: `/run/secrets/<secret_name>`
5. Container para → secret unmounted e flushed da memória

### Node Connectivity:
- Node perde conexão → mantém acesso aos secrets ativos
- Não recebe updates até reconectar

---

## Windows Support

### Diferenças:
- **Sem RAM disk:** Secrets persistem em clear text no disco (root)
- **Removidos quando container para**
- **BitLocker recomendado** para encryption at rest
- **Custom targets:** Usam symbolic links de `C:\ProgramData\Docker\internal\secrets`
- **Sem UID/GID/mode:** Apenas admin e system access

---

## Comandos CLI

### Criar Secret:

```bash
# De arquivo
docker secret create my_secret ./secret.txt

# De stdin
echo "secret_value" | docker secret create my_secret -

# De openssl
openssl rand -base64 20 | docker secret create db_password -
```

### Listar Secrets:

```bash
docker secret ls
```

### Inspecionar:

```bash
docker secret inspect my_secret
```

### Remover:

```bash
docker secret rm my_secret
```

**Nota:** Não pode remover secret em uso por service.

---

## Usar Secrets em Services

### Comando create:

```bash
# Uso básico
docker service create --name myapp --secret db_password nginx

# Com target específico
docker service create --name myapp \
  --secret source=db_password,target=/etc/passwd \
  nginx

# Múltiplos secrets
docker service create --name myapp \
  --secret db_password \
  --secret api_key \
  nginx
```

### Comando update:

```bash
# Adicionar secret
docker service update --secret-add source=new_pass,target=db_password myapp

# Remover secret
docker service update --secret-rm db_password myapp
```

---

## Usar Secrets em Compose

### docker-compose.yml:

```yaml
services:
  db:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
      MYSQL_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_root_password
      - db_password

  wordpress:
    image: wordpress:latest
    environment:
      WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - source: db_password
        target: wp_db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  db_root_password:
    file: ./secrets/db_root_password.txt
```

---

## Rotação de Secrets

### Processo:

1. Criar novo secret (versão 2)
2. Atualizar service com ambos (old + new)
3. Aplicar mudança no application
4. Atualizar service para usar apenas new
5. Remover old secret

### Exemplo:

```bash
# 1. Criar novo secret
openssl rand -base64 20 | docker secret create mysql_password_v2 -

# 2. Atualizar MySQL com ambos
docker service update \
  --secret-rm mysql_password \
  --secret-add source=mysql_password,target=old_mysql_password \
  --secret-add source=mysql_password_v2,target=mysql_password \
  mysql

# 3. Mudar password no MySQL
docker exec <container> mysqladmin \
  --user=wordpress \
  --password="$(< /run/secrets/old_mysql_password)" \
  password "$(< /run/secrets/mysql_password)"

# 4. Atualizar WordPress
docker service update \
  --secret-rm mysql_password \
  --secret-add source=mysql_password_v2,target=wp_db_password \
  wordpress

# 5. Remover old secret
docker service update --secret-rm mysql_password mysql
docker secret rm mysql_password
```

---

## Best Practices

1. **Versão no nome:** `db_password_v1`, `db_password_v2`
2. **Environment variables:** Use `*_FILE` variants
3. **Nunca commitar secrets** em source control
4. **Rotação regular:** Planejar rotação
5. **Minimal access:** Apenas serviços que precisam

---

## Comparação: Secrets vs Configs

| Aspecto | Secrets | Configs |
|---------|---------|---------|
| **Encryption** | Sim (at rest) | Não |
| **Storage** | RAM disk | Filesystem |
| **Use case** | Senhas, keys | Config files |
| **Size limit** | 500 KB | 500 KB |
| **Accessibility** | Swarm only | Swarm only |

---

## Key Takeaways

1. **Encrypted at rest:** Mais seguro que configs
2. **In-memory:** Não persiste no disco (Linux)
3. **Rotation:** Versionar nomes para facilitar
4. **Compose support:** `_FILE` environment variables
5. **500 KB limit:** Suficiente para maioria dos casos