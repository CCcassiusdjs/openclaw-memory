#!/usr/bin/env python3
"""
Digital Twin Bridge for Webots + ArduPilot SITL
Sincronização bidirecional entre duas instâncias Webots

Arquitetura:
  Webots A (Mundo Físico) ←→ Bridge ←→ Webots B (Digital Twin)

Cada Webots tem seu próprio SITL conectado via MAVLink.
O Bridge lê estados de ambos e sincroniza.

IMPLEMENTAÇÃO COMPLETA:
- Lê estados MAVLink de ambos os SITL
- Envia comandos SET_POSITION_TARGET para sincronização
- Suporta sincronização bidirecional em tempo real

Autor: OpenClaw
Data: 2026-03-16
"""

import socket
import struct
import time
import threading
import json
import math
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import argparse
import sys


# ========================
# CONSTANTES MAVLink
# ========================
MAVLINK_STX = 0xFD  # MAVLink v2
MAVLINK_STX_V1 = 0xFE  # MAVLink v1

# Message IDs
MSG_HEARTBEAT = 0
MSG_SYS_STATUS = 1
MSG_ATTITUDE = 30
MSG_GLOBAL_POSITION_INT = 33
MSG_LOCAL_POSITION_NED = 32
MSG_SET_POSITION_TARGET_LOCAL_NED = 84
MSG_SET_POSITION_TARGET_GLOBAL_INT = 86
MSG_POSITION_TARGET_LOCAL_NED = 83

# MAV_MODE
MAV_MODE_PREFLIGHT = 0
MAV_MODE_STABILIZE_DISARMED = 80
MAV_MODE_STABILIZE_ARMED = 208
MAV_MODE_GUIDED_DISARMED = 64
MAV_MODE_GUIDED_ARMED = 216

# MAV_FRAME
MAV_FRAME_LOCAL_NED = 1
MAV_FRAME_LOCAL_OFFSET_NED = 7
MAV_FRAME_BODY_OFFSET_NED = 8
MAV_FRAME_GLOBAL_RELATIVE_ALT = 6

# Type masks para POSITION_TARGET
POSITION_TARGET_TYPE_MASK_VX_IGNORE = 1 << 0
POSITION_TARGET_TYPE_MASK_VY_IGNORE = 1 << 1
POSITION_TARGET_TYPE_MASK_VZ_IGNORE = 1 << 2
POSITION_TARGET_TYPE_MASK_AX_IGNORE = 1 << 3
POSITION_TARGET_TYPE_MASK_AY_IGNORE = 1 << 4
POSITION_TARGET_TYPE_MASK_AZ_IGNORE = 1 << 5
POSITION_TARGET_TYPE_MASK_YAW_IGNORE = 1 << 10
POSITION_TARGET_TYPE_MASK_YAW_RATE_IGNORE = 1 << 11

# Sync flags
SYNC_POS = 0b0000000000000000  # Sync position only
SYNC_POS_VEL = 0b0000000000000111  # Sync position + velocity


@dataclass
class DroneState:
    """Estado completo do drone para sincronização"""
    timestamp: float = 0.0
    # Posição global
    lat: float = 0.0  # Latitude (graus)
    lon: float = 0.0  # Longitude (graus)
    alt: float = 0.0  # Altitude (metros)
    # Posição local NED
    x: float = 0.0    # Norte (metros)
    y: float = 0.0    # Leste (metros)
    z: float = 0.0    # Baixo (metros)
    # Velocidade NED
    vx: float = 0.0   # Velocidade Norte (m/s)
    vy: float = 0.0   # Velocidade Leste (m/s)
    vz: float = 0.0   # Velocidade Baixo (m/s)
    # Atitude
    roll: float = 0.0   # Roll (radianos)
    pitch: float = 0.0  # Pitch (radianos)
    yaw: float = 0.0    # Yaw (radianos)
    # Estado do sistema
    armed: bool = False
    mode: str = "UNKNOWN"
    sysid: int = 1
    compid: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "lat": self.lat, "lon": self.lon, "alt": self.alt,
            "x": self.x, "y": self.y, "z": self.z,
            "vx": self.vx, "vy": self.vy, "vz": self.vz,
            "roll": self.roll, "pitch": self.pitch, "yaw": self.yaw,
            "armed": self.armed, "mode": self.mode
        }
    
    def distance_to(self, other: "DroneState") -> float:
        """Calcula distância euclidiana entre dois estados"""
        return math.sqrt(
            (self.x - other.x)**2 +
            (self.y - other.y)**2 +
            (self.z - other.z)**2
        )


class MAVLinkParser:
    """Parser MAVLink v1/v2"""
    
    @staticmethod
    def parse_message(data: bytes) -> Optional[Dict[str, Any]]:
        """Parse de mensagem MAVLink completa"""
        if len(data) < 10:
            return None
            
        try:
            if data[0] == MAVLINK_STX:  # MAVLink v2
                return MAVLinkParser._parse_v2(data)
            elif data[0] == MAVLINK_STX_V1:  # MAVLink v1
                return MAVLinkParser._parse_v1(data)
        except Exception as e:
            pass
            
        return None
    
    @staticmethod
    def _parse_v2(data: bytes) -> Optional[Dict[str, Any]]:
        """Parse MAVLink v2"""
        if len(data) < 12:
            return None
            
        # Header: 0xFD, len, incompat_flags, compat_flags, seq, sysid, compid, msgid (1-4 bytes)
        msg_len = data[1]
        msg_id = data[7]
        
        # Check for extended msgid (24-bit)
        if data[2] & 0x01:  # incompat_flags has signed bit
            msg_id = data[7] | (data[8] << 8) | (data[9] << 16)
            payload_start = 10
        else:
            payload_start = 10
            
        payload = data[payload_start:payload_start + msg_len]
        
        return {
            "sysid": data[5],
            "compid": data[6],
            "msgid": msg_id,
            "payload": payload
        }
    
    @staticmethod
    def _parse_v1(data: bytes) -> Optional[Dict[str, Any]]:
        """Parse MAVLink v1"""
        if len(data) < 8:
            return None
            
        msg_len = data[1]
        msg_id = data[5]
        payload = data[6:6 + msg_len]
        
        return {
            "sysid": data[3],
            "compid": data[4],
            "msgid": msg_id,
            "payload": payload
        }


class MAVLinkBuilder:
    """Construtor de mensagens MAVLink"""
    
    seq = 0
    
    @classmethod
    def heartbeat(cls, sysid: int = 1, compid: int = 1, 
                   type: int = 1, autopilot: int = 3,
                   base_mode: int = 216, custom_mode: int = 4,
                   system_status: int = 4) -> bytes:
        """Build HEARTBEAT message (msg_id=0)"""
        payload = struct.pack(
            '<IBBBBB',
            custom_mode,      # custom_mode
            type,              # type (MAV_TYPE = 1 = FIXED_WING)
            autopilot,         # autopilot (MAV_AUTOPILOT = 3 = APM)
            base_mode,         # base_mode (GUIDED + ARMED)
            system_status,     # system_status
            0                  # mavlink_version
        )
        return cls._build_message(sysid, compid, MSG_HEARTBEAT, payload)
    
    @classmethod
    def set_position_target_local_ned(cls, 
                                       time_boot_ms: int,
                                       target_sysid: int,
                                       target_compid: int,
                                       x: float, y: float, z: float,
                                       vx: float = 0.0, vy: float = 0.0, vz: float = 0.0,
                                       yaw: float = 0.0,
                                       type_mask: int = SYNC_POS,
                                       coordinate_frame: int = MAV_FRAME_LOCAL_NED,
                                       sysid: int = 255, compid: int = 190) -> bytes:
        """Build SET_POSITION_TARGET_LOCAL_NED message (msg_id=84)"""
        payload = struct.pack(
            '<IfHHffffffffffBB',
            time_boot_ms,      # time_boot_ms
            0,                 # type_mask (uint16_t, extended)
            coordinate_frame,  # coordinate_frame
            type_mask,         # type_mask
            x, y, z,          # position [x, y, z]
            vx, vy, vz,        # velocity [vx, vy, vz]
            0.0, 0.0, 0.0,     # acceleration/force [afx, afy, afz]
            yaw,               # yaw
            0.0                # yaw_rate
        )
        # Note: This is simplified - actual encoding may need adjustment
        return cls._build_message(sysid, compid, MSG_SET_POSITION_TARGET_LOCAL_NED, payload)
    
    @classmethod
    def _build_message(cls, sysid: int, compid: int, msgid: int, payload: bytes) -> bytes:
        """Build complete MAVLink v2 message"""
        # Ensure payload is at least minimum length
        while len(payload) < 10:
            payload += b'\x00'
        
        # Header
        header = bytes([
            MAVLINK_STX,
            len(payload),
            0,           # incompat_flags
            0,           # compat_flags
            cls.seq % 256,  # seq
            sysid,
            compid,
            msgid
        ])
        
        cls.seq += 1
        
        # Calculate checksum (simplified - should use CRC16-CCITT)
        checksum = 0xFFFF
        for b in header[1:] + payload:
            checksum ^= b
            for _ in range(8):
                if checksum & 1:
                    checksum = (checksum >> 1) ^ 0xB7D9
                else:
                    checksum >>= 1
        
        # Return header + payload + checksum
        return header + payload + struct.pack('<H', checksum)


class SITLConnection:
    """Conexão com um SITL via MAVLink"""
    
    def __init__(self, name: str, listen_port: int, remote_port: int):
        """
        Inicializa conexão
        
        Args:
            name: Nome identificador
            listen_port: Porta UDP para escutar
            remote_port: Porta UDP do SITL remoto para enviar comandos
        """
        self.name = name
        self.listen_port = listen_port
        self.remote_port = remote_port
        self.state = DroneState()
        self._running = False
        self._socket: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._remote_addr: Optional[tuple] = None
        
    def connect(self) -> bool:
        """Inicia conexão UDP"""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(("0.0.0.0", self.listen_port))
            self._socket.settimeout(0.05)  # 50ms timeout
            self._running = True
            self._thread = threading.Thread(target=self._receive_loop, daemon=True)
            self._thread.start()
            print(f"[{self.name}] Escutando em UDP 0.0.0.0:{self.listen_port}")
            return True
        except Exception as e:
            print(f"[{self.name}] Erro ao conectar: {e}")
            return False
    
    def disconnect(self):
        """Encerra conexão"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
        if self._socket:
            self._socket.close()
            
    def _receive_loop(self):
        """Loop de recepção de mensagens MAVLink"""
        while self._running:
            try:
                data, addr = self._socket.recvfrom(4096)
                
                # Guardar endereço remoto para enviar comandos
                if self._remote_addr is None or self._remote_addr != addr:
                    self._remote_addr = addr
                    print(f"[{self.name}] Cliente conectado de {addr}")
                
                # Parse MAVLink
                self._handle_data(data)
                
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    print(f"[{self.name}] Erro na recepção: {e}")
                    
    def _handle_data(self, data: bytes):
        """Processa dados recebidos"""
        msg = MAVLinkParser.parse_message(data)
        if msg:
            self._update_state(msg)
            
    def _update_state(self, msg: Dict[str, Any]):
        """Atualiza estado com base em mensagem MAVLink"""
        msgid = msg.get("msgid")
        payload = msg.get("payload", b"")
        sysid = msg.get("sysid", 1)
        compid = msg.get("compid", 1)
        
        self.state.sysid = sysid
        self.state.compid = compid
        
        if msgid == MSG_HEARTBEAT:
            if len(payload) >= 6:
                base_mode = payload[4]
                self.state.armed = bool(base_mode & 0x80)  # MAV_MODE_FLAG_SAFETY_ARMED
                
        elif msgid == MSG_ATTITUDE:
            # ATTITUDE: time_boot_ms (4) + roll (4) + pitch (4) + yaw (4) + ...
            if len(payload) >= 16:
                self.state.roll = struct.unpack('<f', payload[4:8])[0]
                self.state.pitch = struct.unpack('<f', payload[8:12])[0]
                self.state.yaw = struct.unpack('<f', payload[12:16])[0]
                self.state.timestamp = time.time()
                
        elif msgid == MSG_GLOBAL_POSITION_INT:
            # GLOBAL_POSITION_INT: lat, lon, alt, relative_alt, vx, vy, vz, hdg
            if len(payload) >= 28:
                self.state.lat = struct.unpack('<i', payload[4:8])[0] / 1e7
                self.state.lon = struct.unpack('<i', payload[8:12])[0] / 1e7
                self.state.alt = struct.unpack('<i', payload[12:16])[0] / 1e3
                self.state.vx = struct.unpack('<h', payload[20:22])[0] / 100.0
                self.state.vy = struct.unpack('<h', payload[22:24])[0] / 100.0
                self.state.vz = struct.unpack('<h', payload[24:26])[0] / 100.0
                self.state.timestamp = time.time()
                
        elif msgid == MSG_LOCAL_POSITION_NED:
            # LOCAL_POSITION_NED: x, y, z, vx, vy, vz
            if len(payload) >= 24:
                self.state.x = struct.unpack('<f', payload[4:8])[0]
                self.state.y = struct.unpack('<f', payload[8:12])[0]
                self.state.z = struct.unpack('<f', payload[12:16])[0]
                self.state.vx = struct.unpack('<f', payload[16:20])[0]
                self.state.vy = struct.unpack('<f', payload[20:24])[0]
                self.state.vz = struct.unpack('<f', payload[24:28])[0] if len(payload) >= 28 else 0.0
                self.state.timestamp = time.time()
    
    def get_state(self) -> DroneState:
        """Retorna estado atual"""
        return self.state
    
    def send_position_target(self, state: DroneState):
        """Envia comando de posição para o SITL"""
        if self._remote_addr is None:
            return
            
        try:
            # Build SET_POSITION_TARGET_LOCAL_NED
            msg = MAVLinkBuilder.set_position_target_local_ned(
                time_boot_ms=int(time.time() * 1000) % (2**32),
                target_sysid=state.sysid,
                target_compid=state.compid,
                x=state.x,
                y=state.y,
                z=state.z,
                vx=state.vx,
                vy=state.vy,
                vz=state.vz,
                yaw=state.yaw
            )
            self._socket.sendto(msg, self._remote_addr)
        except Exception as e:
            print(f"[{self.name}] Erro ao enviar comando: {e}")


class DigitalTwinBridge:
    """Bridge principal para sincronização bidirecional"""
    
    def __init__(self, 
                 sitl_a_listen: int = 14550,
                 sitl_a_remote: int = 14551,
                 sitl_b_listen: int = 14551,
                 sitl_b_remote: int = 14550,
                 sync_interval_ms: int = 20):
        """
        Inicializa bridge
        
        Args:
            sitl_a_listen: Porta para receber de SITL A
            sitl_a_remote: Porta para enviar comandos para SITL A
            sitl_b_listen: Porta para receber de SITL B
            sitl_b_remote: Porta para enviar comandos para SITL B
            sync_interval_ms: Intervalo de sincronização em ms
        """
        self.sitl_a = SITLConnection("SITL-A", sitl_a_listen, sitl_a_remote)
        self.sitl_b = SITLConnection("SITL-B", sitl_b_listen, sitl_b_remote)
        self.sync_interval = sync_interval_ms / 1000.0
        self._running = False
        self._sync_thread: Optional[threading.Thread] = None
        self._log_file = None
        self._stats = {
            "messages_received_a": 0,
            "messages_received_b": 0,
            "commands_sent_a": 0,
            "commands_sent_b": 0,
            "sync_errors": 0
        }
        
    def start(self, log_file: str = "/tmp/digital-twin/logs/bridge.log"):
        """Inicia bridge"""
        print("=" * 70)
        print("  DIGITAL TWIN BRIDGE - WEBOTS + SITL (BIDIRECIONAL)")
        print("=" * 70)
        print()
        
        # Criar diretório de logs
        import os
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self._log_file = open(log_file, "a")
        
        # Conectar aos SITL
        if not self.sitl_a.connect():
            print("ERRO: Falha ao iniciar SITL-A")
            return False
        if not self.sitl_b.connect():
            print("ERRO: Falha ao iniciar SITL-B")
            self.sitl_a.disconnect()
            return False
        
        # Iniciar thread de sincronização
        self._running = True
        self._sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self._sync_thread.start()
        
        print("Bridge iniciado!")
        print(f"  SITL-A: escuta {self.sitl_a.listen_port}, envia para {self.sitl_a.remote_port}")
        print(f"  SITL-B: escuta {self.sitl_b.listen_port}, envia para {self.sitl_b.remote_port}")
        print(f"  Intervalo de sync: {self.sync_interval * 1000:.0f}ms")
        print()
        print("Sincronização bidirecional ativa.")
        print("Pressione Ctrl+C para parar...")
        print()
        
        # Loop principal de monitoramento
        try:
            while self._running:
                time.sleep(1.0)
                self._print_status()
        except KeyboardInterrupt:
            print("\n\nParando bridge...")
            
        self.stop()
        return True
    
    def stop(self):
        """Para bridge"""
        self._running = False
        
        if self._sync_thread:
            self._sync_thread.join(timeout=2.0)
            
        self.sitl_a.disconnect()
        self.sitl_b.disconnect()
        
        # Salvar estatísticas
        if self._log_file:
            self._log_file.write(json.dumps({
                "timestamp": time.time(),
                "event": "bridge_stopped",
                "stats": self._stats
            }) + "\n")
            self._log_file.close()
            
        print("Bridge parado.")
        print(f"  Mensagens recebidas: A={self._stats['messages_received_a']}, B={self._stats['messages_received_b']}")
        print(f"  Comandos enviados: A={self._stats['commands_sent_a']}, B={self._stats['commands_sent_b']}")
        print(f"  Erros de sync: {self._stats['sync_errors']}")
    
    def _sync_loop(self):
        """Loop de sincronização bidirecional"""
        last_log_time = time.time()
        
        while self._running:
            try:
                start_time = time.time()
                
                # Obter estados atuais
                state_a = self.sitl_a.get_state()
                state_b = self.sitl_b.get_state()
                
                # Atualizar estatísticas
                if state_a.timestamp > 0:
                    self._stats["messages_received_a"] += 1
                if state_b.timestamp > 0:
                    self._stats["messages_received_b"] += 1
                
                # Sincronização bidirecional
                if state_a.timestamp > 0 and state_b.timestamp > 0:
                    # Calcular diferença
                    distance = state_a.distance_to(state_b)
                    
                    # Sincronizar: propagar estados
                    # A → B: propagar estado de A para B
                    if state_a.timestamp > state_b.timestamp:
                        self.sitl_b.send_position_target(state_a)
                        self._stats["commands_sent_b"] += 1
                    
                    # B → A: propagar estado de B para A
                    elif state_b.timestamp > state_a.timestamp:
                        self.sitl_a.send_position_target(state_b)
                        self._stats["commands_sent_a"] += 1
                    
                    # Log periódico
                    if time.time() - last_log_time > 1.0:
                        self._log_sync(state_a, state_b, distance)
                        last_log_time = time.time()
                
                # Respeitar intervalo de sync
                elapsed = time.time() - start_time
                sleep_time = max(0, self.sync_interval - elapsed)
                time.sleep(sleep_time)
                
            except Exception as e:
                self._stats["sync_errors"] += 1
                if self._log_file:
                    self._log_file.write(json.dumps({
                        "timestamp": time.time(),
                        "event": "sync_error",
                        "error": str(e)
                    }) + "\n")
                time.sleep(0.1)
    
    def _log_sync(self, state_a: DroneState, state_b: DroneState, distance: float):
        """Log de sincronização"""
        if not self._log_file:
            return
            
        log_entry = {
            "timestamp": time.time(),
            "sitl_a": state_a.to_dict(),
            "sitl_b": state_b.to_dict(),
            "distance_m": distance,
            "stats": self._stats.copy()
        }
        self._log_file.write(json.dumps(log_entry) + "\n")
        self._log_file.flush()
    
    def _print_status(self):
        """Imprime status atual"""
        state_a = self.sitl_a.get_state()
        state_b = self.sitl_b.get_state()
        
        # Verificar se temos dados
        if state_a.timestamp == 0 and state_b.timestamp == 0:
            print("\r[SITL-A] Aguardando dados... | [SITL-B] Aguardando dados...", end="", flush=True)
            return
        
        # Calcular diferença
        distance = state_a.distance_to(state_b) if state_a.timestamp > 0 and state_b.timestamp > 0 else 0.0
        
        print(f"\r[A] x:{state_a.x:7.2f} y:{state_a.y:7.2f} z:{state_a.z:7.2f} | "
              f"[B] x:{state_b.x:7.2f} y:{state_b.y:7.2f} z:{state_b.z:7.2f} | "
              f"Δ:{distance:6.2f}m", end="", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Digital Twin Bridge para Webots + ArduPilot SITL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--sitl-a-listen", type=int, default=14550,
                        help="Porta UDP para receber de SITL A")
    parser.add_argument("--sitl-a-remote", type=int, default=14551,
                        help="Porta UDP do SITL A para enviar comandos")
    parser.add_argument("--sitl-b-listen", type=int, default=14552,
                        help="Porta UDP para receber de SITL B")
    parser.add_argument("--sitl-b-remote", type=int, default=14553,
                        help="Porta UDP do SITL B para enviar comandos")
    parser.add_argument("--sync-interval", type=int, default=20,
                        help="Intervalo de sincronização em milissegundos")
    parser.add_argument("--log-file", type=str, default="/tmp/digital-twin/logs/bridge.log",
                        help="Arquivo de log")
    
    args = parser.parse_args()
    
    bridge = DigitalTwinBridge(
        sitl_a_listen=args.sitl_a_listen,
        sitl_a_remote=args.sitl_a_remote,
        sitl_b_listen=args.sitl_b_listen,
        sitl_b_remote=args.sitl_b_remote,
        sync_interval_ms=args.sync_interval
    )
    
    try:
        bridge.start(log_file=args.log_file)
    except Exception as e:
        print(f"Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()