# Docker Container Top - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/container/top/
**Prioridade:** Baixa
**Lido em:** 2026-03-11

---

## Uso

```bash
docker container top CONTAINER [ps OPTIONS]
docker top CONTAINER [ps OPTIONS]
```

---

## Descrição

Exibe os processos rodando dentro de um container. Similar ao comando `top` do Linux.

---

## Parâmetros

| Parâmetro | Descrição |
|-----------|-----------|
| `CONTAINER` | Nome ou ID do container |
| `[ps OPTIONS]` | Opções do comando `ps` do Unix |

---

## Como Funciona

- Executa `ps` dentro do namespace do container
- Mostra processos do container, não do host
- Aceita flags do comando `ps`

---

## Exemplos

### Ver Processos
```bash
docker top mycontainer
UID    PID     PPID    C    STIME   TTY    TIME        CMD
root   13642   12345   0    10:00   pts/0  00:00:00    nginx: master process
root   13643   13642   0    10:00   pts/0  00:00:00    nginx: worker process
```

### Com Opções ps
```bash
docker top mycontainer aux
USER   PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root     1  0.0  0.1 123456 7890 ?        Ss   10:00   0:00 nginx: master process
root    10  0.0  0.2 123456 8901 ?        S    10:00   0:00 nginx: worker process
```

### Filtros
```bash
# Apenas processos nginx
docker top mycontainer | grep nginx

# Processos de um usuário específico
docker top mycontainer | grep www-data
```

---

## Output

| Coluna | Descrição |
|--------|-----------|
| `UID` | User ID do processo |
| `PID` | Process ID no host |
| `PPID` | Parent Process ID |
| `C` | CPU usage |
| `STIME` | Start time |
| `TTY` | Terminal |
| `TIME` | Tempo de CPU |
| `CMD` | Comando |

---

## Diferenças vs docker exec ps

| Aspecto | docker top | docker exec ps |
|---------|-----------|----------------|
| Namespace | Host | Container |
| Output | Do host | Do container |
| PID | PID do host | PID do container |
| Overhead | Menor | Executa novo processo |

---

## Conceitos Aprendidos

1. **Namespace do host** - PIDs são do host
2. **ps OPTIONS** - Flags do Unix ps
3. **PPID** - Parent Process ID útil para debug
4. **UID** - User ID do processo

---

## Aplicações Práticas

1. **Debugging** - Ver processos rodando
2. **Security audit** - Identificar processos suspeitos
3. **Resource tracking** - Identificar processos pesados
4. **Process hierarchy** - Ver relação pai/filho

---

## Referências Cruzadas

- Ver: `044-docker-stats.md`
- Ver: `042-docker-exec.md`
- Relacionado: Process namespaces, cgroups