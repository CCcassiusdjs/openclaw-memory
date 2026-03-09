# MultiRad EKF Dataset Analysis - 2026-03-09

## Cenário Inicial do Drone

### Estado de Voo
**Situação:** Drone em repouso sobre superfície horizontal

| Parâmetro | Valor | Interpretação |
|-----------|-------|---------------|
| Velocidade | 0 m/s (N, E, D) | Estacionário |
| Aceleração X/Y | 0 m/s² | Sem movimento lateral/longitudinal |
| Aceleração Z | -9.8 m/s² | Gravidade (eixo Z body aponta para baixo) |
| Giroscópio | 0 rad/s (X, Y, Z) | Sem rotação |
| Throttle (ch3) | 1000 µs | Motores desligados |

### Atitude Estimada
- **PITCH ≈ 0°** (nível)
- **ROLL ≈ 0°** (nível)
- **YAW ≈ 0°** (apontando Norte)

**Eixos de referência:**
- X body = Frente do drone
- Y body = Lateral direito
- Z body = Para baixo (perpendicular à fuselagem)

### Posição GPS
- **Localização:** Porto Alegre, RS, Brasil
- **Coordenadas:** -30.034647°, -51.217658°
- **Altitude GPS:** 100 metros
- **Altitude Barômetro:** 10 metros
- **Diferença:** 90m (offset de calibração ou referência diferente)

### Campo Magnético Terrestre
- **Bx = 200 mG** (horizontal, X - Norte)
- **By = 0 mG** (horizontal, Y - Leste)
- **Bz = 400 mG** (vertical, para baixo)
- **Magnitude total:** ≈ 447 mG
- **Inclinação:** ≈ 63° (hemisfério sul)

### Estado dos Sensores

| Sensor | Status | Observação |
|--------|--------|------------|
| IMU 0 | ✅ OK | Dados limpos, sem ruído |
| IMU 1 | ✅ OK | Offset de +0.001 em todos os valores |
| IMU 2 | ✅ OK | Offset de +0.002 em todos os valores |
| GPS | ✅ OK | 14 satélites, HDOP 0.8, fix estático |
| BARO 0 | ✅ OK | Altitude 10m, ruído σ ≈ 5.7cm |
| BARO 1 | ✅ OK | Offset +10cm |
| BARO 2 | ✅ OK | Offset +20cm |
| MAG 0 | ✅ OK | Campo magnético consistente |
| MAG 1 | ✅ OK | Offset +1 mG em cada componente |
| MAG 2 | ✅ OK | Offset +2 mG em cada componente |

## Arquitetura do Sistema

### Componentes Principais

#### 1. Data Orchestrator (Gerador de Datasets)
- Gera CSVs sintéticos de sensores (IMU, GPS, BARO, MAG, PWM)
- Timeline com taxas configuráveis
- Modelos de movimento (quaternions, NED→LLA)

#### 2. Case Runner (Executor de Testes)
- Validação de paths e arquitetura ELF (x86_64, aarch64, armv7l, riscv64)
- fork/exec + LD_PRELOAD para emulação
- 30+ códigos de erro específicos

#### 3. Output Vector Extractor
- Parser de log de runtime
- Extrai flags de status dos sensores
- Detecta "Init ArduCopter", "Timing Summary", erros

### Estrutura dos CSVs

```
imu.csv (400 Hz/instância, 3 instâncias):
time_ms, gyro_index, accel_index, delAng_x/y/z, delAngDT,
         delVel_x/y/z, delVelDT, accel_x/y/z, gyro_x/y/z

gps.csv (10 Hz):
time_ms, lat, lng, alt_cm, hgt_m, velN/E/D, have_vz, sensor_idx,
         hacc_m, vacc_m, sacc_mps, hdop, num_sats, lag_sec,
         yaw_deg, yaw_accuracy_deg, yaw_time_ms

baro.csv (50 Hz/instância, 3 instâncias):
time_ms, alt_m, instance, healthy

mag.csv (50 Hz/instância, 3 instâncias):
time_ms, field_x/y_z_mG, instance, healthy, use_for_yaw,
         ofs_x/y_z_mG

pwm.csv (50 Hz):
time_us, ch1-16
```

### Taxas de Amostragem

| Sensor | Taxa por Instância | Instâncias | Taxa Total |
|--------|-------------------|------------|------------|
| IMU | ~400 Hz | 3 | ~1200 Hz |
| GPS | ~10 Hz | 1 | ~10 Hz |
| BARO | ~50 Hz | 3 | ~150 Hz |
| MAG | ~50 Hz | 3 | ~150 Hz |
| PWM | ~50 Hz | 1 | ~50 Hz |

## Output Vector (Interface MultiRad)

```c
typedef struct {
  float pos_error_ned_m[3];     // Erro de posição NED
  float att_error_rpy_deg[3];   // Erro de atitude RPY
  uint32_t ekf_flags;           // Bitmask de diagnóstico
  uint8_t armed_successfully;   // Flag de arming
  uint32_t total_gps_drops;     // Contador de GPS drops
} output_vector_type;  // 24 bytes
```

### Flags de Status (ekf_flags)

| Bit | Nome | Significado |
|-----|------|-------------|
| 0 | ProcessOk | Processo executou com sucesso |
| 1 | LogParsed | Log de runtime foi parseado |
| 2 | ArducopterInitSeen | "Init ArduCopter" detectado |
| 3 | ReplayWindowComplete | Replay terminou |
| 4 | GpsReplayOk | GPS replay OK |
| 5 | ImuReplayOk | IMU replay OK |
| 6 | BaroReplayOk | BARO replay OK |
| 7 | MagReplayOk | MAG replay OK |
| 8 | TimingSummarySeen | Timing summary detectado |
| 9 | NoEmulatorErrors | Sem erros do emulador |
| 10 | ArmedSeen | Arming detectado |
| 31 | RunFailed | Falha geral |

**Sucesso:** flags=0x000007FF, armed=1, gps_drops=0

## Parâmetros do ArduCopter (defaults.param)

```
# Logging desabilitado
LOG_BACKEND_TYPE 0
LOG_DISARMED 0
LOG_FILE_DSRMROT 0

# GPS em Serial3
SERIAL3_PROTOCOL 5
SERIAL3_BAUD 115

# Telemetria desabilitada
SERIAL0_PROTOCOL -1

# LEDs desabilitados
NTF_LED_TYPES 0

# Bateria desabilitada
BATT_MONITOR 0

# Compass calibrado
COMPASS_OFS_X/Y/Z 0
COMPASS_EXTERNAL 0
COMPASS_USE 1

# EKF3 habilitado
EK3_ENABLE 1
AHRS_EKF_TYPE 3

# Arming checks desabilitados
ARMING_CHECK 0

# Frame Quad X
FRAME_CLASS 1
FRAME_TYPE 1

# Loop rate
SCHED_LOOP_RATE 400
```

## Propósito do Dataset

### Objetivos
1. ✅ Verificar inicialização do EKF3 com sensores redundantes
2. ✅ Validar fusão de 3 IMUs, 3 BAROs, 3 MAGs
3. ✅ Testar arming com ARMING_CHECK=0
4. ✅ Verificar convergência do EKF para atitude correta (nível)
5. ✅ Validar emulação de sensores (libioctl_shim.so)

### Limitações
- ⚠️ Drone estático (sem dinâmica de voo)
- ⚠️ Intervalo IMU variável (não uniforme)
- ⚠️ Duração curta (10 segundos)
- ⚠️ Offset artificial entre instâncias de sensores

### NÃO Adequado Para
- ❌ Teste de voo dinâmico
- ❌ Teste de resposta a manobras
- ❌ Teste de navegação GPS
- ❌ Teste de resistência a falhas (sensores perfeitos)

## Localização dos Arquivos

```
/home/csilva/Documents/multirad_data_orchestrator/
├── case-study_algorithms/drone/arducopter-ekf/
│   ├── data/                    # CSVs de input
│   │   ├── imu.csv              # 12,001 linhas
│   │   ├── gps.csv              # 101 linhas
│   │   ├── baro.csv             # 1,501 linhas
│   │   ├── mag.csv              # 1,501 linhas
│   │   └── pwm.csv              # 501 linhas
│   ├── runtime/
│   │   ├── datasets/            # Cópia dos CSVs
│   │   ├── checkers_results/    # Resultados
│   │   └── sets_of_output_vectors/
│   └── arducopter/              # Código fonte
│       ├── include/arducopter_ekf/
│       │   ├── case_runner.h
│       │   ├── output_vector_extractor.h
│       │   └── case_study_algorithm_application.h
│       └── src/
│           ├── case_runner.c
│           ├── output_vector_extractor.c
│           └── case_study_algorithm_application.c
└── data_orchestrator/
    └── computer/
        ├── include/core/
        │   ├── orchestrator.h
        │   └── timeline.h
        └── src/synth/
            ├── imu.c, gps.c, baro.c, mag.c
            └── models.c, emit.c
```

## Próximos Passos Sugeridos

1. Analisar o emulador de sensores (libioctl_shim.so)
2. Verificar integração com ArduCopter EKF3
3. Estudar casos de falha (injeção de erros)
4. Documentar arquitetura de injeção de falhas por radiação

---
_Source: Análise detalhada dos CSVs de input do case EKF em 2026-03-09_