# Configure Logging Drivers - Documentação Oficial

**Fonte:** https://docs.docker.com/config/containers/logging/configure/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Visão Geral

Docker usa logging drivers para capturar logs de containers. Cada daemon tem um driver default, e cada container pode usar um driver diferente.

---

## Drivers Disponíveis

| Driver | Descrição |
|--------|-----------|
| `none` | Sem logs, `docker logs` não retorna nada |
| `local` | Formato customizado, rotação automática, baixo overhead |
| `json-file` | JSON interno, **default** |
| `syslog` | Syslog facility |
| `journald` | systemd journal |
| `gelf` | Graylog Extended Log Format |
| `fluentd` | Fluentd (forward input) |
| `awslogs` | Amazon CloudWatch Logs |
| `splunk` | Splunk HTTP Event Collector |
| `etwlogs` | Event Tracing for Windows |
| `gcplogs` | Google Cloud Platform Logging |

---

## ⚠️ Importante: json-file vs local

> **Use `local` logging driver para prevenir disk exhaustion!**

### json-file (Default)
- Sem rotação por default
- Logs podem consumir todo o disco
- Mantido para backward compatibility e Kubernetes

### local (Recomendado)
- Rotação automática por default
- Formato mais eficiente
- Prevenção de disk exhaustion

---

## Configurar Default Logging Driver

### daemon.json
```json
{
  "log-driver": "local"
}
```

### Com Opções
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3",
    "labels": "production_status",
    "env": "os,customer"
  }
}
```

### Verificar Default
```bash
docker info --format '{{.LoggingDriver}}'
# json-file
```

---

## Configurar por Container

### Driver Específico
```bash
docker run -it --log-driver none alpine ash
```

### Com Opções
```bash
docker run -d \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  nginx
```

### Verificar Driver do Container
```bash
docker inspect -f '{{.HostConfig.LogConfig.Type}}' <CONTAINER>
# json-file
```

---

## Delivery Mode

### Blocking (Default)
- Container bloqueia até log ser escrito
- Pode causar backpressure
- Aplicações podem falhar

### Non-blocking
- Buffer intermediário
- Previne bloqueio
- Mensagens podem ser perdidas

```bash
docker run -it \
  --log-opt mode=non-blocking \
  --log-opt max-buffer-size=4m \
  alpine ping 127.0.0.1
```

### Opções
| Opção | Default | Descrição |
|-------|---------|-----------|
| `mode` | `blocking` | `blocking` ou `non-blocking` |
| `max-buffer-size` | `1m` | Tamanho do buffer (non-blocking) |

---

## Environment Variables e Labels

### Passar Variáveis
```bash
docker run -dit \
  --label production_status=testing \
  -e os=ubuntu \
  alpine sh
```

### Output (json-file)
```json
"attrs": {
  "production_status": "testing",
  "os": "ubuntu"
}
```

---

## Limitações

1. **Rotação de logs** - Requer decompressão, aumento temporário de disco e CPU
2. **Capacidade do host** - Limitado pelo storage do host
3. **Drivers** - Nem todos suportam `docker logs`

---

## Logging Driver Plugins

Docker suporta plugins de logging driver:
- [Logging driver plugins](/engine/logging/configure/plugins/)

---

## Best Practices

1. **Use `local` driver** - Prevenção de disk exhaustion
2. **Configure max-size e max-file** - Limite de tamanho
3. **Use non-blocking** - Se logs volumosos
4. **External logging** - syslog, fluentd, cloud para produção
5. **Labels e env** - Metadata para filtro

---

## Conceitos Aprendidos

1. **json-file é default** - Sem rotação, pode encher disco
2. **local é recomendado** - Rotação automática
3. **Non-blocking mode** - Buffer para não bloquear container
4. **Labels e env** - Metadata nos logs
5. **Per-container config** - Override do default

---

## Aplicações Práticas

1. **Production** - syslog/fluentd para centralização
2. **Development** - local ou json-file com rotação
3. **Kubernetes** - json-file (compatibilidade)
4. **Debugging** - non-blocking para não afetar app

---

## Referências Cruzadas

- Ver: `012-docker-logging-drivers.md`
- Ver: `037-container-logs-cli.md`
- Relacionado: json-file, local driver, log rotation