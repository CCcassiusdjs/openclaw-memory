# Advanced Dockerfiles - BuildKit e Multi-stage Builds

**Fonte:** https://www.docker.com/blog/advanced-dockerfiles-faster-builds-and-smaller-images-using-buildkit-and-multistage-builds/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## BuildKit Benefits

- Default no Docker Engine desde 23.0
- Pula stages não utilizados
- Constrói stages em paralelo quando possível
- Cache mais inteligente

---

## Pattern 1: Herdar de Stage

```dockerfile
FROM ubuntu AS base
RUN apt-get update && apt-get install git

FROM base AS src1
RUN git clone …

FROM base AS src2
RUN git clone …
```

### Benefícios
- Código compartilhado em um só lugar
- Stages filhas independentes
- Cache não invalidado entre irmãs
- BuildKit constrói src1 e src2 em paralelo

---

## Pattern 2: Copiar de Imagem Diretamente

```dockerfile
FROM alpine
COPY --from=linuxkit/ca-certificates / /
```

- Usa `--from=image` para copiar de imagem externa
- Não precisa de stage intermediário
- Útil para utilitários estáticos

---

## Pattern 3: Alias para Imagem Comum

```dockerfile
FROM alpine:3.6 AS alpine

FROM alpine
RUN …

FROM alpine
RUN …
```

### Com Build Arg
```dockerfile
ARG ALPINE_VERSION=3.6
FROM alpine:${ALPINE_VERSION} AS alpine

FROM alpine
RUN …
```

### Benefícios
- Uma mudança atualiza todas as referências
- Versionamento centralizado
- Override via `--build-arg`

---

## Pattern 4: Build Args em --from

### NÃO funciona:
```dockerfile
ARG src=stage0
COPY --from=build-${src} . .  # INVÁLIDO
```

### Solução: Alias Stage
```dockerfile
ARG src=stage0
FROM alpine AS build-stage0
RUN …

FROM build-${src} AS copy-src
FROM alpine
COPY --from=copy-src . .
```

**Por que?** Dependências entre stages devem ser determinadas antes do build.

---

## Pattern 5: Condições com Multi-stage

### Pseudocódigo (não existe):
```dockerfile
IF $BUILD_VERSION==1
RUN touch version1
ELSE
RUN touch version2
```

### Implementação Multi-stage:
```dockerfile
ARG BUILD_VERSION=1

FROM alpine AS base
RUN …

FROM base AS branch-version-1
RUN touch version1

FROM base AS branch-version-2
RUN touch version2

FROM branch-version-${BUILD_VERSION} AS after-condition

FROM after-condition
RUN …
```

**BuildKit:** Pula branches não utilizados
**Legacy Builder:** Constrói todos mas descarta

---

## Pattern 6: Dev/Test Helper para Produção Mínima

```dockerfile
FROM golang:alpine AS stage0
…

FROM scratch AS release
COPY --from=stage0 /binary0 /bin
COPY --from=stage1 /binary1 /bin

# Development environment
FROM golang:alpine AS dev-env
COPY --from=release / /
ENTRYPOINT ["ash"]

# Test stage
FROM golang:alpine AS test
COPY --from=release / /
RUN go test …

# Default: production
FROM release
```

### Uso
```bash
# Produção (default)
docker build .

# Desenvolvimento
docker build --target=dev-env .

# Testes
docker build --target=test .
```

### Benefícios
- Garante que dev e test usam MESMO binary de produção
- Não precisa duplicar COPY statements
- Mantém produção minimalista (scratch)
- Debug/dev têm shell e ferramentas

---

## Conceitos Aprendidos

1. **Stage Inheritance** - `FROM stagename` para compartilhar código
2. **Direct Image Copy** - `--from=image` sem stage
3. **Alias Pattern** - Centralizar versão de imagem
4. **Branch Pattern** - Condições via multi-stage
5. **Target Pattern** - Dev/test sem duplicar produção

---

## Best Practices

1. **Use BuildKit** - Paralelismo e skip de stages
2. **Defina ARGs antes de FROM** - Antes do primeiro stage
3. **Alias para versões** - Uma mudança atualiza tudo
4. **Stage para condições** - Multi-stage como IF/ELSE
5. **COPY from release** - Testar o que vai para produção

---

## Comparação: Legacy vs BuildKit

| Aspecto | Legacy Builder | BuildKit |
|---------|---------------|----------|
| Stages não usados | Constrói todos | Pula |
| Paralelismo | Sequencial | Paralelo |
| Cache | Por layer | Smarter |
| Condições | Constrói todas branches | Pula não usadas |

---

## Aplicações Práticas

1. **CI/CD** - Build paralelo e cache eficiente
2. **Multi-ambiente** - Dev/staging/prod do mesmo Dockerfile
3. **Testes** - Testar exatamente o que vai para produção
4. **Versionamento** - Centralizar versão de base image
5. **Condicional Builds** - Features diferentes por build arg

---

## Referências Cruzadas

- Ver: `005-docker-multi-stage-builds.md`
- Ver: `007-docker-build-cache.md`
- Ver: `023-buildkit-deep-dive.md`
- Relacionado: BuildKit frontend, Dockerfile experimental features