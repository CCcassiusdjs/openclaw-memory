# GNSS/MEMS-INS Integration using EKF on Lie Groups

**Source:** arXiv:2210.02983 (2022)
**Type:** Academic Paper
**Relevance:** High - Advanced EKF formulation for drones

## Summary

This paper describes an **Extended Kalman Filter on Lie Groups** for GNSS/INS integration in drone navigation. Uses matrix Lie Groups to aggregate position, velocity, attitude, and IMU biases as a single element.

## Key Concepts

### Lie Group Formulation
- **State representation**: Single element on matrix Lie Group
- **Aggregates**: Position, velocity, attitude, IMU biases
- **Advantage**: Elegant mathematical framework for rotations

### Motivation
- Drone-borne Differential Interferometric SAR (DinSAR)
- High-precision navigation for short-flight missions
- Low-cost MEMS sensors

### Key Contributions
1. **EKF on Lie Groups**: Novel formulation
2. **RTS Smoother**: Rauch-Tung-Striebel implementation
3. **Novel heading initialization**: Alternative to gyro-compassing
4. **Outlier rejection**: Mahalanobis Distance + χ²-test

### Comparison
- Classic quaternion-based navigation
- Euler angle approaches
- Commercial software benchmarking

### Results
- Outperforms state-of-the-art commercial software
- Better DinSAR processing accuracy

## Mathematical Framework

- Dynamic model on matrix Lie Group
- Multiplicative updates for group elements
- Loosely coupled GNSS/INS integration
- Post-processing applications (not real-time)

## Relevance to ArduPilot EKF

- Alternative formulation to quaternion-based EKF
- May provide better numerical properties
- RTS smoother for post-processing
- Outlier rejection techniques applicable

## Cross-References

- EKF state estimation
- Quaternion mathematics
- MEMS sensor limitations

## Tags

`#lie-groups` `#gnss-ins` `#mems-sensors` `#rts-smoother` `#outlier-rejection` `#dinsar`