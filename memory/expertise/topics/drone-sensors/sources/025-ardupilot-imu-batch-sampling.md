# ArduPilot IMU Batch Sampler & FFT Analysis

**Source:** https://ardupilot.org/copter/docs/common-imu-batchsampling.html
**Date:** 2026-03-10
**Status:** completed

## Summary

IMU BatchSampler registra dados de alta frequência dos sensores IMU para análise pós-voo. FFT (Fast Fourier Transform) converte dados do domínio do tempo para frequência, permitindo identificar picos de vibração.

## Conceitos-Chave

### FFT e Análise de Frequência
- **FFT** transforma dados de tempo em frequência
- Mostra frequências de vibração (nível de ruído por frequência)
- **Limitações:**
  - Não detecta frequências acima de metade da taxa de amostragem (Nyquist)
  - Menor frequência detectável = (metade do tamanho da amostra) / taxa de amostragem

### Taxas de Amostragem
- **Sensor rate**: Ex: MPU9250 a 8KHz (com downsampling para 1KHz)
- **Backend rate**: Taxa de filtro do giroscópio (1KHz padrão)
- **INS_GYRO_RATE**: Configura backend rate em 2^N KHz
  - 0 = 1KHz (padrão)
  - 1 = 2KHz
  - Filtros rodam na backend rate (computacionalmente caro)
  - Recomendado apenas em F7/H7

### Aliasing
- Em copters pequenos, 1KHz não é suficiente
- Motor de 3" pode ter frequência de 600Hz
- Ruído acima de 500Hz sofre aliasing para frequências mais baixas
- Solução: Aumentar backend rate

### Parâmetros de Configuração
- **INS_LOG_BAT_OPT**: Modo de sampling
  - 4 = pre e post-filter 1KHz
  - 2 = post-filter gyro data
  - 1 = sensor highest rate (>500Hz para IMUs rápidos)
- **INS_LOG_BAT_MASK**: Quais IMUs amostrar (1 = primeiro IMU)
- **INS_LOG_BAT_CNT**: Número de samples (afeta menor frequência detectável)
- **INS_LOG_BAT_LGIN**: Intervalo entre batches (ms)
- **INS_LOG_BAT_LGCT**: Samples por push

### Análise de Vibração
- **Motor frequency**: Típica em 200Hz (small copter) ou 100Hz (large copter)
- **Harmônicos**: Múltiplos da frequência do motor (2x, 3x)
- **Blade passage frequency**: Frequência onde hélice passa sobre braços
- **Gyro lowpass**: 20Hz padrão, pode aumentar para 60-80Hz após notch

### Harmonic Notch Filter
- Filtra frequências específicas do motor
- **INS_HNTCH_REF**: Hover throttle de referência
- **MOT_HOVER_LEARN**: Aprende hover thrust automaticamente
- Dynamic notch segue frequência do motor

## Insights Práticos

1. **Identificação de problemas**: Peak em 180Hz no acelerômetro indica vibração do motor
2. **Lowpass tradeoff**: Filtro mais baixo = menos ruído mas mais phase lag
3. **Gyro crítico**: Camada interna de controle, mais sensível a phase lag
4. **Accel secundário**: Outer loop, pode manter filtro em 10Hz
5. **H7 advantage**: Raw IMU logging disponível para análise detalhada

## Workflow de Tuning

1. Setup: INS_LOG_BAT_OPT=4, INS_LOG_BAT_MASK=1
2. Voo de 1+ minuto (não apenas hover)
3. Análise FFT no Mission Planner
4. Identificar pico de frequência do motor
5. Configurar harmonic notch filter
6. Voo de confirmação com INS_LOG_BAT_OPT=2
7. Reset INS_LOG_BAT_MASK=0 após análise

## Ferramentas

- **Mission Planner FFT Button**: SETUP/ADVANCED > FFT > IMU Batch Sample
- **pymavlink mavfft_isb.py**: Análise via CLI
- **Web Notch Filter Review Tool**: firmware.ardupilot.org/Tools/WebTools/FilterReview/

## Conexões

- Relacionado com IMU noise (fonte 016-018)
- Conecta com EKF tuning
- Base para notch filter configuration