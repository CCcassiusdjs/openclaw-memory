# Multi-stage Builds - Docker Docs

**URL:** https://docs.docker.com/build/building/multi-stage/
**Lido em:** 2026-03-11
**Categoria:** Multi-stage Builds
**Prioridade:** Alta

---

## Resumo

Documentação completa sobre multi-stage builds para otimização de imagens Docker.

---

## O que são Multi-stage Builds

Permitem usar múltiplos `FROM` statements no Dockerfile:
- Cada `FROM` inicia um novo stage
- Cada stage pode usar base diferente
- Artefatos podem ser copiados entre stages
- Resultado: imagem final menor

---

## Sintaxe Básica

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25
WORKDIR /src
COPY main.go ./
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]
```

### Resultado:
- Imagem final contém apenas o binário
- Go SDK e artefatos intermediários ficam no primeiro stage
- Não são salvos na imagem final

---

## Nomear Stages

### Por Número (Default):
```dockerfile
COPY --from=0 /bin/hello /bin/hello
```

### Por Nome:
```dockerfile
FROM golang:1.25 AS build
WORKDIR /src
COPY main.go ./
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

**Benefício:** Se reordenar instruções, `COPY --from=build` continua funcionando.

---

## Stop at Specific Stage

```bash
# Parar no stage "build"
docker build --target build -t hello .
```

### Casos de Uso:
- Debug de stage específico
- `debug` stage com ferramentas, `production` stage limpo
- `testing` stage com dados de teste, `production` stage com dados reais

---

## External Image as Stage

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

Pode copiar de imagem externa:
- Local image name
- Tag disponível localmente ou em registry
- Tag ID

Docker pulla a imagem automaticamente se necessário.

---

## Previous Stage as New Stage

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

### Benefício:
- Reutiliza stages anteriores
- Evita duplicação de código

---

## BuildKit vs Legacy Builder

### BuildKit:
- Apenas stages que o target depende são processados
- Build paralelo de stages independentes

### Legacy Builder:
- Todos os stages até o target são processados
- Mesmo stages não utilizados

### Exemplo:

```dockerfile
FROM ubuntu AS base
RUN echo "base"

FROM base AS stage1
RUN echo "stage1"

FROM base AS stage2
RUN echo "stage2"
```

**BuildKit:**
```bash
docker build --target stage2 .
# Processa: base + stage2 (stage1 é pulado)
```

**Legacy:**
```bash
docker build --target stage2 .
# Processa: base + stage1 + stage2 (todos)
```

---

## Exemplos Práticos

### Go Application:

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.25 AS build
WORKDIR /src
COPY . .
RUN go build -o /bin/app

FROM scratch
COPY --from=build /bin/app /bin/app
CMD ["/bin/app"]
```

### Node.js Application:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
```

### Python Application:

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12 AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

---

## Key Takeaways

1. **Múltiplos FROM:** Cada um inicia um novo stage
2. **COPY --from:** Copia artefatos de outro stage
3. **AS nome:** Nomear stages para referência
4. **--target:** Parar em stage específico
5. **BuildKit:** Mais eficiente (apenas stages necessários)
6. **Imagens menores:** Apenas o necessário na imagem final