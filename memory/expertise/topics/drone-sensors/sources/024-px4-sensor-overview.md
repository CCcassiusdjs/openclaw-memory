# PX4 Sensor Hardware & Setup

**Source:** https://docs.px4.io/main/en/sensor/
**Date:** 2026-03-10
**Status:** completed

## Summary

Visão geral dos sensores obrigatórios e opcionais em sistemas PX4. PX4 requer no mínimo giroscópio, acelerômetro, magnetômetro e barômetro para estimar estado do veículo.

## Conceitos-Chave

### Sensores Obrigatórios (inclusos em Pixhawks)
1. **Acelerômetro** - Mede aceleração linear
2. **Giroscópio** - Mede orientação (taxa de rotação)
3. **Magnetômetro (Compass)** - Mede heading/direção
4. **Barômetro** - Mede altitude (via pressão do ar)

### Sensores Recomendados
1. **Airspeed Sensor** - Mede velocidade do ar. CRÍTICO para VTOL/Fixed-wing (detecta stall)
2. **GNSS (GPS)** - Posição global. Necessário para missões e modos automáticos
3. **RTK GNSS** - Precisão centimétrica. Pode determinar heading sem magnetômetro

### Sensores Opcionais
1. **Distance Sensors (Rangefinders)** - Distância até alvo. Auxilia pouso, obstacle avoidance, terrain following
2. **Optical Flow** - Estimativa de velocidade com câmera + sensor de distância apontados para baixo. Mais preciso que GPS sozinho, funciona indoor sem GPS
3. **Tachometers** - Contadores de revolução (apenas para logging)

### Calibração
- **IMU Factory Calibration** - Salva calibração em storage persistente
- **Sensor Thermal Compensation** - Compensa variações de temperatura

## Insights

- PX4 estima estado do veículo para estabilização e controle autônomo
- Estado inclui: posição/altitude, heading, velocidade, atitude, taxas de rotação, nível de bateria
- Magnetômetro EXTERNO é recomendado (não apenas interno)
- Airspeed sensor é único mecanismo para detectar stall em VTOL/Fixed-wing
- RTK GNSS pode substituir magnetômetro para heading (dual antenna)
- Optical flow precisa de sensor de distância + câmera para baixo

## Conexões

- Requer conhecimento de IMU noise (tópico anterior)
- Conecta com EKF (ardupilot-ekf)
- Base para calibração de sensores

## Próximos Passos

- Estudar cada sensor em detalhe
- Entender calibração térmica
- Comparar com ArduPilot sensor setup