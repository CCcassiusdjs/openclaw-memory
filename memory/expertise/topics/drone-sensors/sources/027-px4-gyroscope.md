# PX4 Gyroscope

**Source:** https://docs.px4.io/main/en/sensor/gyroscope
**Date:** 2026-03-10
**Status:** completed

## Summary

PX4 usa giroscópio para estimar atitude (orientação) do veículo. Incluído em flight controllers Pixhawk como parte do IMU.

## Conceitos-Chave

### Inclusion in IMU
- Pixhawk FCs incluem giroscópio no IMU
- External INS/AHRS/GNSS também incluem

### Use in PX4
- Estimativa de atitude (orientação)
- Parte do state estimation
- Não é dispositivo standalone externo

### Calibration
- **Obrigatório**: Calibração antes do primeiro uso
- Processo via Gyroscope Calibration (config)

## Insights

- Giroscópio é senso comum em FCs modernos
- Calibração é pré-requisito
- Funciona junto com acelerômetro para attitude estimation