# How to Limit Docker Memory and CPU Usage - PhoenixNAP

**URL:** https://phoenixnap.com/kb/docker-memory-and-cpu-limit
**Lido em:** 2026-03-11
**Categoria:** Performance
**Prioridade:** Média

---

## Resumo

Guia completo sobre limitação de recursos (CPU e memória) em containers Docker.

---

## Por que Limitar Recursos?

### Problemas sem limites:
- Containers com acesso ilimitado aos recursos do host
- Misbehaving containers podem causar performance bottlenecks
- OOM (Out-of-Memory) events
- Instabilidade do sistema
- Problemas com containers co-located

### Benefícios:
- Performance mais previsível
- Segurança contra resource-based attacks
- Isolamento entre containers
- Better multi-tenancy

---

## Memory Limits

### Hard vs Soft Limits

| Tipo | Comportamento |
|------|---------------|
| **Hard limit** | Container terminado ao exceder |
| **Soft limit** | Warning apenas, permite spikes |

> **Nota:** Docker pode terminar container mesmo com soft limit se sistema low memory.

### Opções de Memória

| Opção | Descrição | Mínimo |
|-------|-----------|--------|
| `--memory`, `-m` | Hard limit de memória física | 6 MB |
| `--memory-swap` | Total (RAM + swap) | Maior que --memory |
| `--memory-swappiness` | % de anonymous page swaps | 0-100 |
| `--memory-reservation` | Soft limit | < hard limit |
| `--kernel-memory` | Hard limit de kernel memory | 6 MB |
| `--oom-kill-disable` | Desabilita OOM kill | - |

### Exemplos de Memória

```bash
# Hard limit de 512 MB
docker run -dit --memory="512m" nginx

# Com swap (512 MB RAM + 512 MB swap = 1 GB total)
docker run -dit --memory="512m" --memory-swap="1g" nginx

# Soft + Hard limit
docker run -dit --memory="1g" --memory-reservation="512m" nginx

# Sem swap (--memory-swap = --memory)
docker run -dit --memory="512m" --memory-swap="512m" nginx
```

### Habilitar Swap Support

Se `docker info` mostrar "WARNING: No swap limit support":

```bash
# 1. Editar grub config
sudo nano /etc/default/grub

# 2. Adicionar:
GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"

# 3. Atualizar grub
sudo update-grub

# 4. Reboot
sudo reboot
```

### Verificar Limits de Memória

```bash
# Ver estatísticas em tempo real
docker stats

# Verificar swap
docker inspect [container] | grep MemorySwap

# Verificar soft limit
docker inspect [container] | grep MemoryReservation
```

---

## CPU Limits

### Opções de CPU

| Opção | Descrição | Default |
|-------|-----------|---------|
| `--cpus` | Número de CPUs (decimal) | - |
| `--cpu-period` | CFS scheduler period (μs) | 100000 |
| `--cpu-quota` | CFS quota per period | - |
| `--cpuset-cpus` | CPUs específicos (0,1,2...) | - |
| `--cpu-shares` | CPU cycles allocation | 1024 |

### Exemplos de CPU

```bash
# Limitar a 1 CPU core
docker run -dit --cpus="1.0" nginx

# Fraction of CPU (0.5 = meia CPU)
docker run -dit --cpus="0.5" nginx

# CPU shares (quando há contenção)
docker run -dit --cpu-shares="2048" nginx

# CPUs específicos (cores 0 e 2)
docker run -dit --cpuset-cpus="0,2" nginx

# Range de CPUs (cores 0-3)
docker run -dit --cpuset-cpus="0-3" nginx
```

### CPU Period e Quota

```bash
# Equivalente a --cpus="1.5"
docker run -dit --cpu-period="100000" --cpu-quota="150000" nginx

# Fórmula: cpus = cpu-quota / cpu-period
# 150000 / 100000 = 1.5 CPUs
```

### Verificar Limits de CPU

```bash
# Ver número de CPUs (em nano CPUs)
docker inspect [container] | grep NanoCpus
# 1000000000 = 1 CPU

# Ver CPU shares
docker inspect [container] | grep CpuShares
```

---

## Docker Compose Resource Limits

```yaml
services:
  app:
    image: nginx
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## Riscos de OOM

### O que acontece:
1. Container excede memória
2. Kernel dispara OOM killer
3. Processos são terminados
4. Container pode morrer

### Prevenir OOM:

```bash
# Desabilitar OOM kill (cuidado!)
docker run --oom-kill-disable nginx

# Melhor: ajustar limits adequadamente
docker run --memory="1g" --memory-reservation="512m" nginx
```

---

## Tabela de Sufixos

| Sufixo | Valor |
|--------|-------|
| `b` | bytes |
| `k` | kilobytes |
| `m` | megabytes |
| `g` | gigabytes |

---

## Best Practices

1. **Sempre setar limits:** Containers sem limits são perigosos
2. **Hard + Soft limits:** Permitir spikes sem matar container
3. **Monitorar:** `docker stats` para verificar consumo real
4. **Testar:** Ajustar limits baseado em uso real da aplicação
5. **Swap sparingly:** Swap é lento, usar com cautela
6. **CPU shares:** Útil para priorização em contenção

---

## Comparação com Resource Constraints Docs

| Aspecto | PhoenixNAP | Docker Docs |
|---------|-----------|-------------|
| Foco | How-to prático | Referência completa |
| Exemplos | Mais básicos | Mais variados |
| Swap config | Detalhado | Não cobre |
| CFS scheduler | Mencionado | Detalhado |

---

## Insights

- **Swap support** requer config do grub (não documentado em todos os lugares)
- **--cpu-shares** é soft limit, só funciona em contenção
- **NanoCpus** = CPUs * 1 bilhão (1 CPU = 1000000000 nano CPUs)
- **Memory reservation** < memory sempre