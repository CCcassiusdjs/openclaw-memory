"""
LSA Lab Platform - Backend API
FastAPI application for laboratory management
"""

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from jose import jwt, JWTError
import hashlib
import asyncio
import json
import os

# Settings
class Settings(BaseSettings):
    database_url: str = "postgresql://ardupilot:ardupilot123@10.10.20.13/platform"
    redis_url: str = "redis://10.10.20.11:6379"
    mqtt_broker: str = "10.10.20.11"
    mqtt_port: int = 1883
    jwt_secret: str = "lsa-lab-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    jetson_host: str = "192.168.2.50"
    jetson_user: str = "automation"
    jetson_pass: str = "automation"
    
    class Config:
        env_file = ".env"

settings = Settings()

# App
app = FastAPI(
    title="LSA Lab Platform",
    description="Centralized management for LSA Laboratory",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Models
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "user"

class User(UserBase):
    id: UUID
    role: str
    environment: Optional[Dict[str, Any]] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WidgetBase(BaseModel):
    type: str
    position: Dict[str, int]
    config: Optional[Dict[str, Any]] = None

class Widget(WidgetBase):
    id: UUID
    user_id: UUID
    created_at: datetime

class AccessLog(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None

class DoorStatus(BaseModel):
    status: str  # "open", "closed", "unknown"
    last_action: Optional[str] = None
    last_user: Optional[str] = None
    last_time: Optional[datetime] = None
    lockout_remaining: int = 0

class ClusterNode(BaseModel):
    hostname: str
    status: str
    availability: str
    role: str
    resources: Optional[Dict[str, Any]] = None

class ClusterService(BaseModel):
    name: str
    replicas: str
    image: str
    ports: Optional[List[str]] = None

class CommandResult(BaseModel):
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None

# In-memory database (replace with PostgreSQL)
users_db: Dict[UUID, Dict] = {}
widgets_db: Dict[UUID, Dict] = {}
access_logs: List[Dict] = []

# Helper functions
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
    if user.role != "sudo":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sudo access required")
    return user

# Initialize admin user
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
    
    # Create demo user
    demo_id = uuid4()
    users_db[demo_id] = {
        "id": demo_id,
        "username": "demo",
        "email": "demo@lsa.lab",
        "password_hash": hash_password("demo123"),
        "role": "user",
        "environment": {
            "widgets": [
                {"type": "cluster_status", "position": {"x": 0, "y": 0, "w": 6, "h": 4}},
                {"type": "door_control", "position": {"x": 6, "y": 0, "w": 3, "h": 4}},
                {"type": "cluster_metrics", "position": {"x": 9, "y": 0, "w": 3, "h": 4}}
            ]
        },
        "created_at": datetime.utcnow(),
        "last_login": None
    }

init_db()

# Routes

# Auth
@app.post("/api/auth/login", response_model=Token)
async def login(data: UserLogin):
    for user in users_db.values():
        if user["username"] == data.username and user["password_hash"] == hash_password(data.password):
            user["last_login"] = datetime.utcnow()
            access_logs.append({
                "id": uuid4(),
                "user_id": user["id"],
                "action": "login",
                "timestamp": datetime.utcnow(),
                "details": {"username": user["username"]}
            })
            return Token(access_token=create_token(user["id"]))
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.post("/api/auth/logout")
async def logout(user: User = Depends(get_current_user)):
    access_logs.append({
        "id": uuid4(),
        "user_id": user.id,
        "action": "logout",
        "timestamp": datetime.utcnow()
    })
    return {"message": "Logged out"}

@app.get("/api/auth/me", response_model=User)
async def me(user: User = Depends(get_current_user)):
    return user

# Users (sudo only)
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

@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: UUID, data: dict, admin: User = Depends(get_sudo_user)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].update(data)
    return User(**users_db[user_id])

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID, admin: User = Depends(get_sudo_user)):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted"}

# Dashboard
@app.get("/api/dashboard/widgets", response_model=List[Widget])
async def get_widgets(user: User = Depends(get_current_user)):
    return [Widget(**w) for w in widgets_db.values() if w["user_id"] == user.id]

@app.post("/api/dashboard/widgets", response_model=Widget)
async def create_widget(data: WidgetBase, user: User = Depends(get_current_user)):
    widget_id = uuid4()
    widgets_db[widget_id] = {
        "id": widget_id,
        "user_id": user.id,
        "type": data.type,
        "position": data.position,
        "config": data.config,
        "created_at": datetime.utcnow()
    }
    return Widget(**widgets_db[widget_id])

@app.put("/api/dashboard/widgets/{widget_id}", response_model=Widget)
async def update_widget(widget_id: UUID, data: WidgetBase, user: User = Depends(get_current_user)):
    if widget_id not in widgets_db or widgets_db[widget_id]["user_id"] != user.id:
        raise HTTPException(status_code=404, detail="Widget not found")
    widgets_db[widget_id].update({"type": data.type, "position": data.position, "config": data.config})
    return Widget(**widgets_db[widget_id])

@app.delete("/api/dashboard/widgets/{widget_id}")
async def delete_widget(widget_id: UUID, user: User = Depends(get_current_user)):
    if widget_id not in widgets_db or widgets_db[widget_id]["user_id"] != user.id:
        raise HTTPException(status_code=404, detail="Widget not found")
    del widgets_db[widget_id]
    return {"message": "Widget deleted"}

# Door Control - Integration with Jetson TK2
import httpx

JETSON_DOOR_URL = os.getenv("JETSON_DOOR_URL", "http://192.168.2.117:5000")
JETSON_ADMIN_USER = os.getenv("JETSON_ADMIN_USER", "celebro")
JETSON_ADMIN_PASS = os.getenv("JETSON_ADMIN_PASS", "l@bls@25")

# Session cache for Jetson auth
_jetson_session_cookie = None

async def get_jetson_session() -> str:
    """Login to Jetson and return session cookie"""
    global _jetson_session_cookie
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{JETSON_DOOR_URL}/login",
            data={"username": JETSON_ADMIN_USER, "password": JETSON_ADMIN_PASS},
            follow_redirects=False
        )
        if resp.status_code == 302:
            _jetson_session_cookie = resp.cookies.get("session")
    return _jetson_session_cookie

async def call_jetson_api(endpoint: str, method: str = "GET") -> Dict:
    """Call Jetson door API with authentication"""
    global _jetson_session_cookie
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        cookies = {"session": _jetson_session_cookie} if _jetson_session_cookie else None
        
        if method == "POST":
            resp = await client.post(f"{JETSON_DOOR_URL}{endpoint}", cookies=cookies)
        else:
            resp = await client.get(f"{JETSON_DOOR_URL}{endpoint}", cookies=cookies)
        
        # If unauthorized, re-login and retry
        if resp.status_code == 401 or resp.status_code == 302:
            await get_jetson_session()
            cookies = {"session": _jetson_session_cookie}
            if method == "POST":
                resp = await client.post(f"{JETSON_DOOR_URL}{endpoint}", cookies=cookies)
            else:
                resp = await client.get(f"{JETSON_DOOR_URL}{endpoint}", cookies=cookies)
        
        return resp.json() if resp.status_code == 200 else {"error": resp.text}

@app.get("/api/door/status", response_model=DoorStatus)
async def get_door_status(user: User = Depends(get_current_user)):
    try:
        data = await call_jetson_api("/api/status")
        return DoorStatus(
            status="open" if data.get("aberta") else "closed",
            last_action="open" if data.get("aberta") else "close",
            last_user=data.get("cartao", "unknown"),
            last_time=datetime.utcnow(),
            lockout_remaining=0
        )
    except Exception as e:
        return DoorStatus(
            status="unknown",
            last_action="error",
            last_user="system",
            last_time=datetime.utcnow(),
            lockout_remaining=0
        )

@app.post("/api/door/open")
async def open_door(user: User = Depends(get_current_user)):
    try:
        result = await call_jetson_api("/api/abrir", method="POST")
        success = result.get("sucesso", False)
        
        access_logs.append({
            "id": uuid4(),
            "user_id": user.id,
            "action": "door_open",
            "timestamp": datetime.utcnow(),
            "details": {"username": user.username, "success": success, "response": result}
        })
        
        if success:
            return {"message": "Porta aberta", "user": user.username, "details": result.get("respostas", [])}
        else:
            raise HTTPException(status_code=500, detail=result.get("erro", "Unknown error"))
    except Exception as e:
        access_logs.append({
            "id": uuid4(),
            "user_id": user.id,
            "action": "door_open_failed",
            "timestamp": datetime.utcnow(),
            "details": {"username": user.username, "error": str(e)}
        })
        raise HTTPException(status_code=500, detail=f"Erro ao abrir porta: {str(e)}")

@app.post("/api/door/close")
async def close_door(user: User = Depends(get_current_user)):
    try:
        result = await call_jetson_api("/api/fechar", method="POST")
        success = result.get("sucesso", False)
        
        access_logs.append({
            "id": uuid4(),
            "user_id": user.id,
            "action": "door_close",
            "timestamp": datetime.utcnow(),
            "details": {"username": user.username, "success": success, "response": result}
        })
        
        if success:
            return {"message": "Porta fechada", "user": user.username, "details": result.get("respostas", [])}
        else:
            raise HTTPException(status_code=500, detail=result.get("erro", "Unknown error"))
    except Exception as e:
        access_logs.append({
            "id": uuid4(),
            "user_id": user.id,
            "action": "door_close_failed",
            "timestamp": datetime.utcnow(),
            "details": {"username": user.username, "error": str(e)}
        })
        raise HTTPException(status_code=500, detail=f"Erro ao fechar porta: {str(e)}")

@app.get("/api/door/history", response_model=List[AccessLog])
async def get_door_history(limit: int = 50, user: User = Depends(get_current_user)):
    return [AccessLog(**l) for l in access_logs if "door" in l["action"]][-limit:]

# Cluster Management
@app.get("/api/cluster/nodes", response_model=List[ClusterNode])
async def get_cluster_nodes(user: User = Depends(get_current_user)):
    # TODO: Implement actual cluster query via Docker API
    return [
        ClusterNode(hostname="t620", status="Ready", availability="Active", role="Manager"),
        ClusterNode(hostname="t630a.cluster.local", status="Ready", availability="Active", role="Worker"),
        ClusterNode(hostname="t630b.cluster.local", status="Ready", availability="Active", role="Worker")
    ]

@app.get("/api/cluster/services", response_model=List[ClusterService])
async def get_cluster_services(user: User = Depends(get_current_user)):
    # TODO: Implement actual cluster query via Docker API
    return [
        ClusterService(name="ardupilot_grafana", replicas="1/1", image="grafana/grafana:latest", ports=["3000"]),
        ClusterService(name="ardupilot_postgres", replicas="1/1", image="postgres:15-alpine", ports=["5432"]),
        ClusterService(name="mlpipeline_jupyter", replicas="1/1", image="jupyter/tensorflow-notebook:latest", ports=["8888"])
    ]

@app.post("/api/cluster/scale/{service_name}")
async def scale_service(service_name: str, replicas: int, user: User = Depends(get_sudo_user)):
    # TODO: Implement actual Docker Swarm scaling
    access_logs.append({
        "id": uuid4(),
        "user_id": user.id,
        "action": "cluster_scale",
        "timestamp": datetime.utcnow(),
        "details": {"service": service_name, "replicas": replicas}
    })
    return {"message": f"Scaling {service_name} to {replicas}", "service": service_name, "replicas": replicas}

@app.get("/api/cluster/metrics")
async def get_cluster_metrics(user: User = Depends(get_current_user)):
    # TODO: Implement actual metrics from Prometheus/InfluxDB
    return {
        "nodes": {
            "t620": {"cpu": 15.2, "memory": 45.8, "disk": 62.3},
            "t630a": {"cpu": 25.4, "memory": 55.2, "disk": 48.7},
            "t630b": {"cpu": 18.9, "memory": 52.1, "disk": 55.3}
        },
        "total_containers": 14,
        "running_containers": 14
    }

# Terminal WebSocket
@app.websocket("/api/terminal/connect")
async def terminal_websocket(websocket: WebSocket, user: User = Depends(get_current_user)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # TODO: Implement actual terminal command execution
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        pass

# Health
@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

# Root
@app.get("/")
async def root():
    return {
        "name": "LSA Lab Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)