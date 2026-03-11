# Docker Container Stats - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/container/stats/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Uso

```bash
docker container stats [OPTIONS] [CONTAINER...]
docker stats [OPTIONS] [CONTAINER...]
```

---

## Descrição

Retorna um stream de estatísticas de uso de recursos para containers rodando.

---

## Opções

| Opção | Default | Descrição |
|-------|---------|-----------|
| `-a`, `--all` | - | Mostrar todos os containers (default: só rodando) |
| `--format` | - | Formatar output (table, json, template) |
| `--no-stream` | - | Desabilitar streaming, só primeira leitura |
| `--no-trunc` | - | Não truncar output |

---

## Colunas (Linux)

| Coluna | Descrição |
|--------|-----------|
| `CONTAINER ID` | ID do container |
| `NAME` | Nome do container |
| `CPU %` | Porcentagem de CPU usada |
| `MEM USAGE / LIMIT` | Memória usada / limite |
| `MEM %` | Porcentagem de memória |
| `NET I/O` | Entrada/saída de rede |
| `BLOCK I/O` | Entrada/saída de bloco |
| `PIDS` | Número de processos/threads |

---

## Colunas (Windows)

| Coluna | Descrição |
|--------|-----------|
| `CONTAINER ID` | ID do container |
| `NAME` | Nome do container |
| `CPU %` | Porcentagem de CPU |
| `PRIV WORKING SET` | Memória privada |
| `NET I/O` | Entrada/saída de rede |
| `BLOCK I/O` | Entrada/saída de bloco |

---

## Exemplos

### Todos os Containers Rodando
```bash
docker stats
CONTAINER ID   NAME              CPU %   MEM USAGE / LIMIT   MEM %   NET I/O       BLOCK I/O      PIDS
b95a83497c91   awesome_brattain  0.28%   5.629MiB / 1.952GiB 0.28%   916B / 0B     147kB / 0B     9
67b2525d8ad1   foobar            0.00%   1.727MiB / 1.952GiB 0.09%   2.48kB / 0B   4.11MB / 0B    2
```

### Containers Específicos
```bash
docker stats awesome_brattain 67b2525d8ad1
```

### Uma Leitura Sem Stream
```bash
docker stats --no-stream
```

### Formato JSON
```bash
docker stats nginx --no-stream --format "{{ json . }}"
# {"BlockIO":"0B / 13.3kB","CPUPerc":"0.03%","Container":"nginx",...}
```

### Formato Customizado
```bash
docker stats --all --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
CONTAINER        CPU %     MEM USAGE / LIMIT
fervent_panini   0.00%     56KiB / 15.57GiB
5acfcb1b4fd1     0.07%     32.86MiB / 15.57GiB
```

---

## Placeholders para --format

| Placeholder | Descrição |
|-------------|-----------|
| `.Container` | Nome ou ID (input do usuário) |
| `.Name` | Nome do container |
| `.ID` | ID do container |
| `.CPUPerc` | Porcentagem de CPU |
| `.MemUsage` | Uso de memória |
| `.NetIO` | Network I/O |
| `.BlockIO` | Block I/O |
| `.MemPerc` | Porcentagem de memória (não Windows) |
| `.PIDs` | Número de PIDs (não Windows) |

---

## Notas Importantes

### Cálculo de Memória (Linux)
- Docker CLI subtrai cache do total
- API retorna total e cache separadamente
- Cache = `total_inactive_file` (cgroup v1) ou `inactive_file` (cgroup v2)

### PIDs
- Conta processos E kernel threads
- Valor alto com poucos processos = muitas threads criadas

---

## Formato Default

**Linux:**
```
table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}
```

**Windows:**
```
table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}
```

---

## Conceitos Aprendidos

1. **Streaming por default** - Atualiza continuamente
2. **--no-stream** - Uma leitura apenas
3. **--all** - Inclui containers parados
4. **Cache memory** - Docker subtrai cache do total
5. **PIDs inclui threads** - Não apenas processos

---

## Aplicações Práticas

1. **Monitoramento** - Ver uso de recursos em tempo real
2. **Debugging** - Identificar containers problemáticos
3. **Capacity planning** - Analisar consumo de recursos
4. **Automation** - Parse JSON para alertas
5. **Performance tuning** - Identificar gargalos

---

## Referências Cruzadas

- Ver: `043-docker-inspect.md`
- Ver: `035-resource-constraints.md`
- Relacionado: docker top, cgroups