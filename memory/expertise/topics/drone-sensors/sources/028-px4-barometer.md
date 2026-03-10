# PX4 Barometer

**Source:** https://docs.px4.io/main/en/sensor/barometer
**Date:** 2026-03-10
**Status:** completed

## Summary

Barômetros medem pressão atmosférica e são usados como sensores de altitude. PX4 seleciona automaticamente o barômetro de maior prioridade e usa para estimativa de altura.

## Conceitos-Chave

### Hardware Options
- **Pixhawk standard**: Inclui barômetro (MS5611 comum)
- **External GNSS modules**: Alguns incluem barômetro (CUAV NEO 3 Pro)
- **Drivers suportados**: BMP280, BMP388, DPS310, MS5611, MS5837, LPS22HB, MPL3115A2, etc.

### Auto-Selection
- PX4 seleciona barômetro com maior prioridade automaticamente
- Se detecta falha, faz failover para próximo sensor
- **Geralmente não requer configuração do usuário**

### Configuration Parameters
- **EKF2_BARO_CTRL**: Enable/disable baro como fonte de altura
- **CAL_BAROx_PRIO**: Prioridade de seleção de cada barômetro
- **CAL_BAROx_PRIO = 0**: Desabilita barômetro específico

### Auto-Calibration (Developers)

#### 1. Relative Calibration
- **Sempre habilitado**: Opera durante inicialização
- Estabelece offsets de correção para sensores secundários relativos ao primário
- **Benefícios:**
  - Elimina saltos de altitude ao trocar sensores
  - Leituras consistentes entre barômetros
  - Redundância transparente

#### 2. GNSS-Baro Calibration
- **SENS_BAR_AUTOCAL**: Habilitado por padrão
- Alinha altitude do barômetro com altitude absoluta do GNSS
- **Requisitos:**
  - GNSS operacional com EPV ≤ 8m
  - Relative calibration completa
- **Processo:**
  1. Monitora qualidade GNSS
  2. Coleta diferenças em janela de 2 segundos
  3. Verifica estabilidade (tolerância 4m)
  4. Calcula offsets com precisão 0.1m
  5. Salva em parâmetros (persiste após reboot)

### Limitações
- Vulnerável a dados GNSS defeituosos durante boot
- Calibração incorreta pode causar erros de altitude

## Insights

1. **Redundância automática**: PX4 gerencia múltiplos barômetros transparentemente
2. **Altitude reference**: GNSS-baro calibration alinha baro com GPS
3. **Failover**: Troca automática em falha de sensor
4. **Simplicidade**: Geralmente zero-config para usuários

## Drivers Suportados (2026)

| Driver | Modelos |
|--------|---------|
| bmp280 | BMP280 |
| bmp388 | BMP388, BMP380 |
| dps310 | DPS310 |
| ms5611 | MS5611 (comum em Pixhawk) |
| ms5837 | MS5837 |
| lps22hb | LPS22HB |
| mpl3115a2 | MPL3115A2 |

## Conexões

- Base para altitude estimation (EKF)
- Complementa GPS para altitude
- Relacionado com sensores de pressão atmosférica