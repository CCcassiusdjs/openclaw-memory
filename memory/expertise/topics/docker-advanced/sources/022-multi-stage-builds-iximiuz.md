# Docker Multi-Stage Builds - iximiuz Labs

**Fonte:** https://labs.iximiuz.com/tutorials/docker-multi-stage-builds
**Tipo:** Tutorial
**Lido em:** 2026-03-10
**Status:** completed

---

## O Problema: Imagens Gigantes

### Dependências Build-time vs Run-time
- **Build-time:** Compilers, linters, dev tools (muito mais numerosas)
- **Run-time:** Apenas o necessário para rodar a aplicação

**Problema:** Build-time dependencies frequentemente acabam em imagens de produção.

### Exemplo Go (ERRADO)
```dockerfile
# DO NOT DO THIS
FROM golang:1.23

WORKDIR /app
COPY . .
RUN go build -o binary
CMD ["/app/binary"]
```

**Problemas:**
- `golang` image não é para produção
- Inclui todo toolchain Go
- 800MB+ de pacotes
- ~800 CVEs detectados

### Exemplo Node.js (ERRADO)
```dockerfile
# DO NOT DO THIS
FROM node:22-slim

WORKDIR /app
COPY . .
RUN npm ci
RUN npm run build

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "/app/.output/index.mjs"]
```

**Problemas:**
- `node_modules` completo (500MB)
- Dev dependencies instaladas
- Só ~50MB necessário em `.output`

---

## A Solução: Multi-Stage Builds

### Go - Correto
```dockerfile
# Build stage
FROM golang:1.23 AS builder
WORKDIR /app
COPY . .
RUN go build -o binary

# Runtime stage
FROM scratch
COPY --from=builder /app/binary /binary
CMD ["/binary"]
```

**Resultado:** Imagem mínima com apenas o binário.

### Node.js - Correto
```dockerfile
# Build stage
FROM node:22-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:22-slim
WORKDIR /app
COPY --from=builder /app/.output ./.output
ENV NODE_ENV=production
CMD ["node", ".output/index.mjs"]
```

**Resultado:** Sem dev dependencies na imagem final.

---

## Conceitos-Chave

### Separação de Concerns
- **Build stage:** Compilação, bundling, otimização
- **Runtime stage:** Apenas artefatos necessários

### Benefits
1. **Imagens menores** - Menos storage, faster pulls
2. **Superfície de ataque menor** - Menos CVEs
3. **Build-time isolation** - Dev tools não vazam
4. **Cache efficiency** - Layers separadas

---

## Padrões Comuns

### Distroless para Runtime
```dockerfile
FROM golang:1.23 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o /app/main

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /
CMD ["/main"]
```

### Alpine para Runtime
```dockerfile
FROM node:22-slim AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/main.js"]
```

---

## Boas Práticas

1. **Nomear stages** - `AS builder`, `AS production`
2. **Separar COPY de dependências** - Melhora cache
3. **Usar imagens minimalistas** - Alpine, Distroless, Scratch
4. **Copiar apenas o necessário** - Não copiar node_modules inteiro
5. **Testar em ambos stages** - Build e runtime

## Próximos Passos
- [ ] Revisar Dockerfiles existentes
- [ ] Implementar multi-stage builds
- [ ] Medir redução de tamanho