# Métodos Matemáticos para Reconstrução de Trajetória

## Análise de Fórmulas e Técnicas Disponíveis

---

## 1. Dead Reckoning por Dupla Integração

### Fórmula Fundamental

A estimativa de posição por dead reckoning usa a **segunda lei de Newton**:

```
a(t) = d²x/dt²  →  x(t) = ∫∫ a(t) dt²
```

**Integração dupla:**
```
v(t) = v₀ + ∫₀ᵗ a(τ) dτ
x(t) = x₀ + ∫₀ᵗ v(τ) dτ = x₀ + v₀t + ∫₀ᵗ∫₀ᵗ a(τ) dτ²
```

### Erro Acumulado (Drift)

O erro de posição cresce com o **tempo ao cubo**:

```
σ_position(t) = √(N/3) × a_noise × t^1.5
```

Ou mais precisamente:
```
ε_position(t) = ε_accel × t² / 2 + ε_gyro × t³ / 6
```

**Referência:** *"Position estimation cannot be performed with adequate accuracy for periods longer than a few seconds"* — arXiv:1311.4572

### Implementação com Dados Disponíveis

```python
def dead_reckoning_position(accel_data, dt, initial_pos=(0, 0, 0)):
    """
    Estima posição por dupla integração do acelerômetro.
    
    ERRO ESPERADO:
    - Após 1s:  ~0.1m (tolerável)
    - Após 5s:  ~2.5m (marginal)
    - Após 10s: ~10m (inutilizável)
    """
    velocity = np.zeros(3)
    position = np.array(initial_pos)
    
    for accel in accel_data:
        # Remover gravidade (assumir que Z aponta para baixo)
        accel_corrected = accel - np.array([0, 0, 9.81])
        
        # Integração 1: aceleração → velocidade
        velocity += accel_corrected * dt
        
        # Integração 2: velocidade → posição
        position += velocity * dt
    
    return position
```

### Limitações para Este Caso

| Fator | Valor | Impacto |
|-------|-------|---------|
| Duração do voo | ~10s | Erro ~10m |
| Drone em hover | Aceleração ≈ 0 | Deriva dominante |
| Sem referência externa | Sem correção | Erro acumula |
| IMU com ruído | ~0.01 m/s² | Cresce com t² |

**Conclusão:** Dead reckoning é **impraticável** para durações > 5s.

---

## 2. Estimação de Atitude por Sensores

### Fórmula: Acelerômetro como Inclinômetro

Quando o drone está **parado** (hover), o acelerômetro mede apenas a gravidade:

```
roll = atan2(ay, az)
pitch = atan2(-ax, sqrt(ay² + az²))
```

**Premissa:** O drone está em hover estático, então:
- `ax ≈ 0` (sem aceleração lateral)
- `ay ≈ 0` (sem aceleração longitudinal)
- `az ≈ -9.81 m/s²` (gravidade)

### Fórmula: Magnetômetro para Yaw

```
yaw = atan2(mag_y, mag_x) - mag_declination
```

Onde:
- `mag_x, mag_y` = campo magnético medido
- `mag_declination` = declinação magnática local

### Implementação

```python
def estimate_attitude(accel, mag, mag_declination=0):
    """
    Estima atitude a partir de acelerômetro e magnetômetro.
    
    PREMISSA: Drone em hover estático ou movimento lento.
    
    PRECISÃO:
    - Roll/Pitch: ±0.5° (se estático)
    - Yaw: ±5° (depende de calibração mag)
    """
    # Roll e Pitch (acelerômetro)
    roll = np.arctan2(accel[1], accel[2])
    pitch = np.arctan2(-accel[0], np.sqrt(accel[1]**2 + accel[2]**2))
    
    # Yaw (magnetômetro)
    # Rotacionar para o frame do drone
    mag_x = mag[0] * np.cos(pitch) + mag[2] * np.sin(pitch)
    mag_y = mag[0] * np.sin(roll) * np.sin(pitch) + \
            mag[1] * np.cos(roll) - \
            mag[2] * np.sin(roll) * np.cos(pitch)
    
    yaw = np.arctan2(mag_y, mag_x) - mag_declination
    
    return roll, pitch, yaw
```

### Limitações

| Fator | Impacto |
|-------|---------|
| Movimento do drone | Roll/pitch ficam incorretos |
| Calibração do mag | Yaw pode ter erro de 10-30° |
| Interferência magnética | Yaw incorreto |

---

## 3. Filtro de Kalman Estendido (EKF)

### Estados do EKF3 do ArduPilot

O EKF3 estima **24 estados**:

```
x = [position_NED(3), velocity_NED(3), quaternion(4), 
     gyro_bias(3), accel_bias(3), mag_bias(3), 
     wind(2), terrain(2), ...]
```

### Equações do EKF

**Predição:**
```
x̂ₖ|ₖ₋₁ = f(x̂ₖ₋₁, uₖ)      # Predição do estado
Pₖ|ₖ₋₁ = Fₖ Pₖ₋₁ Fₖᵀ + Qₖ  # Covariância predita
```

**Correção:**
```
Kₖ = Pₖ|ₖ₋₁ Hₖᵀ (Hₖ Pₖ|ₖ₋₁ Hₖᵀ + Rₖ)⁻¹  # Ganho de Kalman
x̂ₖ = x̂ₖ|ₖ₋₁ + Kₖ (zₖ - Hₖ x̂ₖ|ₖ₋₁)      # Estado corrigido
Pₖ = (I - Kₖ Hₖ) Pₖ|ₖ₋₁                 # Covariância corrigida
```

### Implementação Simplificada

```python
class SimpleEKF:
    """
    EKF simplificado para estimar posição e velocidade.
    
    ENTRADA:
    - IMU (accel, gyro)
    - GPS (posição, velocidade) - quando disponível
    - Baro (altitude)
    
    SAÍDA:
    - Posição NED
    - Velocidade NED
    - Quaternion (atitude)
    """
    
    def __init__(self):
        # Estado: [pos_N, pos_E, pos_D, vel_N, vel_E, vel_D]
        self.x = np.zeros(6)
        self.P = np.eye(6) * 0.1  # Covariância inicial
        
        # Ruído do processo
        self.Q = np.eye(6) * 0.01
        
        # Ruído de medição
        self.R_gps = np.eye(3) * 2.0     # GPS: 2m RMS
        self.R_baro = np.eye(1) * 0.5    # Baro: 0.5m RMS
    
    def predict(self, accel, gyro, dt):
        """
        Predição baseada em IMU.
        
        NOTA: Sem correção externa, erro cresce rapidamente.
        """
        # Matriz de transição
        F = np.eye(6)
        F[0:3, 3:6] = np.eye(3) * dt
        
        # Predição do estado
        self.x[3:6] += accel * dt  # velocidade
        self.x[0:3] += self.x[3:6] * dt  # posição
        
        # Predição da covariância
        self.P = F @ self.P @ F.T + self.Q
        
        return self.x.copy()
    
    def correct_gps(self, pos_gps):
        """
        Correção com GPS.
        
        DISPONIBILIDADE: Conforme flags do output vector.
        """
        H = np.zeros((3, 6))
        H[0:3, 0:3] = np.eye(3)
        
        K = self.P @ H.T @ np.linalg.inv(H @ self.P @ H.T + self.R_gps)
        
        self.x += K @ (pos_gps - H @ self.x)
        self.P = (np.eye(6) - K @ H) @ self.P
        
        return self.x.copy()
    
    def correct_baro(self, alt_baro):
        """
        Correção com barômetro.
        
        DISPONIBILIDADE: Conforme flags do output vector.
        """
        H = np.zeros((1, 6))
        H[0, 2] = 1  # pos_D
        
        K = self.P @ H.T @ np.linalg.inv(H @ self.P @ H.T + self.R_baro)
        
        z = np.array([alt_baro])
        self.x += K @ (z - H @ self.x)
        self.P = (np.eye(6) - K @ H) @ self.P
        
        return self.x.copy()
```

### Problema Fundamental

O EKF precisa de **medições externas** (GPS, baro, mag) para corrigir a deriva do IMU.

**Sem GPS/Baro/Mag corretos:**
```
Erro após t segundos = O(t²)
```

---

## 4. Análise do Que Está Disponível

### Dados de Groundtruth

| Dado | Disponível? | Frequência | Qualidade |
|------|-------------|------------|-----------|
| IMU (accel, gyro) | ✅ Sim | 400 Hz | Alta |
| GPS (lat, lng, alt) | ✅ Sim | 5 Hz | Alta |
| Baro (altitude) | ✅ Sim | 50 Hz | Alta |
| Mag (campo) | ✅ Sim | 50 Hz | Alta |
| PWM (controle) | ✅ Sim | 400 Hz | Alta |

### Dados de Output

| Dado | Disponível? | Significado |
|------|-------------|-------------|
| `ekf_flags` | ✅ Sim | Quais sensores completaram |
| `pos_error_ned_m[3]` | ⚠️ Parcial | Flags de status, NÃO posição |
| `att_error_rpy_deg[3]` | ⚠️ Parcial | Flags de status, NÃO atitude |

### Cenário do Teste

**Groundtruth:** Drone em **hover estático** a ~10m de altitude.

```
Posição: Fixa (lat=-30.034647, lng=-51.217658)
Velocidade: Zero
Atitude: Neutra (roll≈0, pitch≈0, yaw arbitrário)
Aceleração: Zero (exceto gravidade = -9.81 m/s² em Z)
```

---

## 5. Métodos Práticos de Reconstrução

### Método 1: Groundtruth Direto (Mais Preciso)

**Premissa:** O drone está em hover estático.

```python
def reconstruct_groundtruth():
    """
    Reconstrução usando groundtruth como verdade absoluta.
    
    PREMISSA: Drone em hover estático.
    
    RESULTADO: Trajetória constante (ponto único).
    """
    position = np.array([0, 0, 10.0])  # NED: (0, 0, 10m)
    velocity = np.zeros(3)
    
    # A partir do groundtruth GPS
    lat = -30.034647
    lng = -51.217658
    alt = 100.0  # GPS altitude
    
    # A partir do groundtruth baro
    rel_alt = 10.0  # Altitude relativa
    
    # A partir do groundtruth IMU
    roll = 0.0  # Hover neutro
    pitch = 0.0
    yaw = estimate_yaw_from_mag(mag_data)
    
    return {
        'position': position,
        'velocity': velocity,
        'attitude': (roll, pitch, yaw)
    }
```

**Limitação:** Não mostra o que aconteceu **durante** a falha.

### Método 2: Dead Reckoning com Correção Inicial

```python
def reconstruct_with_groundtruth_initial(imu_data, groundtruth_pos):
    """
    Dead reckoning com correção usando groundtruth como inicial.
    
    LIMITAÇÃO:
    - Precisão inicial alta
    - Erro cresce com t²
    - Útil apenas por ~5 segundos
    """
    # Condição inicial conhecida
    pos = groundtruth_pos.copy()
    vel = np.zeros(3)
    
    trajectory = [pos.copy()]
    
    for accel, gyro, dt in imu_data:
        # Predição (dead reckoning)
        vel += accel * dt
        pos += vel * dt
        
        trajectory.append(pos.copy())
    
    return np.array(trajectory)
```

**Erro esperado:**
```
Após 1s:  ~0.05m
Após 5s:  ~1.25m
Após 10s: ~5m
```

### Método 3: Filtro Complementar (Atitude + Velocidade)

```python
def complementary_filter_position(accel_data, mag_data, dt):
    """
    Usa filtro complementar para atitude e assume velocidade zero.
    
    PREMISSA: Drone em hover (velocidade ≈ 0).
    
    RESULTADO:
    - Atitude estimada corretamente
    - Posição = constante (não há movimento)
    """
    # Estimar atitude
    roll, pitch, yaw = estimate_attitude(accel_data, mag_data)
    
    # Se o drone está em hover, a posição é constante
    # (a menos que haja vento ou erro de controle)
    
    # A única variação esperada é devido a:
    # 1. Ruído do sensor (filtrar)
    # 2. Vibração do motor (filtrar)
    # 3. Vento (desconhecido)
    
    return {
        'position': initial_position,  # Constante
        'velocity': np.zeros(3),       # Zero
        'attitude': (roll, pitch, yaw)  # Estimada
    }
```

---

## 6. O Que Pode Ser Feito

### 6.1 Reconstrução do Estado Inicial

Com os dados de groundtruth, podemos determinar com **alta precisão**:

| Parâmetro | Valor | Fonte |
|-----------|-------|-------|
| Posição NED | (0, 0, ~10m) | Baro |
| Posição GPS | (-30.034647, -51.217658, 100m) | GPS |
| Velocidade | (0, 0, 0) | Hover estático |
| Roll/Pitch | ~0° | IMU (acelerômetro em hover) |
| Yaw | Depende do mag | Magnetômetro |

### 6.2 Estimativa da Atitude Durante o Voo

**Possível com:** Filtro complementar ou EKF simplificado

```python
# Atitude pode ser estimada com IMU + Mag
attitude = estimate_attitude(accel_imu, mag_data)

# Precisão:
# - Roll/Pitch: ±0.5° (se hover estático)
# - Yaw: ±5° (depende de calibração)
```

### 6.3 Estimativa da Posição Durante o Voo

**NÃO é possível com precisão adequada** porque:

1. **Sem correção externa:** Erro cresce com t²
2. **Duração > 5s:** Erro > 1m
3. **Sem estado do EKF:** Não sabemos a correção aplicada

### 6.4 Reconstrução da Queda

**Possível com:** Física newtoniana

```python
def simulate_fall(initial_height, dt=0.01):
    """
    Simula a queda após falha.
    
    PREMISSA:
    - Drone em hover a altura h
    - Falha de software em t=0
    - Motores desligam (throttle=0)
    - Queda livre até o chão
    
    RESULTADO:
    - Tempo de queda: t = √(2h/g)
    - Velocidade impacto: v = √(2gh)
    - Energia: E = mgh
    """
    g = 9.81
    h = initial_height
    t_fall = np.sqrt(2 * h / g)
    v_impact = np.sqrt(2 * g * h)
    
    # Simular trajetória
    t = np.arange(0, t_fall, dt)
    h_t = h - 0.5 * g * t**2
    v_t = g * t
    
    return t, h_t, v_t
```

---

## 7. Conclusões Matemáticas

### Viabilidade por Parâmetro

| Parâmetro | Método | Viabilidade | Precisão |
|-----------|--------|-------------|----------|
| **Posição inicial** | Groundtruth | ✅ Alta | ±0.1m |
| **Velocidade inicial** | Premissa (hover) | ✅ Alta | 0 m/s |
| **Atitude inicial** | IMU + Mag | ✅ Alta | ±0.5° |
| **Posição durante voo** | Dead reckoning | ⚠️ Baixa | ±5m @ 10s |
| **Velocidade durante voo** | Dead reckoning | ⚠️ Baixa | ±1 m/s @ 10s |
| **Atitude durante voo** | Filtro complementar | ✅ Alta | ±1° |
| **Momento da falha** | Output flags | ❌ Não há timestamp |
| **Causa da falha** | Output flags | ❌ Não há traceback |

### Fórmulas Chave

1. **Erro de posição por dupla integração:**
   ```
   ε_position(t) = ε_accel × t² / 2
   ```

2. **Tempo de queda:**
   ```
   t_fall = √(2h/g)
   ```

3. **Velocidade de impacto:**
   ```
   v_impact = √(2gh) = gt_fall
   ```

4. **Energia de impacto:**
   ```
   E = ½mv² = mgh
   ```

5. **Roll/Pitch por acelerômetro:**
   ```
   roll = atan2(ay, az)
   pitch = atan2(-ax, √(ay² + az²))
   ```

6. **Yaw por magnetômetro:**
   ```
   yaw = atan2(mag_y, mag_x) - decl
   ```

---

## 8. Recomendação Final

### O que PODE ser feito:

1. **Reconstruir estado inicial** (com groundtruth)
2. **Estimar atitude** (com IMU + Mag)
3. **Simular queda** (com física newtoniana)
4. **Classificar falhas** (com output flags)

### O que NÃO PODE ser feito:

1. **Reconstruir trajetória real** (sem EKF state)
2. **Determinar momento exato da falha** (sem timestamp)
3. **Identificar causa raiz** (sem traceback)
4. **Mostrar dinâmica de voo** (sem estado estimado)

### Solução Recomendada para Testes Futuros

Habilitar logging do EKF:

```param
LOG_BACKEND_TYPE 1    # Binário
LOG_DISARMED 1        # Log mesmo desarmado
EK3_LOG_LEVEL 0       # Log completo do EKF3
```

Isso geraria logs com:
- EKF1: Posição, velocidade, atitude
- EKF2: Estados do magnetômetro
- EKF3: Estados do gyro/accel
- EKF4: Inovações e erros

---

*Documento gerado: 2026-03-07*
*Baseado em: Física newtoniana, Dead reckoning, EKF theory, ArduPilot documentation*