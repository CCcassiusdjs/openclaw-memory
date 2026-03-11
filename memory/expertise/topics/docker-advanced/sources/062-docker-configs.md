# Store Configuration Data with Docker Configs - Docker Docs

**URL:** https://docs.docker.com/engine/swarm/configs/
**Lido em:** 2026-03-11
**Categoria:** Secrets Management
**Prioridade:** Alta

---

## Resumo

Documentação completa sobre Docker Configs para armazenar dados de configuração não-sensíveis em Swarm.

---

## O que são Configs

Dados de configuração não-sensíveis armazenados fora da imagem:
- Configuration files (nginx.conf, app.yml)
- Environment-specific settings
- Non-sensitive data

### Características:
- **NOT encrypted** at rest
- **Mounted directly** no filesystem (não usa RAM disk)
- **Shared** entre services
- **Maximum size:** 500 KB

### Limitação:
- **Apenas Swarm services** (não funciona com standalone containers)

---

## Como Docker Gerencia Configs

### Fluxo:
1. Config criado → enviado ao manager via TLS
2. Armazenado no Raft log (encrypted in transit)
3. Replicado para outros managers
4. Quando service acessa config:
   - Mount como arquivo no container
   - Location: `/<config-name>` (Linux)
5. Container para → config unmounted

### Location:
- **Linux:** `/<config_name>` (root)
- **Windows:** `C:\<config_name>` (symbolic link)

### Ownership:
- Default: user running container command (root)
- Pode especificar UID, GID, mode
- Windows: apenas admin/system access

---

## Comandos CLI

### Criar Config:

```bash
# De arquivo
docker config create my-config ./config.yml

# De stdin
echo "server_name: myapp" | docker config create my-config -

# Com template driver
docker config create --template-driver golang homepage index.html.tmpl
```

### Listar Configs:

```bash
docker config ls
```

### Inspecionar:

```bash
docker config inspect my-config
```

### Remover:

```bash
docker config rm my-config
```

**Nota:** Não pode remover config em uso por service.

---

## Usar Configs em Services

### Comando create:

```bash
# Uso básico
docker service create --name nginx --config site.conf nginx

# Com target específico
docker service create --name nginx \
  --config source=site.conf,target=/etc/nginx/conf.d/default.conf \
  nginx

# Com mode específico
docker service create --name nginx \
  --config source=site.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
  nginx

# Múltiplos configs
docker service create --name app \
  --config app.yml \
  --config nginx.conf \
  nginx
```

### Comando update:

```bash
# Adicionar config
docker service update --config-add source=app-v2.yml,target=app.yml myapp

# Remover config
docker service update --config-rm app.yml myapp
```

---

## Templated Configs

### Conceito:
- Conteúdo gerado dinamicamente com template engine
- Renderizado quando container é criado
- Variáveis: `{{ env "VAR" }}`, `{{ .Service.Name }}`

### Exemplo:

```html
<!-- index.html.tmpl -->
<html>
  <body>
    <p>Hello {{ env "HELLO" }}! I'm service {{ .Service.Name }}.</p>
  </body>
</html>
```

```bash
# Criar config com template
docker config create --template-driver golang homepage index.html.tmpl

# Usar com environment variable
docker service create \
  --name hello-template \
  --env HELLO="Docker" \
  --config source=homepage,target=/usr/share/nginx/html/index.html \
  nginx:alpine
```

### Variáveis Disponíveis:

| Placeholder | Descrição |
|-------------|-----------|
| `{{ env "VAR" }}` | Environment variable |
| `{{ .Service.Name }}` | Service name |
| `{{ .Service.ID }}` | Service ID |
| `{{ .Task.ID }}` | Task ID |
| `{{ .Node.ID }}` | Node ID |
| `{{ .Node.Hostname }}` | Node hostname |

---

## Rotação de Configs

### Processo:

1. Criar novo config (versão 2)
2. Atualizar service: remove old, add new
3. Remover old config

### Exemplo:

```bash
# 1. Criar novo config
docker config create site-v2.conf site.conf

# 2. Atualizar service
docker service update \
  --config-rm site.conf \
  --config-add source=site-v2.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
  nginx

# 3. Remover old config
docker config rm site.conf
```

---

## Configs em Compose

### Stack deploy:

```yaml
# compose.yml
services:
  nginx:
    image: nginx:latest
    configs:
      - source: site_conf
        target: /etc/nginx/conf.d/default.conf
        mode: 0440

configs:
  site_conf:
    file: ./nginx.conf
```

```bash
# Deploy como stack
docker stack deploy -c compose.yml mystack
```

### Nota:
- `configs` key é suportado em `docker stack deploy`
- **NÃO** é suportado em `docker compose up`

---

## Comparação: Configs vs Secrets

| Aspecto | Configs | Secrets |
|---------|----------|---------|
| **Encryption at rest** | Não | Sim |
| **Storage** | Filesystem | RAM disk (Linux) |
| **Use case** | Config files | Passwords, keys |
| **Size limit** | 500 KB | 500 KB |
| **Accessibility** | Swarm only | Swarm only |
| **Templating** | Suportado | Não |
| **Mode/UID/GID** | Sim | Sim (Linux only) |

---

## Windows Support

### Diferenças:
- Configs mounted em `C:\ProgramData\Docker\internal\configs`
- Symbolic links para target
- Sem UID/GID/mode (apenas admin/system)
- gMSA credentials: `config://<config-name>`

---

## Exemplos Práticos

### Nginx com Config:

```bash
# Criar config
docker config create site.conf nginx.conf

# Criar service
docker service create \
  --name nginx \
  --config source=site.conf,target=/etc/nginx/conf.d/site.conf,mode=0440 \
  --secret site.key \
  --secret site.crt \
  --publish 3000:443 \
  nginx:latest
```

### MySQL com Config:

```bash
# Criar config my.cnf
docker config create my_cnf my.cnf

# Criar service
docker service create \
  --name mysql \
  --config source=my_cnf,target=/etc/mysql/conf.d/my.cnf \
  --secret db_root_password \
  --secret db_password \
  mysql:latest
```

---

## Key Takeaways

1. **Não usar para dados sensíveis:** Use secrets para isso
2. **Imutáveis:** Não pode atualizar, criar novo
3. **Templating:** Permite configuração dinâmica
4. **Rotation:** Nome diferente para cada versão
5. **Compose:** Use `docker stack deploy`, não `docker compose up`