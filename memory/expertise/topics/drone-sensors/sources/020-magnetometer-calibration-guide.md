# How to Calibrate a Magnetometer

**Source:** appelsiini.net (Joni Kähärä)
**URL:** https://www.appelsiini.net/2018/calibrate-magnetometer/
**Type:** Tutorial
**Relevance:** High - Practical calibration mathematics

## Summary

Practical guide to magnetometer calibration with hard/soft iron correction mathematics and visualization.

## Hard Iron Distortion

**Definition:** Permanent magnetic field from ferromagnetic materials near sensor.

**Characteristics:**
- Always additive to Earth's field
- Location and orientation don't change
- Example: phone speaker

**Correction:**
```python
offset_x = (max(x) + min(x)) / 2
offset_y = (max(y) + min(y)) / 2
offset_z = (max(z) + min(z)) / 2

corrected_x = sensor_x - offset_x
corrected_y = sensor_y - offset_y
corrected_z = sensor_z - offset_z
```

## Soft Iron Distortion

**Definition:** Material that distorts magnetic field but doesn't generate one.

**Characteristics:**
- Distortion depends on orientation relative to magnetometer
- Cannot be removed by simple offset
- Requires transformation matrix or scale factors

**Correction (Scale Bias Method):**
```python
avg_delta_x = (max(x) - min(x)) / 2
avg_delta_y = (max(y) - min(y)) / 2
avg_delta_z = (max(z) - min(z)) / 2

avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

scale_x = avg_delta / avg_delta_x
scale_y = avg_delta / avg_delta_y
scale_z = avg_delta / avg_delta_z

corrected_x = (sensor_x - offset_x) * scale_x
corrected_y = (sensor_y - offset_y) * scale_y
corrected_z = (sensor_z - offset_z) * scale_z
```

## Visualization

**Ideal:** Three spheres centered at (0,0)

**With Hard Iron:** Sphere offset from center

**With Soft Iron:** Ellipsoid instead of sphere

**Corrected:** Sphere centered at origin

## Data Collection

1. Move sensor in figure-8 pattern
2. Rotate multiple times around X, Y, Z axes
3. Capture 1-2 minutes of data
4. More data = better calibration

## Alternative Methods

1. **Ellipsoid Fitting** - More accurate, computationally expensive
2. **Premerlani Offset Cancellation** - On-the-fly calibration
3. **NXP AN4246** - eCompass calibration in presence of interference

## Relevance to ArduPilot

- Hard iron = magnetometer bias learned by EKF
- Soft iron = scale factors in COMPASS_SCALE parameters
- Figure-8 calibration same as PX4 quick calibration
- Ellipsoid fitting = complete calibration

## Cross-References

- PX4 compass calibration
- ArduPilot compass setup
- NXP Application Note AN4246

## Tags

`#magnetometer` `#calibration` `#hard-iron` `#soft-iron` `#scale-factor` `#ellipsoid-fitting`