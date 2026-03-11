# docker service ps - Docker CLI Reference

**URL:** https://docs.docker.com/reference/cli/docker/service/ps/
**Lido em:** 2026-03-11
**Categoria:** Orchestration
**Prioridade:** Média

---

## Resumo

Referência do comando `docker service ps` para listar tasks de um serviço Swarm.

---

## Uso Básico

```bash
docker service ps SERVICE [SERVICE...]
```

Lista todas as tasks de um ou mais serviços.

---

## Output Padrão

```
ID             NAME      IMAGE        NODE      DESIRED STATE  CURRENT STATE          ERROR  PORTS
0qihejybwf1x   redis.1   redis:7.4.0  manager1  Running        Running 8 seconds
bk658fpbex0d   redis.2   redis:7.4.0  worker2   Running        Running 9 seconds
5ls5s5fldaqg   redis.3   redis:7.4.0  worker1   Running        Running 9 seconds
```

### Colunas:
- **ID:** Task ID
- **NAME:** Task name (service.slot)
- **IMAGE:** Image com tag
- **NODE:** Node onde está rodando
- **DESIRED STATE:** Estado desejado (Running, Shutdown, Accepted)
- **CURRENT STATE:** Estado atual e timestamp
- **ERROR:** Mensagem de erro (se houver)
- **PORTS:** Portas publicadas

---

## Task History

O comando mostra também o histórico de tasks:

```
ID            NAME         IMAGE        NODE      DESIRED STATE  CURRENT STATE                   ERROR  PORTS
50qe8lfnxaxk  redis.1      redis:7.4.1  manager1  Running        Running 6 seconds ago
ky2re9oz86r9   \_ redis.1  redis:7.4.0  manager1  Shutdown       Shutdown 8 seconds ago
3s46te2nzl4i  redis.2      redis:7.4.1  worker2   Running        Running less than a second ago
nvjljf7rmor4   \_ redis.2  redis:7.4.1  worker2   Shutdown       Rejected 23 seconds ago        "No such image"
```

- Tasks com `\_` prefix são versões anteriores
- Número de itens controlado por `--task-history-limit` (docker swarm update)

---

## Opções

| Flag | Descrição |
|------|-----------|
| `-f, --filter` | Filtrar output |
| `--format` | Go template para formatar |
| `--no-resolve` | Não resolver IDs para nomes |
| `--no-trunc` | Não truncar output |
| `-q, --quiet` | Mostrar apenas task IDs |

---

## Filtros

### Filtrar por ID

```bash
docker service ps -f "id=8" redis
```

### Filtrar por Nome

```bash
docker service ps -f "name=redis.1" redis
```

### Filtrar por Node

```bash
docker service ps -f "node=manager1" redis
```

### Filtrar por Desired State

```bash
docker service ps -f "desired-state=running" redis
docker service ps -f "desired-state=shutdown" redis
docker service ps -f "desired-state=accepted" redis
```

### Múltiplos Filtros (OR)

```bash
docker service ps -f "name=redis.1" -f "name=redis.7" redis
```

---

## Format (Go Templates)

### Placeholders Disponíveis:

| Placeholder | Descrição |
|-------------|-----------|
| `.ID` | Task ID |
| `.Name` | Task name |
| `.Image` | Task image |
| `.Node` | Node ID |
| `.DesiredState` | Estado desejado |
| `.CurrentState` | Estado atual |
| `.Error` | Mensagem de erro |
| `.Ports` | Portas publicadas |

### Exemplos:

```bash
# Format simples
docker service ps --format "{{.Name}}: {{.Image}}" top

# Output:
# top.1: busybox
# top.2: busybox
# top.3: busybox

# Com headers
docker service ps --format "table {{.Name}}\t{{.Node}}\t{{.CurrentState}}" redis
```

---

## Detalhes com --no-trunc

```bash
docker service ps --no-trunc redis
```

Mostra:
- Task ID completo (não truncado)
- Image digest completo
- Error messages completas

---

## Casos de Uso

### Debug de Tasks Falhando

```bash
# Ver tasks com erro
docker service ps redis | grep -i error

# Ver histórico completo
docker service ps --no-trunc redis
```

### Ver Tasks em Node Específico

```bash
docker service ps -f "node=worker1" redis
```

### Ver Tasks Running

```bash
docker service ps -f "desired-state=running" redis
```

### Ver Tasks Shutdown (History)

```bash
docker service ps -f "desired-state=shutdown" redis
```

---

## Task History Limit

Configurado no swarm:

```bash
# Ver limite atual
docker swarm inspect --format '{{.Spec.TaskHistoryRetentionLimit}}'

# Alterar limite
docker swarm update --task-history-limit 10
```

---

## Key Takeaways

1. **Histórico:** Mostra tasks anteriores com `_` prefix
2. **--no-trunc:** Para debug detalhado
3. **Filtros:** id, name, node, desired-state
4. **Go templates:** Formatação customizada
5. **Task limit:** Configurável no swarm