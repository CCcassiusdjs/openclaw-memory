#!/bin/bash
# Error Learning System - Learns from errors and successes
# Called when errors occur or after successful operations

WORKSPACE="$HOME/.openclaw/workspace"
PATTERNS_FILE="$WORKSPACE/memory/learning-patterns.yaml"
HEURISTICS_FILE="$WORKSPACE/memory/intuition.yaml"

# Ensure files exist
mkdir -p "$WORKSPACE/memory"

# Initialize pattern file if needed
if [ ! -f "$PATTERNS_FILE" ]; then
    cat > "$PATTERNS_FILE" << 'EOF'
# Learning Patterns - Auto-Learning System
# OpenClaw learns from errors and successes

version: "1.0"
created: "2026-03-08"

# Patterns learned from experience
patterns:
  # Pattern: [type] - [context] - [solution]

# Error patterns detected
errors: []

# Success patterns
successes: []

# Heuristics learned
heuristics: []
EOF
fi

# Initialize intuition file if needed
if [ ! -f "$HEURISTICS_FILE" ]; then
    cat > "$HEURISTICS_FILE" << 'EOF'
# Intuition System - Learned Preferences
# OpenClaw develops "intuition" from observing user patterns

version: "1.0"
created: "2026-03-08"

# User behavior patterns observed
observations:
  decision_patterns: []
  rejection_patterns: []
  preference_patterns: []
  timing_patterns: []
  
# Learned heuristics
heuristics: []

# Confidence scores
confidence: {}
EOF
fi

# Function to record error pattern
record_error() {
    local error_type="$1"
    local context="$2"
    local solution="$3"
    local confidence="$4"
    
    # Add to patterns file
    echo "  - type: error" >> "$PATTERNS_FILE.tmp"
    echo "    pattern: \"$error_type\"" >> "$PATTERNS_FILE.tmp"
    echo "    context: \"$context\"" >> "$PATTERNS_FILE.tmp"
    echo "    solution: \"$solution\"" >> "$PATTERNS_FILE.tmp"
    echo "    confidence: $confidence" >> "$PATTERNS_FILE.tmp"
    echo "    learned_at: $(date -Iseconds)" >> "$PATTERNS_FILE.tmp"
    
    echo "✅ Error pattern recorded: $error_type"
}

# Function to record success pattern
record_success() {
    local action="$1"
    local context="$2"
    local outcome="$3"
    local confidence="$4"
    
    # Add to patterns file
    echo "  - type: success" >> "$PATTERNS_FILE.tmp"
    echo "    action: \"$action\"" >> "$PATTERNS_FILE.tmp"
    echo "    context: \"$context\"" >> "$PATTERNS_FILE.tmp"
    echo "    outcome: \"$outcome\"" >> "$PATTERNS_FILE.tmp"
    echo "    confidence: $confidence" >> "$PATTERNS_FILE.tmp"
    echo "    learned_at: $(date -Iseconds)" >> "$PATTERNS_FILE.tmp"
    
    echo "✅ Success pattern recorded: $action"
}

# Function to generate heuristic from patterns
generate_heuristic() {
    local pattern_type="$1"
    local condition="$2"
    local action="$3"
    
    # Add to heuristics
    echo "  - if: \"$condition\"" >> "$HEURISTICS_FILE.tmp"
    echo "    then: \"$action\"" >> "$HEURISTICS_FILE.tmp"
    echo "    type: \"$pattern_type\"" >> "$HEURISTICS_FILE.tmp"
    echo "    confidence: 0.5" >> "$HEURISTICS_FILE.tmp"
    echo "    uses: 0" >> "$HEURISTICS_FILE.tmp"
    echo "    created_at: $(date -Iseconds)" >> "$HEURISTICS_FILE.tmp"
    
    echo "✅ Heuristic generated: IF $condition THEN $action"
}

# Function to analyze recent errors for patterns
analyze_patterns() {
    echo "## Pattern Analysis"
    
    # Count error types
    local error_count=$(grep -c "type: error" "$PATTERNS_FILE" 2>/dev/null || echo 0)
    local success_count=$(grep -c "type: success" "$PATTERNS_FILE" 2>/dev/null || echo 0)
    
    echo "Errors recorded: $error_count"
    echo "Successes recorded: $success_count"
    
    # Find repeated patterns
    if [ "$error_count" -gt 0 ]; then
        echo ""
        echo "### Most Common Errors:"
        grep "pattern:" "$PATTERNS_FILE" 2>/dev/null | sort | uniq -c | sort -rn | head -5
    fi
    
    # Calculate accuracy
    local total=$((error_count + success_count))
    if [ "$total" -gt 0 ]; then
        local accuracy=$((success_count * 100 / total))
        echo ""
        echo "Success rate: $accuracy%"
    fi
}

# Main execution
case "$1" in
    error)
        record_error "$2" "$3" "$4" "$5"
        ;;
    success)
        record_success "$2" "$3" "$4" "$5"
        ;;
    heuristic)
        generate_heuristic "$2" "$3" "$4"
        ;;
    analyze)
        analyze_patterns
        ;;
    *)
        echo "Usage: $0 {error|success|heuristic|analyze} [args...]"
        echo ""
        echo "Examples:"
        echo "  $0 error 'connection_timeout' 'API call' 'retry with backoff' 0.8"
        echo "  $0 success 'spawn_coder' 'code_review' 'completed' 0.9"
        echo "  $0 heuristic 'error' 'connection_timeout' 'retry with exponential backoff'"
        echo "  $0 analyze"
        exit 1
        ;;
esac