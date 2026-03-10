# PX4 RTK GPS Heading with Dual u-blox F9P

**Source:** https://docs.px4.io/main/en/gps_compass/u-blox_f9p_heading
**Date:** 2026-03-10
**Status:** completed

## Summary

Dois módulos u-blox F9P RTK GPS montados no veículo podem calcular heading (yaw) com precisão, sendo alternativa ao compass. Moving Base + Rover configurados para heading.

## Conceitos-Chave

### Princípio
- Compara tempo de chegada do sinal GNSS em duas antenas separadas
- Calcula ângulo da baseline (linha entre antenas)
- **Mínimo 50cm** entre antenas (verificar documentação do fabricante)

### Devices Suportados

| Device | CAN | UART2 | Notes |
|--------|-----|-------|-------|
| ARK RTK GPS | ✓ | | DroneCAN |
| SparkFun GPS-RTK2 | ✓ | ✓ | |
| SIRIUS RTK GNSS ROVER | ✓ | ✓ | |
| Holybro H-RTK F9P Helical | ✓ | ✓ | |
| Holybro DroneCAN H-RTK F9P | ✓ | | DroneCAN |
| CUAV C-RTK 9Ps | ✓ | ✓ | |

### Devices NÃO Suportados
- Freefly RTK GPS (sem CAN ou UART2)
- Holybro H-RTK F9P Rover Lite (sem CAN ou UART2)

## Antenna Setup

- **Antenas idênticas**: Mesmo modelo, orientação
- **Mesmo nível horizontal**: Plano paralelo ao solo
- **Mesmo ground plane**: Tamanho e formato idênticos
- **GPS_YAW_OFFSET**: Configurar ângulo da baseline

## UART Setup

1. Conectar UART2 dos GPS:
   - TXD2 do "Moving Base" → RXD2 do "Rover"
   
2. Conectar UART1 a UARTs separados no FC:
   - Main GPS = Rover
   - Secondary GPS = Moving Base

3. Configurar parâmetros:
   - **GPS_UBX_MODE = 1** (Heading)
   - **EKF2_GPS_CTRL bit 3 = 1** (add 8)
   - **GPS_YAW_OFFSET** = ângulo da baseline

4. Reboot e aguardar GPS reception

## CAN Setup

- Ver documentação específica do device
- ARK RTK GPS: "Setting Up Moving Baseline & GPS Heading"

## Configuration Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| **GPS_UBX_MODE** | 1 | Heading mode |
| **EKF2_GPS_CTRL** | +8 | Bit 3 = Dual antenna heading |
| **GPS_YAW_OFFSET** | 0° | 0 se antena primária na frente |
| | 90° | Se antena primária na direita |

## Insights

1. **Compass alternative**: Yaw sem interferência magnética
2. **50cm minimum**: Distância mínima entre antenas
3. **Identical setup**: Antenas idênticas reduzem erros
4. **UART2 connection**: Necessário para comunicação entre GPS
5. **CAN simpler**: DroneCAN devices mais fáceis de configurar

## Conexões

- Alternativa ao magnetômetro para heading
- Base para RTK positioning + heading
- Integração com EKF2 yaw fusion