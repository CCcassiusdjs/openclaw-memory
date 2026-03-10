#!/bin/bash
# Context Pruning Script - Comprime logs antigos e limpa contexto inchado

WORKSPACE="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
DAYS_TO_KEEP=30

echo "=== Context Pruning - $(date) ==="

# 1. Mover arquivos grandes não-.md para subdiretório
cd "$MEMORY_DIR"
mkdir -p visualizations archives

# Mover HTML/JSON para visualizations
find . -maxdepth 1 -name "*.html" -size +1M -exec mv {} visualizations/ \; 2>/dev/null
find . -maxdepth 1 -name "*.json" -size +1M -exec mv {} visualizations/ \; 2>/dev/null

# 2. Arquivar logs antigos (>30 dias)
find . -maxdepth 1 -name "*.md" -mtime +$DAYS_TO_KEEP ! -name "MEMORY.md" -exec mv {} archives/ \; 2>/dev/null

# 3. Reportar estado
echo ""
echo "=== Estado Atual ==="
echo "Arquivos .md ativos: $(ls -1 *.md 2>/dev/null | wc -l)"
echo "Linhas total: $(wc -l *.md 2>/dev/null | tail -1 | awk '{print $1}')"
echo "Arquivos em visualizations/: $(ls -1 visualizations/ 2>/dev/null | wc -l)"
echo "Arquivos em archives/: $(ls -1 archives/ 2>/dev/null | wc -l)"
echo ""
echo "⚠️  AÇÃO MANUAL: Atualize MEMORY.md com distilação dos logs arquivados"