# Docker Cache Optimization

**Fonte:** https://docs.docker.com/build/cache/optimize/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Técnicas de Otimização de Cache

### 1. Ordenar Layers
- Instruções mais estáveis primeiro
- Instruções que mudam frequentemente por último
- Evita rebuild de layers não modificadas

**Errado:**
```dockerfile
FROM node
WORKDIR /app
COPY . .          # Copia tudo primeiro
RUN npm install   # Invalida se QUALQUER arquivo mudar
RUN npm build
```

**Correto:**
```dockerfile
FROM node
WORKDIR /app
COPY package.json yarn.lock .  # Apenas dependências
RUN npm install                # Cache hit se deps não mudarem
COPY . .                       # Código fonte
RUN npm build                  # Rebuild só se código mudar
```

### 2. Manter Contexto Pequeno
Usar `.dockerignore`:
```plaintext
node_modules
tmp*
*.log
.git
.env
```

### 3. Usar Bind Mounts
Monta arquivos do host sem adicionar layers:

```dockerfile
FROM golang:latest
WORKDIR /build
RUN --mount=type=bind,target=. go build -o /app/hello
```

**Vantagens:**
- Não adiciona arquivos ao cache
- Código fonte disponível durante build
- Output escrito fora do mount point

**Notas:**
- Bind mounts são read-only por default
- Mudanças não são persistidas na imagem
- Arquivos não aparecem no `COPY`

### 4. Usar Cache Mounts
Cache persistente para package managers:

**Node.js:**
```dockerfile
RUN --mount=type=cache,target=/root/.npm npm install
```

**Go:**
```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/hello
```

**Python:**
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Rust:**
```dockerfile
RUN --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/git/db \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    cargo build
```

**Apt (com lock para builds paralelos):**
```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y gcc
```

### 5. Usar Cache Externo
Para CI/CD, usar registry como cache:

```yaml
# GitHub Actions
- name: Build and push
  uses: docker/build-push-action@v7
  with:
    push: true
    tags: user/app:latest
    cache-from: type=registry,ref=user/app:buildcache
    cache-to: type=registry,ref=user/app:buildcache,mode=max
```

**Local:**
```bash
docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

---

## Comparação de Técnicas

| Técnica | Benefício | Quando Usar |
|---------|-----------|-------------|
| Ordenar layers | Cache hits mais frequentes | Sempre |
| .dockerignore | Contexto menor | Sempre |
| Bind mounts | Menos layers no cache | Builds com código fonte grande |
| Cache mounts | Cache de pacotes | Package managers |
| Cache externo | Compartilhar cache | CI/CD |

---

## Boas Práticas

1. **Sempre usar .dockerignore** - Reduz contexto
2. **Separar COPY de dependências** - Maximiza cache hits
3. **Cache mounts para package managers** - Reutiliza downloads
4. **Cache externo em CI/CD** - Compartilha entre builds
5. **Bind mounts para builds** - Evita layers desnecessários

## Próximos Passos
- [ ] Estudar cache backends (S3, GCS, etc.)
- [ ] Implementar em pipelines CI/CD
- [ ] Medir tempo de build antes/depois