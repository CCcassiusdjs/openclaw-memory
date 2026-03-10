# EKF Navigation Overview and Tuning - ArduPilot Dev Docs

**Fonte:** https://ardupilot.org/dev/docs/extended-kalman-filter.html  
**Tipo:** Documentação Oficial (EKF1 - histórico)  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~40min

---

## 📋 Resumo Executivo

Este documento descreve o algoritmo EKF original (EKF1), que foi a base para EKF2 e EKF3. **Nota: EKF1 foi removido do código**, mas os conceitos fundamentais ainda se aplicam.

---

## 🎯 Teoria do EKF

### Estados Estimados (22 estados)
O EKF estima um total de 22 estados:

| Categoria | Estados |
|-----------|---------|
| **Orientação** | Roll, Pitch, Yaw |
| **Velocidade** | VN, VE, VD (NED) |
| **Posição** | PN, PE, PD (NED) |
| **Bias do Giro** | GX, GY, GZ |
| **Bias do Accel** | AZbias |
| **Vento** | VWN, VWE |
| **Campo Mag Terra** | MN, ME, MD |
| **Campo Mag Corpo** | MX, MY, MZ |

### Como Funciona (Simplificado)

1. **State Prediction:**
   - Integra taxas angulares do IMU → posição angular
   - Converte acelerações body→NED, corrige gravidade
   - Integra acelerações → velocidade
   - Integra velocidade → posição

2. **Error Estimation:**
   - EKF_GYRO_NOISE e EKF_ACC_NOISE estimam crescimento do erro
   - Erros capturados na "State Covariance Matrix"

3. **State Correction (quando GPS chega):**
   - Calcula "Innovation" = diferença entre predição e medição
   - Combina Innovation, Covariance Matrix e EKF_POSNE_NOISE
   - Corrige estados usando correlações entre erros

4. **Covariance Update:**
   - Reduz incerteza após medição
   - Retorna ao passo 1

---

## 🔧 Parâmetros de Tuning

### Ruído de Processo (Process Noise)

| Parâmetro | Descrição |
|-----------|-----------|
| `EKF_GYRO_PNOISE` | Erro do giro (excluindo bias). Maior = menos confiança no giro |
| `EKF_ACC_PNOISE` | Erro do acelerômetro (excluindo bias). Maior = menos confiança no accel |
| `EKF_GBIAS_PNOISE` | Taxa de aprendizado do bias do giro. Maior = mais rápido e mais ruidoso |
| `EKF_ABIAS_PNOISE` | Taxa de aprendizado do bias Z do accel |
| `EKF_WIND_PNOISE` | Taxa de estimação do vento |
| `EKF_MAGB_PNOISE` | Taxa de aprendizado do campo mag corpo |
| `EKF_MAGE_PNOISE` | Taxa de aprendizado do campo mag terra |

### Ruído de Medição (Measurement Noise)

| Parâmetro | Descrição |
|-----------|-----------|
| `EKF_ALT_NOISE` | Ruído do barômetro (m). Maior = menos confiança |
| `EKF_POSNE_NOISE` | Ruído GPS horizontal (m) |
| `EKF_VELD_NOISE` | Ruído velocidade vertical GPS (m/s) |
| `EKF_VELNE_NOISE` | Ruído velocidade horizontal GPS (m/s) |
| `EKF_MAG_NOISE` | Ruído do magnetômetro (sensor units / 1000) |
| `EKF_EAS_NOISE` | Ruído do airspeed (m/s) |
| `EKF_FLOW_NOISE` | Ruído do optical flow (rad/s) |

### Gates (Consistency Checks)

| Parâmetro | Descrição |
|-----------|-----------|
| `EKF_POS_GATE` | Gate para posição GPS. Default 3σ |
| `EKF_VEL_GATE` | Gate para velocidade GPS |
| `EKF_HGT_GATE` | Gate para altura barômetro |
| `EKF_MAG_GATE` | Gate para magnetômetro |
| `EKF_EAS_GATE` | Gate para airspeed |
| `EKF_FLOW_GATE` | Gate para optical flow |
| `EKF_RNG_GATE` | Gate para range finder |

### Glitch Protection

| Parâmetro | Descrição |
|-----------|-----------|
| `EKF_GLITCH_RAD` | Máxima diferença de posição GPS antes de ativar proteção (m) |
| `EKF_GLITCH_ACCEL` | Máxima diferença de aceleração GPS (cm/s²) |

---

## 📊 Interpretação de Logs (EKF1-EKF4)

### EKF1 - Outputs Principais
- Roll, Pitch, Yaw (deg)
- VN, VE, VD (m/s)
- PN, PE, PD (m)
- GX, GY, GZ - Bias do giro (deg/min)

### EKF2 - Estados Adicionais
- Ratio - Peso do IMU1 na fusão (deve flutuar ~50%)
- AZ1bias, AZ2bias - Bias Z do accel
- VWN, VWE - Velocidade do vento
- MN, ME, MD - Campo mag terra
- MX, MY, MZ - Bias do magnetômetro

### EKF3 - Inovações
- IVN, IVE, IVD - Inovações velocidade GPS (m/s)
- IPN, IPE - Inovações posição GPS (m)
- IPD - Inovação altura barômetro (m)
- IMX, IMY, IMZ - Inovações magnetômetro
- IVT - Inovação airspeed (m/s)

### EKF4 - Test Ratios (Health)
- SV - Ratio velocidade GPS / EKF_VEL_GATE
- SP - Ratio posição GPS / EKF_POS_GATE
- SH - Ratio altura baro / EKF_HGT_GATE
- SMX, SMY, SMZ - Ratio magnetômetro / EKF_MAG_GATE
- SVT - Ratio airspeed / EKF_EAS_GATE

**Regra:** Valores devem ficar < 1. Se > 1 = medição rejeitada.

---

## 💡 Dicas de Tuning

### Como Ajustar EKF_ALT_NOISE
1. Plotar EKF3.IPD em voo
2. Medir ruído quando veículo está estável
3. Usar valor RMS como ponto inicial
4. Copters geralmente precisam de valor maior que o teórico

### Como Ajustar EKF_VELNE_NOISE
1. Plotar EKF3.IVN e EKF3.IVE
2. Medir ruído em voo não-manobrando
3. Usar valor RMS como ponto inicial
4. HUD deve estar estável em GPS claro

### Como Ajustar EKF_MAG_NOISE
1. Plotar EKF3.IMX, IMY, IMZ
2. Transientes de ~50 são normais (valor default = 0.05)
3. Se spikes > 100, investigar interferência

### Como Ajustar Gates
1. Plotar EKF4.SV, SP, SH, SM*
2. Se valores > 1 com bons sensores, aumentar gate
3. Valores < 0.5 típicos para sensores de qualidade

---

## ⚠️ Problemas Comuns

### EKF2.Ratio perto de 0 ou 100%
- Indica aliasing no acelerômetro
- Investigar montagem com isolamento de vibração

### EKF4.SH alto
- Fluxo de ar afetando barômetro
- Erros de acelerômetro (drift ou aliasing)

### EKF4.SM* alto
- Problema de calibração do compass
- Interferência elétrica (corrente do motor)

### Posições pulando (GPS glitches)
- Verificar EKF_GLITCH_RAD
- Verificar EKF_POS_GATE

---

## 🔗 Links Relacionados

- [Derivações Matemáticas](https://github.com/priseborough/InertialNav/blob/master/derivations/GenerateEquations22states.m)
- [AP_NavEKF2](https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_NavEKF2)
- [AP_NavEKF3](https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_NavEKF3)