# Docker Multi-stage Builds

**Fonte:** https://docs.docker.com/build/building/multi-stage/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. O que são Multi-stage Builds
- Múltiplos `FROM` statements em um Dockerfile
- Cada `FROM` inicia um novo stage de build
- Artifacts podem ser copiados entre stages
- Resultado: imagens menores, sem ferramentas de build

### 2. Benefícios
- Imagens de produção menores
- Dockerfile único (sem scripts separados)
- Separação de build e runtime
- Facilidade de manutenção

### 3. Sintaxe Básica

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25 AS build
WORKDIR /src
COPY main.go .
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

### 4. Nomear Stages
- Default: stages numerados (0, 1, 2...)
- `AS <name>` para nomear stages
- Referenciar por nome é mais robusto

```dockerfile
FROM golang:1.25 AS build
# ...
FROM scratch
COPY --from=build /bin/hello /bin/hello
```

### 5. Stop at Specific Stage
Build apenas até stage específico:

```bash
docker build --target build -t hello .
```

**Use cases:**
- Debugging de stage específico
- Stage `debug` com símbolos vs `production` sem
- Stage `testing` com dados de teste vs `production` com dados reais

### 6. External Image as Stage
Copiar de imagem externa:

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

Docker faz pull automatico se necessário.

### 7. Previous Stage as New Stage
Continuar de stage anterior:

```dockerfile
FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
COPY source1.cpp source.cpp
RUN g++ -o /binary source.cpp

FROM builder AS build2
COPY source2.cpp source.cpp
RUN g++ -o /binary source.cpp
```

### 8. BuildKit vs Legacy Builder

| Aspecto | BuildKit | Legacy Builder |
|---------|----------|----------------|
| Stages não usados | Ignorados | Processados |
| Performance | Melhor (paralelo) | Pior (sequencial) |
| Cache | Mais eficiente | Menos eficiente |

**Exemplo:**
```dockerfile
FROM ubuntu AS base
RUN echo "base"

FROM base AS stage1
RUN echo "stage1"

FROM base AS stage2
RUN echo "stage2"
```

- `--target stage2` com BuildKit: só processa base + stage2
- Sem BuildKit: processa base + stage1 + stage2

---

## Padrões Comuns

### Build + Runtime
```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/main.js"]
```

### Multiple Builds
```dockerfile
# Backend build
FROM golang:1.25 AS backend
WORKDIR /src
COPY backend/ .
RUN go build -o /bin/server ./main.go

# Frontend build
FROM node:20 AS frontend
WORKDIR /app
COPY frontend/ .
RUN npm ci && npm run build

# Final image
FROM alpine:latest
COPY --from=backend /bin/server /server
COPY --from=frontend /app/dist /static
CMD ["/server"]
```

### Distroless Images
```dockerfile
FROM golang:1.25 AS build
WORKDIR /src
COPY main.go .
RUN CGO_ENABLED=0 go build -o /app main.go

FROM gcr.io/distroless/static-debian12
COPY --from=build /app /
CMD ["/app"]
```

### Debug Stage
```dockerfile
FROM golang:1.25 AS build
WORKDIR /src
COPY . .
RUN go build -o /app main.go

# Debug stage (com delves, etc)
FROM build AS debug
RUN go install github.com/go-delve/delve/cmd/dlv@latest
CMD ["dlv", "debug", "/app"]

# Production stage (minimal)
FROM alpine:latest AS production
COPY --from=build /app /
CMD ["/app"]
```

---

## Boas Práticas

1. **Nomear stages** - Facilita manutenção
2. **Usar imagens pequenas** - alpine, distroless, scratch
3. **Separar build e runtime** - Não incluir ferramentas de build na imagem final
4. **Aproveitar cache** - Ordenar instruções da menos frequente para mais frequente
5. **Usar .dockerignore** - Reduz contexto de build
6. **Especificar versões** - `FROM node:20.10.0-alpine` não `FROM node`
7. **BuildKit habilitado** - `DOCKER_BUILDKIT=1` ou Docker 23.0+

## Próximos Passos
- [ ] Estudar BuildKit cache backends
- [ ] Praticar com diferentes linguagens
- [ ] Configurar debug stages