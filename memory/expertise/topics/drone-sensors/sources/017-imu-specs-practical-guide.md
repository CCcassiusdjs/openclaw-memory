# Reading IMU Specs for Fun and Profit

**Source:** stechschulte.net
**URL:** https://stechschulte.net/2023/10/11/imu-specs.html
**Type:** Practical Guide
**Relevance:** Critical - Converting spec sheet values to EKF parameters

## Summary

Practical guide to converting IMU spec sheet values into noise model parameters for Kalman filters. Essential for EKF tuning.

## The IMU Noise Model

**Two components per sensor:**
1. **White Noise** - Zero-mean random variable per sample
2. **Bias** - Modeled as random walk

### Units Matter!

| Parameter | Units | Notes |
|-----------|-------|-------|
| **Acc white noise** | m/s²/√Hz | Multiplied by √(sample_rate) |
| **Acc bias** | m/s² √Hz | Divided by √(sample_rate) |
| **Gyro white noise** | rad/s/√Hz | Same pattern |
| **Gyro bias** | rad/s √Hz | Same pattern |

**Key insight:** White noise increases with sample rate, bias drift decreases.

### Random Walk Math

Standard deviation of random walk after T steps:
```
σ_total = √(T) × σ_step
```

This is why √Hz appears everywhere - variance scales linearly with steps, std dev with √(steps).

## Converting Spec Sheet Values

### White Noise from Noise Density

**Example Gyroscope:**
```
4.68 deg/hr/√Hz
= 4.68 × (π/180) × (1/3600) rad/s/√Hz
= 2.269×10⁻⁵ rad/s/√Hz
```

**Example Accelerometer:**
```
60 µG/√Hz
= 60 × 10⁻⁶ × 9.8 m/s²/√Hz
= 5.88×10⁻⁴ m/s²/√Hz
```

### White Noise from Random Walk

Alternative spec (common on datasheets):
```
0.06 °/√hr (angular random walk)
= 0.06 × (π/180) × (1/√3600) rad/s/√Hz
= 1.745×10⁻⁵ rad/s/√Hz
```

### Bias from "Bias Instability"

When only "bias instability" or "bias stability" is given:
```
0.8 °/hr (gyro bias instability)
= 0.8 × (π/180) × (3600) rad/s
= 3.878×10⁻⁶ rad/s  [add √Hz]
→ Use: 3.878×10⁻⁶ rad/s √Hz
```

**Fudge factor:** Add √Hz to bias specs - they're usually in units/s, not units√Hz.

## IMU Comparison Table

| Model | Grade | Gyro White Noise | Gyro Bias | Acc White Noise | Acc Bias |
|-------|-------|------------------|-----------|-----------------|----------|
| Epson M-G370PDF1 | Tactical | 2.27e-5 | 3.88e-6 | 5.88e-4 | 1.12e-4 |
| OxTS RT3000 v3 | Tactical | 5.82e-5 | 9.70e-6 | 8.33e-5 | 1.96e-5 |
| MicroStrain 3DM-CX5 | Industrial | 8.73e-5 | 3.88e-5 | 1.96e-4 | 3.92e-4 |
| Bosch BHI260AP | Consumer | 1.22e-4 | 2.42e-5 | 8.32e-4 | ? |

**Note:** Industrial/Tactical = 10x better than Consumer

## Practical Tips

1. **Increase noise by 10x** - Real-world worse than ideal conditions
2. **Bias instability is upper bound** - Actual bias may be lower
3. **Look for Allan variance plots** - Better than single values
4. **Units vary by manufacturer** - Always convert to consistent units

## EKF Parameter Mapping

```
# ArduPilot EKF parameters
EKF_GYRO_NOISE = gyro_white_noise × √(IMU_RATE)
EKF_ACC_NOISE = acc_white_noise × √(IMU_RATE)
EKF_GYRO_BIAS_NOISE = gyro_bias / √(IMU_RATE)
EKF_ACC_BIAS_NOISE = acc_bias / √(IMU_RATE)
```

## Cross-References

- Allan Variance analysis
- Kalibr IMU noise model
- OpenVINS sensor calibration

## Tags

`#imu-noise-model` `#spec-sheet` `#noise-density` `#bias-instability` `#ekf-tuning` `#random-walk`