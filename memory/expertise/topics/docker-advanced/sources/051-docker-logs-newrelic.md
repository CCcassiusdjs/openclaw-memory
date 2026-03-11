# Guide to Docker Logs - New Relic

**URL:** https://newrelic.com/blog/infrastructure-monitoring/docker-logs
**Lido em:** 2026-03-11
**Categoria:** Monitoring
**Prioridade:** Média

---

## Resumo

Guia prático sobre logs Docker com foco em monitoramento e troubleshooting.

---

## Conceitos-Chave

### 1. O que são Docker Logs
Logs capturam tudo enviado para stdout/stderr:
- Mensagens, warnings, errors da aplicação
- Kernel messages e system errors
- Lifecycle events (start/stop)
- Resource usage metrics (CPU, memory, disk)
- Network activity (requests/responses)
- Security events (vulnerabilities, unauthorized access)

### 2. Por que ver Docker Logs
- **Troubleshooting:** Exceções, stack traces, warnings
- **Performance bottlenecks:** Response time trends, resource spikes
- **Proactive monitoring:** Baseline behavior, anomaly detection
- **Security audits:** Authentication attempts, data access patterns
- **Compliance:** GDPR, HIPAA, SOC 2

### 3. Comandos Essenciais

```bash
# Ver todos os logs
docker logs <container_id>

# Com timestamps
docker logs --timestamps <container_id>
docker logs -t <container_id>

# Com detalhes adicionais
docker logs --details <container_id>

# Últimas N linhas
docker logs --tail 50 my-project
docker logs -n 50 my-project

# Logs desde timestamp
docker logs --since 2025-03-20 my-project
docker logs --since 45m my-project

# Logs até timestamp
docker logs --until 2025-03-20 my-project
docker logs --until 30m my-project

# Real-time monitoring
docker logs --follow <container_id>
docker logs -f <container_id>

# Combinar opções
docker logs -n 100 -t my-project
```

### 4. Filtragem com Grep

```bash
# Buscar padrões
docker logs <container_id> | grep "error"

# Múltiplos padrões
docker logs <container_id> | grep -E "error|warn|critical"

# Case-insensitive
docker logs <container_id> | grep -i "error"

# Inverter match
docker logs <container_id> | grep -v "healthcheck"
```

### 5. Logging Drivers Comuns

```bash
# JSON file (padrão)
docker run --log-driver=json-file nginx

# Syslog
docker run --log-driver=syslog nginx

# Fluentd
docker run --log-driver=fluentd nginx

# AWS CloudWatch
docker run --log-driver=awslogs nginx
```

### 6. Log Rotation

```yaml
# docker-compose.yml
services:
  app:
    image: nginx
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

### 7. Técnicas Avançadas

**Structured Logging:**
- Output em JSON (não plain text)
- Machine-readable para parsing/filtering

**Aggregation Across Services:**
- Correlation IDs para trace de requests
- Distributed tracing em microservices

**Log Sampling:**
- Para high-volume applications
- Reduz storage mantendo visibility

**External Storage:**
- Plataformas especializadas (New Relic, etc.)
- Advanced querying, visualization, alerting

---

## Best Practices

1. **stdout/stderr:** Sempre log para standard output
2. **JSON format:** Structured logging para parsing
3. **No sensitive data:** Nunca logar passwords, tokens, PII
4. **Orchestration features:** Usar logging do Kubernetes/Swarm
5. **Monitor volume:** Excessive logging impact performance
6. **Log rotation:** Configurar max-size e max-file

---

## Comparação com Dash0

| Aspecto | Dash0 | New Relic |
|---------|-------|-----------|
| Foco | Deep dive técnico | Visão geral + vendas |
| Detalhes técnicos | Mais profundo | Mais superficial |
| Exemplos práticos | Mais completos | Mais básicos |
| OpenTelemetry | Detalhado | Mencionado |

---

## Insights

- New Relic foca mais em "por que usar" vs "como usar"
- Complementa bem o Dash0 para visão de negócio
- Boa introdução para iniciantes
- Menos detalhes técnicos que Dash0