# BTRFS Storage Driver - Documentação Oficial

**Fonte:** https://docs.docker.com/engine/storage/drivers/btrfs-driver/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Aviso Importante

> **Use `overlay2` na maioria dos casos** - Não é necessário usar btrfs apenas porque o filesystem root é Btrfs.

**Known Issues:** [Moby issue #27653](https://github.com/moby/moby/issues/27653)

---

## O que é Btrfs

- **Copy-on-write filesystem** nativo do Linux kernel
- Suporta: block-level operations, thin provisioning, snapshots, administração fácil
- Múltiplos dispositivos físicos em um único filesystem

---

## Pré-requisitos

1. **Suporte no kernel**: `grep btrfs /proc/filesystems`
2. **Pacote btrfsprogs**: SLES ou btrfs-tools (Ubuntu)
3. **Dispositivo dedicado**: Bloco físico formatado como Btrfs
4. **Mount em /var/lib/docker/**

---

## Configuração

### Passos
```bash
# 1. Parar Docker
sudo systemctl stop docker

# 2. Backup
sudo cp -au /var/lib/docker /var/lib/docker.bk
sudo rm -rf /var/lib/docker/*

# 3. Formatar dispositivos
sudo mkfs.btrfs -f /dev/xvdf /dev/xvdg

# 4. Montar
sudo mount -t btrfs /dev/xvdf /var/lib/docker

# 5. Restaurar
sudo cp -au /var/lib/docker.bk/* /var/lib/docker/

# 6. Configurar daemon.json
{
  "storage-driver": "btrfs"
}

# 7. Iniciar Docker
sudo systemctl start docker

# 8. Verificar
docker info | grep "Storage Driver"
```

### fstab (Persistência)
```
/dev/xvdf /var/lib/docker btrfs defaults 0 0
```

---

## Como Funciona

### Subvolumes e Snapshots

```
/var/lib/docker/btrfs/subvolumes/
├── base-layer/          # Subvolume real
├── layer-1/             # Snapshot do base
├── layer-2/             # Snapshot do layer-1
└── container-xxx/       # Snapshot da última layer
```

### Diagrama
```
┌─────────────────────────────────────────────────────┐
│                    Container                        │
│              (Btrfs Snapshot)                        │
├─────────────────────────────────────────────────────┤
│                    Layer 2                          │
│              (Btrfs Snapshot)                        │
├─────────────────────────────────────────────────────┤
│                    Layer 1                           │
│              (Btrfs Snapshot)                        │
├─────────────────────────────────────────────────────┤
│                    Base Layer                        │
│              (Btrfs Subvolume)                        │
└─────────────────────────────────────────────────────┘
```

### Características
- **Base layer**: Subvolume real
- **Layers subsequentes**: Snapshots (diferenças)
- **Container layer**: Snapshot da última layer
- **Alocação on-demand**: ~1GB chunks

---

## Operações de Leitura e Escrita

### Leitura
- Metadata aponta para blocos de dados no storage pool
- Mesma velocidade que subvolumes
- Não há overhead de copy-on-write

### Escrita de Novos Arquivos
- Alocação on-demand nativa do Btrfs
- Velocidade nativa do filesystem

### Modificação de Arquivos Existentes
- **Redirect-on-write** (terminologia Btrfs)
- Apenas blocos modificados escritos na layer writable
- Metadata atualizada no snapshot
- Overhead menor

### Deleção
- Arquivos em layers inferiores: mascarados (ainda existem)
- Arquivos criados e deletados: espaço reclaimado

---

## Performance

### Page Cache Sharing
- **Não suportado** pelo Btrfs
- Cada processo copia arquivo para memória
- **Problema**: Alta densidade (PaaS)

### Small Writes
- Muitos writes pequenos = fragmentação
- Pode causar "out of space" prematuro
- **Solução**: Monitorar com `btrfs filesystem show`

### Sequential Writes
- Journaling overhead
- **Redução de até 50%** em performance

### Fragmentation
- Natural em CoW filesystems
- CPU spikes em SSDs, head thrashing em HDDs
- **Mitigação**: `autodefrag` (kernel 3.9+)

### SSD Optimizations
```bash
# Mount com SSD optimization
mount -t btrfs -o ssd /dev/xvdf /var/lib/docker
```

---

## Gerenciamento

### Adicionar Dispositivo
```bash
# Com Docker rodando (performance impact)
sudo btrfs device add /dev/svdh /var/lib/docker
sudo btrfs filesystem balance /var/lib/docker

# Recomendado: janela de manutenção
```

### Expandir Automaticamente
- Btrfs expande em chunks de ~1GB
- Automático quando space low

---

## Quando Usar

### Vantagens
- Snapshots eficientes
- Thin provisioning nativo
- Block-level copy-on-write
- RAID nativo (striping, mirroring)
- Compression nativa

### Desvantagens
- Page cache sharing não suportado
- Fragmentação
- Known issues (Moby #27653)
- Complexidade de gerenciamento

### Recomendação
- Use **overlay2** se possível
- Use Btrfs apenas se:
  - Sistema já usa Btrfs root
  - Precisa de snapshots nativos
  - RAID/striping necessário

---

## Comparação com overlay2

| Aspecto | Btrfs | overlay2 |
|---------|-------|----------|
| Page cache sharing | Não | Sim |
| Fragmentação | Sim | Menor |
| Configuração | Complexa | Simples |
| Snapshots | Nativo | Não |
| RAID | Nativo | Não |
| Performance | Boa | Melhor |

---

## Conceitos Aprendidos

1. **Subvolume vs Snapshot** - Base é subvolume, layers são snapshots
2. **Redirect-on-write** - Terminologia Btrfs para CoW
3. **Page cache sharing** - Limitação importante para PaaS
4. **Balance frequente** - Necessário para evitar space issues
5. **Autodefrag** - Mitiga fragmentação em kernels novos

---

## Aplicações Práticas

1. **Development environments** - Snapshots rápidos
2. **RAID/striping** - Combinação de dispositivos
3. **Compression** - Redução de espaço
4. **Backup eficiente** - Snapshots Btrfs

---

## Referências Cruzadas

- Ver: `029-docker-storage-drivers.md`
- Ver: `031-zfs-storage-driver.md`
- Ver: `002-docker-volumes.md`
- Relacionado: overlay2, devicemapper