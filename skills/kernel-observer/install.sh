#!/bin/bash
#
# Install Kernel Observer Skill
#
# This script installs bpftrace and sets up the kernel observer skill.
#
# Usage: sudo ./install.sh
#

set -e

echo "=== Kernel Observer Skill Installation ==="

# Check kernel version
KERNEL_VERSION=$(uname -r)
echo "[1/6] Kernel version: $KERNEL_VERSION"

# Check BPF support
echo "[2/6] Checking BPF support..."
if ! grep -q "CONFIG_BPF_SYSCALL=y" /boot/config-$KERNEL_VERSION 2>/dev/null; then
    echo "ERROR: BPF syscall support not enabled in kernel"
    exit 1
fi
echo "  ✓ BPF syscall support enabled"

if ! grep -q "CONFIG_BPF_JIT=y" /boot/config-$KERNEL_VERSION 2>/dev/null; then
    echo "WARNING: BPF JIT not enabled (performance may be reduced)"
else
    echo "  ✓ BPF JIT enabled"
fi

# Install dependencies
echo "[3/6] Installing dependencies..."
if command -v dnf &>/dev/null; then
    sudo dnf install -y bpftrace bpftool
elif command -v apt &>/dev/null; then
    sudo apt update && sudo apt install -y bpftrace linux-tools-$(uname -r)
elif command -v pacman &>/dev/null; then
    sudo pacman -S bpftrace bpftrace-tools
else
    echo "ERROR: Unsupported package manager"
    exit 1
fi
echo "  ✓ Dependencies installed"

# Make scripts executable
echo "[4/6] Setting permissions..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$SCRIPT_DIR/scripts"/*.bt
chmod +x "$SCRIPT_DIR/bridge.js"
echo "  ✓ Scripts made executable"

# Test bpftrace
echo "[5/6] Testing bpftrace..."
if ! sudo bpftrace -e 'BEGIN { printf("bpftrace working!\n"); exit(); }' 2>/dev/null; then
    echo "ERROR: bpftrace test failed"
    exit 1
fi
echo "  ✓ bpftrace working"

# Create log directory
echo "[6/6] Creating directories..."
mkdir -p "$SCRIPT_DIR/logs"
touch "$SCRIPT_DIR/events.log"
echo "  ✓ Directories created"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Usage:"
echo "  sudo bpftrace scripts/syscalls.bt    # Monitor syscalls"
echo "  sudo bpftrace scripts/files.bt       # Monitor file access"
echo "  sudo bpftrace scripts/network.bt     # Monitor network"
echo "  sudo bpftrace scripts/processes.bt    # Monitor processes"
echo "  sudo bpftrace scripts/full.bt         # Monitor everything"
echo ""
echo "  sudo node bridge.js --scope=all      # Start bridge to Gateway"
echo ""
echo "See SKILL.md for detailed documentation."