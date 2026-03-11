# Select a Storage Driver - Documentação Oficial

**Fonte:** https://docs.docker.com/engine/storage/drivers/select-storage-driver/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Docker Engine 29.0+

- **containerd image store** é o default para instalações novas
- Storage drivers clássicos ainda relevantes para entender layers
- Migração possível via documentação do containerd image store

---

## Storage Backends Disponíveis

| Backend | Descrição |
|---------|-----------|
| **containerd (snapshotters)** | Default Docker 29.0+. Multi-platform images, attestations |
| **overlay2** | Driver clássico. Mais compatível, sem config extra |
| **fuse-overlayfs** | Rootless Docker (kernel < 5.11). Não mais necessário desde 5.11+ |
| **btrfs / zfs** | Snapshots, manutenção extra. Requer filesystem específico |
| **vfs** | Testing/debugging apenas. Performance ruim |

---

## Storage Drivers por Distribuição Linux

| Distribuição | Default | Alternativos |
|-------------|---------|--------------|
| Ubuntu | overlay2 | zfs, vfs |
| Debian | overlay2 | vfs |
| CentOS | overlay2 | zfs, vfs |
| Fedora | overlay2 | zfs, vfs |
| RHEL | overlay2 | vfs |
| SLES 15 | overlay2 | vfs |

**Recomendação geral**: Use `overlay2` para compatibilidade ampla.

---

## Backing Filesystems Suportados

| Storage Driver | Backing Filesystems |
|----------------|---------------------|
| overlay2 | xfs (ftype=1), ext4, btrfs, outros |
| fuse-overlayfs | qualquer filesystem |
| btrfs | btrfs |
| zfs | zfs |
| vfs | qualquer filesystem |

**Nota**: Para overlay2, XFS requer `ftype=1` (default na maioria das distros modernas).

---

## Critérios de Seleção

### 1. Workload Suitability

| Workload | Melhor Driver |
|----------|---------------|
| Geral | overlay2 |
| Write-heavy | btrfs, zfs (ou volumes) |
| PaaS / High-density | zfs (Single Copy ARC) |
| Rootless (kernel < 5.11) | fuse-overlayfs |
| Testing | vfs |

### Características

- **overlay2**: File-level, memory efficient, writable layer pode crescer
- **btrfs/zfs**: Block-level, melhor para write-heavy, requer mais memória
- **zfs**: Single Copy ARC - excelente para containers high-density

### 2. Shared Storage Systems

- SAN, NAS, hardware RAID funcionam com Docker
- Docker não integra diretamente
- Seguir best practices do storage driver sobre o shared storage

### 3. Stability

- **overlay2**: Maior estabilidade, mais amplamente testado
- **btrfs/zfs**: Mais features, mais manutenção
- **vfs**: Debugging apenas, não recomendado para produção

---

## Verificar Storage Driver Atual

```bash
docker info | grep "Storage Driver"

# Output exemplo:
# Storage Driver: overlay2
#  Backing Filesystem: xfs
```

---

## Mudar Storage Driver

⚠️ **Cuidado**: Imagens e containers existentes ficam inacessíveis após mudar o driver.

### Passos
1. Salvar imagens importantes: `docker save -o images.tar image1 image2`
2. Parar Docker: `sudo systemctl stop docker`
3. Configurar novo driver em `/etc/docker/daemon.json`
4. Iniciar Docker: `sudo systemctl start docker`
5. Restaurar imagens se necessário

---

## Prioridade de Seleção Automática

Docker seleciona automaticamente na seguinte ordem (se disponível):
1. overlay2 (se backing filesystem suportado)
2. btrfs (se /var/lib/docker em btrfs)
3. zfs (se /var/lib/docker em zfs)
4. vfs (fallback)

Ver [source code](https://github.com/moby/moby/blob/docker-v29.2.1/daemon/graphdriver/driver_linux.go) para ordem completa.

---

## Docker Desktop

- **Não suporta mudar storage driver** via daemon.json
- Usa containerd image store por default (v4.34+)
- Configuração automática

---

## Docker Rootless

Drivers disponíveis em rootless mode:
- overlay2 (kernel 5.11+)
- fuse-overlayfs (kernels mais antigos)

Ver [Rootless mode documentation](/engine/security/rootless/).

---

## Conceitos Aprendidos

1. **containerd image store** - Novo default (Docker 29.0+)
2. **overlay2 é o mais estável** - Melhor para maioria dos casos
3. **Backing filesystem importa** - btrfs/zfs requerem filesystem específico
4. **Write-heavy = volumes** - Sempre preferir volumes ao container layer
5. **zfs para PaaS** - Single Copy ARC eficiente para containers

---

## Recomendações por Cenário

| Cenário | Recomendação |
|---------|-------------|
| Desenvolvimento geral | overlay2 |
| Produção estável | overlay2 |
| Write-heavy workload | btrfs/zfs + volumes |
| PaaS / High-density | zfs (se experiente) |
| Rootless Docker | overlay2 (kernel 5.11+) |
| Debugging | vfs |

---

## Aplicações Práticas

1. **Escolha simples** - Use overlay2 a menos que tenha motivo específico
2. **Write-heavy** - Use volumes, não storage driver
3. **High-density** - Considere zfs se experiência existir
4. **Verificação** - Sempre rodar `docker info` após mudança

---

## Referências Cruzadas

- Ver: `029-docker-storage-drivers.md`
- Ver: `030-btrfs-storage-driver.md`
- Ver: `031-zfs-storage-driver.md`
- Ver: `002-docker-volumes.md`
- Relacionado: containerd image store, snapshotters