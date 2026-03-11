# Docker Container Logs - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/container/logs/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Uso

```bash
docker container logs [OPTIONS] CONTAINER
docker logs [OPTIONS] CONTAINER
```

---

## Descrição

Recupera logs presentes no momento da execução. Para logs em tempo real, use `--follow`.

---

## Opções

| Opção | Default | Descrição |
|-------|---------|-----------|
| `--details` | - | Mostra detalhes extras (env vars, labels) |
| `-f`, `--follow` | - | Stream de logs em tempo real |
| `--since` | - | Logs desde timestamp ou duração |
| `-n`, `--tail` | `all` | Número de linhas do final |
| `-t`, `--timestamps` | - | Mostra timestamps |
| `--until` | - | Logs até timestamp ou duração (API 1.35+) |

---

## Timestamps

### Formato
- RFC3339Nano: `2014-09-16T06:17:46.000000000Z`
- Nanosegundos padded com zeros para alinhamento

### --since
| Formato | Exemplo |
|---------|---------|
| RFC3339 | `2013-01-02T13:23:37Z` |
| RFC3339Nano | `2013-01-02T13:23:37.123456789Z` |
| UNIX timestamp | `1357130217` |
| Go duration | `1m30s`, `3h` |
| Date only | `2006-01-02` |

### Timezone
- Sem `Z` ou offset: usa timezone local do cliente
- Com `Z` ou offset: usa UTC

---

## Exemplos

### Follow em Tempo Real
```bash
docker logs -f nginx
```

### Últimas N Linhas
```bash
docker logs -n 100 nginx
docker logs --tail 50 nginx
```

### Com Timestamps
```bash
docker logs -t nginx
# Output: 2014-09-16T06:17:46.000000000Z Log message
```

### Filtro por Tempo
```bash
# Desde um timestamp
docker logs --since 2013-01-02T13:23:37Z nginx

# Desde uma duração relativa
docker logs --since 1h30m nginx
docker logs --since 42m nginx

# Até um timestamp
docker logs --until 2017-11-14T16:40:02Z nginx

# Combinar since e until
docker logs --since 2023-01-01 --until 2023-01-02 nginx
```

### Detalhes Extras
```bash
# Mostrar environment variables e labels passados ao container
docker logs --details nginx
```

---

## Log Drivers

Para configurar logging drivers, ver [Configure logging drivers](/engine/logging/configure/).

### Drivers Disponíveis
| Driver | Descrição |
|--------|-----------|
| `json-file` | Default, logs em JSON |
| `local` | Logs locais com rotação |
| `syslog` | Syslog daemon |
| `journald` | systemd journal |
| `gelf` | Graylog Extended Log Format |
| `fluentd` | Fluentd logging |
| `awslogs` | Amazon CloudWatch |
| `splunk` | Splunk logging |

---

## Limitações

- Logs são do STDOUT e STDERR do container
- Não funciona com todos os logging drivers
- Alguns drivers não suportam `docker logs`

---

## Conceitos Aprendidos

1. **Batch vs Stream** - Default é batch, `-f` é stream
2. **Timestamps RFC3339Nano** - Formato padrão com nanosegundos
3. **Go duration strings** - `1m30s`, `3h` como input
4. **Details** - Mostra metadata passado ao container
5. **Until** - Filtro temporal inverso (até)

---

## Aplicações Práticas

1. **Debugging** - Logs em tempo real com `-f`
2. **Auditing** - Filtros temporais para análise
3. **Automation** - Parse de logs com `--tail` e `--since`
4. **Monitoring** - Integration com log aggregation

---

## Referências Cruzadas

- Ver: `012-docker-logging-drivers.md`
- Ver: `038-docker-system-df.md`
- Relacionado: Logging drivers, log rotation