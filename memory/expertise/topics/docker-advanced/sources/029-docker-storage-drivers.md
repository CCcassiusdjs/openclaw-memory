# Docker Storage Drivers - Documentação Oficial

**Fonte:** https://docs.docker.com/engine/storage/drivers/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Conceitos Fundamentais

### Docker Engine 29.0+
- Usa **containerd image store** por padrão (snapshotters, não storage drivers clássicos)
- Storage drivers ainda relevantes para entender como layers funcionam

### Storage Drivers vs Volumes
| Aspecto | Storage Driver | Volume |
|---------|---------------|--------|
| Persistência | Container deletado = dados perdidos | Sobrevive ao container |
| Performance | Overhead de CoW | Performance nativa |
| Uso | Dados efêmeros | Dados write-intensive |
| Compartilhamento | Não compartilhado | Entre containers |

---

## Images e Layers

### Estrutura de Layers
```dockerfile
FROM ubuntu:22.04        # Layer 1 (read-only)
LABEL org.opencontainers.image.authors="..."
COPY . /app              # Layer 2 (read-only)
RUN make /app            # Layer 3 (read-only)
RUN rm -r $HOME/.cache   # Layer 4 (read-only)
CMD python /app/app.py   # Metadata (não cria layer)
```

### Conceitos Importantes
1. **Cada layer é um conjunto de diferenças** da layer anterior
2. **Remover arquivos cria uma nova layer** (arquivo ainda existe na layer anterior)
3. **Container layer** é a layer read-write no topo
4. **Múltiplos containers** compartilham as mesmas layers read-only

---

## Container e Layers

### Diagrama
```
┌─────────────────────────────────────────────┐
│           Container Layer (RW)              │
├─────────────────────────────────────────────┤
│           Image Layer N (RO)                │
├─────────────────────────────────────────────┤
│           Image Layer N-1 (RO)              │
├─────────────────────────────────────────────┤
│           ...                              │
├─────────────────────────────────────────────┤
│           Image Layer 1 (RO)               │
└─────────────────────────────────────────────┘
```

### Tamanho do Container
- `size`: dados na layer writable
- `virtual size`: size + layers read-only
- Múltiplos containers compartilham layers read-only

---

## Copy-on-Write (CoW)

### Funcionamento
1. **Leitura**: usa arquivo existente na layer inferior
2. **Primeira escrita**: copia arquivo para layer writable
3. **Modificações**: aplicadas na cópia (layer writable)

### Benefícios
- Economia de espaço (layers compartilhadas)
- Inicialização rápida de containers
- Diferenças armazenadas eficientemente

### Custo
- `copy_up` na primeira modificação
- Overhead depende do storage driver
- Arquivos grandes = maior custo

---

## Sharing Promotes Smaller Images

### Exemplo Prático
```bash
# Imagem base
docker build -t acme/my-base-image:1.0 -f Dockerfile.base .
# Resultado: 7.75MB

# Imagem derivada
docker build -t acme/my-final-image:1.0 -f Dockerfile .
# Resultado: 7.75MB (mesmo tamanho, layers compartilhadas!)
```

### Verificar Layers Compartilhadas
```bash
# Ver layers de cada imagem
docker image inspect --format "{{json .RootFS.Layers}}" acme/my-base-image:1.0
docker image inspect --format "{{json .RootFS.Layers}}" acme/my-final-image:1.0
# Primeiras 2 layers são idênticas (compartilhadas)
```

---

## Container Size on Disk

### Tamanhos Reais
```bash
# 5 containers rodando
docker ps --size --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Size}}"

# Containers sem escrita
SIZE: 0B (virtual 7.75MB)

# Após escrita de 5 bytes
SIZE: 5B (virtual 7.75MB)
```

### Custo Adicional Não Visível
- Logs do logging-driver
- Volumes e bind mounts
- Configurações do container
- Swap (se habilitado)
- Checkpoints (experimental)

---

## Storage Drivers Disponíveis

| Driver | CoW | Performance | Uso Recomendado |
|--------|-----|-------------|-----------------|
| overlay2 | Sim | Alta | Default, mais usado |
| btrfs | Sim | Média | Btrfs filesystem |
| zfs | Sim | Média | ZFS filesystem |
| vfs | Não | Baixa | Debugging apenas |
| devmapper | Sim | Média | Legacy |

---

## Conceitos Aprendidos

1. **Layers são imutáveis** - Apenas a container layer é writable
2. **CoW economiza espaço** - Arquivos copiados apenas na primeira escrita
3. **Virtual size ≠ disk usage** - Layers são compartilhadas
4. **Metadata não cria layer** - CMD, LABEL, ENV não adicionam layers
5. **Write-heavy = use volumes** - Storage driver tem overhead

---

## Best Practices

1. **Use volumes para dados persistentes** - Banco de dados, logs, uploads
2. **Minimize layers** - Combinar RUN commands quando possível
3. **Use multi-stage builds** - Separar build de runtime
4. **Evite write-intensive** - No container layer
5. **Monitore tamanho** - `docker ps -s`, `docker system df`

---

## Containerd Image Store (Docker 29.0+)

- Usa **snapshotters** em vez de storage drivers
- overlayfs, native, stargz são snapshotters
- Mais eficiente para pull/push
- Backward compatible

---

## Referências Cruzadas

- Ver: `002-docker-volumes.md`
- Ver: `003-docker-storage-overview.md`
- Ver: `030-btrfs-storage-driver.md`
- Ver: `031-zfs-storage-driver.md`
- Relacionado: overlay2, devicemapper, vfs