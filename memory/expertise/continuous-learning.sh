#!/bin/bash
# OpenClaw Continuous Learning Loop
# Este script roda PARA SEMPRE, nunca para

EXPERTISE_DIR="/home/csilva/.openclaw/workspace/memory/expertise"
QUEUE_FILE="$EXPERTISE_DIR/queue.yaml"
PROGRESS_FILE="$EXPERTISE_DIR/progress.json"
LOG_FILE="$EXPERTISE_DIR/continuous-learning.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Loop infinito
log "=== INICIANDO APRENDIZADO CONTÍNUO ==="

while true; do
    log "Iniciando ciclo de aprendizado..."
    
    # 1. Verificar se há tópico na fila
    CURRENT_TOPIC=$(grep -A 5 'status: "new"' "$QUEUE_FILE" | grep 'id:' | head -1 | sed 's/.*id: "\([^"]*\)".*/\1/')
    
    if [ -z "$CURRENT_TOPIC" ]; then
        CURRENT_TOPIC=$(grep -A 5 'status: "reading"' "$QUEUE_FILE" | grep 'id:' | head -1 | sed 's/.*id: "\([^"]*\)".*/\1/')
    fi
    
    if [ -n "$CURRENT_TOPIC" ]; then
        log "Tópico atual: $CURRENT_TOPIC"
        
        # 2. Verificar se precisa de levantamento bibliográfico
        BIB_FILE="$EXPERTISE_DIR/topics/$CURRENT_TOPIC/bibliography.md"
        
        if [ ! -f "$BIB_FILE" ]; then
            log "FASE 1: Levantamento bibliográfico necessário"
            # O agente principal fará isso via system event
        else
            log "FASE 2: Continuando leitura"
            # O agente principal fará isso via system event
        fi
    else
        log "Nenhum tópico na fila"
    fi
    
    # 3. Aguardar um pouco antes do próximo ciclo
    # Mas NÃO parar - sempre voltar para aprender mais
    sleep 300  # 5 minutos entre ciclos
    
    # O agente principal será notificado via heartbeat ou system event
    # para continuar o aprendizado
done