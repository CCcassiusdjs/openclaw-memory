# Expertise Topics Index

**Updated:** 2026-03-10

## Active Topics

| Topic | Status | Sources | Hours | Progress |
|-------|--------|---------|-------|----------|
| ardupilot-ekf | ✅ COMPLETED | 16/21 | 5.5h/5.5h | 100% |
| drone-sensors | 📖 READING | 11/21 | 2.5h/4.0h | 52% |

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

## In Progress Topics

### drone-sensors (Reading - 52%)

**Summary:** Drone Sensors & Hardware Integration

**Progress:**
- Sources: 11/21 read
- Time: 2.5h/4.0h estimated

**Concepts Learned (39 total):**
- IMU noise model (white noise + bias random walk)
- Allan variance analysis
- Hard/soft iron magnetometer calibration
- Barometer altitude estimation
- Sensor driver architecture (frontend/backend)
- VectorNav external AHRS integration
- EKF time horizon for latency compensation
- Optical flow velocity estimation
- GPS latency (100-300ms)
- Flow scale factor calibration

**Key Insights:**
- Noise density and random walk use same units (deg/s/√Hz = deg/√s)
- Higher sample rate = more white noise per sample
- Bias instability is upper bound on bias standard deviation
- Hard iron = constant offset, soft iron = transformation matrix
- Barometers calibrated against GPS altitude at startup
- EKF uses delayed time horizon for sensor latency compensation
- GPS latency 100-300ms, optical flow 20-50ms, baro 10-50ms
- Optical flow provides velocity (not position), needs range finder

**Next Steps:**
- GPS accuracy and latency details
- Range finder sensors
- Complete remaining bibliography

## Pending Topics

None defined yet.

## Heuristics Applied

1. Always do bibliography survey BEFORE reading
2. Prioritize official documentation when available
3. Survey papers are good starting points
4. Textbooks for theoretical foundation
5. Tutorials and examples for practical application