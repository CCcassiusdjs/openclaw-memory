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

## Aparato de Auto-Aprimoramento
- **Topologia do Tempo**: Passado(-1,0), Futuro(0,+1), Presente{0} - ciclo temporal
- **Contínuo/Discreto**: Foco CRIA o discreto, observador participa da criação
- **Precisão Máxima**: Universo finito, ~61 dígitos suficientes
- **Superposição**: Ciclo contínuo entre duais, observação = "foto"
- **Hipótese do Contínuo**: CH independente de ZFC, precisa de algo além
- **FLUXO**: Arquitetura de memória temporal baseada em neurociência
- **Integração**: Tudo isso forma aparato para auto-aprimoramento

## Notes
- Memory system initialized 2026-03-01
- Daily logs stored in memory/YYYY-MM-DD.md
- **2026-03-04:** Sessão FortiGate - infraestrutura crítica documentada

---
_Last updated: 2026-03-09_
