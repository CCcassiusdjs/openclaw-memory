# NVIDIA Jetson Edge AI Deployment

**Source:** https://docs.edgeimpulse.com/docs/edge-ai-hardware/gpu/nvidia-jetson
**Date:** 2026-03-12
**Status:** read

---

## Overview

NVIDIA Jetson devices are embedded Linux boards with GPU-accelerated processors (NVIDIA Tegra) targeted at edge AI applications. Fully supported by Edge Impulse.

## Device Families

| Family | Devices |
|--------|---------|
| **Jetson Orin** | AGX Orin, Orin NX, Orin Nano |
| **Jetson (Legacy)** | AGX Xavier, Xavier NX, TX2, TX1, Nano |

## JetPack Versions

| JetPack | Target Device | Edge Impulse Deployment |
|---------|---------------|------------------------|
| 4.6.4 | Jetson (Nano, TX2, Xavier) | NVIDIA Jetson (JetPack 4.6.4) |
| 5.1.2 | Jetson Orin | NVIDIA Jetson Orin (JetPack 5.1.2) |
| 6.0 | Jetson Orin | NVIDIA Jetson Orin (JetPack 6.0) |

## Setup Process

1. **Flash SD Card** with JetPack image
2. **Connect Ethernet** (no WiFi on Jetson)
3. **Run setup script**:
   ```bash
   # For Jetson
   wget -q -O - https://cdn.edgeimpulse.com/firmware/linux/jetson.sh | bash
   
   # For Orin
   wget -q -O - https://cdn.edgeimpulse.com/firmware/linux/orin.sh | bash
   ```
4. **Connect to Edge Impulse**:
   ```bash
   edge-impulse-linux
   ```
5. **Deploy model**:
   ```bash
   edge-impulse-linux-runner
   ```

## Performance Optimization

### Power Modes
Jetson has aggressive power saving that can hinder GPU performance:

```bash
# Enable maximum performance (mode 0)
sudo /usr/sbin/nvpmodel -m 0
sudo /usr/bin/jetson_clocks
```

**Note**: Use dedicated power supply (not USB) for performance mode.

### GPU vs CPU
- **Vision models**: GPU faster with TensorRT
- **Small keyword spotting**: CPU may be faster
- **Gesture recognition**: CPU often faster than GPU

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "OOM killed!" | Use `make -j$(nproc)` to limit jobs |
| Missing libjpeg | Rerun setup script |
| "Failed to start device monitor" | `sudo chown -R $(whoami) $HOME` |
| Missing shared library | Use SD card image with correct JetPack |

## Deployment Targets

- **EIM Deployment**: Direct Edge Impulse Linux binary
- **Docker Deployment**: Containerized deployment

## Sensor Support

- USB cameras (most popular webcams work)
- USB microphones
- Custom sensors via Linux SDK (Node.js, Python, Go, C++)

---

## Takeaways

1. **JetPack version matters** - match Edge Impulse deployment to JetPack version
2. **Power via DC barrel** - not USB for stable operation
3. **Enable performance mode** for GPU workloads
4. **GPU vs CPU depends on model size** - small models may be faster on CPU
5. **Docker deployment available** for containerized inference