#!/bin/bash

# Script para conectar ao switch HP V1910 usando tio
# Tio é mais simples e direto para conexões seriais

PORT="/dev/ttyUSB0"
BAUD="38400"

echo "=== Conexão Switch HP V1910 via TIO ==="
echo "Porta: $PORT"
echo "Baud: $BAUD"
echo ""
echo "Iniciando conexão..."
echo ""

# tio mantém a sessão e permite digitar diretamente
# Para sair: Ctrl+Z
tio -b $BAUD $PORT &

TIO_PID=$!
sleep 2

echo "Sessão tio iniciada (PID: $TIO_PID)"
echo ""
echo "Agora enviando comandos automaticamente..."
sleep 3

# Enviar comandos via /dev/ttyUSB0 diretamente
exec 3<>$PORT

# Configurar porta serial
stty -F $PORT $BAUD raw -echo

# Login
echo "Enviando login..."
echo -n "admin" >&3
sleep 1
echo "" >&3
sleep 2

# Senha
echo "Enviando senha..."
echo -n "admin" >&3
sleep 1
echo "" >&3
sleep 2

# Cmdline mode
echo "Enviando _cmdline-mode on..."
echo -n "_cmdline-mode on" >&3
sleep 1
echo "" >&3
sleep 2

# Confirmação
echo "Enviando confirmação (y)..."
echo -n "y" >&3
sleep 1
echo "" >&3
sleep 2

# Código
echo "Enviando código 512900..."
echo -n "512900" >&3
sleep 1
echo "" >&3

echo ""
echo "=== Comandos enviados! ==="
echo "A sessão tio está ativa. Digite comandos diretamente."
echo "Para sair do tio: Ctrl+Z"
echo ""

# Manter script rodando para a sessão tio
wait $TIO_PID
