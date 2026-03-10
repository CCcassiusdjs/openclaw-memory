#!/usr/bin/env python3
"""Generate accurate EKF system diagram based on ArduPilot source code"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Setup
fig, ax = plt.subplots(1, 1, figsize=(18, 14), facecolor='#0a0a1a')
ax.set_xlim(0, 18)
ax.set_ylim(0, 14)
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
    'code': '#00d4aa',
}

# Title
ax.text(9, 13.5, 'ArduPilot EKF3 - Arquitetura de Cores', 
        ha='center', va='center', fontsize=18, 
        color=colors['text'], fontweight='bold')

ax.text(9, 13.0, 'Baseado no codigo fonte: AP_NavEKF3.cpp', 
        ha='center', va='center', fontsize=10, 
        color=colors['accent1'])

# ============== INPUT SECTION ==============
def draw_sensor_box(ax, x, y, w, h, label, sublabel, color):
    box = FancyBboxPatch((x, y), w, h, 
                          boxstyle="round,pad=0.02,rounding_size=0.05",
                          facecolor=color['bg_light'],
                          edgecolor=color['accent1'],
                          linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h*0.65, label, 
            ha='center', va='center', 
            fontsize=9, color=color['text'],
            fontweight='bold')
    ax.text(x + w/2, y + h*0.3, sublabel, 
            ha='center', va='center', 
            fontsize=8, color=color['accent1'])

# Input section background
input_bg = FancyBboxPatch((0.3, 9.5), 4.4, 3, 
                           boxstyle="round,pad=0.02,rounding_size=0.1",
                           facecolor=colors['bg_medium'],
                           edgecolor=colors['border'],
                           linewidth=1)
ax.add_patch(input_bg)
ax.text(2.5, 12.2, '[INPUT] Sensores', ha='center', va='center', 
        fontsize=11, color=colors['accent1'], fontweight='bold')

# IMU sensors
draw_sensor_box(ax, 0.5, 11.3, 1.2, 0.6, 'IMU 0', '400 Hz', colors)
draw_sensor_box(ax, 1.8, 11.3, 1.2, 0.6, 'IMU 1', '400 Hz', colors)
draw_sensor_box(ax, 3.1, 11.3, 1.2, 0.6, 'IMU 2', '400 Hz', colors)

# Other sensors
draw_sensor_box(ax, 0.5, 10.5, 1.2, 0.6, 'MAG 0', '50 Hz', colors)
draw_sensor_box(ax, 1.8, 10.5, 1.2, 0.6, 'MAG 1', '50 Hz', colors)
draw_sensor_box(ax, 3.1, 10.5, 1.2, 0.6, 'MAG 2', '50 Hz', colors)

draw_sensor_box(ax, 0.5, 9.7, 1.2, 0.6, 'BARO 0', '50 Hz', colors)
draw_sensor_box(ax, 1.8, 9.7, 1.2, 0.6, 'BARO 1', '50 Hz', colors)
draw_sensor_box(ax, 3.1, 9.7, 1.2, 0.6, 'BARO 2', '50 Hz', colors)

# GPS shared
gps_box = FancyBboxPatch((4.0, 10.3), 0.6, 0.8, 
                           boxstyle="round,pad=0.02,rounding_size=0.05",
                           facecolor='#1a3a1a',
                           edgecolor=colors['success'],
                           linewidth=1.5)
ax.add_patch(gps_box)
ax.text(4.3, 10.9, 'GPS', ha='center', va='center', 
        fontsize=8, color=colors['text'], fontweight='bold')
ax.text(4.3, 10.5, '10 Hz', ha='center', va='center', 
        fontsize=7, color=colors['success'])

# ============== EKF CORES SECTION ==============
ekf_bg = FancyBboxPatch((5, 6), 6, 6.5, 
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor=colors['bg_medium'],
                         edgecolor=colors['accent2'],
                         linewidth=2)
ax.add_patch(ekf_bg)
ax.text(8, 12.2, '[EKF CORES] NavEKF3_core', ha='center', va='center', 
        fontsize=11, color=colors['accent2'], fontweight='bold')

# Core 0
core0_box = FancyBboxPatch((5.3, 9.5), 2.5, 2.3, 
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor='#1a2a1a',
                             edgecolor=colors['success'],
                             linewidth=2)
ax.add_patch(core0_box)
ax.text(6.55, 11.5, 'CORE 0 (Primary)', ha='center', va='center', 
        fontsize=10, color=colors['success'], fontweight='bold')
ax.text(6.55, 11.1, 'NavEKF3_core[0]', ha='center', va='center', 
        fontsize=8, color=colors['text'])
ax.text(6.55, 10.6, 'IMU: imu_index[0]', ha='center', va='center', 
        fontsize=8, color=colors['accent1'])
ax.text(6.55, 10.2, 'MAG: use_compass[0]', ha='center', va='center', 
        fontsize=8, color=colors['accent1'])
ax.text(6.55, 9.8, 'BARO: baro_index[0]', ha='center', va='center', 
        fontsize=8, color=colors['accent1'])

# Core 1
core1_box = FancyBboxPatch((5.3, 6.3), 2.5, 2.8, 
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor=colors['bg_dark'],
                             edgecolor=colors['border'],
                             linewidth=1.5)
ax.add_patch(core1_box)
ax.text(6.55, 8.8, 'CORE 1 (Backup)', ha='center', va='center', 
        fontsize=10, color=colors['text'], fontweight='bold')
ax.text(6.55, 8.4, 'NavEKF3_core[1]', ha='center', va='center', 
        fontsize=8, color=colors['text'])
ax.text(6.55, 7.9, 'IMU: imu_index[1]', ha='center', va='center', 
        fontsize=8, color=colors['accent1'])
ax.text(6.55, 7.5, 'MAG: use_compass[1]', ha='center', va='center', 
        fontsize=8, color=colors['accent1'])
ax.text(6.55, 7.1, 'BARO: baro_index[1]', ha='center', va='center', 
        fontsize=8, color=colors['accent1'])
ax.text(6.55, 6.6, 'errorScore: calculado', ha='center', va='center', 
        fontsize=7, color=colors['warning'])

# Core status
ax.text(8.3, 11.5, 'Estrutura interna:', ha='left', va='center', 
        fontsize=9, color=colors['text'], fontweight='bold')
ax.text(8.3, 11.1, 'stateStruct (24 estados)', ha='left', va='center', 
        fontsize=8, color=colors['code'])
ax.text(8.3, 10.7, '  - posN, posE, posD', ha='left', va='center', 
        fontsize=7, color=colors['text'])
ax.text(8.3, 10.4, '  - velN, velE, velD', ha='left', va='center', 
        fontsize=7, color=colors['text'])
ax.text(8.3, 10.1, '  - quaternion (attitude)', ha='left', va='center', 
        fontsize=7, color=colors['text'])
ax.text(8.3, 9.8, '  - gyro_bias, accel_bias', ha='left', va='center', 
        fontsize=7, color=colors['text'])
ax.text(8.3, 9.5, '  - wind, mag_bias, ...', ha='left', va='center', 
        fontsize=7, color=colors['text'])

ax.text(8.3, 9.0, 'Test Ratios:', ha='left', va='center', 
        fontsize=9, color=colors['text'], fontweight='bold')
ax.text(8.3, 8.6, 'velTestRatio = GPS velocity', ha='left', va='center', 
        fontsize=7, color=colors['code'])
ax.text(8.3, 8.3, 'posTestRatio = GPS position', ha='left', va='center', 
        fontsize=7, color=colors['code'])
ax.text(8.3, 8.0, 'hgtTestRatio = Baro height', ha='left', va='center', 
        fontsize=7, color=colors['code'])
ax.text(8.3, 7.7, 'magTestRatio = Magnetometer', ha='left', va='center', 
        fontsize=7, color=colors['code'])

# Arrows from sensors to cores
ax.annotate('', xy=(5.3, 10.5), xytext=(4.7, 11.6),
            arrowprops=dict(arrowstyle='->', color=colors['accent1'], lw=1.5))
ax.annotate('', xy=(5.3, 7.5), xytext=(4.7, 10.8),
            arrowprops=dict(arrowstyle='->', color=colors['accent1'], lw=1.5))
ax.annotate('', xy=(5.3, 10.0), xytext=(4.3, 11.0),
            arrowprops=dict(arrowstyle='->', color=colors['success'], lw=1.5))
ax.annotate('', xy=(5.3, 7.0), xytext=(4.3, 10.5),
            arrowprops=dict(arrowstyle='->', color=colors['success'], lw=1.5))

# ============== CORE SELECTION SECTION ==============
select_bg = FancyBboxPatch((11.5, 9.5), 3.5, 3, 
                            boxstyle="round,pad=0.02,rounding_size=0.1",
                            facecolor=colors['bg_medium'],
                            edgecolor=colors['accent3'],
                            linewidth=2)
ax.add_patch(select_bg)
ax.text(13.25, 12.2, '[SELECAO] Core Primario', ha='center', va='center', 
        fontsize=10, color=colors['accent3'], fontweight='bold')

ax.text(11.7, 11.6, 'updateCoreErrorScores()', ha='left', va='center', 
        fontsize=8, color=colors['code'], fontweight='bold')
ax.text(11.7, 11.2, 'for each core:', ha='left', va='center', 
        fontsize=7, color=colors['text'])
ax.text(11.7, 10.9, '  errorScore[i] =', ha='left', va='center', 
        fontsize=7, color=colors['text'])
ax.text(11.7, 10.6, '    MAX(velTestRatio,', ha='left', va='center', 
        fontsize=7, color=colors['code'])
ax.text(11.7, 10.3, '        posTestRatio,', ha='left', va='center', 
        fontsize=7, color=colors['code'])
ax.text(11.7, 10.0, '        hgtTestRatio)', ha='left', va='center', 
        fontsize=7, color=colors['code'])

ax.text(11.7, 9.7, 'Menor score = primary', ha='left', va='center', 
        fontsize=8, color=colors['success'])

# ============== OUTPUT SECTION ==============
output_bg = FancyBboxPatch((11.5, 6.5), 3.5, 2.8, 
                            boxstyle="round,pad=0.02,rounding_size=0.1",
                            facecolor=colors['bg_medium'],
                            edgecolor=colors['warning'],
                            linewidth=1.5)
ax.add_patch(output_bg)
ax.text(13.25, 9.0, '[OUTPUT] getPrimaryCoreIndex()', ha='center', va='center', 
        fontsize=10, color=colors['warning'], fontweight='bold')

ax.text(11.7, 8.5, 'Retorna dados do core primario:', ha='left', va='center', 
        fontsize=8, color=colors['text'])
ax.text(11.7, 8.1, 'getPosNE() -> posN, posE', ha='left', va='center', 
        fontsize=8, color=colors['code'])
ax.text(11.7, 7.7, 'getPosD() -> posD', ha='left', va='center', 
        fontsize=8, color=colors['code'])
ax.text(11.7, 7.3, 'getEulerAngles() -> r,p,y', ha='left', va='center', 
        fontsize=8, color=colors['code'])
ax.text(11.7, 6.9, 'getVelNED() -> velN,E,D', ha='left', va='center', 
        fontsize=8, color=colors['code'])

# ============== ERROR SCORE CALCULATION ==============
error_bg = FancyBboxPatch((0.5, 5), 4.3, 4, 
                           boxstyle="round,pad=0.02,rounding_size=0.1",
                           facecolor=colors['bg_dark'],
                           edgecolor=colors['border'],
                           linewidth=1)
ax.add_patch(error_bg)
ax.text(2.65, 8.7, 'errorScore() - Codigo Real', ha='center', va='center', 
        fontsize=10, color=colors['code'], fontweight='bold')

code_lines = [
    'float NavEKF3_core::errorScore()',
    '{',
    '    float score = 0.0f;',
    '    if (tiltAlignComplete && yawAlignComplete) {',
    '        // GPS velocity + position',
    '        score = MAX(score,',
    '            0.5f * (velTestRatio + posTestRatio));',
    '        // Barometer height',
    '        score = MAX(score, hgtTestRatio);',
    '        // Magnetometer (if affinity)',
    '        if (affinity & EKF_AFFINITY_MAG) {',
    '            score = MAX(score,',
    '                0.3f * magTestRatio);',
    '        }',
    '    }',
    '    return score;',
    '}',
]

y_pos = 8.3
for i, line in enumerate(code_lines):
    ax.text(0.7, y_pos - i*0.25, line, ha='left', va='center', 
            fontsize=6.5, color=colors['code'] if i > 0 else colors['accent1'],
            family='monospace')

# ============== FAILURE ANALYSIS ==============
failure_bg = FancyBboxPatch((0.5, 0.5), 8, 4, 
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor='#1a0a0a',
                             edgecolor=colors['failure'],
                             linewidth=2)
ax.add_patch(failure_bg)
ax.text(4.5, 4.2, '[X] Falha sob Radiacao - Analise', ha='center', va='center', 
        fontsize=11, color=colors['failure'], fontweight='bold')

ax.text(0.7, 3.7, 'Quando todos os sensores falham:', ha='left', va='center', 
        fontsize=9, color=colors['text'], fontweight='bold')
ax.text(0.7, 3.3, '1. velTestRatio -> infinito (GPS falhou)', ha='left', va='center', 
        fontsize=8, color=colors['failure'])
ax.text(0.7, 2.9, '2. posTestRatio -> infinito (GPS falhou)', ha='left', va='center', 
        fontsize=8, color=colors['failure'])
ax.text(0.7, 2.5, '3. hgtTestRatio -> infinito (BARO falhou)', ha='left', va='center', 
        fontsize=8, color=colors['failure'])
ax.text(0.7, 2.1, '4. magTestRatio -> infinito (MAG falhou)', ha='left', va='center', 
        fontsize=8, color=colors['failure'])

ax.text(0.7, 1.6, 'Resultados:', ha='left', va='center', 
        fontsize=9, color=colors['text'], fontweight='bold')
ax.text(0.7, 1.2, 'CORE 0: errorScore = MAX(inf, inf, inf) = inf', ha='left', va='center', 
        fontsize=8, color=colors['warning'])
ax.text(0.7, 0.8, 'CORE 1: errorScore = MAX(inf, inf, inf) = inf', ha='left', va='center', 
        fontsize=8, color=colors['warning'])
ax.text(0.7, 0.4, 'Ambos os cores com score infinito -> selecao falha!', ha='left', va='center', 
        fontsize=8, color=colors['failure'], fontweight='bold')

# ============== STATISTICS ==============
stats_bg = FancyBboxPatch((9, 0.5), 6, 4, 
                           boxstyle="round,pad=0.02,rounding_size=0.1",
                           facecolor=colors['bg_dark'],
                           edgecolor=colors['border'],
                           linewidth=1)
ax.add_patch(stats_bg)
ax.text(12, 4.2, '[ESTATISTICAS] Teste de Radiacao', ha='center', va='center', 
        fontsize=11, color=colors['accent1'], fontweight='bold')

ax.text(9.2, 3.7, 'Configuracao:', ha='left', va='center', 
        fontsize=9, color=colors['text'], fontweight='bold')
ax.text(9.2, 3.3, 'EKF3 cores: 2 (padrao)', ha='left', va='center', 
        fontsize=8, color=colors['text'])
ax.text(9.2, 2.9, 'IMU_MASK: 3 (bits 0,1)', ha='left', va='center', 
        fontsize=8, color=colors['text'])
ax.text(9.2, 2.5, 'Sensores: 3 IMU, 3 BARO, 3 MAG', ha='left', va='center', 
        fontsize=8, color=colors['text'])

ax.text(9.2, 2.0, 'Resultados:', ha='left', va='center', 
        fontsize=9, color=colors['text'], fontweight='bold')
ax.text(9.2, 1.6, 'Taxa de falha: 100% (61/61)', ha='left', va='center', 
        fontsize=8, color=colors['failure'])
ax.text(9.2, 1.2, 'Resets da placa: 217', ha='left', va='center', 
        fontsize=8, color=colors['warning'])
ax.text(9.2, 0.8, 'Fluencia: 1.68e11 n/cm2', ha='left', va='center', 
        fontsize=8, color=colors['text'])
ax.text(9.2, 0.4, 'Dose: 1.14 Gy (14 MeV)', ha='left', va='center', 
        fontsize=8, color=colors['text'])

plt.tight_layout()
plt.savefig('/home/csilva/.openclaw/workspace/multirad-diagrams/ekf-system-accurate.png', 
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a', edgecolor='none')
print("Diagram saved to: /home/csilva/.openclaw/workspace/multirad-diagrams/ekf-system-accurate.png")