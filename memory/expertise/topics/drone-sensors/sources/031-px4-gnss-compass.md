# PX4 GNSS (GPS) & Compass

**Source:** https://docs.px4.io/main/en/gps_compass/
**Date:** 2026-03-10
**Status:** completed

## Summary

GNSS (GPS, GLONASS, Galileo, Beidou, QZSS, SBAS) é necessário para missões e modos automáticos. PX4 suporta até 2 módulos GPS via UART ou CAN.

## Conceitos-Chave

### GNSS Suportados
- Protocolos: u-blox, MTK Ashtech, Emlid, UAVCAN/DroneCAN
- **Primary GPS**: GNSS + compass + buzzer + safety switch + LED
- **Secondary GPS**: Fallback (opcionais)

### Hardware Popular

| Device | GPS | Compass | CAN | Buzzer/SafeSw/LED | Notas |
|--------|-----|---------|-----|-------------------|-------|
| ARK GPS | M9N | BMM150 | ✓ | ✓ | + Baro, IMU |
| CUAV NEO 3X | M9N | RM3100 | ✓ | ✓ | + Baro |
| Holybro M9N | M9N | IST8310 | ✓ | |
| Holybro M10 | M10 | IST8310 | ✓ | |

### Conexões

#### Pixhawk Standard (UART/I2C)
- **GPS1/GPS&SAFETY**: 10-pin, primary GPS
  - UART para GNSS
  - I2C para compass
  - I2C para LED/buzzer/safety switch
- **GPS2**: 6-pin, secondary GPS (optional)

#### DroneCAN (CAN)
- CAN1/CAN2 ports
- Mais robusto que UART/I2C
- Plug-n-play

### GNSS Configuration

#### Primary GPS (UART)
- **GPS_1_CONFIG**: Port mapping (auto para u-blox)
- **GPS_1_PROTOCOL**: u-blox (default), Trimble, MTK, Emlid
- **SER_GPS1_BAUD**: Auto (default) ou 115200 (Trimble)

#### Secondary GPS (UART)
- **GPS_2_CONFIG**: Port assignment
- **SER_GPS2_BAUD**: Baud rate
- EKF2 deve ser configurado para blend data de ambos GPS

#### DroneCAN
- Configuração automática
- Ver documentação específica

### GPS Yaw/Heading
- Dual-antenna GPS pode prover yaw
- Elimina necessidade de magnetômetro
- Documentado em RTK GPS section

## GNSS Data Terms

- **DOP** (Dilution of Position): Qualidade geométrica dos satélites
- **EPH**: Desvio padrão do erro horizontal (metros)
- **EPV**: Desvio padrão do erro vertical (metros)

### DOP vs EPH/EPV
- DOP: Potencial de precisão baseado em geometria
- EPH/EPV: Estimativa real do erro (inclui ruído, atmosfera)
- Low DOP + High EPH/EPV = boa geometria mas ruído significativo

### Position Fusion Behavior
- GNSS position fusion começa APÓS yaw alignment
- Com magnetômetro: yaw magnético, fusão começa logo após boot
- Sem magnetômetro: precisa GPS yaw (dual-antenna) ou movimento
- Sem yaw válido: EKF não inicia GPS position fusion

## Mounting

- GNSS + Compass deve estar longe de motores/ESCs
- Pedestal ou asa (fixed-wing)
- Interferência magnética afeta compass

## Insights

1. **EPH/EPV > DOP**: Use EPH/EPV para avaliar precisão real
2. **Dual GPS**: Fallback importante para segurança
3. **CAN > UART**: Mais robusto para ambientes ruidosos
4. **Yaw alignment**: Crítico antes de GPS position fusion
5. **Magnetometer mount**: Distância de fontes magnéticas

## RTK Support

- RTK/PPK: Precisão centimétrica
- Dual-antenna: Pode prover heading sem compass

## Conexões

- Base para posicionamento global
- Complementado por optical flow indoor
- Integração EKF2 para fusão de sensores