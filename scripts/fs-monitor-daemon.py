#!/usr/bin/env python3
"""
fs-monitor-daemon.py - Daemon de monitoramento em tempo real com SQLite

Características:
- Monitoramento via inotify
- Armazenamento em SQLite para queries
- Batch processing para alta performance
- API REST para consultas
- Notificações configuráveis
"""

import os
import sys
import json
import time
import signal
import sqlite3
import logging
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List, Set
from concurrent.futures import ThreadPoolExecutor
import queue

# Configuração
WATCH_DIRS = os.environ.get('WATCH_DIRS', '/home/csilva').split(':')
LOG_DIR = Path(os.environ.get('LOG_DIR', '/home/csilva/.openclaw/workspace/logs/fs-monitor'))
DB_PATH = LOG_DIR / 'fs-monitor.db'
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', '100'))
FLUSH_INTERVAL = int(os.environ.get('FLUSH_INTERVAL', '5'))

# Criar diretório de logs
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class FileEvent:
    """Representa um evento de arquivo"""
    timestamp: str
    path: str
    event_type: str
    size: Optional[int] = None
    checksum: Optional[str] = None


class EventQueue:
    """Fila de eventos com batch processing"""
    
    def __init__(self, batch_size: int = BATCH_SIZE, flush_interval: int = FLUSH_INTERVAL):
        self.queue: queue.Queue = queue.Queue()
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.running = True
        self.worker: Optional[threading.Thread] = None
    
    def put(self, event: FileEvent) -> None:
        """Adiciona evento à fila"""
        self.queue.put(event)
    
    def start(self) -> None:
        """Inicia worker thread"""
        self.worker = threading.Thread(target=self._process_loop, daemon=True)
        self.worker.start()
    
    def stop(self) -> None:
        """Para worker thread"""
        self.running = False
        if self.worker:
            self.worker.join()
    
    def _process_loop(self) -> None:
        """Loop de processamento"""
        batch: List[FileEvent] = []
        last_flush = time.time()
        
        while self.running:
            try:
                # Tentar pegar evento
                event = self.queue.get(timeout=0.1)
                batch.append(event)
                
                # Flush se batch cheio
                if len(batch) >= self.batch_size:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()
            
            except queue.Empty:
                # Flush por intervalo
                if batch and (time.time() - last_flush) >= self.flush_interval:
                    self._flush_batch(batch)
                    batch = []
                    last_flush = time.time()
        
        # Flush final
        if batch:
            self._flush_batch(batch)
    
    def _flush_batch(self, batch: List[FileEvent]) -> None:
        """Processa batch de eventos"""
        if not batch:
            return
        
        # Salvar no banco
        save_events_to_db(batch)
        
        # Log
        event_counts = defaultdict(int)
        for event in batch:
            event_counts[event.event_type] += 1
        
        logger.info(f"Batch processado: {dict(event_counts)}")


class Database:
    """Gerenciador de banco de dados SQLite"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()
    
    def _init_db(self) -> None:
        """Inicializa banco de dados"""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                path TEXT NOT NULL,
                event_type TEXT NOT NULL,
                size INTEGER,
                checksum TEXT,
                processed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para queries rápidas
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON events(timestamp)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_path ON events(path)')
        self.conn.execute('CREATE INDEX IF NOT EXISTS idx_event_type ON events(event_type)')
        
        # Tabela de baseline
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS baseline (
                path TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                size INTEGER,
                checksum TEXT
            )
        ''')
        
        # Tabela de estatísticas
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                date TEXT PRIMARY KEY,
                total_events INTEGER DEFAULT 0,
                created INTEGER DEFAULT 0,
                deleted INTEGER DEFAULT 0,
                modified INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def insert_events(self, events: List[FileEvent]) -> None:
        """Insere eventos em batch"""
        cursor = self.conn.cursor()
        cursor.executemany(
            'INSERT INTO events (timestamp, path, event_type, size, checksum) VALUES (?, ?, ?, ?, ?)',
            [(e.timestamp, e.path, e.event_type, e.size, e.checksum) for e in events]
        )
        self.conn.commit()
    
    def update_baseline(self, path: str, timestamp: str, size: Optional[int] = None, 
                       checksum: Optional[str] = None) -> None:
        """Atualiza baseline"""
        self.conn.execute(
            '''INSERT OR REPLACE INTO baseline (path, timestamp, size, checksum) 
               VALUES (?, ?, ?, ?)''',
            (path, timestamp, size, checksum)
        )
        self.conn.commit()
    
    def get_events(self, since: Optional[str] = None, event_type: Optional[str] = None,
                  path_prefix: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Busca eventos com filtros"""
        query = 'SELECT * FROM events WHERE 1=1'
        params = []
        
        if since:
            query += ' AND timestamp >= ?'
            params.append(since)
        
        if event_type:
            query += ' AND event_type = ?'
            params.append(event_type)
        
        if path_prefix:
            query += ' AND path LIKE ?'
            params.append(f'{path_prefix}%')
        
        query += f' ORDER BY timestamp DESC LIMIT {limit}'
        
        cursor = self.conn.execute(query, params)
        columns = [desc[0] for desc in cursor.description]
        
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_stats(self, date: Optional[str] = None) -> Dict:
        """Retorna estatísticas"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor = self.conn.execute(
            'SELECT * FROM stats WHERE date = ?', (date,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                'date': row[0],
                'total_events': row[1],
                'created': row[2],
                'deleted': row[3],
                'modified': row[4]
            }
        
        # Calcular se não existir
        cursor = self.conn.execute(
            '''SELECT event_type, COUNT(*) FROM events 
               WHERE timestamp LIKE ? 
               GROUP BY event_type''',
            (f'{date}%',)
        )
        
        stats = {'date': date, 'total_events': 0, 'created': 0, 'deleted': 0, 'modified': 0}
        for row in cursor.fetchall():
            event_type, count = row
            stats['total_events'] += count
            if event_type in ('CREATE', 'CREATE_ISDIR'):
                stats['created'] += count
            elif event_type in ('DELETE', 'DELETE_ISDIR'):
                stats['deleted'] += count
            elif event_type == 'MODIFY':
                stats['modified'] += count
        
        # Salvar
        self.conn.execute(
            '''INSERT OR REPLACE INTO stats (date, total_events, created, deleted, modified)
               VALUES (?, ?, ?, ?, ?)''',
            (stats['date'], stats['total_events'], stats['created'], stats['deleted'], stats['modified'])
        )
        self.conn.commit()
        
        return stats
    
    def close(self) -> None:
        """Fecha conexão"""
        if self.conn:
            self.conn.close()


# Instância global do banco
db: Optional[Database] = None
event_queue: Optional[EventQueue] = None


def save_events_to_db(events: List[FileEvent]) -> None:
    """Salva eventos no banco"""
    global db
    if db:
        db.insert_events(events)


def calculate_checksum(path: str) -> Optional[str]:
    """Calcula checksum MD5 do arquivo"""
    try:
        result = subprocess.run(
            ['md5sum', path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.split()[0]
    except Exception as e:
        logger.error(f"Erro ao calcular checksum de {path}: {e}")
    return None


def get_file_info(path: str) -> Dict:
    """Retorna informações do arquivo"""
    try:
        stat = os.stat(path)
        return {
            'size': stat.st_size,
            'checksum': calculate_checksum(path) if stat.st_size < 10_000_000 else None
        }
    except Exception:
        return {'size': None, 'checksum': None}


def process_inotify_event(line: str) -> Optional[FileEvent]:
    """Processa linha do inotifywait"""
    try:
        parts = line.strip().split(' ')
        if len(parts) < 2:
            return None
        
        path = parts[0]
        event = parts[1]
        
        # Normalizar tipo de evento
        event_type = event.replace(',', '_')
        
        # Informações adicionais
        info = {}
        if os.path.exists(path) and not event.endswith('ISDIR'):
            info = get_file_info(path)
        
        return FileEvent(
            timestamp=datetime.now().isoformat(),
            path=path,
            event_type=event_type,
            size=info.get('size'),
            checksum=info.get('checksum')
        )
    
    except Exception as e:
        logger.error(f"Erro ao processar evento: {e}")
        return None


def monitor_loop(watch_dirs: List[str]) -> None:
    """Loop principal de monitoramento"""
    global event_queue
    
    logger.info(f"Iniciando monitoramento: {watch_dirs}")
    
    # Construir comando inotifywait
    cmd = [
        'inotifywait',
        '-r',           # recursivo
        '-m',           # monitor (não sai)
        '--format', '%w%f %e',
        '--exclude', r'\.git|\.cache|\.local|/tmp|\.log$'
    ]
    cmd.extend(watch_dirs)
    
    logger.info(f"Comando: {' '.join(cmd)}")
    
    # Executar inotifywait
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        logger.info("inotifywait iniciado")
        
        for line in iter(process.stdout.readline, ''):
            if not line:
                break
            
            event = process_inotify_event(line)
            if event and event_queue:
                event_queue.put(event)
    
    except Exception as e:
        logger.error(f"Erro no monitoramento: {e}")
        raise


def signal_handler(signum, frame) -> None:
    """Handler para sinais de término"""
    global event_queue, db
    
    logger.info(f"Recebido sinal {signum}, encerrando...")
    
    if event_queue:
        event_queue.stop()
    
    if db:
        db.close()
    
    sys.exit(0)


def main() -> None:
    """Função principal"""
    global db, event_queue
    
    logger.info("=== FS Monitor Daemon ===")
    logger.info(f"Diretórios: {WATCH_DIRS}")
    logger.info(f"Banco: {DB_PATH}")
    
    # Verificar dependências
    try:
        subprocess.run(['inotifywait', '--help'], capture_output=True)
    except FileNotFoundError:
        logger.error("inotifywait não encontrado. Instale: sudo dnf install inotifytools")
        sys.exit(1)
    
    # Inicializar banco
    db = Database(DB_PATH)
    logger.info("Banco de dados inicializado")
    
    # Inicializar fila de eventos
    event_queue = EventQueue()
    event_queue.start()
    logger.info("Fila de eventos iniciada")
    
    # Registrar handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Iniciar monitoramento
    try:
        monitor_loop(WATCH_DIRS)
    except KeyboardInterrupt:
        logger.info("Interrompido pelo usuário")
    finally:
        if event_queue:
            event_queue.stop()
        if db:
            db.close()
    
    logger.info("Daemon encerrado")


if __name__ == '__main__':
    main()