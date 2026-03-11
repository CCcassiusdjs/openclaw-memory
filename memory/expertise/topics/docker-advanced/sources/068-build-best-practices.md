# Building Best Practices - Docker Docs

**URL:** https://docs.docker.com/build/building/best-practices/
**Lido em:** 2026-03-11
**Categoria:** Multi-stage Builds
**Prioridade:** Alta

---

## Resumo

Guia completo de melhores práticas para construção de imagens Docker.

---

## Use Multi-stage Builds

### Benefícios:
- Reduz tamanho da imagem final
- Separa build de output
- Execução paralela de stages

### Criar Stages Reutilizáveis:
```dockerfile
FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
# ...

FROM builder AS build2
# ...
```

**Benefício:** Docker constrói o stage comum apenas uma vez.

---

## Choose the Right Base Image

### Tipos de Imagens Confiáveis:

| Badge | Descrição |
|-------|-----------|
| **Official Images** | Curadas, documentadas, atualizadas |
| **Verified Publisher** | Mantidas por organizações |
| **Docker-Sponsored OS** | Projetos open source patrocinados |

### Critérios:
- Fonte confiável
- Imagem pequena
- Atualizações regulares
- Minimal base para produção

### Duas Imagens:
- **Build:** Com compiladores, ferramentas, debug
- **Production:** Slim, sem ferramentas desnecessárias

---

## Rebuild Images Often

### --pull:
```bash
docker build --pull -t my-image:my-tag .
```

Força busca da última versão da base image.

### --no-cache:
```bash
docker build --no-cache -t my-image:my-tag .
```

Rebuild todos os layers do zero.

### Combinado:
```bash
docker build --pull --no-cache -t my-image:my-tag .
```

Build completamente novo com base image atualizada.

---

## Exclude with .dockerignore

```plaintext
# Ignorar arquivos markdown
*.md

# Ignorar diretórios
node_modules/
.git/

# Ignorar arquivos específicos
.env
*.log
```

---

## Create Ephemeral Containers

### Conceito:
- Container pode ser parado, destruído, recriado
- Mínimo setup e configuração
- Stateless

### Twelve-Factor App:
- Processes: stateless, share-nothing

---

## Don't Install Unnecessary Packages

- Complexidade reduzida
- Dependências reduzidas
- File sizes reduzidos
- Build times reduzidos

---

## Decouple Applications

- Um container = um concern
- Facilita scaling horizontal
- Facilita reuso

### Exemplo:
- Web app container
- Database container
- Cache container (Redis)

---

## Sort Multi-line Arguments

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```

### Benefícios:
- Evita duplicação
- Fácil manutenção
- PRs mais fáceis de ler

---

## Leverage Build Cache

Docker cacheia layers por padrão. Entender cache invalidation é crítico para builds rápidos.

---

## Pin Base Image Versions

### Tag (mutável):
```dockerfile
FROM alpine:3.21
```

### Digest (imutável):
```dockerfile
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

**Trade-off:**
- Tag: automático updates, mas sem audit trail
- Digest: garantia de imutabilidade, mas update manual

---

## Dockerfile Instructions

### FROM:
```dockerfile
# Preferir imagens oficiais e minimal
FROM alpine:3.21
```

### LABEL:
```dockerfile
LABEL com.example.version="0.0.1-beta"
LABEL vendor="ACME Inc"
LABEL com.example.release-date="2025-01-15"
```

### RUN:

**apt-get:**
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    && rm -rf /var/lib/apt/lists/*
```

**Cache busting:**
```dockerfile
# Update e install juntos
RUN apt-get update && apt-get install -y package
```

**Version pinning:**
```dockerfile
RUN apt-get install -y package=1.3.*
```

**Pipes:**
```dockerfile
# Falha se qualquer comando falhar
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

### CMD:
```dockerfile
# Exec form (preferido)
CMD ["executable", "param1", "param2"]

# Shell form
CMD executable param1 param2
```

### EXPOSE:
```dockerfile
# Porta tradicional
EXPOSE 80
EXPOSE 27017
```

### ENV:
```dockerfile
ENV PATH=/usr/local/bin:$PATH
ENV VERSION=1.0.0
```

**Cuidado:** ENV cria layers. Para esconder valor:
```dockerfile
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
```

### ADD vs COPY:

| Instrução | Uso |
|-----------|-----|
| **COPY** | Copiar arquivos do contexto ou stage |
| **ADD** | URLs remotas, extração de tar |

```dockerfile
# COPY preferido para arquivos locais
COPY --from=build /app/dist /usr/share/nginx/html

# ADD para URLs e tar
ADD https://example.com/file.tar.gz /tmp/
ADD archive.tar.gz /app/
```

### ENTRYPOINT:
```dockerfile
ENTRYPOINT ["s3cmd"]
CMD ["--help"]
```

**Uso:**
```bash
docker run s3cmd              # Mostra help
docker run s3cmd ls s3://bucket  # Executa ls
```

### VOLUME:
```dockerfile
VOLUME ["/data"]
```

Para database storage, config, arquivos mutáveis.

### USER:
```dockerfile
RUN groupadd -r app && useradd -r -g app app
USER app
```

**Benefício:** Segurança (não rodar como root)

### WORKDIR:
```dockerfile
WORKDIR /app
```

**Sempre usar caminhos absolutos.**

### ONBUILD:
```dockerfile
ONBUILD COPY . /app
ONBUILD RUN npm install
```

Executa em imagens filhas `FROM` esta imagem.

---

## Best Practices Summary

| Prática | Benefício |
|---------|-----------|
| **Multi-stage builds** | Imagens menores |
| **Base image confiável** | Segurança |
| **Rebuild frequentemente** | Updates de segurança |
| **.dockerignore** | Build context menor |
| **Ephemeral containers** | Stateless, escalável |
| **Não instalar extras** | Menor superfície de ataque |
| **Decouple applications** | Escalabilidade |
| **Sort arguments** | Manutenibilidade |
| **Build cache** | Builds mais rápidos |
| **Pin versions** | Reprodutibilidade |
| **CI/CD** | Automação |