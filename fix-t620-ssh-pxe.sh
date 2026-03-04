#!/bin/bash
# Script para corrigir SSH e PXE no T620
# Executar como root ou com sudo

echo "=== Corrigindo configuração T620 Cluster Head ==="

# 1. Liberar SSH no firewall
echo "Liberando SSH no firewall..."
firewall-cmd --permanent --add-service=ssh 2>/dev/null
firewall-cmd --permanent --add-service=dhcp 2>/dev/null
firewall-cmd --permanent --add-service=tftp 2>/dev/null
firewall-cmd --permanent --add-service=dns 2>/dev/null
firewall-cmd --reload 2>/dev/null

# 2. Liberar portas manualmente (iptables)
echo "Liberando portas no iptables..."
iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT
iptables -I INPUT 1 -p udp --dport 67:68 -j ACCEPT
iptables -I INPUT 1 -p udp --dport 69 -j ACCEPT
iptables -I INPUT 1 -p udp --dport 4011 -j ACCEPT
iptables -I INPUT 1 -p udp --dport 53 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT

# 3. Desabilitar SELinux temporariamente
echo "Configurando SELinux..."
setenforce 0
setsebool -P tftp_anon_write 1 2>/dev/null
setsebool -P dnsmasq_use_tftp 1 2>/dev/null

# 4. Reiniciar dnsmasq
echo "Reiniciando dnsmasq..."
systemctl restart dnsmasq

# 5. Verificar serviços
echo ""
echo "=== Status dos serviços ==="
systemctl is-active sshd
systemctl is-active dnsmasq
getenforce

echo ""
echo "=== Configuração concluída ==="
echo "SSH e PXE boot devem estar funcionando agora."
