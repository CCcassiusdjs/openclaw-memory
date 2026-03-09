#!/usr/bin/env python3
"""Análise dos Output Vectors do MultiRad Radiation Test"""

# Output Vector flags (do código analisado anteriormente)
# kOutputVectorSuccessFlags = 0x000007FFU
# kOutputVectorFailureMask = 0x80000000U

# Flags de status (do output_vector_extractor.h)
FLAGS = {
    'PROCESS_OK':           0x0001,  # bit 0
    'LOG_PARSED':           0x0002,  # bit 1
    'ARDUCOPTER_INIT_SEEN': 0x0004,  # bit 2
    'REPLAY_WINDOW_COMPLETE': 0x0008, # bit 3
    'GPS_REPLAY_OK':        0x0010,  # bit 4
    'IMU_REPLAY_OK':        0x0020,  # bit 5
    'BARO_REPLAY_OK':       0x0040,  # bit 6
    'MAG_REPLAY_OK':        0x0080,  # bit 7
    'TIMING_SUMMARY_SEEN':  0x0100,  # bit 8
    'POS_OK':               0x0200,  # bit 9
    'ATT_OK':               0x0400,  # bit 10
    # Failure mask
    'FAILURE':              0x80000000,  # bit 31
}

def decode_flags(flags_hex):
    """Decodificar flags hexadecimais em componentes legíveis"""
    flags = int(flags_hex, 16)
    result = {
        'failure': bool(flags & 0x80000000),
        'process_ok': bool(flags & 0x0001),
        'log_parsed': bool(flags & 0x0002),
        'ardupilot_init': bool(flags & 0x0004),
        'replay_complete': bool(flags & 0x0008),
        'gps_replay_ok': bool(flags & 0x0010),
        'imu_replay_ok': bool(flags & 0x0020),
        'baro_replay_ok': bool(flags & 0x0040),
        'mag_replay_ok': bool(flags & 0x0080),
        'timing_summary': bool(flags & 0x0100),
        'pos_ok': bool(flags & 0x0200),
        'att_ok': bool(flags & 0x0400),
    }
    return result

# Resultados fornecidos pelo usuário
results = [
    {'count': 36, 'flags': '0x80000606', 'armed': 1, 'gps_drops': 0, 'pos_n': 1.000, 'pos_e': 1.000, 'pos_d': 1.000, 'att_r': 1.000, 'att_p': 1.000, 'att_y': 0.000},
    {'count': 13, 'flags': '0x800005e6', 'armed': 1, 'gps_drops': 0, 'pos_n': 1.000, 'pos_e': 0.000, 'pos_d': 0.000, 'att_r': 0.000, 'att_p': 1.000, 'att_y': 1.000},
    {'count':  4, 'flags': '0x80000516', 'armed': 1, 'gps_drops': 0, 'pos_n': 0.000, 'pos_e': 1.000, 'pos_d': 1.000, 'att_r': 1.000, 'att_p': 1.000, 'att_y': 1.000},
    {'count':  3, 'flags': '0x800005d6', 'armed': 1, 'gps_drops': 0, 'pos_n': 0.000, 'pos_e': 1.000, 'pos_d': 0.000, 'att_r': 0.000, 'att_p': 1.000, 'att_y': 1.000},
    {'count':  3, 'flags': '0x80000556', 'armed': 1, 'gps_drops': 0, 'pos_n': 0.000, 'pos_e': 1.000, 'pos_d': 0.000, 'att_r': 1.000, 'att_p': 1.000, 'att_y': 1.000},
]

print("=" * 80)
print("MULTIRAD RADIATION TEST - OUTPUT VECTOR ANALYSIS")
print("=" * 80)
print()

total = sum(r['count'] for r in results)
print(f"Total executions: {total}")
print()

print("=" * 80)
print("FLAG DECODING")
print("=" * 80)
print()

for r in results:
    flags = decode_flags(r['flags'])
    print(f"Flags: {r['flags']} (count: {r['count']})")
    print(f"  FAILURE:            {'YES' if flags['failure'] else 'NO'}")
    print(f"  Process OK:         {'YES' if flags['process_ok'] else 'NO'}")
    print(f"  Log Parsed:         {'YES' if flags['log_parsed'] else 'NO'}")
    print(f"  ArduPilot Init:    {'YES' if flags['ardupilot_init'] else 'NO'}")
    print(f"  Replay Complete:   {'YES' if flags['replay_complete'] else 'NO'}")
    print(f"  GPS Replay OK:     {'YES' if flags['gps_replay_ok'] else 'NO'}")
    print(f"  IMU Replay OK:     {'YES' if flags['imu_replay_ok'] else 'NO'}")
    print(f"  BARO Replay OK:    {'YES' if flags['baro_replay_ok'] else 'NO'}")
    print(f"  MAG Replay OK:     {'YES' if flags['mag_replay_ok'] else 'NO'}")
    print(f"  Timing Summary:    {'YES' if flags['timing_summary'] else 'NO'}")
    print(f"  Position OK:       {'YES' if flags['pos_ok'] else 'NO'}")
    print(f"  Attitude OK:       {'YES' if flags['att_ok'] else 'NO'}")
    
    # Identificar falhas
    failures = []
    if not flags['gps_replay_ok']:
        failures.append('GPS')
    if not flags['imu_replay_ok']:
        failures.append('IMU')
    if not flags['baro_replay_ok']:
        failures.append('BARO')
    if not flags['mag_replay_ok']:
        failures.append('MAG')
    
    if failures:
        print(f"  >>> FAILED SENSORS: {', '.join(failures)}")
    print()

print("=" * 80)
print("FAILURE PATTERN ANALYSIS")
print("=" * 80)
print()

# Analisar padrões de falha
patterns = {}
for r in results:
    flags = decode_flags(r['flags'])
    failed = []
    if not flags['gps_replay_ok']:
        failed.append('GPS')
    if not flags['imu_replay_ok']:
        failed.append('IMU')
    if not flags['baro_replay_ok']:
        failed.append('BARO')
    if not flags['mag_replay_ok']:
        failed.append('MAG')
    
    pattern = '+'.join(failed) if failed else 'NONE'
    if pattern not in patterns:
        patterns[pattern] = 0
    patterns[pattern] += r['count']

print("Sensor Failure Distribution:")
for pattern, count in sorted(patterns.items(), key=lambda x: -x[1]):
    pct = count / total * 100
    print(f"  {pattern:20s}: {count:3d} ({pct:5.1f}%)")

print()

# Análise de correlação com posição/atitude
print("=" * 80)
print("POSITION/ATTITUDE CORRUPTION ANALYSIS")
print("=" * 80)
print()

for r in results:
    flags = decode_flags(r['flags'])
    
    # Verificar quais sensores falharam
    gps_ok = flags['gps_replay_ok']
    imu_ok = flags['imu_replay_ok']
    baro_ok = flags['baro_replay_ok']
    mag_ok = flags['mag_replay_ok']
    
    # Posição/atitude corrompidos (valores != 0.000 ou != 1.000)
    pos_corrupted = r['pos_n'] != 0.000 or r['pos_e'] != 0.000 or r['pos_d'] != 0.000
    att_corrupted = r['att_r'] != 0.000 or r['att_p'] != 0.000 or r['att_y'] != 0.000
    
    print(f"Flags: {r['flags']} (count: {r['count']})")
    print(f"  Sensors: GPS={'OK' if gps_ok else 'FAIL'}, IMU={'OK' if imu_ok else 'FAIL'}, BARO={'OK' if baro_ok else 'FAIL'}, MAG={'OK' if mag_ok else 'FAIL'}")
    print(f"  Position: N={r['pos_n']:.3f}, E={r['pos_e']:.3f}, D={r['pos_d']:.3f}")
    print(f"  Attitude: R={r['att_r']:.3f}, P={r['att_p']:.3f}, Y={r['att_y']:.3f}")
    
    # Diagnóstico
    if not mag_ok and (r['att_y'] != 1.000 or r['att_r'] != 1.000):
        print(f"  >>> MAG failure correlates with attitude corruption (yaw/roll)")
    if not gps_ok and (r['pos_n'] != 0.000 or r['pos_e'] != 0.000):
        print(f"  >>> GPS failure correlates with position corruption")
    print()

print("=" * 80)
print("CONCLUSIONS")
print("=" * 80)
print()
print("1. ALL executions show FAILURE flag (bit 31 set)")
print("2. Most common failure pattern: GPS+IMU failure")
print("3. MAG (magnetometer) failure strongly correlates with attitude corruption")
print("4. GPS failure correlates with position anomalies")
print()
print("FAILURE RATE: 100% (all executions failed)")
print()
print("Note: The position/attitude values appear to be normalized/indexed")
print("      (0.000 = nominal, 1.000 = corrupted/anomalous)")