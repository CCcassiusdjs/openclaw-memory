# Use Compose in Production - Docker Docs

**URL:** https://docs.docker.com/compose/how-tos/production/
**Lido em:** 2026-03-11
**Categoria:** Compose Advanced
**Prioridade:** Média

---

## Resumo

Guia oficial para usar Docker Compose em ambientes de produção.

---

## Modificar Compose para Produção

### Mudanças Comuns:
- Remover volume bindings de código (segurança)
- Bindar portas diferentes no host
- Configurar environment variables para produção
- Especificar restart policy (`restart: always`)
- Adicionar serviços adicionais (log aggregator)

### Multiple Compose Files:

```bash
# Usar compose.production.yaml sobre compose.yaml
docker compose -f compose.yaml -f compose.production.yaml up -d
```

### Exemplo compose.production.yaml:

```yaml
services:
  web:
    image: myapp:latest
    restart: always
    environment:
      - LOG_LEVEL=warning
    ports:
      - "8080:80"
    volumes: []  # Remove dev bindings
```

---

## Deploying Changes

### Rebuild e Recreate:

```bash
# Rebuild imagem
docker compose build web

# Recreate service (sem dependências)
docker compose up --no-deps -d web
```

**Flags:**
- `--no-deps`: Não recreates serviços dependentes
- `-d`: Detached mode

---

## Remote Docker Host

### Variáveis de Ambiente:

```bash
export DOCKER_HOST=tcp://remote-host:2376
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH=/path/to/certs
```

### Após configurar:
Todos os comandos `docker compose` funcionam remotamente.

---

## Swarm Cluster

### Deploy em Swarm:

```bash
# Deploy como stack
docker stack deploy -c compose.yaml mystack
```

---

## Best Practices

### Produção vs Desenvolvimento:

| Aspecto | Desenvolvimento | Produção |
|---------|----------------|----------|
| **Volumes** | Bind mounts | Named volumes |
| **Ports** | Portas expostas | Portas específicas |
| **Restart** | `no` ou `on-failure` | `always` |
| **Logging** | Verbose | Warning/Error |
| **Secrets** | Arquivos locais | Docker secrets |
| **Environment** | .env files | Docker configs |

---

## Key Takeaways

1. **Multiple Compose Files:** Override para produção
2. **Rebuild + Recreate:** Sempre ambos para code changes
3. **--no-deps:** Evita cascata de recreates
4. **DOCKER_HOST:** Deploy remoto transparente
5. **Security:** Remover volume bindings em produção