# Digital Twin Drone - Instalação Nativa (RHEL 10)

## Status
O build Docker travou (timeout/dependências). Recomenda-se instalação nativa.

## Por que instalação nativa?
1. Sua máquina tem recursos suficientes (i9-12900HX, 62GB RAM, RTX 4060)
2. RHEL 10 é compatível com Ubuntu via DNF
3. Evita overhead do Docker
4. Build mais rápido (sem camadas Docker)

## Instalação Rápida

```bash
# 1. Instalar Gazebo Harmonic
sudo dnf install -y gz-harmonic || \
  sudo dnf copr enable -y @openrobotics/gazebo && \
  sudo dnf install -y gz-harmonic

# 2. Compilar ArduPilot SITL
cd ~
git clone --depth 1 --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
./waf configure --board=sitl
./waf copter

# 3. Instalar pymavlink
pip3 install --user pymavlink matplotlib numpy

# 4. Adicionar ao ~/.bashrc
echo 'export PATH=$HOME/ardupilot/build/sitl/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 5. Testar
arducopter --version
```

## Próximos Passos

Após instalação nativa:

1. **Testar SITL único:**
   ```bash
   cd ~/ardupilot
   ./build/sitl/bin/arducopter -S -I0 --home -27.000000,152.000000,0,0 --model JSON
   ```

2. **Testar multi-instância:**
   ```bash
   # Terminal 1: SITL #1
   ./build/sitl/bin/arducopter -S -I0 --home -27.000000,152.000000,0,0 \
       --model JSON --sysid 1 -A udp:127.0.0.1:14550

   # Terminal 2: SITL #2
   ./build/sitl/bin/arducopter -S -I1 --home -27.000000,152.000000,0,0 \
       --model JSON --sysid 2 -A udp:127.0.0.1:14551
   ```

3. **Executar Bridge:**
   ```bash
   cd ~/.openclaw/workspace/digital-twin-drone
   python3 src/dt_bridge.py
   ```

## Alternativa: Ubuntu em VM/WSL2

Se RHEL não funcionar bem com Gazebo:
1. Instalar Ubuntu 22.04 em VM ou WSL2
2. Seguir as instruções do Dockerfile dentro da VM