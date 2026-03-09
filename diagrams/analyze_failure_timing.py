#!/usr/bin/env python3
"""
Análise de Timing de Falhas
===========================

Com base nos flags de output, inferir QUANDO a falha ocorreu.

Premissas:
- Duração total do dataset: ~10s (golden run)
- GPS: completou em ~9.9s
- IMU: completou em ~10s
- BARO: completou em ~10s
- MAG: completou em ~10s

Se um sensor completou, significa que NÃO falhou antes do fim do dataset.
"""

from dataclasses import dataclass
from typing import List, Tuple

# Dados do usuário (output vectors)
RESULTS = [
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000516, "Type C"),
    (0x800005d6, "Type D"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x800005e6, "Type B"),
    (0x800005e6, "Type B"),
    (0x80000606, "Type A"),
    (0x80000516, "Type C"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000556, "Type E"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x800005e6, "Type B"),
    (0x800005e6, "Type B"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
    (0x800005d6, "Type D"),
    (0x80000606, "Type A"),
    (0x80000606, "Type A"),
]

# Timing do golden run (do log)
GOLDEN_TIMING = {
    'GPS': {'start': 0.0, 'end': 9.9, 'rows': 100},
    'IMU': {'start': 0.0, 'end': 9.997, 'rows': 12000},
    'BARO': {'start': 0.0, 'end': 9.98, 'rows': 1500},
    'MAG': {'start': 0.0, 'end': 9.98, 'rows': 1500},
}

# Timing do ArduCopter
ARDUCOPTER_TIMING = {
    'init': 0.0,       # Boot
    'gyro_init': 2.0,  # Init Gyro***
    'imu_init': 4.0,   # IMU config
    'arm': 0.003,      # Time to arm (from log)
}

def parse_flags(flags: int) -> dict:
    """Interpreta os flags."""
    return {
        'process_ok': bool(flags & 0x00000001),
        'log_parsed': bool(flags & 0x00000002),
        'arducopter_init': bool(flags & 0x00000004),
        'replay_window': bool(flags & 0x00000008),
        'gps_replay_ok': bool(flags & 0x00000010),
        'imu_replay_ok': bool(flags & 0x00000020),
        'baro_replay_ok': bool(flags & 0x00000040),
        'mag_replay_ok': bool(flags & 0x00000080),
        'timing_summary': bool(flags & 0x00000100),
        'no_emu_errors': bool(flags & 0x00000200),
        'armed_seen': bool(flags & 0x00000400),
        'run_failed': bool(flags & 0x80000000),
    }

def infer_failure_time(flags: int) -> dict:
    """
    Infere QUANDO a falha ocorreu baseado nos sensores que completaram.
    
    Lógica:
    - Se sensor completou → falhou DEPOIS do fim do sensor
    - Se sensor NÃO completou → falhou ANTES do fim do sensor
    - Se nenhum completou → falhou MUITO CEDO (init)
    """
    f = parse_flags(flags)
    
    result = {
        'flags': flags,
        'type': 'Unknown',
        'min_time': 0.0,
        'max_time': 10.0,
        'best_estimate': 'Unknown',
        'sensors_completed': [],
        'sensors_failed': [],
        'phase': 'Unknown',
    }
    
    # Determinar sensores que completaram/falharam
    sensors = {
        'GPS': f['gps_replay_ok'],
        'IMU': f['imu_replay_ok'],
        'BARO': f['baro_replay_ok'],
        'MAG': f['mag_replay_ok'],
    }
    
    for sensor, completed in sensors.items():
        if completed:
            result['sensors_completed'].append(sensor)
        else:
            result['sensors_failed'].append(sensor)
    
    # Classificar tipo e estimar tempo
    n_completed = sum(sensors.values())
    
    if f['run_failed']:
        # Determinar fase da falha
        if not f['arducopter_init']:
            result['phase'] = 'Boot (antes de inicializar)'
            result['min_time'] = 0.0
            result['max_time'] = 0.1
            result['best_estimate'] = '< 0.1s'
        elif not f['armed_seen']:
            result['phase'] = 'Init (antes de armar)'
            result['min_time'] = 0.0
            result['max_time'] = ARDUCOPTER_TIMING['gyro_init']
            result['best_estimate'] = '~1-2s'
        elif n_completed == 0:
            # Type A: Nenhum sensor completou
            result['type'] = 'Type A (Immediate crash)'
            result['phase'] = 'Muito cedo (antes de qualquer sensor)'
            result['min_time'] = 0.0
            result['max_time'] = 0.5
            result['best_estimate'] = '< 0.5s'
        elif n_completed == 1 and f['gps_replay_ok']:
            # Type C: Apenas GPS completou
            result['type'] = 'Type C (Attitude failure)'
            result['phase'] = 'Após GPS (~9.9s), antes de IMU/BARO/MAG'
            result['min_time'] = GOLDEN_TIMING['GPS']['end']
            result['max_time'] = GOLDEN_TIMING['IMU']['end']
            result['best_estimate'] = '~9.9s'
        elif n_completed == 3 and sensors['GPS'] and sensors['IMU'] and sensors['BARO']:
            # Type D: GPS+IMU+BARO OK, MAG falhou
            result['type'] = 'Type D (Late MAG failure)'
            result['phase'] = 'Após IMU/BARO (~10s), MAG no final'
            result['min_time'] = GOLDEN_TIMING['IMU']['end']
            result['max_time'] = GOLDEN_TIMING['IMU']['end'] + 0.5
            result['best_estimate'] = '~10s (final)'
        elif n_completed == 2 and sensors['GPS'] and sensors['BARO']:
            # Type E: GPS+BARO OK
            result['type'] = 'Type E (Partial)'
            result['phase'] = 'Após GPS/BARO, antes de IMU/MAG'
            result['min_time'] = GOLDEN_TIMING['GPS']['end']
            result['max_time'] = GOLDEN_TIMING['IMU']['end']
            result['best_estimate'] = '~10s'
        elif n_completed == 3 and sensors['IMU'] and sensors['BARO'] and sensors['MAG']:
            # Type B: GPS falhou, outros OK
            result['type'] = 'Type B (GPS failure)'
            result['phase'] = 'GPS falhou durante (~9.9s)'
            result['min_time'] = 0.0
            result['max_time'] = GOLDEN_TIMING['GPS']['end']
            result['best_estimate'] = '~5-10s'
        else:
            result['type'] = 'Unknown'
            result['phase'] = 'Indeterminado'
            result['best_estimate'] = 'Unknown'
    else:
        result['type'] = 'SUCCESS'
        result['phase'] = 'Não houve falha'
        result['min_time'] = GOLDEN_TIMING['IMU']['end']
        result['max_time'] = GOLDEN_TIMING['IMU']['end']
        result['best_estimate'] = '10s (completo)'
    
    return result

def analyze_all_runs():
    """Analisa todas as execuções."""
    print("=" * 80)
    print("ANÁLISE DE TIMING DE FALHAS")
    print("=" * 80)
    print()
    
    # Agrupar por tipo
    by_type = {}
    
    for flags, type_label in RESULTS:
        if type_label not in by_type:
            by_type[type_label] = []
        by_type[type_label].append((flags, infer_failure_time(flags)))
    
    # Mostrar cada tipo
    for type_label in sorted(by_type.keys()):
        runs = by_type[type_label]
        print(f"\n{type_label}")
        print("-" * 40)
        print(f"Ocorrências: {len(runs)}")
        
        # Mostrar alguns exemplos
        for i, (flags, info) in enumerate(runs[:3]):
            print(f"\n  Run {i+1}:")
            print(f"    Sensores completados: {', '.join(info['sensors_completed']) or 'Nenhum'}")
            print(f"    Sensores falharam: {', '.join(info['sensors_failed']) or 'Nenhum'}")
            print(f"    Fase: {info['phase']}")
            print(f"    Tempo estimado: {info['best_estimate']}")
            print(f"    Intervalo: [{info['min_time']:.1f}s, {info['max_time']:.1f}s]")
    
    # Resumo
    print("\n" + "=" * 80)
    print("RESUMO")
    print("=" * 80)
    
    # Calcular tempos
    all_times = []
    for flags, type_label in RESULTS:
        info = infer_failure_time(flags)
        all_times.append((type_label, info['best_estimate'], info['min_time'], info['max_time']))
    
    # Contar por tipo
    from collections import Counter
    type_counts = Counter([t for t, _, _, _ in all_times])
    
    print("\nDistribuição de falhas:")
    for type_label, count in sorted(type_counts.items()):
        pct = count / len(all_times) * 100
        print(f"  {type_label}: {count} ({pct:.1f}%)")
    
    # Estatísticas de tempo
    print("\nEstimativa de tempo de falha:")
    print(f"  Mais rápida: < 0.5s (Type A - crash imediato)")
    print(f"  Mais lenta:  ~10s (Type D - MAG no final)")
    
    # Dead reckoning
    print("\n" + "=" * 80)
    print("ESFERA DE INCERTEZA (Dead Reckoning)")
    print("=" * 80)
    
    print("""
Para Type A (crash imediato):
  - Tempo: < 0.5s
  - Posição inicial: groundtruth (±0.1m)
  - Movimento: quase nenhum (drone ainda em hover)
  - Esfera de incerteza: raio ~0.5m (deriva por 0.5s)

Para Type B (GPS falhou):
  - Tempo: ~5-10s
  - Posição inicial: groundtruth
  - Movimento: hover por ~5-10s
  - Esfera de incerteza: raio ~5-10m (deriva por 5-10s sem GPS)

Para Type C (atitude falhou):
  - Tempo: ~9.9s
  - Posição inicial: groundtruth
  - GPS completou → posição ainda OK
  - Esfera de incerteza: raio ~0.5m (GPS manteve posição)

Para Type D (MAG falhou no final):
  - Tempo: ~10s
  - Posição inicial: groundtruth
  - GPS+IMU+BARO completaram → posição OK
  - Esfera de incerteza: raio ~0.5m

Para Type E (parcial):
  - Tempo: ~10s
  - Posição inicial: groundtruth
  - GPS+BARO OK → altitude OK
  - Esfera de incerteza: raio ~2-5m (sem IMU para atitude)
""")
    
    # Fórmula da esfera
    print("\nFórmula da esfera de incerteza:")
    print("  raio(t) = 0.5 × a_error × t²")
    print("  onde a_error ≈ 0.01 m/s² (erro típico de acelerômetro)")
    print()
    print("  Após 0.5s: raio ≈ 0.001m")
    print("  Após 5s:   raio ≈ 0.125m")
    print("  Após 10s:  raio ≈ 0.5m")
    print()
    print("  NOTA: Esferas MENORES que isso porque o drone está em HOVER!")
    print("  Em hover, a aceleração média é ~0, então deriva é menor.")

def main():
    analyze_all_runs()

if __name__ == '__main__':
    main()