#!/usr/bin/env python3
"""Análise do log MultiRad - apenas durações válidas (< 1 hora)"""

import re
from datetime import datetime

def parse_ts(ts_str):
    parts = ts_str.split('__')
    dt = datetime.strptime(f'{parts[0]} {parts[1]}', '%Y-%m-%d %H:%M:%S')
    us = int(parts[2])
    return dt.timestamp() + us / 1000000.0

started_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i([01])\[(\d+)\] started r(\d+)')
exited_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i([01])\[(\d+)\] exited (?:code=(\d+)|signal=(\w+))')

import sys
log_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/multirad_full.log'

with open(log_file, 'r') as f:
    lines = f.read().strip().split('\n')

pending = {}
runs = []

for line in lines:
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
            status = f"code={code}" if code else f"signal={signal}"
            runs.append({
                'run': run,
                'instance': inst,
                'pid': pid,
                'duration': duration,
                'status': status,
                'code': int(code) if code else None,
                'signal': signal,
                'start': start_ts,
                'end': end_ts,
                'start_dt': datetime.fromtimestamp(start_ts),
                'end_dt': datetime.fromtimestamp(end_ts)
            })
            del pending[key]

# Filtrar durações válidas: > 0 e < 3600 segundos (1 hora)
# Isso exclui execuções com timestamps incorretos
MAX_DURATION = 3600  # 1 hora
valid_runs = [r for r in runs if 0 < r['duration'] < MAX_DURATION]
invalid_runs = [r for r in runs if r['duration'] >= MAX_DURATION or r['duration'] <= 0]

total_duration = sum(r['duration'] for r in valid_runs)
success = sum(1 for r in valid_runs if r['code'] == 0)
fail = sum(1 for r in valid_runs if r['code'] and r['code'] != 0)
segv = sum(1 for r in valid_runs if r['signal'] == 'SEGV')

print("=" * 80)
print("MULTIRAD RADIATION TEST - ANÁLISE (durações < 1h)")
print("=" * 80)
print()
print(f"Linhas processadas:                 {len(lines)}")
print(f"Pares started/exited encontrados:   {len(runs)}")
print(f"Execuções com duração válida (<1h): {len(valid_runs)}")
print(f"Execuções com duração inválida:     {len(invalid_runs)}")
print(f"Sucesso (code=0):                   {success}")
print(f"Falha (code!=0):                    {fail}")
print(f"SEGV:                               {segv}")
print()

if invalid_runs:
    print("=" * 80)
    print("EXECUÇÕES COM DURAÇÃO SUSPEITA (ignoradas)")
    print("=" * 80)
    for r in invalid_runs:
        print(f"Run {r['run']:3d} [i{r['instance']}] [pid {r['pid']:>5}]: {r['duration']/3600:.2f}h")
    print()

print("=" * 80)
print("TEMPOS DE EXECUÇÃO VÁLIDOS")
print("=" * 80)
print(f"{'Run':>4} {'Inst':>4} {'PID':>6} {'Duração':>12} {'Status':<15}")
print("-" * 80)
for r in sorted(valid_runs, key=lambda x: (x['run'], x['instance'])):
    dur_min = r['duration'] / 60
    print(f"{r['run']:>4} {r['instance']:>4} {r['pid']:>6} {r['duration']:>8.2f}s ({dur_min:>5.1f}min) {r['status']:<15}")

print()
print("=" * 80)
print("CÁLCULO DE FLUÊNCIA")
print("=" * 80)
print()
print(f"Tempo total de execução: {total_duration:.2f} segundos")
print(f"                         {total_duration/60:.2f} minutos")
print(f"                         {total_duration/3600:.4f} horas")
print()
print(f"Fluxo de nêutrons:       2.6 × 10⁶ n/cm²/s")
print(f"FLUÊNCIA TOTAL:          {2.6e6 * total_duration:.4e} n/cm²")
print()

if valid_runs:
    durations = [r['duration'] for r in valid_runs]
    print("=" * 80)
    print("ESTATÍSTICAS")
    print("=" * 80)
    print(f"Duração mínima: {min(durations):.2f}s ({min(durations)/60:.1f}min)")
    print(f"Duração máxima: {max(durations):.2f}s ({max(durations)/60:.1f}min)")
    print(f"Duração média:  {sum(durations)/len(durations):.2f}s ({sum(durations)/len(durations)/60:.1f}min)")
    print(f"Duração mediana: {sorted(durations)[len(durations)//2]:.2f}s ({sorted(durations)[len(durations)//2]/60:.1f}min)")