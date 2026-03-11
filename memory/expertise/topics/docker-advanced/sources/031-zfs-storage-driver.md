# ZFS Storage Driver - Documentação Oficial

**Fonte:** https://docs.docker.com/engine/storage/drivers/zfs-driver/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Aviso Importante

> **Não recomendado para produção** a menos que tenha experiência substancial com ZFS on Linux (ZoL).

**Licensing**: CDDL vs GPL incompatibilidade - não pode ser shipado no kernel mainline.

---

## O que é ZFS

- **Next generation filesystem** criado pela Sun Microsystems
- Features: volume management, snapshots, checksumming, compression, deduplication, replication
- **ZoL (ZFS on Linux)**: Port nativo para Linux (não FUSE)

---

## Objetos ZFS

| Objeto | Descrição |
|--------|-----------|
| **Filesystems** | Thin provisioned, alocados on-demand do zpool |
| **Snapshots** | Read-only, space-efficient, point-in-time copies |
| **Clones** | Read-write copies de snapshots |

### Diagrama de Clone
```
┌─────────────────────────────────────────────────────┐
│                    Clone (RW)                        │
│         Container Layer / Image Layer               │
├─────────────────────────────────────────────────────┤
│                    Snapshot (RO)                     │
│         Point-in-time copy                          │
├─────────────────────────────────────────────────────┤
│                    Filesystem                        │
│         Base layer (ZFS Dataset)                    │
└─────────────────────────────────────────────────────┘
```

---

## Pré-requisitos

1. **Dispositivos dedicados**: Preferencialmente SSDs
2. **/var/lib/docker/ em ZFS filesystem**
3. **ZoL instalado**: Kernel module + userspace tools

---

## Configuração

### Passos
```bash
# 1. Parar Docker
sudo systemctl stop docker

# 2. Backup
sudo cp -au /var/lib/docker /var/lib/docker.bk
sudo rm -rf /var/lib/docker/*

# 3. Criar zpool
sudo zpool create -f zpool-docker -m /var/lib/docker /dev/xvdf /dev/xvdg

# 4. Verificar
sudo zfs list
# NAME           USED  AVAIL  REFER  MOUNTPOINT
# zpool-docker    55K  96.4G    19K  /var/lib/docker

# 5. Configurar daemon.json
{
  "storage-driver": "zfs"
}

# 6. Iniciar Docker
sudo systemctl start docker

# 7. Verificar
docker info | grep "Storage Driver"
```

---

## Gerenciamento

### Aumentar Capacidade
```bash
# Adicionar dispositivo ao pool
sudo zpool add zpool-docker /dev/xvdh
```

### Quota por Container
```json
// /etc/docker/daemon.json
{
  "storage-driver": "zfs",
  "storage-opts": ["size=256M"]
}
```

---

## Como Funciona

### Image e Container Layers

```
┌─────────────────────────────────────────────────────┐
│              Container Layer (Clone)                 │
│         Writable, espaço alocado on-demand           │
├─────────────────────────────────────────────────────┤
│              Layer 1 (Clone)                         │
│         Snapshot + Clone da Layer abaixo             │
├─────────────────────────────────────────────────────┤
│              Base Layer (Filesystem)                 │
│         ZFS Dataset real, thin provisioned           │
└─────────────────────────────────────────────────────┘
```

### Processo de Criação
1. **Base layer**: ZFS filesystem
2. **Layers subsequentes**: Clone de snapshot da layer pai
3. **Container**: Clone de snapshot da última layer
4. **Escrita**: Blocos de 128k alocados on-demand

---

## Operações de Leitura e Escrita

### Leitura
- Clone compartilha dados com o dataset original
- Leitura rápida, mesmo de layers profundas
- Block sharing eficiente

### Escrita de Novos Arquivos
- Espaço alocado on-demand do zpool
- Blocos escritos diretamente na layer writable

### Modificação de Arquivos Existentes
- **Copy-on-Write (CoW)**
- Apenas blocos modificados alocados
- Minimiza tamanho da layer

### Deleção
- Arquivos em layers inferiores: mascarados
- Arquivos criados e deletados: blocos reclaimados pelo zpool

---

## Performance

### Fatores de Impacto

| Fator | Impacto | Recomendação |
|-------|---------|--------------|
| **Memória** | Alto | ZFS foi feito para servidores enterprise |
| **Deduplication** | Muito alto | Desabilitar para Docker |
| **ARC Cache** | Positivo | Single Copy ARC para containers |
| **Fragmentation** | Médio | Block size 128k ajuda |
| **ZFS FUSE** | Negativo | Evitar, usar ZoL nativo |

### Single Copy ARC
- Feature única do ZFS
- Múltiplos containers compartilham um bloco cached
- **Excelente para PaaS** e alta densidade

### ZIL e Delayed Writes
- ZFS Intent Log reduz fragmentação
- Coalescing de writes ajuda performance

---

## Performance Best Practices

1. **Use SSDs** - Leituras/escritas mais rápidas
2. **Use volumes** - Bypass do storage driver para write-heavy
3. **Desabilite deduplication** - Muito overhead de memória
4. **Use ZoL nativo** - Não FUSE
5. **Monitore fragmentação** - `zpool status`

---

## Quando Usar

### Vantagens
- **Single Copy ARC** - Compartilhamento eficiente
- Snapshots eficientes
- Checksumming nativo
- Compression nativa
- RAID nativo (RAID-Z)

### Desvantagens
- Não shipado no kernel (licensing)
- Complexidade de setup
- Requer experiência com ZFS
- Overhead de memória

### Recomendação
- Use **overlay2** se possível
- Use ZFS apenas se:
  - Sistema já usa ZFS root
  - Precisa de Single Copy ARC (PaaS)
  - Experiência prévia com ZFS

---

## Comparação com Btrfs

| Aspecto | ZFS | Btrfs |
|---------|-----|-------|
| Page cache sharing | Sim (ARC) | Não |
| Licença | CDDL (separado) | GPL (mainline) |
| Deduplication | Sim (desabilitar) | Sim |
| RAID nativo | RAID-Z | RAID |
| Estabilidade | Alta | Média |
| Setup | Complexo | Médio |

---

## Comparação com overlay2

| Aspecto | ZFS | overlay2 |
|---------|-----|----------|
| Page cache sharing | Sim | Sim |
| Snapshots | Nativo | Não |
| RAID | Nativo | Não |
| Configuração | Complexa | Simples |
| Memory overhead | Alto | Baixo |
| Performance | Boa | Melhor |

---

## Conceitos Aprendidos

1. **ZFS Objects** - Filesystem, Snapshot, Clone
2. **Single Copy ARC** - Feature única para containers
3. **Block size 128k** - Padrão ZFS para Docker
4. **Zpool** - Pool de armazenamento subjacente
5. **Quota por container** - storage-opts size=M

---

## Aplicações Práticas

1. **PaaS / High-density** - Single Copy ARC eficiente
2. **Data integrity** - Checksumming nativo
3. **Compression** - Redução de espaço transparente
4. **RAID-Z** - RAID nativo sem hardware RAID

---

## Referências Cruzadas

- Ver: `029-docker-storage-drivers.md`
- Ver: `030-btrfs-storage-driver.md`
- Ver: `002-docker-volumes.md`
- Relacionado: overlay2, devicemapper, containerd snapshotters