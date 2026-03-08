#!/bin/bash
# LaTeX Live Preview Script
# Usage: ./latex-live.sh <file.tex>

TEXFILE="${1:-radiation_test_report.tex}"
BASENAME=$(basename "$TEXFILE" .tex)
PDFNAME="${BASENAME}.pdf"

echo "=== LaTeX Live Preview ==="
echo "File: $TEXFILE"
echo "PDF: $PDFNAME"
echo ""

# Initial compile
echo "[1/2] Compiling initial PDF..."
pdflatex -interaction=nonstopmode "$TEXFILE" > /dev/null 2>&1
pdflatex -interaction=nonstopmode "$TEXFILE" > /dev/null 2>&1
echo "[2/2] Done!"

# Open PDF viewer in background
echo ""
echo "Opening PDF viewer..."
mupdf "$PDFNAME" &
VIEWER_PID=$!

echo "Viewer PID: $VIEWER_PID"
echo ""
echo "=== Watching for changes ==="
echo "Edit $TEXFILE and save to see live updates"
echo "Press Ctrl+C to stop"
echo ""

# Watch for changes and recompile
inotifywait -m -e close_write,moved_to "$TEXFILE" 2>/dev/null | while read dir action file; do
    echo "$(date '+%H:%M:%S') - Change detected, recompiling..."
    pdflatex -interaction=nonstopmode "$TEXFILE" > /tmp/latex-compile.log 2>&1
    if [ $? -eq 0 ]; then
        echo "$(date '+%H:%M:%S') - Compiled successfully!"
        # Reload viewer
        kill -HUP $VIEWER_PID 2>/dev/null
    else
        echo "$(date '+%H:%M:%S') - Compilation error!"
        tail -5 /tmp/latex-compile.log
    fi
done