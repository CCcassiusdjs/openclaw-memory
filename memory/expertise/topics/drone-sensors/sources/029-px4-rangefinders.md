# PX4 Distance Sensors (Rangefinders)

**Source:** https://docs.px4.io/main/en/sensor/rangefinders
**Date:** 2026-03-10
**Status:** completed

## Summary

Sensores de distância (rangefinders) medem distância até objetos/solo. Usados para terrain following, precision hover, pouso melhorado, limite de altura regulatório, e collision prevention.

## Conceitos-Chave

### Tecnologias de Rangefinder

| Tecnologia | Exemplo | Range | Conexão | Notas |
|------------|---------|-------|---------|-------|
| **Microwave Radar** | Ainstein US-D1 | ~50m | UART | All weather, all terrain |
| **ToF IR (Time-of-Flight)** | ARK DIST SR | 8cm-30m | DroneCAN/UART | Fast, accurate |
| **ToF IR Laser** | LightWare SF11 | ~120m | UART/I2C | Long range |
| **Ultrasonic** | MaxBotix MaxSonar | Curto | I2C | Low cost, short range |
| **ToF IR** | TeraRanger Evo | 0.5-60m | I2C | High speed (600Hz) |

### Conexões Suportadas
- **DroneCAN/CAN**: Robusto, permite múltiplos sensores
- **UART/Serial**: Comum em sensores de alta performance
- **I2C**: Simples, mas menos robusto
- **PWM**: Alguns modelos (Lidar-Lite)

### Sensores Populares

1. **ARK DIST SR/MR** (DroneCAN, 8cm-50m)
   - Open-source
   - PX4 DroneCAN Firmware
   - Conecta via porta CAN

2. **LightWare SF11/C** (Laser, até 120m)
   - UART ou I2C
   - High-performance

3. **Benewake TFmini** (Laser, 12m)
   - Low cost, low power
   - UART

4. **Holybro VL53L1X** (ToF IR, 4m)
   - Fast (50Hz)
   - I2C
   - Miniature ToF sensor

### EKF2_RNG_* Parameters

- **EKF2_RNG_POS_X/Y/Z**: Offset do rangefinder do CG
- **EKF2_RNG_PITCH**: Ângulo (0° = down, 90° = forward)
- **EKF2_RNG_DELAY**: Latência de dados (~ms)
- **EKF2_RNG_SFE**: Range-dependent noise scaler
- **EKF2_RNG_NOISE**: Measurement noise para fusão

### Optical Flow + Rangefinder
- Alguns optical flow sensors incluem rangefinder
- Exemplo: ARK Flow, ARK Flow MR
- Combinação permite estimativa de posição indoor

## Use Cases

1. **Terrain Following**: Manter altitude constante sobre terreno variável
2. **Terrain Holding**: Hover preciso para fotografia
3. **Precision Landing**: Pouso guiado por distância
4. **Height Limit**: Alerta de limite regulatório
5. **Collision Prevention**: Detectar obstáculos

## Testing

### QGroundControl MAVLink Inspector
- Menu Q > Analyze Tools
- DISTANCE_SENSOR message
- Plot current_distance

### MAVLink Console
```bash
listener distance_sensor 5
```

## Simulation (Gazebo)

```bash
# Down-facing LIDAR (landing, terrain following)
make px4_sitl gz_x500_lidar_down

# Front-facing LIDAR (collision prevention)
make px4_sitl gz_x500_lidar_front

# 2D LIDAR (collision prevention)
make px4_sitl gz_x500_lidar_2d
```

## Insights

1. **DroneCAN > I2C**: CAN é mais robusto para ambientes de UAV
2. **Weather matters**: Radar funciona em todas condições, laser pode ter problemas
3. **Position offset**: Importante configurar offset do CG para precisão
4. **Delay tuning**: EKF precisa saber latência para fusão correta

## Conexões

- Complementa Optical Flow para posição indoor
- Base para terrain following/holding
- Usado no EKF para altitude relativa