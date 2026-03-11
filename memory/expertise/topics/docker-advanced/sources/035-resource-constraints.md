# Resource Constraints - Documentação Oficial

**Fonte:** https://docs.docker.com/config/containers/resource_constraints/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Visão Geral

Por default, containers não têm limites de recursos e podem usar todo recurso disponível. Docker permite controlar memory, CPU, e GPU.

---

## Memory Constraints

### Riscos de OOME
- Kernel detecta pouca memória → OOME (Out Of Memory Exception)
- Kernel mata processos para liberar memória
- Qualquer processo pode ser morto, incluindo Docker
- Docker ajusta OOM priority para ser menos provável de ser morto

### Limites de Memória

| Opção | Descrição |
|-------|-----------|
| `-m`, `--memory=` | Limite máximo de memória. Mínimo: 6m |
| `--memory-swap` | Total de memória + swap permitido |
| `--memory-swappiness` | Percentual de páginas anônimas swapáveis (0-100) |
| `--memory-reservation` | Limite soft (ativado em contenção) |
| `--kernel-memory` | Limite de kernel memory. Mínimo: 6m |
| `--oom-kill-disable` | Desabilita OOM killer no container |

### --memory-swap Details

| Configuração | Resultado |
|-------------|-----------|
| `--memory=300m --memory-swap=1g` | 300m RAM + 700m swap |
| `--memory=300m --memory-swap=0` | Ignorado (tratado como unset) |
| `--memory=300m --memory-swap=300m` | **Sem swap** |
| `--memory=300m` (sem swap) | 300m RAM + 300m swap (default: 2x memory) |
| `--memory=300m --memory-swap=-1` | Swap ilimitado |

### Prevenir Swap
```bash
# Mesmo valor = sem swap
docker run -m 300m --memory-swap=300m ubuntu
```

### Soft Limit com Reservation
```bash
# Hard limit: 500m, Soft limit: 200m
docker run -m 500m --memory-reservation=200m ubuntu
```
- Container pode usar até 500m
- Em contenção de memória, kernel tenta reduzir para 200m
- Soft limit não garante limite

### OOM Kill Disable
```bash
# Perigoso: sem limite de memória
docker run --oom-kill-disable ubuntu  # ❌

# Correto: com limite de memória
docker run -m 100m --oom-kill-disable ubuntu  # ✅
```

---

## CPU Constraints

### Opções do CFS Scheduler

| Opção | Descrição |
|-------|-----------|
| `--cpus=<value>` | CPUs que o container pode usar (ex: 1.5) |
| `--cpu-period=<value>` | Período do CFS scheduler (default: 100000μs) |
| `--cpu-quota=<value>` | Quota de CPU por período |
| `--cpuset-cpus` | CPUs específicas (ex: 0-3, 1,3) |
| `--cpu-shares` | Peso relativo (default: 1024) |

### Exemplos

```bash
# Limitar a 0.5 CPU
docker run --cpus=".5" ubuntu

# Equivalente com period/quota
docker run --cpu-period=100000 --cpu-quota=50000 ubuntu

# Usar CPUs específicas (cores 0, 1, 2)
docker run --cpuset-cpus="0-2" ubuntu

# Usar CPUs 1 e 3
docker run --cpuset-cpus="1,3" ubuntu
```

### CPU Shares (Soft Limit)
```bash
# Container A: 1024 shares (default)
# Container B: 512 shares
# Container C: 512 shares

# Resultado quando todos precisam de CPU:
# A: 50%, B: 25%, C: 25%
```
- **Importante**: Só aplica quando há contenção de CPU
- Quando idle, containers podem usar 100% da CPU

---

## Real-Time Scheduler

### Pré-requisitos
1. Kernel com `CONFIG_RT_GROUP_SCHED` habilitado
2. Docker daemon com `--cpu-rt-runtime`

### Opções

| Opção | Descrição |
|-------|-----------|
| `--cap-add=sys_nice` | Permite raise process nice values |
| `--cpu-rt-runtime=<value>` | Microsegundos de runtime RT |
| `--ulimit rtprio=<value>` | Prioridade RT máxima |

### Exemplo
```bash
docker run -it \
    --cpu-rt-runtime=950000 \
    --ulimit rtprio=99 \
    --cap-add=sys_nice \
    debian:jessie
```

---

## GPU Constraints

### NVIDIA GPU

```bash
# Instalar nvidia-container-toolkit
# Expor todas as GPUs
docker run --gpus all ubuntu nvidia-smi

# GPU específica por ID
docker run --gpus device=GPU-3a23c669... ubuntu nvidia-smi

# GPUs específicas por índice
docker run --gpus '"device=0,2"' ubuntu nvidia-smi

# Com capabilities
docker run --gpus 'all,capabilities=utility' ubuntu nvidia-smi
```

### Capabilities
- `utility`: Adiciona `nvidia-smi`
- `compute`: CUDA support
- `video`: Video decoding/encoding

---

## Block IO Constraints

| Opção | Descrição |
|-------|-----------|
| `--blkio-weight` | Peso IO (10-1000, default: 500) |
| `--blkio-weight-device` | Peso por dispositivo |
| `--device-read-bps` | Limite leitura (bytes/s) |
| `--device-write-bps` | Limite escrita (bytes/s) |
| `--device-read-iops` | Limite leitura (IO/s) |
| `--device-write-iops` | Limite escrita (IO/s) |

### Exemplos
```bash
# Peso de IO
docker run --blkio-weight 300 ubuntu
docker run --blkio-weight-device "/dev/sda:200" ubuntu

# Limite de taxa
docker run --device-read-bps /dev/sda:1mb ubuntu
docker run --device-write-bps /dev/sda:1mb ubuntu
docker run --device-read-iops /dev/sda:1000 ubuntu
```

---

## Conceitos Aprendidos

1. **OOME é perigoso** - Kernel pode matar Docker ou processos críticos
2. **Hard vs Soft limits** - Memory reservation é soft, --memory é hard
3. **CPU shares são relativos** - Só aplicam em contenção
4. **--cpus é mais simples** - Combina period e quota
5. **GPU requer toolkit** - nvidia-container-toolkit para NVIDIA

---

## Best Practices

1. **Sempre setar --memory** - Evita OOME
2. **Não desabilitar OOM killer sem limite** - Perigoso
3. **Usar soft limits para burst** - Reservation permite picos
4. **Testar requisitos** - Antes de produção, medir uso real
5. **Usar volumes para write-heavy** - Container layer tem overhead

---

## Aplicações Práticas

1. **Multi-tenant** - Limites por container
2. **CI/CD** - Resource limits para builds
3. **Development** - Containers não competem com host
4. **Production** - Resource isolation garantido
5. **GPU workloads** - ML/AI com resource constraints

---

## Referências Cruzadas

- Ver: `006-docker-resource-limits.md`
- Ver: `037-container-isolation.md`
- Relacionado: cgroups, Linux namespaces