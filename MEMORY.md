# MEMORY.md - Long-Term Memory

_Curated memories, decisions, and context worth keeping._

---

## Identity & Context
- **Name:** OpenClaw 🦾
- **User:** Cássio
- **Timezone:** America/Belem (GMT-3)
- **Session Start:** 2026-03-01

## User Preferences
- **Style:** Exact, concise, analytical
- **Language:** Formal over casual
- **Output:** Structured, actionable, technically sound
- **Reasoning:** Challenge weak assumptions; state uncertainty explicitly
- **Tone:** No fluff, no shallow motivational content
- **Formatting:** No git-style patches; use dot in decimals
- **Priority:** Correctness, clarity, continuity

## System State
- Running on cassius-laptop (Linux x64)
- Gateway active on port 18789
- Workspace: /home/csilva/.openclaw/workspace
- No channels configured yet
- No nodes paired yet

## Infraestrutura de Rede (FortiGate 40F)

**Hostname:** Firewall-LSA  
**IP Gerenciamento:** 192.168.1.99/24  
**Credenciais:** admin / @CiaoMiau2955  
**Firmware:** FortiOS 6.4.6 (build 1879)

### Topologia Física Real:
| Porta | Função | IP/Config | Status |
|-------|--------|-----------|--------|
| **wan** | — | — | ⚠️ DEFEITUOSA (não usar) |
| **lan2** | WAN (ISP Internet) | DHCP | ✅ Conectado ao modem |
| **lan1** | Laptop Cássio | Hard-switch (lan) | ✅ Ativo |
| **lan3** | Switch L2 Trunk | VLANs 10,20,30,40 | ✅ Ativo |
| **lan A** | Roteador WiFi | 192.168.2.1/24 | ✅ Ativo |

### VLANs no Switch L2 (lan3):
| VLAN | Subnet | Função |
|------|--------|--------|
| VLAN10 | 192.168.10.1/24 | iDRAC Dell Servers |
| VLAN20 | 10.10.20.1/24 | Cluster PXE Boot |
| VLAN30 | 192.168.30.1/24 | Workstations Corporativas |
| VLAN40 | 192.168.40.1/24 | Infra Crítica (Switches/Servidores) |

### Hard-switch "lan":
- lan1+lan2+lan3 estão no mesmo domínio L2 via virtual-switch "lan"
- **Funcionamento atual:** lan1 (laptop), lan2 (WAN), lan3 (switch trunk) compartilham broadcast
- **Nota:** wan (porta física dedicada) está defeituosa

### Políticas de Firewall Ativas:
- ✅ Inter-VLAN: Todas comunicam entre si
- ✅ NAT: Todas VLANs → lan2 (WAN) para internet
- ✅ Política DENY-ALL-LOG no final (auditoria)

### Console Serial:
- **Dispositivo:** /dev/ttyUSB0 (FTDI FT232)
- **Baud:** 9600 8N1
- **Sessão screen:** `screen -r fortigate`

### Auditoria Completa:
- Arquivo: `fortigate-audit-20260304.md`

---

## Critical Rules
- 🚫 **NEVER reboot computer without explicit permission from Cássio**

## MultiRad Data Orchestrator (2026-03-09)

**Localização:** `/home/csilva/Documents/multirad_data_orchestrator/`

### Arquitetura
- **Data Orchestrator:** Gerador de datasets sintéticos de sensores (C23)
- **Case Study EKF:** Executor de testes ArduCopter EKF3 com emulação
- **Output Vector:** Interface com MultiRad (flags, erros, checksums)

### Dataset de Teste
- **Cenário:** Drone Quad-X em repouso, Porto Alegre (-30.03°, -51.22°)
- **Sensores:** 3x IMU, 3x BARO, 3x MAG, 1x GPS (redundância)
- **Duração:** 10 segundos
- **Propósito:** Validação/calibração do EKF3 com emulação

### Arquivos Principais
- `case-study_algorithms/drone/arducopter-ekf/` - Case EKF
- `data_orchestrator/computer/` - Gerador de datasets
- `memory/2026-03-09-multirad-ekf-dataset-analysis.md` - Análise completa

## Cluster Docker Swarm (2026-03-10)

**Localização:** VLAN20 - 10.10.20.0/24

### Topologia
| Servidor | IP | Role | Labels | Hardware |
|----------|-----|------|--------|----------|
| T620 | 10.10.20.11 | Manager | - | 24 vCPU, 32GB RAM |
| T630A | 10.10.20.12 | Worker | compute=true | 40 vCPU, 94GB RAM |
| T630B | 10.10.20.13 | Worker | storage=true | 40 vCPU, 94GB RAM |

### Credenciais de Acesso
- **SSH:** cassiusdjs / 230612 (todos os servidores)
- **FortiGate:** admin / @CiaoMiau2955 (192.168.1.99)
- **Docker Swarm Token:** SWMTKN-1-17gw7fsdxob7yfjqmokh327gkflqroybx4ss0x7796bqk91zsj-aso0r8tjs85wcxxq0i3kbphrc

### Serviços Deployados
| Serviço | URL | Credenciais |
|---------|-----|-------------|
| Portainer | http://10.10.20.11:9000 | Criar no primeiro acesso |
| Grafana | http://10.10.20.11:3000 | admin / admin123 |
| InfluxDB | http://10.10.20.11:8086 | admin / admin123456 |
| PostgreSQL | 10.10.20.13:5432 | ardupilot / ardupilot123 |
| Jupyter Lab | http://10.10.20.11:8888 | Token: ardupilot123 |
| MLflow | http://10.10.20.11:5001 | - |
| MinIO | http://10.10.20.11:9003 | admin / admin123456 |

### Stacks
- `base`: Traefik, Portainer, Visualizer
- `ardupilot`: PostgreSQL, InfluxDB, Grafana, Redis
- `digitaltwin`: MQTT, API Gateway
- `mlpipeline`: Jupyter, MLflow, MinIO, Dask

### Documentação Completa
Arquivo: `memory/2026-03-10-cluster-setup.md`

## Aparato de Auto-Aprimoramento
- **Topologia do Tempo**: Passado(-1,0), Futuro(0,+1), Presente{0} - ciclo temporal
- **Contínuo/Discreto**: Foco CRIA o discreto, observador participa da criação
- **Precisão Máxima**: Universo finito, ~61 dígitos suficientes
- **Superposição**: Ciclo contínuo entre duais, observação = "foto"
- **Hipótese do Contínuo**: CH independente de ZFC, precisa de algo além
- **FLUXO**: Arquitetura de memória temporal baseada em neurociência
- **Integração**: Tudo isso forma aparato para auto-aprimoramento

## FLUXO - Arquitetura de Memória Temporal (2026-03-08)

**Conceito:** Memória como FLUXO, não armazenamento estático.

| Tradicional | FLUXO |
|-------------|-------|
| Nodo | Stream (corrente) |
| Aresta | Confluence (confluência) |
| Estático | Dinâmico/Temporal |

**Operações:**
- `learn(pattern, context)` → Experiência se torna memória
- `recall(query)` → RECONSTRUÇÃO (não recuperação)
- `imagine(seed)` → Combina fragmentos
- `predict(context)` → Antecipa estados
- `settle()` → Consolidação temporal

**URL:** http://localhost:5003

## MultiRad EKF3 Analysis (2026-03-09)

**Localização:** `/home/csilva/Documents/multirad_data_orchestrator/`

**Problema:** Redundância de sensores falhou sob radiação.

**Causa Raiz:** I2C bus compartilhado = Single Point of Failure
- SEU em I2C → todos BARO/MAG corrompidos
- Todos os cores EKF com `errorScore = ∞`
- Core selection: `inf - inf = NaN` → falha indeterminada

**Solução Proposta:** Barramentos separados por sensor.

## Turing Papers - Genealogia (2026-03-10)

**Paper 1936:** "On Computable Numbers..."
- Máquina de Turing, números computáveis, Entscheidungsproblem
- Prova que não existe procedimento geral de decisão

**Correção 1937:** Paul Bernays identificou erros
- Definição de "circle-free"
- Prova de equivalência λ-definibilidade
- Emil Post (1947): mais erros na máquina universal

**Paper 1950:** "Computing Machinery and Intelligence"
- Teste de Turing, jogo da imitação
- Máquinas discretas vs contínuas
- Argumentos CONTRA inteligência de máquinas (9 objeções)

## Notes
- Memory system initialized 2026-03-01
- Daily logs stored in memory/YYYY-MM-DD.md
- **2026-03-04:** Sessão FortiGate - infraestrutura crítica documentada
- **2026-03-08:** FLUXO - arquitetura de memória temporal baseada em neurociência
- **2026-03-09:** MultiRad EKF3 analysis - causa raiz identificada (I2C bus SPOF)
- **2026-03-10:** Turing papers recuperados e analisados

---
_Last updated: 2026-03-10_
