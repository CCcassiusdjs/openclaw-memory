"""
LSA Lab Platform - Backend API
FastAPI application for laboratory management with telemetry and terminal
"""

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any, AsyncGenerator
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from jose import jwt, JWTError
import hashlib
import asyncio
import json
import os
import subprocess
import aiofiles
import paramiko
import httpx
from dataclasses import dataclass
from collections import defaultdict
import psutil

# Settings
class Settings(BaseSettings):
    database_url: str = "postgresql://ardupilot:ardupilot123@10.10.20.13/platform"
    redis_url: str = "redis://10.10.20.11:6379"
    mqtt_broker: str = "10.10.20.11"
    mqtt_port: int = 1883
    jwt_secret: str = "lsa-lab-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    
    # Cluster nodes
    t620_host: str = "10.10.20.11"
    t630a_host: str = "10.10.20.12"
    t630b_host: str = "10.10.20.13"
    cluster_user: str = "cassiusdjs"
    cluster_pass: str = "230612"
    
    # iDRAC
    idrac_t620: str = "192.168.10.11"
    idrac_t630a: str = "192.168.10.12"
    idrac_t630b: str = "192.168.10.13"
    
    # Jetson Door Controller
    jetson_door_url: str = "http://192.168.2.117:5000"
    jetson_admin_user: str = "celebro"
    jetson_admin_pass: str = "l@bls@25"
    
    class Config:
        env_file = ".env"

settings = Settings()

# App
app = FastAPI(
    title="LSA Lab Platform",
    description="Centralized management for LSA Laboratory",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# ==================== MODELS ====================

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str
    role: str = "user"

class User(UserBase):
    id: UUID
    role: str
    environment: Optional[Dict[str, Any]] = None
    created_at: datetime
    last_login: Optional[datetime] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

# Telemetry Models
class NodeMetrics(BaseModel):
    hostname: str
    cpu_percent: float
    memory_percent: float
    memory_used: float
    memory_total: float
    disk_percent: float
    disk_used: float
    disk_total: float
    network_in: float
    network_out: float
    load_avg: List[float]
    uptime_seconds: int
    temperature: Optional[float] = None
    fans: Optional[List[Dict[str, Any]]] = None

class ServiceStatus(BaseModel):
    name: str
    stack: str
    replicas: str
    image: str
    ports: List[str]
    status: str
    created: Optional[str] = None

class iDRACStatus(BaseModel):
    hostname: str
    ip: str
    status: str
    temperature: Optional[float] = None
    fans: Optional[List[Dict[str, Any]]] = None
    power: Optional[float] = None

class ClusterHealth(BaseModel):
    status: str
    nodes_total: int
    nodes_healthy: int
    services_total: int
    services_healthy: int
    cpu_avg: float
    memory_avg: float
    disk_avg: float

class DoorStatus(BaseModel):
    status: str
    last_action: Optional[str] = None
    last_user: Optional[str] = None
    last_time: Optional[datetime] = None

class AccessLog(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    username: str
    action: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

class ConnectionString(BaseModel):
    service: str
    host: str
    port: int
    protocol: str
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    url: str
    description: str

class CommandResult(BaseModel):
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None

# ==================== IN-MEMORY DATABASE ====================

users_db: Dict[UUID, Dict] = {}
access_logs: List[Dict] = []
metrics_cache: Dict[str, Any] = {}
terminal_sessions: Dict[str, Dict] = {}

# ==================== HELPERS ====================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_token(user_id: UUID) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> Optional[UUID]:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return UUID(payload.get("sub"))
    except:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    user_id = decode_token(token)
    if not user_id or user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return User(**users_db[user_id])

async def get_sudo_user(user: User = Depends(get_current_user)) -> User:
    if user.role not in ["sudo", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

# SSH Client for remote commands
class SSHClient:
    def __init__(self, host: str, user: str = settings.cluster_user, password: str = settings.cluster_pass):
        self.host = host
        self.user = user
        self.password = password
        self.client = None
    
    async def __aenter__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.user, password=self.password)
        return self
    
    async def __aexit__(self, *args):
        if self.client:
            self.client.close()
    
    async def run(self, command: str) -> tuple[str, str, int]:
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode(), stdout.channel.recv_exit_status()

# ==================== INITIALIZATION ====================

def init_db():
    admin_id = uuid4()
    users_db[admin_id] = {
        "id": admin_id,
        "username": "admin",
        "email": "admin@lsa.lab",
        "password_hash": hash_password("lsa@dm1n"),
        "role": "sudo",
        "environment": {},
        "created_at": datetime.utcnow(),
        "last_login": None
    }
    
    demo_id = uuid4()
    users_db[demo_id] = {
        "id": demo_id,
        "username": "demo",
        "email": "demo@lsa.lab",
        "password_hash": hash_password("demo123"),
        "role": "user",
        "environment": {},
        "created_at": datetime.utcnow(),
        "last_login": None
    }

init_db()

# ==================== AUTH ROUTES ====================

@app.post("/api/auth/login", response_model=Token)
async def login(data: UserLogin):
    for user in users_db.values():
        if user["username"] == data.username and user["password_hash"] == hash_password(data.password):
            user["last_login"] = datetime.utcnow()
            access_logs.append({
                "id": uuid4(),
                "user_id": user["id"],
                "username": user["username"],
                "action": "login",
                "timestamp": datetime.utcnow(),
                "details": {"ip": "web"}
            })
            return Token(
                access_token=create_token(user["id"]),
                user=User(**user)
            )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(user: User = Depends(get_current_user)):
    access_logs.append({
        "id": uuid4(),
        "user_id": user.id,
        "username": user.username,
        "action": "logout",
        "timestamp": datetime.utcnow()
    })
    return {"message": "Logged out"}

@app.get("/api/auth/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    return user

# ==================== USER MANAGEMENT ====================

@app.get("/api/users", response_model=List[User])
async def list_users(admin: User = Depends(get_sudo_user)):
    return [User(**u) for u in users_db.values()]

@app.post("/api/users", response_model=User)
async def create_user(data: UserCreate, admin: User = Depends(get_sudo_user)):
    if any(u["username"] == data.username for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = uuid4()
    users_db[user_id] = {
        "id": user_id,
        "username": data.username,
        "email": data.email,
        "password_hash": hash_password(data.password),
        "role": data.role,
        "environment": {},
        "created_at": datetime.utcnow(),
        "last_login": None
    }
    return User(**users_db[user_id])

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID, admin: User = Depends(get_sudo_user)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted"}

# ==================== CLUSTER METRICS ====================

async def get_node_metrics_ssh(host: str) -> NodeMetrics:
    """Get metrics from a node via SSH"""
    async with SSHClient(host) as ssh:
        # CPU usage
        cpu_out, _, _ = await ssh.run("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
        cpu_percent = float(cpu_out.strip() or 0)
        
        # Memory
        mem_out, _, _ = await ssh.run("free -m | awk 'NR==2{print $3,$2}'")
        mem_parts = mem_out.strip().split()
        memory_used = float(mem_parts[0]) if len(mem_parts) > 0 else 0
        memory_total = float(mem_parts[1]) if len(mem_parts) > 1 else 1
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        
        # Disk
        disk_out, _, _ = await ssh.run("df -h / | awk 'NR==2{print $3,$2}' | sed 's/G//g'")
        disk_parts = disk_out.strip().split()
        disk_used = float(disk_parts[0]) if len(disk_parts) > 0 else 0
        disk_total = float(disk_parts[1]) if len(disk_parts) > 1 else 1
        disk_percent = (disk_used / disk_total * 100) if disk_total > 0 else 0
        
        # Network
        net_out, _, _ = await ssh.run("cat /proc/net/dev | grep -E 'eno|bond|eth' | awk '{print $2,$10}'")
        net_parts = net_out.strip().split()
        network_in = float(net_parts[0]) / 1024 / 1024 if len(net_parts) > 0 else 0  # MB
        network_out = float(net_parts[1]) / 1024 / 1024 if len(net_parts) > 1 else 0  # MB
        
        # Load average
        load_out, _, _ = await ssh.run("cat /proc/loadavg | awk '{print $1,$2,$3}'")
        load_avg = [float(x) for x in load_out.strip().split()]
        
        # Uptime
        uptime_out, _, _ = await ssh.run("cat /proc/uptime | awk '{print $1}'")
        uptime_seconds = int(float(uptime_out.strip() or 0))
        
        # Temperature (try ipmitool)
        temp = None
        fans = None
        temp_out, _, code = await ssh.run("sudo ipmitool sensor | grep -E 'Temp|Fan' 2>/dev/null || true")
        if code == 0 and temp_out.strip():
            lines = temp_out.strip().split('\n')
            temps = []
            fans = []
            for line in lines:
                if 'Temp' in line:
                    try:
                        temp_val = float(line.split('|')[1].strip())
                        temps.append(temp_val)
                    except:
                        pass
                elif 'Fan' in line:
                    try:
                        parts = line.split('|')
                        fan_name = parts[0].strip()
                        fan_speed = int(float(parts[1].strip()))
                        fans.append({"name": fan_name, "speed": fan_speed})
                    except:
                        pass
            if temps:
                temp = max(temps)
        
        # Hostname
        hostname_out, _, _ = await ssh.run("hostname -s")
        hostname = hostname_out.strip()
        
        return NodeMetrics(
            hostname=hostname,
            cpu_percent=round(cpu_percent, 1),
            memory_percent=round(memory_percent, 1),
            memory_used=round(memory_used, 1),
            memory_total=round(memory_total, 1),
            disk_percent=round(disk_percent, 1),
            disk_used=round(disk_used, 1),
            disk_total=round(disk_total, 1),
            network_in=round(network_in, 2),
            network_out=round(network_out, 2),
            load_avg=load_avg,
            uptime_seconds=uptime_seconds,
            temperature=temp,
            fans=fans
        )

@app.get("/api/admin/metrics/realtime", response_model=Dict[str, NodeMetrics])
async def get_realtime_metrics(admin: User = Depends(get_sudo_user)):
    """Get real-time metrics from all cluster nodes"""
    metrics = {}
    
    # Get metrics from each node concurrently
    tasks = {
        "t620": get_node_metrics_ssh(settings.t620_host),
        "t630a": get_node_metrics_ssh(settings.t630a_host),
        "t630b": get_node_metrics_ssh(settings.t630b_host)
    }
    
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    
    for (name, _), result in zip(tasks.items(), results):
        if isinstance(result, Exception):
            metrics[name] = NodeMetrics(
                hostname=name,
                cpu_percent=0,
                memory_percent=0,
                memory_used=0,
                memory_total=0,
                disk_percent=0,
                disk_used=0,
                disk_total=0,
                network_in=0,
                network_out=0,
                load_avg=[0, 0, 0],
                uptime_seconds=0
            )
        else:
            metrics[name] = result
    
    return metrics

@app.get("/api/admin/metrics/history")
async def get_metrics_history(
    hours: int = 1,
    metric: str = "cpu",
    admin: User = Depends(get_sudo_user)
):
    """Get historical metrics from InfluxDB"""
    # TODO: Implement InfluxDB query
    # For now, return mock data
    import random
    from datetime import timedelta
    
    now = datetime.utcnow()
    data = []
    for i in range(hours * 60):  # 1 point per minute
        timestamp = now - timedelta(minutes=i)
        data.append({
            "time": timestamp.isoformat(),
            "t620": random.uniform(10, 50),
            "t630a": random.uniform(20, 60),
            "t630b": random.uniform(15, 45)
        })
    
    return {"metric": metric, "data": list(reversed(data))}

@app.get("/api/admin/nodes/detail")
async def get_nodes_detail(admin: User = Depends(get_sudo_user)):
    """Get detailed information about each node"""
    nodes = []
    
    # Get Docker node info from T620 (manager)
    async with SSHClient(settings.t620_host) as ssh:
        # Docker nodes - parse table format
        nodes_out, _, _ = await ssh.run("sudo docker node ls")
        
        # Skip header line
        lines = nodes_out.strip().split('\n')[1:]
        
        for line in lines:
            if line.strip():
                # Split by whitespace
                parts = line.split()
                if len(parts) >= 4:
                    # Docker node ls output format:
                    # ID [HOSTNAME] STATUS AVAILABILITY [MANAGER_STATUS] [ENGINE_VERSION]
                    # Note: ID may have * suffix for current node, which becomes a separate field
                    # Example: qmpujjbb... * t620 Ready Active Leader 29.3.0
                    
                    # Check if parts[1] is '*' (current node marker)
                    if parts[1] == '*':
                        hostname_raw = parts[2]
                        status = parts[3]
                        availability = parts[4]
                        manager_status_idx = 5
                    else:
                        hostname_raw = parts[1]
                        status = parts[2]
                        availability = parts[3]
                        manager_status_idx = 4
                    
                    # Remove domain suffix from hostname
                    hostname = hostname_raw.replace('*', '')
                    hostname_normalized = hostname.split('.')[0]
                    
                    # Determine role based on Manager Status
                    role = "worker"
                    if len(parts) > manager_status_idx:
                        manager_status = parts[manager_status_idx]
                        if manager_status in ["Leader", "Reachable", "Unreachable"]:
                            role = "manager"
                    
                    # Get IP based on hostname
                    ip_map = {
                        "t620": settings.t620_host,
                        "t630a": settings.t630a_host,
                        "t630b": settings.t630b_host
                    }
                    
                    nodes.append({
                        "hostname": hostname_normalized,
                        "status": status,
                        "availability": availability,
                        "role": role,
                        "ip": ip_map.get(hostname_normalized, "unknown")
                    })
    
    return nodes

@app.get("/api/admin/services/status")
async def get_services_status(admin: User = Depends(get_sudo_user)):
    """Get status of all Docker Swarm services"""
    services = []
    
    async with SSHClient(settings.t620_host) as ssh:
        # Get all services
        services_out, _, _ = await ssh.run("sudo docker service ls --format '{{.Name}}|{{.Replicas}}|{{.Image}}|{{.Ports}}'")
        
        for line in services_out.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) >= 3:
                    name = parts[0]
                    replicas = parts[1]
                    image = parts[2]
                    ports = parts[3].split(',') if len(parts) > 3 else []
                    
                    # Extract stack name
                    stack = name.split('_')[0] if '_' in name else 'default'
                    
                    services.append({
                        "name": name,
                        "stack": stack,
                        "replicas": replicas,
                        "image": image,
                        "ports": ports,
                        "status": "running" if replicas.startswith(replicas.split('/')[1]) else "degraded"
                    })
    
    return services

@app.get("/api/admin/idrac/status")
async def get_idrac_status(admin: User = Depends(get_sudo_user)):
    """Get iDRAC status for all servers"""
    results = []
    
    idracs = [
        ("t620", settings.idrac_t620),
        ("t630a", settings.idrac_t630a),
        ("t630b", settings.idrac_t630b)
    ]
    
    for hostname, ip in idracs:
        # Ping test
        proc = await asyncio.create_subprocess_shell(
            f"ping -c 1 -W 2 {ip}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        status = "online" if proc.returncode == 0 else "offline"
        
        results.append({
            "hostname": hostname,
            "ip": ip,
            "status": status
        })
    
    return results

@app.get("/api/admin/cluster/health", response_model=ClusterHealth)
async def get_cluster_health(admin: User = Depends(get_sudo_user)):
    """Get overall cluster health"""
    try:
        # Get real metrics
        metrics = await get_realtime_metrics(admin)
        
        nodes_healthy = sum(1 for m in metrics.values() if m.cpu_percent > 0)
        
        # Get services
        services = await get_services_status(admin)
        services_healthy = sum(1 for s in services if s["status"] == "running")
        
        # Calculate averages
        cpu_avg = sum(m.cpu_percent for m in metrics.values()) / len(metrics) if metrics else 0
        mem_avg = sum(m.memory_percent for m in metrics.values()) / len(metrics) if metrics else 0
        disk_avg = sum(m.disk_percent for m in metrics.values()) / len(metrics) if metrics else 0
        
        # Determine status
        if nodes_healthy == 3 and services_healthy == len(services):
            status = "healthy"
        elif nodes_healthy >= 2 and services_healthy >= len(services) * 0.5:
            status = "degraded"
        else:
            status = "critical"
        
        return ClusterHealth(
            status=status,
            nodes_total=3,
            nodes_healthy=nodes_healthy,
            services_total=len(services),
            services_healthy=services_healthy,
            cpu_avg=round(cpu_avg, 1),
            memory_avg=round(mem_avg, 1),
            disk_avg=round(disk_avg, 1)
        )
    except Exception as e:
        return ClusterHealth(
            status="unknown",
            nodes_total=3,
            nodes_healthy=0,
            services_total=0,
            services_healthy=0,
            cpu_avg=0,
            memory_avg=0,
            disk_avg=0
        )

# ==================== USER ENDPOINTS ====================

@app.get("/api/user/services")
async def get_user_services(user: User = Depends(get_current_user)):
    """Get services available to regular users"""
    return [
        {"name": "Jupyter Lab", "url": "http://10.10.20.11:8888", "status": "running", "description": "Jupyter Notebook environment"},
        {"name": "MLflow", "url": "http://10.10.20.11:5001", "status": "running", "description": "ML experiment tracking"},
        {"name": "MinIO", "url": "http://10.10.20.11:9002", "status": "running", "description": "Object storage"},
        {"name": "Grafana", "url": "http://10.10.20.11:3000", "status": "running", "description": "Monitoring dashboards"},
        {"name": "Portainer", "url": "http://10.10.20.11:9000", "status": "running", "description": "Container management"},
    ]

@app.get("/api/user/connections", response_model=List[ConnectionString])
async def get_user_connections(user: User = Depends(get_current_user)):
    """Get connection strings for services"""
    return [
        ConnectionString(
            service="PostgreSQL",
            host="10.10.20.13",
            port=5432,
            protocol="postgresql",
            database="ardupilot",
            username="ardupilot",
            password="***",
            url="postgresql://ardupilot:***@10.10.20.13:5432/ardupilot",
            description="PostgreSQL database for ArduPilot data"
        ),
        ConnectionString(
            service="InfluxDB",
            host="10.10.20.11",
            port=8086,
            protocol="http",
            url="http://10.10.20.11:8086",
            description="Time series database"
        ),
        ConnectionString(
            service="Redis",
            host="10.10.20.11",
            port=6379,
            protocol="redis",
            url="redis://10.10.20.11:6379",
            description="In-memory cache"
        ),
        ConnectionString(
            service="MQTT",
            host="10.10.20.11",
            port=1883,
            protocol="mqtt",
            url="mqtt://10.10.20.11:1883",
            description="Message broker"
        ),
    ]

@app.get("/api/user/status")
async def get_user_status(user: User = Depends(get_current_user)):
    """Get cluster status for users"""
    try:
        health = await get_cluster_health(user)
        return {
            "status": health.status,
            "message": {
                "healthy": "All systems operational",
                "degraded": "Some services may be slow",
                "critical": "Experiencing issues",
                "unknown": "Status unknown"
            }.get(health.status, "Unknown"),
            "services_available": health.services_healthy,
            "services_total": health.services_total
        }
    except:
        return {"status": "unknown", "message": "Unable to determine status", "services_available": 0, "services_total": 0}

# ==================== SECURITY ====================

# Jetson session
_jetson_session_cookie = None

async def get_jetson_session() -> str:
    """Login to Jetson and return session cookie"""
    global _jetson_session_cookie
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.jetson_door_url}/login",
            data={"username": settings.jetson_admin_user, "password": settings.jetson_admin_pass},
            follow_redirects=False
        )
        if resp.status_code == 302:
            _jetson_session_cookie = resp.cookies.get("session")
    return _jetson_session_cookie

async def call_jetson_api(endpoint: str, method: str = "GET") -> Dict:
    """Call Jetson door API"""
    global _jetson_session_cookie
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        cookies = {"session": _jetson_session_cookie} if _jetson_session_cookie else None
        
        if method == "POST":
            resp = await client.post(f"{settings.jetson_door_url}{endpoint}", cookies=cookies)
        else:
            resp = await client.get(f"{settings.jetson_door_url}{endpoint}", cookies=cookies)
        
        if resp.status_code == 401 or resp.status_code == 302:
            await get_jetson_session()
            cookies = {"session": _jetson_session_cookie}
            if method == "POST":
                resp = await client.post(f"{settings.jetson_door_url}{endpoint}", cookies=cookies)
            else:
                resp = await client.get(f"{settings.jetson_door_url}{endpoint}", cookies=cookies)
        
        return resp.json() if resp.status_code == 200 else {"error": resp.text}

@app.get("/api/admin/security/door")
async def get_door_status(admin: User = Depends(get_sudo_user)):
    """Get door status"""
    try:
        data = await call_jetson_api("/api/status")
        return {
            "status": "open" if data.get("aberta") else "closed",
            "last_action": "open" if data.get("aberta") else "close",
            "last_user": data.get("cartao", "unknown"),
            "last_time": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"status": "unknown", "error": str(e)}

@app.post("/api/admin/security/door/open")
async def open_door(admin: User = Depends(get_sudo_user)):
    """Open the door"""
    try:
        result = await call_jetson_api("/api/abrir", method="POST")
        
        access_logs.append({
            "id": uuid4(),
            "user_id": admin.id,
            "username": admin.username,
            "action": "door_open",
            "timestamp": datetime.utcnow(),
            "details": {"success": result.get("sucesso", False)}
        })
        
        if result.get("sucesso"):
            return {"message": "Door opened", "user": admin.username}
        else:
            raise HTTPException(status_code=500, detail=result.get("erro", "Unknown error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/security/door/close")
async def close_door(admin: User = Depends(get_sudo_user)):
    """Close the door"""
    try:
        result = await call_jetson_api("/api/fechar", method="POST")
        
        access_logs.append({
            "id": uuid4(),
            "user_id": admin.id,
            "username": admin.username,
            "action": "door_close",
            "timestamp": datetime.utcnow(),
            "details": {"success": result.get("sucesso", False)}
        })
        
        if result.get("sucesso"):
            return {"message": "Door closed", "user": admin.username}
        else:
            raise HTTPException(status_code=500, detail=result.get("erro", "Unknown error"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/security/sessions")
async def get_active_sessions(admin: User = Depends(get_sudo_user)):
    """Get active sessions count"""
    # Count logged-in users in the last hour
    now = datetime.utcnow()
    active = sum(1 for u in users_db.values() if u.get("last_login") and (now - u["last_login"]).total_seconds() < 3600)
    return {"count": active}

@app.get("/api/admin/security/logs")
async def get_security_logs(limit: int = 50, admin: User = Depends(get_sudo_user)):
    """Get security logs"""
    return [
        {
            "id": str(log["id"]),
            "username": log.get("username", "unknown"),
            "action": log["action"],
            "timestamp": log["timestamp"].isoformat(),
            "details": log.get("details")
        }
        for log in access_logs[-limit:]
    ]

@app.get("/api/admin/security/failed-logins")
async def get_failed_logins(admin: User = Depends(get_sudo_user)):
    """Get failed login attempts in the last 24h"""
    now = datetime.utcnow()
    failed = [
        log for log in access_logs
        if log["action"] == "login_failed" and (now - log["timestamp"]).total_seconds() < 86400
    ]
    return {"count": len(failed), "attempts": failed[-10:]}

# ==================== TERMINAL (xterm.js compatible) ====================

class TerminalSession:
    def __init__(self, session_id: str, host: str):
        self.session_id = session_id
        self.host = host
        self.client = None
        self.channel = None
    
    async def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=settings.cluster_user, password=settings.cluster_pass)
        self.channel = self.client.invoke_shell(term='xterm-256color')
        self.channel.resize(80, 24)
    
    async def send(self, data: str):
        if self.channel:
            self.channel.send(data)
    
    async def recv(self, size: int = 1024) -> bytes:
        if self.channel and self.channel.recv_ready():
            return self.channel.recv(size)
        return b''
    
    async def resize(self, cols: int, rows: int):
        if self.channel:
            self.channel.resize_pty(width=cols, height=rows)
    
    def close(self):
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()

@app.websocket("/api/terminal/{host}")
async def terminal_websocket(websocket: WebSocket, host: str):
    """WebSocket terminal to cluster nodes (admin only)"""
    # Wait for auth token
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return
    
    user_id = decode_token(token)
    if not user_id or user_id not in users_db:
        await websocket.close(code=4001)
        return
    
    user = User(**users_db[user_id])
    if user.role not in ["sudo", "admin"]:
        await websocket.close(code=4003)
        return
    
    # Map host to IP
    host_map = {
        "t620": settings.t620_host,
        "t630a": settings.t630a_host,
        "t630b": settings.t630b_host
    }
    
    if host not in host_map:
        await websocket.close(code=4004)
        return
    
    await websocket.accept()
    
    session = None
    try:
        session = TerminalSession(str(uuid4()), host_map[host])
        await session.connect()
        
        access_logs.append({
            "id": uuid4(),
            "user_id": user.id,
            "username": user.username,
            "action": "terminal_connect",
            "timestamp": datetime.utcnow(),
            "details": {"host": host}
        })
        
        async def read_output():
            while True:
                try:
                    data = await session.recv()
                    if data:
                        await websocket.send_bytes(data)
                    await asyncio.sleep(0.01)
                except:
                    break
        
        read_task = asyncio.create_task(read_output())
        
        while True:
            data = await websocket.receive()
            
            if data["type"] == "websocket.receive":
                if "text" in data:
                    await session.send(data["text"])
                elif "bytes" in data:
                    await session.send(data["bytes"].decode())
            elif data["type"] == "websocket.disconnect":
                break
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_text(f"\r\n\r\nError: {str(e)}\r\n")
    finally:
        if session:
            session.close()

# ==================== TELEMETRY STREAM ====================

@app.get("/api/admin/telemetry/stream")
async def telemetry_stream(admin: User = Depends(get_sudo_user)):
    """Server-Sent Events stream for real-time telemetry"""
    async def generate() -> AsyncGenerator[str, None]:
        while True:
            try:
                metrics = await get_realtime_metrics(admin)
                data = {name: m.dict() for name, m in metrics.items()}
                yield f"data: {json.dumps(data)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            await asyncio.sleep(2)  # Update every 2 seconds
    
    return StreamingResponse(generate(), media_type="text/event-stream")

# ==================== SERVICE ACTIONS ====================

@app.post("/api/admin/services/{service_name}/restart")
async def restart_service(service_name: str, admin: User = Depends(get_sudo_user)):
    """Restart a Docker Swarm service"""
    async with SSHClient(settings.t620_host) as ssh:
        stdout, stderr, code = await ssh.run(f"docker service update --force {service_name}")
        
        access_logs.append({
            "id": uuid4(),
            "user_id": admin.id,
            "username": admin.username,
            "action": "service_restart",
            "timestamp": datetime.utcnow(),
            "details": {"service": service_name, "success": code == 0}
        })
        
        if code == 0:
            return {"message": f"Service {service_name} restarted", "output": stdout}
        else:
            raise HTTPException(status_code=500, detail=stderr)

@app.post("/api/admin/services/{service_name}/scale/{replicas}")
async def scale_service(service_name: str, replicas: int, admin: User = Depends(get_sudo_user)):
    """Scale a Docker Swarm service"""
    async with SSHClient(settings.t620_host) as ssh:
        stdout, stderr, code = await ssh.run(f"docker service scale {service_name}={replicas}")
        
        access_logs.append({
            "id": uuid4(),
            "user_id": admin.id,
            "username": admin.username,
            "action": "service_scale",
            "timestamp": datetime.utcnow(),
            "details": {"service": service_name, "replicas": replicas, "success": code == 0}
        })
        
        if code == 0:
            return {"message": f"Service {service_name} scaled to {replicas}", "output": stdout}
        else:
            raise HTTPException(status_code=500, detail=stderr)

@app.get("/api/admin/services/{service_name}/logs")
async def get_service_logs(service_name: str, lines: int = 100, admin: User = Depends(get_sudo_user)):
    """Get logs from a Docker Swarm service"""
    async with SSHClient(settings.t620_host) as ssh:
        stdout, stderr, code = await ssh.run(f"docker service logs --tail {lines} {service_name}")
        
        if code == 0:
            return {"service": service_name, "logs": stdout}
        else:
            raise HTTPException(status_code=500, detail=stderr)

# ==================== HEALTH ====================

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/")
async def root():
    return {
        "name": "LSA Lab Platform",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)