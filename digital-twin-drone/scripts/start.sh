#!/bin/bash
# start.sh - Inicia os ambientes Digital Twin

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$PROJECT_DIR/docker"

cd "$DOCKER_DIR"

# Verificar container runtime
if command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
elif command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
else
    echo "❌ Erro: Docker ou Podman não encontrado"
    exit 1
fi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Digital Twin Drone - Iniciando Ambientes                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se as imagens existem
if ! $CONTAINER_CMD images | grep -q "digital-twin-drone"; then
    echo "❌ Imagem não encontrada. Execute primeiro:"
    echo "   ./scripts/build.sh"
    exit 1
fi

# Verificar X11
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY não definido. Interface gráfica pode não funcionar."
    echo "   Para X11 forwarding: export DISPLAY=:0"
fi

# Permitir X11
xhost +local:root 2>/dev/null || true

echo "🚀 Iniciando ambientes..."
echo ""

# Iniciar com docker-compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif $CONTAINER_CMD compose version &> /dev/null; then
    COMPOSE_CMD="$CONTAINER_CMD compose"
else
    echo "❌ docker-compose não encontrado"
    exit 1
fi

$COMPOSE_CMD up -d

echo ""
echo "⏳ Aguardando ambientes iniciarem..."
sleep 10

# Verificar containers
echo ""
echo "📊 Status dos containers:"
$CONTAINER_CMD ps --filter "name=dt-"

echo ""
echo "✓ Ambientes iniciados!"
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  AMBIENTE A (Mundo Real)                                   │"
echo "│    Porta MAVLink: 14550                                     │"
echo "│    SYSID: 1                                                 │"
echo "│                                                             │"
echo "│  AMBIENTE B (Digital Twin)                                 │"
echo "│    Porta MAVLink: 14551                                     │"
echo "│    SYSID: 2                                                 │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""
echo "Para iniciar o bridge Python:"
echo "  cd $PROJECT_DIR"
echo "  python3 src/dt_bridge.py"
echo ""
echo "Para parar:"
echo "  ./scripts/stop.sh"
echo ""
echo "Para ver logs:"
echo "  $CONTAINER_CMD logs -f dt-world-a"
echo "  $CONTAINER_CMD logs -f dt-world-b"