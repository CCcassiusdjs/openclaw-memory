# Topologia de Rede Completa - LSA

**Data:** 2026-03-05
**Gerado por:** OpenClaw

---

## Visão Geral

```
                                    ┌─────────────────────────────────────┐
                                    │           INTERNET (ISP)            │
                                    │           10.32.163.250             │
                                    └─────────────────┬───────────────────┘
                                                      │
                                                      │ lan2 (DHCP)
                                                      │ 10.32.162.22/22
                                    ┌─────────────────▼───────────────────┐
                                    │          FORTIGATE 40F              │
                                    │          Firewall-LSA              │
                                    │        Firmware: 6.4.6             │
                                    └─────────────────┬───────────────────┘
                                                      │
                         ┌────────────────────────────┼────────────────────────────┐
                         │                            │                            │
                    ┌────┴────┐                  ┌────┴────┐                  ┌────┴────┐
                    │   wan   │                  │  lan1   │                  │  lan3   │
                    │ (DEFEITUOSA)               │  ADMIN  │                  │  TRUNK  │
                    │    -     │                  │192.168.1.99              │ VLANs   │
                    └─────────┘                  └────┬────┘                  └────┬────┘
                                                      │                            │
                                                 ┌────┴────┐               ┌─────────┴─────────┐
                                                 │ Laptop  │               │    VLANs:         │
                                                 │(Ethernet)│               │  10 - IDRAC       │
                                                 │192.168.1.100             │  20 - DATA        │
                                                 └─────────┘               │  30 - EXCLUSIVE   │
                                                                           │  40 - PERIPH      │
                                    ┌──────────────────────────────────────┴──────────────────────┐
                                    │                                                               │
                              ┌─────┴─────┐                                                   ┌─────┴─────┐
                              │    "a"    │                                                   │  "modem"  │
                              │  WiFi AP  │                                                   │  (não usado)│
                              │192.168.2.1│                                                   │     -     │
                              │  Bridge   │                                                   └───────────┘
                              └─────┬─────┘
                                    │
                              ┌─────┴─────┐
                              │   WiFi    │
                              │192.168.2.0/24
                              │  Clients  │
                              │ Laptop    │
                              │192.168.2.x│
                              └───────────┘
```

---

## FortiGate 40F - Interfaces

| Interface | Tipo | IP | Status | Descrição |
|-----------|------|----|---------|-----------|
| **wan** | Physical | - | DOWN | ⚠️ PORTA DEFEITUOSA |
| **lan1** | Physical | 192.168.1.99/24 | UP | Rede ADMIN (Ethernet) |
| **lan2** | Physical | 10.32.162.22/22 | UP | WAN (ISP/Modem) |
| **lan3** | Physical | 192.168.3.1/24 | UP | Porta física (hard-switch) |
| **a** | Physical | 192.168.2.1/24 | UP | WiFi AP (Bridge) |
| **modem** | Physical | - | - | Não utilizado |
| **lan3.10** | VLAN | 192.168.10.1/24 | UP | VLAN IDRAC |
| **lan3.20** | VLAN | 10.10.20.1/24 | UP | VLAN DATA |
| **lan3.30** | VLAN | 192.168.30.1/24 | UP | VLAN EXCLUSIVE |
| **lan3.40** | VLAN | 192.168.40.1/24 | UP | VLAN PERIPH |

---

## Tabela ARP - FortiGate

| IP | MAC | Interface |
|----|-----|-----------|
| 192.168.2.100 | de:69:9d:45:64:c6 | a (WiFi) |
| 192.168.2.102 | a0:80:69:d7:4b:23 | a (WiFi) |
| 192.168.2.103 | 52:56:3a:70:1a:c8 | a (WiFi) |
| 10.10.20.11 | 90:b1:1c:36:6b:59 | lan3.20 (DATA) |
| 10.32.163.250 | 04:eb:40:3d:ca:f0 | lan2 (WAN/ISP) |

---

## Switch HP V1910-16G - Portas

### Portas Agregadas (LACP/Bond)

| Porta | Status | Velocidade | VLAN | Descrição | Conectado a |
|-------|--------|------------|------|-----------|-------------|
| **BAGG1** | UP | 2G (agregado) | 20 | T620_DATA_LACP_BAGG1_VL20 | Servidor T620 (bond0) |
| **BAGG2** | UP | 1G | 20 | T630A_DATA_LACP_BAGG2_VL20 | Servidor T630A |
| **BAGG3** | UP | 1G | 20 | T630B_DATA_LACP_BAGG3_VL20 | Servidor T630B |

### Portas Físicas (GE1/0/1 a GE1/0/20)

| Porta | Status | VLAN | Descrição | Dispositivo | Observação |
|-------|--------|------|-----------|-------------|------------|
| **GE1/0/1** | UP | 20 | T620_DATA_LACP_MEMBER_P1 | T620 (bond) | Membro BAGG1 |
| **GE1/0/2** | UP | 20 | T620_DATA_LACP_MEMBER_P2 | T620 (bond) | Membro BAGG1 |
| **GE1/0/3** | UP | 10 | T620_IDRAC_VL10 | **T620 iDRAC** | IP: 192.168.10.x |
| **GE1/0/4** | ADM | 999 | UNUSED_VL999_P4 | - | Admin down |
| **GE1/0/5** | UP | 20 | T630A_DATA_P1_VL20 | T630A | Membro BAGG2 |
| **GE1/0/6** | DOWN | 20 | T630A_DATA_P2_VL20 | - | ⚠️ Desconectada |
| **GE1/0/7** | UP | 10 | T630B_IDRAC_VL10 | **T630B iDRAC** | IP: 192.168.10.x |
| **GE1/0/8** | ADM | 999 | UNUSED_VL999_P8 | - | Admin down |
| **GE1/0/9** | UP | 20 | T630B_DATA_P1_VL20 | T630B | Membro BAGG3 |
| **GE1/0/10** | UP | 20 | T630B_DATA_P2_VL20 | T630B | Membro BAGG3 |
| **GE1/0/11** | UP | 10 | T630A_IDRAC_VL10 | **T630A iDRAC** | IP: 192.168.10.x |
| **GE1/0/12** | ADM | 999 | UNUSED_VL999_P12 | - | Admin down |
| **GE1/0/13** | UP | Trunk | FGT_P3_TRUNK | **FortiGate** | VLANs 1,10,20,30,40 |
| **GE1/0/14** | DOWN | 40 | PERIPH_VL40_ACCESS_P14 | - | Desconectada |
| **GE1/0/15** | DOWN | 40 | PERIPH_VL40_ACCESS_P15 | - | Desconectada |
| **GE1/0/16** | DOWN | 40 | PERIPH_VL40_ACCESS_P16 | - | Desconectada |
| **GE1/0/17** | DOWN | 1 | SPARE_P17 | - | Desconectada |
| **GE1/0/18** | DOWN | 1 | SPARE_P18 | - | Desconectada |
| **GE1/0/19** | DOWN | 1 | SPARE_P19 | - | Desconectada |
| **GE1/0/20** | DOWN | 1 | SPARE_P20 | - | Desconectada |

---

## VLANs

| VLAN ID | Nome | Subnet | Gateway | Função |
|---------|------|--------|---------|--------|
| **1** | default | - | - | VLAN padrão |
| **10** | IDRAC | 192.168.10.0/24 | 192.168.10.1 | iDRAC dos servidores |
| **20** | DATA | 10.10.20.0/24 | 10.10.20.1 | Rede de dados (servidores) |
| **30** | EXCLUSIVE | 192.168.30.0/24 | 192.168.30.1 | Reservada |
| **40** | PERIPH | 192.168.40.0/24 | 192.168.40.1 | Periféricos / Switch |
| **999** | UNUSED | - | - | Portas desabilitadas |

---

## Tabela MAC Address - Switch

| MAC Address | VLAN | Porta | Dispositivo |
|-------------|------|-------|-------------|
| **c81f-66cc-a833** | 10 | GE1/0/11 | T630A iDRAC |
| **90b1-1c36-6b59** | 20 | BAGG1 | T620 (bond0) |
| **90b1-1c36-6b5a** | 20 | BAGG1 | T620 (bond0) |
| **c81f-66cc-a835** | 20 | BAGG3 | T630B |
| **38c0-eac6-a669** | 20 | GE1/0/13 | FortiGate |
| **38c0-eac6-a669** | 40 | GE1/0/13 | FortiGate |

---

## Servidores Conectados

### T620 (10.10.20.11)

| Componente | Detalhes |
|------------|----------|
| **Hostname** | t620 |
| **IP (bond0)** | 10.10.20.11/24 |
| **Bond** | BAGG1 (GE1/0/1 + GE1/0/2) - LACP |
| **iDRAC** | GE1/0/3 (VLAN 10) |
| **CPU** | Intel Xeon E5-2620 @ 2.00GHz (24 cores) |
| **RAM** | 31GB |
| **Disco** | 70GB (root) + 4.2TB (home) |
| **OS** | RHEL 9.7 |
| **Uptime** | 9 dias |

### T630A (Status Parcial)

| Componente | Detalhes |
|------------|----------|
| **Status** | ⚠️ Parcial (porta 6 DOWN) |
| **Bond** | BAGG2 (GE1/0/5, GE1/0/6) - LACP |
| **iDRAC** | GE1/0/11 (VLAN 10) |
| **Porta 6** | DOWN (desconectada) |

### T630B

| Componente | Detalhes |
|------------|----------|
| **Status** | ✅ UP |
| **Bond** | BAGG3 (GE1/0/9 + GE1/0/10) - LACP |
| **iDRAC** | GE1/0/7 (VLAN 10) |

---

## Diagrama de Conectividade

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                      INTERNET (ISP)                         │
                    │                      10.32.163.250                          │
                    └─────────────────────────────┬───────────────────────────────┘
                                                  │
                                                  │ lan2 (DHCP)
                                                  ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                     FORTIGATE 40F                           │
                    │                     Firewall-LSA                             │
                    │  ┌───────────────────────────────────────────────────────┐  │
                    │  │ Interfaces:                                           │  │
                    │  │  wan      - DEFEITUOSA                                │  │
                    │  │  lan1     - ADMIN (192.168.1.99) ───────────► Laptop   │  │
                    │  │  lan2     - WAN/ISP (10.32.162.22)                    │  │
                    │  │  lan3     - TRUNK (192.168.3.1)                        │  │
                    │  │  a        - WiFi (192.168.2.1) ─────────────► WiFi AP  │  │
                    │  │  lan3.10  - IDRAC (192.168.10.1)                      │  │
                    │  │  lan3.20  - DATA (10.10.20.1)                          │  │
                    │  │  lan3.30  - EXCLUSIVE (192.168.30.1)                  │  │
                    │  │  lan3.40  - PERIPH (192.168.40.1) ─────────► Switch   │  │
                    │  └───────────────────────────────────────────────────────┘  │
                    └─────────────────────────────┬───────────────────────────────┘
                                                  │
                                                  │ GE1/0/13 (Trunk)
                                                  │ VLANs: 1, 10, 20, 30, 40
                                                  ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                   SWITCH HP V1910-16G                        │
                    │                   SWITCH-CORE-LSA                            │
                    │                   192.168.40.2 (VLAN 40)                     │
                    │  ┌───────────────────────────────────────────────────────┐  │
                    │  │ Portas Ativas:                                        │  │
                    │  │  GE1/0/1-2  ─ BAGG1 ─► T620 (bond)     [VLAN 20]      │  │
                    │  │  GE1/0/3     ─────────► T620 iDRAC      [VLAN 10]      │  │
                    │  │  GE1/0/5     ─ BAGG2 ─► T630A            [VLAN 20]      │  │
                    │  │  GE1/0/6     ─ DOWN (desconectada)                      │  │
                    │  │  GE1/0/7     ─────────► T630B iDRAC      [VLAN 10]      │  │
                    │  │  GE1/0/9-10  ─ BAGG3 ─► T630B            [VLAN 20]      │  │
                    │  │  GE1/0/11    ─────────► T630A iDRAC      [VLAN 10]      │  │
                    │  │  GE1/0/13    ─────────► FortiGate (Trunk)               │  │
                    │  └───────────────────────────────────────────────────────┘  │
                    └─────────────────────────────┬───────────────────────────────┘
                                                  │
          ┌───────────────────────────────────────┼───────────────────────────────────────┐
          │                                       │                                       │
          │  ┌─────────────────┐                  │                  ┌─────────────────┐  │
          │  │   T620 iDRAC    │                  │                  │   T630A iDRAC   │  │
          │  │  GE1/0/3 (VLAN10)│                  │                  │ GE1/0/11 (VLAN10)│ │
          │  │ 192.168.10.x     │                  │                  │ 192.168.10.x    │  │
          │  └─────────────────┘                  │                  └─────────────────┘  │
          │                                       │                                       │
          │  ┌─────────────────┐                  │                  ┌─────────────────┐  │
          │  │    T620 (bond)  │                  │                  │    T630A        │  │
          │  │  BAGG1 (VLAN20) │                  │                  │ BAGG2 (VLAN20)  │  │
          │  │  GE1/0/1 + 2    │                  │                  │ GE1/0/5 (+ 6?)  │  │
          │  │  10.10.20.11    │                  │                  │ 10.10.20.x      │  │
          │  └─────────────────┘                  │                  └─────────────────┘  │
          │                                       │                                       │
          │                      ┌────────────────┴────────────────┐                      │
          │                      │          T630B                 │                      │
          │                      │  ┌─────────────────────────┐   │                      │
          │                      │  │ iDRAC: GE1/0/7 (VLAN10) │   │                      │
          │                      │  │ bond: BAGG3 (VLAN20)    │   │                      │
          │                      │  │ Ports: GE1/0/9 + 10     │   │                      │
          │                      │  └─────────────────────────┘   │                      │
          │                      └─────────────────────────────────┘                      │
          │                                                                               │
          └───────────────────────────────────────────────────────────────────────────────┘
```

---

## Políticas de Firewall (FortiGate)

| ID | Nome | Origem | Destino | Status |
|----|------|--------|---------|--------|
| 20 | WIFI-to-VLAN40 | a (WiFi) | lan3.40 | ✅ Ativa |
| 21 | VLAN40-to-WIFI | lan3.40 | a (WiFi) | ✅ Ativa |
| 22 | WIFI-to-VLAN10 | a (WiFi) | lan3.10 (IDRAC) | ✅ Ativa |
| 23 | VLAN10-to-WIFI | lan3.10 (IDRAC) | a (WiFi) | ✅ Ativa |
| 24 | WIFI-to-VLAN20 | a (WiFi) | lan3.20 (DATA) | ✅ Ativa |
| 25 | VLAN20-to-WIFI | lan3.20 (DATA) | a (WiFi) | ✅ Ativa |
| 26 | WIFI-to-VLAN30 | a (WiFi) | lan3.30 (EXCLUSIVE) | ✅ Ativa |
| 27 | VLAN30-to-WIFI | lan3.30 (EXCLUSIVE) | a (WiFi) | ✅ Ativa |

---

## Problemas Detectados

### 1. Porta DEFEITUOSA - wan (FortiGate)
- **Status:** PORTA WAN DEFEITUOSA
- **Impacto:** Não pode ser usada para WAN
- **Solução:** WAN conectada em lan2

### 2. Porta Desconectada - GE1/0/6 (Switch)
- **Status:** DOWN
- **Descrição:** T630A_DATA_P2_VL20
- **Impacto:** T630A opera com apenas 1 porta do bond (LACP parcial)
- **Solução:** Verificar cabo ou conectar porta

### 3. Portas Não Utilizadas
- **Switch:** GE1/0/4, GE1/0/8, GE1/0/12 (admin down - VLAN 999)
- **Switch:** GE1/0/14-16 (VLAN 40 - sem dispositivos)
- **Switch:** GE1/0/17-20 (SPARE)

---

## Rotas do Sistema

### FortiGate

```
S* 0.0.0.0/0 via 10.32.163.250 (lan2) - Internet
C  10.10.20.0/24 (lan3.20) - VLAN DATA
C  192.168.2.0/24 (a) - WiFi
C  192.168.3.0/24 (lan3) - Trunk
C  192.168.10.0/24 (lan3.10) - VLAN IDRAC
C  192.168.30.0/24 (lan3.30) - VLAN EXCLUSIVE
C  192.168.40.0/24 (lan3.40) - VLAN PERIPH
```

### Laptop (via WiFi)

```
192.168.10.0/24 → 192.168.2.1 (WiFi)
192.168.30.0/24 → 192.168.2.1 (WiFi)
192.168.40.0/24 → 192.168.2.1 (WiFi)
10.10.20.0/24 → 192.168.2.1 (WiFi)
```

---

## Credenciais

| Dispositivo | IP | Usuário | Senha |
|-------------|-----|---------|-------|
| **FortiGate** | 192.168.2.1 | admin | @CiaoMiau2955 |
| **Switch HP** | 192.168.40.2 | admin | admin |
| **T620** | 10.10.20.11 | cassiusdjs | 230612 |
| **T620** | 10.10.20.11 | root | 230612 |

---

## Acessos Verificados

| Dispositivo | SSH | Status |
|-------------|-----|--------|
| **FortiGate** | ✅ admin@192.168.2.1 | Funcionando |
| **Switch HP** | ✅ admin@192.168.40.2 | Funcionando |
| **T620** | ✅ cassiusdjs@10.10.20.11 | Funcionando |

---

_Gerado em: 2026-03-05_