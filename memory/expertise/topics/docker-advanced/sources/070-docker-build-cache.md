# Docker Build Cache - Docker Docs

**URL:** https://docs.docker.com/build/cache/
**Lido em:** 2026-03-11
**Categoria:** BuildKit
**Prioridade:** Alta

---

## Resumo

Documentação sobre como funciona o cache de build do Docker e como otimizar builds.

---

## Como o Cache Funciona

### Conceito Básico:
- Cada instrução do Dockerfile → um layer
- Layers são empilhados (stack)
- Mudança em um layer invalida layers subsequentes

### Exemplo:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

### Fluxo de Cache:

```
FROM ubuntu:latest        ← Layer base (cached)
RUN apt-get update...     ← Layer cached
COPY main.c Makefile...    ← MUDOU! Cache invalidado
WORKDIR /src/             ← Precisa reexecutar
RUN make build            ← Precisa reexecutar
```

### Invalidation Cascata:
- Layer muda → todos os layers subsequentes são invalidados
- Mesmo se não mudariam nada, precisam reexecutar

---

## Diagrama

### Stack Normal:
```
┌─────────────────────┐
│   RUN make build     │ ← Topo
├─────────────────────┤
│   WORKDIR /src/      │
├─────────────────────┤
│   COPY main.c...     │
├─────────────────────┤
│   RUN apt-get...     │
├─────────────────────┤
│   FROM ubuntu        │ ← Base
└─────────────────────┘
```

### Cache Invalidado:
```
┌─────────────────────┐
│   RUN make build     │ ← INVALIDADO
├─────────────────────┤
│   WORKDIR /src/      │ ← INVALIDADO
├─────────────────────┤
│   COPY main.c...     │ ← MUDOU AQUI
├─────────────────────┤
│   RUN apt-get...     │ ← Cached
├─────────────────────┤
│   FROM ubuntu        │ ← Cached
└─────────────────────┘
```

---

## Otimização

### Ordem das Instruções:
- Instruções que mudam frequentemente → fim do Dockerfile
- Instruções estáveis → início do Dockerfile

### Exemplo Ruim:
```dockerfile
# Muda frequentemente no início
COPY . /app
RUN apt-get update && apt-get install -y deps
RUN build-app
```

### Exemplo Bom:
```dockerfile
# Dependências primeiro (cached)
RUN apt-get update && apt-get install -y deps
# Código depois (muda frequentemente)
COPY . /app
RUN build-app
```

---

## Recursos Relacionados

| Recurso | Descrição |
|---------|-----------|
| [Cache invalidation](/build/cache/invalidation/) | Quando o cache é invalidado |
| [Optimize build cache](/build/cache/optimization/) | Otimização avançada |
| [Garbage collection](/build/cache/garbage-collection/) | Limpeza de cache |
| [Cache storage backends](/build/backends/) | Backends de storage |

---

## Key Takeaways

1. **Layer stack:** Cada instrução é um layer empilhado
2. **Invalidation cascata:** Layer muda → subsequentes invalidados
3. **Ordem importa:** Instruções estáveis primeiro
4. **COPY depois:** Código que muda frequentemente no fim
5. **Cache = Speed:** Entender cache = builds mais rápidos