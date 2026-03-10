# Magnetometer Calibration (PX4 Guide)

**Source:** PX4 Documentation
**URL:** https://docs.px4.io/main/en/config/compass.html
**Type:** Official Documentation
**Relevance:** High - Practical calibration guide

## Summary

Complete guide to compass calibration in PX4. Covers hard/soft iron calibration, different calibration types, and verification.

## Calibration Types

| Type | Use Case | What it Does |
|------|----------|--------------|
| **Complete** | First setup, major changes | Offset + scale factor per axis |
| **Partial (Quick)** | Routine, payload changes | Offset only (hard iron) |
| **Large Vehicle** | Cannot rotate vehicle | Offset only using WMM |

## Hard Iron vs Soft Iron

**Hard Iron:**
- Permanent magnetic field in vehicle
- Causes constant offset
- Examples: speakers, motors, ferromagnetic parts
- Corrected by offset removal

**Soft Iron:**
- Material that distorts magnetic field
- Depends on orientation relative to magnetometer
- Requires 3x3 transformation matrix or scale factors

## Calibration Process (Complete)

1. Choose location away from metal objects
2. Connect via telemetry radio (not USB - causes interference)
3. Mount external compass away from electronics
4. Position vehicle in each orientation shown
5. Rotate around specified axis
6. Repeat for all orientations

## Quick Calibration (Figure-8)

```
Hold vehicle → Random partial rotations (~30°) → All axes → Wait for heading to stabilize
```

- Runs continuously when disarmed
- Applied immediately, saved after arming/disarming
- Compensates hard iron only

## Large Vehicle Calibration

```
 commander calibrate mag quick
```

Requirements:
- GNSS fix (for location)
- Vehicle aligned to True North
- Uses World Magnetic Model (WMM)

## Verification

After calibration:
- Heading indicator stable
- Arrow on map matches vehicle orientation
- No "mag sensors inconsistent" error

## Recalibration Triggers

- Compass module/orientation changed
- Exposure to strong magnetic field
- Structural/wiring/payload changes
- Region with different magnetic characteristics
- QGC reports inconsistency
- Heading drifts or toilet-bowls

## Parameters

| Parameter | Purpose |
|-----------|---------|
| CAL_MAGx_PRIO | Compass priority |
| CAL_MAGn_ROT | Rotation (internal if ==1) |
| SDLOG_MODE | Debug logging |

## Debugging

Set `SDLOG_MODE=1` and `SDLOG_PROFILE=64` to log raw sensor data.

## Relevance to ArduPilot

- Same calibration concepts
- Hard/soft iron compensation
- Mag consistency checks
- Priority-based compass selection

## Tags

`#magnetometer` `#compass-calibration` `#hard-iron` `#soft-iron` `#px4` `#calibration`