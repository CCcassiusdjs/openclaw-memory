# Digital Twin Architecture - Crazyflie Simulation

## Proposta de Pesquisa

**Objetivo:** Demonstrar conceito de Digital Twin usando Webots como gêmeo digital e simulador Python como "mundo físico", sincronizados em tempo real.

**Motivação:** Pesquisa acadêmica sem acesso a drone físico real.

---

## Arquitetura Proposta

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌─────────────────────────────┐     ┌─────────────────────────────┐      │
│   │      MUNDO FÍSICO           │     │      DIGITAL TWIN            │      │
│   │   (Simulador Python)        │     │      (Webots Crazyflie)      │      │
│   │                             │     │                             │      │
│   │  ┌─────────────────────┐   │     │  ┌─────────────────────┐    │      │
│   │  │  Physics Engine     │   │     │  │  Webots Physics     │    │      │
│   │  │  - PyBullet/NumPy    │   │     │  │  - ODE Engine       │    │      │
│   │  │  - Custom dynamics   │   │     │  │  - Crazyflie model  │    │      │
│   │  └─────────────────────┘   │     │  └─────────────────────┘    │      │
│   │           │                 │     │           │                 │      │
│   │           ▼                 │     │           ▼                 │      │
│   │  ┌─────────────────────┐   │     │  ┌─────────────────────┐    │      │
│   │  │  Sensor Model       │   │     │  │  Sensor Model       │    │      │
│   │  │  - IMU (gyro, accel)│   │     │  │  - IMU (Webots API) │    │      │
│   │  │  - Range finders    │   │     │  │  - Range finders    │    │      │
│   │  │  - GPS (simulated)  │   │     │  │  - GPS              │    │      │
│   │  └─────────────────────┘   │     │  └─────────────────────┘    │      │
│   │           │                 │     │           │                 │      │
│   │           ▼                 │     │           ▼                 │      │
│   │  ┌─────────────────────┐   │     │  ┌─────────────────────┐    │      │
│   │  │  State Vector       │   │     │  │  State Vector       │    │      │
│   │  │  [x, y, z,          │   │     │  │  [x, y, z,          │    │      │
│   │  │   roll, pitch, yaw, │   │     │  │   roll, pitch, yaw, │    │      │
│   │  │   vx, vy, vz,       │   │     │  │   vx, vy, vz,       │    │      │
│   │  │   ωx, ωy, ωz]       │   │     │  │   ωx, ωy, ωz]       │    │      │
│   │  └─────────────────────┘   │     │  └─────────────────────┘    │      │
│   │           │                 │     │           │                 │      │
│   └───────────┼─────────────────┘     └───────────┼─────────────────┘      │
│               │                                   │                        │
│               │         ┌───────────────┐         │                        │
│               └────────▶│   BRIDGE      │◀────────┘                        │
│               │         │   ZeroMQ/IPC   │                                  │
│               │         │   Protocol     │                                  │
│               │         └───────────────┘                                  │
│               │                 │                                          │
│               │                 ▼                                          │
│               │         ┌───────────────┐                                  │
│               │         │   SYNC LAYER  │                                  │
│               │         │ - State sync  │                                  │
│               │         │ - Event inject│                                  │
│               │         │ - Fault inject│                                  │
│               │         └───────────────┘                                  │
│               │                 │                                          │
│               ▼                 ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐     │
│   │                    VISUALIZATION / LOGGING                       │     │
│   │  - Real-time state comparison                                    │     │
│   │  - Error metrics (Δposition, Δorientation)                      │     │
│   │  - Event timeline                                                │     │
│   └─────────────────────────────────────────────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Componentes

### 1. Mundo Físico (Simulador Python)

**Propósito:** Simular o "drone real" com física própria

```python
# Estrutura proposta
class PhysicalWorld:
    """
    Simulador Python do mundo físico.
    Usa PyBullet ou física própria NumPy.
    """
    def __init__(self):
        self.physics_engine = PhysicsEngine()  # PyBullet ou custom
        self.drone_state = DroneState()
        self.sensors = SensorModel()
        
    def step(self, dt):
        """Avança simulação um passo"""
        self.physics_engine.step(dt)
        self.drone_state.update()
        self.sensors.read()
        
    def inject_fault(self, fault_type):
        """Injeta falhas (ex: SEU, I2C bus failure)"""
        pass
```

**Sensores simulados:**
- IMU (gyro, accel) com ruído e bias
- Range finders (front, left, right, back)
- GPS simulado (lat, lon, alt)
- Câmera (opcional)

### 2. Digital Twin (Webots)

**Propósito:** Réplica visual e de física do drone

```python
# Baseado no controlador Crazyflie existente
class DigitalTwinController:
    """
    Controlador Webots para o Digital Twin.
    Recebe comandos do bridge e atualiza estado.
    """
    def __init__(self, robot):
        self.robot = robot
        self.motors = self.init_motors()
        self.sensors = self.init_sensors()
        
    def sync_state(self, physical_state):
        """Sincroniza estado com mundo físico"""
        # Posição, orientação, velocidades
        pass
        
    def run(self):
        """Loop principal"""
        while self.robot.step(timestep) != -1:
            state = self.get_state()
            self.send_to_bridge(state)
            cmd = self.receive_from_bridge()
            self.apply_command(cmd)
```

### 3. Bridge de Comunicação

**Protocolo:** ZeroMQ ou IPC (Unix socket)

```python
# Mensagens
{
    "type": "state",
    "timestamp": 1234567890.123,
    "source": "physical",  # ou "digital"
    "data": {
        "position": [x, y, z],
        "orientation": [roll, pitch, yaw],
        "velocity": [vx, vy, vz],
        "angular_velocity": [wx, wy, wz],
        "sensors": {
            "imu": {"accel": [...], "gyro": [...]},
            "range": {"front": d1, "left": d2, ...},
            "gps": {"lat": ..., "lon": ..., "alt": ...}
        }
    }
}

{
    "type": "command",
    "timestamp": 1234567890.123,
    "source": "control",  # controlador externo
    "data": {
        "motor_power": [m1, m2, m3, m4],
        # ou
        "velocity": [vx, vy, vz, yaw_rate]
    }
}

{
    "type": "fault_inject",
    "timestamp": 1234567890.123,
    "fault": {
        "type": "sensor_noise",
        "sensor": "imu",
        "params": {"noise_std": 0.1}
    }
}
```

---

## Fluxo de Dados

```
┌─────────────┐     command      ┌─────────────┐
│   Control   │─────────────────▶│   Physical  │
│   (User)    │                  │   World     │
└─────────────┘                  └──────┬──────┘
      │                                 │
      │                                 │ state
      │                                 ▼
      │                          ┌─────────────┐
      │                          │   Bridge    │
      │                          │   (Sync)    │
      │                          └──────┬──────┘
      │                                 │
      │                                 │ state
      │                                 ▼
      │                          ┌─────────────┐
      │                          │   Digital   │
      │                          │   Twin      │
      │                          │  (Webots)   │
      │                          └─────────────┘
      │                                 │
      │◀──────── visualization ─────────┘
      │        (comparison)
```

---

## Cenários de Teste

### Cenário 1: Sincronização Básica
- Drone no mundo físico executa trajetória
- Digital Twin deve seguir a mesma trajetória
- Métrica: erro RMS de posição/orientação

### Cenário 2: Injeção de Falhas
- Injeta falha no mundo físico (ex: sensor ruidoso)
- Digital Twin continua normal (modelo ideal)
- Comparação mostra desvio causado pela falha

### Cenário 3: Controle em Loop Fechado
- Controlador usa estado do Digital Twin
- Comandos aplicados ao mundo físico
- Analisa se gêmeo digital melhora controle

### Cenário 4: Predição
- Digital Twin roda à frente no tempo
- Prediz estado futuro do mundo físico
- Compara predição com realização

---

## Implementação - Estrutura de Arquivos

```
digital-twin-crazyflie/
├── physical_world/
│   ├── __init__.py
│   ├── physics.py          # Motor de física (PyBullet/NumPy)
│   ├── drone_model.py      # Modelo dinâmico do Crazyflie
│   ├── sensors.py          # Modelos de sensores
│   └── faults.py           # Injeção de falhas
│
├── digital_twin/
│   ├── __init__.py
│   ├── webots_controller.py # Controlador Webots
│   ├── crazyflie_model.py   # Adapter para modelo Webots
│   └── sync.py              # Sincronização
│
├── bridge/
│   ├── __init__.py
│   ├── protocol.py          # Definição de mensagens
│   ├── zmq_bridge.py        # Bridge ZeroMQ
│   └── ipc_bridge.py        # Bridge IPC local
│
├── control/
│   ├── __init__.py
│   ├── pid_controller.py    # Controlador PID
│   ├── trajectory.py        # Gerador de trajetórias
│   └── fault_injector.py    # Interface de injeção
│
├── visualization/
│   ├── __init__.py
│   ├── live_plot.py         # Plot em tempo real
│   ├── state_comparison.py  # Comparação de estados
│   └── metrics.py           # Cálculo de métricas
│
├── experiments/
│   ├── scenario_1_sync.py
│   ├── scenario_2_faults.py
│   ├── scenario_3_control.py
│   └── scenario_4_prediction.py
│
├── config/
│   ├── drone_params.yaml    # Parâmetros do Crazyflie
│   ├── physics.yaml         # Configuração de física
│   └── network.yaml          # Configuração de rede
│
├── main.py                   # Entry point
└── requirements.txt
```

---

## Parâmetros do Crazyflie

```yaml
# config/drone_params.yaml
crazyflie:
  mass: 0.027  # kg
  arm_length: 0.046  # m (motor to motor / 2)
  motor_const: 2.88e-11  # thrust coefficient
  moment_const: 0.016  # moment coefficient
  
  # Moments of inertia (kg*m^2)
  Ixx: 1.395e-5
  Iyy: 1.395e-5
  Izz: 2.173e-5
  
  # Motor limits
  motor_min: 0
  motor_max: 600
  
  # Sensor noise
  imu:
    accel_noise_std: 0.01
    gyro_noise_std: 0.01
    accel_bias_range: [-0.05, 0.05]
    gyro_bias_range: [-0.01, 0.01]
    
  range_finder:
    noise_std: 0.01
    max_range: 2.0
    
  gps:
    noise_std: 0.1
    update_rate: 5  # Hz
```

---

## Próximos Passos

1. **Implementar mundo físico Python**
   - Modelo dinâmico do Crazyflie
   - Integração com PyBullet ou física própria
   
2. **Adaptar controlador Webots**
   - Comunicação com bridge
   - Sincronização de estado
   
3. **Implementar bridge ZeroMQ**
   - Protocolo de mensagens
   - Sincronização temporal
   
4. **Criar cenários de teste**
   - Validação de sincronização
   - Injeção de falhas

---

## Referências

- Webots Crazyflie: `/home/csilva/PycharmProjects/webots/projects/robots/bitcraze/crazyflie/`
- Controlador Python: `crazyflie_py_wallfollowing.py`
- PID Controller: `pid_controller.py`
- World file: `crazyflie.wbt`

---

_Criado: 2026-03-12_