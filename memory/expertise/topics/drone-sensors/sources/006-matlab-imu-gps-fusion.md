# IMU and GPS Fusion for Inertial Navigation (MATLAB Tutorial)

**Source:** MathWorks Documentation
**URL:** https://www.mathworks.com/help/nav/ug/imu-and-gps-fusion-for-inertial-navigation.html
**Type:** Tutorial/Documentation
**Relevance:** High - Practical implementation guide

## Summary

MATLAB tutorial demonstrating IMU + GPS fusion for UAV/quadcopter navigation using `insfilterMARG`. Shows practical implementation of sensor fusion with accelerometer, gyroscope, magnetometer, and GPS.

## Key Concepts

### System Architecture
- **IMU Sampling**: 160 Hz (accelerometer, gyroscope)
- **GPS Sampling**: 1 Hz
- **Magnetometer**: Low rate (1/160 of IMU rate)
- **Fusion**: Extended Kalman Filter tracking 22 states

### 22-State Vector (insfilterMARG)
| State | Description | Index |
|-------|-------------|-------|
| Orientation | Quaternion | 1:4 |
| Position (NED) | meters | 5:7 |
| Velocity (NED) | m/s | 8:10 |
| Delta Angle Bias | rad | 11:13 |
| Delta Velocity Bias | m/s | 14:16 |
| Geomagnetic Field (NED) | µT | 17:19 |
| Magnetometer Bias | µT | 20:22 |

### Fusion Methods
- **predict()**: Called at IMU rate, uses accel + gyro
- **fusegps()**: Called at GPS rate, updates position/velocity
- **fusemag()**: Called at magnetometer rate, updates orientation

### Sensor Models
**Accelerometer:**
- MeasurementRange: 19.6133 m/s²
- Resolution: 0.0023928 m/s²
- ConstantBias: 0.19 m/s²
- NoiseDensity: 0.0012356 m/s²/√Hz

**Gyroscope:**
- MeasurementRange: 250°/s (±250°/s)
- Resolution: 0.0625°
- ConstantBias: 3.125°/s
- AxesMisalignment: 1.5%

**Magnetometer:**
- MeasurementRange: 1000 µT
- Resolution: 0.1 µT
- ConstantBias: 100 µT
- NoiseDensity: 0.0424 µT/√Hz

### Noise Parameters
```matlab
Rmag = 0.0862;  % Magnetometer measurement noise
Rvel = 0.0051;  % GPS Velocity measurement noise
Rpos = 5.169;   % GPS Position measurement noise
```

### Process Noise Parameters
```matlab
fusionfilt.AccelerometerBiasNoise = 0.010716;
fusionfilt.AccelerometerNoise = 9.7785;
fusionfilt.GyroscopeBiasNoise = 1.3436e-14;
fusionfilt.GyroscopeNoise = 0.00016528;
fusionfilt.MagnetometerBiasNoise = 2.189e-11;
fusionfilt.GeomagneticVectorNoise = 7.67e-13;
```

## Results
- **Position RMS Error**: X: 0.50m, Y: 0.79m, Z: 0.65m
- **Orientation Error**: 1.45° (quaternion distance)

## Relevance to ArduPilot EKF

- Same sensor fusion principles
- `insfilterMARG` similar to EKF2/EKF3 in ArduPilot
- State vector structure similar (quaternion + position + velocity + biases)
- Noise tuning methodology applicable

## Cross-References

- Relates to EKF state estimation
- Demonstrates MARG sensor fusion
- Shows practical noise tuning

## Tags

`#matlab` `#insfilterMARG` `#imu-gps-fusion` `#sensor-modeling` `#noise-tuning` `#marg-sensors`