# PX4 Optical Flow

**Source:** https://docs.px4.io/main/en/sensor/optical_flow
**Date:** 2026-03-10
**Status:** completed

## Summary

Optical Flow usa câmera apontada para baixo + sensor de distância para estimar velocidade. Permite navegação sem GNSS (indoor, underground, GNSS-denied).

## Conceitos-Chave

### Setup Requirements
- **Câmera downward-facing**: Captura movimento do terreno
- **Distance sensor (LIDAR preferido)**: Mede altura para conversão de fluxo
- Podem ser combinados (ARK Flow, H-Flow) ou separados

### Output Convention
| Movimento | Integrated Flow |
|-----------|-----------------|
| Forward | +Y |
| Backward | -Y |
| Right | -X |
| Left | +X |

### Scale Factor
- **SENS_FLOW_SCALE**: Ajusta escala do fluxo óptico
- Para rotação pura: integrated_xgyro == integrated_x
- Se não coincidem, ajustar scale factor
- **Altitude alta (>20m)**: Baixa resolução causa oscilações lentas → reduzir scale factor

### Flow Sensors/Cameras

1. **ARK Flow** (DroneCAN)
   - PAW3902 optical flow sensor
   - Broadcom AFBR-S50LV85D 30m distance sensor
   - Invensense ICM-42688-P IMU
   - All-in-one

2. **ARK Flow MR** (Mid-Range)
   - PixArt PAA3905 optical flow sensor
   - Broadcom AFBR-S50LX85D 50m distance sensor
   - Invensense IIM-42653 IMU

3. **Holybro H-Flow** (DroneCAN)
   - PixArt PAA3905 optical flow
   - Broadcom AFBR-S50LV85D distance sensor
   - ICM-42688-P IMU
   - Infrared LED para low-light

4. **PMW3901-Based Sensors**
   - Similar a mouse sensor
   - Works 80mm to infinity
   - Bitcraze, Tindie, Hex, Thone, Alientek

### Distance Sensor Preference
- **LIDAR recommended** over sonar
- Robustez e precisão superiores
- Qualquer distance sensor suportado funciona

## EKF2 Configuration

- **EKF2_OF_CTRL**: Habilita optical flow fusion
- **EKF2_OF_POS_X/Y/Z**: Offset do optical flow do CG
- Offset é relativo ao body frame

### EKF2 Optical Flow Fusion
- Fusion com outras fontes de velocidade
- Parâmetros de posição importantes para precisão
- Consulte EKF2 Optical Flow tuning para detalhes

## Insights

1. **All-in-one > separados**: ARK Flow/H-Flow simplifica instalação
2. **LIDAR > sonar**: Precisão e robustez superiores
3. **Offset matters**: Configurar POS_X/Y/Z corretamente
4. **Scale factor tuning**: Pode resolver oscilações em altitude alta
5. **GNSS-denied navigation**: Principal use case

## Use Cases

1. **Indoor flight**: Sem GPS
2. **Underground mining**: GNSS denied
3. **Urban canyons**: GPS bloqueado
4. **Precision hover**: Complementa GPS

## Conexões

- Complementa rangefinder para posição
- Base para EKF velocity estimation
- Alternativa ao GPS para velocidade
- Requer IMU + distance sensor para funcionar