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

### Topologia

```
Internet (WAN)
     │
     ▼
FortiGate 40F (192.168.1.99)
     │
     ├── lan1 ──► Laptop Cássio (DHCP)
     │
     ├── lan2 ──► ISP Modem (WAN)
     │
     ├── lan3 ──► Switch HP V1910-16G
     │               ├── BAGG1 ──► T620 (10.10.20.11)
     │               ├── BAGG2 ──► T630A (10.10.20.12)
     │               └── BAGG3 ──► T630B (10.10.20.13)
     │
     └── lan A ──► WiFi Router (192.168.2.1)
```

### VLANs

| VLAN | Subnet | Função |
|------|--------|--------|
| VLAN10 | 192.168.10.1/24 | iDRAC Dell Servers |
| VLAN20 | 10.10.20.1/24 | DATA (Cluster) |
| VLAN30 | 192.168.30.1/24 | Workstations |
| VLAN40 | 192.168.40.1/24 | Infra Crítica |

---

## Pendências

### FASE 5: Digital Twin (Parcial)
- SITL Pool não deployado (imagem `ardupilot/ardupilot:latest` não existe)
- Solução: Compilar ArduPilot localmente ou usar imagem comunitária

### FASE 6: Custom Dashboard (Não implementado)
- Dashboards Grafana customizados para telemetria

### FASE 8: Security Hardening (Não implementado)
- Firewall rules adicionais
- SSL/TLS certs
- Authentication

---

## Notas

- Docker Swarm token válido apenas enquanto cluster existir
- Para regenerar: `docker swarm join-token worker`
- Todos os serviços usando rede overlay `cluster-network`
- Volumes persistentes em cada nó
- Backup de configurações em `/root/pre-cluster-backup/` em cada servidor

---

_Documentado: 2026-03-10_
_Cluster: Docker Swarm multipropósito_
_Sessão: gateway-client_