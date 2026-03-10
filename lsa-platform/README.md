# LSA Lab Platform

Plataforma web centralizada para gerenciamento do laboratório LSA.

## Características

- **Dashboard Personalizável**: Widgets arrastáveis estilo Power BI
- **Controle de Acesso**: Gerenciamento de porta do laboratório
- **Gerenciamento de Cluster**: Status de nodes e serviços Docker Swarm
- **Terminal Web**: Emulação de terminal no navegador
- **Multi-usuário**: Suporte a múltiplos usuários com níveis de permissão
- **Ambientes Pessoais**: Cada usuário tem seu dashboard personalizado

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  Dashboard │ Door Control │ Terminal │ Admin Panel            │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                           │
│  Auth │ Dashboard │ Door │ Cluster │ Terminal │ Users         │
└─────────────────────────────────────────────────────────────────┘
                              │
┌───────────────┬───────────────┬───────────────┬───────────────┐
│  PostgreSQL   │   Redis       │   MQTT        │   Jetson      │
│  (Users)      │   (Cache)     │   (Events)    │   (Door)      │
└───────────────┴───────────────┴───────────────┴───────────────┘
```

## Recursos Integrados

### Cluster Docker Swarm
| Node | IP | Role |
|------|-----|------|
| T620 | 10.10.20.11 | Manager |
| T630A | 10.10.20.12 | Worker (Compute) |
| T630B | 10.10.20.13 | Worker (Storage) |

### Serviços
- Portainer (9000)
- Grafana (3000)
- InfluxDB (8086)
- PostgreSQL (5432)
- Jupyter (8888)
- MLflow (5001)
- MinIO (9002)
- MQTT (1883)
- Dask (8787)

### Jetson TK2 (Automação)
- IP: 192.168.2.50 (fixo via DHCP reservation)
- MAC: 00:04:4b:8c:e2:aa
- Controle de porta
- GPIO para sensores

## Instalação

### Pré-requisitos
- Docker Swarm configurado
- PostgreSQL, Redis, MQTT rodando
- Node.js 18+ (para build do frontend)
- Python 3.11+ (para backend)

### Deploy Rápido

```bash
# 1. Build do frontend
cd frontend && npm install && npm run build

# 2. Deploy no cluster
./deploy.sh --build
```

### Deploy Manual

```bash
# 1. Copiar arquivos para o manager
scp -r ./* cassiusdjs@10.10.20.11:/home/cassiusdjs/lsa-platform/

# 2. SSH no manager
ssh cassiusdjs@10.10.20.11

# 3. Deploy
cd /home/cassiusdjs/lsa-platform/deploy
sudo docker stack deploy -c docker-compose.yml lsa-platform
```

## Uso

### Acesso
- URL: http://10.10.20.11 ou http://lab.lsa.local
- Admin: admin / lsa@dm1n
- Demo: demo / demo123

### Dashboards Disponíveis
1. **Dashboard Principal**: Status do cluster, métricas, controle de porta
2. **Serviços**: Lista de todos os serviços do cluster
3. **Terminal**: Emulação de terminal (em desenvolvimento)
4. **Usuários**: Gerenciamento de usuários (admin)
5. **Configurações**: Preferências do usuário

### API Endpoints

```
# Auth
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me

# Users (sudo)
GET    /api/users
POST   /api/users
PUT    /api/users/{id}
DELETE /api/users/{id}

# Dashboard
GET    /api/dashboard/widgets
POST   /api/dashboard/widgets
PUT    /api/dashboard/widgets/{id}
DELETE /api/dashboard/widgets/{id}

# Door Control
GET  /api/door/status
POST /api/door/open
POST /api/door/close
GET  /api/door/history

# Cluster
GET  /api/cluster/nodes
GET  /api/cluster/services
GET  /api/cluster/metrics
POST /api/cluster/scale/{service}
```

## Estrutura do Projeto

```
lsa-platform/
├── api/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # React application
│   │   ├── main.tsx         # Entry point
│   │   └── index.css        # Styles
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
├── deploy/
│   ├── docker-compose.yml  # Swarm stack
│   └── nginx.conf          # Nginx configuration
├── deploy.sh               # Deploy script
└── README.md
```

## Desenvolvimento

### Backend

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Testes

```bash
# Backend
cd api
pytest

# Frontend
cd frontend
npm test
```

## Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| DATABASE_URL | PostgreSQL connection | postgresql://...@postgres/platform |
| REDIS_URL | Redis connection | redis://redis:6379 |
| MQTT_BROKER | MQTT broker host | mqtt |
| MQTT_PORT | MQTT port | 1883 |
| JETSON_HOST | Jetson IP | 192.168.2.50 |
| JWT_SECRET | Secret for JWT | lsa-lab-secret-change-in-production |

### Níveis de Usuário

| Nível | Permissões |
|-------|------------|
| sudo | Gerenciamento completo, usuários, configurações |
| user | Dashboard pessoal, controle de porta |

## Integração com Jetson

O backend se comunica com a Jetson TK2 para controle de porta:

```python
# Door control via SSH
async def send_door_command(action: str):
    async with asyncssh.connect(
        settings.jetson_host,
        username=settings.jetson_user,
        password=settings.jetson_pass
    ) as conn:
        result = await conn.run(f"door-control {action}")
        return result.stdout
```

## Segurança

- JWT para autenticação
- Hash bcrypt para senhas
- CORS configurado
- Rate limiting (recomendado para produção)
- HTTPS via Traefik (recomendado para produção)

## Roadmap

- [x] Dashboard básico
- [x] Autenticação JWT
- [x] Controle de porta
- [x] Status do cluster
- [ ] Terminal web completo
- [ ] Integração MQTT em tempo real
- [ ] Dashboards personalizáveis (drag & drop)
- [ ] Notificações push
- [ ] Logs de auditoria
- [ ] Backup automático
- [ ] Multi-idioma
- [ ] Temas (dark/light)
- [ ] API Keys para automação
- [ ] Integração com Grafana
- [ ] Integração com Jupyter
- [ ] Agendamento de tarefas

## Licença

MIT License

## Autores

LSA Lab Platform - OpenClaw Assistant
2026-03-10