# MultiRad Radiation Testing Analysis - 2026-03-08

## Session Summary

Análise completa do projeto `multirad_data_orchestrator` e dos resultados de testes de radiação do ArduCopter EKF.

---

## 1. Project Architecture

### Location
`/home/csilva/Documents/multirad_data_orchestrator`

### Components

#### 1.1 Data Orchestrator (Computer)
- **Path:** `data_orchestrator/computer/`
- **Function:** Generates synthetic sensor datasets
- **Language:** C23
- **Key modules:**
  - `core/orchestrator.c` - Main generation engine
  - `core/timeline.c` - Temporal event management
  - `synth/imu.c` - IMU data synthesis
  - `synth/gps.c` - GPS data synthesis
  - `synth/baro.c` - Barometer data synthesis
  - `synth/mag.c` - Magnetometer data synthesis
  - `synth/pwm.c` - PWM signal synthesis
  - `io/csv_*` - CSV I/O

#### 1.2 Sensor Emulator (Raspberry Pi)
- **Path:** `data_orchestrator/raspberry/emulator/`
- **Function:** Intercepts I/O calls from ArduCopter via LD_PRELOAD
- **Key components:**
  - `shim.c` - I/O interception (open, ioctl, clock_gettime)
  - `emulator_state.c` - Global state management
  - `models/icm20602_model.c` - IMU (SPI)
  - `models/bmp280_model.c` - Barometer (I2C 0x76)
  - `models/ak09916_model.c` - Magnetometer (I2C 0x0C)
  - `models/pca9685_model.c` - PWM controller (I2C 0x40)
  - `gps_pty_bridge.c` - GPS serial bridge

#### 1.3 MultiRad Framework
- **Path:** `case-study_algorithms/multirad/`
- **Function:** Radiation test harness with CRC verification
- **Key features:**
  - Dual output buffers
  - CRC32C checksums
  - 10 error codes classification
  - Interface with ccX (control computer)

#### 1.4 ArduCopter EKF Case Study
- **Path:** `case-study_algorithms/drone/arducopter-ekf/`
- **Function:** Tests EKF3 under radiation with emulated sensors
- **Key files:**
  - `case_runner.c` - Executes ArduCopter binary
  - `output_vector_extractor.c` - Extracts results
  - `set_of_input_vectors.c` - Configuration paths

---

## 2. Radiation Test Results

### Source File
`/home/csilva/Downloads/2026-log-rad-drone.txt`

### Test Campaign
- **Dates:** 2026-02-25 to 2026-02-27
- **Location:** TIMA Laboratory, Grenoble
- **SUT:** Raspberry Pi with ArduCopter EKF3

### Overall Statistics

| Metric | Value | Percentage |
|--------|-------|------------|
| Total runs | 269 | 100% |
| Success (code=0) | 27 | 10.0% |
| Failure (code=2) | 59 | 21.9% |
| SEGV crash | 1 | 0.4% |
| No exit recorded | 182 | 67.7% |
| Power cycles | 217 | - |

### By Day

| Date | Success | Failure | Rate |
|------|---------|---------|------|
| 2026-02-25 | 24 | 27 | 47.1% |
| 2026-02-26 | 1 | 29+1 SEGV | 3.2% |
| 2026-02-27 | 2 | 3 | 40.0% |

### By Instance

| Instance | Success | % of Successes |
|----------|---------|----------------|
| i0 (first attempt) | 15 | 55.6% |
| i1 (second attempt) | 12 | 44.4% |

---

## 3. Error Flag Analysis

### Error Flags from EKF Output

| Count | Flags | Interpretation |
|-------|-------|----------------|
| 36 | 0x80000606 | Mag fail, GPS fail, Replay incomplete |
| 13 | 0x800005e6 | Mag fail, Emulator errors |
| 4 | 0x80000516 | IMU fail, Mag fail, Emulator errors |
| 3 | 0x800005d6 | Mag fail, Emulator errors |
| 3 | 0x80000556 | IMU fail, Mag fail |

### Flag Decoding

```
Bit 0  (0x001): ProcessOk
Bit 1  (0x002): LogParsed
Bit 2  (0x004): ArducopterInitSeen
Bit 3  (0x008): ReplayWindowComplete
Bit 4  (0x010): GpsReplayOk
Bit 5  (0x020): ImuReplayOk
Bit 6  (0x040): BaroReplayOk
Bit 7  (0x080): MagReplayOk
Bit 8  (0x100): TimingSummarySeen
Bit 9  (0x200): NoEmulatorErrors
Bit 10 (0x400): ArmedSeen
Bit 31 (0x80000000): RunFailed
```

### Sensor Failure Correlation

| Sensor | Present in Failures | Interface |
|--------|---------------------|-----------|
| Magnetometer (AK09916) | 100% (59/59) | I2C 0x0C |
| GPS | 61% (36/59) | PTY/Serial |
| IMU (ICM20602) | 12% (7/59) | SPI |
| Barometer (BMP280) | 0% isolated | I2C 0x76 |

---

## 4. Key Findings

### Critical Finding: Magnetometer as Primary Failure Point
- AK09916 on I2C 0x0C implicated in 100% of classified failures
- I2C interface shows higher sensitivity than SPI
- Possible causes:
  1. I2C bus sensitivity to radiation transients
  2. Timing violations in emulation shim
  3. EKF arming timeout due to delayed magnetometer initialization

### Day 2 Degradation
- Success rate dropped from 47% to 3%
- Possible causes:
  1. Cumulative radiation damage
  2. Increased beam flux
  3. Thermal effects

### SEGV Event
- Single segmentation fault on 2026-02-26 10:15:33
- Indicates potential SEFI (Single-Event Functional Interrupt)
- Memory corruption in SUT

---

## 5. Radiation Parameters (RECEIVED)

### Beam Configuration
| Parameter | Value |
|-----------|-------|
| Particle type | Neutron |
| Flux | $2.6 \times 10^{6}$ n/cm²/s |
| Beam energy | TBD |

### Exposure by Day
| Date | Duration | Fluence |
|------|----------|---------|
| 2026-02-25 | 8.35 hours | $7.82 \times 10^{10}$ n/cm² |
| 2026-02-26 | 8.11 hours | $7.59 \times 10^{10}$ n/cm² |
| 2026-02-27 | 4.55 hours | $4.26 \times 10^{10}$ n/cm² |
| **Total** | **21.01 hours** | **$1.97 \times 10^{11}$ n/cm²** |

### Calculated Metrics
| Metric | Value |
|--------|-------|
| Device cross-section | $3.05 \times 10^{-10}$ cm² |
| Classified error cross-section | $3.00 \times 10^{-10}$ cm² |
| Magnetometer cross-section | $3.00 \times 10^{-10}$ cm² |
| GPS cross-section | $1.83 \times 10^{-10}$ cm² |
| IMU cross-section | $3.56 \times 10^{-11}$ cm² |
| SER | 2.86 errors/hour |
| MTBF | 0.35 hours (21 minutes) |

---

## 6. Calculations Ready (When Fluence Arrives)

### Cross-Section Formula
```
σ = N_errors / Φ
```
Where:
- σ = cross-section (cm²/particle)
- N_errors = number of errors (59 classified + 1 SEGV + 182 unknown)
- Φ = fluence (particles/cm²)

### Error Rate Formula
```
SER = N_errors / (N_devices × T_test)
```

### MTBF Estimation
```
MTBF = 1 / (σ × Φ_mission)
```

---

## 7. Recommendations

### Immediate
1. Verify magnetometer dataset (`datasets/mag.csv`)
2. Increase EKF arming timeout
3. Add retry logic to AK09916 model
4. Implement graceful degradation (GPS yaw fallback)

### Medium Term
1. Add fluence/flux measurement to logs
2. Shield magnetometer differently
3. Log I2C transaction timing
4. Add thermal monitoring

### Long Term
1. Triple Modular Redundancy (TMR) for critical sensors
2. Radiation-hardened I2C buffers
3. Watchdog timer for sensor initialization

---

## 8. Report Structure (IEEE/IMRaD)

### Draft Outline
1. **Abstract** - Summary of campaign and findings
2. **Introduction** - MultiRad project, ArduCopter EKF, radiation testing context
3. **Experimental Setup** - SUT, radiation environment, sensor emulation
4. **Methodology** - Test procedure, error classification, statistical methods
5. **Results** - Tables, temporal distribution, sensor analysis
6. **Discussion** - Magnetometer failure analysis, day 2 degradation
7. **Conclusions** - Summary, recommendations
8. **References** - Radiation testing literature
9. **Appendices** - Raw logs, configuration files

---

## 9. Files Analyzed

| File | Content |
|------|---------|
| `data_orchestrator/computer/src/core/orchestrator.c` | Dataset generation engine |
| `data_orchestrator/computer/src/synth/imu.c` | IMU synthesis |
| `data_orchestrator/raspberry/emulator/src/shim.c` | I/O interception |
| `data_orchestrator/raspberry/emulator/src/models/*.c` | Sensor models |
| `case-study_algorithms/multirad/common/sources/multirad.c` | Test harness |
| `case-study_algorithms/drone/arducopter-ekf/arducopter/src/case_runner.c` | EKF runner |
| `/home/csilva/Downloads/2026-log-rad-drone.txt` | Radiation test log |

---

## 10. Next Steps

1. **Await fluence data from colleague**
2. Calculate cross-section and error rates
3. Complete technical report
4. Prepare visualization (error distribution, temporal analysis)
5. Submit to radiation effects conference/journal

---

_Last updated: 2026-03-08_
_Pending: Fluence data from colleague_