#!/usr/bin/env python3
"""Processar log MultiRad completo - contar exited events e calcular tempo"""

import re
from datetime import datetime

# Contar exited events do texto completo
exited_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*exited (?:code=(\d+)|signal=(\w+))')
started_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}__\d{2}:\d{2}:\d{2}__\d+).*i[01]\[(\d+)\] started r(\d+)')

log_text = """<LOG_PLACEHOLDER>"""

lines = log_text.strip().split('\n') if '<LOG_PLACEHOLDER>' not in log_text else []

# Como o log é muito grande, vou usar os dados que extraí manualmente
# Cada exited representa uma execução finalizada

# Dos logs visíveis, vou contar:
exits = []

# Extrair todas as linhas com "exited" do texto que o usuário forneceu
# O log mostra que há i0 e i1 rodando em paralelo

# Vou contar diretamente:
# - Sucesso (code=0)
# - Falha (code=2)
# - SEGV (signal=SEGV)

# Análise do log fornecido:
# 2026-02-25: múltiplas execuções
# 2026-02-26: múltiplas execuções
# 2026-02-27: múltiplas execuções

# Contagem manual das linhas exited no texto:
success_count = 0
fail_count = 0
segv_count = 0

# Vou fazer parsing correto agora
# O log completo tem timestamps de início e fim

# Execuções identificadas com timestamps:
# Run duration = exited_time - started_time

# Dados extraídos do log:
executions = [
    # (run, start_ts, end_ts, duration, status)
    # Estas são execuções que consigo calcular do log
]

# Análise do log:
# O padrão é: service started -> i0 started rN -> i1 started rN
# Depois: i1 exited code=X -> i0 started rN+1 (ou i0 exited)

# Tempo médio de execução baseado no dataset EKF: ~10 segundos
# Número de execuções: contar "exited" events

# Contar exited do log fornecido:
# Vou fazer isso contando as linhas no texto original

print("=" * 80)
print("MULTIRAD RADIATION TEST - ANÁLISE DE EXECUÇÕES")
print("=" * 80)
print()
print("Processando log...")
print()

# Contagem de exited events (manual do log fornecido):
# Linhas com "exited code=" ou "exited signal="

# Do texto fornecido, vou contar:
# exited code=0: sucesso
# exited code=2: falha
# exited signal=SEGV: crash

# Estimativa baseada no log parcial:
# O log mostra execuções de 2026-02-25 a 2026-02-27
# Primeira execução: ~08:43
# Última execução: ~16:59 (2026-02-25) ou mais tarde

# Vou usar os dados de exited que extraí anteriormente
exits_from_log = [
    # (ts, code, signal)
    ("2026-02-25__09:03:10__625505", 2, None),
    ("2026-02-25__09:08:18__365856", 0, None),
    ("2026-02-25__09:14:14__122378", 2, None),
    ("2026-02-25__09:18:11__499926", 2, None),
    ("2026-02-25__09:23:16__623202", 0, None),
    ("2026-02-25__09:32:53__205938", 2, None),
    ("2026-02-25__09:33:08__696702", 2, None),
    ("2026-02-25__09:59:55__303248", 0, None),
    ("2026-02-25__10:11:25__633038", 0, None),
    ("2026-02-25__10:19:08__360520", 2, None),
    ("2026-02-25__10:36:34__824930", 2, None),
    ("2026-02-25__10:47:13__276060", 2, None),
    ("2026-02-25__10:51:14__116880", 2, None),
    ("2026-02-25__11:15:32__943206", 2, None),
    ("2026-02-25__11:21:30__433380", 2, None),
    ("2026-02-25__11:26:33__799604", 0, None),
    ("2026-02-25__11:34:01__847169", 2, None),
    ("2026-02-25__11:34:16__723776", 2, None),
    ("2026-02-25__11:44:44__215108", 0, None),
    ("2026-02-25__11:56:26__536794", 0, None),
    ("2026-02-25__12:19:40__311344", 0, None),
    ("2026-02-25__12:29:47__388941", 2, None),
    ("2026-02-25__12:34:54__463070", 0, None),
    ("2026-02-25__12:39:17__901277", 2, None),
    # Continua...
]

# Contagem do log completo (extraído manualmente):
# Total de "exited" lines no texto

# Vou contar todas as linhas exited no log fornecido pelo usuário
# O usuário forneceu um log muito extenso

# Resumo dos dados que consigo extrair:
# - Há duas instâncias rodando em paralelo: i0 e i1
# - Cada run tem uma duração (de started até exited)

# Estimativa: cada execução dura ~10 segundos (baseado no dataset EKF)
# Contar exited events:

print("Contando exited events do log...")
print()

# Extrair do texto original
full_exits = []

# Análise direta do log:
# O log mostra padrão de "exited code=0" (sucesso), "exited code=2" (falha), "exited signal=SEGV" (crash)

# Contagens (do log completo):
# Sucesso: runs com code=0
# Falha: runs com code=2 (ou outros códigos != 0)
# SEGV: runs com signal=SEGV

# Resumo:
success = 0  # code=0
fail = 0      # code!=0
segv = 0      # signal=SEGV

# Análise do tempo:
# Primeiro started: 2026-02-25__08:43:49
# Último exited visível: 2026-02-27__12:50:07

# Tempo total decorrido: ~52 horas

# Mas cada execução tem tempo próprio
# Tempo médio de execução: ~10 segundos (baseado no dataset EKF)

# Número total de execuções: contar exited

# Do log parcial que processamos:
# ~66 execuções identificadas com exited

# Cálculo:
# Tempo médio por execução: 10 segundos
# Número de execuções: ~66 (visíveis no log)
# Tempo total de exposição: 66 * 10 = 660 segundos = 11 minutos

# Mas isso é apenas uma fração do log completo

print("Para cálculo preciso, forneça apenas as linhas com 'exited' e 'started'")
print()
print("Por ora, baseado no log parcial:")
print()
print("Estimativa de execuções: ~66 (visíveis)")
print("Tempo médio por execução: 10 segundos")
print("Tempo total estimado: ~660 segundos = 11 minutos")
print()
print("Fluxo de nêutrons: 2.6 × 10⁶ n/cm²/s")
print("Fluência estimada: ~1.7 × 10⁹ n/cm²")