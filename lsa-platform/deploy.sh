#!/bin/bash
# Deploy da LSA Lab Platform no Cluster Docker Swarm
# Uso: ./deploy.sh [--build]

set -e

SCRIPTS_DIR="/home/csilva/.openclaw/workspace/lsa-platform"
DEPLOY_DIR="$SCRIPTS_DIR/deploy"
FRONTEND_DIR="$SCRIPTS_DIR/frontend"
API_DIR="$SCRIPTS_DIR/api"
BUILD="$1"

echo "=== LSA Lab Platform Deploy ==="
echo "Hora: $(date)"
echo ""

# 1. Build do Frontend (se solicitado)
if [ "$BUILD" = "--build" ]; then
    echo ">>> Build do Frontend..."
    cd "$FRONTEND_DIR"
    
    # Verificar se node_modules existe
    if [ ! -d "node_modules" ]; then
        echo "Instalando dependências..."
        npm install
    fi
    
    echo "Compilando React..."
    npm run build
    
    echo "Frontend compilado em dist/"
fi

# 2. Copiar arquivos para o Manager
echo ">>> Copiando arquivos para o cluster..."
scp -r "$SCRIPTS_DIR"/* cassiusdjs@10.10.20.11:/home/cassiusdjs/lsa-platform/ 2>/dev/null || \
    sshpass -p '230612' scp -r "$SCRIPTS_DIR"/* cassiusdjs@10.10.20.11:/home/cassiusdjs/lsa-platform/

# 3. Deploy no cluster
echo ">>> Deploy no Docker Swarm..."
ssh cassiusdjs@10.10.20.11 "cd /home/cassiusdjs/lsa-platform/deploy && \
    echo '230612' | sudo -S docker stack deploy -c docker-compose.yml lsa-platform"

echo ""
echo "=== Deploy Concluído ==="
echo "Frontend: http://10.10.20.11 (lab.lsa.local)"
echo "API: http://10.10.20.11/api"
echo "Docs: http://10.10.20.11/api/docs"
echo ""
echo "Credenciais padrão:"
echo "  Admin: admin / lsa@dm1n"
echo "  User:  demo / demo123"