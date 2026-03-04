# FortiGate 40F - Melhorias Recomendadas

**Data:** 2026-03-04
**Hostname:** Firewall-LSA
**Firmware:** FortiOS 6.4.6 (build 1879)
**Serial:** FGT40FTK2309DUMZ

---

## 1. PROBLEMAS CRÍTICOS IDENTIFICADOS

### 🔴 1.1 Interface "lan" sem acesso à Internet

**Problema:** A interface "lan" (hard-switch com lan1) não tem política NAT para sair pela WAN (lan2).

**Impacto:** Laptop conectado em lan1 não tem acesso à Internet.

**Solução:** Criar política firewall:
```
config firewall policy
    edit [novo-id]
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

### 🔴 1.2 DHCP não configurado na interface "lan"

**Problema:** Não há DHCP server na interface "lan" (192.168.1.0/24).

**Impacto:** Dispositivos em lan1 precisam de IP estático.

**Solução:** Criar DHCP server:
```
config system dhcp server
    edit [novo-id]
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

## 2. ASSINATURAS DE SEGURANÇA DESATUALIZADAS

### ⚠️ FortiGuard Status

| Componente | Versão | Data | Status |
|------------|--------|------|--------|
| AV Engine | 6.162 | 2021-04-30 | ⚠️ Desatualizado |
| Virus Definitions | 1.000 | 2018-04-09 | 🔴 Crítico |
| Attack Definitions | 6.741 | 2015-12-01 | 🔴 Crítico |
| IPS Engine | 6.091 | 2021-05-10 | ⚠️ Desatualizado |
| Application DB | 6.741 | 2015-12-01 | 🔴 Crítico |

**Problema:** Assinaturas de segurança com quase 10 anos sem atualização!

**Impacto:**
- Sem proteção contra ameaças recentes
- IPS ineficaz contra vulnerabilidades modernas
- Application control desatualizado

**Solução:** 
1. Registrar FortiGate no FortiCloud (gratuito para atualizações básicas)
2. Configurar atualização automática:
```
config system autoupdate schedule
    set status enable
    set frequency daily
    set time 03:00
end
```

---

## 3. RECURSOS NÃO UTILIZADOS

### 3.1 IPS (Intrusion Prevention System)

**Status:** Desatualizado e provavelmente não aplicado nas políticas.

**Recomendação:**
1. Atualizar assinaturas IPS
2. Aplicar perfil IPS nas políticas de saída para Internet:
```
config firewall policy
    edit 21
        set ips-sensor "default"
    next
    edit 22
        set ips-sensor "default"
    next
    ...
end
```

### 3.2 Application Control

**Status:** Database desatualizada (2015).

**Recomendação:**
1. Atualizar database
2. Criar perfil para bloquear aplicações não autorizadas:
```
config application profile
    edit "block-p2p-torrent"
        set comment "Block P2P and Torrent"
        config entries
            edit 1
                set application "BitTorrent" "eDonkey" "Gnutella"
                set action block
            next
        end
    next
end
```

### 3.3 Antivírus / Malware Protection

**Status:** Desatualizado (2018).

**Recomendação:**
1. Atualizar definições de vírus
2. Aplicar AV nas políticas de Internet:
```
config firewall policy
    edit [id]
        set av-profile "default"
    next
end
```

### 3.4 Web Filtering

**Status:** Não configurado.

**Recomendação:** Aplicar filtro web para bloquear categorias maliciosas:
```
config webfilter profile
    edit "security-profile"
        config ftgd-wf
            config filters
                edit 1
                    set category 86  ; Malicious Websites
                    set action block
                next
                edit 2
                    set category 61  ; Phishing
                    set action block
                next
            end
        end
    next
end
```

### 3.5 SSL Inspection

**Status:** Provavelmente não configurado.

**Importância:** Essencial para inspecionar tráfego HTTPS.

**Recomendação:** Configurar SSL inspection para tráfego outbound.

### 3.6 DNS Filter

**Status:** Não verificado.

**Recomendação:** Configurar DNS filtering para bloquear domínios maliciosos.

### 3.7 Logging & Analytics

**Status:** Sem disco rígido local ("Log hard disk: Not available").

**Recomendação:**
1. Configurar logging para FortiCloud (gratuito com limitações)
2. OU configurar syslog server externo
3. OU usar FortiAnalyzer/VM

```
config log syslogd setting
    set status enable
    set server [IP-syslog-server]
    set port 514
end
```

---

## 4. MELHORIAS DE SEGURANÇA

### 4.1 Políticas de Firewall

**Recomendação:** Refinar políticas "allow all" para princípio de menor privilégio:

**Políticas Atuais:**
- srcaddr "all" + dstaddr "all" + service "ALL"

**Melhoria:**
- Especificar endereços/grupos
- Limitar serviços ao necessário
- Aplicar profiles de segurança

### 4.2 Hardening Básico

```
config system global
    set admin-scp disable          ; Desabilitar SCP para admin
    set admintimeout 10            ; Timeout de 10 minutos
    set strong-crypto enable       ; Criptografia forte (já ativo)
end

config system settings
    set gui-allow-unsafe-encryption-ciphers disable
end
```

### 4.3 Acesso Administrativo

**Atual:** Muitos protocolos habilitados em lan3:
```
set allowaccess ping https ssh snmp http fgfm radius-acct fabric ftm
```

**Recomendação:** Limitar a apenas HTTPS e SSH:
```
config system interface
    edit "lan3"
        set allowaccess https ssh
    next
end
```

### 4.4 SNMP

**Recomendação:** Configurar SNMP v3 (criptografado) para monitoramento:
```
config system snmp sysinfo
    set status enable
    set description "Firewall-LSA"
    set location "LSA Datacenter"
end

config system snmp community
    edit [community-name]
        set status enable
        config hosts
            edit 1
                set interface "lan3"
                set ip [IP-monitoramento]
            next
        end
    next
end
```

---

## 5. RECOMENDAÇÕES DE REDE

### 5.1 DHCP para VLANs

**VLAN10 (iDRAC):** Sem DHCP - Adicionar para facilitar gestão iDRAC

**VLAN30 (Corporate LAN):** Sem DHCP - Adicionar para workstations

**VLAN40 (Infrastructure):** Sem DHCP - Considerar para switches/servidores

### 5.2 DNS Personalizado

**Recomendação:** Usar DNS internos ou FortiGuard DNS:
```
config system dns
    set primary 8.8.8.8
    set secondary 8.8.4.4
    set protocol clear
end
```

### 5.3 Roteamento Estático

**Rota existente:** 192.168.80.0/24 via 192.168.2.100

**Verificar:** Esta rota é necessária? Para que serve?

---

## 6. BACKUP E RECUPERAÇÃO

### 6.1 Backup Automático

**Recomendação:** Configurar backup automático:

```
config system backup settings
    set status enable
    set server-type ftp
    set server-ip [IP-FTP-Server]
    set username [user]
    set password [pass]
    set directory /backup/firewall
    set schedule daily
    set time 02:00
end
```

### 6.2 Configuração Atual

**Última verificação:** Sem disco local para logs/backups

---

## 7. MONITORAMENTO

### 7.1 FortiCloud (Gratuito)

**Benefícios:**
- Atualizações de segurança
- Analytics básico
- Alertas de segurança

**Configuração:**
```
config system fortiguard
    set antispam-force-off disable
    set webfilter-force-off disable
    set antispam-cache enable
end

execute update-now
```

### 7.2 Syslog Externo

**Para logs detalhados:** Configurar syslog server externo.

---

## 8. RESUMO DE PRIORIDADES

### 🔴 Crítico (Fazer Agora)

1. **Criar política "lan → lan2"** para laptop ter Internet
2. **Configurar DHCP na interface "lan"**
3. **Atualizar assinaturas de segurança** (IPS, AV, App Control)

### ⚠️ Importante (Esta Semana)

4. Aplicar perfis de segurança nas políticas de Internet
5. Configurar SSL inspection
6. Limitar acesso administrativo em lan3
7. Configurar backup automático

### 📋 Recomendado (Este Mês)

8. Refinar políticas de firewall (least privilege)
9. Configurar SNMP v3 para monitoramento
10. Configurar DNS filtering
11. Configurar syslog externo
12. Documentar topologia de rede

---

## 9. COMANDOS PARA IMPLEMENTAÇÃO IMEDIATA

### 9.1 Política LAN → WAN

```bash
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

### 9.2 DHCP Server na LAN

```bash
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

### 9.3 Atualização de Assinaturas

```bash
execute update-now
```

---

**Auditoria realizada por:** OpenClaw
**Método:** Console serial /dev/ttyUSB0
**Sessão:** screen -r fortigate