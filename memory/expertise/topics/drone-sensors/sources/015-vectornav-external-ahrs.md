# VectorNav External AHRS Integration

**Source:** ArduPilot Copter Documentation
**URL:** https://ardupilot.org/copter/docs/common-external-ahrs-vectornav.html
**Type:** Hardware Integration Guide
**Relevance:** High - Professional AHRS/INS integration

## Summary

Documentation for integrating VectorNav high-performance IMU/AHRS/GNSS-INS systems with ArduPilot. Shows how external navigation systems can bypass or feed ArduPilot's EKF.

## Key Concepts

### VectorNav Product Line

| Model | Type | Use Case |
|-------|------|----------|
| **VN-100** | IMU/AHRS | Attitude-only, no GNSS |
| **VN-200/210** | GNSS/INS | Fixed-wing without hovering |
| **VN-300/310** | Dual GNSS/INS | Multicopter, static heading |

### Benefits
- Higher accuracy heading, pitch, roll
- More robust GNSS positioning
- Better performance in GNSS-contested environments
- Handles high dynamics (catapult, VTOL, high-g)

### Two Integration Modes

**1. External Sensor Set:**
- VectorNav provides raw sensor data
- ArduPilot's EKF processes data
- EAHRS_TYPE = 1, AHRS_EKF_TYPE = 3
- EAHRS_RATE sets IMU update rate (up to 800Hz)

**2. External AHRS (Bypass EKF):**
- VectorNav provides complete PVTA solution
- Bypasses ArduPilot's EKF entirely
- AHRS_EKF_TYPE = 11 (External AHRS)
- Requires VN-2X0 or VN-3X0 (INS-enabled)

### Hardware Setup

**Wiring:**
- Connect VectorNav UART to flight controller serial port
- RS-232 levels on VN-X00 industrial units (use UART2 for TTL)

**Mounting:**
- Any orientation allowed (configure reference frame rotation)
- GNSS antenna must be rigid relative to IMU
- Dual GNSS: secondary antenna rigid relative to primary

### Binary Output Configuration

**Binary Output 1 (IMU):**
- Rate: EAHRS_RATE (default 50Hz, up to 800Hz)
- Contains: TimeStartup, AngularRate, Accel, Imu, MagPres

**Binary Output 2 (EKF):**
- Rate: 50Hz
- VN-1X0: Ypr, Quaternion, YprU
- VN-2X0/3X0: + InsStatus, PosLla, VelNed, PosU, VelU

**Binary Output 3 (GNSS):**
- Rate: 5Hz
- Contains: TimeGps, NumSats, GnssFix, GnssPosLla, GnssVelNed, GnssDop

### ArduPilot Parameters

```
# Serial configuration
SERIALx_PROTOCOL = 36 (AHRS)
SERIALx_BAUD = 921600 (recommended)

# External sensor set mode
AHRS_EKF_TYPE = 3 (EKF3)
EAHRS_TYPE = 1 (VectorNav)
EAHRS_OPTIONS = 1 (disable bias-compensated data)

# External AHRS mode (bypass EKF)
AHRS_EKF_TYPE = 11 (External AHRS)
EAHRS_TYPE = 1 (VectorNav)
```

### DataFlash Log Messages

| Message | Content |
|---------|---------|
| **EAHI** | IMU data (temp, pressure, mag, accel, gyro) |
| **EAHA** | Attitude (quaternion, YPR, uncertainty) |
| **EAHK** | INS data (status, position, velocity, uncertainty) |

## Relevance to ArduPilot EKF

- Shows how external high-grade sensors can feed EKF
- Alternative to built-in MEMS IMUs
- Reference for professional-grade navigation
- Demonstrates EKF bypass architecture

## Cross-References

- Sensor driver architecture
- External AHRS protocol
- GNSS/INS integration

## Tags

`#vectornav` `#external-ahrs` `#gnss-ins` `#high-performance-imu` `#ekf-bypass` `#professional-navigation`