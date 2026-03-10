# Extended Kalman Filter Tuning (ArduPilot Dev)

**Source:** ArduPilot Dev Documentation
**URL:** https://ardupilot.org/dev/docs/extended-kalman-filter.html
**Type:** Technical Documentation
**Relevance:** Critical - EKF parameter tuning

## Summary

Overview of EKF1 algorithm (historical reference, basis for EKF2/EKF3). Describes 22-state EKF and tuning parameters.

## Theory

**State Vector (22 states):**
1. Angular position (roll, pitch, yaw)
2. Velocity (NED)
3. Position (NED)
4. Gyro biases (3)
5. Accelerometer bias (Z)
6. Wind velocities (3)
7. Compass biases (3)
8. Earth magnetic field (3)

**Process Flow:**
1. IMU angular rates → Angular position (integration)
2. IMU acceleration → Earth frame (transformation)
3. Acceleration → Velocity (integration)
4. Velocity → Position (integration)
5. State Covariance update (noise propagation)

## Key Parameters

### Noise Parameters (State Prediction)

| Parameter | Function |
|-----------|----------|
| **EKF_GYRO_NOISE** | Gyro noise, controls angle error growth |
| **EKF_ACC_NOISE** | Accelerometer noise, controls velocity error growth |
| **EKF_GBIAS_PNOISE** | Gyro bias noise, controls bias estimation speed |
| **EKF_ABIAS_PNOISE** | Accel bias noise, controls Z-acc bias estimation |

### Measurement Noise Parameters

| Parameter | Function |
|-----------|----------|
| **EKF_ALT_NOISE** | Barometer noise (RMS), controls baro weighting |
| **EKF_POSNE_NOISE** | GPS position noise, controls GPS weighting |
| **EKF_EAS_NOISE** | Airspeed noise, controls airspeed weighting |
| **EKF_FLOW_NOISE** | Optical flow noise, controls flow weighting |

### Gate Parameters (Innovation Consistency)

| Parameter | Function |
|-----------|----------|
| **EKF_EAS_GATE** | Airspeed gate (std dev scale) |
| **EKF_FLOW_GATE** | Optical flow gate |
| **EKF_HGT_GATE** | Height measurement gate |

### Glitch Protection

| Parameter | Function |
|-----------|----------|
| **EKF_GLITCH_ACCEL** | Max accel difference from GPS (cm/s²) |
| **EKF_GLITCH_RAD** | Max position difference from GPS (m) |

## Innovation

**Definition:** Difference between predicted and measured values.

**Equation:**
```
Innovation = Predicted_State - Measured_Value
```

**Consistency Check:**
- Gate = Innovation / sqrt(Innovation_Variance)
- If |Gate| > threshold, measurement rejected

## State Correction

**How it works:**
1. Innovation calculated
2. Kalman gain computed from covariance and noise
3. State correction applied to all correlated states
4. Covariance updated (reduced)

**Key insight:** GPS position can correct position, velocity, angles, and gyro bias due to state correlation.

## Altitude Sources

| Value | Source |
|-------|--------|
| 0 | Barometer |
| 1 | Range finder (terrain-relative) |

**Warning:** Range finder altitude only suitable for low altitude, low speed, flat surfaces.

## Glitch Protection Logic

1. Position step < GLITCH_RAD: temporarily ignored
2. Position step persists: accepted, filter moves
3. Position step > GLITCH_RAD: correction applied
4. Correction decays to zero at constant rate

## Magnetometer Learning

| Value | Mode |
|-------|------|
| 0 | Learn when airborne (speed + height criteria) |
| 1 | Learn always (not recommended) |
| 2 | Never learn |

## Relevance to ArduPilot

- EKF2/EKF3 share same principles
- Parameter names similar (EKF2_*, EKF3_*)
- Innovation/gate concept identical
- Glitch protection still used

## Tags

`#ekf-tuning` `#noise-parameters` `#innovation` `#state-correction` `#glitch-protection` `#altitude-estimation`