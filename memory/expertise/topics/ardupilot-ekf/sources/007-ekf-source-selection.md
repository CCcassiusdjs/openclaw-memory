# EKF Source Selection and Switching - ArduPilot Copter Docs

**Fonte:** https://ardupilot.org/copter/docs/common-ekf-sources.html  
**Tipo:** Documentação Oficial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~15min

---

## 📋 Resumo Executivo

O EKF3 permite configurar fontes de posição e velocidade via parâmetros `EK3_SRCn_*`. Três conjuntos de fontes podem ser configurados e trocados em voo.

---

## 🎯 Parâmetros Principais (EK3_SRC1)

### POSXY - Posição Horizontal
| Opção | Fonte |
|-------|-------|
| 1 | Baro (não aplicável para POSXY) |
| 2 | GPS |
| 4 | Beacon |
| 6 | ExternalNAV |

### VELXY - Velocidade Horizontal
| Opção | Fonte |
|-------|-------|
| 1 | Baro (não aplicável) |
| 2 | GPS |
| 5 | Optical Flow |
| 6 | ExternalNAV |

### POSZ - Posição Vertical
| Opção | Fonte | Descrição |
|-------|-------|-----------|
| **1** | Baro | Default, funciona bem para maioria |
| 2 | RangeFinder | Raramente usado, apenas indoor com piso plano |
| 3 | GPS | Longos voos com GPS de alta qualidade (UBlox F9P) |
| 4 | Beacon | Quando beacons substituem GPS |
| 6 | ExternalNAV | Dispositivo companheiro fornece posição |

### VELZ - Velocidade Vertical
| Opção | Fonte |
|-------|-------|
| 1 | Baro |
| 2 | GPS |
| 6 | ExternalNAV |

### YAW - Orientação
| Opção | Fonte | Descrição |
|-------|-------|-----------|
| **1** | Compass | Default normal |
| 2 | GPS | GPS com yaw (Moving Baseline) |
| 3 | GPS + Compass Fallback | Usa GPS yaw, aprende compass offsets |
| 6 | ExternalNAV | Dispositivo companheiro |
| 8 | GSF | Gaussian Sum Filter, usado em compass-less |

---

## 🔄 Troca de Fontes (Source Switching)

### Três Conjuntos Disponíveis
- `EK3_SRC1_*` - Conjunto 1 (default)
- `EK3_SRC2_*` - Conjunto 2
- `EK3_SRC3_*` - Conjunto 3

### Como Trocar
1. **RC Auxiliary Switch:** `RCx_OPTION = 90` (EKF Source Set)
2. **MAVLink Command:** `MAV_CMD_SET_EKF_SOURCE_SET`
3. **Auto por IMU:** `EK3_OPTIONS` bit 3 força SRC1 para IMU1, SRC2 para IMU2, etc.

### Use Case Principal
- GPS ↔ Non-GPS transitions
- Indoor/outdoor transitions
- Optical Flow ↔ ExternalNAV

---

## ⚙️ Opções Avançadas

### EK3_SRC_OPTIONS (Bitmask)

| Bit | Função |
|-----|--------|
| 0 | Fundir todas as fontes de velocidade |
| 1 | Alinhar ExternalNAV com OpticalFlow |

### Velocity Source Fusing
- Combina velocidades de todas as fontes definidas
- **Atenção:** Fontes devem estar no mesmo frame de referência

### ExternalNAV/Optical Flow Transitions
- Bit 1 de `EK3_SRC_OPTIONS` mantém alinhamento
- Evita "bumps" de posição/velocidade na troca

---

## 💡 Conceitos-Chave

### Source Set
- Conjunto completo de fontes para o EKF
- Pode ter até 3 conjuntos configurados
- Troca via RC ou MAVLink

### GSF (Gaussian Sum Filter)
- Fornece yaw sem compass
- Baseado em velocidade e posição GPS
- Plane usa automaticamente em compass-less
- Copter requer configuração explícita

### GPS Yaw (Moving Baseline)
- GPS de alta qualidade pode fornecer yaw
- Útil quando compass é problemático
- Fallback para compass automático (opção 3)

---

## 📝 Configuração Típica

### Outdoor com GPS
```
EK3_SRC1_POSXY = 2 (GPS)
EK3_SRC1_VELXY = 2 (GPS)
EK3_SRC1_POSZ = 1 (Baro)
EK3_SRC1_VELZ = 2 (GPS)
EK3_SRC1_YAW = 1 (Compass)
```

### Indoor com Optical Flow
```
EK3_SRC1_POSXY = 0 (None - posição relativa)
EK3_SRC1_VELXY = 5 (Optical Flow)
EK3_SRC1_POSZ = 2 (RangeFinder)
EK3_SRC1_VELZ = 0 (None)
EK3_SRC1_YAW = 1 (Compass)
```

### GPS/Non-GPS Transition
```
# Source Set 1: GPS
EK3_SRC1_POSXY = 2 (GPS)
EK3_SRC1_VELXY = 2 (GPS)
# ... (outros)

# Source Set 2: Optical Flow
EK3_SRC2_POSXY = 0 (None)
EK3_SRC2_VELXY = 5 (Optical Flow)
# ... (outros)

# RC switch para alternar
RC6_OPTION = 90 (EKF Source Set)
```

---

## 🔗 Links Relacionados

- [GPS for Yaw (Moving Baseline)](https://ardupilot.org/copter/docs/common-gps-for-yaw.html)
- [GPS / Non-GPS Transitions](https://ardupilot.org/copter/docs/common-non-gps-to-gps.html)
- [Compass-less Configurations](https://ardupilot.org/copter/docs/common-compassless.html)