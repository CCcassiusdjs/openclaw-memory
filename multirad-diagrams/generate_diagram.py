#!/usr/bin/env python3
"""Generate EKF system diagram as PNG"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Setup
fig, ax = plt.subplots(1, 1, figsize=(16, 12), facecolor='#0a0a1a')
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#0a0a1a')

# Colors
colors = {
    'bg_dark': '#0f0f1a',
    'bg_medium': '#1a1a2e',
    'bg_light': '#16213e',
    'border': '#4a4a6a',
    'text': '#eeeeee',
    'accent1': '#00b894',
    'accent2': '#6c5ce7',
    'accent3': '#fd79a8',
    'failure': '#e74c3c',
    'success': '#27ae60',
    'warning': '#f39c12',
}

def draw_box(ax, x, y, w, h, label, color, fontsize=10):
    box = FancyBboxPatch((x, y), w, h, 
                          boxstyle="round,pad=0.02,rounding_size=0.1",
                          facecolor=color['bg_medium'],
                          edgecolor=color['border'],
                          linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label, 
            ha='center', va='center', 
            fontsize=fontsize, color=color['text'],
            fontweight='bold', wrap=True)

def draw_sensor_box(ax, x, y, w, h, label, rate, color, fontsize=9):
    box = FancyBboxPatch((x, y), w, h, 
                          boxstyle="round,pad=0.02,rounding_size=0.05",
                          facecolor=color['bg_light'],
                          edgecolor=color['accent1'],
                          linewidth=1)
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.65, label, 
            ha='center', va='center', 
            fontsize=fontsize, color=color['text'],
            fontweight='bold')
    ax.text(x + w/2, y + h*0.3, rate, 
            ha='center', va='center', 
            fontsize=fontsize-2, color=color['accent1'])

def draw_ekf_box(ax, x, y, w, h, label, color, fontsize=11):
    box = FancyBboxPatch((x, y), w, h, 
                          boxstyle="round,pad=0.02,rounding_size=0.1",
                          facecolor=color['bg_medium'],
                          edgecolor=color['accent2'],
                          linewidth=2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label, 
            ha='center', va='center', 
            fontsize=fontsize, color=color['text'],
            fontweight='bold')

def draw_arrow(ax, start, end, color='#6a6a8a', style='->', lw=1.5):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))

# Title
ax.text(8, 11.5, 'Sistema EKF3 - ArduPilot', 
        ha='center', va='center', fontsize=18, 
        color=colors['text'], fontweight='bold')

# INPUT Section
ax.text(2, 10.5, '[INPUT]', ha='center', va='center', 
        fontsize=12, color=colors['accent1'], fontweight='bold')

# Sensors
draw_sensor_box(ax, 0.5, 9.2, 1.5, 0.7, 'IMU 0', '400 Hz', colors)
draw_sensor_box(ax, 0.5, 8.3, 1.5, 0.7, 'IMU 1', '400 Hz', colors)
draw_sensor_box(ax, 0.5, 7.4, 1.5, 0.7, 'IMU 2', '400 Hz', colors)

draw_sensor_box(ax, 2.2, 9.2, 1.5, 0.7, 'BARO 0', '50 Hz', colors)
draw_sensor_box(ax, 2.2, 8.3, 1.5, 0.7, 'BARO 1', '50 Hz', colors)
draw_sensor_box(ax, 2.2, 7.4, 1.5, 0.7, 'BARO 2', '50 Hz', colors)

draw_sensor_box(ax, 3.9, 9.2, 1.5, 0.7, 'MAG 0', '50 Hz', colors)
draw_sensor_box(ax, 3.9, 8.3, 1.5, 0.7, 'MAG 1', '50 Hz', colors)
draw_sensor_box(ax, 3.9, 7.4, 1.5, 0.7, 'MAG 2', '50 Hz', colors)

draw_sensor_box(ax, 5.6, 8.3, 1.5, 0.7, 'GPS', '10 Hz', colors)

# EKF Section
ax.text(8, 10.5, '[EKF CORES]', ha='center', va='center', 
        fontsize=12, color=colors['accent2'], fontweight='bold')

# Core boxes
draw_ekf_box(ax, 7, 9, 2, 1.5, 'CORE 0\n\nIMU 0\nBARO 0\nMAG 0', colors)
draw_ekf_box(ax, 7, 7.2, 2, 1.5, 'CORE 1\n\nIMU 1\nBARO 1\nMAG 1', colors)

# Core 2 (disabled)
box2 = FancyBboxPatch((9.2, 8.1), 1.8, 1.5, 
                       boxstyle="round,pad=0.02,rounding_size=0.1",
                       facecolor='#1a1a1a',
                       edgecolor='#444444',
                       linewidth=1,
                       linestyle='--')
ax.add_patch(box2)
ax.text(10.1, 8.85, 'CORE 2\n(não usado)', 
        ha='center', va='center', fontsize=9, 
        color='#666666', style='italic')

# GPS shared
ax.text(8, 6.6, 'GPS compartilhado', ha='center', va='center', 
        fontsize=9, color=colors['warning'])

# Arrows from sensors to cores
draw_arrow(ax, (2, 9.55), (7, 9.75), colors['accent1'])
draw_arrow(ax, (3.7, 9.55), (7, 9.5), colors['accent1'])
draw_arrow(ax, (5.4, 9.55), (7, 9.25), colors['accent1'])

draw_arrow(ax, (2, 8.65), (7, 7.95), colors['accent1'])
draw_arrow(ax, (3.7, 8.65), (7, 7.7), colors['accent1'])
draw_arrow(ax, (5.4, 8.65), (7, 7.45), colors['accent1'])

# GPS arrow
draw_arrow(ax, (6.35, 8.65), (6.5, 8.0), colors['warning'])
ax.annotate('', xy=(7, 8.0), xytext=(6.5, 8.0),
            arrowprops=dict(arrowstyle='->', color=colors['warning'], lw=1.5))

# VOTING Section
ax.text(11.5, 10.5, '[VOTACAO]', ha='center', va='center', 
        fontsize=12, color=colors['accent3'], fontweight='bold')

# Voting box
box_vote = FancyBboxPatch((11, 8.5), 1.5, 1.5, 
                           boxstyle="round,pad=0.02,rounding_size=0.1",
                           facecolor=colors['bg_medium'],
                           edgecolor=colors['accent3'],
                           linewidth=2)
ax.add_patch(box_vote)
ax.text(11.75, 9.25, 'Seleção\n\nCompara\ncores', 
        ha='center', va='center', fontsize=9, 
        color=colors['text'], fontweight='bold')

# Arrows to voting
draw_arrow(ax, (9, 9.75), (11, 9.5), colors['accent2'])
draw_arrow(ax, (9, 7.95), (11, 9.0), colors['accent2'])

# OUTPUT Section
ax.text(14, 10.5, '[OUTPUT]', ha='center', va='center', 
        fontsize=12, color=colors['failure'], fontweight='bold')

# Output box
box_out = FancyBboxPatch((13, 7.5), 2.5, 2.5, 
                          boxstyle="round,pad=0.02,rounding_size=0.1",
                          facecolor=colors['bg_medium'],
                          edgecolor=colors['failure'],
                          linewidth=2)
ax.add_patch(box_out)
ax.text(14.25, 9.5, 'FLAGS', ha='center', va='center', 
        fontsize=10, color=colors['text'], fontweight='bold')
ax.text(14.25, 8.8, '0x80000606', ha='center', va='center', 
        fontsize=9, color=colors['failure'])
ax.text(14.25, 8.2, 'posN=1.0 [X]', ha='center', va='center', 
        fontsize=9, color=colors['failure'])
ax.text(14.25, 7.9, 'roll=1.0 [X]', ha='center', va='center', 
        fontsize=9, color=colors['failure'])

# Arrow to output
draw_arrow(ax, (12.5, 9.25), (13, 9), colors['accent3'])

# Failure explanation
ax.text(8, 5.5, '[X] FALHA: Barramento I2C compartilhado', 
        ha='center', va='center', fontsize=11, 
        color=colors['failure'], fontweight='bold')

ax.text(8, 5.0, 'Quando o neutron atinge o barramento I2C,', 
        ha='center', va='center', fontsize=10, color=colors['text'])
ax.text(8, 4.6, 'todos os sensores conectados sao afetados simultaneamente.', 
        ha='center', va='center', fontsize=10, color=colors['text'])
ax.text(8, 4.2, 'CORE 0 e CORE 1 recebem os mesmos dados corrompidos.', 
        ha='center', va='center', fontsize=10, color=colors['text'])
ax.text(8, 3.8, 'A votacao nao detecta falha porque ambos "concordam" no erro.', 
        ha='center', va='center', fontsize=10, color=colors['text'])

# Statistics box
box_stats = FancyBboxPatch((0.5, 0.5), 6, 2.5, 
                            boxstyle="round,pad=0.02,rounding_size=0.1",
                            facecolor=colors['bg_dark'],
                            edgecolor=colors['border'],
                            linewidth=1)
ax.add_patch(box_stats)

ax.text(3.5, 2.7, '[ESTATISTICAS] Estatisticas do Teste', 
        ha='center', va='center', fontsize=11, 
        color=colors['accent1'], fontweight='bold')
ax.text(1, 2.2, '• Taxa de falha: 100%', fontsize=10, color=colors['failure'])
ax.text(1, 1.8, '• Execuções: 61 válidas', fontsize=10, color=colors['text'])
ax.text(1, 1.4, '• Resets: 217 em 18h', fontsize=10, color=colors['text'])
ax.text(1, 1.0, '• Fluência: 1.68×10¹¹ n/cm²', fontsize=10, color=colors['text'])
ax.text(1, 0.6, '• Energia: 14 MeV', fontsize=10, color=colors['text'])

# Vulnerability box
box_vuln = FancyBboxPatch((7, 0.5), 8.5, 2.5, 
                           boxstyle="round,pad=0.02,rounding_size=0.1",
                           facecolor=colors['bg_dark'],
                           edgecolor=colors['border'],
                           linewidth=1)
ax.add_patch(box_vuln)

ax.text(11.25, 2.7, '[!] Vulnerabilidades Identificadas', 
        ha='center', va='center', fontsize=11, 
        color=colors['warning'], fontweight='bold')
ax.text(7.5, 2.2, '• MAG (magnetômetro): 100% de falha', fontsize=10, color=colors['failure'])
ax.text(7.5, 1.8, '• GPS: 83% de falha', fontsize=10, color=colors['failure'])
ax.text(7.5, 1.4, '• IMU: 68% de falha', fontsize=10, color=colors['failure'])
ax.text(7.5, 1.0, '• BARO: 68% de falha', fontsize=10, color=colors['failure'])
ax.text(7.5, 0.6, '• Barramento I2C: ponto único de falha', fontsize=10, color=colors['warning'])

plt.tight_layout()
plt.savefig('/home/csilva/.openclaw/workspace/multirad-diagrams/ekf-system.png', 
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a', edgecolor='none')
print("Diagram saved to: /home/csilva/.openclaw/workspace/multirad-diagrams/ekf-system.png")