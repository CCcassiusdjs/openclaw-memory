#!/usr/bin/env python3
"""
Complete Architecture Diagram for MultiRad + EKF Platform
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np

fig = plt.figure(figsize=(20, 24))

# ============================================
# TITLE
# ============================================
fig.suptitle('MultiRad + EKF Platform - Complete Architecture', fontsize=20, fontweight='bold', y=0.98)

# ============================================
# PLOT 1: EKF Libraries Comparison
# ============================================
ax1 = fig.add_subplot(3, 2, 1)

ekf_versions = ['EKF (Original)', 'EKF2', 'EKF3']
lines_of_code = [2333, 12469, 17215]
core_files = [3, 14, 15]

x = np.arange(len(ekf_versions))
width = 0.35

bars1 = ax1.bar(x - width/2, lines_of_code, width, label='Lines of Code', color='#3498db', edgecolor='black')
ax1_twin = ax1.twinx()
bars2 = ax1_twin.bar(x + width/2, core_files, width, label='Core Files', color='#e74c3c', edgecolor='black')

ax1.set_xlabel('EKF Version')
ax1.set_ylabel('Lines of Code', color='#3498db')
ax1_twin.set_ylabel('Number of Files', color='#e74c3c')
ax1.set_xticks(x)
ax1.set_xticklabels(ekf_versions)
ax1.set_title('EKF Library Evolution')
ax1.tick_params(axis='y', labelcolor='#3498db')
ax1_twin.tick_params(axis='y', labelcolor='#e74c3c')

for bar, val in zip(bars1, lines_of_code):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200, str(val), ha='center', fontsize=9)
for bar, val in zip(bars2, core_files):
    ax1_twin.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, str(val), ha='center', fontsize=9)

ax1.grid(True, alpha=0.3, axis='y')

# ============================================
# PLOT 2: EKF3 Module Breakdown
# ============================================
ax2 = fig.add_subplot(3, 2, 2)

modules = ['core.cpp', 'core.h', 'PosVelFusion', 'MagFusion', 'Measurements', 'Outputs', 'Control', 'AirDataFusion', 'OptFlowFusion', 'RngBcnFusion', 'VehicleStatus', 'Logging', 'GyroBias']
lines = [2272, 1666, 2116, 1635, 1544, 678, 881, 714, 789, 688, 482, 456, 24]

colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(modules)))
bars = ax2.barh(modules, lines, color=colors, edgecolor='black')
ax2.set_xlabel('Lines of Code')
ax2.set_title('EKF3 Module Breakdown (17,215 lines total)')
ax2.grid(True, alpha=0.3, axis='x')

for bar, val in zip(bars, lines):
    ax2.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=8)

# ============================================
# PLOT 3: MultiRad Platform Architecture
# ============================================
ax3 = fig.add_subplot(3, 2, 3)
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.set_title('MultiRad Platform Architecture', fontsize=14, fontweight='bold')

# Draw boxes
def draw_box(ax, x, y, w, h, label, color='#3498db', fontsize=8):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", 
                         facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.8)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=fontsize, fontweight='bold', wrap=True)

# Level 0: SUT (System Under Test)
draw_box(ax3, 0.5, 0.5, 4, 1.5, 'SUT (sut4)\nRaspberry Pi / ARM', '#e74c3c', 10)
draw_box(ax3, 5.5, 0.5, 4, 1.5, 'ccX (Control)\nLinux/x86_64', '#2ecc71', 10)

# Level 1: MultiRad Platform
draw_box(ax3, 1, 2.5, 8, 1.5, 'MultiRad Platform\n(multirad_platform_radiation_tests)', '#9b59b6', 10)

# Level 2: Case Studies
draw_box(ax3, 0.2, 4.5, 3, 1.3, 'EKF Case\n(arducopter-ekf)', '#f39c12', 9)
draw_box(ax3, 3.5, 4.5, 3, 1.3, 'MobileNet Case\n(mobilenet-x1)', '#f39c12', 9)
draw_box(ax3, 6.8, 4.5, 3, 1.3, 'Edge Case\n(edge)', '#f39c12', 9)

# Level 3: Case Components
draw_box(ax3, 0.5, 6.5, 3.5, 1, 'case_runner.c\n(exec fork/wait)', '#1abc9c', 8)
draw_box(ax3, 4.5, 6.5, 3, 1, 'output_vector\n_extractor.c', '#1abc9c', 8)
draw_box(ax3, 8, 6.5, 1.5, 1, 'checksums', '#1abc9c', 8)

# Level 4: ArduCopter
draw_box(ax3, 0.5, 8, 9, 1.5, 'ArduCopter (linux-emu board)\n+ libioctl_shim.so (LD_PRELOAD)', '#34495e', 10)

# Arrows
ax3.annotate('', xy=(2.5, 2.3), xytext=(2.5, 2.1), arrowprops=dict(arrowstyle='->', lw=1.5))
ax3.annotate('', xy=(5, 4.3), xytext=(5, 4.1), arrowprops=dict(arrowstyle='->', lw=1.5))
ax3.annotate('', xy=(2, 6.3), xytext=(2, 6.1), arrowprops=dict(arrowstyle='->', lw=1.5))
ax3.annotate('', xy=(5, 7.8), xytext=(5, 7.6), arrowprops=dict(arrowstyle='->', lw=1.5))

# ============================================
# PLOT 4: EKF3 State and Sensor Flow
# ============================================
ax4 = fig.add_subplot(3, 2, 4)
ax4.set_xlim(0, 12)
ax4.set_ylim(0, 10)
ax4.set_aspect('equal')
ax4.axis('off')
ax4.set_title('EKF3 State Estimation Flow', fontsize=14, fontweight='bold')

# Input sensors
sensors = [
    (1, 8.5, 'GPS\n(NMEA)', '#3498db'),
    (3.5, 8.5, 'IMU\n(ICM20602)', '#e74c3c'),
    (6, 8.5, 'BARO\n(BMP280)', '#2ecc71'),
    (8.5, 8.5, 'MAG\n(AK09916)', '#f39c12'),
]
for x, y, label, color in sensors:
    draw_box(ax4, x-0.7, y-0.6, 1.4, 1.2, label, color, 7)

# 3 EKF Cores
for i in range(3):
    draw_box(ax4, 1.5 + i*3.5, 5.5, 3, 1.5, f'EKF3_core[{i}]\n24 states\nerrorScore', '#9b59b6', 8)

# Voting
draw_box(ax4, 4, 3, 4, 1.2, 'Core Selection\n(errorScore voting)', '#1abc9c', 9)

# Output
draw_box(ax4, 4.5, 0.5, 3, 1.2, 'Output\nPosition/Velocity\nAttitude', '#34495e', 8)

# Arrows - sensors to cores
for i in range(3):
    for sx, sy, _, _ in sensors:
        ax4.annotate('', xy=(3+i*3.5, 7), xytext=(sx, sy-0.6), 
                    arrowprops=dict(arrowstyle='->', lw=0.5, alpha=0.5))

# Arrows - cores to voting
for i in range(3):
    ax4.annotate('', xy=(6, 4.2), xytext=(3+i*3.5, 5.5), 
                arrowprops=dict(arrowstyle='->', lw=1.5))

# Arrow - voting to output
ax4.annotate('', xy=(6, 1.7), xytext=(6, 3), arrowprops=dict(arrowstyle='->', lw=2))

# Labels
ax4.text(0.3, 8.5, 'SENSORS', fontsize=10, fontweight='bold', rotation=90, va='center')
ax4.text(0.3, 5.5, 'CORES', fontsize=10, fontweight='bold', rotation=90, va='center')

# ============================================
# PLOT 5: Test Platform Hardware
# ============================================
ax5 = fig.add_subplot(3, 2, 5)
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 10)
ax5.set_aspect('equal')
ax5.axis('off')
ax5.set_title('Radiation Test Platform (sut4)', fontsize=14, fontweight='bold')

# Main board
draw_box(ax5, 2, 3, 6, 4, 'Raspberry Pi / SBC\n(ARM Cortex-A)\n\nLinux + Emulator\nShim + Sensors', '#2c3e50', 10)

# Radiation source
draw_box(ax5, 0.5, 7, 2, 1.5, 'Neutron\nSource\n14 MeV', '#e74c3c', 9)
ax5.annotate('', xy=(3, 6.5), xytext=(2.5, 7.5), arrowprops=dict(arrowstyle='->', lw=2, color='red'))

# External components
draw_box(ax5, 8.2, 5, 1.5, 2, 'GPS\nAntenna', '#3498db', 8)
draw_box(ax5, 8.2, 3, 1.5, 1.5, 'Debug\nUART', '#f39c12', 8)

# Control connection
ax5.annotate('', xy=(2, 5), xytext=(0.5, 5), arrowprops=dict(arrowstyle='<->', lw=1.5))
ax5.text(0.5, 4, 'Control\n(ccX)', fontsize=8, ha='center')

# Reset relay
draw_box(ax5, 0.5, 2, 1.5, 1, 'Reset\nRelay', '#9b59b6', 8)
ax5.annotate('', xy=(2, 3), xytext=(2, 2.5), arrowprops=dict(arrowstyle='->', lw=1))

# Test parameters
ax5.text(5, 0.5, 'Flux: 2.6×10⁶ n/cm²/s  |  Fluence: 1.68×10¹¹ n/cm²  |  Dose: ~1.14 Gy', 
         fontsize=9, ha='center', style='italic')

# ============================================
# PLOT 6: Failure Analysis Summary
# ============================================
ax6 = fig.add_subplot(3, 2, 6)

# Data from radiation test
categories = ['Total Execs', 'Success', 'Failure', 'Crash', 'Resets']
values = [269, 27, 59, 0, 217]
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']

bars = ax6.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
ax6.set_ylabel('Count')
ax6.set_title('Radiation Test Results Summary', fontsize=12, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='y')

for bar, val in zip(bars, values):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, str(val), ha='center', fontsize=10, fontweight='bold')

# Add failure rate annotation
ax6.text(2.5, 200, 'Failure Rate: 68.6%\n(59/86 completed)', fontsize=10, ha='center', 
         bbox=dict(boxstyle='round', facecolor='#e74c3c', alpha=0.3))

# Add sensor correlation
ax6.text(4.5, 150, 'Sensor Failures:\nGPS: 83%\nIMU: 78%\nMAG: 73%\nBARO: 68%', 
         fontsize=8, ha='center', bbox=dict(boxstyle='round', facecolor='#f39c12', alpha=0.3))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/csilva/.openclaw/workspace/multirad-diagrams/multirad-complete-architecture.png', dpi=150, bbox_inches='tight')
print("Architecture diagram saved to: /home/csilva/.openclaw/workspace/multirad-diagrams/multirad-complete-architecture.png")