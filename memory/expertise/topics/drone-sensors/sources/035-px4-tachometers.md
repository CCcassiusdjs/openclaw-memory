# PX4 Tachometers (Revolution Counters)

**Source:** https://docs.px4.io/main/en/sensor/tachometers
**Date:** 2026-03-10
**Status:** completed

## Summary

Tacômetros (revolution counters) medem taxa de rotação de partes do veículo: rotores, motores, rodas. **Atualmente PX4 apenas loga dados RPM — não é usado para state estimation ou controle.**

## Hardware Suportado

- **ThunderFly TFRPM01**: Tacômetro I²C para PX4

## Uso Atual

- Logging apenas
- Não usado em EKF
- Não usado em controle

## Conexões

- Potencial para monitoramento de saúde de motores
- Logging para análise pós-voo