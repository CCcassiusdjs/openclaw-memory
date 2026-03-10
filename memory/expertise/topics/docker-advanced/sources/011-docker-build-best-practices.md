# Docker Build Best Practices

**Fonte:** https://docs.docker.com/build/building/best-practices/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Melhores Práticas de Build

### 1. Usar Multi-stage Builds
- Separar build de runtime
- Imagens menores e mais seguras
- Execução paralela de stages

**Stages reutilizáveis:**
```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS builder
RUN npm ci
COPY . .
RUN npm run build

FROM base AS production
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/main.js"]
```

### 2. Escolher a Base Image Correta
| Tipo | Fonte | Confiabilidade |
|------|-------|----------------|
| Docker Official Images | hub.docker.com | Alta |
| Verified Publisher | hub.docker.com | Alta |
| Docker-Sponsored OSS | hub.docker.com | Média |

**Critérios:**
- Tamanho pequeno (Alpine, Distroless)
- Atualizações regulares
- Documentação clara
- Fonte confiável

### 3. Rebuildar Imagens Frequentemente
Imagens são imutáveis - precisam ser reconstruídas para updates:

```bash
# Pull fresh base image
docker build --pull -t my-image:latest .

# Clean build (no cache)
docker build --no-cache -t my-image:latest .

# Both together
docker build --pull --no-cache -t my-image:latest .
```

### 4. Usar .dockerignore
```plaintext
# Dependencies
node_modules
vendor

# Build artifacts
dist
build
*.o
*.pyc

# Development
.git
.env
*.log
tmp*

# IDE
.vscode
.idea
```

### 5. Containers Efêmeros
- Containers podem ser destruídos e recriados
- Configuração mínima no startup
- State externo (volumes, databases)

### 6. Não Instalar Pacotes Desnecessários
- Menor complexidade
- Menor superfície de ataque
- Menor tamanho
- Builds mais rápidos

### 7. Desacoplar Aplicações
Um container = uma responsabilidade:
- Web app + database + cache = 3 containers
- Facilita escala horizontal
- Reutilização de containers

### 8. Ordenar Argumentos Multi-linha
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```

**Benefícios:**
- Fácil manutenção
- Evita duplicação
- PRs mais fáceis de revisar

### 9. Aproveitar Build Cache
Ver: Cache Optimization (source 010)

### 10. Pin Base Image Versions
**Mutable tag:**
```dockerfile
FROM alpine:3.21  # Aponta para patch mais recente
```

**Pinned por digest:**
```dockerfile
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

**Trade-offs:**
- Tags: Updates automáticos, mas sem controle
- Digest: Controle total, mas updates manuais

### 11. Build e Test em CI/CD
Automatizar builds com GitHub Actions ou similar.

---

## Dockerfile Instructions

### FROM
- Usar imagens oficiais quando possível
- Alpine: < 6 MB, tightly controlled

### LABEL
Organizar imagens:
```dockerfile
LABEL com.example.version="0.0.1"
LABEL vendor="ACME Inc"
LABEL com.example.release-date="2024-01-15"
```

### RUN
Comandos longos em múltiplas linhas:
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo \
    && rm -rf /var/lib/apt/lists/*
```

---

## Checklist de Build

- [ ] Multi-stage builds para imagens menores
- [ ] Base image oficial e minimal
- [ ] .dockerignore configurado
- [ ] Layers ordenados (estáveis primeiro)
- [ ] Cache mounts para package managers
- [ ] Version pinning (tag ou digest)
- [ ] CI/CD configurado
- [ ] Containers efêmeros
- [ ] Uma responsabilidade por container

## Próximos Passos
- [ ] Revisar Dockerfiles existentes
- [ ] Implementar multi-stage builds
- [ ] Configurar cache mounts