# PX4 Accelerometer

**Source:** https://docs.px4.io/main/en/sensor/accelerometer
**Date:** 2026-03-10
**Status:** completed

## Summary

PX4 usa dados do acelerômetro para estimativa de velocidade. Acelerômetros já estão incluídos em flight controllers Pixhawk como parte do IMU.

## Conceitos-Chave

### Inclusion in IMU
- Flight controllers Pixhawk incluem acelerômetro no IMU
- External INS/AHRS/GNSS systems também incluem giroscópio

### Calibration
- **Obrigatório**: Calibração antes do primeiro uso
- Processo via Accelerometer Calibration (config)

### Use in PX4
- Estimativa de velocidade
- Parte do state estimation (EKF)
- Não é dispositivo standalone externo

## Insights

- Acelerômetro é senso comum em FCs modernos
- Não precisa conectar acelerômetro externo separado
- Calibração é pré-requisito para funcionamento correto

## Conexões

- Parte do IMU junto com giroscópio
- Base para EKF state estimation