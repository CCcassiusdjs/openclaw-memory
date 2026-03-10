# LSA Lab Platform - Arquitetura

## Visão Geral

Plataforma web centralizada para gerenciamento do laboratório LSA, oferecendo:
- Dashboard personalizável estilo Power BI
- Controle de acesso físico (porta)
- Gerenciamento de recursos do cluster
- Terminal web embutido
- Ambientes pessoais por usuário

---

## Recursos Disponíveis

### Cluster Docker Swarm (VLAN20)
| Recurso | IP | Função |
|---------|-----|--------|
| T620 (Manager) | 10.10.20.11 | Traefik, Portainer, Grafana, Redis, MQTT, MLflow, Dask |
| T630A (Compute) | 10.10.20.12 | Jupyter, Dask Workers |
| T630B (Storage) | 10.10.20.13 | PostgreSQL, InfluxDB, MinIO |

### Serviços
| Serviço | Porta | URL |
|---------|-------|-----|
| Portainer | 9000 | http://10.10.20.11:9000 |
| Grafana | 3000 | http://10.10.20.11:3000 |
| InfluxDB | 8086 | http://10.10.20.11:8086 |
| PostgreSQL | 5432 | 10.10.20.13:5432 |
| Jupyter | 8888 | http://10.10.20.11:8888 |
| MLflow | 5001 | http://10.10.20.11:5001 |
| MinIO | 9002 | http://10.10.20.11:9002 |
| MQTT | 1883 | 10.10.20.11:1883 |
| Dask | 8787 | http://10.10.20.11:8787 |
| API Gateway | 5000 | http://10.10.20.11:5000 |

### Jetson TK2 (Automação)
| Campo | Valor |
|-------|-------|
| IP Atual | 192.168.2.117 |
| IP Fixo | 192.168.2.50 |
| MAC | 00:04:4b:8c:e2:aa |
| Usuário | automation |
| Senha | automation |
| Função | Controle de porta, automação |
| GPIO | 5 gpiochips disponíveis |
| Serviço | door-access.service (Flask) |

### FortiGate (Firewall)
| Campo | Valor |
|-------|-------|
| IP | 192.168.2.1 |
| Usuário | admin |
| Senha | @CiaoMiau2955 |

---

## Arquitetura da Plataforma

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LSA LAB PLATFORM                             │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     FRONTEND (React/Vue)                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │   │
│  │  │ Dashboard│ │  Door    │ │ Terminal │ │  Admin   │       │   │
│  │  │ (PowerBI)│ │  Control │ │   Web    │ │  Panel   │       │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     API GATEWAY (FastAPI)                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │   │
│  │  │  Auth    │ │  Proxy   │ │  MQTT    │ │  WS      │       │   │
│  │  │  Module  │ │  Module  │ │  Client  │ │  Server  │       │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     DATABASE LAYER                           │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                     │   │
│  │  │PostgreSQL│ │ InfluxDB │ │  Redis   │                     │   │
│  │  │ (Users,  │ │ (Metrics)│ │ (Cache)  │                     │   │
│  │  │  Config) │ │          │ │          │                     │   │
│  │  └──────────┘ └──────────┘ └──────────┘                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  JETSON TK2   │    │ DOCKER SWARM  │    │   FORTIGATE   │
│  (Door Ctrl)  │    │   (Cluster)   │    │   (Firewall)  │
│               │    │               │    │               │
│ - Door Lock   │    │ - Containers  │    │ - VLANs       │
│ - GPIO        │    │ - Services     │    │ - Policies    │
│ - Sensors     │    │ - Logs        │    │ - DHCP        │
└───────────────┘    └───────────────┘    └───────────────┘
```

---

## Módulos da Plataforma

### 1. Dashboard Principal (Power BI Style)
- Widgets arrastáveis e redimensionáveis
- Painéis personalizáveis por usuário
- Métricas em tempo real (CPU, RAM, Disco, Network)
- Status dos serviços do cluster
- Gráficos de uso de recursos

### 2. Controle de Acesso (Door)
- Botão para abrir/fechar porta
- Status atual da porta (aberto/fechado)
- Histórico de acessos
- Lockout de 10s após abertura
- Integração com leitor de cartão RFID

### 3. Terminal Web
- xterm.js para emulação de terminal
- Acesso SSH aos servidores
- Acesso ao console do Docker
- Histórico de comandos

### 4. Gerenciamento de Cluster
- Status dos nodes
- Status dos serviços
- Logs em tempo real
- Escalonamento de serviços
- Deploy de stacks

### 5. Painel de Admin (sudo)
- Gerenciamento de usuários
- Configurações do sistema
- Backup/Restore
- Auditoria de ações

### 6. Ambiente Pessoal
- Workspaces individuais
- Configurações pessoais
- Dashboards salvos
- Preferências de tema

---

## Tecnologias

### Frontend
- **Framework**: React 18 + TypeScript
- **UI Library**: Material-UI ou Ant Design
- **Dashboard**: React-Grid-Layout (drag & drop)
- **Charts**: Recharts ou Apache ECharts
- **Terminal**: xterm.js
- **State**: Zustand ou Redux Toolkit

### Backend
- **Framework**: FastAPI (Python)
- **Auth**: JWT + OAuth2
- **Database**: PostgreSQL (users, config) + InfluxDB (metrics)
- **Cache**: Redis
- **WebSocket**: FastAPI WebSocket
- **MQTT**: paho-mqtt

### Infraestrutura
- **Container**: Docker Swarm
- **Reverse Proxy**: Traefik
- **SSL**: Let's Encrypt (opcional)
- **Monitoring**: Prometheus + Grafana

---

## Modelos de Dados

### User
```python
class User:
    id: UUID
    username: str
    email: str
    password_hash: str
    role: str  # "sudo" | "user"
    environment: JSON  # Dashboard config
    created_at: datetime
    last_login: datetime
```

### Dashboard Widget
```python
class Widget:
    id: UUID
    user_id: UUID
    type: str  # "metric" | "chart" | "terminal" | "door" | "service"
    position: dict  # {x, y, w, h}
    config: JSON  # Widget-specific config
    created_at: datetime
```

### Access Log
```python
class AccessLog:
    id: UUID
    user_id: UUID
    action: str  # "door_open" | "door_close" | "login" | ...
    timestamp: datetime
    details: JSON
```

---

## APIs

### Auth
```
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
POST /api/auth/refresh
```

### Users (sudo)
```
GET    /api/users
POST   /api/users
GET    /api/users/{id}
PUT    /api/users/{id}
DELETE /api/users/{id}
```

### Dashboard
```
GET    /api/dashboard/widgets
POST   /api/dashboard/widgets
PUT    /api/dashboard/widgets/{id}
DELETE /api/dashboard/widgets/{id}
```

### Door Control
```
GET  /api/door/status
POST /api/door/open
POST /api/door/close
GET  /api/door/history
```

### Cluster
```
GET  /api/cluster/nodes
GET  /api/cluster/services
GET  /api/cluster/metrics
POST /api/cluster/scale/{service}
GET  /api/cluster/logs/{service}
```

### Terminal (WebSocket)
```
WS /api/terminal/connect
```

---

## Fluxo de Autenticação

1. Usuário acessa plataforma
2. Login com username/password
3. Backend valida e gera JWT
4. Frontend armazena JWT
5. Requests subsequentes incluem JWT
6. Middleware valida JWT e injeta user
7. Verifica permissões (sudo/user)

---

## Deploy no Cluster

### Stack: lsa-platform

```yaml
services:
  # Frontend (React)
  frontend:
    image: nginx:alpine
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
    networks:
      - cluster-network
    deploy:
      placement:
        constraints:
          - node.role == manager

  # Backend API (FastAPI)
  api:
    image: python:3.11-slim
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    volumes:
      - ./api:/app
    networks:
      - cluster-network
    environment:
      - DATABASE_URL=postgresql://ardupilot:ardupilot123@postgres/platform
      - REDIS_URL=redis://redis:6379
      - MQTT_BROKER=mqtt://mqtt:1883
    deploy:
      placement:
        constraints:
          - node.role == manager

  # PostgreSQL (extend existing)
  # Redis (extend existing)
  # MQTT (extend existing)
```

---

## Próximos Passos

1. [x] Mapear recursos da rede
2. [x] Configurar IP fixo para Jetson
3. [ ] Criar repositório do projeto
4. [ ] Implementar backend (FastAPI)
5. [ ] Implementar frontend (React)
6. [ ] Integrar com Jetson (porta)
7. [ ] Integrar com cluster (Docker)
8. [ ] Deploy no cluster
9. [ ] Testes e documentação

---

_Documentado: 2026-03-10_
_Arquitetura: LSA Lab Platform_