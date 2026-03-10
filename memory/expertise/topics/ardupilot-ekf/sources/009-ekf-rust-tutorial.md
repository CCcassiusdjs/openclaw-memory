# EKF for UAV Attitude Estimation in Rust - Medium Tutorial

**Fonte:** https://medium.com/@opinoquintana/i-wrote-an-extended-kalman-filter-for-uav-attitude-estimation-from-scratch-in-rust-b8748ff33b12  
**Autor:** Orlando Quintana  
**Tipo:** Tutorial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~45min

---

## 📋 Resumo Executivo

Implementação completa de EKF quaternion-based para estimação de atitude de quadcopter em Rust. Fusiona giroscópio e acelerômetro com bias correction. Testado em SITL (1M samples < 1s) e hardware (1kHz via ROS2).

---

## 🎯 Decisões de Design

### Quaternions vs Euler Angles

| Aspecto | Quaternions | Euler Angles |
|---------|-------------|--------------|
| **Gimbal Lock** | ✅ Sem singularity | ❌ ±90° causa problemas |
| **Angle Wrapping** | ✅ Sem descontinuidades | ❌ Requer unwrapping |
| **Computação** | ✅ Sem trig | ❌ Sin/Cos caros |
| **Robustez** | ✅ Estável numericamente | ❌ Problemas em manobras |

### State Vector (7 estados)
- **q0, q1, q2, q3:** Quaternion (orientação)
- **bx, by, bz:** Bias do giroscópio

### Yaw Angle
- Acelerômetro não detecta yaw (rotação sobre gravidade)
- EKF prevê yaw via integração do giroscópio
- Drift aceitável para voos curtos
- Pronto para fusão com magnetômetro no futuro

### Gyro Bias
- Inclusão explícita no state vector
- Mitiga drift de orientação
- Melhora precisão sem depender de sensores externos
- Custo computacional mínimo (7-state vs 4-state)

---

## 🔧 Implementação

### Estruturas em Rust
```rust
type Vector7 = Matrix<f64, Const<7>, Const<1>, ...>;
type Matrix7 = Matrix<f64, Const<7>, Const<7>, ...>;
type Matrix3x7 = Matrix<f64, Const<3>, Const<7>, ...>;

pub struct EKF {
    pub state: Vector7,           // [q0, q1, q2, q3, bx, by, bz]
    pub covariance: Matrix7,      // P matrix
    pub process_noise: Matrix7,   // Q matrix
    pub measurement_noise: Matrix3, // R matrix
}
```

### Inicialização com Acelerômetro
- Usa acelerômetro para estimar quaternion inicial
- Evita "spin-up time" de convergência
- Yaw inicial = 0 (não observável por accel)

### Prediction Phase
1. **Dynamic Model:** q̇ = 0.5 * Ω(ω) * q
2. **Jacobian:** ∂f/∂x (7x7 matrix)
3. **Covariance Update:** P' = FPFᵀ + Q

### Update Phase
1. **Measurement Model:** h(x) = R^T * g (gravidade no body frame)
2. **Innovation:** y = z - h(x)
3. **Measurement Jacobian:** ∂h/∂x (3x7 matrix)
4. **Kalman Gain:** K = PH^T(HPH^T + R)^{-1}
5. **State Update:** x' = x + K*y
6. **Covariance Update:** P' = (I - KH)*P
7. **Quaternion Normalize:** q = q / ||q||

---

## 📊 Resultados

### SITL Testing
- 1 milhão de samples processados em < 1 segundo
- Quaternion converge para orientação correta
- Bias do gyro estimado com precisão

### HITL Testing (Hardware-in-the-Loop)
- ROS2 pipeline com ICM-20948 IMU
- Rodando a 1kHz em tempo real
- Captura "unsteadiness" de movimento manual

### Yaw Lock
- Durante testes, yaw é "travado" para isolar roll/pitch
- Evita drift sem magnetômetro
- Permite tuning focado em X e Y

---

## 💡 Conceitos-Chave

### Dynamic Model (Quaternion Propagation)
- q̇ = 0.5 * Ω(ω) * q
- Ω(ω) é matriz skew-symmetric das taxas angulares
- Integração preserva unidade se normalizado

### Measurement Model (Gravity Vector)
- Gravidade é referência global constante
- R^T transforma para body frame
- Acelerômetro mede = gravidade + aceleração linear
- Assume aeronave em hover ou movimento lento

### Jacobian Derivation
- Derivadas parciais do modelo dinâmico
- Derivadas parciais do modelo de medição
- Essencial para EKF (não UKF)

### Noise Matrices Tuning
- **Q (Process Noise):** Confiança no modelo dinâmico
  - Alto = mais confiança no sensor
  - Baixo = mais confiança no modelo
- **R (Measurement Noise):** Confiança no sensor
  - Alto = menos confiança no sensor
  - Baixo = mais confiança no sensor

---

## 📝 Lições Aprendidas

1. **Rust para Robótica:**
   - Performance de C++ com safety
   - nalgebra crate para álgebra linear
   - Zero-cost abstractions
   - Compile-time safety

2. **Unidades Importam:**
   - Gyro em rad/s
   - Accel em m/s²
   - Erros de unidade são silenciosos e mortais

3. **Frame Alignment:**
   - Body frame: X forward, Y right, Z down
   - Sensores podem ter frames diferentes
   - Mapeamento incorreto = drift ou flip

4. **Tuning:**
   - Começar com Q pequeno, R médio
   - Ajustar baseado em inovações
   - Inovações devem ser centradas em zero

---

## 🔗 Links

- [GitHub: rust-ekf](https://github.com/OrlandoQuintana/rust-ekf)
- [Beard & McLain - Small Unmanned Aircraft: Theory and Practice](https://github.com/OrlandoQuintana/rust-ekf)