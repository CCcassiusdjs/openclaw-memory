# Expertise Topics Index

**Updated:** 2026-03-10

## Active Topics

| Topic | Status | Sources | Hours | Progress |
|-------|--------|---------|-------|----------|
| ardupilot-ekf | ✅ COMPLETED | 16/21 | 5.5h/5.5h | 100% |
| drone-sensors | ✅ COMPLETED | 36/36 | 4.5h/4.5h | 100% |

## Completed Topics

### ardupilot-ekf (Completed 2026-03-10)

**Summary:** ArduPilot EKF & State Estimation

**Key Concepts Learned (44 total):**
- Extended Kalman Filter (EKF) architecture
- Error State EKF (ES-EKF) for GPS-denied navigation
- Lie Group formulation for GNSS/INS integration
- Lane switching and sensor affinity
- EKF2 vs EKF3 comparison
- 24-state EKF2 state vector
- Glitch protection and failsafe
- Source selection and switching
- GSF (Gaussian Sum Filter) for compass-less yaw
- Allan variance for IMU noise characterization
- Magnetometer bias learning in-flight
- EKF tuning parameters (noise, gates)
- Innovation and state correction

**Key Insights:**
- EKF3 is the current standard, EKF2 still available but without modern features
- Multiple IMUs = multiple EKF cores running in parallel
- Lane switching based on accumulated error (not instantaneous)
- UKF theoretically better but not used in ArduPilot (computational cost)
- Quaternions avoid gimbal lock and angle wrapping
- ES-EKF numerically more stable than standard EKF
- GPS-denied EKF uses LiDAR SLAM, visual odometry, or UWB
- Noise parameters control error growth rate
- GPS position can correct velocity, angles, and gyro bias

**Sources Read:** 16 of 21
- Official documentation (ArduPilot, PX4)
- Academic papers (ES-EKF, Lie Groups, UKF comparison)
- Source code structure
- Tutorials (MATLAB, Rust)

### drone-sensors (Completed 2026-03-10)

**Summary:** Drone Sensors & Hardware Integration

**Key Concepts Learned (50+ total):**
- IMU selection and noise characteristics
- Temperature effects on MEMS IMUs
- Vibration analysis and filtering (FFT, notch filters)
- Sensor redundancy and heterogeneous fusion
- VTOL-specific sensor requirements
- PX4 sensor architecture and configuration
- RTK GPS and dual-antenna heading
- Optical flow for GNSS-denied navigation
- Airspeed sensors for stall detection
- Rangefinders for terrain following
- Tachometers for RPM logging

**Key Insights:**
- Airspeed is CRITICAL for fixed-wing - only way to detect stall
- RTK provides centimeter-level accuracy
- Dual-antenna GPS can replace magnetometer for heading
- Optical flow requires distance sensor for velocity estimation
- DOP is potential accuracy; EPH/EPV is actual accuracy
- IMU batch sampling + FFT identifies vibration frequencies
- Harmonic notch filters reduce motor vibration
- CAN interface more robust than UART/I2C
- EPH/EPV metrics better than DOP for real accuracy
- Position fusion requires yaw alignment first

**Sources Read:** 36 of 36
- Academic papers (IMU noise, sensor fusion)
- PX4 official documentation (sensors)
- ArduPilot documentation (IMU batch sampling)

## In Progress Topics

None currently in progress.

## Pending Topics

None defined yet.

## Heuristics Applied

1. Always do bibliography survey BEFORE reading
2. Prioritize official documentation when available
3. Survey papers are good starting points
4. Textbooks for theoretical foundation
5. Tutorials and examples for practical application