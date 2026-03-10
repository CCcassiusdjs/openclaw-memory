# EKF2 Estimation System - ArduPilot Dev Docs

**Fonte:** https://ardupilot.org/dev/docs/ekf2-estimation-system.html  
**Tipo:** Documentação Oficial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~30min

---

## 📋 Resumo Executivo

O EKF2 é um **Extended Kalman Filter de 24 estados** implementado na biblioteca `AP_NavEKF2` do ArduPilot. Estima posição, velocidade, atitude e vários biases/calibrações de sensores.

---

## 🎯 Estados Estimados (24 estados)

| Categoria | Estados | Descrição |
|-----------|---------|-----------|
| **Atitude** | Quaternions (4) | Orientação do veículo |
| **Velocidade** | VN, VE, VD (3) | Velocidade NED (North, East, Down) |
| **Posição** | PN, PE, PD (3) | Posição NED |
| **Bias do Giro** | GX, GY, GZ (3) | Offset do giroscópio |
| **Escala do Giro** | GSX, GSY, GSZ (3) | Fator de escala do giroscópio |
| **Bias Acel.** | AZbias (1) | Bias do acelerômetro no eixo Z |
| **Campo Mag. Terra** | MN, ME, MD (3) | Campo magnético terrestre |
| **Campo Mag. Corpo** | MX, MY, MZ (3) | Campo magnético no frame do corpo |
| **Vento** | VWN, VWE (2) | Velocidade do vento NED |
| **Total** | **24 estados** | |

---

## ✅ Vantagens do EKF2

1. **Múltiplos IMUs** - Roda EKF separado para cada IMU (melhor recuperação de falhas)
2. **Troca de magnetômetro** - Pode alternar entre magnetômetros em caso de falha
3. **Estimação de escala do giro** - Melhora precisão em manobras de alta taxa
4. **Inicialização em movimento** - Não depende do algoritmo DCM para orientação inicial
5. **Maior tolerância a bias do giro** - Lida com mudanças maiores em voo
6. **Recuperação mais rápida** - De dados de sensor ruins
7. **Output mais suave** - E levemente mais preciso
8. **Menor custo computacional** - Otimizações de código

---

## 🔧 Como Funciona

### Rotação de Erro (Error Rotation Vector)
- Em vez de estimar quaternion diretamente, estima um **vetor de rotação de erro**
- Aplica correção ao quaternion das equações de navegação inercial
- Melhor para grandes erros de ângulo (evita linearização de quaternion)
- Baseado em: "Rotation Vector in Attitude Estimation" - Mark E. Pittelkau (2003)

### Delayed Time Horizon
- EKF roda em um horizonte de tempo atrasado
- Medições são fundidas usando estados e covariância do mesmo instante
- Estados atrasados são preditos para tempo atual via filtro complementar
- Inspirado em: "Recursive Attitude Estimation in the Presence of Multi-rate and Multi-delay Vector Measurements" - Khosravian et al. (2015)

---

## 📊 Log Data (NKF1-NKF5)

| Packet | Conteúdo |
|--------|----------|
| **NKF1** | Outputs para controle de voo (roll, pitch, yaw, velocidade, posição, gyro bias) |
| **NKF2** | Estados adicionais (accel bias, gyro scale, vento, campo mag) |
| **NKF3** | Inovações (diferença entre predição e medição) |
| **NKF4** | Health e status (test ratios, erros) |
| **NKF5** | Optical flow e range finder |

### Test Ratios (NKF4)
- Valor < 1: medição passou nas verificações
- Valor > 1: medição rejeitada
- Valor < 0.3 em voo = típico para sensores de boa qualidade

---

## ⚙️ Parâmetros Principais

### Habilitação
```
EK2_ENABLE = 1    # Liga EKF2
AHRS_EKF_TYPE = 2 # Usa EKF2 para controle
EK2_IMU_MASK = 3  # Usa IMU1 e IMU2 (dual EKF)
```

### GPS
- `EK2_GPS_TYPE` - Tipo de uso GPS (0: 3D vel + 2D pos, 1: 2D vel + 2D pos, etc.)
- `EK2_VELNE_NOISE` - Ruído de velocidade horizontal GPS
- `EK2_POSNE_NOISE` - Ruído de posição horizontal GPS
- `EK2_GLITCH_RAD` - Raio máximo de glitch GPS antes de reset

### Altitude
- `EK2_ALT_SOURCE` - Fonte de altitude (0: Baro, 1: Range Finder, 2: GPS)
- `EK2_ALT_NOISE` - Ruído de altitude

### Magnetômetro
- `EK2_MAG_CAL` - Quando calibrar (0: airborne, 1: maneuvering, 2: never, 3: first in-air, 4: always)
- `EK2_MAG_GATE` - Gate de consistência

### Ruído de Processo
- `EK2_GYRO_PNOISE` - Ruído de processo do giro (confiança no gyro)
- `EK2_ACC_PNOISE` - Ruído de processo do acelerômetro
- `EK2_GBIAS_PNOISE` - Taxa de aprendizado do bias do giro

---

## 💡 Conceitos-Chave

### Innovation (Inovação)
- Diferença entre valor predito pelo EKF e valor medido pelo sensor
- Inovações pequenas = menor erro do sensor
- IMU ruim pode causar inovações grandes em todas as medições

### Test Ratio
- Razão entre inovação e variância esperada
- < 1 = medição aceita
- > 1 = medição rejeitada

### GPS Checks (EK2_GPS_CHECK)
Bitmask para verificações pré-voo:
- Bit 0: >= 6 satélites
- Bit 1: HDoP >= 2.5
- Bit 2: Speed accuracy < 1.0 m/s
- Bit 3: Position accuracy < 5.0 m
- Bit 4: Magnetometer checks passing
- Bits 5-7: Drift checks

---

## 🔗 Referências

- Pittelkau, M.E. (2003). "Rotation Vector in Attitude Estimation", Journal of Guidance, Control, and Dynamics
- Khosravian, A. et al. (2015). "Recursive Attitude Estimation in the Presence of Multi-rate and Multi-delay Vector Measurements"
- GitHub: priseborough/InertialNav - Derivações matemáticas

---

## 📝 Anotações Pessoais

- EKF2 é mais simples que EKF3, mas ainda muito capaz
- Delayed time horizon é uma técnica interessante para lidar com latência de sensores
- Múltiplos IMUs é uma grande vantagem para redundância
- Parâmetros EK2_* vs EK3_* para EKF3