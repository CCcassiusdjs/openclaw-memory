# Digital Twin Drone - Setup Rápido (Alternativa ao Docker)

Se o Docker apresentar problemas com GPU ou display, você pode instalar nativamente:

## Ubuntu 22.04+ / RHEL 10

### 1. Instalar Gazebo Harmonic

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y wget lsb-release gnupg

# Adicionar repositório OSRF
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

sudo apt-get update
sudo apt-get install -y gz-harmonic
```

```bash
# RHEL/Fedora
sudo dnf install -y dnf-plugins-core
sudo dnf copr enable -y @openrobotics/gazebo
sudo dnf install -y gz-harmonic
```

### 2. Compilar ArduPilot SITL

```bash
# Clonar
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot

# Dependências (Ubuntu)
sudo apt-get install -y python3-pip
pip3 install --user pymavlink matplotlib numpy

# Compilar
./waf configure --board=sitl
./waf copter
```

### 3. Plugin ardupilot_gazebo

```bash
git clone https://github.com/ArduPilot/ardupilot_gazebo.git
cd ardupilot_gazebo
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr
make -j$(nproc)
sudo make install
```

### 4. Variáveis de Ambiente

```bash
# Adicionar ao ~/.bashrc
export GZ_SIM_RESOURCE_PATH=/opt/ardupilot_gazebo/models:/opt/ardupilot_gazebo/worlds
export GZ_SIM_PLUGIN_PATH=/opt/ardupilot_gazebo/build
export PATH=$HOME/ardupilot/build/sitl/bin:$PATH
```

### 5. Testar

```bash
# Terminal 1: Gazebo
gz sim -g worlds/iris_arducopter_runway.sdf

# Terminal 2: SITL
cd ~/ardupilot
./build/sitl/bin/arducopter -S -I0 --home -27.000000,152.000000,0,0 --model JSON --speedup 1
```

## Alternativa: Docker com GPU

```bash
# Verificar se NVIDIA Container Toolkit está configurado
docker run --rm --gpus all nvidia/cuda:12-base nvidia-smi

# Se funcionar, o docker-compose deve usar GPU automaticamente
```