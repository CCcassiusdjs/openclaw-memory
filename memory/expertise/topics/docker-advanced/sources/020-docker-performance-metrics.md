# Docker Container Performance Metrics (Last9)

**Fonte:** https://last9.io/blog/docker-container-performance-metrics/
**Tipo:** Blog Post (Observability)
**Lido em:** 2026-03-10
**Status:** completed

---

## Métricas Críticas

### CPU Metrics
| Métrica | Descrição |
|---------|-----------|
| CPU Usage % | Uso do CPU alocado |
| CPU Throttling | Quando atinge limites |
| CPU Load Average | Profundidade da fila de processamento |

**Alert thresholds:**
- Warning: >70% por 5 min
- Critical: >85% por 5 min

### Memory Metrics
| Métrica | Descrição |
|---------|-----------|
| Memory Usage | RAM atual |
| Memory Limit | Limite configurado |
| Cache Usage | Memória para cache |
| Swap Usage | Uso de disco como memória |
| Memory Failures | Tentativas de exceder limite |
| OOM Kills | Kills por exaustão de memória |

**Alert thresholds:**
- Warning: >75% por 5 min
- Critical: >90% por 2 min

### Disk I/O Metrics
| Métrica | Descrição |
|---------|-----------|
| Read/Write Ops | Contagem de operações |
| Bytes Read/Written | Volume de dados |
| I/O Wait Time | Tempo de espera |
| Disk Space Usage | Armazenamento disponível |
| Inode Usage | Consumo de inodes |

### Network Metrics
| Métrica | Descrição |
|---------|-----------|
| Bytes Received/Sent | Tráfego total |
| Packet Rate | Pacotes processados |
| Error Rate | Operações falhadas |
| Connection Count | Conexões ativas |
| Network Latency | Latência entre containers |

### Container Lifecycle Metrics
| Métrica | Descrição |
|---------|-----------|
| Container Count | Por estado (running, stopped, paused) |
| Container Restarts | Frequência de restarts |
| Container Uptime | Tempo rodando |
| Exit Codes | Razão de término |

---

## Ferramentas de Monitoramento

### Built-in: docker stats
```bash
docker stats [CONTAINER_ID]
```
- CPU, memory, network, I/O em tempo real
- Sem dados históricos

### cAdvisor
```bash
docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:latest
```
- Dashboard visual
- Métricas históricas

### Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'docker'
    static_configs:
      - targets: ['localhost:9323']
```

### Stack Completa
| Stack | Uso |
|-------|-----|
| Telegraf + InfluxDB | Alta performance |
| Elasticsearch + Kibana | Logs + métricas |
| Portainer | UI de gestão |
| Prometheus + Grafana | Observability padrão |

---

## Application Metrics

### Expor métricas customizadas (Node.js)
```javascript
const express = require('express');
const app = express();
const prom = require('prom-client');

const apiCallsCounter = new prom.Counter({
  name: 'api_calls_total',
  help: 'Total number of API calls'
});

app.get('/api/data', (req, res) => {
  apiCallsCounter.inc();
  // API logic
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', prom.register.contentType);
  res.end(await prom.register.metrics());
});
```

---

## Diagnóstico de Performance

### Memory Leak
- Aumento gradual de memória que nunca estabiliza
- Comparar uso com padrões de tráfego

### Noisy Neighbor
- Comparar CPU steal entre containers
- Identificar contenção de recursos

### Correlação de Eventos
- Marcar deployments, config changes, eventos
- Relacionar com mudanças nas métricas

---

## Right-Sizing

```bash
# Container nunca usa mais que 256MB, mas tem 1GB
docker run --memory=384m --memory-reservation=256m your-image

# CPU quota
docker run --cpu-quota=50000 --cpu-period=100000 your-image
# Limita a 50% de CPU
```

---

## Boas Práticas

1. **Coletar métricas a 15-30s** - Balanceia detalhe e storage
2. **Alertar apenas no crítico** - Evita alert fatigue
3. **Manter tiered retention** - 15s por 2 dias, 1min por 4 semanas
4. **Right-size containers** - Usar dados históricos
5. **Correlacionar eventos** - Deployments, mudanças de config

## Próximos Passos
- [ ] Configurar Prometheus
- [ ] Criar dashboards Grafana
- [ ] Implementar alertas