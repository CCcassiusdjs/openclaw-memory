#!/bin/bash
# Teste do JFlex - Compilação e Execução

set -e

WORKDIR="/home/csilva/.openclaw/workspace/jflex_test"
cd "$WORKDIR"

echo "=== COMPILANDO SCANNER JFLEX ==="

# Limpar arquivos anteriores
rm -f Scanner.java Scanner.class

# Gerar scanner Java
jflex --verbose exemplo.flex

echo ""
echo "=== COMPILANDO JAVA ==="

# Compilar o scanner gerado
javac Scanner.java

echo ""
echo "=== TESTE 1: Números e Palavras ==="
echo "123 abc 456.78 xyz + - * / =" | java Scanner

echo ""
echo "=== TESTE 2: Código Simples ==="
cat << 'EOF' | java Scanner
int x = 10;
float y = 20.5;
if (x < y) {
    return x + y;
}
EOF

echo ""
echo "=== TESTE 3: Erros ==="
echo "abc @#\$ 123" | java Scanner

echo ""
echo "✅ TESTES CONCLUÍDOS!"