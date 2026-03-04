#!/bin/bash
# Script de configuração do T620 para acesso remoto e PXE server
# Execute no console físico do T620

echo "=========================================="
echo "CONFIGURANDO T620 - CLUSTER MASTER"
echo "=========================================="
echo ""

# Verificar se é root
if [ "$EUID" -ne 0 ]; then 
  echo "Execute como root (sudo -i)"
  exit 1
fi

echo "1. Configurando firewall para permitir SSH de qualquer origem..."
# Desabilitar firewall temporariamente
ufw disable 2>/dev/null || echo "ufw não encontrado"
systemctl stop firewalld 2>/dev/null || echo "firewalld não encontrado"

# Liberar SSH no iptables
iptables -F INPUT 2>/dev/null || echo "iptables não disponível"
iptables -P INPUT ACCEPT 2>/dev/null

echo "2. Verificando configuração do SSH..."
# Backup do sshd_config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d)

# Habilitar login por senha
sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication/PasswordAuthentication/' /etc/ssh/sshd_config
sed -i 's/^PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# Reiniciar SSH
systemctl restart sshd 2>/dev/null || service ssh restart 2>/dev/null || echo "Falha ao reiniciar SSH"

echo "3. Adicionando rota para MGMT-NET (192.168.1.0/24)..."
# Adicionar rota
ip route add 192.168.1.0/24 via 10.10.20.1 2>/dev/null || echo "Rota já existe ou falhou"

# Tornar rota persistente
if [ -f /etc/network/interfaces ]; then
  grep -q "192.168.1.0/24" /etc/network/interfaces || \
  echo "up ip route add 192.168.1.0/24 via 10.10.20.1" >> /etc/network/interfaces
fi

echo "4. Verificando interfaces de rede..."
ip addr show
echo ""
echo "5. Verificando bond0..."
if [ -f /sys/class/net/bond0/bonding/slaves ]; then
  echo "Slaves do bond0: $(cat /sys/class/net/bond0/bonding/slaves)"
else
  echo "bond0 não encontrado!"
fi

echo ""
echo "6. Testando conectividade..."
ping -c 2 10.10.20.1 && echo "✓ Gateway OK" || echo "✗ Gateway falhou"
ping -c 2 192.168.1.99 && echo "✓ FortiGate OK" || echo "✗ FortiGate falhou"

echo ""
echo "=========================================="
echo "CONFIGURAÇÃO CONCLUÍDA!"
echo "=========================================="
echo ""
echo "Agora teste do seu laptop:"
echo "  ssh csilva@10.10.20.11"
echo "  Senha: 230612"
echo ""
echo "Se ainda não funcionar, verifique:"
echo "  - Se o SSH está rodando: systemctl status sshd"
echo "  - Logs do SSH: journalctl -u sshd -n 20"
echo "  - Se há outras regras de firewall: iptables -L -n"
echo ""
