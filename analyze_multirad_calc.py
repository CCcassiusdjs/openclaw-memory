#!/usr/bin/env python3
"""Processar log MultiRad COMPLETO e calcular tempo total de execução"""

import re
from datetime import datetime

# Log completo fornecido pelo usuário
log_full = """
2026-02-25__08:43:49__734007 INFO: i0[204417] started r1 >>>>>>>>>> r27
2026-02-25__09:03:10__625505 INFO: i1[627] exited code=2
2026-02-25__09:03:10__987416 INFO: i0[10032] started r3 >>>>>>>>>> r29
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
2026-02-25__16:47:37__932292 INFO: service stopped result=success code=killed status=TERM
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

# Linhas com started (para calcular duração)
started_lines = """
2026-02-25__08:43:49__734007 INFO: i0[204417] started r1 >>>>>>>>>> r27
2026-02-25__08:17:15__579871 INFO: i1[621] started r1 >>>>>>>>>> r27
2026-02-25__08:17:24__134562 INFO: i0[625] started r2 >>>>>>>>>> r28
2026-02-25__08:17:20__967577 INFO: i1[627] started r2 >>>>>>>>>> r28
2026-02-25__09:03:10__987416 INFO: i0[10032] started r3 >>>>>>>>>> r29
2026-02-25__09:08:18__548954 INFO: i1[20026] started r3 >>>>>>>>>> r29
2026-02-25__08:17:16__240700 INFO: i0[626] started r4 >>>>>>>>>> r30
2026-02-25__09:14:14__300878 INFO: i1[3727] started r4 >>>>>>>>>> r30
2026-02-25__09:18:11__876033 INFO: i0[8796] started r5 >>>>>>>>>> r31
2026-02-25__09:23:16__821931 INFO: i1[9402] started r5 >>>>>>>>>> r31
2026-02-25__09:17:26__413735 INFO: i0[626] started r6 >>>>>>>>>> r32
2026-02-25__09:17:23__263850 INFO: i1[663] started r6 >>>>>>>>>> r32
2026-02-25__09:17:16__634891 INFO: i0[625] started r7 >>>>>>>>>> r33
2026-02-25__09:17:24__040792 INFO: i1[622] started r7 >>>>>>>>>> r33
2026-02-25__09:32:53__465936 INFO: i0[1611] started r8 >>>>>>>>>> r34
2026-02-25__09:33:08__914254 INFO: i1[2114] started r8 >>>>>>>>>> r34
2026-02-25__09:17:25__820703 INFO: i0[624] started r9 >>>>>>>>>> r35
2026-02-25__09:17:16__324308 INFO: i1[628] started r9 >>>>>>>>>> r35
2026-02-25__09:17:19__479559 INFO: i0[662] started r10 >>>>>>>>>> r36
2026-02-25__09:17:26__833175 INFO: i1[623] started r10 >>>>>>>>>> r36
2026-02-25__09:59:56__844720 INFO: i0[10583] started r11 >>>>>>>>>> r37
2026-02-25__09:17:15__863686 INFO: i1[608] started r11 >>>>>>>>>> r37
2026-02-25__09:17:15__824209 INFO: i0[620] started r12 >>>>>>>>>> r38
2026-02-25__10:11:25__842749 INFO: i1[11008] started r12 >>>>>>>>>> r38
2026-02-25__09:17:15__941292 INFO: i0[617] started r13 >>>>>>>>>> r39
2026-02-25__09:17:18__824087 INFO: i1[623] started r13 >>>>>>>>>> r39
2026-02-25__10:19:08__739969 INFO: i0[3134] started r14 >>>>>>>>>> r40
2026-02-25__09:17:18__289764 INFO: i1[623] started r14 >>>>>>>>>> r40
2026-02-25__09:17:26__700645 INFO: i0[784] started r15 >>>>>>>>>> r41
2026-02-25__09:17:17__883022 INFO: i1[626] started r15 >>>>>>>>>> r41
2026-02-25__09:17:22__104868 INFO: i0[625] started r16 >>>>>>>>>> r42
2026-02-25__10:36:35__288683 INFO: i1[4064] started r16 >>>>>>>>>> r42
2026-02-25__10:39:48__174179 INFO: i0[807] started r17 >>>>>>>>>> r43
2026-02-25__09:17:17__573256 INFO: i1[625] started r17 >>>>>>>>>> r43
2026-02-25__09:17:20__908098 INFO: i0[622] started r18 >>>>>>>>>> r44
2026-02-25__10:47:13__528867 INFO: i1[2224] started r18 >>>>>>>>>> r44
2026-02-25__10:51:18__951740 INFO: i0[9921] started r19 >>>>>>>>>> r45
2026-02-25__09:17:16__078417 INFO: i1[621] started r19 >>>>>>>>>> r45
2026-02-25__09:17:20__437716 INFO: i0[626] started r20 >>>>>>>>>> r46
2026-02-25__11:01:37__892015 INFO: i1[6123] started r20 >>>>>>>>>> r46
2026-02-25__09:17:21__013035 INFO: i0[625] started r21 >>>>>>>>>> r47
2026-02-25__09:17:16__153611 INFO: i1[626] started r21 >>>>>>>>>> r47
2026-02-25__11:15:33__380110 INFO: i0[9660] started r22 >>>>>>>>>> r48
2026-02-25__11:17:16__484391 INFO: i1[627] started r22 >>>>>>>>>> r48
2026-02-25__11:21:30__931309 INFO: i0[1749] started r23 >>>>>>>>>> r49
2026-02-25__11:26:34__127767 INFO: i1[10476] started r23 >>>>>>>>>> r49
2026-02-25__11:17:16__205872 INFO: i0[622] started r24 >>>>>>>>>> r50
2026-02-25__11:34:02__069173 INFO: i1[8789] started r24 >>>>>>>>>> r50
2026-02-25__11:34:16__940718 INFO: i0[9254] started r25 >>>>>>>>>> r51
2026-02-25__11:17:16__352131 INFO: i1[621] started r25 >>>>>>>>>> r51
2026-02-25__11:44:44__451555 INFO: i0[10386] started r26 >>>>>>>>>> r52
2026-02-25__11:17:24__639808 INFO: i1[619] started r26 >>>>>>>>>> r52
2026-02-25__11:17:15__353749 INFO: i0[619] started r27 >>>>>>>>>> r53
2026-02-25__11:17:25__873968 INFO: i1[623] started r27 >>>>>>>>>> r53
2026-02-25__11:56:26__729070 INFO: i0[10489] started r28 >>>>>>>>>> r54
2026-02-25__11:17:15__863974 INFO: i1[643] started r28 >>>>>>>>>> r54
2026-02-25__11:17:16__620301 INFO: i0[627] started r29 >>>>>>>>>> r55
2026-02-25__11:17:18__517926 INFO: i1[623] started r29 >>>>>>>>>> r55
2026-02-25__11:17:24__158240 INFO: i0[623] started r30 >>>>>>>>>> r56
2026-02-25__12:19:40__618138 INFO: i1[10605] started r30 >>>>>>>>>> r56
2026-02-25__12:17:23__169125 INFO: i0[624] started r31 >>>>>>>>>> r57
2026-02-25__12:17:16__961787 INFO: i1[624] started r31 >>>>>>>>>> r57
2026-02-25__12:29:47__660949 INFO: i0[5328] started r32 >>>>>>>>>> r58
2026-02-25__12:34:54__978369 INFO: i1[15235] started r32 >>>>>>>>>> r58
2026-02-25__12:17:15__473616 INFO: i0[623] started r33 >>>>>>>>>> r59
2026-02-25__12:39:29__620633 INFO: i1[2157] started r33 >>>>>>>>>> r59
2026-02-25__12:17:19__085964 INFO: i0[621] started r34 >>>>>>>>>> r60
""".strip()

def parse_ts(ts_str):
    """Parse timestamp like 2026-02-25__08:43:49__734007"""
    parts = ts_str.split('__')
    dt = datetime.strptime(f'{parts[0]} {parts[1]}', '%Y-%m-%d %H:%M:%S')
    us = int(parts[2])
    return dt.timestamp() + us / 1000000.0

# Processar started
started_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i([01])\[(\d+)\] started r(\d+)')
pending = {}
for line in started_lines.split('\n'):
    m = started_re.search(line)
    if m:
        ts, inst, pid, run = m.groups()
        pending[(inst, pid)] = (parse_ts(ts), int(run))

# Processar exited
exited_re = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i([01])\[(\d+)\] exited (?:code=(\d+)|signal=(\w+))')
runs = []
for line in log_full.split('\n'):
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
                'duration': duration,
                'status': status,
                'code': int(code) if code else None,
                'signal': signal
            })
            del pending[key]

# Resultados
total_duration = sum(r['duration'] for r in runs)
success = sum(1 for r in runs if r['code'] == 0)
fail = sum(1 for r in runs if r['code'] and r['code'] != 0)
segv = sum(1 for r in runs if r['signal'] == 'SEGV')

print("=" * 80)
print("MULTIRAD RADIATION TEST - ANÁLISE DE TEMPO DE EXECUÇÃO")
print("=" * 80)
print()
print(f"Execuções processadas: {len(runs)}")
print(f"Sucesso (code=0):      {success}")
print(f"Falha (code!=0):       {fail}")
print(f"SEGV:                  {segv}")
print()

print("=" * 80)
print("TEMPOS DE EXECUÇÃO")
print("=" * 80)
for r in sorted(runs, key=lambda x: x['run']):
    print(f"Run {r['run']:3d} [i{r['instance']}]: {r['duration']:8.2f}s | {r['status']}")

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

# Estatísticas
if runs:
    durations = [r['duration'] for r in runs]
    print("=" * 80)
    print("ESTATÍSTICAS")
    print("=" * 80)
    print(f"Duração mínima: {min(durations):.2f}s")
    print(f"Duração máxima: {max(durations):.2f}s")
    print(f"Duração média:  {sum(durations)/len(durations):.2f}s")