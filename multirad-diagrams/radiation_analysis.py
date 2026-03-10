#!/usr/bin/env python3
"""
Radiation Test Analysis for MultiRad EKF Case Study
Generates plots for failure analysis and correlation with radiation dose.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import re
import numpy as np
from collections import defaultdict

# Parse the log file
log_file = "/home/csilva/Downloads/2026-log-rad-drone(3).txt"

with open(log_file, 'r') as f:
    log_content = f.read()

# Extract events
executions = []  # (start_time, end_time, exit_code, pid, run_id, core)
resets = []  # (timestamp,)
crashes = []  # (timestamp, signal)

# Parse execution starts
start_pattern = r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d{6}) INFO: i([01])\[(\d+)\] started r(\d+)'
for match in re.finditer(start_pattern, log_content):
    timestamp_str, instance, pid, run_id = match.groups()
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d__%H:%M:%S__%f')
    executions.append({
        'start': timestamp,
        'instance': int(instance),
        'pid': int(pid),
        'run_id': int(run_id),
        'end': None,
        'exit_code': None,
        'signal': None
    })

# Parse execution ends (exited code=X or exited signal=Y)
exit_pattern = r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d{6}) (INFO|ERROR): i([01])\[(\d+)\] exited (code|signal)=(\d+)'
for match in re.finditer(exit_pattern, log_content):
    timestamp_str, level, instance, pid, exit_type, value = match.groups()
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d__%H:%M:%S__%f')
    
    # Find matching execution
    for exec_data in executions:
        if exec_data['instance'] == int(instance) and exec_data['pid'] == int(pid) and exec_data['end'] is None:
            exec_data['end'] = timestamp
            if exit_type == 'code':
                exec_data['exit_code'] = int(value)
            else:
                exec_data['signal'] = value
                exec_data['exit_code'] = -1  # Signal = crash
            break

# Parse resets
reset_pattern = r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d{6}) INFO: sut4 has been turned off'
for match in re.finditer(reset_pattern, log_content):
    timestamp_str = match.group(1)
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d__%H:%M:%S__%f')
    resets.append(timestamp)

# Parse service stopped (end of test)
stop_pattern = r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d{6}) INFO: service stopped'
service_stops = []
for match in re.finditer(stop_pattern, log_content):
    timestamp_str = match.group(1)
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d__%H:%M:%S__%f')
    service_stops.append(timestamp)

# Output vector data (from user)
output_vectors = [
    (36, 0x80000606, 1, 0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0),
    (13, 0x800005e6, 1, 0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0),
    (4,  0x80000516, 1, 0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0),
    (3,  0x800005d6, 1, 0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0),
    (3,  0x80000556, 1, 0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0),
]

# Flag definitions
FLAG_PROCESS_OK = 1 << 0
FLAG_LOG_PARSED = 1 << 1
FLAG_INIT_SEEN = 1 << 2
FLAG_REPLAY_COMPLETE = 1 << 3
FLAG_GPS_OK = 1 << 4
FLAG_IMU_OK = 1 << 5
FLAG_BARO_OK = 1 << 6
FLAG_MAG_OK = 1 << 7
FLAG_TIMING_OK = 1 << 8
FLAG_NO_ERRORS = 1 << 9
FLAG_ARMED_SEEN = 1 << 10
FAILURE_BIT = 1 << 31

def decode_flags(flags):
    """Decode output vector flags into component status."""
    is_failure = bool(flags & FAILURE_BIT)
    return {
        'failure': is_failure,
        'process_ok': bool(flags & FLAG_PROCESS_OK),
        'log_parsed': bool(flags & FLAG_LOG_PARSED),
        'init_seen': bool(flags & FLAG_INIT_SEEN),
        'replay_complete': bool(flags & FLAG_REPLAY_COMPLETE),
        'gps_ok': bool(flags & FLAG_GPS_OK),
        'imu_ok': bool(flags & FLAG_IMU_OK),
        'baro_ok': bool(flags & FLAG_BARO_OK),
        'mag_ok': bool(flags & FLAG_MAG_OK),
        'timing_ok': bool(flags & FLAG_TIMING_OK),
        'no_errors': bool(flags & FLAG_NO_ERRORS),
        'armed_seen': bool(flags & FLAG_ARMED_SEEN),
    }

# Analyze data
print(f"Total executions: {len(executions)}")
print(f"Executions with end: {sum(1 for e in executions if e['end'] is not None)}")
print(f"Total resets: {len(resets)}")
print(f"Service stops: {len(service_stops)}")

# Separate by date
feb25_execs = [e for e in executions if e['start'].date() == datetime(2026, 2, 25).date()]
feb26_execs = [e for e in executions if e['start'].date() == datetime(2026, 2, 26).date()]
feb27_execs = [e for e in executions if e['start'].date() == datetime(2026, 2, 27).date()]

print(f"Feb 25 executions: {len(feb25_execs)}")
print(f"Feb 26 executions: {len(feb26_execs)}")
print(f"Feb 27 executions: {len(feb27_execs)}")

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 20))

# ============================================
# PLOT 1: Execution Timeline
# ============================================
ax1 = fig.add_subplot(3, 2, 1)

# Filter executions with both start and end
complete_execs = [e for e in executions if e['end'] is not None and e['start'].date() == datetime(2026, 2, 25).date()]
complete_execs.sort(key=lambda x: x['start'])

if complete_execs:
    # Convert to hours from start
    start_time = datetime(2026, 2, 25, 8, 0, 0)
    
    for i, e in enumerate(complete_execs[:60]):  # First 60 for clarity
        start_h = (e['start'] - start_time).total_seconds() / 3600
        end_h = (e['end'] - start_time).total_seconds() / 3600
        duration = end_h - start_h
        
        color = 'green' if e['exit_code'] == 0 else ('red' if e['exit_code'] == 2 else 'orange')
        ax1.barh(i, duration, left=start_h, height=0.6, color=color, alpha=0.7)
    
    ax1.set_xlabel('Time (hours from 08:00)')
    ax1.set_ylabel('Execution #')
    ax1.set_title('Feb 25: Execution Timeline\n(Green=Success, Red=Fail code=2, Orange=Crash)')
    ax1.grid(True, alpha=0.3)

# ============================================
# PLOT 2: Resets Over Time
# ============================================
ax2 = fig.add_subplot(3, 2, 2)

if resets:
    feb25_resets = [r for r in resets if r.date() == datetime(2026, 2, 25).date()]
    start_time = datetime(2026, 2, 25, 8, 0, 0)
    
    # Bin resets by hour
    reset_hours = defaultdict(int)
    for r in feb25_resets:
        h = int((r - start_time).total_seconds() / 3600)
        reset_hours[h] += 1
    
    hours = sorted(reset_hours.keys())
    counts = [reset_hours[h] for h in hours]
    
    ax2.bar(hours, counts, color='red', alpha=0.7, edgecolor='darkred')
    ax2.set_xlabel('Time (hours from 08:00)')
    ax2.set_ylabel('Number of Resets')
    ax2.set_title(f'Feb 25: Board Resets Over Time\n(Total: {len(feb25_resets)} resets)')
    ax2.grid(True, alpha=0.3)
    
    # Add cumulative line
    cumulative = np.cumsum([reset_hours.get(h, 0) for h in range(max(hours)+1)])
    ax2_twin = ax2.twinx()
    ax2_twin.plot(range(max(hours)+1), cumulative, 'b--', linewidth=2, label='Cumulative')
    ax2_twin.set_ylabel('Cumulative Resets', color='blue')
    ax2_twin.tick_params(axis='y', labelcolor='blue')

# ============================================
# PLOT 3: Output Vector Flag Analysis
# ============================================
ax3 = fig.add_subplot(3, 2, 3)

# Decode flags and count failures per sensor
total_execs = sum(ov[0] for ov in output_vectors)
sensor_failures = {
    'GPS': 0,
    'IMU': 0,
    'BARO': 0,
    'MAG': 0,
    'Timing': 0,
    'Process': 0,
}

for count, flags, armed, gps_drops, pos_n, pos_e, pos_d, att_r, att_p, att_y in output_vectors:
    decoded = decode_flags(flags)
    if decoded['failure']:
        if not decoded['gps_ok']:
            sensor_failures['GPS'] += count
        if not decoded['imu_ok']:
            sensor_failures['IMU'] += count
        if not decoded['baro_ok']:
            sensor_failures['BARO'] += count
        if not decoded['mag_ok']:
            sensor_failures['MAG'] += count
        if not decoded['timing_ok']:
            sensor_failures['Timing'] += count
        if not decoded['process_ok']:
            sensor_failures['Process'] += count

sensors = list(sensor_failures.keys())
failures = list(sensor_failures.values())
colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

bars = ax3.bar(sensors, failures, color=colors, edgecolor='black', linewidth=1.5)
ax3.set_ylabel('Number of Executions with Failure')
ax3.set_title(f'Failure Distribution by Sensor\n(Total Executions: {total_execs}, All Failed)')
ax3.grid(True, alpha=0.3, axis='y')

# Add counts on bars
for bar, count in zip(bars, failures):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             str(count), ha='center', va='bottom', fontweight='bold')

# ============================================
# PLOT 4: Output Vector Flag Breakdown
# ============================================
ax4 = fig.add_subplot(3, 2, 4)

# Create heatmap of flag patterns
flag_names = ['Failure', 'Process', 'Log', 'Init', 'Replay', 'GPS', 'IMU', 'BARO', 'MAG', 'Timing', 'NoErr', 'Armed']
patterns = []
labels = []

for count, flags, armed, gps_drops, pos_n, pos_e, pos_d, att_r, att_p, att_y in output_vectors:
    decoded = decode_flags(flags)
    pattern = [
        decoded['failure'],
        decoded['process_ok'],
        decoded['log_parsed'],
        decoded['init_seen'],
        decoded['replay_complete'],
        decoded['gps_ok'],
        decoded['imu_ok'],
        decoded['baro_ok'],
        decoded['mag_ok'],
        decoded['timing_ok'],
        decoded['no_errors'],
        decoded['armed_seen'],
    ]
    patterns.append(pattern)
    labels.append(f'0x{flags:08X}\n(n={count})')

data = np.array(patterns).T

im = ax4.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax4.set_xticks(range(len(labels)))
ax4.set_xticklabels(labels, rotation=45, ha='right')
ax4.set_yticks(range(len(flag_names)))
ax4.set_yticklabels(flag_names)
ax4.set_title('Output Vector Flag Patterns\n(Green=OK, Red=Fail)')

# Add text annotations
for i in range(len(flag_names)):
    for j in range(len(labels)):
        text = 'OK' if data[i, j] else 'X'
        color = 'white' if data[i, j] else 'black'
        ax4.text(j, i, text, ha='center', va='center', color=color, fontsize=8, fontweight='bold')

plt.colorbar(im, ax=ax4, label='Status (1=OK, 0=Fail)')

# ============================================
# PLOT 5: Attitude Error Distribution
# ============================================
ax5 = fig.add_subplot(3, 2, 5)

# Parse attitude errors from output vectors
att_errors = []
for count, flags, armed, gps_drops, pos_n, pos_e, pos_d, att_r, att_p, att_y in output_vectors:
    att_errors.append({
        'count': count,
        'roll': att_r,
        'pitch': att_p,
        'yaw': att_y,
        'flags': flags,
    })

# Group by unique attitude error patterns
x_labels = [f"Pattern {i+1}\n(n={e['count']})" for i, e in enumerate(att_errors)]
x = np.arange(len(att_errors))
width = 0.25

bars1 = ax5.bar(x - width, [e['roll']*100 for e in att_errors], width, label='Roll Error', color='#e74c3c')
bars2 = ax5.bar(x, [e['pitch']*100 for e in att_errors], width, label='Pitch Error', color='#3498db')
bars3 = ax5.bar(x + width, [e['yaw']*100 for e in att_errors], width, label='Yaw Error', color='#2ecc71')

ax5.set_ylabel('Error Rate (%)')
ax5.set_xlabel('Failure Pattern')
ax5.set_title('Attitude Error Distribution by Failure Pattern')
ax5.set_xticks(x)
ax5.set_xticklabels(x_labels, rotation=45, ha='right')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# ============================================
# PLOT 6: Neutron Fluence vs Time
# ============================================
ax6 = fig.add_subplot(3, 2, 6)

# Neutron flux and time
flux = 2.6e6  # n/cm²/s
total_time_hours = 17.98
total_time_seconds = total_time_hours * 3600
fluence_total = flux * total_time_seconds

# Cumulative fluence over time
hours = np.linspace(0, total_time_hours, 100)
fluence = flux * hours * 3600  # n/cm²

ax6.plot(hours, fluence / 1e11, 'b-', linewidth=2, label='Cumulative Fluence')
ax6.fill_between(hours, 0, fluence / 1e11, alpha=0.3)

# Mark total fluence
ax6.axhline(y=fluence_total / 1e11, color='red', linestyle='--', linewidth=1.5, 
            label=f'Total: {fluence_total:.2e} n/cm²')

ax6.set_xlabel('Exposure Time (hours)')
ax6.set_ylabel('Neutron Fluence (×10¹¹ n/cm²)')
ax6.set_title(f'Accumulated Neutron Fluence\n(Flux: {flux:.1e} n/cm²/s)')
ax6.legend()
ax6.grid(True, alpha=0.3)
ax6.set_xlim(0, total_time_hours)
ax6.set_ylim(0, fluence_total / 1e11 * 1.1)

# Add second y-axis for dose
ax6_twin = ax6.twinx()
dose_rate = 1.14 / total_time_hours  # Gy/hour (approximate)
ax6_twin.set_ylabel('Approximate Dose (Gy)', color='green')
ax6_twin.plot(hours, hours * dose_rate, 'g--', alpha=0.5)
ax6_twin.tick_params(axis='y', labelcolor='green')
ax6_twin.set_ylim(0, total_time_hours * dose_rate * 1.1)

plt.tight_layout()
plt.savefig('/home/csilva/.openclaw/workspace/multirad-diagrams/radiation_analysis.png', dpi=150, bbox_inches='tight')
print("\nPlot saved to: /home/csilva/.openclaw/workspace/multirad-diagrams/radiation_analysis.png")

# ============================================
# SUMMARY STATISTICS
# ============================================
print("\n" + "="*60)
print("SUMMARY STATISTICS")
print("="*60)

# Execution outcomes
success_count = sum(1 for e in executions if e['exit_code'] == 0)
fail_count = sum(1 for e in executions if e['exit_code'] == 2)
crash_count = sum(1 for e in executions if e['exit_code'] == -1)
running_count = sum(1 for e in executions if e['end'] is None)

print(f"\nExecution Outcomes:")
print(f"  Success (exit 0): {success_count}")
print(f"  Failure (exit 2): {fail_count}")
print(f"  Crash (signal):   {crash_count}")
print(f"  Running/Unknown:  {running_count}")

# Failure rate
total_complete = success_count + fail_count + crash_count
if total_complete > 0:
    print(f"\n  Failure Rate: {(fail_count + crash_count) / total_complete * 100:.1f}%")

# Output vector analysis
print(f"\nOutput Vector Analysis:")
print(f"  Total executions analyzed: {total_execs}")
print(f"  Failure patterns: {len(output_vectors)}")
print(f"  All patterns have FAILURE bit set: 100% failure rate")

print(f"\nSensor Failure Correlation:")
for sensor, count in sensor_failures.items():
    print(f"  {sensor}: {count}/{total_execs} ({count/total_execs*100:.0f}%)")

print(f"\nRadiation Exposure:")
print(f"  Neutron flux: {flux:.2e} n/cm²/s")
print(f"  Exposure time: {total_time_hours:.2f} hours")
print(f"  Total fluence: {fluence_total:.2e} n/cm²")
print(f"  Approximate dose: ~1.14 Gy (14 MeV)")

# Time analysis
if feb25_resets:
    print(f"\nReset Analysis (Feb 25):")
    print(f"  Total resets: {len(feb25_resets)}")
    print(f"  Reset rate: {len(feb25_resets) / total_time_hours:.1f} resets/hour")
    print(f"  Mean time between resets: {total_time_hours * 60 / len(feb25_resets):.1f} minutes")