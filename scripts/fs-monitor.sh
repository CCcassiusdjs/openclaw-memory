#!/bin/bash
# fs-monitor.sh - Monitoramento em tempo real de sistema de arquivos
# Autor: OpenClaw
# Data: 2026-03-08

set -euo pipefail

# Configuração
WATCH_DIRS="${WATCH_DIRS:-/home/csilva}"
LOG_DIR="${LOG_DIR:-/home/csilva/.openclaw/workspace/logs/fs-monitor}"
MAX_EVENTS="${MAX_EVENTS:-10000}"
BATCH_INTERVAL="${BATCH_INTERVAL:-5}"  # segundos

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Criar diretório de logs
mkdir -p "$LOG_DIR"

# Arquivos de log
EVENT_LOG="$LOG_DIR/events-$(date +%Y%m%d).log"
ERROR_LOG="$LOG_DIR/errors-$(date +%Y%m%d).log"
BASELINE_FILE="$LOG_DIR/baseline.txt"

log_event() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S.%3N')
    local event_type="$1"
    local path="$2"
    echo "[$timestamp] [$event_type] $path" >> "$EVENT_LOG"
}

log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$ERROR_LOG"
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

# Verificar se inotify-tools está instalado
check_dependencies() {
    if ! command -v inotifywait &> /dev/null; then
        echo -e "${YELLOW}inotify-tools não instalado. Instalando...${NC}"
        sudo dnf install -y inotifytools || {
            log_error "Falha ao instalar inotify-tools"
            exit 1
        }
    fi
    
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}jq não instalado. Instalando...${NC}"
        sudo dnf install -y jq || {
            log_error "Falha ao instalar jq"
            exit 1
        }
    fi
}

# Verificar e ajustar limites do sistema
check_limits() {
    local max_watches=$(cat /proc/sys/fs/inotify/max_user_watches)
    local max_instances=$(cat /proc/sys/fs/inotify/max_user_instances)
    
    echo -e "${BLUE}Limites atuais:${NC}"
    echo -e "  max_user_watches: $max_watches"
    echo -e "  max_user_instances: $max_instances"
    
    # Contar diretórios
    local dir_count=$(find "$WATCH_DIRS" -type d 2>/dev/null | wc -l)
    echo -e "  Diretórios a monitorar: $dir_count"
    
    # Verificar se precisa aumentar
    local recommended=$((dir_count * 2))
    if [ "$max_watches" -lt "$recommended" ]; then
        echo -e "${YELLOW}Recomendado aumentar max_user_watches para $recommended${NC}"
        echo -e "${YELLOW}Execute: sudo sysctl fs.inotify.max_user_watches=$recommended${NC}"
    fi
}

# Criar baseline do sistema de arquivos
create_baseline() {
    echo -e "${BLUE}Criando baseline do sistema de arquivos...${NC}"
    
    local baseline_time=$(date +%s)
    
    # Usar find com formato estruturado
    find "$WATCH_DIRS" -type f -printf '%T@ %p\n' 2>/dev/null | \
        sort > "$BASELINE_FILE.tmp"
    
    mv "$BASELINE_FILE.tmp" "$BASELINE_FILE"
    
    local file_count=$(wc -l < "$BASELINE_FILE")
    local elapsed=$(($(date +%s) - baseline_time))
    
    echo -e "${GREEN}Baseline criado: $file_count arquivos em ${elapsed}s${NC}"
    log_event "BASELINE_CREATED" "$file_count files"
}

# Detectar mudanças desde o baseline
detect_changes() {
    if [ ! -f "$BASELINE_FILE" ]; then
        echo -e "${YELLOW}Baseline não existe. Criando...${NC}"
        create_baseline
        return
    fi
    
    echo -e "${BLUE}Detectando mudanças...${NC}"
    
    # Criar snapshot atual
    local current_file="$LOG_DIR/current-$(date +%s).tmp"
    find "$WATCH_DIRS" -type f -printf '%T@ %p\n' 2>/dev/null | sort > "$current_file"
    
    # Comparar com baseline
    local added=0
    local removed=0
    local modified=0
    
    # Arquivos novos (em current mas não em baseline)
    comm -13 <(cut -d' ' -f2 "$BASELINE_FILE" | sort) \
              <(cut -d' ' -f2 "$current_file" | sort) > "$LOG_DIR/added.txt"
    added=$(wc -l < "$LOG_DIR/added.txt")
    
    # Arquivos removidos (em baseline mas não em current)
    comm -23 <(cut -d' ' -f2 "$BASELINE_FILE" | sort) \
              <(cut -d' ' -f2 "$current_file" | sort) > "$LOG_DIR/removed.txt"
    removed=$(wc -l < "$LOG_DIR/removed.txt")
    
    # Arquivos modificados (timestamps diferentes)
    while IFS= read -r line; do
        local path=$(echo "$line" | cut -d' ' -f2-)
        local old_ts=$(grep " $path$" "$BASELINE_FILE" | cut -d' ' -f1)
        local new_ts=$(grep " $path$" "$current_file" | cut -d' ' -f1)
        if [ -n "$old_ts" ] && [ -n "$new_ts" ]; then
            if [ "$old_ts" != "$new_ts" ]; then
                echo "$path" >> "$LOG_DIR/modified.txt"
            fi
        fi
    done < <(comm -12 <(cut -d' ' -f2 "$BASELINE_FILE" | sort) \
                   <(cut -d' ' -f2 "$current_file" | sort))
    
    modified=$(wc -l < "$LOG_DIR/modified.txt" 2>/dev/null || echo 0)
    
    echo -e "${GREEN}Mudanças detectadas:${NC}"
    echo -e "  ${GREEN}Adicionados: $added${NC}"
    echo -e "  ${RED}Removidos: $removed${NC}"
    echo -e "  ${YELLOW}Modificados: $modified${NC}"
    
    # Atualizar baseline
    mv "$current_file" "$BASELINE_FILE"
    
    # Log
    log_event "CHANGES_DETECTED" "added=$added,removed=$removed,modified=$modified"
}

# Monitoramento em tempo real com inotifywait
monitor_realtime() {
    echo -e "${BLUE}Iniciando monitoramento em tempo real...${NC}"
    echo -e "${BLUE}Diretórios: $WATCH_DIRS${NC}"
    
    # Usar inotifywait em modo contínuo
    # -r: recursivo
    # -m: monitor (não sai após primeiro evento)
    # --format: formato personalizado
    # --exclude: excluir padrões
    
    inotifywait -r -m --format '%w%f %e' \
        --exclude '\.git|\.cache|\.local|tmp|\.log$' \
        "$WATCH_DIRS" 2>/dev/null | \
    while read -r line; do
        local path=$(echo "$line" | cut -d' ' -f1)
        local event=$(echo "$line" | cut -d' ' -f2)
        
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S.%3N')
        
        # Log estruturado
        echo "{\"timestamp\":\"$timestamp\",\"path\":\"$path\",\"event\":\"$event\"}" >> "$EVENT_LOG.json"
        
        # Output colorido por tipo de evento
        case "$event" in
            CREATE|CREATE,ISDIR)
                echo -e "${GREEN}[$timestamp] CREATED: $path${NC}"
                ;;
            DELETE|DELETE,ISDIR)
                echo -e "${RED}[$timestamp] DELETED: $path${NC}"
                ;;
            MODIFY|CLOSE_WRITE)
                echo -e "${YELLOW}[$timestamp] MODIFIED: $path${NC}"
                ;;
            MOVED_FROM|MOVED_TO)
                echo -e "${BLUE}[$timestamp] MOVED: $path${NC}"
                ;;
            *)
                echo -e "[$timestamp] $event: $path"
                ;;
        esac
        
        # Batch events para processamento
        echo "$path" >> "$LOG_DIR/batch-$(date +%s).tmp"
    done
}

# Processar eventos em batch
process_batch() {
    local batch_file="$1"
    
    if [ ! -f "$batch_file" ]; then
        return
    fi
    
    echo -e "${BLUE}Processando batch: $(basename $batch_file)${NC}"
    
    # Agrupar por tipo de mudança
    local added=$(grep -c "CREATE" "$batch_file" 2>/dev/null || echo 0)
    local removed=$(grep -c "DELETE" "$batch_file" 2>/dev/null || echo 0)
    local modified=$(grep -c "MODIFY" "$batch_file" 2>/dev/null || echo 0)
    
    echo -e "  Adicionados: $added"
    echo -e "  Removidos: $removed"
    echo -e "  Modificados: $modified"
    
    # Mover para arquivo processado
    mv "$batch_file" "$batch_file.processed"
    
    log_event "BATCH_PROCESSED" "added=$added,removed=$removed,modified=$modified"
}

# Gerar relatório de estatísticas
generate_report() {
    echo -e "${BLUE}=== Relatório de Monitoramento ===${NC}"
    
    if [ -f "$EVENT_LOG.json" ]; then
        echo -e "\n${YELLOW}Eventos por tipo:${NC}"
        jq -r '.event' "$EVENT_LOG.json" | sort | uniq -c | sort -rn
        
        echo -e "\n${YELLOW}Top 10 diretórios com mais mudanças:${NC}"
        jq -r '.path' "$EVENT_LOG.json" | xargs dirname | sort | uniq -c | sort -rn | head -10
        
        echo -e "\n${YELLOW}Timeline de eventos:${NC}"
        jq -r '.timestamp' "$EVENT_LOG.json" | cut -d'T' -f2 | cut -d':' -f1 | sort | uniq -c
    fi
    
    echo -e "\n${YELLOW}Estatísticas do sistema:${NC}"
    echo -e "  Watches usados: $(find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | wc -l)"
    echo -e "  Limites: $(cat /proc/sys/fs/inotify/max_user_watches) watches, $(cat /proc/sys/fs/inotify/max_user_instances) instances"
}

# Limpar arquivos antigos
cleanup_old_logs() {
    echo -e "${BLUE}Limpando logs antigos (>7 dias)...${NC}"
    find "$LOG_DIR" -name "*.log" -mtime +7 -delete
    find "$LOG_DIR" -name "*.json" -mtime +7 -delete
    find "$LOG_DIR" -name "*.tmp" -delete
}

# Uso do script
usage() {
    echo "Uso: $0 [opção]"
    echo ""
    echo "Opções:"
    echo "  --check        Verificar dependências e limites"
    echo "  --baseline     Criar baseline do sistema de arquivos"
    echo "  --changes      Detectar mudanças desde o baseline"
    echo "  --monitor      Iniciar monitoramento em tempo real"
    echo "  --report       Gerar relatório de estatísticas"
    echo "  --cleanup      Limpar logs antigos"
    echo "  --all          Executar check + baseline + monitor"
    echo ""
    echo "Variáveis de ambiente:"
    echo "  WATCH_DIRS     Diretórios a monitorar (padrão: /home/csilva)"
    echo "  LOG_DIR        Diretório de logs (padrão: ~/.openclaw/workspace/logs/fs-monitor)"
    echo ""
    echo "Exemplos:"
    echo "  $0 --check"
    echo "  WATCH_DIRS=/home/csilva/Documents $0 --monitor"
    echo "  $0 --all"
}

# Main
main() {
    case "${1:-}" in
        --check)
            check_dependencies
            check_limits
            ;;
        --baseline)
            check_dependencies
            create_baseline
            ;;
        --changes)
            detect_changes
            ;;
        --monitor)
            check_dependencies
            check_limits
            monitor_realtime
            ;;
        --report)
            generate_report
            ;;
        --cleanup)
            cleanup_old_logs
            ;;
        --all)
            check_dependencies
            check_limits
            create_baseline
            monitor_realtime
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"