#!/usr/bin/env python3
"""Análise de tempos de execução do MultiRad"""

import re
from datetime import datetime

log_data = """
2026-02-25__08:43:49__734007 INFO: i0[204417] started r1 >>>>>>>>>> r27
2026-02-25__08:43:50__263647 INFO: service[204375] started
2026-02-25__08:48:02__358473 INFO: sut4 has been turned off via relay channel 1
2026-02-25__08:48:05__985491 INFO: sut4 has been turned on via relay channel 1
2026-02-25__08:17:14__947098 INFO: service[530] started
2026-02-25__08:17:15__579871 INFO: i1[621] started r1 >>>>>>>>>> r27
2026-02-25__08:53:33__581415 INFO: sut4 has been turned off via relay channel 1
2026-02-25__08:53:37__354266 INFO: sut4 has been turned on via relay channel 1
2026-02-25__08:54:50__438811 INFO: sut4 has been turned off via relay channel 1
2026-02-25__08:54:57__213775 INFO: sut4 has been turned on via relay channel 1
2026-02-25__08:17:23__122813 INFO: service[534] started
2026-02-25__08:17:24__134562 INFO: i0[625] started r2 >>>>>>>>>> r28
2026-02-25__08:57:25__705677 INFO: sut4 has been turned off via relay channel 1
2026-02-25__08:57:29__366053 INFO: sut4 has been turned on via relay channel 1
2026-02-25__08:17:20__420829 INFO: service[536] started
2026-02-25__08:17:20__967577 INFO: i1[627] started r2 >>>>>>>>>> r28
2026-02-25__09:03:10__625505 INFO: i1[627] exited code=2
2026-02-25__09:03:10__987416 INFO: i0[10032] started r3 >>>>>>>>>> r29
2026-02-25__09:08:18__365856 INFO: i0[10032] exited code=0
2026-02-25__09:08:18__548954 INFO: i1[20026] started r3 >>>>>>>>>> r29
2026-02-25__09:11:43__493507 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:11:47__208364 INFO: sut4 has been turned on via relay channel 1
2026-02-25__08:17:15__859074 INFO: service[535] started
2026-02-25__08:17:16__240700 INFO: i0[626] started r4 >>>>>>>>>> r30
2026-02-25__09:14:14__122378 INFO: i0[626] exited code=2
2026-02-25__09:14:14__300878 INFO: i1[3727] started r4 >>>>>>>>>> r30
2026-02-25__09:18:11__499926 INFO: i1[3727] exited code=2
2026-02-25__09:18:11__876033 INFO: i0[8796] started r5 >>>>>>>>>> r31
2026-02-25__09:23:16__623202 INFO: i0[8796] exited code=0
2026-02-25__09:23:16__821931 INFO: i1[9402] started r5 >>>>>>>>>> r31
2026-02-25__09:23:41__389342 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:23:45__125126 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:25__326783 INFO: service[536] started
2026-02-25__09:17:26__413735 INFO: i0[626] started r6 >>>>>>>>>> r32
2026-02-25__09:25:40__018824 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:25:43__737694 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:21__741086 INFO: service[536] started
2026-02-25__09:17:23__263850 INFO: i1[663] started r6 >>>>>>>>>> r32
2026-02-25__09:28:46__066555 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:28:49__753742 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__916184 INFO: service[534] started
2026-02-25__09:17:16__634891 INFO: i0[625] started r7 >>>>>>>>>> r33
2026-02-25__09:31:19__498662 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:31:23__235719 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:23__642040 INFO: service[531] started
2026-02-25__09:17:24__040792 INFO: i1[622] started r7 >>>>>>>>>> r33
2026-02-25__09:32:53__205938 INFO: i1[622] exited code=2
2026-02-25__09:32:53__465936 INFO: i0[1611] started r8 >>>>>>>>>> r34
2026-02-25__09:33:08__696702 INFO: i0[1611] exited code=2
2026-02-25__09:33:08__914254 INFO: i1[2114] started r8 >>>>>>>>>> r34
2026-02-25__09:34:00__165730 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:34:03__865469 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:25__453271 INFO: service[533] started
2026-02-25__09:17:25__820703 INFO: i0[624] started r9 >>>>>>>>>> r35
2026-02-25__09:37:07__729172 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:37:11__430198 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__989597 INFO: service[537] started
2026-02-25__09:17:16__324308 INFO: i1[628] started r9 >>>>>>>>>> r35
2026-02-25__09:40:12__870276 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:40:16__589707 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:16__247041 INFO: service[533] started
2026-02-25__09:17:19__479559 INFO: i0[662] started r10 >>>>>>>>>> r36
2026-02-25__09:52:26__209039 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:52:29__933086 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:53:42__909920 INFO: sut4 has been turned off via relay channel 1
2026-02-25__09:53:49__753272 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:26__411063 INFO: service[532] started
2026-02-25__09:17:26__833175 INFO: i1[623] started r10 >>>>>>>>>> r36
2026-02-25__09:59:55__303248 INFO: i1[623] exited code=0
2026-02-25__09:59:56__844720 INFO: i0[10583] started r11 >>>>>>>>>> r37
2026-02-25__10:02:31__918739 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:02:35__613492 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__489553 INFO: service[517] started
2026-02-25__09:17:15__863686 INFO: i1[608] started r11 >>>>>>>>>> r37
2026-02-25__10:05:13__524226 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:05:17__312766 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__456628 INFO: service[529] started
2026-02-25__09:17:15__824209 INFO: i0[620] started r12 >>>>>>>>>> r38
2026-02-25__10:11:25__633038 INFO: i0[620] exited code=0
2026-02-25__10:11:25__842749 INFO: i1[11008] started r12 >>>>>>>>>> r38
2026-02-25__10:12:12__820418 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:12:16__609197 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__279563 INFO: service[526] started
2026-02-25__09:17:15__941292 INFO: i0[617] started r13 >>>>>>>>>> r39
2026-02-25__10:16:50__154253 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:16:53__865773 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:18__456999 INFO: service[532] started
2026-02-25__09:17:18__824087 INFO: i1[623] started r13 >>>>>>>>>> r39
2026-02-25__10:19:08__360520 INFO: i1[623] exited code=2
2026-02-25__10:19:08__739969 INFO: i0[3134] started r14 >>>>>>>>>> r40
2026-02-25__10:19:57__846127 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:20:01__658309 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:17__862455 INFO: service[532] started
2026-02-25__09:17:18__289764 INFO: i1[623] started r14 >>>>>>>>>> r40
2026-02-25__10:25:04__037768 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:25:07__793182 INFO: sut4 has been turned on via relay channel 1
2026-02-25__10:26:20__589715 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:26:27__467266 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:21__410396 INFO: service[535] started
2026-02-25__09:17:26__700645 INFO: i0[784] started r15 >>>>>>>>>> r41
2026-02-25__10:32:15__310140 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:32:19__041320 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:17__404916 INFO: service[535] started
2026-02-25__09:17:17__883022 INFO: i1[626] started r15 >>>>>>>>>> r41
2026-02-25__10:33:51__183427 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:33:55__061895 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:21__367697 INFO: service[534] started
2026-02-25__09:17:22__104868 INFO: i0[625] started r16 >>>>>>>>>> r42
2026-02-25__10:36:34__824930 INFO: i0[625] exited code=2
2026-02-25__10:36:35__288683 INFO: i1[4064] started r16 >>>>>>>>>> r42
2026-02-25__10:37:22__288542 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:37:26__172410 INFO: sut4 has been turned on via relay channel 1
2026-02-25__10:38:37__981563 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:38:44__874933 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:17__088430 INFO: service[533] started
2026-02-25__10:39:48__174179 INFO: i0[807] started r17 >>>>>>>>>> r43
2026-02-25__10:41:35__195260 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:41:38__890184 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:16__996087 INFO: service[534] started
2026-02-25__09:17:17__573256 INFO: i1[625] started r17 >>>>>>>>>> r43
2026-02-25__10:45:16__178535 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:45:19__873956 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:20__547650 INFO: service[532] started
2026-02-25__09:17:20__908098 INFO: i0[622] started r18 >>>>>>>>>> r44
2026-02-25__10:47:13__276060 INFO: i0[622] exited code=2
2026-02-25__10:47:13__528867 INFO: i1[2224] started r18 >>>>>>>>>> r44
2026-02-25__10:51:14__116880 INFO: i1[2224] exited code=2
2026-02-25__10:51:18__951740 INFO: i0[9921] started r19 >>>>>>>>>> r45
2026-02-25__10:56:09__606599 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:56:13__450664 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__733932 INFO: service[530] started
2026-02-25__09:17:16__078417 INFO: i1[621] started r19 >>>>>>>>>> r45
2026-02-25__10:57:49__963250 INFO: sut4 has been turned off via relay channel 1
2026-02-25__10:57:53__784685 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:20__002882 INFO: service[535] started
2026-02-25__09:17:20__437716 INFO: i0[626] started r20 >>>>>>>>>> r46
2026-02-25__11:01:37__600263 INFO: i0[626] exited code=2
2026-02-25__11:01:37__892015 INFO: i1[6123] started r20 >>>>>>>>>> r46
2026-02-25__11:04:07__532476 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:04:11__285853 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:20__610756 INFO: service[534] started
2026-02-25__09:17:21__013035 INFO: i0[625] started r21 >>>>>>>>>> r47
2026-02-25__11:10:05__066978 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:10:08__821788 INFO: sut4 has been turned on via relay channel 1
2026-02-25__09:17:15__620085 INFO: service[535] started
2026-02-25__09:17:16__153611 INFO: i1[626] started r21 >>>>>>>>>> r47
2026-02-25__11:15:32__943206 INFO: i1[626] exited code=2
2026-02-25__11:15:33__380110 INFO: i0[9660] started r22 >>>>>>>>>> r48
2026-02-25__11:18:36__690919 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:18:40__490445 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:19:54__388347 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:20:01__162784 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:16__052251 INFO: service[536] started
2026-02-25__11:17:16__484391 INFO: i1[627] started r22 >>>>>>>>>> r48
2026-02-25__11:21:30__433380 INFO: i1[627] exited code=2
2026-02-25__11:21:30__931309 INFO: i0[1749] started r23 >>>>>>>>>> r49
2026-02-25__11:26:33__799604 INFO: i0[1749] exited code=0
2026-02-25__11:26:34__127767 INFO: i1[10476] started r23 >>>>>>>>>> r49
2026-02-25__11:28:54__247627 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:28:58__018970 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:15__793137 INFO: service[531] started
2026-02-25__11:17:16__205872 INFO: i0[622] started r24 >>>>>>>>>> r50
2026-02-25__11:34:01__847169 INFO: i0[622] exited code=2
2026-02-25__11:34:02__069173 INFO: i1[8789] started r24 >>>>>>>>>> r50
2026-02-25__11:34:16__723776 INFO: i1[8789] exited code=2
2026-02-25__11:34:16__940718 INFO: i0[9254] started r25 >>>>>>>>>> r51
2026-02-25__11:37:31__333616 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:37:35__049239 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:38:46__989781 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:38:53__765138 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:16__019713 INFO: service[530] started
2026-02-25__11:17:16__352131 INFO: i1[621] started r25 >>>>>>>>>> r51
2026-02-25__11:44:44__215108 INFO: i1[621] exited code=0
2026-02-25__11:44:44__451555 INFO: i0[10386] started r26 >>>>>>>>>> r52
2026-02-25__11:46:27__226438 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:46:30__977059 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:24__267060 INFO: service[528] started
2026-02-25__11:17:24__639808 INFO: i1[619] started r26 >>>>>>>>>> r52
2026-02-25__11:47:44__950975 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:47:51__878735 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:15__055196 INFO: service[528] started
2026-02-25__11:17:15__353749 INFO: i0[619] started r27 >>>>>>>>>> r53
2026-02-25__11:50:19__657518 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:50:23__333925 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:25__514923 INFO: service[532] started
2026-02-25__11:17:25__873968 INFO: i1[623] started r27 >>>>>>>>>> r53
2026-02-25__11:56:26__536794 INFO: i1[623] exited code=0
2026-02-25__11:56:26__729070 INFO: i0[10489] started r28 >>>>>>>>>> r54
2026-02-25__11:59:47__301250 INFO: sut4 has been turned off via relay channel 1
2026-02-25__11:59:51__098228 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:15__468175 INFO: service[540] started
2026-02-25__11:17:15__863974 INFO: i1[643] started r28 >>>>>>>>>> r54
2026-02-25__12:05:47__369064 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:05:50__997540 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:16__180929 INFO: service[536] started
2026-02-25__11:17:16__620301 INFO: i0[627] started r29 >>>>>>>>>> r55
2026-02-25__12:11:37__565395 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:11:41__289885 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:18__160594 INFO: service[532] started
2026-02-25__11:17:18__517926 INFO: i1[623] started r29 >>>>>>>>>> r55
2026-02-25__12:13:32__993768 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:13:36__609510 INFO: sut4 has been turned on via relay channel 1
2026-02-25__11:17:23__488569 INFO: service[532] started
2026-02-25__11:17:24__158240 INFO: i0[623] started r30 >>>>>>>>>> r56
2026-02-25__12:19:40__311344 INFO: i0[623] exited code=0
2026-02-25__12:19:40__618138 INFO: i1[10605] started r30 >>>>>>>>>> r56
2026-02-25__12:22:06__061181 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:22:09__799302 INFO: sut4 has been turned on via relay channel 1
2026-02-25__12:17:22__411993 INFO: service[533] started
2026-02-25__12:17:23__169125 INFO: i0[624] started r31 >>>>>>>>>> r57
2026-02-25__12:26:28__925837 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:26:32__662295 INFO: sut4 has been turned on via relay channel 1
2026-02-25__12:17:16__595837 INFO: service[533] started
2026-02-25__12:17:16__961787 INFO: i1[624] started r31 >>>>>>>>>> r57
2026-02-25__12:29:47__388941 INFO: i1[624] exited code=2
2026-02-25__12:29:47__660949 INFO: i0[5328] started r32 >>>>>>>>>> r58
2026-02-25__12:34:54__463070 INFO: i0[5328] exited code=0
2026-02-25__12:34:54__978369 INFO: i1[15235] started r32 >>>>>>>>>> r58
2026-02-25__12:37:37__081183 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:37:40__904930 INFO: sut4 has been turned on via relay channel 1
2026-02-25__12:17:14__941763 INFO: service[532] started
2026-02-25__12:17:15__473616 INFO: i0[623] started r33 >>>>>>>>>> r59
2026-02-25__12:39:17__901277 INFO: i0[623] exited code=2
2026-02-25__12:39:29__620633 INFO: i1[2157] started r33 >>>>>>>>>> r59
2026-02-25__12:40:56__023995 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:40:59__805112 INFO: sut4 has been turned on via relay channel 1
2026-02-25__12:17:18__508098 INFO: service[530] started
2026-02-25__12:17:19__085964 INFO: i0[621] started r34 >>>>>>>>>> r60
2026-02-25__12:43:58__874851 INFO: sut4 has been turned off via relay channel 1
2026-02-25__12:43:58__874851 INFO: sut4 has been turned off via relay channel 1
""".strip()

def parse_timestamp(ts_str):
    """Parse timestamp like 2026-02-25__08:43:49__734007"""
    # Extract date, time, microseconds
    match = re.match(r'(\d{4}-\d{2}-\d{2})__(\d{2}:\d{2}:\d{2})__(\d+)', ts_str)
    if not match:
        return None
    date_str, time_str, us_str = match.groups()
    dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    return dt, int(us_str)

def calculate_duration(start_ts, end_ts):
    """Calculate duration in seconds between two timestamps"""
    start_dt, start_us = parse_timestamp(start_ts)
    end_dt, end_us = parse_timestamp(end_ts)
    if start_dt.date() != end_dt.date():
        # Cross midnight - simplified
        delta = (end_dt - start_dt).total_seconds()
    else:
        delta = (end_dt - start_dt).total_seconds()
    # Add microsecond difference
    delta += (end_us - start_us) / 1000000.0
    return delta

# Parse the log
lines = log_data.strip().split('\n')
runs = []
current_start = None
current_run = None

started_pattern = re.compile(r'INFO: i[01]\[(\d+)\] started r(\d+)')
exited_pattern = re.compile(r'INFO: i[01]\[(\d+)\] exited code=(\d+)')
exited_signal_pattern = re.compile(r'INFO: i[01]\[(\d+)\] exited signal=(\w+)')

for line in lines:
    ts = line[:26]  # 2026-02-25__08:43:49__734007
    
    started_match = started_pattern.search(line)
    if started_match:
        pid, run_num = started_match.groups()
        if current_start is not None:
            # Calculate previous run duration (from start to next start)
            pass
        current_start = ts
        current_run = int(run_num)
        continue
    
    exited_match = exited_pattern.search(line)
    if exited_match:
        pid, code = exited_match.groups()
        if current_start:
            duration = calculate_duration(current_start, ts)
            runs.append({
                'run': current_run,
                'start': current_start,
                'end': ts,
                'duration': duration,
                'exit_code': int(code),
                'signal': None
            })
            current_start = None
            continue
    
    exited_signal_match = exited_signal_pattern.search(line)
    if exited_signal_match:
        pid, sig = exited_signal_match.groups()
        if current_start:
            duration = calculate_duration(current_start, ts)
            runs.append({
                'run': current_run,
                'start': current_start,
                'end': ts,
                'duration': duration,
                'exit_code': None,
                'signal': sig
            })
            current_start = None
            continue

# Print results
print("=" * 80)
print("MULTIRAD RADIATION TEST - RUN ANALYSIS")
print("=" * 80)
print()

total_duration = 0
success_count = 0
fail_count = 0
segv_count = 0

for run in runs:
    total_duration += run['duration']
    if run['signal'] == 'SEGV':
        segv_count += 1
        fail_count += 1
        status = "SEGV"
    elif run['exit_code'] == 0:
        success_count += 1
        status = "SUCCESS"
    else:
        fail_count += 1
        status = f"FAIL(code={run['exit_code']})"
    
    print(f"Run {run['run']:3d}: {run['duration']:8.2f}s | {status}")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total runs:       {len(runs)}")
print(f"Successful:        {success_count}")
print(f"Failed:            {fail_count}")
print(f"  - SEGV crashes:  {segv_count}")
print(f"  - Other errors:  {fail_count - segv_count}")
print()
print(f"Total duration:    {total_duration:.2f} seconds")
print(f"                  {total_duration/60:.2f} minutes")
print(f"                  {total_duration/3600:.4f} hours")
print()
print("=" * 80)
print("FLUENCE CALCULATION")
print("=" * 80)
print(f"Neutron flux:      2.6 × 10⁶ n/cm²/s")
print(f"Total duration:    {total_duration:.2f} s")
print(f"Total fluence:     {2.6e6 * total_duration:.4e} n/cm²")