# Multi-stage Builds - Documentação Oficial

**Fonte:** https://docs.docker.com/build/building/multi-stage/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## O que são Multi-stage Builds

Múltiplos `FROM` statements no Dockerfile, cada um iniciando um novo stage. Permite copiar artifacts de um stage para outro, deixando atrás o que não é necessário.

---

## Exemplo Básico

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25
WORKDIR /src
COPY <<EOF ./main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]
```

### Resultado
- Imagem final: apenas o binary
- Go SDK e build tools: não incluídos
- Tamanho: mínimo possível

---

## Nomear Stages

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25 AS build
WORKDIR /src
COPY <<EOF /src/main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

### Benefícios
- Nomes são mais legíveis que números
- Reordenação de instructions não quebra COPY
- Melhor manutenibilidade

---

## Parar em Stage Específico

```bash
# Parar no stage "build"
docker build --target build -t hello .
```

### Casos de Uso
- **Debugging** - Debug stage com símbolos e tools
- **Testing** - Stage com dados de teste
- **Production** - Stage otimizado para produção

---

## Copiar de Imagem Externa

```dockerfile
# Copiar de imagem externa
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

### Benefícios
- Não precisa criar stage intermediário
- Imagem é pulled automaticamente
- Útil para binários estáticos, configs

---

## Herdar de Stage Anterior

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
COPY source1.cpp source.cpp
RUN g++ -o /binary source.cpp

FROM builder AS build2
COPY source2.cpp source.cpp
RUN g++ -o /binary source.cpp
```

### Benefícios
- Código compartilhado em um só lugar
- Stages independentes podem ser construídos em paralelo

---

## BuildKit vs Legacy Builder

### Legacy Builder
- Constrói TODOS os stages até o target
- Inclui stages não usados
- Mais lento para Dockerfiles complexos

### BuildKit
- Constrói apenas stages necessários
- Pula stages não dependentes do target
- Paralelismo automático

### Exemplo

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu AS base
RUN echo "base"

FROM base AS stage1
RUN echo "stage1"

FROM base AS stage2
RUN echo "stage2"
```

#### BuildKit (target: stage2)
```
# Processa apenas: base, stage2
# stage1 é SKIPADO
```

#### Legacy Builder (target: stage2)
```
# Processa: base, stage1, stage2
# stage1 é construído mesmo não sendo usado
```

---

## Sintaxe Completa

### FROM com AS
```dockerfile
FROM <image>[:<tag>] [AS <name>]
```

### COPY com --from
```dockerfile
COPY --from=<stage|image> <src>... <dest>
```

### FROM de stage anterior
```dockerfile
FROM <stage-name> [AS <new-name>]
```

---

## Padrões Comuns

### 1. Build + Runtime
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

### 2. Build + Distroless
```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o /app/main

# Distroless runtime
FROM gcr.io/distroless/static-debian11
COPY --from=builder /app/main /main
CMD ["/main"]
```

### 3. Dev + Test + Prod
```dockerfile
# Base stage
FROM node:20 AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Test stage
FROM base AS test
COPY . .
RUN npm test

# Production stage
FROM base AS production
COPY . .
RUN npm run build
CMD ["node", "dist/main.js"]
```

---

## Conceitos Aprendidos

1. **Cada FROM é um stage novo** - Independente do anterior
2. **COPY --from** - Copia de stage ou imagem externa
3. **AS name** - Nomes para referência e manutenção
4. **BuildKit otimiza** - Pula stages não usados
5. **Target stage** - Para em stage específico para debug/test

---

## Best Practices

1. **Sempre nomear stages** - Legibilidade e manutenção
2. **Usar BuildKit** - Default em Docker moderno
3. **Separar build e runtime** - Imagens finais mínimas
4. **Copiar apenas o necessário** - Não copiar todo o filesystem
5. **Usar imagens externas** - Binários pré-compilados, configs

---

## Comparação: Single-stage vs Multi-stage

| Aspecto | Single-stage | Multi-stage |
|---------|--------------|-------------|
| Tamanho final | Grande | Mínimo |
| Build tools na imagem | Sim | Não |
| Complexidade | Baixa | Média |
| Manutenção | Simples | Modular |
| Segurança | Mais attack surface | Menor attack surface |

---

## Aplicações Práticas

1. **Linguagens compiladas** - Go, Rust, C++ - imagem final mínima
2. **Frontend** - Node build → nginx serve
3. **Dev + Prod** - Mesmo Dockerfile, targets diferentes
4. **Binários estáticos** - Copiar de imagem externa
5. **Secrets** - Build stage com secrets, final stage sem

---

## Referências Cruzadas

- Ver: `005-docker-multi-stage-builds.md`
- Ver: `028-advanced-dockerfiles-buildkit-multistage.md`
- Ver: `003-docker-security-overview.md` (attack surface)
- Relacionado: Distroless images, BuildKit, minimal containers