# Digital Twin Bidirecional para Drones

Demonstração de Digital Twin usando duas instâncias Gazebo + ArduPilot SITL sincronizadas via MAVLink.

## 🎯 Conceito

```
┌─────────────────┐       MAVLink/UDP        ┌─────────────────┐
│   AMBIENTE A    │◄─────────────────────────►│   AMBIENTE B    │
│   (Mundo Real)  │      ~20ms latência       │   (Digital Twin)│
│                 │                           │                 │
│  Gazebo #1      │                           │  Gazebo #2      │
│  ArduCopter #1  │                           │  ArduCopter #2  │
│  SYSID: 1       │                           │  SYSID: 2       │
└─────────────────┘                           └─────────────────┘
```

Quando você mexe em QUALQUER drone em QUALQUER ambiente, o comportamento é refletido no ambiente oposto.

## 📋 Pré-requisitos

- Docker ou Podman
- NVIDIA Container Toolkit (para GPU)
- 16GB RAM mínimo
- Ubuntu 22.04+ ou RHEL 10+

## 🚀 Quick Start

```bash
# Clone e entre no diretório
cd ~/.openclaw/workspace/digital-twin-drone

# Construa as imagens
./scripts/build.sh

# Inicie os ambientes
./scripts/start.sh

# Execute o bridge Python
python3 src/dt_bridge.py
```

## 📁 Estrutura

```
digital-twin-drone/
├── README.md
├── docker/
│   ├── Dockerfile.gazebo-sitl
│   └── docker-compose.yml
├── scripts/
│   ├── build.sh
│   ├── start.sh
│   └── stop.sh
├── src/
│   ├── dt_bridge.py
│   └── utils/
├── config/
│   ├── world_a.sdf
│   ├── world_b.sdf
│   └── params/
└── docs/
    ├── SRS.md
    ├── SAD.md
    └── POC.md
```

## 🔧 Componentes

| Componente | Tecnologia | Função |
|------------|------------|--------|
| Simulador | Gazebo Harmonic | Física e visualização |
| Controlador | ArduPilot SITL | Controle de voo |
| Protocolo | MAVLink v2 | Comunicação |
| Bridge | Python + pymavlink | Sincronização bidirecional |

## 📊 Requisitos de Latência

- **Alvo:** < 50ms
- **Update rate:** 50Hz (20ms/ciclo)
- **Protocolo:** UDP over localhost

## 🔗 Referências

- [ArduPilot SITL Documentation](https://ardupilot.org/dev/docs/sitl-with-gazebo.html)
- [Gazebo Harmonic](https://gazebosim.org/)
- [MAVLink Protocol](https://mavlink.io/en/)
- [ardupilot_gazebo Plugin](https://github.com/ArduPilot/ardupilot_gazebo)

---
**Status:** Em desenvolvimento
**Última atualização:** 2026-03-16