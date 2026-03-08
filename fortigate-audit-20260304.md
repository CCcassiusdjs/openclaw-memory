# FortiGate 40F - Auditoria Completa
**Data:** 2026-03-04  
**Hostname:** Firewall-LSA  
**IP de Gerenciamento:** 192.168.1.99/24

---

## 1. Interfaces de Rede

### Hardware Switch (lan)
| Interface | Tipo | IP/Máscara | Status | Descrição |
|-----------|------|-------------|--------|-----------|
| **lan** | Hardware Switch | 192.168.1.99/24 | UP | LAN Principal (hard-switch) |
| └─ lan1 | Physical | — | UP | Porta física (membro do switch) |
| └─ lan2 | Physical | — | UP | WAN Internet (conectado ao modem) |
| └─ lan3 | Physical | — | UP | Switch L2 Trunk (VLANs) |

### Physical Interfaces
| Interface | Tipo | IP/Máscara | Status | Descrição |
|-----------|------|-------------|--------|-----------|
| **a** | Physical | 192.168.2.1/24 | UP | WiFi Router (DataCom Bridge) |
| **wan** | Physical | 0.0.0.0 | DOWN | Porta defeituosa (não usar) |
| **lan2** | Physical | 10.32.162.22/22 | UP | WAN Internet (DHCP do ISP) |
| **lan3** | Physical | — | UP | Switch L2 Trunk (sem IP) |

### VLANs (via lan3 - Switch Trunk)
| VLAN | Nome | IP/Máscara | Alias | Descrição |
|------|------|------------|-------|-----------|
| **10** | VLAN10_IDRAC | 192.168.10.1/24 | IDRAC-MGMT | iDRAC Dell Servers |
| **20** | VLAN20_DATA | 10.10.20.1/24 | CLUSTER-DATA | Cluster PXE Boot |
| **30** | VLAN30_LAN | 192.168.30.1/24 | CORP-LAN | Workstations Corporativas |
| **40** | VLAN40_PERIPHER | 192.168.40.1/24 | INFRA-CRIT | Infra Crítica (Switches/Servidores) |

### Software/Tunnel Interfaces
| Interface | Tipo | IP/Máscara | Status |
|-----------|------|------------|--------|
| wqt.root | Software Switch | 10.253.255.254/20 | UP |
| ssl.root | Tunnel | 0.0.0.0 | UP |
| l2t.root | Tunnel | 0.0.0.0 | DOWN |
| naf.root | Tunnel | 0.0.0.0 | DOWN |

---

## 2. Tabela de Roteamento

```
S*  0.0.0.0/0 [5/0] via 10.32.163.250, lan2    # Default Gateway (ISP)
C   10.10.20.0/24 is directly connected, VLAN20_DATA
C   10.32.160.0/22 is directly connected, lan2  # WAN ISP
C   10.253.240.0/20 is directly connected, wqt.root
C   192.168.1.0/24 is directly connected, lan
C   192.168.2.0/24 is directly connected, a      # WiFi Router
C   192.168.10.0/24 is directly connected, VLAN10_IDRAC
C   192.168.30.0/24 is directly connected, VLAN30_LAN
C   192.168.40.0/24 is directly connected, VLAN40_PERIPHER
S   192.168.80.0/24 [10/0] via 192.168.2.100, a # Rota para DataCom (obsoleta)
```

**⚠️ Nota:** A rota 192.168.80.0/24 é obsoleta (do modo Router do DataCom, agora em Bridge).

---

## 3. Políticas de Firewall

### Resumo das Políticas
| ID | Nome | Origem | Destino | Ação | NAT | Status |
|----|------|--------|---------|------|-----|--------|
| 1-6 | Inter-VLAN | VLANs | VLANs | ACCEPT | ❌ | Ativo |
| 7 | DENY-ALL-LOG | any | any | DENY | ❌ | Ativo (auditoria) |
| 21 | VLAN10-iDRAC-to-WAN | IDRAC-MGMT | WAN-INTERNET | ACCEPT | ✅ | Ativo |
| 22 | VLAN20-Cluster-to-WAN | CLUSTER-DATA | WAN-INTERNET | ACCEPT | ✅ | Ativo |
| 23 | VLAN30-CorpLAN-to-WAN | CORP-LAN | WAN-INTERNET | ACCEPT | ✅ | Ativo |
| 24 | VLAN40-Infra-to-WAN | INFRA-CRIT | WAN-INTERNET | ACCEPT | ✅ | Ativo |
| 25 | AUX-WiFiRouter-to-WAN | WIFI-ROUTER | WAN-INTERNET | ACCEPT | ✅ | Ativo |
| 26 | LAN-to-WAN-Internet | LAN-PRIMARY | WAN-INTERNET | ACCEPT | ✅ | Ativo |

### Inter-VLAN (Políticas 1-6)
| De | Para | Descrição |
|----|------|-----------|
| INFRA-CRIT | DATA-NET | Infra → Cluster |
| INFRA-CRIT | IDRAC-MGMT | Infra → iDRAC |
| INFRA-CRIT | CORP-LAN | Infra → Workstations |
| DATA-NET | INFRA-CRIT | Cluster → Infra |
| IDRAC-MGMT | INFRA-CRIT | iDRAC → Infra |
| CORP-LAN | INFRA-CRIT | Workstations → Infra |

### Política DENY-ALL-LOG
- **Posição:** Última (ID 7)
- **Ação:** DENY
- **Log:** Habilitado
- **Função:** Auditoria de tráfego bloqueado

---

## 4. DHCP Servers

### LAN (lan) - ID 4
| Configuração | Valor |
|--------------|-------|
| Interface | lan |
| Gateway | 192.168.1.99 |
| Netmask | 255.255.255.0 |
| Range | 192.168.1.100 - 192.168.1.200 |
| DNS | Default (FortiGate) |

### WiFi Router (a) - ID 1
| Configuração | Valor |
|--------------|-------|
| Interface | a |
| Gateway | 192.168.2.1 |
| Netmask | 255.255.255.0 |
| Range | 192.168.2.100 - 192.168.2.200 |
| DNS | Default (FortiGate) |
| **Clientes Ativos** | **1** (cassius-laptop: 192.168.2.100) |

### VLANs (sem DHCP configurado)
- VLAN10_IDRAC: ❌ Sem DHCP
- VLAN20_DATA: ❌ Sem DHCP
- VLAN30_LAN: ❌ Sem DHCP
- VLAN40_PERIPHER: ❌ Sem DHCP

---

## 5. Conexões Físicas

### Topologia Atual
```
[ISP Modem] ──lan2──► [FortiGate 40F] ──lan──► [Switch L2] ──lan1──► [Laptop]
                               │
                               ├──a──► [DataCom DM956] (Bridge Mode)
                               │           └── WiFi: LSA2.4GHz / LSA5GHz
                               │
                               └──lan3──► [Switch L2 Trunk]
                                              ├── VLAN10 (iDRAC)
                                              ├── VLAN20 (Cluster)
                                              ├── VLAN30 (Corp LAN)
                                              └── VLAN40 (Infra Crítica)
```

### Status das Portas
| Porta | Conexão | Status | Velocidade |
|-------|---------|--------|------------|
| wan | — | DOWN | N/A (defeituosa) |
| lan1 | Laptop | UP | — |
| lan2 | ISP Modem | UP | 1Gbps |
| lan3 | Switch L2 Trunk | UP | 1Gbps |
| a | DataCom DM956 | UP | — |

---

## 6. Configurações WiFi (DataCom DM956)

### Modo: Bridge
- **Função:** Access Point (sem NAT)
- **Porta utilizada:** LAN (não WAN)
- **Conectado a:** FortiGate porta "a"

### SSIDs Ativos
| Band | SSID | Canal | Status |
|------|------|-------|--------|
| 2.4GHz | LSA2.4GHz | 6 | Ativo |
| 5GHz | LSA5GHz | 36 | Ativo |

### DHCP
- **Fonte:** FortiGate (192.168.2.1)
- **Range:** 192.168.2.100-200

---

## 7. Recomendações

### ⚠️ Problemas Identificados

1. **Rota Obsoleta**: `192.168.80.0/24 via 192.168.2.100` deve ser removida (DataCom agora em Bridge)

2. **VLANs sem DHCP**: VLANs 10, 20, 30, 40 não têm DHCP configurado

3. **Porta WAN Defeituosa**: A porta física `wan` está down (hardware)

### ✅ Configurações Corretas

1. **Firewall Policies**: Todas as inter-VLAN e WAN estão configuradas corretamente

2. **NAT**: Habilitado apenas para saída WAN (correto)

3. **Logging**: DENY-ALL-LOG habilitado para auditoria

4. **DHCP na LAN e WiFi**: Funcionando corretamente

---

## 8. Próximos Passos

1. **Remover rota obsoleta:**
   ```
   config router static
   delete 1
   end
   ```

2. **Configurar DHCP nas VLANs** (se necessário)

3. **Verificar se VLANs precisam de DHCP** (iDRAC geralmente usa IP estático)

---

**Auditoria realizada em:** 2026-03-04 12:50  
**Ferramenta:** FortiGate Web UI + CLI via Serial