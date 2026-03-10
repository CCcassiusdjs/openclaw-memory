# EKF Time Horizon and Sensor Latency (PX4 EKF2)

**Source:** PX4 Documentation
**URL:** https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf
**Type:** Technical Documentation
**Relevance:** Critical - Understanding EKF latency compensation

## Summary

The PX4 EKF2 runs on a delayed "fusion time horizon" to compensate for different sensor latencies relative to the IMU.

## Key Concept: Fusion Time Horizon

**Problem:** Different sensors have different latencies:
- IMU: ~0ms (immediate)
- GPS: ~100-300ms (satellite processing + transmission)
- Barometer: ~10-50ms (ADC filtering)
- Magnetometer: ~0-10ms
- Optical Flow: ~20-50ms

**Solution:**
```
EKF Time Horizon = IMU_Time - Buffer_Delay
```

The EKF buffers all measurements and processes them at the correct time.

## Implementation

**Data Flow:**
1. IMU data arrives at high rate (400-1000Hz)
2. GPS data arrives with timestamp (1-5Hz)
3. Each sensor's data is FIFO buffered
4. EKF retrieves data from buffer at correct time

**Parameters:**
- `EKF2_DELAY`: Maximum time delay (default 10ms)
- Each sensor has specific delay compensation

## Sensor Buffering

| Sensor | Typical Delay | Buffer Mechanism |
|--------|--------------|------------------|
| IMU | 0ms | Reference clock |
| GPS | 100-300ms | Timestamp-based |
| Baro | 10-50ms | FIFO buffer |
| Mag | 0-10ms | FIFO buffer |
| Optical Flow | 20-50ms | Timestamp-based |

## Optical Flow Integration

**Parameters:**
- `EKF2_OF_CTRL`: Enable optical flow fusion
- `EKF2_OF_N_MIN`: Minimum optical flow noise
- `EKF2_OF_N_MAX`: Maximum optical flow noise

**Requirements:**
- Range finder for altitude
- Good lighting and texture
- Sensor offset from center specified

**Setup:**
1. Set EKF2_OF_CTRL = 1
2. Configure sensor position offset
3. Calibrate flow scale factor
4. Set range finder max altitude

## Relevance to ArduPilot

- Same concept applies to EKF3
- EK3_FLOW_DELAY parameter for latency
- Buffer-based time synchronization
- Critical for multi-sensor fusion

## Cross-References

- EKF tuning parameters
- Sensor timestamping
- GPS latency compensation

## Tags

`#ekf-latency` `#time-horizon` `#sensor-buffering` `#gps-delay` `#optical-flow-fusion`