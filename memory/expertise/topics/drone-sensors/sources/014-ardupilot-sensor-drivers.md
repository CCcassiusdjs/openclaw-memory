# ArduPilot Sensor Drivers Architecture

**Source:** ArduPilot Dev Documentation
**URL:** https://ardupilot.org/dev/docs/code-overview-sensor-drivers.html
**Type:** Technical Documentation
**Relevance:** High - Architecture for sensor integration

## Summary

Explains the architecture of sensor drivers in ArduPilot, including supported protocols, front-end/back-end split, and how driver code runs.

## Key Concepts

### Supported Protocols

| Protocol | Speed | Distance | Pins | Notes |
|----------|-------|----------|------|-------|
| **I2C** | 100-400kHz | <1m | 4 | Multi-slave, low speed |
| **SPI** | 20MHz+ | <10cm | 5+ | Very fast, single slave |
| **UART/Serial** | 57K-1.5Mbps | ~1m | 4-6 | Character-based, longer distance |
| **CAN (UAVCAN/DroneCAN)** | 1Mbps | Long | 3+ | Multi-master, packet-based |

### Front-End / Back-End Split

**Architecture:**
- **Front-End**: Vehicle-facing API, holds user parameters
- **Back-End**: Sensor-specific implementation
- **Pattern**: One front-end, multiple back-ends

**How it works:**
1. Front-end creates back-ends at startup (auto-detect or via `_TYPE` params)
2. Back-ends run in background thread
3. Main thread (400Hz for copter) pulls latest data from front-end

### Thread Architecture

```
Background Thread                    Main Thread (400Hz)
     │                                      │
     │  ┌─────────────────┐                │
     └──│ Sensor Backends │                │
        │ - Read raw data │                │
        │ - Convert units │                │
        │ - Buffer data   │                │
        └─────────────────┘                │
                    │                      │
                    └───── Buffers ────────┼──→ AHRS/EKF
                                           └──→ Vehicle code
```

### Driver Patterns

**I2C/SPI Drivers:**
- Must run in background thread
- Use `register_periodic_callback()` for timer
- Use semaphores for bus access

**UART/Serial Drivers:**
- Can run in main thread
- Serial driver has its own buffer
- Check for new characters in `get_reading()`

### Code Examples

**Front-End Update Method:**
```cpp
void AP_RangeFinder::update(void) {
    for (uint8_t i=0; i<num_drivers; i++) {
        _drivers[i]->update();
    }
}
```

**Back-End Timer Registration (I2C):**
```cpp
// Register timer at 20Hz
_dev->register_periodic_callback(20000, FUNCTOR_BIND_MEMBER(&AP_RangeFinder_LightWare_I2C::timer, void));
```

**SPI High-Rate Read (MPU9250):**
```cpp
// Read at 1000Hz
_dev->register_periodic_callback(1000, FUNCTOR_BIND_MEMBER(&AP_InertialSensor_MPU9250::_read_sample, void));
```

## Important Rules

1. **No wait/sleep code** - Blocks main or background thread
2. **Use semaphores** - For shared bus access (SPI/I2C)
3. **Add library to wscript** - Must be linked in vehicle directory

## Data Flow

```
Sensor Hardware
      ↓
Back-End (Background Thread)
      ↓ Raw data → Convert → Buffer
Front-End (Main Thread Access)
      ↓
AHRS/EKF → Vehicle Code
```

## Relevance to ArduPilot EKF

- EKF pulls data from sensor front-ends
- IMU data at 400-1000Hz typical
- GPS data at 1-5Hz typical
- Understanding driver architecture helps debug sensor issues

## Tags

`#sensor-drivers` `#architecture` `#i2c` `#spi` `#uart` `#can-bus` `#frontend-backend` `#threading`