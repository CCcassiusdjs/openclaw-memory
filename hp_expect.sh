#!/usr/bin/expect -f

# Script expect para automatizar conexão ao switch HP V1910
# Via conexão serial direta (sem UI automation)

set timeout 45
set port "/dev/ttyUSB0"
set baud 38400

puts "=== Conexão Switch HP V1910 via Expect ==="
puts "Porta: $port | Baud: $baud"
puts ""

# Iniciar conexão com tio em modo background
spawn tio -b $baud $port

# Aguardar conexão estabelecer
sleep 2

puts "Enviando comandos..."

# Enviar login
send "admin\r"
sleep 1

# Enviar senha
send "admin\r"
sleep 2

# Enviar comando cmdline-mode
send "_cmdline-mode on\r"
sleep 2

# Enviar confirmação
send "y\r"
sleep 2

# Enviar código de ativação
send "512900\r"
sleep 1

puts ""
puts "=== Comandos enviados! ==="
puts "Sessão mantida aberta para interação"
puts "Para sair: Ctrl+Z"
puts ""

# Manter sessão aberta
interact
