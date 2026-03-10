# Kalibr IMU Noise Model

**Source:** Kalibr Wiki (ETH Zurich)
**URL:** https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model
**Type:** Reference Implementation
**Relevance:** Critical - Standard IMU noise model for calibration

## Summary

Defines the IMU measurement model used in Kalibr for camera-IMU calibration. Standard reference for IMU noise parameters.

## Measurement Model

**Angular rate measurement (gyro, single axis):**
```
ω̃(t) = ω(t) + b(t) + n(t)
```

**Components:**
- **n(t)**: Additive "white noise" (rapid fluctuations)
- **b(t)**: Slowly varying sensor bias ("random walk")

**Same model for accelerometer.**

## White Noise Process

**Continuous-time:**
```
E[n(t)] = 0
E[n(t₁)n(t₂)] = σ² δ(t₁ - t₂)
```

**Discrete-time implementation:**
```
n_d[k] = σ_g_d × w[k]
σ_g_d = σ_g / √(Δt)
```

**Key insight:** Higher sampling rate → lower discrete noise (filtering assumption).

## Bias Random Walk

**Continuous-time:**
```
ḃ_g(t) = σ_bg × w(t)
```

**Discrete-time:**
```
b_d[k] = b_d[k-1] + σ_bg_d × w[k]
σ_bg_d = σ_bg × √(Δt)
```

## Parameter Summary

| Parameter | YAML Element | Units | Notes |
|-----------|-------------|-------|-------|
| Gyro white noise | `gyroscope_noise_density` | rad/s/√Hz | σ_g |
| Accel white noise | `accelerometer_noise_density` | m/s²/√Hz | σ_a |
| Gyro random walk | `gyroscope_random_walk` | rad/s²/√Hz | σ_bg |
| Accel random walk | `accelerometer_random_walk` | m/s³/√Hz | σ_ba |
| IMU rate | `update_rate` | Hz | 1/Δt |

## Allan Deviation Method

**From Allan Deviation Plot:**
1. **White noise (σ_g, σ_a)**: Value at τ = 1s (slope -½)
2. **Random walk (σ_bg, σ_ba)**: Value at τ = 3s (slope +½)

**Minimum at τ:**
- In-run bias stability = minimum of Allan Deviation curve
- Approximate accuracy limit for bias estimation

## Practical Guidelines

1. **Static, constant temperature data** - Model is optimistic
2. **Increase by 10x for low-cost MEMS** - Real-world worse than datasheet
3. **15-24 hour dataset** - For Allan variance calculation
4. **Use allan_variance_ros** - Tool for computing parameters

## Discrete vs Continuous

**White noise:**
- Continuous: σ × δ(t)
- Discrete: σ / √(Δt) per sample

**Bias random walk:**
- Continuous: σ × √Hz
- Discrete: σ × √(Δt) per sample

**Opposite effects of sample rate!**

## EKF Relevance

This is the standard model used in:
- Kalibr (camera-IMU calibration)
- ROS IMU drivers
- Visual-inertial odometry systems
- ArduPilot EKF parameter derivation

## References

1. IEEE Std 952-1997 - FOG test procedure
2. Trawny & Roumeliotis - Indirect KF for 3D Attitude
3. Crassidis - Sigma-Point KF for GPS/INS

## Tags

`#imu-noise-model` `#allan-variance` `#kalibr` `#random-walk` `#white-noise` `#bias-estimation`