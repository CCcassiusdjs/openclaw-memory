#!/bin/bash
# Script para compilar e executar o analisador léxico

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║             ANALISADOR LÉXICO - JFlex                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Criar diretório de build
mkdir -p build

# Compilar
echo "📦 Gerando Lexer com JFlex..."
jflex --quiet -d build src/Lexer.flex

echo "📦 Compilando Java..."
javac -d build src/Main.java build/Lexer.java

echo ""
echo "✅ Compilação concluída!"
echo ""

# Executar teste
echo "══════════════════════════════════════════════════════════════════"
echo "                    EXECUTANDO TESTE                              "
echo "══════════════════════════════════════════════════════════════════"
echo ""

cd build
java Main --test

echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "                    ANÁLISE CONCLUÍDA                            "
echo "══════════════════════════════════════════════════════════════════"