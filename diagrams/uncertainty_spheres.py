#!/usr/bin/env python3
"""
Visualização das Esferas de Incerteza
=====================================

Mostra onde o drone poderia estar no momento da falha,
baseado em dead reckoning.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d

# Constantes
G = 9.81  # m/s²
MASS = 1.5  # kg
INITIAL_HEIGHT = 10.0  # m

# Tempos de falha estimados
FAILURE_TIMES = {
    'Type A': {'min': 0.0, 'max': 0.5, 'best': 0.25, 'pct': 69.0},
    'Type B': {'min': 5.0, 'max': 10.0, 'best': 7.5, 'pct': 13.8},
    'Type C': {'min': 9.9, 'max': 10.0, 'best': 9.95, 'pct': 6.9},
    'Type D': {'min': 9.9, 'max': 10.0, 'best': 9.95, 'pct': 6.9},
    'Type E': {'min': 9.9, 'max': 10.0, 'best': 9.95, 'pct': 3.4},
}

# Erro de acelerômetro típico (m/s²)
ACCEL_ERROR = 0.01  # Conservador para IMU de qualidade

# Drone em hover: aceleração média é ~0 (não há movimento)
HOVER_ACCEL_ERROR = 0.001  # Muito menor em hover!

def calculate_uncertainty_radius(time_seconds, accel_error=ACCEL_ERROR, is_hover=True):
    """
    Calcula o raio da esfera de incerteza.
    
    Fórmula: raio = 0.5 × a_error × t²
    
    Em hover: a_error é muito menor (drone estático)
    """
    if is_hover:
        # Em hover, a aceleração média é ~0
        # O erro é dominado por ruído, não por movimento
        return accel_error * time_seconds  # Linear em hover
    else:
        # Em movimento, erro cresce com t²
        return 0.5 * accel_error * time_seconds**2

def calculate_fall_trajectory(initial_height, g=G):
    """Calcula a trajetória de queda."""
    t_fall = np.sqrt(2 * initial_height / g)
    v_impact = np.sqrt(2 * g * initial_height)
    return t_fall, v_impact

def create_sphere_visualization():
    """Cria visualização 3D das esferas de incerteza."""
    
    fig = plt.figure(figsize=(16, 12))
    
    # 3D plot
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.set_title('Esferas de Incerteza no Momento da Falha', fontsize=12, fontweight='bold')
    
    # Posição inicial (groundtruth)
    pos_0 = np.array([0, 0, INITIAL_HEIGHT])
    
    # Desenhar drone no início
    ax1.scatter([pos_0[0]], [pos_0[1]], [pos_0[2]], c='blue', s=200, marker='^', 
                label='Posição inicial (groundtruth)')
    
    # Cores para cada tipo
    colors = {
        'Type A': 'red',
        'Type B': 'orange',
        'Type C': 'yellow',
        'Type D': 'green',
        'Type E': 'purple',
    }
    
    # Desenhar esferas
    for i, (type_name, info) in enumerate(FAILURE_TIMES.items()):
        t = info['best']
        r = calculate_uncertainty_radius(t, HOVER_ACCEL_ERROR)
        
        # Posição estimada (mesma do groundtruth em hover)
        pos = pos_0.copy()
        
        # Desenhar esfera
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        x = r * np.outer(np.cos(u), np.sin(v)) + pos[0]
        y = r * np.outer(np.sin(u), np.sin(v)) + pos[1]
        z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + pos[2]
        
        ax1.plot_surface(x, y, z, alpha=0.2, color=colors[type_name])
        ax1.scatter([pos[0]], [pos[1]], [pos[2]], c=colors[type_name], s=100, 
                    label=f'{type_name}: r={r:.2f}m')
    
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.legend(loc='upper left', fontsize=8)
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.set_zlim(0, INITIAL_HEIGHT + 2)
    
    # Gráfico 2: Raio vs Tempo
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_title('Raio da Esfera de Incerteza vs Tempo', fontsize=12, fontweight='bold')
    
    t = np.linspace(0, 10, 100)
    r_hover = calculate_uncertainty_radius(t, HOVER_ACCEL_ERROR, is_hover=True)
    r_moving = calculate_uncertainty_radius(t, ACCEL_ERROR, is_hover=False)
    
    ax2.plot(t, r_hover * 100, 'g-', linewidth=2, label='Hover (a_error=0.001)')
    ax2.plot(t, r_moving * 100, 'r--', linewidth=2, label='Movimento (a_error=0.01)')
    
    # Marcar tempos de falha
    for type_name, info in FAILURE_TIMES.items():
        ax2.axvline(x=info['best'], color='gray', linestyle=':', alpha=0.5)
        ax2.text(info['best'], 0.5, type_name, fontsize=8, rotation=90, va='bottom')
    
    ax2.set_xlabel('Tempo (s)')
    ax2.set_ylabel('Raio (cm)')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0.1, 1000)
    
    # Gráfico 3: Tempo de falha por tipo
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_title('Tempo Estimado de Falha por Tipo', fontsize=12, fontweight='bold')
    
    types = list(FAILURE_TIMES.keys())
    mins = [FAILURE_TIMES[t]['min'] for t in types]
    maxs = [FAILURE_TIMES[t]['max'] for t in types]
    bests = [FAILURE_TIMES[t]['best'] for t in types]
    pcts = [FAILURE_TIMES[t]['pct'] for t in types]
    
    x_pos = np.arange(len(types))
    bar_width = 0.6
    
    # Barras com intervalo de erro
    bars = ax3.bar(x_pos, bests, bar_width, yerr=[[b-m for b, m in zip(bests, mins)],
                                                    [m-b for b, m in zip(bests, maxs)]],
                   color=[colors[t] for t in types], alpha=0.7, capsize=5)
    
    # Adicionar porcentagem
    for i, (bar, pct) in enumerate(zip(bars, pcts)):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
    
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(types)
    ax3.set_ylabel('Tempo (s)')
    ax3.set_xlabel('Tipo de Falha')
    ax3.grid(True, axis='y', alpha=0.3)
    ax3.set_ylim(0, 12)
    
    # Gráfico 4: Esferas 2D (vista de cima)
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_title('Vista de Cima (Posição XY)', fontsize=12, fontweight='bold')
    
    # Posição inicial
    ax4.scatter([0], [0], c='blue', s=200, marker='^', label='Groundtruth')
    
    # Círculos de incerteza
    for type_name, info in FAILURE_TIMES.items():
        t = info['best']
        r = calculate_uncertainty_radius(t, HOVER_ACCEL_ERROR)
        circle = Circle((0, 0), r, fill=False, color=colors[type_name], 
                        linewidth=2, linestyle='--', alpha=0.7)
        ax4.add_patch(circle)
        ax4.text(r + 0.05, 0, f'{type_name}\nr={r:.3f}m', fontsize=8, va='center')
    
    ax4.set_xlim(-0.5, 1.5)
    ax4.set_ylim(-1, 1)
    ax4.set_xlabel('X (m)')
    ax4.set_ylabel('Y (m)')
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig('/home/csilva/.openclaw/workspace/diagrams/uncertainty_spheres.png', 
                dpi=150, bbox_inches='tight')
    print("Salvo: uncertainty_spheres.png")
    
    return fig

def print_summary():
    """Imprime resumo das esferas de incerteza."""
    print("=" * 80)
    print("ESFERAS DE INCERTEZA - RESUMO")
    print("=" * 80)
    print()
    print("Posição inicial conhecida (groundtruth):")
    print(f"  X = 0.0 m (centro)")
    print(f"  Y = 0.0 m (centro)")
    print(f"  Z = {INITIAL_HEIGHT} m (altitude)")
    print()
    print("Em HOVER, a incerteza cresce LINEARMENTE (não quadrática):")
    print("  raio(t) = a_error × t")
    print(f"  onde a_error = {HOVER_ACCEL_ERROR} m/s² (hover)")
    print()
    print("-" * 80)
    print()
    
    for type_name, info in sorted(FAILURE_TIMES.items()):
        t_min = info['min']
        t_max = info['max']
        t_best = info['best']
        r_min = calculate_uncertainty_radius(t_min, HOVER_ACCEL_ERROR)
        r_max = calculate_uncertainty_radius(t_max, HOVER_ACCEL_ERROR)
        r_best = calculate_uncertainty_radius(t_best, HOVER_ACCEL_ERROR)
        
        print(f"{type_name} ({info['pct']:.1f}%):")
        print(f"  Tempo de falha: {t_min:.1f}s - {t_max:.1f}s (melhor: {t_best:.2f}s)")
        print(f"  Raio da esfera: {r_min*100:.2f}cm - {r_max*100:.2f}cm (melhor: {r_best*100:.2f}cm)")
        print(f"  Posição: (0.0 ± {r_best:.3f}, 0.0 ± {r_best:.3f}, {INITIAL_HEIGHT} ± {r_best:.3f})")
        print()
    
    print("=" * 80)
    print("CONCLUSÃO")
    print("=" * 80)
    print()
    print("✅ Para Type A (69%):")
    print("   - Esfera muito pequena: raio ~0.25mm")
    print("   - Posição praticamente no groundtruth")
    print("   - Altura: 10m")
    print()
    print("✅ Para Type B (14%):")
    print("   - Esfera: raio ~0.75cm")
    print("   - Ainda muito precisa")
    print()
    print("✅ Para Type C, D, E (17%):")
    print("   - Esfera: raio ~1cm")
    print("   - Posição muito precisa")
    print()
    print("📍 MOTIVO: Drone em HOVER (aceleração ~0)")
    print("   Em hover, a deriva é MÍNIMA!")
    print()

def main():
    print_summary()
    create_sphere_visualization()
    print("\nVisualização salva em: uncertainty_spheres.png")

if __name__ == '__main__':
    main()