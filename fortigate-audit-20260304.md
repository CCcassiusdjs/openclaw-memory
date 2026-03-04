# FortiGate 40F - Auditoria Completa
**Data:** 2026-03-04 09:29 GMT-3
**Serial:** FGT40FTK2309DUMZ
**Hostname:** Firewall-LSA
**Firmware:** FortiOS 6.4.6 (build 1879)

---

## 1. Status do Sistema

| Campo | Valor |
|-------|-------|
| **Hostname** | Firewall-LSA |
| **Alias** | FortiGate-40F |
| **Serial** | FGT40FTK2309DUMZ |
| **BIOS** | 05000030 |
| **Operation Mode** | NAT |
| **HA Mode** | Standalone |
| **Virtual Domains** | 1 (root) |
| **Timezone** | 18 |
| **Switch Controller** | Enabled |

---

## 2. Interfaces Físicas

### Portas e Status

| Porta | Status | Modo | IP/Config | Descrição |
|-------|--------|------|-----------|-----------|
| **wan** | DOWN | DHCP | 0.0.0.0 | ⚠️ DEFEITUOSA - Não usar |
| **lan2** | UP (1000Mbps Full) | DHCP | 10.32.162.22/22 | ✅ WAN Secundária (ISP Internet) |
| **lan3** | UP (1000Mbps Full) | Static | 0.0.0.0 (Trunk) | ✅ Switch L2 Trunk |
| **lanA** | — | — | — | Roteador WiFi (porta auxiliar) |
| **lan1** | — | — | — | ⚠️ Hard-switch ativo (ver nota) |

### Detalhes por Interface

#### wan (Porta Física)
- Status: DOWN
- Problema: **Porta defeituosa - não usar**

#### lan2 (WAN Ativa)
- Status: UP, 1000Mbps Full Duplex
- IP: 10.32.162.22/22 (DHCP)
- Gateway: 10.32.163.250
- Função: **Conexão ISP Internet**

#### lan3 (Switch Trunk)
- Status: UP, 1000Mbps Full Duplex
- IP: 0.0.0.0 (interface física, sem IP)
- Descrição: "PORT3 - L2 Switch Trunk (VLANs 10,20,30,40)"
- Alias: SWITCH-TRUNK
- Acesso: ping, https, ssh, snmp, http, fgfm, radius-acct, fabric, ftm
- VLANs: 10, 20, 30, 40

#### Virtual Switch "lan"
- Porta física: sw0
- Portas membros: **apenas lan1**
- Problema: Hard-switch ativo agrupa lan1+lan2+lan3

---

## 3. VLANs e Sub-redes

| VLAN ID | Nome | Sub-rede | Gateway | Função |
|---------|------|----------|---------|--------|
| VLAN 10 | VLAN10_IDRAC | 192.168.10.0/24 | 192.168.10.1 | iDRAC Dell Servers |
| VLAN 20 | VLAN20_DATA | 10.10.20.0/24 | 10.10.20.1 | Cluster PXE Boot |
| VLAN 30 | VLAN30_LAN | 192.168.30.0/24 | 192.168.30.1 | Workstations Corporativas |
| VLAN 40 | VLAN40_PERIPHER | 192.168.40.0/24 | 192.168.40.1 | Infra Crítica (Switches/Servidores) |

### Interface "a" (WiFi Router)
- Sub-rede: 192.168.2.0/24
- Gateway: 192.168.2.1
- DHCP Range: 192.168.2.100-200
- Rota estática: 192.168.80.0/24 via 192.168.2.100

### Interface "lan" (Hard-switch)
- Sub-rede: 192.168.1.0/24
- Status: Conectado ao virtual-switch

### Quarantine VLAN
- Nome: wqtn.11.default
- VLAN ID: 4093
- Security Mode: Captive Portal

---

## 4. DHCP Servers

| Interface | Gateway | Range | Notas |
|-----------|---------|-------|-------|
| VLAN20_DATA | 10.10.20.1 | 10.10.20.100-200 | PXE Boot: pxelinux.0 |
| a | 192.168.2.1 | 192.168.2.100-200 | WiFi Router |

---

## 5. Políticas de Firewall

### Inter-VLAN (Tráfego Interno)

| ID | Nome | Origem | Destino | Ação | NAT |
|----|------|--------|---------|------|-----|
| 3 | INFRA-CRIT to IDRAC-MGMT | VLAN40_PERIPHER | VLAN10_IDRAC | ACCEPT | No |
| 4 | INFRA-CRIT to CORP-LAN | VLAN40_PERIPHER | VLAN30_LAN | ACCEPT | No |
| 5 | DATA-NET to INFRA-CRIT | VLAN20_DATA | VLAN40_PERIPHER | ACCEPT | No |
| 6 | IDRAC-MGMT to INFRA-CRIT | VLAN10_IDRAC | VLAN40_PERIPHER | ACCEPT | No |
| 7 | CORP-LAN to INFRA-CRIT | VLAN30_LAN | VLAN40_PERIPHER | ACCEPT | No |

### Saída para Internet (NAT)

| ID | Nome | Origem | Destino | Ação | NAT |
|----|------|--------|---------|------|-----|
| 21 | VLAN10-iDRAC-to-WAN-Internet | VLAN10_IDRAC | lan2 | ACCEPT | Yes |
| 22 | VLAN20-Cluster-to-WAN-Internet | VLAN20_DATA | lan2 | ACCEPT | Yes |
| 23 | VLAN30-CorpLAN-to-WAN-Internet | VLAN30_LAN | lan2 | ACCEPT | Yes |
| 24 | VLAN40-Infra-to-WAN-Internet | VLAN40_PERIPHER | lan2 | ACCEPT | Yes |
| 25 | AUX-WiFiRouter-to-WAN-Internet | a | lan2 | ACCEPT | Yes |

### Política Final (Auditoria)

| ID | Nome | Origem | Destino | Ação | Notas |
|----|------|--------|---------|------|-------|
| 999 | DENY-ALL-LOG | any | any | DENY | Log para auditoria |

---

## 6. Roteamento

```
S*  0.0.0.0/0 [5/0] via 10.32.163.250, lan2    (Default Gateway)
C   10.10.20.0/24 is directly connected, VLAN20_DATA
C   10.32.160.0/22 is directly connected, lan2
C   10.253.240.0/20 is directly connected, wqt.root
C   192.168.1.0/24 is directly connected, lan
C   192.168.2.0/24 is directly connected, a
C   192.168.10.0/24 is directly connected, VLAN10_IDRAC
C   192.168.30.0/24 is directly connected, VLAN30_LAN
C   192.168.40.0/24 is directly connected, VLAN40_PERIPHER
S   192.168.80.0/24 [10/0] via 192.168.2.100, a
```

---

## 7. DNS e NTP

### DNS
```
Primary:   96.45.45.45
Secondary: 96.45.46.46
```

### NTP
- NTP Sync: Enabled
- Server Mode: Enabled
- Interfaces: lan2, lan, lan3

---

## 8. Problemas Identificados

### ⚠️ CRÍTICO: Hard-switch "lan"
- O virtual-switch "lan" agrupa fisicamente as portas lan1+lan2+lan3
- **Problema:** Isso impede o uso independente de lan1
- **Solução:** Remover hard-switch via console serial para usar lan1 como porta independente

### ⚠️ Porta WAN Defeituosa
- Porta "wan" está DOWN
- Recomendação: Usar lan2 como WAN primária (já configurado)

### 🔧 Configuração Pendente
- lan1 está no hard-switch mas não tem interface L3 própria
- Para usar lan1 como porta de manutenção independente, é necessário:
  1. Remover do virtual-switch via console serial
  2. Criar interface L3 separada

---

## 9. Recomendações

1. **Backup Regular:** Configurar backup automático da configuração
2. **Hard-switch:** Avaliar remoção do hard-switch para usar lan1 independentemente
3. **Documentação:** Atualizar diagrama de rede com topologia atual
4. **Monitoramento:** Configurar SNMP para monitoramento externo

---

## 10. Endereços Configurados

| Nome | IP | Tipo |
|------|-----|------|
| VLAN20_DATA address | 10.10.20.1/24 | interface-subnet |
| VLAN30_LAN address | 192.168.30.1/24 | interface-subnet |
| VLAN40_PERIPHER address | 192.168.40.1/24 | interface-subnet |
| SWITCH-L2-CRITICO | 192.168.40.2/32 | host (Switch de infraestrutura) |

---

**Auditoria concluída em:** 2026-03-04
**Console:** /dev/ttyUSB0 (FTDI FT232 Serial)
**Conexão:** 9600 8N1