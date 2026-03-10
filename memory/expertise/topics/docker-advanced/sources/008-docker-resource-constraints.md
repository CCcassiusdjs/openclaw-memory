# Docker Resource Constraints

**Fonte:** https://docs.docker.com/engine/containers/resource_constraints/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Default Behavior
- Containers não têm limites de recursos por default
- Podem usar todo recurso disponível no host
- Kernel scheduler gerencia alocação

### 2. Riscos de Memória Ilimitada
- **OOME (Out Of Memory Exception)** - Kernel mata processos
- Docker daemon tem prioridade ajustada (menos chance de ser morto)
- Containers têm prioridade normal (mais chance de ser mortos)

---

## Memory Constraints

### Tipos de Limites
| Tipo | Descrição |
|------|-----------|
| **Hard limit** | Container não pode usar mais que X |
| **Soft limit** | Container pode usar mais, mas kernel pode reclamar |

### Opções de Memória

| Flag | Descrição |
|------|-----------|
| `-m`, `--memory=` | Máximo de memória (mínimo: 6m) |
| `--memory-swap` | Total de memória + swap |
| `--memory-swappiness` | Porcentagem de swap (0-100) |
| `--memory-reservation` | Soft limit (ativado em contenção) |
| `--kernel-memory` | Limite de kernel memory (deprecated) |
| `--oom-kill-disable` | Desabilita OOM killer (PERIGOSO) |

### --memory-swap Comportamentos

| Valor | Comportamento |
|-------|---------------|
| Não definido | swap = memory (2x total) |
| Igual a memory | **Sem swap** (recomendado para produção) |
| Valor maior | swap = valor - memory |
| `-1` | Swap ilimitado |

### Exemplos

```bash
# Limite de 512MB, sem swap
docker run -m 512m --memory-swap 512m nginx

# Limite de 1GB, com 500MB de swap
docker run -m 1g --memory-swap 1.5g nginx

# Soft limit de 256MB, hard limit de 512MB
docker run -m 512m --memory-reservation 256m nginx
```

---

## CPU Constraints

### CFS Scheduler (Default)

| Flag | Descrição |
|------|-----------|
| `--cpus=<value>` | CPUs disponíveis (ex: 1.5) |
| `--cpu-period` | Período CFS (default: 100000µs) |
| `--cpu-quota` | Quota por período |
| `--cpu-shares` | Peso relativo (default: 1024) |
| `--cpuset-cpus` | CPUs específicas (ex: 0-3, 0,1) |

### Exemplos

```bash
# Limitar a 1.5 CPUs
docker run --cpus=1.5 nginx

# Limitar a CPUs 0 e 1
docker run --cpuset-cpus=0,1 nginx

# Dar prioridade 2x (relativo)
docker run --cpu-shares=2048 nginx

# Equivalente a --cpus=1.5
docker run --cpu-period=100000 --cpu-quota=150000 nginx
```

### Real-Time Scheduler

| Flag | Descrição |
|------|-----------|
| `--cpu-rt-runtime` | Tempo real-time por período |
| `--cpu-rt-period` | Período real-time |

---

## GPU Constraints

```bash
# Usar GPU específica
docker run --gpus device=0 nvidia/cuda

# Usar todas as GPUs
docker run --gpus all nvidia/cuda

# Limitar capacidades GPU
docker run --gpus 'capabilities=compute,utility' nvidia/cuda
```

---

## Outros Recursos

### PIDs
```bash
# Limitar número de processos
docker run --pids-limit 100 nginx
```

### Ulimits
```bash
# Limitar file descriptors
docker run --ulimit nofile=1024:2048 nginx

# Limitar processos de usuário
docker run --ulimit nproc=100 nginx
```

---

## Mitigação de OOME

1. **Testar requisitos de memória** antes de produção
2. **Rodar em hosts adequados** (recursos suficientes)
3. **Limitar memória** em todos containers
4. **Configurar swap** (buffer contra OOM)
5. **Usar service constraints** em Swarm
6. **Monitorar uso** e alertar

---

## Boas Práticas

1. **Sempre limitar memória** em produção
2. **Definir swap limits** (igual a memory = sem swap)
3. **Usar CPU shares** para prioridade relativa
4. **Monitorar recursos** com `docker stats`
5. **Testar antes de produção** para entender requisitos
6. **Não desabilitar OOM killer** sem memória definida

## Próximos Passos
- [ ] Estudar cgroups em detalhes
- [ ] Configurar monitoring de recursos
- [ ] Praticar com diferentes workloads