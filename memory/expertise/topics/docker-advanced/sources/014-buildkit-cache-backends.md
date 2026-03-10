# Docker BuildKit Cache Backends

**Fonte:** https://docs.docker.com/build/cache/backends/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## O que são Cache Backends

BuildKit suporta exportar/importar cache de/para localizações externas, essencial para CI/CD.

---

## Backends Disponíveis

| Backend | Descrição | Status |
|---------|-----------|--------|
| **inline** | Cache embutido na imagem | Estável |
| **registry** | Cache em registry separado | Estável |
| **local** | Cache em diretório local | Estável |
| **gha** | GitHub Actions cache | Beta |
| **s3** | AWS S3 bucket | Unreleased |
| **azblob** | Azure Blob Storage | Unreleased |

**Nota:** inline, local, registry, gha requerem containerd image store habilitado.

---

## Sintaxe de Comando

```bash
# Exportar cache
docker buildx build \
  --cache-to type=<backend>,ref=<location>[,options...] \
  --cache-from type=<backend>,ref=<location>[,options...] \
  -t <image> .
```

### Exemplo com Registry
```bash
docker buildx build --push -t registry.example.com/app:latest \
  --cache-to type=registry,ref=registry.example.com/app:cache \
  --cache-from type=registry,ref=registry.example.com/app:cache .
```

---

## Múltiplos Caches

Padrão comum: importar de branch atual + main:
```bash
docker buildx build --push -t registry.example.com/app:latest \
  --cache-to type=registry,ref=registry.example.com/app:cache:feature-branch \
  --cache-from type=registry,ref=registry.example.com/app:cache:feature-branch \
  --cache-from type=registry,ref=registry.example.com/app:cache:main .
```

---

## Opções de Configuração

### Cache Mode
| Modo | Descrição |
|------|-----------|
| `min` (default) | Apenas layers exportadas na imagem final |
| `max` | Todas as layers, incluindo intermediárias |

```bash
--cache-to type=registry,ref=cache-image,mode=max
```

**Trade-off:**
- `min`: Cache menor, import/export mais rápido
- `max`: Mais cache hits, mas maior

### Compressão
```bash
--cache-to type=registry,ref=cache-image,compression=zstd
```

Formatos: gzip (default), zstd (mais rápido)

### OCI Media Types
```bash
--cache-to type=registry,ref=cache-image,oci-mediatypes=true
```

Para registries que suportam OCI:
- Amazon ECR: usar `image-manifest=true`

```bash
--cache-to type=registry,ref=cache-image,oci-mediatypes=true,image-manifest=true
```

---

## Exemplos por Backend

### Inline
```bash
docker buildx build -t registry.example.com/app:latest \
  --cache-to type=inline \
  --push .
```
Cache embutido na própria imagem.

### Registry
```bash
docker buildx build --push -t registry.example.com/app:latest \
  --cache-to type=registry,ref=registry.example.com/app:cache,mode=max \
  --cache-from type=registry,ref=registry.example.com/app:cache .
```

### Local
```bash
docker buildx build -t app:latest \
  --cache-to type=local,dest=./cache \
  --cache-from type=local,src=./cache .
```

### GitHub Actions
```bash
docker buildx build -t app:latest \
  --cache-to type=gha \
  --cache-from type=gha .
```

---

## Boas Práticas

1. **Usar registry cache em CI/CD** - Compartilha entre pipelines
2. **Múltiplos cache-from** - Importar de branch + main
3. **mode=max para builds complexos** - Mais cache hits
4. **Compressão zstd** - Melhor performance
5. **Separar cache por branch** - Evita overwrites

## Próximos Passos
- [ ] Configurar cache backend em CI/CD
- [ ] Testar performance com mode=min vs mode=max
- [ ] Implementar em GitHub Actions