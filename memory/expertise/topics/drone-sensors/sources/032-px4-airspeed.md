# PX4 Airspeed Sensors

**Source:** https://docs.px4.io/main/en/sensor/airspeed
**Date:** 2026-03-10
**Status:** completed

## Summary

Sensores de airspeed são **altamente recomendados** para fixed-wing e VTOL. O autopilot não tem outro meio de detectar stall. Para voo fixed-wing, é a velocidade do ar que garante sustentação — não a velocidade de solo!

## Conceitos-Chave

### Tecnologias

#### Pitot Tube (Differential Pressure)
- **MS4525DO / MS5525DSO**: I2C, popular
- Mede diferença de pressão estática vs dinâmica
- **Modelos:**
  - mRo I2C Airspeed Sensor JST-GH MS4525DO
  - Holybro Digital Airspeed Sensor MS4525DO / MS5525DSO
  - Drotek Digital Differential Airspeed Sensor

#### Sensirion SDP3x (I2C)
- ThunderFly TFPITOT01 Lightweight Pitot Tube
- Drotek SDP3x Airspeed Sensor Kit
- Mais moderno, leve

#### DroneCAN Interface
- Holybro High Precision DroneCAN Airspeed Sensor (DLVR)
- RaccoonLab Cyphal/CAN Airspeed Sensor (MS4525DO)
- Avionics Anonymous Air Data Computer (com OAT probe)
- Interface mais robusta

#### Venturi Effect
- **TFSLOT**: Sensor alternativo baseado em Venturi

### Configuration

#### Enable Parameters
- **SENS_EN_SDP3X**: Sensirion SDP3X
- **SENS_EN_MS4525DO**: TE MS4525
- **SENS_EN_MS5525DS**: TE MS5525
- **SENS_EN_ETSASPD**: Eagle Tree airspeed
- **ASPD_PRIMARY**: 1 (default) = primeiro sensor

#### Multiple Airspeed Sensors (Experimental)
- **ASPD_PRIMARY**: Seleciona sensor preferido
  - 0: Synthetic airspeed (groundspeed - windspeed)
  - 1: Primeiro sensor (default)
  - 2: Segundo sensor
  - 3: Terceiro sensor
- Fallback automático se sensor primário falhar
- **ASPD_DO_CHECKS**: Configura validação

#### Sensor-Specific
- **CAL_AIR_CMODEL**: Calibration model
- **CAL_AIR_TUBED_MM**: Tube diameter (mm)
- **CAL_AIR_TUBELEN**: Tube length

### Calibration
- Seguir: Basic Configuration > Airspeed
- Validação avançada: Airspeed Validation

## Insights

1. **Stall detection**: Airspeed é ÚNICO meio de detectar stall
2. **Lift = airspeed, not groundspeed**: Conceito crítico para fixed-wing
3. **Pitot tube > Venturi**: Mais comum, mais testado
4. **DroneCAN robust**: Interface mais resistente a ruído
5. **Multiple sensors**: Experimental mas útil para redundância

## Warning

- **VTOL sem airspeed**: Possível, mas requer configuração especial
- Ver documentação: VTOL Without an Airspeed Sensor

## Conexões

- Crítico para fixed-wing e VTOL
- Base para controle de stall
- Integração com EKF2 para fusão