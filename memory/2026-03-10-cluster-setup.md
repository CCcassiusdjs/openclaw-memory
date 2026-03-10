# Cluster Docker Swarm - Setup Completo

## Visão Geral

Cluster multipropósito para ArduPilot SITL, Gêmeos Digitais e ML Pipeline.

---

## Topologia

```
┌─────────────────────────────────────────────────────────────────┐
│  T620 (Manager) - 24 vCPU, 32GB RAM                           │
│  IP: 10.10.20.11                                                │
│  Role: Manager                                                  │
│  Labels: -                                                      │
│  Serviços: Traefik, Portainer, Visualizer, Grafana, Redis,     │
│            MQTT, API Gateway, MLflow, Dask Scheduler           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  T630A (Compute) - 40 vCPU, 94GB RAM                           │
│  IP: 10.10.20.12                                                │
│  Role: Worker                                                   │
│  Labels: compute=true                                           │
│  Serviços: Jupyter, Dask Workers                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  T630B (Storage) - 40 vCPU, 94GB RAM                           │
│  IP: 10.10.20.13                                                │
│  Role: Worker                                                   │
│  Labels: storage=true                                            │
│  Serviços: PostgreSQL, InfluxDB, MinIO                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Credenciais de Acesso

### Servidores (SSH)

| Servidor | IP | Usuário | Senha | hostname |
|----------|-----|---------|-------|----------|
| T620 | 10.10.20.11 | cassiusdjs | 230612 | t620 |
| T630A | 10.10.20.12 | cassiusdjs | 230612 | t630a.cluster.local |
| T630B | 10.10.20.13 | cassiusdjs | 230612 | t630b.cluster.local |

### FortiGate (Firewall)

| Campo | Valor |
|-------|-------|
| IP | 192.168.1.99 |
| Usuário | admin |
| Senha | @CiaoMiau2955 |
| SSH Port | 22 |

### Docker Swarm

| Campo | Valor |
|-------|-------|
| Join Token (Worker) | SWMTKN-1-17gw7fsdxob7yfjqmokh327gkflqroybx4ss0x7796bqk91zsj-aso0r8tjs85wcxxq0i3kbphrc |
| Manager | t620 (10.10.20.11:2377) |

---

## Serviços e URLs

### Gestão e Visualização

| Serviço | URL | Credenciais | Observações |
|---------|-----|-------------|-------------|
| Portainer | http://10.10.20.11:9000 | Criar senha no primeiro acesso | Gerenciamento de containers |
| Swarm Visualizer | http://10.10.20.11:8081 | - | Visualização do cluster |
| Traefik Dashboard | http://10.10.20.11:8080 | - | Reverse proxy |

### Banco de Dados

| Serviço | URL/Porta | Credenciais | Localização |
|---------|-----------|-------------|-------------|
| PostgreSQL | 10.10.20.13:5432 | ardupilot / ardupilot123 | T630B |
| InfluxDB | http://10.10.20.11:8086 | admin / admin123456 | T630B |
| Redis | 10.10.20.11:6379 | - | T620 |

### Visualização de Dados

| Serviço | URL | Credenciais | Observações |
|---------|-----|-------------|-------------|
| Grafana | http://10.10.20.11:3000 | admin / admin123 | Dashboards |

### MQTT e APIs

| Serviço | URL/Porta | Credenciais | Observações |
|---------|-----------|-------------|-------------|
| MQTT Broker | 10.10.20.11:1883 | - | Eclipse Mosquitto |
| API Gateway | http://10.10.20.11:5000 | - | Python HTTP Server |

### ML Pipeline

| Serviço | URL | Credenciais | Observações |
|---------|-----|-------------|-------------|
| Jupyter Lab | http://10.10.20.11:8888 | Token: ardupilot123 | TensorFlow notebook |
| MLflow | http://10.10.20.11:5001 | - | Experiment tracking |
| MinIO Console | http://10.10.20.11:9003 | admin / admin123456 | Object storage |
| Dask Dashboard | http://10.10.20.11:8787 | - | Computação distribuída |

---

## Stacks Docker

### Base Stack (base)

```yaml
- traefik:v2.10 (reverse proxy)
- portainer/portainer-ce:latest (container management)
- dockersamples/visualizer:latest (swarm visualization)
```

### ArduPilot Stack (ardupilot)

```yaml
- postgres:15-alpine (database)
- influxdb:2.7-alpine (time-series)
- grafana/grafana:latest (dashboards)
- redis:7-alpine (cache/filas)
```

### Digital Twin Stack (digitaltwin)

```yaml
- eclipse-mosquitto:2 (MQTT broker)
- python:3.11-slim (API gateway)
```

### ML Pipeline Stack (mlpipeline)

```yaml
- jupyter/tensorflow-notebook:latest (Jupyter Lab)
- ghcr.io/mlflow/mlflow:latest (experiment tracking)
- minio/minio:latest (object storage)
- daskdev/dask:latest (scheduler + workers)
```

---

## Portas Abertas (Firewall)

| Porta | Protocol | Serviço |
|-------|----------|---------|
| 2377 | TCP | Docker Swarm management |
| 7946 | TCP/UDP | Docker Swarm node communication |
| 4789 | UDP | Docker Overlay network |

---

## Arquivos de Stack

Localização: `/home/cassiusdjs/stacks/` em T620

- `base-stack.yml`
- `ardupilot-stack.yml`
- `digital-twin-stack.yml`
- `ml-pipeline-stack.yml`

---

## Comandos Úteis

### SSH para servidores

```bash
# T620 (Manager)
sshpass -p '230612' ssh cassiusdjs@10.10.20.11

# T630A (Compute)
sshpass -p '230612' ssh cassiusdjs@10.10.20.12

# T630B (Storage)
sshpass -p '230612' ssh cassiusdjs@10.10.20.13
```

### Docker Swarm

```bash
# Listar nós
docker node ls

# Listar serviços
docker service ls

# Listar containers no nó
docker ps

# Ver logs de serviço
docker service logs <serviço>

# Escalar serviço
docker service scale <serviço>=<replicas>

# Atualizar stack
docker stack deploy -c <arquivo.yml> <stack_name>
```

### Status do Cluster

```bash
# Verificar todos os serviços
docker service ls

# Verificar tarefas de um serviço
docker service ps <serviço>

# Verificar nós
docker node ls

# Verificar networks
docker network ls
```

---

## Rede

### Topologia Atual (2026-03-10)

```
Internet (WAN via DHCP)
     │
     ▼
ISP Modem → FortiGate 40F (lan2: 10.32.162.22)
     │
     ├── lan A (WiFi) ──► 192.168.2.1 ──► Laptop Cássio (192.168.2.102)
     │                                           │
     │                                           └── Rota para VLAN20: via 192.168.2.1
     │
     ├── lan1 (192.168.1.99) ──► DOWN (cabo desconectado)
     │
     ├── lan3 (192.168.3.1) ──► Switch HP V1910-16G (Trunk)
     │                               ├── VLAN10 ──► iDRAC (192.168.10.x)
     │                               ├── VLAN20 ──► T620 (10.10.20.11)
     │                               │              T630A (10.10.20.12)
     │                               │              T630B (10.10.20.13)
     │                               ├── VLAN30 ──► Workstations (192.168.30.x)
     │                               └── VLAN40 ──► Infra Crítica (192.168.40.x)
     │
     └── wan ──► DOWN (defeituosa)
```

### Status das Interfaces FortiGate

| Interface | IP | Status | Função |
|-----------|-----|--------|--------|
| wan | 0.0.0.0 | DOWN | Defeituosa |
| lan1 | 192.168.1.99/24 | DOWN | Gerenciamento (cabo off) |
| lan2 | 10.32.162.22/22 (DHCP) | UP | WAN/Internet |
| lan3 | 192.168.3.1/24 | UP | Trunk Switch |
| lan3.10 | 192.168.10.1/24 | UP | iDRAC |
| lan3.20 | 10.10.20.1/24 | UP | Cluster Docker |
| lan3.30 | 192.168.30.1/24 | UP | Workstations |
| lan3.40 | 192.168.40.1/24 | UP | Infra Crítica |
| a (WiFi) | 192.168.2.1/24 | UP | WiFi Router |

### Rota Persistente (Laptop)

```bash
# NetworkManager - rota para VLAN20 via WiFi
nmcli connection modify "LSA5GHz-New" +ipv4.routes "10.10.20.0/24 192.168.2.1"
```

### VLANs

| VLAN | Subnet | Função |
|------|--------|--------|
| VLAN10 | 192.168.10.1/24 | iDRAC Dell Servers |
| VLAN20 | 10.10.20.1/24 | DATA (Cluster) |
| VLAN30 | 192.168.30.1/24 | Workstations |
| VLAN40 | 192.168.40.1/24 | Infra Crítica |

---

## Status do Cluster (2026-03-10 19:40)

### Todos os Serviços Operacionais ✅

| Serviço | Status | Porta | URL |
|---------|--------|-------|-----|
| Traefik | ✅ Up | 80, 8080 | http://10.10.20.11:8080 |
| Portainer | ✅ Up | 9000 | http://10.10.20.11:9000 |
| Visualizer | ✅ Up | 8081 | http://10.10.20.11:8081 |
| PostgreSQL | ✅ Up | 5432 | 10.10.20.13:5432 |
| InfluxDB | ✅ Up | 8086 | http://10.10.20.11:8086 |
| Grafana | ✅ Up | 3000 | http://10.10.20.11:3000 |
| Redis | ✅ Up | 6379 | 10.10.20.11:6379 |
| MQTT | ✅ Up | 1883, 9001 | 10.10.20.11:1883 |
| API Gateway | ✅ Up | 5000 | http://10.10.20.11:5000 |
| Jupyter Lab | ✅ Up | 8888 | http://10.10.20.11:8888 |
| MLflow | ✅ Up | 5001 | http://10.10.20.11:5001 |
| MinIO | ✅ Up | 9002, 9003 | http://10.10.20.11:9002 |
| Dask Scheduler | ✅ Up | 8786, 8787 | http://10.10.20.11:8787 |
| Dask Worker (2x) | ✅ Up | - | T630A |

## Pendências

### FASE 5: Digital Twin
- ~~SITL Pool não deployado~~ → Removido do stack (imagem não disponível)
- Para usar ArduPilot SITL: compilar localmente ou usar imagem alternativa

### FASE 6: Custom Dashboard
- Dashboards Grafana customizados para telemetria

### FASE 7: API Gateway
- Atualmente: Python http.server (placeholder)
- Necessário: Implementar API REST real

### FASE 8: Security Hardening
- Firewall rules adicionais
- SSL/TLS certs (Traefik)
- Authentication (Portainer, Grafana, InfluxDB)

---

## Notas

- Docker Swarm token válido apenas enquanto cluster existir
- Para regenerar: `docker swarm join-token worker`
- Todos os serviços usando rede overlay `cluster-network`
- Volumes persistentes em cada nó
- Backup de configurações em `/root/pre-cluster-backup/` em cada servidor

---

## Automação

### Script Principal

```bash
# SSH no manager
ssh cassiusdjs@10.10.20.11

# Usar o script
~/scripts/cluster.sh <command>

# Ou usar aliases (adicionar ao .bashrc)
alias cluster="~/scripts/cluster.sh"
alias cs="~/scripts/cluster.sh"
alias chealth="~/scripts/cluster.sh health"
alias cstatus="~/scripts/cluster.sh status"
alias clogs="~/scripts/cluster.sh logs"
alias cmonitor="~/scripts/cluster.sh monitor"
```

### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `status` | Status do cluster |
| `deploy <stack>` | Deploy de um stack específico |
| `deploy-all` | Deploy todos os stacks |
| `scale <svc> <n>` | Escala serviço para N réplicas |
| `update` | Atualiza todas as imagens |
| `backup [vol]` | Backup de volumes |
| `health` | Health check completo |
| `nodes` | Lista nodes com recursos |
| `drain <node>` | Drena um node |
| `activate <node>` | Ativa um node |
| `update-node <n>` | Atualiza sistema de um node |
| `reboot-node <n>` | Drena e reinicia um node |
| `monitor` | Monitoramento contínuo |
| `logs <svc>` | Logs de um serviço |
| `restart <svc>` | Reinicia um serviço |
| `ps` | Lista containers em todos os nodes |

### Scripts Disponíveis

```
/home/cassiusdjs/scripts/
├── cluster.sh              # Script principal
├── backup/
│   └── backup-volumes.sh   # Backup de volumes
├── deploy/
│   ├── deploy-stack.sh     # Deploy de stack
│   ├── deploy-all.sh       # Deploy todos
│   ├── scale-service.sh    # Escalar serviço
│   └── update-images.sh    # Atualizar imagens
├── health/
│   ├── health-check.sh     # Health check
│   └── manage-nodes.sh     # Gerenciar nodes
└── monitor/
    └── monitor.sh          # Monitoramento contínuo
```

### Exemplos de Uso

```bash
# Health check completo
~/scripts/cluster.sh health

# Monitoramento em tempo real
~/scripts/cluster.sh monitor

# Deploy de stack específico
~/scripts/cluster.sh deploy ardupilot

# Escalar serviço
~/scripts/cluster.sh scale mlpipeline_dask-worker 4

# Atualizar todas as imagens
~/scripts/cluster.sh update

# Ver logs de serviço
~/scripts/cluster.sh logs ardupilot_grafana

# Drenar node para manutenção
~/scripts/cluster.sh drain t630a

# Reativar node
~/scripts/cluster.sh activate t630a

# Backup de volumes
sudo ~/scripts/cluster.sh backup
```

---

_Documentado: 2026-03-10_
_Cluster: Docker Swarm multipropósito_
_Sessão: gateway-client_
_Atualizado: Scripts de automação criados_