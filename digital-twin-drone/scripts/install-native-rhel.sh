#!/bin/bash
# install-native-rhel.sh - Instalação nativa para RHEL 10

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Digital Twin Drone - Instalação Nativa (RHEL 10)           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# 1. Verificar se é RHEL
if [ ! -f /etc/redhat-release ]; then
    echo -e "${RED}Este script é para RHEL/CentOS/Fedora.${NC}"
    echo "Para Ubuntu/Debian, use Docker."
    exit 1
fi

echo -e "${GREEN}[1/5] Instalando dependências do sistema...${NC}"
sudo dnf install -y git cmake build-essential python3 python3-pip python3-devel \
    libtool libxml2-devel libxslt-devel geographiclib-devel \
    opencv-devel protobuf-devel protobuf-c

echo -e "${GREEN}[2/5] Instalando Gazebo Harmonic...${NC}"
# Tentar via COPR ou EPEL
if ! command -v gz &> /dev/null; then
    echo "Gazebo não encontrado. Tentando instalar..."
    
    # Verificar se existe pacote gz-harmonic
    if dnf list available 2>/dev/null | grep -q "gz-harmonic"; then
        sudo dnf install -y gz-harmonic
    else
        echo -e "${RED}Gazebo Harmonic não disponível via DNF.${NC}"
        echo "Alternativas:"
        echo "  1. Instalar Ubuntu 22.04 em VM/WSL2"
        echo "  2. Compilar Gazebo do source (demorado)"
        echo "  3. Usar Docker com Ubuntu 22.04"
        exit 1
    fi
fi

echo -e "${GREEN}[3/5] Clonando ArduPilot...${NC}"
if [ ! -d "$HOME/ardupilot" ]; then
    cd "$HOME"
    git clone --depth 1 --recurse-submodules https://github.com/ArduPilot/ardupilot.git
else
    echo "ArduPilot já existe em ~/ardupilot"
fi

echo -e "${GREEN}[4/5] Compilando ArduPilot SITL...${NC}"
cd "$HOME/ardupilot"
if [ ! -f "build/sitl/bin/arducopter" ]; then
    ./waf configure --board=sitl
    ./waf copter
else
    echo "ArduPilot já compilado"
fi

echo -e "${GREEN}[5/5] Instalando pymavlink...${NC}"
pip3 install --user pymavlink matplotlib numpy empy==3.3.4 future lxml pexpect

# Configurar PATH
echo ""
echo "Adicionando ao PATH..."
if ! grep -q "ardupilot/build/sitl/bin" "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH=$HOME/ardupilot/build/sitl/bin:$PATH' >> "$HOME/.bashrc"
    echo "Adicionado ao ~/.bashrc"
else
    echo "PATH já configurado"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✓ Instalação concluída!                                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Para completar, execute:"
echo "  source ~/.bashrc"
echo ""
echo "Para testar:"
echo "  cd ~/ardupilot"
echo "  ./build/sitl/bin/arducopter --version"
echo ""
echo "Bridge Python:"
echo "  cd ~/.openclaw/workspace/digital-twin-drone"
echo "  python3 src/dt_bridge.py"