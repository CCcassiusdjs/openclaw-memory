#!/usr/bin/env python3
"""
fs-query.py - Consulta ao banco de monitoramento

Uso:
    fs-query.py --today
    fs-query.py --since 2026-03-01
    fs-query.py --type CREATE --limit 20
    fs-query.py --path /home/csilva/Documents
    fs-query.py --stats
"""

import argparse
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


DB_PATH = Path('/home/csilva/.openclaw/workspace/logs/fs-monitor/fs-monitor.db')


def query_events(args):
    """Consulta eventos"""
    conn = sqlite3.connect(str(DB_PATH))
    
    query = 'SELECT * FROM events WHERE 1=1'
    params = []
    
    if args.since:
        query += ' AND timestamp >= ?'
        params.append(args.since)
    
    if args.until:
        query += ' AND timestamp <= ?'
        params.append(args.until)
    
    if args.type:
        query += ' AND event_type = ?'
        params.append(args.type)
    
    if args.path:
        query += ' AND path LIKE ?'
        params.append(f'{args.path}%')
    
    query += f' ORDER BY timestamp DESC LIMIT {args.limit}'
    
    cursor = conn.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    
    events = []
    for row in cursor.fetchall():
        events.append(dict(zip(columns, row)))
    
    conn.close()
    return events


def get_stats(args):
    """Retorna estatísticas"""
    conn = sqlite3.connect(str(DB_PATH))
    
    if args.date:
        date = args.date
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # Total de eventos
    cursor = conn.execute(
        'SELECT COUNT(*) FROM events WHERE timestamp LIKE ?',
        (f'{date}%',)
    )
    total = cursor.fetchone()[0]
    
    # Por tipo
    cursor = conn.execute(
        '''SELECT event_type, COUNT(*) FROM events 
           WHERE timestamp LIKE ? 
           GROUP BY event_type''',
        (f'{date}%',)
    )
    by_type = dict(cursor.fetchall())
    
    # Top diretórios
    cursor = conn.execute(
        '''SELECT 
             SUBSTR(path, 1, INSTR(SUBSTR(path, 2), '/') + 1) as root_dir,
             COUNT(*) as count
           FROM events 
           WHERE timestamp LIKE ?
           GROUP BY root_dir
           ORDER BY count DESC
           LIMIT 10''',
        (f'{date}%',)
    )
    top_dirs = cursor.fetchall()
    
    # Timeline (por hora)
    cursor = conn.execute(
        '''SELECT 
             SUBSTR(timestamp, 12, 2) as hour,
             COUNT(*) as count
           FROM events 
           WHERE timestamp LIKE ?
           GROUP BY hour
           ORDER BY hour''',
        (f'{date}%',)
    )
    timeline = dict(cursor.fetchall())
    
    conn.close()
    
    return {
        'date': date,
        'total_events': total,
        'by_type': by_type,
        'top_directories': top_dirs,
        'timeline': timeline
    }


def get_baseline(args):
    """Retorna baseline"""
    conn = sqlite3.connect(str(DB_PATH))
    
    query = 'SELECT * FROM baseline WHERE 1=1'
    params = []
    
    if args.path:
        query += ' AND path LIKE ?'
        params.append(f'{args.path}%')
    
    query += f' LIMIT {args.limit}'
    
    cursor = conn.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    
    baseline = []
    for row in cursor.fetchall():
        baseline.append(dict(zip(columns, row)))
    
    conn.close()
    return baseline


def detect_anomalies(args):
    """Detecta anomalias"""
    conn = sqlite3.connect(str(DB_PATH))
    
    anomalies = []
    
    # 1. Muitos deletions em pouco tempo (possível ataque ou erro)
    cursor = conn.execute('''
        SELECT 
            SUBSTR(timestamp, 1, 16) as minute,
            COUNT(*) as count
        FROM events
        WHERE event_type LIKE '%DELETE%'
        GROUP BY minute
        HAVING count > ?
        ORDER BY count DESC
        LIMIT 10
    ''', (args.threshold,))
    
    mass_deletions = cursor.fetchall()
    if mass_deletions:
        anomalies.append({
            'type': 'mass_deletion',
            'description': f'{len(mass_deletions)} minutos com >{args.threshold} deleções',
            'data': mass_deletions
        })
    
    # 2. Arquivos grandes criados recentemente
    cursor = conn.execute('''
        SELECT path, size, timestamp
        FROM events
        WHERE event_type = 'CREATE'
          AND size > 1073741824  -- 1GB
          AND timestamp >= datetime('now', '-7 days')
        ORDER BY size DESC
        LIMIT 10
    ''')
    
    large_files = cursor.fetchall()
    if large_files:
        anomalies.append({
            'type': 'large_files',
            'description': 'Arquivos grandes criados recentemente',
            'data': large_files
        })
    
    # 3. Padrão suspeito de acessos
    cursor = conn.execute('''
        SELECT 
            path,
            COUNT(*) as access_count
        FROM events
        WHERE timestamp >= datetime('now', '-1 day')
        GROUP BY path
        HAVING access_count > 100
        ORDER BY access_count DESC
        LIMIT 20
    ''')
    
    hot_files = cursor.fetchall()
    if hot_files:
        anomalies.append({
            'type': 'hot_files',
            'description': 'Arquivos com alto acesso recentemente',
            'data': hot_files
        })
    
    conn.close()
    return anomalies


def format_output(data, format='table'):
    """Formata saída"""
    if format == 'json':
        return json.dumps(data, indent=2)
    
    if isinstance(data, list):
        if not data:
            return "Nenhum resultado."
        
        # Table format
        headers = data[0].keys()
        col_widths = {h: len(h) for h in headers}
        
        for row in data:
            for h in headers:
                col_widths[h] = max(col_widths[h], len(str(row.get(h, ''))))
        
        # Header
        header = ' | '.join(h.ljust(col_widths[h]) for h in headers)
        separator = '-+-'.join('-' * col_widths[h] for h in headers)
        
        result = f"{header}\n{separator}\n"
        
        # Rows
        for row in data[:20]:  # Limitar a 20 linhas
            result += ' | '.join(str(row.get(h, '')).ljust(col_widths[h]) for h in headers) + '\n'
        
        return result
    
    elif isinstance(data, dict):
        # Key-value format
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"\n{key}:")
                for k, v in value.items():
                    lines.append(f"  {k}: {v}")
            elif isinstance(value, list):
                lines.append(f"\n{key}:")
                for item in value:
                    lines.append(f"  {item}")
            else:
                lines.append(f"{key}: {value}")
        
        return '\n'.join(lines)
    
    return str(data)


def main():
    parser = argparse.ArgumentParser(
        description='Consulta ao banco de monitoramento de arquivos'
    )
    
    # Comandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Comando: events
    events_parser = subparsers.add_parser('events', help='Consultar eventos')
    events_parser.add_argument('--since', help='Data/hora inicial (ISO format)')
    events_parser.add_argument('--until', help='Data/hora final (ISO format)')
    events_parser.add_argument('--type', help='Tipo de evento (CREATE, DELETE, MODIFY, etc.)')
    events_parser.add_argument('--path', help='Filtrar por caminho')
    events_parser.add_argument('--limit', type=int, default=100, help='Limite de resultados')
    events_parser.add_argument('--format', choices=['table', 'json'], default='table')
    
    # Comando: stats
    stats_parser = subparsers.add_parser('stats', help='Estatísticas')
    stats_parser.add_argument('--date', help='Data (YYYY-MM-DD)')
    stats_parser.add_argument('--format', choices=['table', 'json'], default='table')
    
    # Comando: baseline
    baseline_parser = subparsers.add_parser('baseline', help='Baseline')
    baseline_parser.add_argument('--path', help='Filtrar por caminho')
    baseline_parser.add_argument('--limit', type=int, default=100, help='Limite de resultados')
    baseline_parser.add_argument('--format', choices=['table', 'json'], default='table')
    
    # Comando: anomalies
    anomaly_parser = subparsers.add_parser('anomalies', help='Detectar anomalias')
    anomaly_parser.add_argument('--threshold', type=int, default=50, help='Limiar para detecção')
    anomaly_parser.add_argument('--format', choices=['table', 'json'], default='table')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'events':
            data = query_events(args)
        elif args.command == 'stats':
            data = get_stats(args)
        elif args.command == 'baseline':
            data = get_baseline(args)
        elif args.command == 'anomalies':
            data = detect_anomalies(args)
        else:
            parser.print_help()
            return
        
        print(format_output(data, args.format))
    
    except sqlite3.OperationalError as e:
        print(f"Erro: Banco de dados não encontrado. Execute o daemon primeiro.")
        print(f"Detalhes: {e}")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == '__main__':
    main()