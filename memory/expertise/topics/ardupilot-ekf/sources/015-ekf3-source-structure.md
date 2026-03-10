# ArduPilot EKF3 Source Code Structure

**Source:** GitHub ArduPilot Repository
**URL:** https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_NavEKF3
**Type:** Source Code Reference
**Relevance:** Critical - Direct implementation reference

## Summary

EKF3 is implemented in the `AP_NavEKF3` library. Modular architecture with separate files for each fusion type.

## File Structure

| File | Purpose |
|------|---------|
| **AP_NavEKF3.cpp** | Main EKF class implementation |
| **AP_NavEKF3.h** | Header file, public interface |
| **AP_NavEKF3_core.cpp** | Core EKF algorithm |
| **AP_NavEKF3_core.h** | Core state and covariance |
| **AP_NavEKF3_AirDataFusion.cpp** | Airspeed, barometer fusion |
| **AP_NavEKF3_Control.cpp** | Control interface |
| **AP_NavEKF3_GyroBias.cpp** | Gyroscope bias estimation |
| **AP_NavEKF3_Logging.cpp** | DataFlash logging |
| **AP_NavEKF3_MagFusion.cpp** | Magnetometer fusion |
| **AP_NavEKF3_Measurements.cpp** | IMU measurement handling |
| **AP_NavEKF3_OptFlowFusion.cpp** | Optical flow fusion |
| **AP_NavEKF3_Outputs.cpp** | Output interface (position, velocity, attitude) |
| **AP_NavEKF3_PosVelFusion.cpp** | GPS position/velocity fusion |
| **AP_NavEKF3_RngBcnFusion.cpp** | Range beacon fusion |
| **AP_NavEKF3_VehicleStatus.cpp** | Vehicle status handling |
| **AP_NavEKF3_feature.h** | Feature flags |
| **LogStructure.h** | Log message definitions |
| **derivation/** | Mathematical derivation docs |

## Architecture Insights

### Modular Fusion
- Each sensor type has dedicated fusion file
- Easy to understand sensor contribution
- Clear separation of concerns

### Core Components
- **core.cpp**: State propagation, covariance update
- **Measurements.cpp**: IMU data processing
- **Outputs.cpp**: Provides estimated states to vehicle code

### Key Files for Understanding

1. **AP_NavEKF3_core.h**: State vector definition (24 states)
2. **AP_NavEKF3_Measurements.cpp**: How IMU feeds EKF
3. **AP_NavEKF3_PosVelFusion.cpp**: GPS integration logic
4. **AP_NavEKF3_MagFusion.cpp**: Compass integration

## State Vector (from core.h)

Based on previous research, EKF3 tracks:
- Position (NED): 3 states
- Velocity (NED): 3 states
- Attitude (quaternion): 4 states
- Gyro bias: 3 states
- Accel bias: 3 states
- Magnetometer bias: 3 states
- Wind: 3 states
- Terrain: 2 states
- **Total: 24 states**

## Tags

`#source-code` `#ekf3` `#ardupilot-implementation` `#modular-architecture` `#state-vector`