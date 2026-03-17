#!/bin/bash
# stop.sh - Para os ambientes Digital Twin

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
echo "║  Digital Twin Drone - Parando Ambientes                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# docker-compose down
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif $CONTAINER_CMD compose version &> /dev/null; then
    COMPOSE_CMD="$CONTAINER_CMD compose"
else
    echo "❌ docker-compose não encontrado"
    exit 1
fi

$COMPOSE_CMD down

echo ""
echo "✓ Ambientes parados!"