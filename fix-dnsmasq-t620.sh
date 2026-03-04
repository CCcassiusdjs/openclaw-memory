#!/bin/bash
# Script para corrigir dnsmasq no T620
# Execute como root ou com sudo

echo "=== Corrigindo dnsmasq PXE Boot ==="

# 1. Remover config errada
rm -f /etc/dnsmasq.d/pxe-boot.conf

# 2. Criar config correta
cat > /etc/dnsmasq.d/pxe-boot.conf << 'DNSEOF'
interface=bond0
bind-interfaces
dhcp-range=10.10.20.100,10.10.20.200,255.255.255.0,12h
dhcp-option=3,10.10.20.11
dhcp-option=6,8.8.8.8,8.8.4.4
enable-tftp
tftp-root=/var/lib/tftpboot
dhcp-boot=pxelinux.0
log-dhcp
log-queries
tftp-mtu=1408
DNSEOF

echo "✓ Configuração criada"

# 3. Testar
dnsmasq --test && echo "✓ Config OK" || echo "✗ Config com erro"

# 4. Reiniciar dnsmasq
systemctl restart dnsmasq
sleep 2

# 5. Verificar status
systemctl status dnsmasq --no-pager | head -6

# 6. Verificar portas
echo ""
echo "Portas escutando:"
netstat -ulnp 2>/dev/null | grep -E ":(67|69)" || echo "dnsmasq não escutando"

# 7. Testar TFTP
echo ""
echo "Testando TFTP:"
cd /tmp && rm -f test-pxe.bin
echo "get pxelinux.0 test-pxe.bin" | tftp 127.0.0.1 2>&1
ls -la test-pxe.bin 2>/dev/null && echo "✓ TFTP OK" || echo "⚠ TFTP falhou"

echo ""
echo "=== Configuração concluída ==="
echo "Para monitorar PXE boot: ~/monitor-pxe.sh"
echo "Ou: watch -n 2 cat /var/lib/dnsmasq.leases"
