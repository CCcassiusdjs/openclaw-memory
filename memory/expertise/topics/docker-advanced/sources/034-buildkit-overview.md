# BuildKit Overview - Documentação Oficial

**Fonte:** https://docs.docker.com/build/buildkit/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## O que é BuildKit

Backend melhorado para substituir o legacy builder. Default no Docker Desktop e Docker Engine v23.0+.

---

## Funcionalidades Principais

| Feature | Descrição |
|---------|-----------|
| **Detect unused stages** | Pula stages não usados automaticamente |
| **Parallel building** | Constrói stages independentes em paralelo |
| **Incremental context** | Transfere apenas arquivos modificados |
| **Skip unused files** | Detecta e ignora arquivos não usados |
| **Dockerfile frontends** | Múltiplas implementações de frontends |
| **Clean API** | Sem side effects (intermediate images/containers) |
| **Cache prioritization** | Cache inteligente para pruning automático |

---

## LLB (Low-Level Build)

### Definição
Formato binário intermediário que permite extensões do BuildKit. Define um **grafo de dependências content-addressable**.

### Características
- Content-addressable dependency graph
- Tracking de checksums de build graphs
- Cache pode ser exportado para registry
- Pull on-demand por qualquer host

### Diagrama
```
┌─────────────────────────────────────────────────────┐
│                  LLB Definition                      │
│         (Content-Addressable Graph)                  │
├─────────────────────────────────────────────────────┤
│    ┌───────┐    ┌───────┐    ┌───────┐             │
│    │ Exec  │───▶│ Exec  │───▶│ Exec  │             │
│    │ Op A  │    │ Op B  │    │ Op C  │             │
│    └───────┘    └───────┘    └───────┘             │
│         │            │            │                  │
│         ▼            ▼            ▼                  │
│    ┌───────┐    ┌───────┐    ┌───────┐             │
│    │ Cache │    │ Cache │    │ Cache │             │
│    │  A    │    │  B    │    │  C    │             │
│    └───────┘    └───────┘    └───────┘             │
└─────────────────────────────────────────────────────┘
```

### Geração
- **Dockerfile**: Frontend converte para LLB
- **Go client**: `github.com/moby/buildkit/client/llb` - Define operações em Go

---

## Frontend

Componente que converte formato humano para LLB. Pode ser distribuído como **imagem**.

### Exemplo: Dockerfile Frontend
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "hello"
```

A directive `# syntax=` especifica qual frontend usar.

### Benefícios
- Versionamento de frontend
- Features garantidas para um formato
- Extensibilidade

---

## Habilitando BuildKit

### Docker Desktop
- Default habilitado
- Nenhuma configuração necessária

### Docker Engine < 23.0
```bash
# Environment variable
DOCKER_BUILDKIT=1 docker build .

# Ou daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

### Docker Buildx
- Sempre usa BuildKit
- Nenhuma configuração adicional

---

## BuildKit vs Legacy Builder

| Aspecto | Legacy Builder | BuildKit |
|---------|----------------|----------|
| Unused stages | Constrói todos | Pula automaticamente |
| Paralelismo | Sequencial | Paralelo automático |
| Context transfer | Completo | Incremental |
| Cache | Image-based | Content-addressable |
| Portability | Local apenas | Cache em registry |
| Extensibility | Limitada | Frontends, LLB |

---

## Exemplo: Dockerfile com BuildKit

### Legacy Builder
```
Processa: base, stage1, stage2 (todos)
Tempo: soma de todos os stages
```

### BuildKit
```
Target: stage2
Processa: base, stage2 (stage1 é SKIPADO)
Tempo: apenas stages necessários
```

---

## BuildKit on Windows

### Status
- **Linux containers**: Full support
- **Windows containers**: Experimental (v0.13+)

### Limitations
- Windows Server 2019, 2022, Windows 11
- Base images: ServerCore, NanoServer
- Ver [GitHub issues](https://github.com/moby/buildkit/issues?q=is%3Aissue%20state%3Aopen%20label%3Aarea%2Fwindows-wcow)

### Setup Windows
1. Enable Hyper-V and Containers features
2. Switch to Windows containers in Docker Desktop
3. Install containerd 1.7.7+
4. Download BuildKit release
5. Start `buildkitd.exe`
6. Create remote builder: `docker buildx create --name buildkit-exp --use --driver=remote npipe:////./pipe/buildkitd`

---

## Benefícios de Performance

1. **Parallel execution** - Stages independentes em paralelo
2. **Incremental context** - Apenas arquivos modificados
3. **Smart cache** - Checksums precisos, não heurísticas
4. **Registry cache** - Cache pode ser push/pull de registry
5. **Skip unused** - Stages não usados não são construídos

---

## Cache Export/Import

### Exportar Cache
```bash
docker buildx build \
  --cache-to type=registry,ref=myregistry/cache \
  -t myapp:latest .
```

### Importar Cache
```bash
docker buildx build \
  --cache-from type=registry,ref=myregistry/cache \
  -t myapp:latest .
```

### Benefícios
- Cache compartilhado entre hosts
- CI/CD mais rápido
- Builds reproduzíveis

---

## Inline Cache

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS base
# ... build steps

# Cache inline nas metadas da imagem
```

```bash
docker buildx build \
  --cache-to type=inline \
  --cache-from type=registry,ref=myapp:latest \
  -t myapp:latest .
```

---

## Conceitos Aprendidos

1. **LLB é o core** - Grafo content-addressable, não heurísticas
2. **Frontends são extensíveis** - Dockerfile é apenas um frontend
3. **Cache é portável** - Export/import para registry
4. **Paralelismo automático** - Stages independentes em paralelo
5. **Windows support é experimental** - Linux containers são full support

---

## Aplicações Práticas

1. **CI/CD** - Cache em registry, builds mais rápidos
2. **Monorepos** - Stages independentes em paralelo
3. **Multi-platform** - Buildx + BuildKit para cross-compilation
4. **Development** - Context incremental, rebuilds rápidos
5. **Custom frontends** - Linguagens alternativas ao Dockerfile

---

## Referências Cruzadas

- Ver: `023-buildkit-deep-dive.md`
- Ver: `028-advanced-dockerfiles-buildkit-multistage.md`
- Ver: `033-multi-stage-builds-docs.md`
- Relacionado: Docker Buildx, LLB, Frontends, Cache management