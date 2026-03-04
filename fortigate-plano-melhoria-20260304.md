# FortiGate 40F - Plano de Melhoria (Recursos Locais Gratuitos)

**Data:** 2026-03-04
**Firmware:** FortiOS 6.4.6 (build 1879)
**Restrição:** Sem licença FortiGuard, sem atualização de firmware

---

## Recursos DISPONÍVEIS Sem Licença

De acordo com a documentação Fortinet e comunidade, os seguintes recursos funcionam **sem necessidade de licença**:

| Recurso | Status | Notas |
|---------|--------|-------|
| ✅ Firewall Policies | Gratuito | Todas as políticas de firewall |
| ✅ NAT / PAT | Gratuito | Network Address Translation |
| ✅ VLANs / Routing | Gratuito | VLANs, routing estático e dinâmico |
| ✅ IPsec VPN | Gratuito | Túneis ilimitados |
| ✅ SSL VPN | Gratuito | Sem restrição de licença |
| ✅ Local Logging (Memory) | Gratuito | Logs em memória RAM |
| ✅ Syslog Export | Gratuito | Envio para servidor externo |
| ✅ Traffic Shaping / QoS | Gratuito | Controle de bandwidth |
| ✅ DDNS (FortiGuard) | Gratuito | Dynamic DNS sem licença |
| ✅ Local-in Policies | Gratuito | Proteção do próprio FortiGate |
| ✅ DHCP Server | Gratuito | Todas as funções DHCP |
| ✅ DNS Server/Forwarder | Gratuito | DNS local |
| ✅ NetFlow / sFlow | Gratuito | Export de flows |
| ✅ GRE / VXLAN | Gratuito | Encapsulamento |
| ✅ VRF | Gratuito | Virtual Routing |
| ✅ SD-WAN Básico | Gratuito | Sem features avançadas |
| ⚠️ IPS/AV/App Control | Limitado | Funciona mas com assinaturas antigas |

---

## FASE 1: CORREÇÕES CRÍTICAS (Imediato)

### 1.1 Criar Política LAN → WAN

**Problema:** Interface "lan" (192.168.1.99/24) não tem política para sair pela Internet.

**Solução:**
```
config firewall policy
    edit 26
        set name "LAN-to-WAN-Internet"
        set srcintf "lan"
        set dstintf "lan2"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic all
        set nat enable
    next
end
```

### 1.2 Configurar DHCP na Interface LAN

**Problema:** Sem DHCP server na interface "lan".

**Solução:**
```
config system dhcp server
    edit 4
        set dns-service default
        set default-gateway 192.168.1.99
        set netmask 255.255.255.0
        set interface "lan"
        config ip-range
            edit 1
                set start-ip 192.168.1.100
                set end-ip 192.168.1.200
            next
        end
    next
end
```

---

## FASE 2: HARDENING DE SEGURANÇA (Esta Semana)

### 2.1 Local-in Policies (Proteção do FortiGate)

Proteger o próprio FortiGate de acessos não autorizados:

```
config firewall local-in-policy
    edit 1
        set intf "lan2"
        set srcaddr "all"
        set dstaddr "all"
        set service "ALL"
        set schedule "always"
        set action deny
    next
    edit 2
        set intf "lan2"
        set srcaddr "all"
        set dstaddr "all"
        set service "PING"
        set schedule "always"
        set action accept
    next
end
```

### 2.2 Restringir Acesso Administrativo

**Atual:** lan2 tem muitos serviços habilitados (ping, https, ssh, snmp, http, fgfm, radius-acct, fabric, ftm)

**Recomendado:** Limitar a HTTPS e SSH:

```
config system interface
    edit "lan2"
        set allowaccess https ssh
    next
    edit "lan3"
        set allowaccess https ssh ping
    next
end
```

### 2.3 Configurar Trusted Hosts para Admin

Limitar acesso administrativo a IPs específicos:

```
config system admin
    edit "admin"
        set trusted-host1 192.168.1.0/24
        set trusted-host2 192.168.40.0/24
    next
end
```

### 2.4 Desabilitar Serviços Desnecessários

```
config system global
    set admin-scp disable
    set admintimeout 10
end

config system settings
    set gui-allow-unsafe-encryption-ciphers disable
end
```

---

## FASE 3: LOGGING E MONITORAMENTO (Esta Semana)

### 3.1 Configurar Logging em Memória

```
config log memory global-setting
    set status enable
end

config log memory setting
    set status enable
end
```

### 3.2 Configurar Syslog Externo (se houver servidor)

```
config log syslogd setting
    set status enable
    set server [IP-SYSLOG-SERVER]
    set port 514
    set format rfc5424
end
```

### 3.3 Logs Detalhados nas Políticas

Já configurado com `set logtraffic all` nas políticas existentes. Verificar se está ativo.

---

## FASE 4: VPN E ACESSO REMOTO (Esta Semana)

### 4.1 IPsec VPN para Acesso Remoto

**Recursos Gratuitos:** IPsec VPN ilimitado sem licença

**Configuração Básica:**
```
config vpn ipsec phase1-interface
    edit "vpn-remote"
        set interface "lan2"
        set proposal aes256-sha256
        set pre-shared-key [CHAVE-SEGURA]
        set dpd on-idle
    next
end

config vpn ipsec phase2-interface
    edit 1
        set phase1name "vpn-remote"
        set proposal aes256-sha256
        set src-addr-type subnet
        set dst-addr-type subnet
        set src-subnet 192.168.0.0 255.255.0.0
        set dst-subnet 10.0.0.0 255.255.0.0
    next
end
```

### 4.2 SSL VPN (Alternativa)

**Recursos Gratuitos:** SSL VPN funciona sem licença

```
config vpn ssl settings
    set interface "lan2"
    set port 10443
    set default-portal "full-access"
end
```

---

## FASE 5: DDNS E ACESSO EXTERNO (Esta Semana)

### 5.1 Configurar FortiGuard DDNS (GRATUITO)

**Importante:** DDNS FortiGuard funciona SEM licença!

```
config system ddns
    edit 1
        set ddns-server "FortiGuardDDNS"
        set ddns-domain "firewall-lsa.fortiddns.com"
        set ddns-username ""
        set ddns-password ""
        set ddns-ip 10.32.163.250
    next
end
```

Ou usar DDNS de terceiros (No-IP, DynDNS):
```
config system ddns
    edit 1
        set ddns-server "DynDNS"
        set ddns-domain "meu-dominio.ddns.net"
        set ddns-username "usuario"
        set ddns-password "senha"
    next
end
```

---

## FASE 6: TRAFFIC SHAPING E QoS (Esta Semana)

### 6.1 Traffic Shaping por Interface

Controlar uso de bandwidth:

```
config firewall shaper traffic-shaper
    edit "high-priority"
        set guaranteed-bandwidth 50000
        set maximum-bandwidth 100000
    next
    edit "low-priority"
        set guaranteed-bandwidth 10000
        set maximum-bandwidth 50000
    next
end
```

### 6.2 Aplicar Shaper nas Políticas

```
config firewall policy
    edit 21
        set traffic-shaper "high-priority"
    next
end
```

---

## FASE 7: VLANs E SEGMENTAÇÃO (Já Implementado)

### Status Atual

| VLAN | Nome | Sub-rede | DHCP | Internet |
|------|------|----------|------|----------|
| 10 | VLAN10_IDRAC | 192.168.10.0/24 | ❌ Não | ✅ Sim |
| 20 | VLAN20_DATA | 10.10.20.0/24 | ✅ Sim (PXE) | ✅ Sim |
| 30 | VLAN30_LAN | 192.168.30.0/24 | ❌ Não | ✅ Sim |
| 40 | VLAN40_PERIPHER | 192.168.40.0/24 | ❌ Não | ✅ Sim |
| lan | LAN-PRIMARY | 192.168.1.0/24 | ❌ Não | ❌ **FALTA** |

### Melhorias

1. **DHCP para VLAN10 (iDRAC):**
```
config system dhcp server
    edit 5
        set dns-service default
        set default-gateway 192.168.10.1
        set netmask 255.255.255.0
        set interface "VLAN10_IDRAC"
        config ip-range
            edit 1
                set start-ip 192.168.10.100
                set end-ip 192.168.10.200
            next
        end
    next
end
```

2. **DHCP para VLAN30 (Workstations):**
```
config system dhcp server
    edit 6
        set dns-service default
        set default-gateway 192.168.30.1
        set netmask 255.255.255.0
        set interface "VLAN30_LAN"
        config ip-range
            edit 1
                set start-ip 192.168.30.100
                set end-ip 192.168.30.200
            next
        end
    next
end
```

---

## FASE 8: ISOLAMENTO E SEGMENTAÇÃO (Opcional)

### 8.1 Políticas Inter-VLAN Mais Restritivas

**Atual:** Todas as VLANs podem comunicar entre si.

**Melhoria:** Isolar VLANs conforme necessidade:

| Origem | Destino | Ação | Justificativa |
|--------|---------|------|---------------|
| VLAN10 (iDRAC) | VLAN40 (Infra) | ✅ Allow | Gestão de servidores |
| VLAN10 (iDRAC) | VLAN30 (Corp) | ❌ Deny | Segurança |
| VLAN20 (Cluster) | VLAN40 (Infra) | ✅ Allow | Acesso a switches |
| VLAN30 (Corp) | VLAN10 (iDRAC) | ❌ Deny | Isolamento |
| VLAN30 (Corp) | VLAN40 (Infra) | ✅ Allow | Acesso a infra |

### 8.2 Política DENY-ALL-LOG

Já existe (ID 999). Manter no final para auditoria.

---

## FASE 9: BACKUP E RECUPERAÇÃO

### 9.1 Backup Automático via Script

Sem FortiAnalyzer, usar backup manual ou script:

```
config system backup settings
    set status enable
    set server-type ftp
    set server-ip [IP-FTP]
    set username [user]
    set password [pass]
    set directory /backup/firewall
    set schedule daily
    set time 02:00
end
```

### 9.2 Backup via TFTP (Manual)

```
execute backup config tftp [IP-TFTP] firewall-lsa-backup.conf
```

---

## FASE 10: DNS E NTP

### 10.1 DNS Forwarder (Gratuito)

Configurar DNS local para a rede:

```
config system dns-server
    edit "lan"
        set mode forward-only
        set forward-server "system"
    next
    edit "VLAN30_LAN"
        set mode forward-only
        set forward-server "system"
    next
end
```

### 10.2 NTP Server (Já configurado)

```
config system ntp
    set ntpsync enable
    set server-mode enable
    set interface "lan2" "lan" "lan3"
end
```

---

## RESUMO DO PLANO

### Prioridade Alta (Fazer Hoje)

| Tarefa | Comando |
|--------|---------|
| Política LAN→WAN | `config firewall policy` edit 26 |
| DHCP na LAN | `config system dhcp server` edit 4 |
| Restringir admin access | `config system interface` |

### Prioridade Média (Esta Semana)

| Tarefa | Comando |
|--------|---------|
| Local-in policies | `config firewall local-in-policy` |
| Logging em memória | `config log memory setting` |
| Trusted hosts | `config system admin` |
| DDNS | `config system ddns` |

### Prioridade Baixa (Este Mês)

| Tarefa | Comando |
|--------|---------|
| VPN IPsec/SSL | `config vpn ipsec` / `config vpn ssl` |
| Traffic Shaping | `config firewall shaper` |
| DHCP VLANs | `config system dhcp server` |
| DNS Forwarder | `config system dns-server` |

---

## COMANDOS PRONTOS PARA EXECUÇÃO

### Script de Correção Imediata

```bash
# 1. Política LAN → WAN
config firewall policy
    edit 26
        set name "LAN-to-WAN-Internet"
        set srcintf "lan"
        set dstintf "lan2"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set logtraffic all
        set nat enable
    next
end

# 2. DHCP na LAN
config system dhcp server
    edit 4
        set dns-service default
        set default-gateway 192.168.1.99
        set netmask 255.255.255.0
        set interface "lan"
        config ip-range
            edit 1
                set start-ip 192.168.1.100
                set end-ip 192.168.1.200
            next
        end
    next
end

# 3. Restringir acesso admin em lan2
config system interface
    edit "lan2"
        set allowaccess https ssh ping
    next
end

# 4. Local-in policy para proteger FortiGate
config firewall local-in-policy
    edit 1
        set name "Block-All-WAN"
        set intf "lan2"
        set srcaddr "all"
        set dstaddr "all"
        set action deny
        set service "ALL"
        set schedule "always"
    next
end
```

---

## PRÓXIMOS PASSOS

1. **Executar script de correção imediata** (política LAN→WAN, DHCP)
2. **Aplicar hardening de segurança** (local-in policies, trusted hosts)
3. **Configurar logging** (memória + syslog externo)
4. **Configurar DDNS** para acesso externo
5. **Avaliar VPN** para acesso remoto seguro

---

**Referências:**
- Fortinet Docs: Features without License
- FortiOS 6.4 Hardening Guide
- Fortinet Community: VPN without License
- Fortinet Docs: DDNS (no license required)
- Fortinet Docs: Traffic Shaping