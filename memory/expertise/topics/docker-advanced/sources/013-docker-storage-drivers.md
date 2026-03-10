# Docker Storage Drivers

**Fonte:** https://docs.docker.com/engine/storage/drivers/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Storage Drivers vs Volumes
- **Storage Drivers:** Gerenciam image layers e writable layer do container
- **Volumes:** Persistem dados além do ciclo de vida do container

**Nota:** Docker Engine 29.0+ usa containerd image store por default (snapshotters, não storage drivers clássicos).

### 2. Images e Layers
Cada instrução no Dockerfile = uma layer:
```dockerfile
FROM ubuntu:22.04      # Layer 1 (base)
COPY . /app            # Layer 2
RUN make /app          # Layer 3
RUN rm -r $HOME/.cache # Layer 4 (remover também cria layer!)
CMD python /app/app.py # Metadata only
```

**Importante:** Remover arquivos NÃO reduz tamanho da imagem - arquivo ainda existe na layer anterior.

### 3. Container Layer
- Top layer = writable (container layer)
- Todas as layers abaixo = read-only
- Mudanças escritas apenas na container layer
- Container layer deletada quando container removido

### 4. Copy-on-Write (CoW)
Quando container precisa modificar arquivo:
1. Arquivo copiado da read-only layer para container layer
2. Modificação feita na cópia
3. Original permanece inalterado nas read-only layers

**Benefícios:**
- I/O mínimo
- Layers menores
- Eficiência de espaço

### 5. Tamanho do Container no Disco
```bash
docker ps -s
```

| Coluna | Significado |
|--------|-------------|
| `size` | Tamanho da writable layer |
| `virtual size` | size + read-only image data |

**Nota:** Containers da mesma imagem compartilham read-only layers.

### 6. Storage Drivers Disponíveis
| Driver | Filesystem | Recomendado Para |
|--------|------------|------------------|
| overlay2 | overlayFS | Linux moderno (default) |
| devicemapper | LVM | Legado |
| btrfs | btrfs | btrfs systems |
| zfs | zfs | Solaris/Nexenta |
| vfs | virtual | Debugging (sem CoW) |

### 7. containerd Image Store (Docker 29.0+)
- Novo default para instalações fresh
- Usa **snapshotters** ao invés de storage drivers
- Mais eficiente e moderno
- Ver documentação de containerd para detalhes

---

## Comparação Visual

```
┌─────────────────────────────────────────────┐
│           CONTAINER FILESYSTEM              │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │     Container Layer (writable)      │ ← Mudanças aqui
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │ Layer 4: RUN rm -r $HOME/.cache     │ ← Read-only
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │ Layer 3: RUN make /app              │ ← Read-only
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │ Layer 2: COPY . /app                │ ← Read-only
│  └─────────────────────────────────────┘    │
│  ┌─────────────────────────────────────┐    │
│  │ Layer 1: FROM ubuntu:22.04          │ ← Base image
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## Boas Práticas

1. **Usar volumes para dados write-intensive** - Databases, logs, uploads
2. **Multi-stage builds** - Reduz número de layers
3. **Ordenar instruções** - Mais estáveis primeiro
4. **Limpar cache em builds** - `--no-cache` quando necessário
5. **Usar overlay2** - Driver mais eficiente (default)

## Próximos Passos
- [ ] Estudar containerd image store
- [ ] Entender snapshotters
- [ ] Comparar performance entre drivers