# Síntese: Sensores para Drones

**Data de Conclusão:** 2026-03-10
**Fontes Estudadas:** 36
**Tempo de Estudo:** ~45 minutos

---

## Visão Geral

Este documento sintetiza o conhecimento adquirido sobre sensores para drones, cobrindo desde IMUs básicos até sistemas RTK de alta precisão. O foco principal foi a documentação PX4 e papers acadêmicos sobre IMU noise e fusão de sensores.

---

## Categorias de Sensores

### 1. IMU (Inertial Measurement Unit)

#### Componentes Obrigatórios
| Sensor | Função | Unidades |
|--------|--------|----------|
| **Acelerômetro** | Aceleração linear | m/s² |
| **Giroscópio** | Taxa de rotação | rad/s |
| **Magnetômetro** | Heading/Direção | µT |
| **Barômetro** | Altitude (pressão) | Pa |

#### Características Críticas
- **Noise Density**: Densidade espectral de ruído (°/s/√Hz)
- **Bias Stability**: Estabilidade do bias ao longo do tempo
- **Temperature Effects**: Variação com temperatura (requer calibração térmica)
- **Vibration Sensitivity**: Sensibilidade a vibrações do motor

#### Seleção de IMU
1. **High-end**: IMUs industriais (bias < 0.01°/s/hr)
2. **Mid-range**: MEMS capacitivos (bias ~1-10°/s)
3. **Low-cost**: MEMS MEMS básicos (bias > 10°/s)

#### Redundância
- Múltiplos IMUs melhoram robustez
- Fusão heterogênea combina sensores de diferentes qualidades
- PX4 suporta até 3 IMUs simultâneos

### 2. GNSS/GPS

#### Níveis de Precisão
| Tipo | Precisão | Aplicação |
|------|----------|-----------|
| **GPS Standard** | ~2-5m | Navegação básica |
| **DGPS** | ~0.5-2m | Melhor precisão |
| **RTK Float** | ~0.2-0.5m | Surveying |
| **RTK Fixed** | ~1-2cm | Alta precisão |

#### Dual-Antenna Heading
- **Benefício**: Elimina dependência de magnetômetro
- **Distância mínima**: ~50cm entre antenas
- **Configuração**: EKF2_GPS_CTRL bit 3 = 1
- **Devices**: u-blox F9P dual, Septentrio, Trimble MB-Two

#### Considerações
- EPH/EPV são métricas melhores que DOP para precisão real
- Position fusion só começa após yaw alignment
- RTK requer Survey-In (vários minutos)

### 3. Optical Flow

#### Princípio
- Câmera downward-facing + distance sensor
- Estima velocidade sem GPS
- Funciona indoor, underground, GNSS-denied

#### Configuração
- **SENS_FLOW_SCALE**: Ajusta escala do fluxo
- **EKF2_OF_POS_X/Y/Z**: Offset do CG
- **EKF2_OF_CTRL**: Habilita fusão

#### Sensores Populares
- ARK Flow (DroneCAN, all-in-one)
- Holybro H-Flow
- PMW3901-based sensors

### 4. Rangefinders (Distance Sensors)

#### Tecnologias
| Tipo | Range | Precisão | Ambiente |
|------|-------|----------|----------|
| **LIDAR** | 0.1-120m | Alta | Indoor/outdoor |
| **ToF IR** | 0.08-50m | Média | Indoor/outdoor |
| **Ultrasonic** | 0.3-5m | Baixa | Indoor |
| **Radar** | ~50m | Alta | All weather |

#### Use Cases
- Terrain following
- Precision hover
- Improved landing
- Height limit (regulatory)
- Collision prevention

### 5. Airspeed Sensors

#### Importância
- **CRÍTICO para fixed-wing e VTOL**
- **Único meio de detectar stall**
- Velocidade do ar ≠ velocidade de solo

#### Tecnologias
- **Pitot tube**: MS4525DO, MS5525DSO (mais comum)
- **Sensirion SDP3x**: Mais moderno, leve
- **DroneCAN**: Interface mais robusta

#### Configuração
- **ASPD_PRIMARY**: Seleciona sensor primário
- **SENS_EN_MS4525DO**: Habilita sensor

### 6. Barômetro

#### Função Principal
- Estimativa de altitude (via pressão atmosférica)
- Incluído em Pixhawk FCs

#### Auto-Calibração
- **SENS_BAR_AUTOCAL**: Alinha baro com GNSS altitude
- Requer GNSS operacional (EPV ≤ 8m)
- Salva offsets em parâmetros persistentes

### 7. Magnetômetro (Compass)

#### Importância
- Estimativa de heading
- Muito suscetível a interferência magnética
- Calibração obrigatória antes do uso

#### Boas Práticas
- Montar longe de motores/ESCs
- Usar compass externo (não apenas interno do FC)
- Calibrar em ambiente limpo magneticamente

### 8. Tachometers (RPM)

#### Status Atual
- **Logging apenas** (não usado em controle)
- Potencial futuro para monitoramento de saúde

#### Hardware
- ThunderFly TFRPM01 (I²C)
- Sensores: Hall-effect ou optical

---

## Análise de Vibração

### IMU Batch Sampling
- **INS_LOG_BAT_OPT**: Modo de sampling
- **FFT**: Transforma domínio do tempo → frequência
- Permite identificar frequências de vibração

### Harmonic Notch Filter
- Filtra frequências específicas do motor
- **INS_HNTCH_REF**: Hover throttle de referência
- **MOT_HOVER_LEARN**: Aprende automaticamente

### Workflow de Tuning
1. Setup batch sampling
2. Voo de 1+ minuto (não apenas hover)
3. Análise FFT no Mission Planner
4. Configurar notch filter
5. Voo de confirmação

---

## Calibração de Sensores

### Calibrações Obrigatórias
1. **Accelerometer**: Antes do primeiro voo
2. **Gyroscope**: Antes do primeiro voo
3. **Compass**: Antes do primeiro voo
4. **Airspeed**: Antes do primeiro voo (fixed-wing)

### Calibração Térmica
- Compensa variação de temperatura
- IMU Factory Calibration: Salva em storage persistente

### Calibração de Barômetro
- Auto-calibração com GNSS
- Relative calibration: Sensores secundários vs primário

---

## EKF2 e Fusão de Sensores

### Fontes de Dados
- **Position**: GNSS, Optical Flow, Rangefinder
- **Velocity**: Optical Flow, GNSS doppler
- **Heading**: Magnetômetro, GPS dual-antenna
- **Altitude**: Barômetro, GNSS, Rangefinder

### Parâmetros Críticos
- **EKF2_GPS_V_NOISE**: Ruído de velocidade GPS
- **EKF2_GPS_P_NOISE**: Ruído de posição GPS
- **EKF2_OF_CTRL**: Optical flow fusion
- **EKF2_BARO_CTRL**: Barômetro como fonte de altura

---

## Conexões com Outros Tópicos

| Tópico | Relação |
|--------|---------|
| **ardupilot-ekf** | Fusão de sensores no estimador |
| **drone-vibration** | Análise de vibração dos sensores |
| **flight-modes** | Requisitos de sensores por modo |
| **mission-planning** | Requisitos para missões |

---

## Próximos Passos

1. **Estudar EKF2 em detalhe**: Algoritmo de fusão
2. **Comparar com ArduPilot**: Diferenças de implementação
3. **Pesquisar sensores industriais**: IMUs de alta precisão
4. **Calibração avançada**: Métodos e ferramentas

---

## Referências Principais

1. PX4 Sensor Documentation (docs.px4.io)
2. ArduPilot IMU Batch Sampling
3. MEMS IMU Noise Characteristics (papers)
4. Sensor Fusion for UAV Navigation (papers)

---

*Gerado automaticamente pelo agente de aprendizado contínuo.*