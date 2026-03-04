#!/bin/bash

# Script para conectar ao switch HP V1910 usando tio em modo interativo
PORT="/dev/ttyUSB0"
BAUD="38400"

echo "=== Conexão Switch HP V1910 via TIO ==="
echo "Porta: $PORT | Baud: $BAUD"
echo ""
echo "Iniciando tio em modo interativo..."
echo "Digite os comandos manualmente ou aguarde a automação"
echo ""
echo "Para sair: Ctrl+Z"
echo ""

# tio em modo interativo - os comandos são digitados diretamente na sessão
tio -b $BAUD $PORT
