#!/usr/bin/env python3
"""Análise completa e detalhada do log MultiRad"""

import re
from datetime import datetime
from collections import defaultdict

def parse_ts(ts_str):
    parts = ts_str.split('__')
    dt = datetime.strptime(f'{parts[0]} {parts[1]}', '%Y-%m-%d %H:%M:%S')
    us = int(parts[2])
    return dt.timestamp() + us / 1000000.0

started_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i([01])\[(\d+)\] started r(\d+)')
exited_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i([01])\[(\d+)\] exited (?:code=(\d+)|signal=(\w+))')
relay_re = re.compile(r'sut4 has been turned (off|on) via relay')

import sys
log_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/multirad_full.log'

with open(log_file, 'r') as f:
    lines = f.read().strip().split('\n')

# Coletar eventos
pending = {}
runs = []
relay_off = []
relay_on = []

for line in lines:
    # Relay events
    m = relay_re.search(line)
    if m:
        ts = line.split('__')[0] + '__' + line.split('__')[1][:8] + '__' + line.split('__')[1][9:]
        try:
            ts_full = line.split('INFO')[0].strip()
            # Parse timestamp from line
            parts = line.split(' ')
            date_time = parts[0]
            time_part = parts[1]
            ts_str = f"{date_time}__{time_part}"
            dt = datetime.strptime(f'{date_time} {time_part}', '%Y-%m-%d %H:%M:%S')
            ts_val = dt.timestamp()
            if m.group(1) == 'off':
                relay_off.append(ts_val)
            else:
                relay_on.append(ts_val)
        except:
            pass
    
    # Started/exited
    m = started_re.search(line)
    if m:
        ts, inst, pid, run = m.groups()
        pending[(inst, pid)] = (parse_ts(ts), int(run))
        continue
    
    m = exited_re.search(line)
    if m:
        ts, inst, pid, code, signal = m.groups()
        key = (inst, pid)
        if key in pending:
            start_ts, run = pending[key]
            end_ts = parse_ts(ts)
            duration = end_ts - start_ts
            runs.append({
                'run': run,
                'instance': inst,
                'pid': pid,
                'duration': duration,
                'code': int(code) if code else None,
                'signal': signal,
                'start': start_ts,
                'end': end_ts,
                'start_dt': datetime.fromtimestamp(start_ts),
                'end_dt': datetime.fromtimestamp(end_ts)
            })
            del pending[key]

# Filtrar durações válidas (< 3600s)
valid_runs = [r for r in runs if 0 < r['duration'] < 3600]
invalid_runs = [r for r in runs if r['duration'] >= 3600 or r['duration'] <= 0]

# Análise temporal
valid_runs.sort(key=lambda x: x['start'])

# Calcular tempo total de exposição
total_time = sum(r['duration'] for r in valid_runs)

# Análise por dia
by_day = defaultdict(list)
for r in valid_runs:
    day = r['start_dt'].strftime('%Y-%m-%d')
    by_day[day].append(r)

# Análise por hora do dia
by_hour = defaultdict(list)
for r in valid_runs:
    hour = r['start_dt'].hour
    by_hour[hour].append(r)

# Calcular taxa de falha por tempo
success_count = sum(1 for r in valid_runs if r['code'] == 0)
fail_count = sum(1 for r in valid_runs if r['code'] and r['code'] != 0)
segv_count = sum(1 for r in valid_runs if r['signal'] == 'SEGV')

print("=" * 80)
print("MULTIRAD RADIATION TEST - ANÁLISE DETALHADA")
print("=" * 80)
print()

print("=" * 80)
print("1. RESUMO GERAL")
print("=" * 80)
print(f"Linhas no log:                    {len(lines)}")
print(f"Pares started/exited:            {len(runs)}")
print(f"Execuções válidas (<1h):          {len(valid_runs)}")
print(f"Execuções suspeitas (≥1h):       {len(invalid_runs)}")
print(f"Resets da placa (relay):         {len(relay_off)}")
print()

print("=" * 80)
print("2. TEMPO DE EXPOSIÇÃO")
print("=" * 80)
print(f"Tempo total válido:               {total_time:.2f} segundos")
print(f"                                 {total_time/60:.2f} minutos")
print(f"                                 {total_time/3600:.4f} horas")
print(f"Fluência (Φ = 2.6×10⁶ × t):      {2.6e6 * total_time:.4e} n/cm²")
print()

print("=" * 80)
print("3. RESULTADOS DAS EXECUÇÕES")
print("=" * 80)
print(f"Sucesso (code=0):                {success_count} ({100*success_count/len(valid_runs):.1f}%)")
print(f"Falha (code≠0):                  {fail_count} ({100*fail_count/len(valid_runs):.1f}%)")
print(f"SEGV (crash):                    {segv_count} ({100*segv_count/len(valid_runs):.1f}%)")
print()

print("=" * 80)
print("4. ANÁLISE POR DIA")
print("=" * 80)
print(f"{'Dia':<12} {'Execs':>6} {'Sucesso':>8} {'Falha':>8} {'Taxa':>8}")
print("-" * 50)
for day in sorted(by_day.keys()):
    execs = len(by_day[day])
    succ = sum(1 for r in by_day[day] if r['code'] == 0)
    fail = sum(1 for r in by_day[day] if r['code'] and r['code'] != 0)
    rate = 100 * fail / execs if execs > 0 else 0
    print(f"{day:<12} {execs:>6} {succ:>8} {fail:>8} {rate:>7.1f}%")
print()

print("=" * 80)
print("5. DISTRIBUIÇÃO DE DURAÇÕES")
print("=" * 80)
durations = [r['duration'] for r in valid_runs]
durations.sort()

# Quartis
q1 = durations[len(durations)//4]
q2 = durations[len(durations)//2]
q3 = durations[3*len(durations)//4]

print(f"Duração mínima:                  {min(durations):.2f}s ({min(durations)/60:.1f}min)")
print(f"Q1 (25%):                        {q1:.2f}s ({q1/60:.1f}min)")
print(f"Mediana (50%):                   {q2:.2f}s ({q2/60:.1f}min)")
print(f"Q3 (75%):                        {q3:.2f}s ({q3/60:.1f}min)")
print(f"Duração máxima:                  {max(durations):.2f}s ({max(durations)/60:.1f}min)")
print(f"Média:                           {sum(durations)/len(durations):.2f}s ({sum(durations)/len(durations)/60:.1f}min)")
print()

# Faixas de duração
print("Faixas de duração:")
bins = [(0, 10), (10, 60), (60, 300), (300, 600), (600, 1800), (1800, 3600)]
for low, high in bins:
    count = sum(1 for d in durations if low <= d < high)
    print(f"  {low:>5}s - {high:>5}s: {count:>3} execuções ({100*count/len(durations):.1f}%)")
print()

print("=" * 80)
print("6. TAXA DE SEU")
print("=" * 80)
# Assumindo que cada execução falha por causa de SEU
# Taxa = número de falhas / tempo total
seu_rate = fail_count / total_time if total_time > 0 else 0
print(f"SEU observados:                  {fail_count}")
print(f"Tempo de exposição:              {total_time:.2f}s")
print(f"Taxa de SEU:                     {seu_rate:.4f} SEU/s")
print(f"                                {seu_rate*60:.2f} SEU/min")
print(f"                                {seu_rate*3600:.1f} SEU/hora")
print()

# Taxa por fluxo
flux = 2.6e6  # n/cm²/s
if total_time > 0:
    cross_section = fail_count / (flux * total_time)
    print(f"Seção de choque estimada:        {cross_section:.4e} cm²")
    print(f"                                {cross_section*1e9:.2f} × 10⁻⁹ cm²")
    print(f"                                {cross_section*1e10:.2f} × 10⁻¹⁰ cm²")
print()

print("=" * 80)
print("7. ANÁLISE DE RESETS")
print("=" * 80)
print(f"Total de resets (relay off):     {len(relay_off)}")
print(f"Resets por hora:                 {len(relay_off)/(total_time/3600):.1f}")
print(f"MTBF (tempo médio entre falhas): {total_time/fail_count:.1f}s" if fail_count > 0 else "N/A")
print(f"MTBF em minutos:                 {total_time/fail_count/60:.1f}min" if fail_count > 0 else "N/A")
print()

print("=" * 80)
print("8. DADOS NECESSÁRIOS PARA ANÁLISE COMPLETA")
print("=" * 80)
print("""
Faltando para análise completa:

1. LOG COMPLETO COM TODOS OS STARTED/EXITED
   - Verificar se há gaps no log
   - Confirmar timestamps corretos

2. ESPECIFICAÇÃO DOS SENSORES
   - Modelo exato do IMU, GPS, MAG, BARO
   - Área sensível de cada sensor

3. ENERGIA DO FEIXE DE NÊUTRONS
   - Energia em MeV
   - Espectro do feixe

4. TEMPERATURA DURANTE O TESTE
   - Logs de temperatura do SUT
   - Correlação com falhas

5. OUTPUT VECTORS COMPLETOS
   - Todos os flags de todas as execuções
   - Correlação com tipos de falha

6. CHECKERS_RESULTS
   - Resultados dos checksums
   - Detecção de corrupção de memória
""")