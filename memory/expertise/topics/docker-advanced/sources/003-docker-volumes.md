# Docker Volumes - Deep Dive

**Fonte:** https://docs.docker.com/engine/storage/volumes/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. O que são Volumes
- Armazenamento persistente gerenciado pelo Docker
- Criados explicitamente (`docker volume create`) ou automaticamente
- Armazenados em diretório no host (`/var/lib/docker/volumes/`)
- Isolados do funcionamento do host

### 2. Quando Usar Volumes

✅ **Use volumes quando:**
- Backup/migração é necessário
- Gerenciamento via Docker CLI/API
- Containers Linux e Windows
- Compartilhamento entre múltiplos containers
- Pre-popular dados em novo volume
- Alta performance I/O

❌ **Não use volumes quando:**
- Precisa acessar arquivos do host diretamente → use bind mounts

### 3. Performance
- Volumes > bind mounts > writable layer
- Razão: volumes escrevem direto no filesystem do host
- Writable layer precisa de storage driver (abstração adicional)

### 4. Lifecycle do Volume
- Conteúdo persiste após container destruído
- Um volume pode ser montado em múltiplos containers
- Volumes não são removidos automaticamente
- `docker volume prune` remove volumes não utilizados

### 5. Named vs Anonymous Volumes

| Tipo | Nome | Persistência | Comportamento |
|------|------|--------------|---------------|
| **Named** | Especificado pelo usuário | Persiste | Reutilizável |
| **Anonymous** | Gerado automaticamente (único) | Persiste* | Removido com `--rm` |

*Anonymous volumes com `--rm` são destruídos com o container.

### 6. Mounting Behavior

**Volume não-vazio em diretório com dados:**
- Arquivos existentes são obscurecidos (como mount de USB)
- Não há como remover mount para revelar arquivos obscurecidos
- Solução: recriar container sem o mount

**Volume vazio em diretório com dados:**
- Arquivos são copiados para o volume automaticamente
- Útil para pre-popular dados
- `volume-nocopy` para prevenir cópia

### 7. Syntax: `--mount` vs `-v`

**`--mount` (preferido):**
```bash
docker run --mount type=volume,src=<volume-name>,dst=<mount-path>
```

**`-v` (tradicional):**
```bash
docker run -v <volume-name>:<mount-path>
```

**`--mount` é necessário para:**
- Volume driver options
- Mount volume subdirectory
- Swarm services

### 8. Opções do `--mount`

| Opção | Descrição |
|-------|-----------|
| `source`, `src` | Nome do volume (omitido para anonymous) |
| `destination`, `dst`, `target` | Caminho no container |
| `volume-subpath` | Subdiretório do volume |
| `readonly`, `ro` | Monta como read-only |
| `volume-nocopy` | Não copia dados se volume vazio |
| `volume-opt` | Opções do driver (key-value) |

### 9. Opções do `-v`

| Opção | Descrição |
|-------|-----------|
| `readonly`, `ro` | Read-only |
| `volume-nocopy` | Não copia dados |

### 10. Comandos Principais

```bash
# Criar volume
docker volume create my-vol

# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect my-vol

# Remover volume
docker volume rm my-vol

# Remover volumes não utilizados
docker volume prune
```

### 11. Docker Compose

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
volumes:
  myapp:
```

**Volume externo (criado fora do Compose):**
```yaml
volumes:
  myapp:
    external: true
```

### 12. Services e Volumes
- Cada container de serviço tem seu próprio volume local
- Volume driver `local` não compartilha dados entre containers
- Para compartilhamento: usar volume drivers que suportam shared storage

## Exemplos Práticos

### Criar e Usar Volume
```bash
# Criar volume
docker volume create myvol2

# Usar em container
docker run -d \
  --name devtest \
  --mount source=myvol2,target=/app \
  nginx:latest

# Verificar mount
docker inspect devtest --format '{{json .Mounts}}' | jq
```

### Volume Read-Only
```bash
docker run -d \
  --name=nginxtest \
  --mount source=nginx-vol,destination=/usr/share/nginx/html,ro \
  nginx:latest
```

### Pre-popular Volume
```bash
# Volume é preenchido com conteúdo do /usr/share/nginx/html
docker run -d \
  --name=nginxtest \
  --mount source=nginx-vol,destination=/usr/share/nginx/html \
  nginx:latest
```

## Boas Práticas

1. **Nomear volumes** - Facilita identificação e backup
2. **Usar Docker Compose** - Define volumes como código
3. **Volumes para dados críticos** - Databases, uploads, configs
4. **Backup regular** - `docker run --rm -v myvol:/data -v $(pwd):/backup alpine tar cvf /backup/myvol.tar /data`
5. **Limpar volumes órfãos** - `docker volume prune`
6. **Documentar** - Nome, propósito, aplicação

## Próximos Passos
- [ ] Estudar volume drivers (NFS, cloud storage)
- [ ] Praticar backup/restore de volumes
- [ ] Entender volume subpaths