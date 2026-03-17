#!/usr/bin/env python3
"""
dt_bridge.py - Digital Twin Bidirectional Bridge
Sincroniza estados entre duas instâncias Gazebo/SITL via MAVLink.

Arquitetura:
  Ambiente A (Mundo Real) ◄──────► Ambiente B (Digital Twin)
       Gazebo #1                        Gazebo #2
       SITL #1 (SYSID 1)                SITL #2 (SYSID 2)
       UDP:14550                        UDP:14551
                 ▲           ▲
                 │           │
                 └─────┬─────┘
                       │
              dt_bridge.py
              (Bridge Python)
"""

import time
import threading
import logging
import argparse
import signal
import sys
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from queue import Queue, Empty

try:
    from pymavlink import mavutil
except ImportError:
    print("Erro: pymavlink não instalado.")
    print("Instale com: pip install pymavlink")
    sys.exit(1)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('DTBridge')


@dataclass
class DroneState:
    """Estado completo de um drone."""
    timestamp: float = 0.0
    
    # Posição (GLOBAL_POSITION_INT)
    lat: float = 0.0  # graus
    lon: float = 0.0  # graus
    alt: float = 0.0  # metros
    relative_alt: float = 0.0  # metros
    
    # Velocidade
    vx: float = 0.0  # m/s
    vy: float = 0.0  # m/s
    vz: float = 0.0  # m/s
    
    # Atitude (ATTITUDE)
    roll: float = 0.0  # radianos
    pitch: float = 0.0  # radianos
    yaw: float = 0.0  # radianos
    
    # Status
    armed: bool = False
    mode: str = ""
    sysid: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'position': {'lat': self.lat, 'lon': self.lon, 'alt': self.alt, 'relative_alt': self.relative_alt},
            'velocity': {'vx': self.vx, 'vy': self.vy, 'vz': self.vz},
            'attitude': {'roll': self.roll, 'pitch': self.pitch, 'yaw': self.yaw},
            'status': {'armed': self.armed, 'mode': self.mode, 'sysid': self.sysid}
        }


class DroneConnection:
    """Gerencia conexão MAVLink com uma instância de drone."""
    
    def __init__(self, name: str, port: int, sysid: int = 1):
        self.name = name
        self.port = port
        self.sysid = sysid
        self.connection: Optional[mavutil.mavlink_connection] = None
        self.state = DroneState(sysid=sysid)
        self.connected = False
        self._lock = threading.Lock()
        
    def connect(self) -> bool:
        """Conecta ao drone via MAVLink UDP."""
        try:
            url = f'udpin:0.0.0.0:{self.port}'
            logger.info(f"[{self.name}] Conectando em {url}...")
            self.connection = mavutil.mavlink_connection(url)
            return True
        except Exception as e:
            logger.error(f"[{self.name}] Erro ao conectar: {e}")
            return False
            
    def wait_heartbeat(self, timeout: float = 30.0) -> bool:
        """Aguarda heartbeat do drone."""
        if not self.connection:
            return False
            
        logger.info(f"[{self.name}] Aguardando heartbeat...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            msg = self.connection.recv_match(type='HEARTBEAT', blocking=True, timeout=1.0)
            if msg:
                self.connected = True
                self.state.sysid = msg.get_srcSystem()
                logger.info(f"[{self.name}] ✓ Conectado! SYSID={self.state.sysid}, Type={msg.type}")
                return True
                
        logger.error(f"[{self.name}] ✗ Timeout aguardando heartbeat")
        return False
        
    def update_state(self) -> Optional[DroneState]:
        """Lê e atualiza o estado atual do drone."""
        if not self.connection or not self.connected:
            return None
            
        with self._lock:
            # Lê GLOBAL_POSITION_INT
            msg = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
            if msg:
                self.state.lat = msg.lat / 1e7
                self.state.lon = msg.lon / 1e7
                self.state.alt = msg.alt / 1e3
                self.state.relative_alt = msg.relative_alt / 1e3
                self.state.vx = msg.vx / 100.0
                self.state.vy = msg.vy / 100.0
                self.state.vz = msg.vz / 100.0
                self.state.timestamp = time.time()
                
            # Lê ATTITUDE
            msg = self.connection.recv_match(type='ATTITUDE', blocking=False)
            if msg:
                self.state.roll = msg.roll
                self.state.pitch = msg.pitch
                self.state.yaw = msg.yaw
                
            # Lê HEARTBEAT para status
            msg = self.connection.recv_match(type='HEARTBEAT', blocking=False)
            if msg:
                self.state.armed = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                self.state.mode = mavutil.mode_string_v10(msg).split(':')[0] if msg.autopilot != 0 else "UNKNOWN"
                
        return self.state
        
    def send_position_target(self, state: DroneState):
        """Envia comando de posição alvo para o drone."""
        if not self.connection or not self.connected:
            return False
            
        with self._lock:
            try:
                # SET_POSITION_TARGET_GLOBAL_INT
                self.connection.mav.set_position_target_global_int_send(
                    int(time.time() * 1000),  # time_boot_ms
                    self.state.sysid,  # target_system
                    1,  # target_component
                    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
                    0b1111111111111000,  # type_mask (apenas posição)
                    int(state.lat * 1e7),  # lat_int
                    int(state.lon * 1e7),  # lon_int
                    state.relative_alt,  # alt
                    0, 0, 0,  # velocidade
                    0, 0, 0,  # aceleração
                    0, 0  # yaw, yaw_rate
                )
                return True
            except Exception as e:
                logger.error(f"[{self.name}] Erro ao enviar posição: {e}")
                return False
                
    def close(self):
        """Fecha a conexão."""
        if self.connection:
            self.connection.close()
        self.connected = False


class DigitalTwinBridge:
    """
    Bridge bidirecional entre dois ambientes de drone.
    
    Sincroniza estados entre Ambiente A (Mundo Real) e Ambiente B (Digital Twin).
    """
    
    def __init__(self, port_a: int = 14550, port_b: int = 14551, 
                 latency_threshold_ms: float = 50.0, 
                 sync_rate_hz: float = 50.0):
        """
        Inicializa o bridge.
        
        Args:
            port_a: Porta UDP do Ambiente A (Mundo Real)
            port_b: Porta UDP do Ambiente B (Digital Twin)
            latency_threshold_ms: Limite de latência para alertas
            sync_rate_hz: Taxa de sincronização (Hz)
        """
        self.drone_a = DroneConnection("Ambiente A", port_a, sysid=1)
        self.drone_b = DroneConnection("Ambiente B", port_b, sysid=2)
        
        self.latency_threshold_ms = latency_threshold_ms
        self.sync_interval = 1.0 / sync_rate_hz
        
        self.running = False
        self._stop_event = threading.Event()
        
        # Estatísticas
        self.stats = {
            'sync_count': 0,
            'latency_samples': [],
            'errors': 0,
            'start_time': None
        }
        
    def connect(self) -> bool:
        """Conecta a ambos os drones."""
        logger.info("=== Conectando aos ambientes ===")
        
        # Conecta A
        if not self.drone_a.connect():
            return False
        if not self.drone_a.wait_heartbeat(timeout=30):
            return False
            
        # Conecta B
        if not self.drone_b.connect():
            return False
        if not self.drone_b.wait_heartbeat(timeout=30):
            return False
            
        logger.info("✓ Ambos os ambientes conectados!")
        return True
        
    def _sync_loop(self):
        """Loop principal de sincronização."""
        last_sync = time.time()
        
        while self.running:
            loop_start = time.time()
            
            try:
                # Atualiza estados
                state_a = self.drone_a.update_state()
                state_b = self.drone_b.update_state()
                
                # Sincronização bidirecional
                if state_a and state_b:
                    # A → B
                    self.drone_b.send_position_target(state_a)
                    # B → A
                    self.drone_a.send_position_target(state_b)
                    
                    self.stats['sync_count'] += 1
                    
                # Mede latência
                loop_time = (time.time() - last_sync) * 1000  # ms
                last_sync = time.time()
                
                self.stats['latency_samples'].append(loop_time)
                if len(self.stats['latency_samples']) > 100:
                    self.stats['latency_samples'].pop(0)
                    
                # Alerta de latência alta
                if loop_time > self.latency_threshold_ms:
                    logger.warning(f"Latência alta: {loop_time:.1f}ms")
                else:
                    if self.stats['sync_count'] % 50 == 0:
                        avg = sum(self.stats['latency_samples']) / len(self.stats['latency_samples'])
                        logger.info(f"Sync #{self.stats['sync_count']} | Latência média: {avg:.1f}ms")
                        
            except Exception as e:
                logger.error(f"Erro no loop de sincronização: {e}")
                self.stats['errors'] += 1
                
            # Aguarda próximo ciclo
            elapsed = time.time() - loop_start
            if elapsed < self.sync_interval:
                time.sleep(self.sync_interval - elapsed)
                
    def run(self):
        """Inicia o bridge."""
        if not self.connect():
            logger.error("Falha ao conectar. Encerrando.")
            return
            
        self.running = True
        self.stats['start_time'] = time.time()
        
        logger.info(f"\n{'='*50}")
        logger.info("🔄 INICIANDO SINCRONIZAÇÃO BIDIRECIONAL")
        logger.info(f"  Ambiente A: UDP {self.drone_a.port} (SYSID {self.drone_a.sysid})")
        logger.info(f"  Ambiente B: UDP {self.drone_b.port} (SYSID {self.drone_b.sysid})")
        logger.info(f"  Taxa: {1/self.sync_interval:.0f}Hz | Latência alvo: <{self.latency_threshold_ms}ms")
        logger.info(f"{'='*50}\n")
        
        try:
            self._sync_loop()
        except KeyboardInterrupt:
            logger.info("\nInterrupção recebida. Encerrando...")
        finally:
            self.stop()
            
    def stop(self):
        """Para o bridge."""
        self.running = False
        self._stop_event.set()
        
        # Exibe estatísticas finais
        if self.stats['start_time'] and self.stats['sync_count'] > 0:
            duration = time.time() - self.stats['start_time']
            avg_latency = sum(self.stats['latency_samples']) / len(self.stats['latency_samples']) if self.stats['latency_samples'] else 0
            
            logger.info(f"\n{'='*50}")
            logger.info("📊 ESTATÍSTICAS FINAIS")
            logger.info(f"  Duração: {duration:.1f}s")
            logger.info(f"  Sincronizações: {self.stats['sync_count']}")
            logger.info(f"  Latência média: {avg_latency:.1f}ms")
            logger.info(f"  Erros: {self.stats['errors']}")
            logger.info(f"{'='*50}\n")
            
        # Fecha conexões
        self.drone_a.close()
        self.drone_b.close()
        logger.info("✓ Bridge encerrado.")


def main():
    parser = argparse.ArgumentParser(
        description='Digital Twin Bidirectional Bridge - Sincroniza dois ambientes de drone via MAVLink'
    )
    parser.add_argument('--port-a', type=int, default=14550,
                       help='Porta UDP do Ambiente A (default: 14550)')
    parser.add_argument('--port-b', type=int, default=14551,
                       help='Porta UDP do Ambiente B (default: 14551)')
    parser.add_argument('--latency', type=float, default=50.0,
                       help='Limite de latência para alertas em ms (default: 50)')
    parser.add_argument('--rate', type=float, default=50.0,
                       help='Taxa de sincronização em Hz (default: 50)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Output detalhado')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        
    bridge = DigitalTwinBridge(
        port_a=args.port_a,
        port_b=args.port_b,
        latency_threshold_ms=args.latency,
        sync_rate_hz=args.rate
    )
    
    # Handler para SIGINT/SIGTERM
    def signal_handler(sig, frame):
        logger.info("\nSinal de interrupção recebido...")
        bridge.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    bridge.run()


if __name__ == '__main__':
    main()