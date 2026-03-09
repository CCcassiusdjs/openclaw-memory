#!/usr/bin/env python3
"""
Radiation Test Visual Simulation
================================

Simula visualmente o que acontece com o drone durante os testes de radiação,
usando apenas o groundtruth (CSVs) e os flags de resultado.

Groundtruth:
- GPS: Posição fixa (lat=-30.034647, lng=-51.217658, alt=100m)
- Baro: Altitude ~10m
- IMU: Aceleração e giroscópio (drone estacionário)
- PWM: Throttle=1000 (motores desligados/idle)

Flags de falha:
- 0x80000606 → Type A (crash imediato)
- 0x80000516 → Type C (atitude falhou)
- 0x800005d6 → Type D (MAG falhou)
- 0x800005e6 → Type B (GPS falhou)
- 0x80000556 → Type E (parcial)
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass
from typing import List, Tuple
import os

# Constantes físicas
G = 9.81  # m/s²
MASS = 1.5  # kg (drone típico)
AIR_RESISTANCE = 0.05  # coeficiente de arrasto simplificado

@dataclass
class SensorData:
    """Dados de sensores do groundtruth."""
    time_ms: float
    accel: np.ndarray  # [ax, ay, az] m/s²
    gyro: np.ndarray   # [gx, gy, gz] rad/s
    position: np.ndarray  # [lat, lng, alt] (GPS)
    altitude: float  # baro altitude m
    mag: np.ndarray   # [mx, my, mz] mG
    pwm: np.ndarray   # [ch1-ch16]

@dataclass
class TestResult:
    """Resultado de um teste."""
    flags: int
    armed: int
    gps_drops: int
    pos_n: float
    pos_e: float
    pos_d: float
    att_r: float
    att_p: float
    att_y: float

def parse_flags(flags_hex: int) -> dict:
    """Interpreta os flags de status."""
    return {
        'process_ok': bool(flags_hex & 0x00000001),
        'log_parsed': bool(flags_hex & 0x00000002),
        'arducopter_init': bool(flags_hex & 0x00000004),
        'replay_window': bool(flags_hex & 0x00000008),
        'gps_replay_ok': bool(flags_hex & 0x00000010),
        'imu_replay_ok': bool(flags_hex & 0x00000020),
        'baro_replay_ok': bool(flags_hex & 0x00000040),
        'mag_replay_ok': bool(flags_hex & 0x00000080),
        'timing_summary': bool(flags_hex & 0x00000100),
        'no_emu_errors': bool(flags_hex & 0x00000200),
        'armed_seen': bool(flags_hex & 0x00000400),
        'run_failed': bool(flags_hex & 0x80000000),
    }

def classify_failure(flags_hex: int) -> str:
    """
    Classifica o tipo de falha baseado nos flags.
    
    Mapeamento dos tipos A-E:
    - Type A (0x80000606): Nenhum sensor completou, crash imediato
    - Type B (0x800005e6): GPS falhou, IMU+BARO+MAG OK
    - Type C (0x80000516): Apenas GPS completou (atitude falhou)
    - Type D (0x800005d6): GPS+IMU+BARO OK, MAG falhou
    - Type E (0x80000556): GPS+BARO OK, IMU+MAG falharam (parcial)
    """
    f = parse_flags(flags_hex)
    
    if not f['run_failed']:
        return 'SUCCESS'
    
    # Contar quantos sensores completaram
    sensors_ok = sum([
        f['gps_replay_ok'],
        f['imu_replay_ok'],
        f['baro_replay_ok'],
        f['mag_replay_ok']
    ])
    
    # Type A: Armed mas nenhum sensor completou (crash imediato)
    if f['armed_seen'] and sensors_ok == 0:
        return 'Type A (Immediate crash)'
    
    # Type B: IMU+BARO+MAG OK, GPS falhou
    if f['imu_replay_ok'] and f['baro_replay_ok'] and f['mag_replay_ok'] and not f['gps_replay_ok']:
        return 'Type B (GPS failed, others OK)'
    
    # Type C: Apenas GPS completou
    if f['gps_replay_ok'] and not f['imu_replay_ok']:
        return 'Type C (Attitude failure)'
    
    # Type D: GPS+IMU+BARO OK, MAG falhou
    if f['gps_replay_ok'] and f['imu_replay_ok'] and f['baro_replay_ok'] and not f['mag_replay_ok']:
        return 'Type D (Late MAG failure)'
    
    # Type E: GPS+BARO OK, outros falharam (parcial)
    if f['gps_replay_ok'] and f['baro_replay_ok'] and not f['imu_replay_ok']:
        return 'Type E (Partial)'
    
    return f'Unknown (flags=0x{flags_hex:08x}, sensors={sensors_ok})'

def load_groundtruth(data_dir: str) -> Tuple[List[SensorData], float]:
    """Carrega dados do groundtruth dos CSVs."""
    data = []
    duration = 0.0
    
    # Carregar IMU
    imu_data = {}
    with open(os.path.join(data_dir, 'imu.csv'), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = float(row['time_ms'])
            duration = max(duration, t)
            if t not in imu_data:
                imu_data[t] = {}
            imu_data[t]['accel'] = np.array([
                float(row.get('accel_x', 0)),
                float(row.get('accel_y', 0)),
                float(row.get('accel_z', -9.81))
            ])
            imu_data[t]['gyro'] = np.array([
                float(row.get('gyro_x', 0)),
                float(row.get('gyro_y', 0)),
                float(row.get('gyro_z', 0))
            ])
    
    # Carregar GPS
    gps_data = {}
    with open(os.path.join(data_dir, 'gps.csv'), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = float(row['time_ms'])
            gps_data[t] = np.array([
                float(row['lat']) / 1e7,  # Convert from degrees*1e7
                float(row['lng']) / 1e7,
                float(row.get('alt_cm', 10000)) / 100  # Convert to meters
            ])
    
    # Carregar Baro
    baro_data = {}
    with open(os.path.join(data_dir, 'baro.csv'), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = float(row['time_ms'])
            baro_data[t] = float(row['alt_m'])
    
    # Carregar Mag
    mag_data = {}
    with open(os.path.join(data_dir, 'mag.csv'), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = float(row['time_ms'])
            mag_data[t] = np.array([
                float(row['field_x_mG']),
                float(row['field_y_mG']),
                float(row['field_z_mG'])
            ])
    
    # Carregar PWM
    pwm_data = {}
    with open(os.path.join(data_dir, 'pwm.csv'), 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = float(row['time_us']) / 1000.0  # Convert to ms
            pwm_data[t] = np.array([
                float(row.get(f'ch{i}', 1500)) for i in range(1, 17)
            ])
    
    # Combinar dados
    all_times = sorted(set(imu_data.keys()) | set(gps_data.keys()) | 
                       set(baro_data.keys()) | set(mag_data.keys()))
    
    for t in all_times:
        sd = SensorData(
            time_ms=t,
            accel=imu_data.get(t, {}).get('accel', np.array([0, 0, -9.81])),
            gyro=imu_data.get(t, {}).get('gyro', np.array([0, 0, 0])),
            position=gps_data.get(t, np.array([-30.034647, -51.217658, 100.0])),
            altitude=baro_data.get(t, 10.0),
            mag=mag_data.get(t, np.array([200, 0, 400])),
            pwm=pwm_data.get(t, np.array([1500]*16))
        )
        data.append(sd)
    
    return data, duration

def simulate_fall(initial_height: float, duration: float, dt: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simula a queda do drone após falha.
    
    Args:
        initial_height: Altura inicial em metros
        duration: Duração em segundos
        dt: Passo de tempo
    
    Returns:
        Tuple de (tempo, altura, velocidade)
    """
    n_steps = int(duration / dt)
    t = np.linspace(0, duration, n_steps)
    h = np.zeros(n_steps)
    v = np.zeros(n_steps)
    
    h[0] = initial_height
    v[0] = 0.0
    
    for i in range(1, n_steps):
        # Queda livre com arrasto simples
        drag = AIR_RESISTANCE * v[i-1]**2
        a = -G + drag if v[i-1] > 0 else -G - drag
        v[i] = v[i-1] + a * dt
        h[i] = h[i-1] + v[i-1] * dt + 0.5 * a * dt**2
        
        # Parar no chão
        if h[i] <= 0:
            h[i] = 0
            v[i] = 0
            break
    
    return t, h, v

def create_3d_simulation(data_dir: str, output_file: str = 'drone_simulation.png'):
    """Cria visualização 3D da simulação."""
    
    print("Carregando groundtruth...")
    data, duration = load_groundtruth(data_dir)
    print(f"Duração: {duration/1000:.2f}s, {len(data)} amostras")
    
    # Extrair dados de posição
    times = np.array([d.time_ms for d in data])
    positions = np.array([d.position for d in data])
    altitudes = np.array([d.altitude for d in data])
    
    # Posições NED (North-East-Down) relativas
    # Groundtruth é estático, então usamos altitude baro
    initial_height = altitudes[0] if len(altitudes) > 0 else 10.0
    
    # Criar figura
    fig = plt.figure(figsize=(16, 12))
    
    # 3D trajectory
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.set_title('Ground Truth Position (GPS)', fontsize=12, fontweight='bold')
    
    # Posição GPS é fixa, mostrar ponto
    lat, lng, alt = positions[0]
    ax1.scatter([lng], [lat], [alt], c='blue', s=200, marker='^', label='GPS Position')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.set_zlabel('Altitude (m)')
    ax1.legend()
    
    # Altitude over time
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_title('Barometric Altitude vs Time', fontsize=12, fontweight='bold')
    ax2.plot(times/1000, altitudes, 'b-', linewidth=2, label='Baro Altitude')
    ax2.axhline(y=initial_height, color='r', linestyle='--', label=f'Initial: {initial_height:.1f}m')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Altitude (m)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Simulated fall
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_title('Simulated Fall After Failure', fontsize=12, fontweight='bold')
    
    # Simular queda de 10m
    t_fall, h_fall, v_fall = simulate_fall(initial_height, 3.0)
    
    ax3.plot(t_fall, h_fall, 'r-', linewidth=2, label=f'Height (m)')
    ax3.plot(t_fall, v_fall, 'b--', linewidth=2, label=f'Velocity (m/s)')
    ax3.axhline(y=0, color='brown', linestyle=':', label='Ground')
    ax3.axvline(x=np.sqrt(2*initial_height/G), color='orange', linestyle='--', 
                label=f'Impact: {np.sqrt(2*initial_height/G):.2f}s')
    ax3.set_xlabel('Time after failure (s)')
    ax3.set_ylabel('Value')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # IMU data
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_title('IMU Data (Ground Truth)', fontsize=12, fontweight='bold')
    
    accel_x = [d.accel[0] for d in data[:500]]
    accel_y = [d.accel[1] for d in data[:500]]
    accel_z = [d.accel[2] for d in data[:500]]
    t_imu = [d.time_ms/1000 for d in data[:500]]
    
    ax4.plot(t_imu, accel_x, 'r-', alpha=0.7, label='Accel X')
    ax4.plot(t_imu, accel_y, 'g-', alpha=0.7, label='Accel Y')
    ax4.plot(t_imu, accel_z, 'b-', alpha=0.7, label='Accel Z')
    ax4.axhline(y=-9.81, color='k', linestyle='--', alpha=0.5, label='-g')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Acceleration (m/s²)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Salvo: {output_file}")
    
    return fig

def create_failure_visualization(results: List[TestResult], output_file: str = 'failure_analysis.png'):
    """Cria visualização da análise de falhas."""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Classificar falhas
    classifications = [classify_failure(r.flags) for r in results]
    
    # Contar tipos
    from collections import Counter
    counts = Counter(classifications)
    
    # Pie chart
    ax1 = axes[0, 0]
    labels = list(counts.keys())
    sizes = list(counts.values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=90)
    ax1.set_title('Failure Type Distribution', fontsize=12, fontweight='bold')
    
    # Flags heatmap
    ax2 = axes[0, 1]
    flag_names = ['GPS', 'IMU', 'BARO', 'MAG', 'Armed', 'Failed']
    flag_matrix = []
    for r in results:
        f = parse_flags(r.flags)
        flag_matrix.append([
            int(f['gps_replay_ok']),
            int(f['imu_replay_ok']),
            int(f['baro_replay_ok']),
            int(f['mag_replay_ok']),
            int(f['armed_seen']),
            int(f['run_failed'])
        ])
    
    flag_array = np.array(flag_matrix)
    im = ax2.imshow(flag_array.T, aspect='auto', cmap='RdYlGn_r')
    ax2.set_yticks(range(len(flag_names)))
    ax2.set_yticklabels(flag_names)
    ax2.set_xlabel('Test Run')
    ax2.set_title('Status Flags per Run', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=ax2, label='Status (0=Fail, 1=OK)')
    
    # Timeline of failures
    ax3 = axes[1, 0]
    run_ids = range(len(results))
    colors = ['red' if r.flags & 0x80000000 else 'green' for r in results]
    ax3.scatter(run_ids, [r.flags & 0xFFF for r in results], c=colors, alpha=0.7)
    ax3.set_xlabel('Run ID')
    ax3.set_ylabel('Flags (lower 12 bits)')
    ax3.set_title('Failure Timeline', fontsize=12, fontweight='bold')
    ax3.axhline(y=0x606, color='r', linestyle='--', alpha=0.5, label='Type A')
    ax3.axhline(y=0x516, color='orange', linestyle='--', alpha=0.5, label='Type C')
    ax3.legend()
    
    # Impact velocity distribution
    ax4 = axes[1, 1]
    # Assumindo altura de 10m
    initial_height = 10.0
    impact_velocity = np.sqrt(2 * G * initial_height)
    impact_energy = 0.5 * MASS * impact_velocity**2
    
    # Mostrar física do impacto
    heights = np.linspace(1, 50, 50)
    velocities = np.sqrt(2 * G * heights)
    energies = 0.5 * MASS * velocities**2
    
    ax4.plot(heights, velocities, 'b-', linewidth=2, label='Impact Velocity (m/s)')
    ax4.axvline(x=initial_height, color='r', linestyle='--', 
                label=f'Test Height: {initial_height}m')
    ax4.axhline(y=impact_velocity, color='orange', linestyle=':', 
                label=f'Impact: {impact_velocity:.1f} m/s')
    ax4.fill_between([initial_height-0.5, initial_height+0.5], 0, 35, 
                     alpha=0.3, color='red')
    ax4.set_xlabel('Fall Height (m)')
    ax4.set_ylabel('Impact Velocity (m/s)')
    ax4.set_title('Impact Physics', fontsize=12, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Salvo: {output_file}")
    
    return fig

def generate_report(data_dir: str, results: List[TestResult], output_file: str = 'simulation_report.md'):
    """Gera relatório markdown da simulação."""
    
    # Carregar groundtruth
    data, duration = load_groundtruth(data_dir)
    initial_height = data[0].altitude if data else 10.0
    
    # Calcular física
    impact_velocity = np.sqrt(2 * G * initial_height)
    impact_energy = 0.5 * MASS * impact_velocity**2
    fall_time = np.sqrt(2 * initial_height / G)
    
    # Classificar falhas
    classifications = [classify_failure(r.flags) for r in results]
    from collections import Counter
    counts = Counter(classifications)
    
    report = f"""# Radiation Test Simulation Report

## Groundtruth Summary

- **Duration**: {duration/1000:.2f} seconds
- **Samples**: {len(data)} sensor readings
- **Initial Height**: {initial_height:.1f} m
- **Position**: Lat={data[0].position[0]:.6f}, Lng={data[0].position[1]:.6f}
- **IMU Rate**: {len([d for d in data if d.time_ms == 0])} sensors

## Physical Consequences

When the software fails at {initial_height:.1f}m height:

- **Fall Time**: {fall_time:.2f} seconds
- **Impact Velocity**: {impact_velocity:.1f} m/s ({impact_velocity*3.6:.0f} km/h)
- **Impact Energy**: {impact_energy:.1f} J (for {MASS} kg drone)

### Damage Severity

| Height (m) | Velocity (m/s) | Energy (J) | Damage Level |
|------------|----------------|------------|--------------|
| 1          | {np.sqrt(2*G*1):.1f}           | {0.5*MASS*np.sqrt(2*G*1)**2:.1f}        | Light         |
| 5          | {np.sqrt(2*G*5):.1f}           | {0.5*MASS*np.sqrt(2*G*5)**2:.1f}        | Moderate      |
| 10         | {impact_velocity:.1f}           | {impact_energy:.1f}        | Severe        |
| 50         | {np.sqrt(2*G*50):.1f}          | {0.5*MASS*np.sqrt(2*G*50)**2:.1f}       | Destruction   |

## Failure Classification

| Type       | Count | Percentage | Description                           |
|------------|-------|------------|---------------------------------------|
"""
    
    total = len(results)
    for ftype, count in sorted(counts.items()):
        pct = count / total * 100
        desc = {
            'Type A (Immediate crash)': 'Software crash before sensors complete',
            'Type B (GPS failed, others OK)': 'GPS subsystem failure',
            'Type C (GPS only)': 'Attitude system failure',
            'Type D (Late MAG failure)': 'Magnetometer failure near end',
            'Type E (Partial)': 'Multiple partial failures',
            'SUCCESS': 'All systems OK (impossible with radiation)',
        }.get(ftype, 'Unknown failure type')
        report += f"| {ftype:30} | {count:5} | {pct:6.1f}%   | {desc:38} |\n"
    
    report += f"""
## Flags Interpretation

The output vector flags indicate which subsystems completed replay:

| Flag            | Bit  | Meaning                    |
|-----------------|------|----------------------------|
| ProcessOk       | 0    | Process exited normally    |
| LogParsed       | 1    | Runtime log parsed         |
| ArduCopterInit  | 2    | Firmware initialized       |
| ReplayWindow    | 3    | Full replay completed      |
| GPS ReplayOk    | 4    | GPS dataset completed      |
| IMU ReplayOk    | 5    | IMU dataset completed      |
| BARO ReplayOk   | 6    | Barometer completed        |
| MAG ReplayOk    | 7    | Magnetometer completed     |
| ArmedSeen       | 10   | Arming detected            |
| RunFailed       | 31   | Overall failure flag       |

## Visualization

Files generated:
- `drone_simulation.png` - Ground truth and fall simulation
- `failure_analysis.png` - Failure classification and physics

---

*Generated by radiation_test_simulation.py*
"""
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Relatório salvo: {output_file}")
    return report

def main():
    """Função principal."""
    import sys
    
    # Diretório de dados
    data_dir = '/home/csilva/Documents/DATASET_ORCHESTRATOR/case-study_algorithms/drone/arducopter-ekf/data'
    output_dir = '/home/csilva/.openclaw/workspace/diagrams'
    
    # Resultados dos testes (do usuário)
    test_results = [
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000516, armed=1, gps_drops=0, pos_n=0.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x800005d6, armed=1, gps_drops=0, pos_n=0.0, pos_e=1.0, pos_d=0.0, att_r=0.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x800005e6, armed=1, gps_drops=0, pos_n=1.0, pos_e=0.0, pos_d=0.0, att_r=0.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x800005e6, armed=1, gps_drops=0, pos_n=1.0, pos_e=0.0, pos_d=0.0, att_r=0.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000516, armed=1, gps_drops=0, pos_n=0.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000556, armed=1, gps_drops=0, pos_n=0.0, pos_e=1.0, pos_d=0.0, att_r=1.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x800005e6, armed=1, gps_drops=0, pos_n=1.0, pos_e=0.0, pos_d=0.0, att_r=0.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x800005e6, armed=1, gps_drops=0, pos_n=1.0, pos_e=0.0, pos_d=0.0, att_r=0.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x800005d6, armed=1, gps_drops=0, pos_n=0.0, pos_e=1.0, pos_d=0.0, att_r=0.0, att_p=1.0, att_y=1.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
        TestResult(flags=0x80000606, armed=1, gps_drops=0, pos_n=1.0, pos_e=1.0, pos_d=1.0, att_r=1.0, att_p=1.0, att_y=0.0),
    ]
    
    print("=== Radiation Test Simulation ===")
    print(f"Carregando dados de: {data_dir}")
    print(f"Total de resultados: {len(test_results)}")
    print()
    
    # Gerar visualizações
    print("Gerando visualizações...")
    create_3d_simulation(data_dir, os.path.join(output_dir, 'drone_simulation.png'))
    create_failure_visualization(test_results, os.path.join(output_dir, 'failure_analysis.png'))
    
    # Gerar relatório
    print("\nGerando relatório...")
    report = generate_report(data_dir, test_results, os.path.join(output_dir, 'simulation_report.md'))
    
    # Mostrar classificação
    print("\n=== Classificação de Falhas ===")
    from collections import Counter
    classifications = [classify_failure(r.flags) for r in test_results]
    for ftype, count in sorted(Counter(classifications).items()):
        print(f"  {ftype}: {count} ({count/len(test_results)*100:.1f}%)")
    
    print("\n=== Física do Impacto ===")
    initial_height = 10.0
    impact_velocity = np.sqrt(2 * G * initial_height)
    print(f"  Altura: {initial_height:.1f} m")
    print(f"  Tempo de queda: {np.sqrt(2*initial_height/G):.2f} s")
    print(f"  Velocidade de impacto: {impact_velocity:.1f} m/s ({impact_velocity*3.6:.0f} km/h)")
    print(f"  Energia de impacto: {0.5*MASS*impact_velocity**2:.1f} J")

if __name__ == '__main__':
    main()