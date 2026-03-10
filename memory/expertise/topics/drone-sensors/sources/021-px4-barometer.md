# Barometers (PX4 Guide)

**Source:** PX4 Documentation
**URL:** https://docs.px4.io/main/en/sensor/barometer
**Type:** Official Documentation
**Relevance:** High - Altitude estimation in drones

## Summary

Barometers measure atmospheric pressure and provide altitude data. PX4 supports multiple barometer types with automatic selection and calibration.

## Hardware Options

| Sensor | Type | Notes |
|--------|------|-------|
| **BMP280** | I2C/SPI | Common in FCs |
| **BMP388** | I2C/SPI | ±0.66m accuracy |
| **DPS310** | I2C/SPI | High precision |
| **MS5611** | I2C/SPI | Pixhawk standard |
| **MS5837** | I2C | Water resistant |
| **LPS22HB** | I2C | Low power |
| **LPS33HW** | I2C | Waterproof |

## Accuracy Specifications

| Sensor | Resolution | Accuracy | TCO |
|--------|------------|----------|-----|
| **BMP388** | 17-bit | ±0.66m | 0.75 Pa/K |
| **ND015A** | 17-bit | 0.10% | - |

## PX4 Configuration

Parameters:
- **EKF2_BARO_CTRL**: Enable/disable baro for height estimation
- **CAL_BAROx_PRIO**: Selection priority (higher = preferred)
- **CAL_BAROx_PRIO = 0**: Disable barometer

## Auto-Calibration

### Relative Calibration
- Runs at startup
- Aligns secondary sensors to primary
- Prevents altitude jumps during sensor switch
- Always enabled

### GNSS-Baro Calibration
- Requires GNSS with EPV ≤ 8m
- Aligns baro to GNSS altitude
- 0.1m precision
- Saves offsets to parameters
- One-time per boot
- **Vulnerability**: Faulty GNSS during boot = wrong altitude reference

## Accuracy Factors

1. **Temperature drift**: Sensor temperature coefficient (TCO)
2. **Pressure changes**: Weather, altitude changes
3. **Prop wash**: Airflow from propellers affects reading
4. **GPS fusion**: Baro calibrated against GPS altitude

## EKF Integration

Barometer provides:
- Vertical position measurement
- Vertical velocity (via derivative)
- Used with GPS for altitude estimation

## Relevance to ArduPilot

- Same barometer types supported
- Same auto-calibration concept
- EKF_ALT_NOISE controls baro weighting
- Altitude source selection (baro vs range finder)

## Tags

`#barometer` `#altitude` `#pressure-sensor` `#bmp388` `#ms5611` `#auto-calibration`