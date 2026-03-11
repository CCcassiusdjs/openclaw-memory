# Mastering Docker Logs - Dash0

**URL:** https://www.dash0.com/guides/mastering-docker-logs
**Lido em:** 2026-03-11
**Categoria:** Monitoring
**Prioridade:** Alta

---

## Resumo

Guia completo sobre gerenciamento de logs em Docker, desde comandos básicos até estratégias de produção.

---

## Conceitos-Chave

### 1. Comandos Básicos de Logs
```bash
# Ver todos os logs
docker logs <container>

# Seguir logs em tempo real
docker logs -f <container>

# Últimas 100 linhas
docker logs --tail 100 <container>

# Logs dos últimos 15 minutos
docker logs --since 15m <container>

# Filtrar com grep
docker logs <container> | grep <filter>

# Docker Compose
docker compose logs <service>
docker compose logs -f
docker compose logs --no-log-prefix <service>
```

### 2. Localização dos Logs
- **Path padrão:** `/var/lib/docker/containers/<container-id>/<container-id>-json.log`
- **Verificar path:** `docker inspect -f '{{.LogPath}}' <container>`
- **Verificar driver:** `docker inspect -f '{{.HostConfig.LogConfig.Type}}' <container>`

### 3. Logging Drivers
| Driver | Uso |
|--------|-----|
| `json-file` | Padrão, armazena em JSON |
| `local` | Recomendado, mais eficiente, rotação built-in |
| `none` | Desabilita logging |
| `syslog` | Envia para syslog daemon |
| `journald` | Escreve para journald |
| `fluentd` | Forward para Fluentd |
| `awslogs/gcplogs` | Cloud platforms |

### 4. Configuração Global (daemon.json)
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "4",
    "compress": "true"
  }
}
```

### 5. Configuração por Container
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    logging:
      driver: "local"
      options:
        max-size: "50m"
        max-file: "4"
        compress: "true"
```

### 6. YAML Anchors para Reuso
```yaml
x-default-logging: &logging
  driver: "local"
  options:
    max-size: "50m"
    max-file: "4"

services:
  app1:
    logging: *logging
  app2:
    logging: *logging
```

### 7. Log Delivery Mode

**Blocking Mode (padrão):**
- Síncrono
- Aplicação espera confirmação
- Bom para drivers locais (local, json-file)
- Problemático para drivers de rede

**Non-Blocking Mode:**
- Assíncrono
- Buffer em memória (default 1MB)
- Risco de perda de logs se buffer encher
- Aumentar buffer: `max-buffer-size: "50m"`

```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "mode": "non-blocking",
    "max-buffer-size": "50m"
  }
}
```

### 8. Filtros de Tempo
```bash
# Logs desde timestamp
docker logs --since "2013-01-02T13:23:37Z" <container>

# Logs até timestamp
docker logs --until "2025-06-13T10:00:00" <container>

# Combinar
docker logs --since 2025-06-13T18:00:00 --until 2025-06-13T18:15:00 <container>
```

### 9. GUI Tools
- **Docker Desktop:** Aba Logs integrada
- **Dozzle:** Leve, web-based
```bash
docker run -d --name dozzle \
  -p 8888:8080 \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  amir20/dozzle:latest
```

### 10. OpenTelemetry Integration
```yaml
# daemon.json
{
  "log-driver": "fluentd",
  "log-opts": {
    "fluentd-address": "localhost:8006",
    "tag": "opentelemetry-demo"
  }
}

# OTel Collector config
receivers:
  fluentforward:
    endpoint: 0.0.0.0:8006
processors:
  batch:
  resourcedetection/system:
exporters:
  otlphttp/dash0:
    endpoint: <endpoint>
service:
  pipelines:
    logs:
      receivers: [fluentforward]
      processors: [batch, resourcedetection/system]
      exporters: [otlphttp/dash0]
```

---

## Troubleshooting

### docker logs shows no output
**Causa:** Aplicação não escreve para stdout/stderr
**Solução:** 
```dockerfile
# Redirecionar logs de arquivo
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log
```

### Logging driver does not support reading
**Causa:** Remote drivers não armazenam localmente
**Solução:** Habilitar cache
```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "cache-disabled": "false"
  }
}
```

---

## Best Practices

1. **stdout/stderr:** Sempre escrever logs para stdout/stderr
2. **Non-blocking mode:** Para drivers de rede
3. **Metadata:** Incluir container name, ID, service
4. **Log rotation:** Sempre configurar max-file e max-size
5. **Structured logging:** Preferir JSON logs

---

## Insights Práticos

- **local driver** é melhor que json-file (compactação + rotação built-in)
- **Non-blocking** é essencial para não bloquear aplicação com drivers de rede
- **YAML anchors** reduzem repetição em compose files
- **Dozzle** é alternativa leve para visualização de logs
- **fluentd driver** + OTel Collector = melhor pipeline para produção