# IMU Specifications Explained (VectorNav)

**Source:** VectorNav Resources
**URL:** https://www.vectornav.com/resources/inertial-navigation-primer/specifications--and--error-budgets/specs-imuspecs
**Type:** Technical Reference
**Relevance:** Critical - Understanding IMU specs for EKF tuning

## Summary

Comprehensive guide to IMU specifications including noise, bias, scale factor, and orthogonality errors. Essential for understanding sensor performance characteristics.

## Key Specifications

### Basic Parameters

| Parameter | Description |
|-----------|-------------|
| **Range** | Min/max input values measurable |
| **Resolution** | Smallest unit of measure |
| **Bandwidth** | Max frequency response (-3 dB point) |
| **Sample Rate** | Samples per second (≠ bandwidth) |

### Noise Characteristics

**Noise Density:**
- Units: °/s/√Hz (gyro), m/s²/√Hz (accel)
- Relationship: σ = ND × √(SR)
- Higher sample rate = more noise per sample

**Random Walk:**
- **Angle Random Walk (ARW)**: Gyroscope drift integration
- **Velocity Random Walk (VRW)**: Accelerometer drift integration
- Units: °/√s or °/√hr (ARW), m/s/√s or m/s/√hr (VRW)

**Unit Conversions:**
```
Noise density [°/s/√Hz] = ARW [°/√s] (same units!)
60 √s = √hr
1 mg ≈ 0.01 m/s²
```

### Bias Parameters

| Type | Description | Importance |
|------|-------------|------------|
| **In-Run Bias Stability** | Drift during operation at constant temp | Most critical - floor for bias estimation |
| **Turn-on Bias Stability** | Initial bias variation between startups | Important for unaided navigation |
| **Bias Temp Sensitivity** | Bias variation over temperature | Requires calibration |

### Scale Factor Errors

**Scale Factor Error:**
- Units: ppm or %
- Example: 0.1% error on 9.81 m/s² → reports 9.82 m/s²

**Nonlinearity:**
- Errors in ratio being non-linear
- Units: ppm or %FS (full scale)

### Orthogonality Errors

| Type | Description |
|------|-------------|
| **Cross-Axis Sensitivity** | X-axis sensed in Z-axis |
| **Misalignment** | Internal axes don't match case marking |

### Gyroscope Acceleration Sensitivity

**g-Sensitivity:**
- Bias shift from constant linear acceleration
- Must test both parallel and perpendicular to sensing axis

**g²-Sensitivity (Vibration Rectification):**
- Bias shift from oscillatory acceleration
- Important in high-vibration environments

## EKF Relevance

These specifications directly map to EKF parameters:
- **Noise Density** → EKF_GYRO_NOISE, EKF_ACC_NOISE
- **Bias Stability** → EKF_GYRO_BIAS_NOISE, EKF_ACC_BIAS_NOISE
- **Scale Factor** → Calibration parameters

## Tags

`#imu-specs` `#noise-density` `#bias-stability` `#random-walk` `#scale-factor` `#allan-variance`