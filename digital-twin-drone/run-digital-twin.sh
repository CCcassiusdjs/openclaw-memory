#!/bin/bash
# Digital Twin Bidirecional - Versão Simplificada
# Usa binários já compilados ao invés de sim_vehicle.py

set -e

# =========================================
# CONFIGURAÇÃO
# =========================================

# Diretórios
ARDUPILOT_DIR="/home/csilva/Documents/multirad_data_orchestrator/data_orchestrator/raspberry/arducopter"
WEBOTS_DIR="/home/csilva/PycharmProjects/webots"
PROJECT_DIR="/home/csilva/.openclaw/workspace/digital-twin-drone"

# Binários
SITL_BIN="/home/csilva/ardupilot-sitl/build/sitl/bin/arducopter"

# Arquivos
ORIGINAL_DIR="/home/csilva/Documents/multirad_data_orchestrator/data_orchestrator/raspberry/arducopter/libraries/SITL/examples/Webots_Python"
WORLD_A="$ORIGINAL_DIR/worlds/world_a.wbt"
WORLD_B="$ORIGINAL_DIR/worlds/world_b.wbt"
BRIDGE_SCRIPT="$PROJECT_DIR/src/dt_bridge_webots.py"

# PID files
PID_DIR="/tmp/digital-twin/pids"
mkdir -p "$PID_DIR"
mkdir -p /tmp/digital-twin/logs

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =========================================
# FUNÇÕES
# =========================================

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_dependencies() {
    log_info "Verificando dependências..."
    
    if [ ! -f "$SITL_BIN" ]; then
        log_error "ArduPilot SITL não encontrado: $SITL_BIN"
        exit 1
    fi
    
    if [ ! -x "$WEBOTS_DIR/webots" ]; then
        log_error "Webots não encontrado: $WEBOTS_DIR/webots"
        exit 1
    fi
    
    if [ ! -f "$WORLD_A" ]; then
        log_error "Mundo A não encontrado: $WORLD_A"
        exit 1
    fi
    
    if [ ! -f "$WORLD_B" ]; then
        log_error "Mundo B não encontrado: $WORLD_B"
        exit 1
    fi
    
    log_success "Dependências OK"
}

kill_process() {
    local pid_file="$1"
    local name="$2"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "Parando $name (PID: $pid)..."
            kill "$pid" 2>/dev/null || true
            sleep 1
            kill -9 "$pid" 2>/dev/null || true
        fi
        rm -f "$pid_file"
    fi
}

stop_all() {
    log_info "Parando todos os processos..."
    kill_process "$PID_DIR/bridge.pid" "Bridge"
    kill_process "$PID_DIR/webots_a.pid" "Webots A"
    kill_process "$PID_DIR/webots_b.pid" "Webots B"
    kill_process "$PID_DIR/sitl_a.pid" "SITL A"
    kill_process "$PID_DIR/sitl_b.pid" "SITL B"
    # Matar qualquer processo órfão
    pkill -f "arducopter.*-I" 2>/dev/null || true
    pkill -f "webots.*world" 2>/dev/null || true
    pkill -f "dt_bridge_webots" 2>/dev/null || true
    log_success "Processos parados"
}

start_sitl_a() {
    log_info "Iniciando SITL A (Instância 0)..."
    
    cd "$ORIGINAL_DIR"
    
    # SITL para Webots:
    # -I 0: instância 0
    # --model webots-python: modelo para Webots controller Python
    # --sim-address: endereço do simulador (Webots controller)
    # --sim-port-in: porta para receber dados do controller (9003)
    # --sim-port-out: porta para enviar dados para controller (9002)
    $SITL_BIN -I 0 --model webots-python \
        --sim-address 127.0.0.1 \
        --sim-port-in 9003 \
        --sim-port-out 9002 \
        --defaults "$ORIGINAL_DIR/params/crazyflie.parm" \
        &> /tmp/digital-twin/logs/sitl_a.log &
    
    local pid=$!
    echo $pid > "$PID_DIR/sitl_a.pid"
    log_success "SITL A iniciado (PID: $pid, Instância: 0)"
    
    cd - > /dev/null
    sleep 3
}

start_sitl_b() {
    log_info "Iniciando SITL B (Instância 1)..."
    
    cd "$ORIGINAL_DIR"
    
    # SITL para Webots (instância 1):
    # -I 1: instância 1
    # --model webots-python: modelo para Webots controller Python
    # --sim-address: endereço do simulador (Webots controller)
    # --sim-port-in: porta para receber dados do controller (9013)
    # --sim-port-out: porta para enviar dados para controller (9012)
    $SITL_BIN -I 1 --model webots-python \
        --sim-address 127.0.0.1 \
        --sim-port-in 9013 \
        --sim-port-out 9012 \
        --defaults "$ORIGINAL_DIR/params/crazyflie.parm" \
        &> /tmp/digital-twin/logs/sitl_b.log &
    
    local pid=$!
    echo $pid > "$PID_DIR/sitl_b.pid"
    log_success "SITL B iniciado (PID: $pid, Instância: 1)"
    
    cd - > /dev/null
    sleep 3
}

start_webots_a() {
    log_info "Iniciando Webots A (Porta 1234)..."
    
    "$WEBOTS_DIR/webots" --batch --no-rendering --port=1234 "$WORLD_A" &> /tmp/digital-twin/logs/webots_a.log &
    
    local pid=$!
    echo $pid > "$PID_DIR/webots_a.pid"
    log_success "Webots A iniciado (PID: $pid)"
    
    sleep 3
}

start_webots_b() {
    log_info "Iniciando Webots B (Porta 1235)..."
    
    "$WEBOTS_DIR/webots" --batch --no-rendering --port=1235 "$WORLD_B" &> /tmp/digital-twin/logs/webots_b.log &
    
    local pid=$!
    echo $pid > "$PID_DIR/webots_b.pid"
    log_success "Webots B iniciado (PID: $pid)"
    
    sleep 3
}

start_bridge() {
    log_info "Iniciando Bridge Python..."
    
    python3 "$BRIDGE_SCRIPT" \
        --sitl-a-listen 14550 \
        --sitl-b-listen 14551 \
        &> /tmp/digital-twin/logs/bridge.log &
    
    local pid=$!
    echo $pid > "$PID_DIR/bridge.pid"
    log_success "Bridge iniciado (PID: $pid)"
}

show_status() {
    echo ""
    echo "========================================"
    echo "  DIGITAL TWIN - STATUS"
    echo "========================================"
    echo ""
    
    local running=0
    
    if [ -f "$PID_DIR/sitl_a.pid" ]; then
        local pid=$(cat "$PID_DIR/sitl_a.pid")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} SITL A (PID: $pid)"
            ((running++))
        else
            echo -e "  ${RED}✗${NC} SITL A (parado)"
        fi
    fi
    
    if [ -f "$PID_DIR/sitl_b.pid" ]; then
        local pid=$(cat "$PID_DIR/sitl_b.pid")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} SITL B (PID: $pid)"
            ((running++))
        else
            echo -e "  ${RED}✗${NC} SITL B (parado)"
        fi
    fi
    
    if [ -f "$PID_DIR/webots_a.pid" ]; then
        local pid=$(cat "$PID_DIR/webots_a.pid")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Webots A (PID: $pid)"
            ((running++))
        else
            echo -e "  ${RED}✗${NC} Webots A (parado)"
        fi
    fi
    
    if [ -f "$PID_DIR/webots_b.pid" ]; then
        local pid=$(cat "$PID_DIR/webots_b.pid")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Webots B (PID: $pid)"
            ((running++))
        else
            echo -e "  ${RED}✗${NC} Webots B (parado)"
        fi
    fi
    
    if [ -f "$PID_DIR/bridge.pid" ]; then
        local pid=$(cat "$PID_DIR/bridge.pid")
        if kill -0 "$pid" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Bridge (PID: $pid)"
            ((running++))
        else
            echo -e "  ${RED}✗${NC} Bridge (parado)"
        fi
    fi
    
    echo ""
    echo "Processos ativos: $running/5"
}

monitor_logs() {
    log_info "Monitorando logs (Ctrl+C para parar)..."
    tail -f /tmp/digital-twin/logs/*.log 2>/dev/null || {
        log_warning "Logs não encontrados"
    }
}

# =========================================
# MAIN
# =========================================

case "${1:-start}" in
    start)
        log_info "Iniciando Digital Twin Bidirecional..."
        echo ""
        check_dependencies
        stop_all
        echo ""
        log_info "Iniciando componentes..."
        echo ""
        
        start_sitl_a
        start_sitl_b
        start_webots_a
        start_webots_b
        start_bridge
        
        echo ""
        show_status
        echo ""
        log_success "Digital Twin iniciado!"
        echo ""
        echo "Logs: /tmp/digital-twin/logs/"
        echo "Para parar: $0 stop"
        echo "Para status: $0 status"
        echo ""
        monitor_logs
        ;;
    
    stop)
        stop_all
        ;;
    
    status)
        show_status
        ;;
    
    logs)
        monitor_logs
        ;;
    
    restart)
        stop_all
        sleep 2
        $0 start
        ;;
    
    *)
        echo "Uso: $0 {start|stop|status|logs|restart}"
        exit 1
        ;;
esac