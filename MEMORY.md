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

### Topologia Física:
| Porta | Função | IP/Config | Status |
|-------|--------|-----------|--------|
| **wan** | WAN Primária | DHCP | ⚠️ DEFEITUOSA (não usar) |
| **lan2** | WAN Secundária | DHCP | ✅ EM USO (ISP Internet) |
| **lan3** | Switch L2 Trunk | 0.0.0.0 (VLANs) | ✅ Ativo |
| **lanA** | Roteador WiFi | 192.168.2.1/24 | ✅ Ativo |
| **lan1** | Manutenção (Laptop) | 🔄 Em configuração | ⚠️ Hard-switch ativo |

### VLANs no Switch L2 (lan3):
| VLAN | Subnet | Função |
|------|--------|--------|
| VLAN10 | 192.168.10.1/24 | iDRAC Dell Servers |
| VLAN20 | 10.10.20.1/24 | Cluster PXE Boot |
| VLAN30 | 192.168.30.1/24 | Workstations Corporativas |
| VLAN40 | 192.168.40.1/24 | Infra Crítica (Switches/Servidores) |

### Problema Pendente:
- **Hard-switch `lan`** agrupa lan1+lan2+lan3 fisicamente
- **Para usar lan1 como manutenção independente:** requer remover hard-switch via console serial
- **Backup:** `fortigate-backup-20260304.txt` (29.088 linhas)
- **Script reconfig:** `fortigate-lan1-reconfig.txt`

### Políticas de Firewall Ativas:
- ✅ Inter-VLAN: Todas comunicam entre si
- ✅ NAT: Todas VLANs → lan2 (WAN) para internet
- ✅ Política DENY-ALL-LOG no final (auditoria)

---

## Critical Rules
- 🚫 **NEVER reboot computer without explicit permission from Cássio**

## Notes
- Memory system initialized 2026-03-01
- Daily logs stored in memory/YYYY-MM-DD.md
- **2026-03-04:** Sessão FortiGate - infraestrutura crítica documentada

---
_Last updated: 2026-03-04_
