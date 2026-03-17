#!/bin/bash
set -e

# Configurar variáveis de ambiente
export GZ_SIM_RESOURCE_PATH=/opt/ardupilot_gazebo/models:/opt/ardupilot_gazebo/worlds
export GZ_SIM_PLUGIN_PATH=/opt/ardupilot_gazebo/build
export LD_LIBRARY_PATH=/opt/gz_harmonic_install/lib:${LD_LIBRARY_PATH}
export PATH=/opt/ardupilot/build/sitl/bin:${PATH}

# Criar diretórios de trabalho
mkdir -p /workspace/logs

# Aguardar comando
echo "=== Digital Twin Drone Environment ==="
echo "Gazebo Harmonic: $(gz sim --version 2>/dev/null || echo 'disponível')"
echo "ArduPilot SITL: $(ls /opt/ardupilot/build/sitl/bin/ 2>/dev/null || echo 'disponível')"
echo "pymavlink: $(python3 -c 'import pymavlink; print(pymavlink.__version__)')"
echo ""
echo "Ambiente pronto. Use os scripts em /workspace/scripts/"

exec "$@"