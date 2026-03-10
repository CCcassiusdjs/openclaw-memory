#!/bin/bash
# Auto-study script - Executa aprendizado em background
# Executado pelo cron do OpenClaw

EXPERTISE_DIR="/home/csilva/.openclaw/workspace/memory/expertise"
QUEUE_FILE="$EXPERTISE_DIR/queue.yaml"
PROGRESS_FILE="$EXPERTISE_DIR/progress.json"
TOPICS_DIR="$EXPERTISE_DIR/topics"

# Log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$EXPERTISE_DIR/study.log"
}

# Verificar se há tópico em progresso
get_current_topic() {
    if [ -f "$PROGRESS_FILE" ]; then
        cat "$PROGRESS_FILE" | jq -r '.current_topic // empty'
    fi
}

# Obter próximo tópico da fila
get_next_topic() {
    if [ -f "$QUEUE_FILE" ]; then
        # Parse YAML é complexo, usar grep simples
        grep -A 10 'status: "in_progress"' "$QUEUE_FILE" | head -1 | sed 's/.*id: "\(.*\)".*/\1/' || \
        grep -A 10 'status: "queued"' "$QUEUE_FILE" | head -1 | sed 's/.*id: "\(.*\)".*/\1/'
    fi
}

# Criar diretório do tópico se não existir
ensure_topic_dir() {
    local topic="$1"
    mkdir -p "$TOPICS_DIR/$topic"
}

# Atualizar progress
update_progress() {
    local topic="$1"
    local source="$2"
    local status="$3"
    
    if [ -f "$PROGRESS_FILE" ]; then
        # Atualizar usando jq
        tmp=$(mktemp)
        jq --arg topic "$topic" --arg source "$source" --arg status "$status" '
            .current_topic = $topic |
            .current_source = $source |
            .statistics.total_pages_read += 1 |
            .topics_progress[$topic].status = $status |
            .topics_progress[$topic].last_study = (now | todate)
        ' "$PROGRESS_FILE" > "$tmp" && mv "$tmp" "$PROGRESS_FILE"
    fi
}

# Função principal
main() {
    log "Iniciando sessão de auto-estudo"
    
    # Obter tópico atual ou próximo
    TOPIC=$(get_current_topic)
    if [ -z "$TOPIC" ]; then
        TOPIC=$(get_next_topic)
    fi
    
    if [ -z "$TOPIC" ]; then
        log "Nenhum tópico na fila"
        exit 0
    fi
    
    log "Tópico: $TOPIC"
    ensure_topic_dir "$TOPIC"
    
    # O aprendizado real será feito pelo agente principal
    # Este script apenas prepara o contexto
    
    log "Preparado para estudar: $TOPIC"
}

main "$@"