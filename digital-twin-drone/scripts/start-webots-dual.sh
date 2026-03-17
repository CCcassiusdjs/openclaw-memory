#!/bin/bash
# Digital Twin Bidirecional - Duas instâncias Webots separadas
# Arquitetura: Webots A (Mundo Físico) ←→ Bridge ←→ Webots B (Digital Twin)

set -e

# Diretórios
ARDUPILOT_DIR="/home/csilva/Documents/multirad_data_orchestrator/data_orchestrator/raspberry/arducopter"
WEBOTS_DIR="/home/csilva/PycharmProjects/webots"
WEBOTS_PYTHON="${ARDUPILOT_DIR}/libraries/SITL/examples/Webots_Python"

# ArduPilot SITL compilado
SITL_BIN="/home/csilva/Documents/multirad_data_orchestrator/case-study_algorithms/drone/arducopter-ekf/runtime/assets/x86_64/arducopter"

echo "=========================================="
echo "  DIGITAL TWIN BIDIRECIONAL - WEBOTS"
echo "=========================================="
echo ""

# Verificar se arquivos existem
if [ ! -f "$SITL_BIN" ]; then
    echo "ERRO: ArduPilot SITL não encontrado em $SITL_BIN"
    exit 1
fi

if [ ! -d "$WEBOTS_DIR" ]; then
    echo "ERRO: Webots não encontrado em $WEBOTS_DIR"
    exit 1
fi

if [ ! -d "$WEBOTS_PYTHON" ]; then
    echo "ERRO: Webots Python controller não encontrado em $WEBOTS_PYTHON"
    exit 1
fi

echo "✓ ArduPilot SITL: $SITL_BIN"
echo "✓ Webots: $WEBOTS_DIR"
echo "✓ Webots Python: $WEBOTS_PYTHON"
echo ""

# Criar diretórios de trabalho
mkdir -p /tmp/digital-twin/env_a
mkdir -p /tmp/digital-twin/env_b
mkdir -p /tmp/digital-twin/logs

echo "=========================================="
echo "  PASSO 1: COPIAR MUNDOS WEBOTS"
echo "=========================================="

# Copiar mundos para diretórios temporários
cp "$WEBOTS_PYTHON/worlds/crazyflie.wbt" /tmp/digital-twin/env_a/world_a.wbt
cp "$WEBOTS_PYTHON/worlds/crazyflie.wbt" /tmp/digital-twin/env_b/world_b.wbt

# Copiar parâmetros
cp "$WEBOTS_PYTHON/params/crazyflie.parm" /tmp/digital-twin/env_a/
cp "$WEBOTS_PYTHON/params/crazyflie.parm" /tmp/digital-twin/env_b/

# Copiar controller
cp -r "$WEBOTS_PYTHON/controllers" /tmp/digital-twin/env_a/
cp -r "$WEBOTS_PYTHON/controllers" /tmp/digital-twin/env_b/
cp -r "$WEBOTS_PYTHON/protos" /tmp/digital-twin/env_a/
cp -r "$WEBOTS_PYTHON/protos" /tmp/digital-twin/env_b/

echo "✓ Mundos copiados"
echo ""

echo "=========================================="
echo "  PASSO 2: CONFIGURAR WEBOTS PARA MÚLTIPLAS INSTÂNCIAS"
echo "=========================================="

# Webots usa porta TCP para comunicação com controllers externos
# Porta padrão: 1234
# Instância A: porta 1234 (padrão)
# Instância B: porta 1235

echo ""
echo "Para executar duas instâncias Webots em paralelo:"
echo ""
echo "TERMINAL 1 - WEBOTS A (Mundo Físico):"
echo "  $WEBOTS_DIR/webots /tmp/digital-twin/env_a/world_a.wbt &"
echo ""
echo "TERMINAL 2 - SITL A:"
echo "  cd $ARDUPILOT_DIR"
echo "  ./Tools/autotest/sim_vehicle.py -v ArduCopter -w --model webots-python \\"
echo "    --add-param-file=/tmp/digital-twin/env_a/crazyflie.parm \\"
echo "    --base-port=5760"
echo ""
echo "TERMINAL 3 - WEBOTS B (Digital Twin):"
echo "  WEBOTS_PORT=1235 $WEBOTS_DIR/webots /tmp/digital-twin/env_b/world_b.wbt &"
echo ""
echo "TERMINAL 4 - SITL B:"
echo "  cd $ARDUPILOT_DIR"
echo "  ./Tools/autotest/sim_vehicle.py -v ArduCopter -w --model webots-python \\"
echo "    --add-param-file=/tmp/digital-twin/env_b/crazyflie.parm \\"
echo "    --base-port=5770"
echo ""
echo "TERMINAL 5 - BRIDGE PYTHON:"
echo "  python3 /home/csilva/.openclaw/workspace/digital-twin-drone/src/dt_bridge_webots.py"
echo ""

echo "=========================================="
echo "  NOTAS IMPORTANTES"
echo "=========================================="
echo ""
echo "1. Cada Webots precisa de sua própria janela (processo separado)"
echo "2. SITL A conecta no Webots A (porta 9002)"
echo "3. SITL B conecta no Webots B (porta 9012)"
echo "4. Bridge Python sincroniza estados entre os dois"
echo ""
echo "PRÓXIMO PASSO: Execute os comandos acima em terminais separados"
echo ""