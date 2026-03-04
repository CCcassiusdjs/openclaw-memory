#!/bin/bash

# Script para conectar ao switch HP V1910 via serial
# Uso: ./hp_connect.sh

PORT="/dev/ttyUSB0"
BAUD="38400"

echo "Conectando ao switch HP em $PORT ($BAUD baud)..."
echo "Usuario: admin"
echo "Senha: admin"
echo ""
echo "Comandos a executar:"
echo "  _cmdline-mode on"
echo "  y"
echo "  512900"
echo ""
echo "Pressione Ctrl+A, K para sair do screen"
echo ""

# Iniciar sessao screen
screen $PORT $BAUD
