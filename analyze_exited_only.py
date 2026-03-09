#!/usr/bin/env python3
"""Calcular tempo total baseado nos EXITED events do log completo"""

import re
from datetime import datetime

# Log completo fornecido pelo usuário - extraindo apenas EXITED
log_exited = """
2026-02-25__09:03:10__625505 INFO: i1[627] exited code=2
2026-02-25__09:08:18__365856 INFO: i0[10032] exited code=0
2026-02-25__09:14:14__122378 INFO: i0[626] exited code=2
2026-02-25__09:18:11__499926 INFO: i1[3727] exited code=2
2026-02-25__09:23:16__623202 INFO: i0[8796] exited code=0
2026-02-25__09:32:53__205938 INFO: i1[622] exited code=2
2026-02-25__09:33:08__696702 INFO: i0[1611] exited code=2
2026-02-25__09:59:55__303248 INFO: i1[623] exited code=0
2026-02-25__10:11:25__633038 INFO: i0[620] exited code=0
2026-02-25__10:19:08__360520 INFO: i1[623] exited code=2
2026-02-25__10:36:34__824930 INFO: i0[625] exited code=2
2026-02-25__10:47:13__276060 INFO: i0[622] exited code=2
2026-02-25__10:51:14__116880 INFO: i1[2224] exited code=2
2026-02-25__11:15:32__943206 INFO: i1[626] exited code=2
2026-02-25__11:21:30__433380 INFO: i1[627] exited code=2
2026-02-25__11:26:33__799604 INFO: i0[1749] exited code=0
2026-02-25__11:34:01__847169 INFO: i0[622] exited code=2
2026-02-25__11:34:16__723776 INFO: i1[8789] exited code=2
2026-02-25__11:44:44__215108 INFO: i1[621] exited code=0
2026-02-25__11:56:26__536794 INFO: i1[623] exited code=0
2026-02-25__12:19:40__311344 INFO: i0[623] exited code=0
2026-02-25__12:29:47__388941 INFO: i1[624] exited code=2
2026-02-25__12:34:54__463070 INFO: i0[5328] exited code=0
2026-02-25__12:39:17__901277 INFO: i0[623] exited code=2
2026-02-25__13:25:21__575859 INFO: i1[1321] exited code=0
2026-02-25__13:30:11__068832 INFO: i1[622] exited code=2
2026-02-25__13:49:05__448384 INFO: i1[460] exited code=0
2026-02-25__14:02:49__440857 INFO: i0[629] exited code=2
2026-02-25__14:13:00__404979 INFO: i1[625] exited code=2
2026-02-25__14:14:50__580605 INFO: i0[10408] exited code=2
2026-02-25__14:18:53__532543 INFO: i1[13987] exited code=2
2026-02-25__14:29:57__702659 INFO: i0[637] exited code=0
2026-02-25__14:34:50__382964 INFO: i1[10813] exited code=0
2026-02-25__14:39:43__607388 INFO: i0[20479] exited code=0
2026-02-25__14:40:31__219617 INFO: i1[30111] exited code=2
2026-02-25__14:51:30__608662 INFO: i1[820] exited code=0
2026-02-25__14:59:38__459802 INFO: i1[620] exited code=0
2026-02-25__15:11:07__561306 INFO: i1[625] exited code=2
2026-02-25__15:16:14__921981 INFO: i0[4319] exited code=0
2026-02-25__15:20:20__954416 INFO: i1[14324] exited code=2
2026-02-25__15:25:23__411223 INFO: i0[22403] exited code=0
2026-02-25__15:25:33__111753 INFO: i1[32296] exited code=2
2026-02-25__16:08:43__333772 INFO: i0[623] exited code=0
2026-02-25__16:13:34__284233 INFO: i1[10434] exited code=0
2026-02-25__16:24:17__577652 INFO: i1[624] exited code=0
2026-02-25__16:28:18__589861 INFO: i0[10574] exited code=2
2026-02-25__16:33:23__411705 INFO: i1[18487] exited code=0
2026-02-25__16:38:29__613440 INFO: i0[28367] exited code=0
2026-02-26__10:10:35__642488 INFO: i0[16518] exited code=0
2026-02-26__10:15:33__981906 ERROR: i0[621] exited signal=SEGV
2026-02-26__10:26:45__654554 INFO: i1[639] exited code=2
2026-02-26__10:44:25__394596 INFO: i1[625] exited code=2
2026-02-26__10:47:00__856080 INFO: i0[14178] exited code=2
2026-02-26__10:47:44__953691 INFO: i1[19314] exited code=2
2026-02-26__11:02:56__341792 INFO: i0[625] exited code=2
2026-02-26__11:33:10__691666 INFO: i0[625] exited code=2
2026-02-26__11:34:06__828742 INFO: i1[2507] exited code=2
2026-02-26__11:44:53__076279 INFO: i1[625] exited code=2
2026-02-26__11:57:37__129595 INFO: i0[625] exited code=2
2026-02-26__12:53:55__475216 INFO: i0[630] exited code=2
2026-02-26__13:24:49__813106 INFO: i1[627] exited code=2
2026-02-26__13:50:41__896000 INFO: i0[622] exited code=2
2026-02-26__13:52:09__076131 INFO: i1[4261] exited code=2
2026-02-26__13:57:36__493191 INFO: i1[624] exited code=2
2026-02-26__14:03:00__503883 INFO: i1[625] exited code=2
2026-02-26__14:07:40__315043 INFO: i1[624] exited code=2
2026-02-26__14:31:17__444608 INFO: i0[619] exited code=2
2026-02-26__14:44:58__682816 INFO: i0[625] exited code=2
2026-02-26__15:03:01__161769 INFO: i1[676] exited code=2
2026-02-26__15:03:13__472641 INFO: i0[2802] exited code=2
2026-02-26__15:03:13__757077 INFO: i1[3153] exited code=2
2026-02-26__15:36:39__160536 INFO: i0[622] exited code=2
2026-02-26__15:39:22__901474 INFO: i1[2150] exited code=2
2026-02-26__15:39:35__244488 INFO: i0[7384] exited code=2
2026-02-26__15:58:46__803402 INFO: i1[624] exited code=2
2026-02-26__16:04:44__387522 INFO: i0[4188] exited code=2
2026-02-27__11:54:05__134117 INFO: i0[626] exited code=0
2026-02-27__12:05:02__822526 INFO: i1[625] exited code=2
2026-02-27__12:19:39__847835 INFO: i0[622] exited code=2
2026-02-27__12:20:46__023362 INFO: i1[5613] exited code=2
2026-02-27__12:50:07__144282 INFO: i1[627] exited code=0
""".strip()

def parse_ts(ts_str):
    """Parse timestamp like 2026-02-25__08:43:49__734007"""
    parts = ts_str.split('__')
    dt = datetime.strptime(f'{parts[0]} {parts[1]}', '%Y-%m-%d %H:%M:%S')
    us = int(parts[2])
    return dt.timestamp() + us / 1000000.0

exited_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*exited (?:code=(\d+)|signal=(\w+))')

exits = []
for line in log_exited.split('\n'):
    m = exited_re.search(line)
    if m:
        ts = m.group(1)
        code = m.group(2)
        signal = m.group(3)
        exits.append({
            'ts': parse_ts(ts),
            'code': int(code) if code else None,
            'signal': signal
        })

# Contagem
success = sum(1 for e in exits if e['code'] == 0)
fail = sum(1 for e in exits if e['code'] and e['code'] != 0)
segv = sum(1 for e in exits if e['signal'] == 'SEGV')

# Calcular tempo total
# Método 1: Tempo decorrido entre primeiro e último exited
first_ts = min(e['ts'] for e in exits)
last_ts = max(e['ts'] for e in exits)
elapsed = last_ts - first_ts

# Método 2: Estimativa baseada no número de execuções e tempo médio
# O dataset EKF tem ~10 segundos de execução por run
avg_run_time = 10  # segundos
estimated_total = len(exits) * avg_run_time

print("=" * 80)
print("MULTIRAD RADIATION TEST - ANÁLISE DE TEMPO")
print("=" * 80)
print()
print(f"Total de execuções (exited): {len(exits)}")
print(f"Sucesso (code=0):           {success}")
print(f"Falha (code!=0):            {fail}")
print(f"SEGV:                        {segv}")
print()

print("=" * 80)
print("MÉTODO 1: TEMPO DECORRIDO")
print("=" * 80)
print(f"Primeiro exited: {datetime.fromtimestamp(first_ts)}")
print(f"Último exited:   {datetime.fromtimestamp(last_ts)}")
print(f"Tempo decorrido: {elapsed:.2f} segundos")
print(f"                {elapsed/60:.2f} minutos")
print(f"                {elapsed/3600:.4f} horas")
print()

print("=" * 80)
print("MÉTODO 2: ESTIMATIVA POR TEMPO MÉDIO")
print("=" * 80)
print(f"Execuções:       {len(exits)}")
print(f"Tempo médio/run: {avg_run_time} segundos")
print(f"Tempo estimado:  {estimated_total} segundos")
print(f"                {estimated_total/60:.2f} minutos")
print(f"                {estimated_total/3600:.4f} horas")
print()

print("=" * 80)
print("CÁLCULO DE FLUÊNCIA")
print("=" * 80)
print()
print(f"Fluxo de nêutrons:    2.6 × 10⁶ n/cm²/s")
print()
print("MÉTODO 1 (tempo decorrido):")
print(f"  Fluência:           {2.6e6 * elapsed:.4e} n/cm²")
print()
print("MÉTODO 2 (tempo médio):")
print(f"  Fluência:           {2.6e6 * estimated_total:.4e} n/cm²")
print()

# Calcular tempo médio entre execuções consecutivas
exits_sorted = sorted(exits, key=lambda x: x['ts'])
intervals = []
for i in range(1, len(exits_sorted)):
    interval = exits_sorted[i]['ts'] - exits_sorted[i-1]['ts']
    intervals.append(interval)

if intervals:
    avg_interval = sum(intervals) / len(intervals)
    print("=" * 80)
    print("ANÁLISE DE INTERVALOS")
    print("=" * 80)
    print(f"Intervalo médio entre execuções: {avg_interval:.2f} segundos")
    print(f"                               {avg_interval/60:.2f} minutos")
    
    # O intervalo médio inclui tempo de execução + tempo entre execuções
    # Se cada execução dura ~10s, então o tempo entre execuções é:
    avg_gap = avg_interval - avg_run_time
    print(f"Tempo médio entre execuções:    ~{avg_gap:.2f} segundos")