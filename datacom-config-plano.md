# Plano de Ação - Configuração DataCom DM956 AX1800

_Criado em: 2026-03-04_

---

## Especificações do Roteador

| Característica | Valor |
|----------------|-------|
| **Modelo** | DataCom DM956 5GT AX1800 |
| **Portas LAN** | 4x Gigabit Ethernet |
| **Porta WAN** | 1x Gigabit Ethernet |
| **Wi-Fi** | 2.4GHz + 5GHz (Wi-Fi 6, AX1800) |
| **Modos** | Router / Bridge |
| **Gerência Remota** | TR-069 (ISP) |

---

## Credenciais Padrão

| Item | Valor |
|------|-------|
| **IP Padrão** | `192.168.1.1` (ou `192.168.0.1` em alguns modelos) |
| **Usuário Padrão** | `admin` |
| **Senha Padrão** | `letmein` OU últimos 4 dígitos do MAC |

### Como Encontrar a Senha
1. Ver etiqueta na parte inferior do roteador
2. Se não tiver, tente:
   - `admin` / `letmein`
   - `admin` / últimos 4 dígitos do MAC
3. Se foi alterada pelo provedor (ex: OI, Vivo), pode ser necessário reset

---

## Plano de Ação

### PASSO 1: Acesso ao Roteador

**Conexão física:**
1. Conectar cabo Ethernet do laptop em uma porta LAN (1-4)
2. OU conectar via WiFi na rede padrão (SSID e senha na etiqueta)

**Configurar IP do laptop (se necessário):**
```bash
# IP estático na mesma faixa do roteador
sudo nmcli con mod "Conexão" ipv4.addresses 192.168.1.100/24
sudo nmcli con mod "Conexão" ipv4.gateway 192.168.1.1
sudo nmcli con up "Conexão"
```

**Acessar interface web:**
```
http://192.168.1.1
```

**Testar conectividade:**
```bash
ping 192.168.1.1
```

---

### PASSO 2: Verificar Modo Atual

**Na interface do roteador, verificar:**
1. Menu: Configurações → Modo de Operação
2. Opções: **Router** ou **Bridge**

**Se estiver em modo Router:**
- WAN deve receber IP via DHCP ou PPPoE
- LAN fornece IPs via DHCP próprio
- NAT ativo (Double NAT)

**Se estiver em modo Bridge:**
- Todas as portas funcionam como switch
- DHCP desabilitado
- Sem NAT

---

### PASSO 3: Configurar para Integrar com FortiGate

#### Opção A: Modo Router (Mais Simples)

**Configuração WAN:**
- Modo: Router
- WAN IP: DHCP Client (automático)
- Conectar: Porta WAN do DataCom → Porta "a" do FortiGate

**Configuração LAN:**
- IP LAN: `192.168.80.1` (ou outra faixa, diferente de 192.168.2.x)
- DHCP: Ativo (range: 192.168.80.100-200)

**Fluxo de Rede:**
```
Dispositivos WiFi → DataCom (192.168.80.x)
       ↓
    NAT (Double NAT)
       ↓
FortiGate "a" (192.168.2.x)
       ↓
    NAT
       ↓
Internet (via lan2)
```

#### Opção B: Modo Access Point (Sem Double NAT - RECOMENDADO)

**Configuração:**
1. Modo: **Bridge / Access Point**
2. IP Estático: `192.168.2.2` (fora do range DHCP do FortiGate)
3. DHCP: **DESBILITADO**
4. Gateway: `192.168.2.1` (IP do FortiGate)

**Conexão física:**
- Porta LAN (não WAN!) → Porta "a" do FortiGate

**Fluxo de Rede:**
```
Dispositivos WiFi → FortiGate "a" (192.168.2.x)
       ↓
    NAT (único)
       ↓
Internet (via lan2)
```

**Vantagens:**
- Sem Double NAT (melhor para jogos, VoIP, etc.)
- Dispositivos na mesma rede do FortiGate
- DHCP gerenciado pelo FortiGate

---

### PASSO 4: Verificar Conectividade

**Após configurar, testar:**

1. **Do laptop conectado ao DataCom:**
   ```bash
   ping 192.168.2.1    # FortiGate
   ping 8.8.8.8        # Internet
   ```

2. **Do FortiGate (via console):**
   ```bash
   diagnose ip arp list | grep "a "
   # Deve mostrar MAC do DataCom
   ```

3. **Tabela ARP do FortiGate:**
   - Interface "a" deve ter IP do DataCom (modo Router)
   - OU MAC do DataCom (modo AP, mesmo IP que clientes)

---

### PASSO 5: Configurar Wi-Fi

**Configurações recomendadas:**
- **2.4GHz:** SSID diferente (ex: `Casa-2G`)
- **5GHz:** SSID diferente (ex: `Casa-5G`)
- **Senha:** WPA2-PSK (mínimo 12 caracteres)
- **Canal:** Auto (ou fixar se tiver interferência)

**Para evitar conflito:**
- Não usar mesmo SSID do modem do provedor
- Verificar canais menos congestionados

---

## Troubleshooting

### Problema: Não consegue acessar 192.168.1.1

**Soluções:**
1. Reset do roteador (botão por 10 segundos)
2. Verificar se laptop está na mesma rede
3. Tentar `192.168.0.1`
4. Verificar se não há conflito de IP

### Problema: Senha não funciona

**Soluções:**
1. Ver etiqueta na parte inferior
2. Tentar `admin` / `admin`
3. Tentar `admin` / senha em branco
4. Reset para restaurar padrão de fábrica

### Problema: Internet não funciona

**Verificar:**
1. WAN está recebendo IP? (Status → WAN)
2. DNS está configurado? (8.8.8.8 / 1.1.1.1)
3. Cabo está na porta correta? (WAN para Router, LAN para AP)
4. FortiGate está com política NAT correta?

### Problema: Double NAT causando problemas

**Solução:**
- Usar modo Access Point (Bridge)
- Configurar DMZ no DataCom apontando para FortiGate
- Porta forwarding específico

---

## Configuração FortiGate (Já Feita)

A configuração do FortiGate está **correta**:

| Interface | Configuração |
|-----------|--------------|
| **a (lanA)** | 192.168.2.1/24, DHCP server (100-200) |
| **Política ID 25** | a → lan2 (NAT) |

**Não é necessário alterar nada no FortiGate.**

---

## Próximos Passos

1. Conectar o DataCom via cabo Ethernet ao laptop
2. Acessar `http://192.168.1.1`
3. Login com credenciais padrão
4. Verificar e configurar modo de operação
5. Conectar DataCom à porta "a" do FortiGate
6. Testar conectividade

---

## Contatos Úteis

- **DataCom Brasil:** https://www.datacom.com.br
- **Manual DM956:** PDF disponível no site
- **Suporte TR-069:** Gerenciado pelo ISP

---

_Arquivo criado para avaliação e configuração do roteador DataCom DM956_