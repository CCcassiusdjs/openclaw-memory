#!/usr/bin/env python3
"""
Drone Fall 3D Animation
=======================

Animação 3D simplificada da queda do drone após falha de software.
Usa groundtruth + física de queda livre.

Como não temos a trajetória estimada pelo EKF, assumimos:
- Drone em hover estático antes da falha
- Queda livre após falha
- Sem rotação (atitude desconhecida)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches
import os

# Constantes físicas
G = 9.81  # m/s²
MASS = 1.5  # kg
DRONE_SIZE = 0.3  # metros (tamanho do drone para visualização)

def parse_flags(flags_hex: int) -> dict:
    """Interpreta os flags de status."""
    return {
        'gps_replay_ok': bool(flags_hex & 0x00000010),
        'imu_replay_ok': bool(flags_hex & 0x00000020),
        'baro_replay_ok': bool(flags_hex & 0x00000040),
        'mag_replay_ok': bool(flags_hex & 0x00000080),
        'armed_seen': bool(flags_hex & 0x00000400),
        'run_failed': bool(flags_hex & 0x80000000),
    }

def classify_failure(flags_hex: int) -> str:
    """Classifica o tipo de falha."""
    f = parse_flags(flags_hex)
    
    if not f['run_failed']:
        return 'SUCCESS'
    
    sensors_ok = sum([
        f['gps_replay_ok'],
        f['imu_replay_ok'],
        f['baro_replay_ok'],
        f['mag_replay_ok']
    ])
    
    if f['armed_seen'] and sensors_ok == 0:
        return 'Type A'
    if f['imu_replay_ok'] and f['baro_replay_ok'] and f['mag_replay_ok'] and not f['gps_replay_ok']:
        return 'Type B'
    if f['gps_replay_ok'] and not f['imu_replay_ok']:
        return 'Type C'
    if f['gps_replay_ok'] and f['imu_replay_ok'] and f['baro_replay_ok'] and not f['mag_replay_ok']:
        return 'Type D'
    if f['gps_replay_ok'] and f['baro_replay_ok'] and not f['imu_replay_ok']:
        return 'Type E'
    
    return 'Unknown'

def simulate_fall_3d(initial_height: float, duration: float, dt: float = 0.02):
    """
    Simula a queda do drone em 3D.
    
    Returns:
        Tuple de arrays: (t, x, y, z, vx, vy, vz)
    """
    n_frames = int(duration / dt)
    t = np.linspace(0, duration, n_frames)
    
    # Posição inicial (hover)
    x = np.zeros(n_frames)
    y = np.zeros(n_frames)
    z = np.ones(n_frames) * initial_height
    
    # Velocidade inicial
    vx = np.zeros(n_frames)
    vy = np.zeros(n_frames)
    vz = np.zeros(n_frames)
    
    # Simular queda
    for i in range(1, n_frames):
        # Queda livre (sem arrasto para simplificar)
        vz[i] = vz[i-1] - G * dt
        z[i] = max(0, z[i-1] + vz[i-1] * dt)
        
        # Pequeno deslocamento horizontal (turbulência)
        vx[i] = np.random.normal(0, 0.1)
        vy[i] = np.random.normal(0, 0.1)
        x[i] = x[i-1] + vx[i] * dt
        y[i] = y[i-1] + vy[i] * dt
        
        # Parar no chão
        if z[i] <= 0:
            z[i:] = 0
            vz[i:] = 0
            break
    
    return t, x, y, z, vx, vy, vz

def create_drone_mesh(x, y, z, ax, color='blue'):
    """Desenha um drone simplificado."""
    # Corpo central
    body_size = DRONE_SIZE / 2
    
    # Braços do drone (X shape)
    arm_length = DRONE_SIZE * 0.8
    
    # Desenhar como marcadores
    drone = ax.scatter([x], [y], [z], c=color, s=500, marker='s', 
                        edgecolors='black', linewidth=2, alpha=0.8)
    
    return drone

def create_animation(output_file: str = 'drone_fall_animation.gif'):
    """Cria animação da queda do drone."""
    
    # Parâmetros
    initial_height = 10.0  # metros
    fall_duration = 2.0     # segundos
    hover_duration = 1.0    # segundos
    total_duration = hover_duration + fall_duration
    
    # Simular queda
    t_fall, x_fall, y_fall, z_fall, vx_fall, vy_fall, vz_fall = simulate_fall_3d(
        initial_height, fall_duration, dt=0.02
    )
    
    # Criar figura
    fig = plt.figure(figsize=(14, 10))
    
    # 3D plot
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.set_title('Drone Position (3D)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Height (m)')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_zlim(0, initial_height + 2)
    
    # Height vs time
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_title('Height vs Time', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Height (m)')
    ax2.set_xlim(0, total_duration)
    ax2.set_ylim(0, initial_height + 2)
    ax2.axhline(y=initial_height, color='green', linestyle='--', alpha=0.5, label='Initial')
    ax2.axhline(y=0, color='brown', linestyle='-', alpha=0.5, label='Ground')
    ax2.grid(True, alpha=0.3)
    
    # Velocity vs time
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_title('Vertical Velocity vs Time', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Velocity (m/s)')
    ax3.set_xlim(0, total_duration)
    ax3.set_ylim(-20, 5)
    ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax3.axhline(y=-14.0, color='red', linestyle=':', alpha=0.5, label='Impact velocity')
    ax3.grid(True, alpha=0.3)
    
    # Status
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_title('Status', fontsize=12, fontweight='bold')
    ax4.axis('off')
    
    # Inicializar elementos
    drone, = ax1.plot([], [], [], 's', markersize=20, color='blue', 
                       markeredgecolor='black', markeredgewidth=2)
    trail, = ax1.plot([], [], [], 'r-', alpha=0.3, linewidth=1)
    
    height_line, = ax2.plot([], [], 'b-', linewidth=2, label='Height')
    height_marker, = ax2.plot([], [], 'bo', markersize=8)
    
    velocity_line, = ax3.plot([], [], 'r-', linewidth=2, label='Velocity')
    velocity_marker, = ax3.plot([], [], 'ro', markersize=8)
    
    # Texto de status
    status_text = ax4.text(0.5, 0.5, '', fontsize=14, ha='center', va='center',
                           family='monospace', transform=ax4.transAxes)
    
    def init():
        drone.set_data([], [])
        drone.set_3d_properties([])
        trail.set_data([], [])
        trail.set_3d_properties([])
        height_line.set_data([], [])
        height_marker.set_data([], [])
        velocity_line.set_data([], [])
        velocity_marker.set_data([], [])
        status_text.set_text('')
        return drone, trail, height_line, height_marker, velocity_line, velocity_marker, status_text
    
    def animate(frame):
        dt = 0.02
        t = frame * dt
        
        # Hover phase
        if t < hover_duration:
            x = 0
            y = 0
            z = initial_height
            vz = 0
            phase = 'HOVER'
            color = 'green'
            status = f"Phase: HOVER\nTime: {t:.2f}s\nHeight: {z:.1f}m\nVelocity: 0.0 m/s\nStatus: NOMINAL"
        else:
            # Fall phase
            t_f = t - hover_duration
            idx = min(int(t_f / 0.02), len(x_fall) - 1)
            x = x_fall[idx]
            y = y_fall[idx]
            z = z_fall[idx]
            vz = vz_fall[idx]
            phase = 'FALL'
            color = 'red' if z > 0 else 'gray'
            
            # Calcular velocidade de impacto
            impact_v = abs(vz)
            status = f"Phase: {phase}\nTime: {t:.2f}s\nHeight: {z:.1f}m\nVelocity: {impact_v:.1f} m/s\n"
            
            if z <= 0:
                status += "Status: IMPACT\nDamage: SEVERE"
            else:
                status += "Status: FAILING"
        
        # Atualizar 3D
        drone.set_data([x], [y])
        drone.set_3d_properties([z])
        drone.set_color(color)
        
        # Trail
        if t > hover_duration:
            idx = min(int((t - hover_duration) / 0.02), len(x_fall) - 1)
            trail.set_data(x_fall[:idx+1], y_fall[:idx+1])
            trail.set_3d_properties(z_fall[:idx+1])
        
        # Height plot
        if t < hover_duration:
            height_line.set_data([0, t], [initial_height, initial_height])
            height_marker.set_data([t], [initial_height])
        else:
            t_f = t - hover_duration
            idx = min(int(t_f / 0.02), len(t_fall) - 1)
            height_line.set_data([0] + list(t_fall[:idx+1] + hover_duration), 
                                 [initial_height] + list(z_fall[:idx+1]))
            height_marker.set_data([t], [z])
        
        # Velocity plot
        if t > hover_duration:
            t_f = t - hover_duration
            idx = min(int(t_f / 0.02), len(t_fall) - 1)
            velocity_line.set_data(t_fall[:idx+1] + hover_duration, vz_fall[:idx+1])
            velocity_marker.set_data([t], [vz])
        else:
            velocity_line.set_data([], [])
            velocity_marker.set_data([], [])
        
        # Status
        status_text.set_text(status)
        
        return drone, trail, height_line, height_marker, velocity_line, velocity_marker, status_text
    
    n_frames = int(total_duration / 0.02)
    anim = FuncAnimation(fig, animate, init_func=init, frames=n_frames,
                         interval=20, blit=True)
    
    plt.tight_layout()
    
    # Salvar como GIF
    print(f"Salvando animação: {output_file}")
    anim.save(output_file, writer='pillow', fps=50)
    print("Animação salva!")
    
    # Salvar frame final como PNG
    plt.savefig(output_file.replace('.gif', '.png'), dpi=150, bbox_inches='tight')
    
    return fig

def create_failure_timeline(output_file: str = 'failure_timeline.png'):
    """Cria timeline visual das falhas."""
    
    # Dados das falhas
    results = [
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000516, 'Type C'),
        (0x800005d6, 'Type D'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x800005e6, 'Type B'),
        (0x800005e6, 'Type B'),
        (0x80000606, 'Type A'),
        (0x80000516, 'Type C'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000556, 'Type E'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x800005e6, 'Type B'),
        (0x800005e6, 'Type B'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
        (0x800005d6, 'Type D'),
        (0x80000606, 'Type A'),
        (0x80000606, 'Type A'),
    ]
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Timeline
    ax1 = axes[0]
    ax1.set_title('Failure Timeline', fontsize=14, fontweight='bold')
    
    colors = {
        'Type A': '#FF4444',
        'Type B': '#FF8844',
        'Type C': '#FFFF44',
        'Type D': '#44FF44',
        'Type E': '#4444FF',
    }
    
    for i, (flags, ftype) in enumerate(results):
        ax1.scatter(i, 1, c=colors[ftype], s=100, marker='s', edgecolors='black', linewidth=1)
    
    ax1.set_xlim(-1, len(results) + 1)
    ax1.set_ylim(0.5, 1.5)
    ax1.set_xlabel('Test Run')
    ax1.set_yticks([])
    
    # Legenda
    legend_elements = [mpatches.Patch(facecolor=colors[t], edgecolor='black', label=t) 
                       for t in ['Type A', 'Type B', 'Type C', 'Type D', 'Type E']]
    ax1.legend(handles=legend_elements, loc='upper right')
    
    # Sensor status
    ax2 = axes[1]
    ax2.set_title('Sensor Completion Status', fontsize=14, fontweight='bold')
    
    sensor_names = ['GPS', 'IMU', 'BARO', 'MAG']
    for i, (flags, ftype) in enumerate(results):
        f = parse_flags(flags)
        sensors = [f['gps_replay_ok'], f['imu_replay_ok'], f['baro_replay_ok'], f['mag_replay_ok']]
        for j, s in enumerate(sensors):
            ax2.scatter(i, j, c='green' if s else 'red', s=50, marker='o')
    
    ax2.set_xlim(-1, len(results) + 1)
    ax2.set_ylim(-0.5, 3.5)
    ax2.set_yticks(range(4))
    ax2.set_yticklabels(sensor_names)
    ax2.set_xlabel('Test Run')
    ax2.grid(True, axis='y', alpha=0.3)
    
    # Statistics
    ax3 = axes[2]
    ax3.set_title('Failure Distribution', fontsize=14, fontweight='bold')
    
    from collections import Counter
    counts = Counter([ftype for _, ftype in results])
    
    wedges, texts, autotexts = ax3.pie(
        counts.values(),
        labels=counts.keys(),
        colors=[colors[t] for t in counts.keys()],
        autopct='%1.1f%%',
        startangle=90,
        explode=[0.05] * len(counts)
    )
    ax3.axis('equal')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Salvo: {output_file}")
    
    return fig

def main():
    """Função principal."""
    output_dir = '/home/csilva/.openclaw/workspace/diagrams'
    
    print("=== Criando animação da queda ===")
    create_animation(os.path.join(output_dir, 'drone_fall_animation.gif'))
    
    print("\n=== Criando timeline de falhas ===")
    create_failure_timeline(os.path.join(output_dir, 'failure_timeline.png'))
    
    print("\nConcluído!")

if __name__ == '__main__':
    main()