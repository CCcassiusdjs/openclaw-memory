# PX4 RTK GNSS (GPS)

**Source:** https://docs.px4.io/main/en/gps_compass/rtk_gps
**Date:** 2026-03-10
**Status:** completed

## Summary

RTK (Real Time Kinematic) GNSS fornece precisão centimétrica, permitindo aplicações como surveying de precisão. Requer base station no solo + rover no drone + link de telemetria.

## Conceitos-Chave

### Precisão RTK
- **Centimeter-level accuracy**
- Base station fixa + rover móvel
- Correções transmitidas via MAVLink 2

### Hardware Suportado
- **u-blox M8P, F9P**
- **Trimble MB-Two**
- **Septentrio mosaic-X5, AsteRx-m3**
- **Holybro H-RTK series**
- **CUAV C-RTK series**

### Features por Device

| Feature | Descrição |
|---------|-----------|
| **GPS Yaw** | Dual antenna heading |
| **DroneCAN** | Interface CAN |
| **PPK** | Post-Processing Kinematic |

### RTK Setup Process

1. **Survey-In**: Base station determina posição precisa (vários minutos)
2. **RTK Lock**: QGC icon fica branco
3. **Streaming**: Correções enviadas ao rover
4. **Vehicle Mode**: GPS mostra "3D RTK GPS Lock"

### GPS Yaw/Heading Source

- **Single device + dual antenna**: Alguns devices suportam
- **Dual F9P**: Dois módulos F9P podem calcular heading
- **Benefício**: Yaw não afetado por interferência magnética
- **Distância mínima**: ~50cm entre antenas

#### Configuration

| Parameter | Setting |
|-----------|---------|
| **GPS_YAW_OFFSET** | Ângulo da baseline relativa ao eixo X do veículo |
| **EKF2_GPS_CTRL** | Bit 3 = Dual antenna heading (add 8) |

### RTK GPS Settings (QGroundControl)

- Survey-In minimum duration
- Survey-In minimum accuracy
- Use Specified Base Position (para reutilizar posição conhecida)

### MAVLink2

- **Obrigatório**: Mais eficiente em canais de baixa bandwidth
- **MAV_PROTO_VER = 2**: Assegurar protocolo correto

### EKF Tuning para RTK

- **EKF2_GPS_V_NOISE**: Reduzir para 0.2
- **EKF2_GPS_P_NOISE**: Reduzir para 0.2
- Default assume precisão em metros, não centímetros

## Insights

1. **Centimeter accuracy**: RTK transforma precisão GPS
2. **Magnetic interference immunity**: GPS yaw elimina problemas de compass
3. **Dual F9P heading**: Alternativa ao compass para yaw
4. **Survey-In time**: Leva vários minutos, pode reutilizar posição fixa
5. **MAVLink2**: Necessário para bandwidth eficiente

## Hardware Recommendations

- **Holybro H-RTK F9P**: Popular, bem suportado
- **Septentrio AsteRx-m3**: Alta precisão, dual antenna heading nativo
- **ARK RTK GPS**: DroneCAN, fácil integração

## Conexões

- Base para positioning preciso
- GPS yaw alternativa ao magnetômetro
- Integração com EKF2 para fusão