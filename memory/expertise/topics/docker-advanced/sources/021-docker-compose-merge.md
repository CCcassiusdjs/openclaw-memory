# Docker Compose Merge Files

**Fonte:** https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Arquivos Default
- `compose.yaml` - Configuração base
- `compose.override.yaml` - Overrides (opcional)
- Compose lê automaticamente os dois

### 2. Múltiplos Arquivos
```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```
- Ordem importa: arquivos posteriores sobrepõem anteriores
- Útil para: dev, staging, production

---

## Regras de Merge

### Single-Value Options (Replace)
`image`, `command`, `mem_limit`, etc.

```yaml
# compose.yaml
services:
  myservice:
    command: python app.py

# compose.override.yaml
services:
  myservice:
    command: python otherapp.py

# Resultado
services:
  myservice:
    command: python otherapp.py
```

### Multi-Value Options (Concatenate)
`ports`, `expose`, `external_links`, `dns`, `dns_search`, `tmpfs`

```yaml
# compose.yaml
services:
  myservice:
    expose:
      - "3000"

# compose.override.yaml
services:
  myservice:
    expose:
      - "4000"
      - "5000"

# Resultado
services:
  myservice:
    expose:
      - "3000"
      - "4000"
      - "5000"
```

### Merged Options (Key-based)
`environment`, `labels`, `volumes`, `devices`

```yaml
# compose.yaml
services:
  myservice:
    environment:
      - FOO=original
      - BAR=original

# compose.override.yaml
services:
  myservice:
    environment:
      - BAR=local
      - BAZ=local

# Resultado
services:
  myservice:
    environment:
      - FOO=original
      - BAR=local    # Sobrescrito
      - BAZ=local    # Adicionado
```

### Volumes (Container Path)
Merge pelo caminho no container:

```yaml
# compose.yaml
services:
  myservice:
    volumes:
      - ./original:/foo
      - ./original:/bar

# compose.override.yaml
services:
  myservice:
    volumes:
      - ./local:/bar
      - ./local:/baz

# Resultado
services:
  myservice:
    volumes:
      - ./original:/foo
      - ./local:/bar    # Sobrescrito
      - ./local:/baz    # Adicionado
```

---

## Exemplo: Dev vs Production

### compose.yaml (Base)
```yaml
services:
  web:
    image: example/my_web_app:latest
    depends_on:
      - db
      - cache

  db:
    image: postgres:18

  cache:
    image: redis:latest
```

### compose.override.yaml (Dev)
```yaml
services:
  web:
    build: .
    volumes:
      - '.:/code'
    ports:
      - 8883:80
    environment:
      DEBUG: 'true'

  db:
    command: '-d'
    ports:
      - 5432:5432

  cache:
    ports:
      - 6379:6379
```

### compose.prod.yaml (Production)
```yaml
services:
  web:
    ports:
      - 80:80
    environment:
      PRODUCTION: 'true'

  cache:
    environment:
      TTL: '500'
```

### Deploy Production
```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```
- Não usa compose.override.yaml

---

## Usar stdin
```bash
docker compose -f - <<EOF
webapp:
  image: examples/web
  ports:
   - "8000:8000"
  volumes:
   - "/data"
  environment:
   - DEBUG=1
EOF
```

---

## Limitações

- Paths são relativos ao arquivo base
- Não funciona bem com monorepo
- Usar `docker compose config` para verificar merge

---

## Boas Práticas

1. **Base minimal** - compose.yaml com configuração canônica
2. **Override específico** - compose.override.yaml para dev
3. **Arquivos por ambiente** - compose.prod.yaml, compose.staging.yaml
4. **Verificar merge** - `docker compose config` antes de deploy
5. **Paths consistentes** - Sempre relativos ao arquivo base

## Próximos Passos
- [ ] Criar compose.override.yaml para dev
- [ ] Separar compose.prod.yaml
- [ ] Automatizar com scripts de deploy