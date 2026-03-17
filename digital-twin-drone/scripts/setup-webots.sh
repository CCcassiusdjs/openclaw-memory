#!/bin/bash
# Digital Twin Bidirecional - Setup Corrigido
# Prepara os ambientes Webots corretamente

set -e

echo "=== PREPARANDO AMBIENTES WEBOTS ==="

# Diretórios
ARDUPILOT_DIR="/home/csilva/Documents/multirad_data_orchestrator/data_orchestrator/raspberry/arducopter"
WEBOTS_PYTHON="${ARDUPILOT_DIR}/libraries/SITL/examples/Webots_Python"
BASE_DIR="/tmp/digital-twin"

# Limpar e recriar estrutura correta
echo "Limpando estrutura antiga..."
rm -rf "${BASE_DIR}/env_a" "${BASE_DIR}/env_b" "${BASE_DIR}/controllers"

echo "Criando nova estrutura..."
mkdir -p "${BASE_DIR}/env_a/controllers"
mkdir -p "${BASE_DIR}/env_b/controllers"
mkdir -p "${BASE_DIR}/logs"
mkdir -p "${BASE_DIR}/pids"

# Copiar controller (mesmo diretório dos mundos)
echo "Copiando controller..."
cp -r "${WEBOTS_PYTHON}/controllers/ardupilot_vehicle_controller" "${BASE_DIR}/env_a/controllers/"
cp -r "${WEBOTS_PYTHON}/controllers/ardupilot_vehicle_controller" "${BASE_DIR}/env_b/controllers/"

# Copiar mundos
echo "Copiando mundos..."
cp "${WEBOTS_PYTHON}/worlds/crazyflie.wbt" "${BASE_DIR}/env_a/world_a.wbt"
cp "${WEBOTS_PYTHON}/worlds/crazyflie.wbt" "${BASE_DIR}/env_b/world_b.wbt"

# Copiar parâmetros
echo "Copiando parâmetros..."
cp "${WEBOTS_PYTHON}/params/crazyflie.parm" "${BASE_DIR}/env_a/"
cp "${WEBOTS_PYTHON}/params/crazyflie.parm" "${BASE_DIR}/env_b/"

# Copiar protos
echo "Copiando protos..."
cp -r "${WEBOTS_PYTHON}/protos" "${BASE_DIR}/env_a/" 2>/dev/null || true
cp -r "${WEBOTS_PYTHON}/protos" "${BASE_DIR}/env_b/" 2>/dev/null || true

# Verificar estrutura final
echo ""
echo "=== ESTRUTURA FINAL ==="
find "${BASE_DIR}" -type d | head -20

echo ""
echo "=== VERIFICANDO CONTROLLERS ==="
ls -la "${BASE_DIR}/env_a/controllers/ardupilot_vehicle_controller/"

echo ""
echo "✓ Setup completo!"