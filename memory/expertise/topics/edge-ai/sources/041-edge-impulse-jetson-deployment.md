# Edge Impulse NVIDIA Jetson Deployment

**Source:** https://docs.edgeimpulse.com/docs/edge-ai-hardware/gpu/nvidia-jetson
**Type:** Official Documentation (Edge Impulse)
**Date:** 2025
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

Complete guide for deploying Edge Impulse ML models on NVIDIA Jetson devices (Orin and legacy series). Covers setup, configuration, GPU acceleration, and troubleshooting.

## NVIDIA Jetson Device Families

### NVIDIA Jetson Orin (Current Generation)
- Jetson AGX Orin Series
- Jetson Orin NX Series
- Jetson Orin Nano Series

### NVIDIA Jetson (Legacy Generation)
- Jetson AGX Xavier Series
- Jetson Xavier NX Series
- Jetson TX2 Series
- Jetson TX1
- Jetson Nano

## Hardware Setup

### Power Considerations
- **USB Power**: Technically supported but unreliable
- **DC Barrel Connector**: Recommended for stable operation
- **Jumper Configuration**: Must change when switching power sources
- **First Boot**: Can boot without external monitor/keyboard when using DC power

### JetPack Versions

| Device | JetPack Version | L4T Reference |
|--------|-----------------|---------------|
| Jetson Orin | 5.1.2 or 6.0 | R35.4.1 / R36.x |
| Jetson Legacy | 4.6.4 | R32.7.5 |

> **Note**: Migration to JetPack 6.0 requires UEFI firmware update from earlier versions.

## Edge Impulse Setup

### Installation Script
```bash
# For Jetson (legacy)
wget -q -O - https://cdn.edgeimpulse.com/firmware/linux/jetson.sh | bash

# For Orin (current)
wget -q -O - https://cdn.edgeimpulse.com/firmware/linux/orin.sh | bash
```

### Connecting to Edge Impulse
```bash
# Connect device
edge-impulse-linux

# Switch projects
edge-impulse-linux --clean
```

## GPU Acceleration

### Automatic Hardware Acceleration
The `edge-impulse-linux-runner` automatically:
1. Compiles model with full GPU acceleration
2. Downloads optimized model to Jetson
3. Starts classification with hardware acceleration

### Deployment Targets

| JetPack Version | EIM Deployment | Docker Deployment |
|-----------------|----------------|-------------------|
| 4.6.4 | NVIDIA Jetson (JetPack 4.6.4) | Docker (JetPack 4.6.4) |
| 5.1.2 | NVIDIA Jetson Orin (JetPack 5.1.2) | Docker (JetPack 5.1.2) |
| 6.0 | NVIDIA Jetson Orin (JetPack 6.0) | Docker (JetPack 6.0) |

## Performance Optimization

### Power Modes
Jetson devices have aggressive power saving features that can affect GPU performance.

**Enable Maximum Performance:**
```bash
# Switch to maximum power mode (mode ID 0)
sudo /usr/sbin/nvpmodel -m 0

# Set clocks to maximum
sudo /usr/bin/jetson_clocks
```

> **For NVIDIA Jetson Xavier NX**: Use **mode ID 8** instead of 0

### Model Size vs. Efficiency
- **Small models**: May run faster on CPU than GPU
- **Large models**: Benefit significantly from GPU acceleration
- **Vision models**: Generally faster on GPU
- **Keyword spotting (small)**: Often faster on CPU
- **Gesture recognition**: Mixed results - test both

## Troubleshooting

### OOM Killed Error
**Problem**: `make -j` without job limits causes out-of-memory.

**Solution**:
```bash
# Use nproc to limit jobs
make -j$(nproc)
```

### Missing Image Format Support
**Problem**: "Input buffer contains unsupported image format"

**Diagnosis**:
```bash
vips --vips-config
# Look for: file import/export with libjpeg: yes
```

**Solution**: Rerun setup script and check for errors.

### Failed Device Monitor
**Problem**: "Failed to start device monitor!"

**Solution**:
```bash
sudo chown -R $(whoami) $HOME
```

### Missing Shared Library
**Problem**: `libnvinfer.so.8: cannot open shared object file`

**Solution**: Use official SD card image with JetPack (includes TensorRT libraries).

## Camera/Microphone Integration

- USB webcams work out-of-box
- Most popular USB cameras supported
- Linux SDK available for custom sensors (Node.js, Python, Go, C++ examples)

## Live Classification Demo

When running image models, access the camera feed:
1. Find "Want to see a feed of the camera..." message in console
2. Open URL in browser on same network
3. View camera feed with live classification overlay

## Key Takeaways

1. **Power Matters**: Use DC barrel connector for stable operation
2. **JetPack Versions**: Match deployment target to installed JetPack
3. **GPU Efficiency**: Larger models benefit more from GPU acceleration
4. **Performance Modes**: Enable maximum performance for benchmarking
5. **Model Testing**: Test both CPU and GPU paths for small models

## Related Topics

- TensorRT optimization
- Jetson Linux Developer Guide
- Edge Impulse Linux SDK
- Docker deployment on Jetson