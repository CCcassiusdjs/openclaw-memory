# Optical Flow Sensor Setup (ArduPilot)

**Source:** ArduPilot Copter Documentation
**URL:** https://ardupilot.org/copter/docs/common-optical-flow-sensor-setup.html
**Type:** Setup Guide
**Relevance:** High - Practical optical flow integration

## Summary

Complete guide for setting up optical flow sensors in ArduPilot for indoor navigation and GPS-denied flight.

## Supported Sensors

| Sensor | Type | Interface |
|--------|------|-----------|
| **PX4Flow** | Camera + Gyro | I2C/Serial |
| **MTF-01** | Optical + Range | CAN/Serial |
| **ARK Flow** | Camera + Range | DroneCAN |

## How Optical Flow Works

**Principle:**
1. Downward camera captures ground texture
2. Image processing detects motion
3. Gyroscope compensates for rotation
4. Range finder provides altitude
5. Velocity = Flow × Altitude

**Equation:**
```
Velocity = (Flow_rate × Altitude) / Focal_length
```

## Inflight Calibration

**Method 1: GPS-Assisted Calibration**
1. Set EK3_SRC1_VELXY = 3 (GPS)
2. Fly to 10m+ altitude
3. Rock vehicle in roll and pitch
4. System calculates flow scale factors
5. Set EK3_SRC1_VELXY = 5 (Optical Flow)

**Method 2: Log-Based Calibration**
1. Remove propellers
2. Rotate ±15° in roll, repeat 5-10x
3. Rotate ±15° in pitch, repeat 5-10x
4. Analyze OF.flowX vs OF.bodyX
5. Adjust FLOW_FXSCALER, FLOW_FYSCALER

## EKF3 Source Configuration

**GPS + Optical Flow (Dual Mode):**
```
EK3_SRC1_POSXY = 3 (GPS)
EK3_SRC1_VELXY = 3 (GPS)
EK3_SRC1_POSZ = 1 (Baro)
EK3_SRC1_VELZ = 3 (GPS)
EK3_SRC1_YAW = 1 (Compass)

EK3_SRC2_POSXY = 0 (None)
EK3_SRC2_VELXY = 5 (Optical Flow)
EK3_SRC2_POSZ = 1 (Baro)
EK3_SRC2_VELZ = 0 (None)
EK3_SRC2_YAW = 1 (Compass)
```

**Optical Flow Only (Indoor):**
```
EK3_SRC1_POSXY = 0 (None)
EK3_SRC1_VELXY = 5 (Optical Flow)
EK3_SRC1_POSZ = 1 (Baro)
EK3_SRC1_VELZ = 0 (None)
EK3_SRC1_YAW = 1 (Compass)
```

## Key Parameters

| Parameter | Purpose |
|-----------|---------|
| FLOW_FXSCALER | X-axis flow scale |
| FLOW_FYSCALER | Y-axis flow scale |
| FLOW_ORIENT_YAW | Sensor yaw orientation |
| EK3_FLOW_DELAY | Flow sensor latency (default 10ms) |
| RNGFNDx_MAX | Max range finder altitude |

## Safety Mechanism

**Important:** When Optical Flow is the only horizontal position source:
- Vehicle won't climb above RNGFNDx_MAX
- EKF failsafe triggers if range finder lost
- Prevents flyaway when out of range

## Troubleshooting

**OF.flowX vs IMU.GyrX:**
- Should correlate strongly
- Opposite sign → wrong FLOW_ORIENT_YAW
- Different amplitude → adjust FLOW_FXSCALER

**Erratic movement:**
- Check range finder continuous
- Verify good lighting and texture
- Ensure sensor is level

## Relevance to EKF

- Optical Flow provides velocity (not position)
- Needs range finder for altitude reference
- Time delay compensation via EK3_FLOW_DELAY
- Can be combined with GPS via source switching

## Tags

`#optical-flow` `#px4flow` `#indoor-navigation` `#gps-denied` `#flow-calibration` `#range-finder`