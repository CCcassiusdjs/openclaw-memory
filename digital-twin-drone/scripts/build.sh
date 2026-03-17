#!/bin/bash
# build.sh - Constrói as imagens Docker para o Digital Twin Drone Demo

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$PROJECT_DIR/docker"

cd "$DOCKER_DIR"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Digital Twin Drone - Build Docker Images                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Docker/Podman
if command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
elif command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
else
    echo "❌ Erro: Docker ou Podman não encontrado"
    exit 1
fi

echo "✓ Container runtime: $CONTAINER_CMD"
echo ""

# Verificar NVIDIA Container Toolkit (para GPU)
if command -v nvidia-container-toolkit &> /dev/null || $CONTAINER_CMD info 2>/dev/null | grep -q nvidia; then
    echo "✓ NVIDIA Container Toolkit detectado"
    USE_GPU=true
else
    echo "⚠️  NVIDIA Container Toolkit não detectado (modo CPU-only)"
    USE_GPU=false
fi

# Build da imagem principal
echo ""
echo "📦 Construindo imagem gazebo-sitl..."
echo "   Isso pode levar 15-30 minutos na primeira execução."
echo ""

$CONTAINER_CMD build \
    -t digital-twin-drone:gazebo-sitl \
    -f Dockerfile.gazebo-sitl \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build concluído com sucesso!"
    echo ""
    echo "Imagem: digital-twin-drone:gazebo-sitl"
    echo ""
    echo "Próximos passos:"
    echo "  cd $PROJECT_DIR"
    echo "  ./scripts/start.sh"
else
    echo ""
    echo "❌ Erro no build. Verifique os logs acima."
    exit 1
fi