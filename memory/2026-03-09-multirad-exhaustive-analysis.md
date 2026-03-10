# MultiRad + EKF Platform - Análise Exaustiva

## 1. Visão Geral da Plataforma

### 1.1 Estrutura de Diretórios

```
/home/csilva/Documents/multirad_data_orchestrator/
├── case-study_algorithms/
│   ├── drone/
│   │   ├── arducopter-ekf/          # Case EKF (este projeto)
│   │   └── mobilenet-x1-multirad/    # Case MobileNet
│   ├── edge/                         # Case Edge
│   └── multirad/                      # Plataforma MultiRad
│       ├── common/                    # Código comum
│       │   ├── multirad.h
│       │   ├── multirad_checkers.h
│       │   ├── multirad_interface.h
│       │   ├── multirad_time.h
│       │   └── multirad_user.h
│       ├── bare_metal/                # Versão bare-metal
│       ├── linux/                     # Versão Linux
│       └── sensors/                   # Versão com sensores
│
└── data_orchestrator/
    └── raspberry/
        └── arducopter/
            └── libraries/
                ├── AP_NavEKF/         # EKF Original (2,333 linhas)
                ├── AP_NavEKF2/        # EKF2 (12,469 linhas)
                └── AP_NavEKF3/        # EKF3 (17,215 linhas)
```

---

## 2. Libraries EKF - Comparação

### 2.1 EKF (Original) - 2,333 linhas

| Arquivo | Linhas | Função |
|---------|--------|--------|
| AP_NavEKF_Source.cpp | 611 | Fonte de dados de navegação |
| EKFGSF_yaw.cpp | 668 | Filtro Gaussiano para yaw |
| AP_NavEKF_core_common.cpp | 35 | Código comum |
| EKF_Buffer.cpp | 202 | Buffer circular |
| LogStructure.h | 88 | Estruturas de log |

**Características:**
- Versão inicial do EKF
- Filtro único (sem redundância)
- 15 estados básicos

### 2.2 EKF2 - 12,469 linhas

| Arquivo | Linhas | Função |
|---------|--------|--------|
| AP_NavEKF2_core.cpp | 1,689 | Core do filtro |
| AP_NavEKF2.cpp | 1,604 | Frontend |
| AP_NavEKF2_PosVelFusion.cpp | 1,119 | Fusão GPS |
| AP_NavEKF2_MagFusion.cpp | 1,270 | Fusão magnetômetro |
| AP_NavEKF2_Measurements.cpp | 1,092 | Medidas |
| AP_NavEKF2_OptFlowFusion.cpp | 728 | Fluxo óptico |
| AP_NavEKF2_RngBcnFusion.cpp | 574 | Ranging beacon |
| AP_NavEKF2_Outputs.cpp | 585 | Saídas |
| AP_NavEKF2_AirDataFusion.cpp | 425 | Dados de ar |
| AP_NavEKF2_Control.cpp | 566 | Controle |
| AP_NavEKF2_VehicleStatus.cpp | 443 | Status |
| AP_NavEKF2_Logging.cpp | 339 | Logging |
| AP_NavEKF2_core.h | 1,218 | Header |
| AP_NavEKF2.h | 480 | Header |

**Características:**
- 2 cores paralelos
- Votação entre cores
- 24 estados

### 2.3 EKF3 - 17,215 linhas

| Arquivo | Linhas | Função |
|---------|--------|--------|
| AP_NavEKF3_core.cpp | 2,272 | Core do filtro (maior) |
| AP_NavEKF3.cpp | 2,164 | Frontend + seleção de core |
| AP_NavEKF3_PosVelFusion.cpp | 2,116 | Fusão GPS (maior) |
| AP_NavEKF3_core.h | 1,666 | Estado + estruturas |
| AP_NavEKF3_MagFusion.cpp | 1,635 | Fusão magnetômetro |
| AP_NavEKF3_Measurements.cpp | 1,544 | Medidas |
| AP_NavEKF3_OptFlowFusion.cpp | 789 | Fluxo óptico |
| AP_NavEKF3_AirDataFusion.cpp | 714 | Dados de ar |
| AP_NavEKF3_Outputs.cpp | 678 | Saídas + errorScore |
| AP_NavEKF3_RngBcnFusion.cpp | 688 | Ranging beacon |
| AP_NavEKF3_Control.cpp | 881 | Controle |
| AP_NavEKF3_VehicleStatus.cpp | 482 | Status |
| AP_NavEKF3_Logging.cpp | 456 | Logging |
| AP_NavEKF3_GyroBias.cpp | 24 | Bias do giroscópio |

**Características:**
- **3 cores paralelos** (redundância tripla)
- Votação baseada em `errorScore`
- 24 estados + estados auxiliares
- Fusão de 9+ sensores

---

## 3. EKF3 - Arquitetura Detalhada

### 3.1 Estados (24 estados)

```cpp
struct stateStruct {
    Vector3F position;      // [0-2]   posN, posE, posD (NED)
    Vector3F velocity;      // [3-5]   velN, velE, velD (NED)
    Vector3F gyro_bias;     // [6-8]   bias do giroscópio
    Vector3F accel_bias;    // [9-11]  bias do acelerômetro
    Vector3F wind;          // [12-14] velocidade do vento (NED)
    Vector3F mag_bias;      // [15-17] bias do magnetômetro
    Vector3F earth_mag;     // [18-20] campo magnético terrestre
    Vector3F body_mag;      // [21-23] campo magnético no corpo
    ftype   yaw_glitch;     // glitch de yaw
    // ... estados auxiliares
};
```

### 3.2 Fusão de Sensores

| Sensor | Taxa | Fusão | Arquivo |
|--------|------|-------|---------|
| GPS (NMEA) | 10 Hz | Posição/Velocidade | PosVelFusion.cpp |
| IMU (ICM20602) | 400 Hz | δângulo/δvelocidade | core.cpp |
| BARO (BMP280) | 50 Hz | Altitude | Measurements.cpp |
| MAG (AK09916) | 50 Hz | Yaw | MagFusion.cpp |
| Optical Flow | 10 Hz | Velocidade visual | OptFlowFusion.cpp |
| Airspeed | 10 Hz | Velocidade do ar | AirDataFusion.cpp |
| Ranging Beacon | 10 Hz | Posição | RngBcnFusion.cpp |

### 3.3 Seleção de Core (Voting)

```cpp
// Cálculo do errorScore
float NavEKF3_core::errorScore() const {
    float score = 0.0f;
    if (tiltAlignComplete && yawAlignComplete) {
        score = MAX(score, 0.5f * (velTestRatio + posTestRatio));
        score = MAX(score, hgtTestRatio);
        if (assume_zero_sideslip()) {
            score = MAX(score, 0.3f * tasTestRatio);
        }
        if (frontend->_affinity & EKF_AFFINITY_MAG) {
            score = MAX(score, 0.3f * (magTestRatio.x + magTestRatio.y + magTestRatio.z));
        }
    }
    return score;
}

// Troca de core
void NavEKF3::updateCoreRelativeErrors() {
    for (uint8_t i = 0; i < num_cores; i++) {
        if (i != primary) {
            float error = coreErrorScores[i] - coreErrorScores[primary];
            if (error > 0 || error < -MAX(_err_thresh, 0.05)) {
                coreRelativeErrors[i] += error;
                coreRelativeErrors[i] = constrain(coreRelativeErrors[i], -1.0, 1.0);
            }
        }
    }
}
```

**Condição de troca:**
- `primaryErrorScore > 1.0f` (erro alto)
- OU `!core[primary].healthy()` (core doente)
- OU `betterCore` (erro relativo < -BETTER_THRESH)

---

## 4. MultiRad Platform

### 4.1 Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ccX (Control Computer)                      │
│                     Linux/x86_64 ou similar                       │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                 MultiRad Platform                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │  │
│  │  │ checkers.c  │  │  time.c     │  │ interface.c │         │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘         │  │
│  │                                                              │  │
│  │  multirad_platform_radiation_tests()                        │  │
│  │       │                                                      │  │
│  │       ▼                                                      │  │
│  │  for each cluster:                                           │  │
│  │    for each run:                                             │  │
│  │      - execute case_study_algorithm_application()            │  │
│  │      - capture output_vector                                 │  │
│  │      - calculate checksums                                   │  │
│  │      - compare with reference                                │  │
│  │      - log error codes                                       │  │
│  │                                                              │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                     │
└──────────────────────────────│─────────────────────────────────────┘
                               │
                               │ UART/Serial
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         sut4 (System Under Test)                    │
│                      Raspberry Pi / ARM Cortex-A                     │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                   Case Study Algorithm                        │  │
│  │                                                              │  │
│  │  ┌───────────────────────────────────────────────────────┐   │  │
│  │  │              arducopter-ekf Case                         │   │  │
│  │  │                                                         │   │  │
│  │  │  case_runner.c:                                         │   │  │
│  │  │    - fork/exec arducopter binary                        │   │  │
│  │  │    - LD_PRELOAD=libioctl_shim.so                        │   │  │
│  │  │    - EMU_PREARM_DISABLED=1                              │   │  │
│  │  │    - wait for completion                                │   │  │
│  │  │                                                         │   │  │
│  │  │  output_vector_extractor.c:                              │   │  │
│  │  │    - parse arducopter_runtime.log                       │   │  │
│  │  │    - extract flags: GPS/IMU/BARO/MAG OK                  │   │  │
│  │  │    - extract armed status                                │   │  │
│  │  │    - extract error counts                                │   │  │
│  │  │                                                         │   │  │
│  │  └───────────────────────────────────────────────────────┘   │  │
│  │                              │                                │  │
│  │                              ▼                                │  │
│  │  ┌───────────────────────────────────────────────────────┐   │  │
│  │  │          ArduCopter (linux-emu board)                   │   │  │
│  │  │                                                         │   │  │
│  │  │  ┌─────────────────────────────────────────────────┐    │   │  │
│  │  │  │              AP_NavEKF3                         │    │   │  │
│  │  │  │                                                 │    │   │  │
│  │  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │    │   │  │
│  │  │  │  │ Core[0] │ │ Core[1] │ │ Core[2] │           │    │   │  │
│  │  │  │  │  IMU0   │ │  IMU1   │ │  IMU2   │           │    │   │  │
│  │  │  │  └────┬────┘ └────┬────┘ └────┬────┘           │    │   │  │
│  │  │  │       │           │           │                │    │   │  │
│  │  │  │       └───────────┼───────────┘                │    │   │  │
│  │  │  │                   │                            │    │   │  │
│  │  │  │                   ▼                            │    │   │  │
│  │  │  │           Core Selection                      │    │   │  │
│  │  │  │           (errorScore voting)                 │    │   │  │
│  │  │  │                   │                            │    │   │  │
│  │  │  └───────────────────│────────────────────────────┘    │   │  │
│  │  │                      │                                 │   │  │
│  │  └──────────────────────│─────────────────────────────────┘   │  │
│  │                         ▼                                     │  │
│  │  ┌───────────────────────────────────────────────────────┐   │  │
│  │  │           libioctl_shim.so (Emulator)                  │   │  │
│  │  │                                                        │   │  │
│  │  │  Intercepts:                                           │   │  │
│  │  │    - open("/dev/i2c-*") → virtual FD                   │   │  │
│  │  │    - open("/dev/spidev*") → virtual FD                 │   │  │
│  │  │    - ioctl(I2C_*) → sensor models                      │   │  │
│  │  │    - ioctl(SPI_*) → sensor models                      │   │  │
│  │  │    - clock_gettime() → emulated time                   │   │  │
│  │  │                                                        │   │  │
│  │  │  Sensor Models:                                        │   │  │
│  │  │    ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │  │
│  │  │    │ ICM20602 │  │  BMP280  │  │ AK09916  │           │   │  │
│  │  │  │  │  (IMU)   │  │  (BARO)  │  │  (MAG)   │           │   │  │
│  │  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘           │   │  │
│  │  │  │       │             │             │                 │   │  │
│  │  │  │       ▼             ▼             ▼                 │   │  │
│  │  │  │  ┌─────────────────────────────────────────┐       │   │  │
│  │  │  │  │            CSV Dataset Reader           │       │   │  │
│  │  │  │  │                                         │       │   │  │
│  │  │  │  │  imu.csv  baro.csv  mag.csv  gps.csv   │       │   │  │
│  │  │  │  └─────────────────────────────────────────┘       │   │  │
│  │  │  └────────────────────────────────────────────────────┘   │  │
│  │  └────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  Reset Relay ◄────────────────────────────────────────────────────│
│  (Power Cycle)                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Fluxo de Execução

```c
// multirad.c - Fluxo principal
int multirad_platform_radiation_tests(uint32_t first_run_within_program) {
    // Para cada cluster de runs
    for (index_of_cluster = 1; index_of_cluster <= total_number_of_clusters; index_of_cluster++) {
        // Para cada run dentro do cluster
        for (index_of_run_within_cluster = 1; index_of_run_within_cluster <= runs_per_cluster; index_of_run_within_cluster++) {
            
            // 1. Copia vetor de entrada
            copy_set_of_input_vectors(input_buffer);
            
            // 2. Executa algoritmo
            case_study_algorithm_application(
                input_buffer,
                output_vector,
                &input_checksum_1,
                &input_checksum_2
            );
            
            // 3. Copia vetor de saída para buffers redundantes
            copy_output_vector_to_buffer(output_buffer_1, output_vector);
            copy_output_vector_to_buffer(output_buffer_2, output_vector);
            
            // 4. Calcula checksums
            output_checksum_1 = calculate_checksum(output_buffer_1);
            output_checksum_2 = calculate_checksum(output_buffer_2);
            
            // 5. Compara com referências
            input_error_code_1 = verify_checksum(...);
            output_error_code_1 = verify_checksum(...);
            
            // 6. Log de erros
            if (error_in_run) {
                log_error(...);
            }
        }
        
        // Envia resultados para ccX
        send_cluster_results(...);
    }
    
    return exit_code;
}
```

### 4.3 Output Vector

```c
// Flags do output vector
enum {
    kOutputVectorFlagProcessOk            = 1 << 0,  // exit(0)
    kOutputVectorFlagLogParsed            = 1 << 1,  // log parseado
    kOutputVectorFlagArducopterInitSeen   = 1 << 2,  // "Init ArduCopter"
    kOutputVectorFlagReplayWindowComplete = 1 << 3,  // datasets consumidos
    kOutputVectorFlagGpsReplayOk          = 1 << 4,  // GPS OK
    kOutputVectorFlagImuReplayOk          = 1 << 5,  // IMU OK
    kOutputVectorFlagBaroReplayOk         = 1 << 6,  // BARO OK
    kOutputVectorFlagMagReplayOk         = 1 << 7,  // MAG OK
    kOutputVectorFlagTimingSummarySeen    = 1 << 8,  // timing OK
    kOutputVectorFlagNoEmulatorErrors     = 1 << 9,  // sem erros [EMU]
    kOutputVectorFlagArmedSeen            = 1 << 10, // arm detectado
};

kOutputVectorSuccessFlags = 0x000007FFU;  // todos OK
kOutputVectorFailureMask  = 0x80000000U;  // bit de falha
```

---

## 5. Resultados dos Testes de Radiação

### 5.1 Estatísticas

| Métrica | Valor |
|---------|-------|
| Execuções iniciadas | 269 |
| Execuções completadas | 86 |
| Sucesso (exit 0) | 27 |
| Falha (exit 2) | 59 |
| Crash (signal) | 0 |
| Running/Unknown | 183 |
| **Taxa de falha (completados)** | **68.6%** |
| Resets da placa | 217 |
| Tempo de exposição | 17.98 horas |
| Fluxo de nêutrons | 2.6 × 10⁶ n/cm²/s |
| Fluência total | 1.68 × 10¹¹ n/cm² |
| Dose aproximada | 1.14 Gy (14 MeV) |

### 5.2 Correlação de Falhas por Sensor

| Sensor | Execuções com Falha | % |
|--------|---------------------|---|
| Process | 59/59 | 100% |
| GPS | 49/59 | 83% |
| IMU | 46/59 | 78% |
| MAG | 43/59 | 73% |
| BARO | 40/59 | 68% |
| Timing | 36/59 | 61% |

### 5.3 Padrões de Output Vector

```
Flags          | Count | GPS | IMU | BARO | MAG | Timing
---------------|-------|-----|-----|------|-----|--------
0x80000606     | 36    | X   |     |      | X   | X
0x800005e6     | 13    | X   |     | X    |     | X
0x80000516     | 4     |     | X   | X    | X   | X
0x800005d6     | 3     |     | X   |      |     | X
0x80000556     | 3     |     | X   |      | X   | X
```

### 5.4 Análise de Resets

- Total de resets: 217
- Taxa de reset: 5.0 resets/hora
- Tempo médio entre resets: 12 minutos

---

## 6. Análise de Causa Raiz

### 6.1 Por que a Redundância Falhou

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CENÁRIO NORMAL                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  I2C Bus ─┬─► BMP280_0 (BARO 0) ──► EKF3_core[0]                   │
│           ├─► AK09916_0 (MAG 0) ──►                                │
│           ├─► BMP280_1 (BARO 1) ──► EKF3_core[1]                   │
│           ├─► AK09916_1 (MAG 1) ──►                                │
│           ├─► BMP280_2 (BARO 2) ──► EKF3_core[2]                   │
│           └─► AK09916_2 (MAG 2) ──►                                │
│                                                                    │
│  SPI Bus ──► ICM20602 (IMU 0/1/2) ──► EKF3_all_cores               │
│                                                                    │
│  Resultado:                                                        │
│  - CORE 0: errorScore = 0.05 (saudável)                           │
│  - CORE 1: errorScore = 0.08 (saudável)                           │
│  - CORE 2: errorScore = 0.10 (saudável)                           │
│  - Seleção: CORE 0 (menor erro)                                   │
│  - Status: SUCCESS (0x000007FF)                                   │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    CENÁRIO COM SEU (Radiação)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  SEU no I2C Bus:                                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Bit flip no barramento I2C                                  │   │
│  │ ↓                                                           │   │
│  │ BMP280/AK09916 recebem dados corrompidos                    │   │
│  │ ↓                                                           │   │
│  │ hgtTestRatio → ∞ (BARO)                                    │   │
│  │ magTestRatio → ∞ (MAG)                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  SEU no SPI Bus:                                                   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Bit flip no barramento SPI                                  │   │
│  │ ↓                                                           │   │
│  │ ICM20602 retorna dados corrompidos                          │   │
│  │ ↓                                                           │   │
│  │ velTestRatio → ∞ (IMU afeta velocidade)                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  Resultado:                                                        │
│  - CORE 0: errorScore = MAX(∞, ∞, ∞) = ∞                          │
│  - CORE 1: errorScore = MAX(∞, ∞, ∞) = ∞                          │
│  - CORE 2: errorScore = MAX(∞, ∞, ∞) = ∞                          │
│  - Seleção: INDETERMINADO (todos com erro infinito)               │
│  - Status: FAILURE (0x80000000)                                   │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Ponto Único de Falha (SPOF)

| Componente | Barramento | Sensores Afetados |
|------------|------------|-------------------|
| I2C | Único | BMP280×3 (BARO), AK09916×3 (MAG) |
| SPI | Único | ICM20602×3 (IMU) |
| GPS | UART | Único GPS |

**Problema:** Um único SEU no barramento corrompe **todos** os sensores conectados, afetando **todos** os cores simultaneamente.

---

## 7. Recomendações

### 7.1 Para Tolerância a Radiação

1. **Barramentos Separados**: Cada sensor em barramento I2C/SPI fisicamente separado
2. **Dados Independentes**: Cada core deve receber dados de sensores independentes
3. **Detecção de Barramento Corrompido**: CRC/checksum por transação
4. **Fallback para Sensores Saudáveis**: Isolar sensores com dados corrompidos
5. **Watchdog para Seleção de Core**: Timeout para evitar deadlock quando todos os cores têm erro infinito

### 7.2 Arquitetura Proposta

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA PROPOSTA                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  EKF3_core[0]:                                                     │
│    - I2C_0 → BMP280_0, AK09916_0                                   │
│    - SPI_0 → ICM20602_0                                            │
│                                                                    │
│  EKF3_core[1]:                                                     │
│    - I2C_1 → BMP280_1, AK09916_1                                   │
│    - SPI_1 → ICM20602_1                                            │
│                                                                    │
│  EKF3_core[2]:                                                     │
│    - I2C_2 → BMP280_2, AK09916_2                                   │
│    - SPI_2 → ICM20602_2                                            │
│                                                                    │
│  GPS_0, GPS_1, GPS_2 (redundância GPS)                              │
│                                                                    │
│  Cada barramento independente:                                      │
│    - SEU em I2C_0 afeta APENAS core[0]                            │
│    - Core[1] e Core[2] continuam saudáveis                        │
│    - Votação funciona corretamente                                 │
│                                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8. Arquivos do Projeto

| Caminho | Descrição |
|---------|-----------|
| `case-study_algorithms/drone/arducopter-ekf/` | Case EKF |
| `case-study_algorithms/multirad/` | Plataforma MultiRad |
| `data_orchestrator/raspberry/arducopter/libraries/AP_NavEKF3/` | EKF3 source |
| `data_orchestrator/raspberry/emulator/` | Emulator shim |
| `case-study_algorithms/drone/arducopter-ekf/data/` | Datasets CSV |

---

## 9. Diagramas Gerados

| Arquivo | Conteúdo |
|---------|----------|
| `radiation_analysis.png` | Análise de radiação (6 plots) |
| `ekf-system.png` | Diagrama do sistema EKF |
| `multirad-complete-architecture.png` | Arquitetura completa |

---

**Gerado em:** 2026-03-09
**Autor:** OpenClaw
**Baseado em:** Análise exaustiva do código fonte e logs de radiação