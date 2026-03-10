# ES-EKF for UAV Indoor Localization (GPS-Denied Environments)

**Source:** arXiv:2109.04908 (2021)
**Type:** Academic Paper
**Relevance:** High - Directly related to EKF state estimation for UAVs

## Summary

This paper addresses UAV indoor navigation where GPS and magnetometer measurements are unavailable or unreliable. Proposes an **Error State Extended Kalman Filter (ES-EKF)** for multi-sensor fusion.

## Key Concepts

### Problem Statement
- Indoor UAV navigation lacks GPS and magnetometer data
- Traditional navigation filters fail in denied environments
- Need for robust sensor fusion without external positioning

### Proposed Solution: ES-EKF
- **Error State Formulation**: Tracks errors rather than full states
- **Multi-sensor fusion**: Combines multiple sensor sources
- **Drift compensation**: Extended state model accounts for sensor drift
- **Calibration handling**: Accounts for calibration inaccuracies

### Implementation Details
- **IMU Data**: From PixHawk 2.1 flight controller
- **Pose Measurements**: LiDAR Cartographer SLAM
- **Visual Odometry**: Intel T265 camera
- **Position Measurements**: Pozyx UWB indoor positioning system
- **Ground Truth**: Optitrack motion capture system

### State Model Extensions
- Sensor bias estimation
- Drift compensation
- Calibration error modeling

## Results

- Validated against Optitrack ground truth
- Demonstrated use in position control loop
- Successfully stabilized UAV in GPS-denied indoor environments

## Mathematical Framework

The ES-EKF formulation:
- Uses error state representation (delta angles, delta velocities)
- Propagates covariance through Jacobian linearization
- Updates with multiple heterogeneous sensors
- Maintains numerical stability (error states small)

## Relevance to ArduPilot EKF

- Alternative formulation to standard EKF
- Error-state approach similar to EKF2/EKF3
- Demonstrates multi-sensor fusion architecture
- Provides insight into indoor GPS-denied navigation

## Cross-References

- Related to EKF state estimation
- Complements outdoor GPS/INS fusion
- Extends to LiDAR/Visual odometry integration

## Tags

`#es-ekf` `#indoor-navigation` `#gps-denied` `#multi-sensor-fusion` `#uav-localization` `#state-estimation`