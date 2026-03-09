# FS Monitor - Sistema de Monitoramento em Tempo Real

Sistema completo para monitoramento de alterações em sistema de arquivos com 3.2M+ arquivos.

## Componentes

### 1. `fs-monitor.sh` - Script Bash (Monitoramento Básico)

**Uso:**
```bash
# Verificar dependências e limites
./fs-monitor.sh --check

# Criar baseline
./fs-monitor.sh --baseline

# Detectar mudanças
./fs-monitor.sh --changes

# Monitorar em tempo real
./fs-monitor.sh --monitor

# Relatório
./fs-monitor.sh --report

# Tudo junto
./fs-monitor.sh --all
```

**Variáveis de ambiente:**
- `WATCH_DIRS` - Diretórios a monitorar (padrão: `/home/csilva`)
- `LOG_DIR` - Diretório de logs (padrão: `~/.openclaw/workspace/logs/fs-monitor`)
- `MAX_EVENTS` - Máximo de eventos antes de flush (padrão: 10000)
- `BATCH_INTERVAL` - Intervalo de flush em segundos (padrão: 5)

### 2. `fs-monitor-daemon.py` - Daemon Python (Monitoramento Avançado)

**Características:**
- ✅ Monitoramento via `inotifywait` (Linux)
- ✅ Armazenamento em SQLite para queries
- ✅ Batch processing para alta performance
- ✅ Processamento paralelo
- ✅ Logs estruturados

**Uso:**
```bash
# Direto
python3 fs-monitor-daemon.py

# Com variáveis de ambiente
WATCH_DIRS=/home/csilva:/mnt/data python3 fs-monitor-daemon.py
```

### 3. `fs-query.py` - Consulta ao Banco

**Uso:**
```bash
# Eventos recentes
./fs-query.py events --since 2026-03-08 --limit 20

# Filtrar por tipo
./fs-query.py events --type CREATE --path /home/csilva/Documents

# Estatísticas do dia
./fs-query.py stats --date 2026-03-08

# Estatísticas de hoje
./fs-query.py stats

# Detectar anomalias
./fs-query.py anomalies --threshold 50

# Baseline
./fs-query.py baseline --path /home/csilva/Documents

# Saída JSON
./fs-query.py stats --format json
```

### 4. `fs-monitor.service` - Systemd Service

**Instalação:**
```bash
# Copiar para systemd
sudo cp fs-monitor.service /etc/systemd/system/

# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar
sudo systemctl enable fs-monitor.service

# Iniciar
sudo systemctl start fs-monitor.service

# Ver status
sudo systemctl status fs-monitor.service

# Ver logs
journalctl -u fs-monitor.service -f
```

## Limites do Sistema

### inotify

Verificar limites atuais:
```bash
cat /proc/sys/fs/inotify/max_user_watches  # Default: 504,252
cat /proc/sys/fs/inotify/max_user_instances  # Default: 128
```

**Com 365,366 diretórios, você precisa de pelo menos 400,000 watches.**

Aumentar limites:
```bash
# Temporário
sudo sysctl fs.inotify.max_user_watches=1000000
sudo sysctl fs.inotify.max_user_instances=512

# Permanente (adicionar ao /etc/sysctl.d/99-inotify.conf)
sudo tee /etc/sysctl.d/99-inotify.conf <<EOF
fs.inotify.max_user_watches=1000000
fs.inotify.max_user_instances=512
fs.inotify.max_queued_events=32768
EOF

sudo sysctl -p /etc/sysctl.d/99-inotify.conf
```

## Performance

### Estimativa de Recursos

| Métrica | Estimativa |
|---------|------------|
| **Watches necessários** | ~400,000 |
| **Memória por watch** | ~1KB |
| **Memória total** | ~400MB |
| **CPU (idle)** | ~1-2% |
| **CPU (atividade alta)** | ~10-20% |
| **I/O (batch)** | Moderado |
| **Banco SQLite** | ~10-50MB/dia |

### Otimizações Implementadas

1. **Batch Processing** - Eventos agregados antes de escrever
2. **Fila Assíncrona** - Worker thread separado para I/O
3. **Exclusões** - Padrões como `.git`, `.cache` ignorados
4. **Índices SQLite** - Queries rápidas por timestamp, path, tipo

## Estrutura de Logs

```
~/.openclaw/workspace/logs/fs-monitor/
├── events-20260308.log          # Eventos diários (texto)
├── events-20260308.log.json     # Eventos diários (JSON)
├── daemon.log                    # Log do daemon
├── baseline.txt                  # Baseline atual
├── fs-monitor.db                 # Banco SQLite
└── errors-20260308.log          # Erros
```

## Exemplos de Uso

### Monitoramento Contínuo

```bash
# Iniciar daemon (background)
nohup python3 fs-monitor-daemon.py > /dev/null 2>&1 &

# Ou via systemd
sudo systemctl start fs-monitor.service
```

### Consultas Úteis

```bash
# O que mudou hoje?
./fs-query.py stats --date $(date +%Y-%m-%d)

# Arquivos criados recentemente
./fs-query.py events --type CREATE --since $(date -d '1 hour ago' +%Y-%m-%dT%H:%M:%S)

# Anomalias (deletions em massa)
./fs-query.py anomalies --threshold 100

# Timeline de atividade
./fs-query.py stats --format json | jq '.timeline'
```

### Integração com Alertas

```bash
# Script de alerta (exemplo)
#!/bin/bash
ANOMALIES=$(./fs-query.py anomalies --threshold 50 --format json)
COUNT=$(echo "$ANOMALIES" | jq 'length')

if [ "$COUNT" -gt 0 ]; then
    echo "ALERTA: $COUNT anomalias detectadas"
    echo "$ANOMALIES" | jq -r '.[] | .description'
fi
```

## Troubleshooting

### Erro: "No space left on device" (inotify)

```bash
# Verificar uso atual
find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | wc -l

# Aumentar limite
sudo sysctl fs.inotify.max_user_watches=1000000
```

### Erro: "Too many open files"

```bash
# Verificar limite
ulimit -n

# Aumentar temporário
ulimit -n 65536

# Permanente (adicionar ao ~/.bashrc)
echo "ulimit -n 65536" >> ~/.bashrc
```

### Performance Lenta

1. **Reduzir escopo** - Monitorar apenas diretórios críticos
2. **Aumentar batch size** - `BATCH_SIZE=500`
3. **Aumentar flush interval** - `FLUSH_INTERVAL=10`
4. **Excluir mais padrões** - Adicionar ao `--exclude` do inotifywait

## Próximos Passos

1. **API REST** - Flask/FastAPI para consultas remotas
2. **Web Dashboard** - Interface gráfica para visualização
3. **Alertas em tempo real** - Integração com notificações
4. **Compressão de logs** - Rotação automática
5. **Backup incremental** - Sincronização com armazenamento externo