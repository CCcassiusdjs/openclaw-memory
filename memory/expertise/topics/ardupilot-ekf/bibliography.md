# ArduPilot EKF & State Estimation - Bibliografia

**Tópico:** ardupilot-ekf  
**Criado:** 2026-03-10  
**Status:** researching

---

## 📚 Organização por Relevância

### 🔴 ALTA PRIORIDADE - Documentação Oficial ArduPilot

| # | Fonte | Tipo | URL | Prioridade |
|---|-------|------|-----|------------|
| 1 | EKF2 Estimation System | Docs Oficial | https://ardupilot.org/dev/docs/ekf2-estimation-system.html | ⭐⭐⭐⭐⭐ |
| 2 | Extended Kalman Filter Overview (Copter) | Docs Oficial | https://ardupilot.org/copter/docs/common-apm-navigation-extended-kalman-filter-overview.html | ⭐⭐⭐⭐⭐ |
| 3 | Extended Kalman Filter Overview (Plane) | Docs Oficial | https://ardupilot.org/plane/docs/common-apm-navigation-extended-kalman-filter-overview.html | ⭐⭐⭐⭐⭐ |
| 4 | EKF Navigation Overview and Tuning | Docs Oficial | https://ardupilot.org/dev/docs/extended-kalman-filter.html | ⭐⭐⭐⭐⭐ |
| 5 | EKF3 Affinity and Lane Switching | Docs Oficial | https://ardupilot.org/dev/docs/common-ek3-affinity-lane-switching.html | ⭐⭐⭐⭐⭐ |
| 6 | EKF Failsafe (Copter) | Docs Oficial | https://ardupilot.org/copter/docs/ekf-inav-failsafe.html | ⭐⭐⭐⭐ |
| 7 | EKF Source Selection and Switching | Docs Oficial | https://ardupilot.org/copter/docs/common-ekf-sources.html | ⭐⭐⭐⭐ |

### 🟡 MÉDIA PRIORIDADE - Papers Acadêmicos

| # | Fonte | Tipo | URL | Prioridade |
|---|-------|------|-----|------------|
| 8 | Estimation for Quadrotors (arXiv:1809.00037) | Paper Acadêmico | https://arxiv.org/abs/1809.00037 | ⭐⭐⭐⭐⭐ |
| 9 | Investigating EKF, UKF, PF for Quadrotor Position (arXiv:2509.13243) | Paper Acadêmico | https://arxiv.org/abs/2509.13243 | ⭐⭐⭐⭐ |
| 10 | Improved State Estimation in Quadrotor MAVs (arXiv:1509.03388) | Paper Acadêmico | https://arxiv.org/pdf/1509.03388 | ⭐⭐⭐⭐ |
| 11 | Sensor Fusion for Drone Position and Attitude (ResearchGate 2025) | Paper Acadêmico | https://www.researchgate.net/publication/393590343 | ⭐⭐⭐⭐ |
| 12 | INS/GPS Fusion Architectures for UAVs | Paper Acadêmico | https://www.researchgate.net/publication/276417225 | ⭐⭐⭐ |
| 13 | Experimentally Validated EKF for UAV State Estimation | Paper Acadêmico | https://www.sciencedirect.com/science/article/pii/S2405896318317488 | ⭐⭐⭐ |

### 🟢 BAIXA PRIORIDADE - Tutoriais e Artigos

| # | Fonte | Tipo | URL | Prioridade |
|---|-------|------|-----|------------|
| 14 | EKF for UAV Attitude Estimation in Rust (Medium) | Tutorial | https://medium.com/@opinoquintana/i-wrote-an-extended-kalman-filter-for-uav-attitude-estimation-from-scratch-in-rust-b8748ff33b12 | ⭐⭐⭐ |
| 15 | Rust Meets Robotics: EKF for Drone Navigation (Medium) | Tutorial | https://medium.com/@puneetpm/rust-meets-robotics-implementing-extended-kalman-filters-for-drone-navigation-e207cadee419 | ⭐⭐⭐ |
| 16 | Design of EKF for UAV Localization (IEEE) | Paper Acadêmico | https://ieeexplore.ieee.org/document/4252506/ | ⭐⭐⭐ |
| 17 | Pose Estimation Using Dynamic EKF (IEEE) | Paper Acadêmico | https://ieeexplore.ieee.org/document/9646187/ | ⭐⭐⭐ |

### 🔵 REFERÊNCIAS - Discussões e Código

| # | Fonte | Tipo | URL | Prioridade |
|---|-------|------|-----|------------|
| 18 | EKF2 vs EKF3 Discussion (ArduPilot Discourse) | Discussão | https://discuss.ardupilot.org/t/whats-the-difference-between-ekf2-ekf3/86094 | ⭐⭐ |
| 19 | EKF3 Affinity PR #14674 (GitHub) | Código Fonte | https://github.com/ArduPilot/ardupilot/pull/14674 | ⭐⭐⭐ |
| 20 | AP_NavEKF2_core.h (GitHub) | Código Fonte | https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_NavEKF2/AP_NavEKF2_core.h | ⭐⭐⭐ |
| 21 | EKF3 Distance Limit Issue (GitHub) | Issue | https://github.com/ArduPilot/ardupilot/issues/16736 | ⭐⭐ |

---

## 📖 Resumo dos Conteúdos

### Documentação Oficial ArduPilot

**EKF2 vs EKF3:**
- EKF2: 24-state Extended Kalman Filter na biblioteca AP_NavEKF2
- EKF3: Mais moderno, suporta sensor affinity, lane switching, beacons, wheel encoders, visual odometry
- Recomendação: Usar EKF3 para novos projetos
- EKF2 pode rodar um EKF separado para cada IMU (melhor recuperação de falhas)

**Sensores Suportados:**
- IMU (giroscópio + acelerômetro)
- GPS
- Magnetômetro (bússola)
- Barômetro
- Airspeed (para aviões)
- Range Finder (altímetro laser)
- Optical Flow
- Visual Odometry (EKF3)
- Beacons (EKF3)
- Wheel Encoders (EKF3)

**EKF3 Sensor Affinity:**
- Permite usar instâncias não-primárias de sensores
- EK3_AFFINITY bitmask para configurar
- EK3_ERR_THRESH controla sensibilidade do lane switching
- Erros acumulados ao longo do tempo para decidir troca de lane

### Papers Acadêmicos

**Estimation for Quadrotors (arXiv:1809.00037):**
- Objetivo: Inferir estado do drone (pose, velocidade, aceleração, biases) de sensores
- Abordagem: EKF padrão com modelo cinemático
- Pseudocódigo fornecido para implementação

**EKF vs UKF vs PF (arXiv:2509.13243):**
- Compara filtros em condições de vento turbulento (Von Karman)
- UKF mais suave e preciso em condições não-lineares
- PF mais robusto mas computacionalmente caro

---

## 🎯 Conceitos-Chave para Estudar

1. **Extended Kalman Filter (EKF)**
   - Linearização de sistemas não-lineares
   - Matriz Jacobiana
   - Predição vs Atualização

2. **State Estimation**
   - Estados estimados: posição, velocidade, atitude
   - Estados internos: biases, variâncias

3. **Sensor Fusion**
   - IMU + GPS + Magnetômetro + Barômetro
   - Técnicas de fusão loosely-coupled vs tightly-coupled

4. **Lane Switching**
   - Múltiplos EKF cores rodando em paralelo
   - Troca automática baseada em erro acumulado

5. **Sensor Affinity**
   - Atribuição de sensores a cores EKF específicos
   - Gerenciamento de qualidade de sensores

---

## 📅 Plano de Leitura

| Ordem | Fonte | Tempo Estimado | Status |
|-------|-------|----------------|--------|
| 1 | EKF2 Estimation System (Doc Oficial) | 30min | pending |
| 2 | EKF Overview Copter (Doc Oficial) | 30min | pending |
| 3 | EKF3 Affinity and Lane Switching | 30min | pending |
| 4 | Estimation for Quadrotors (arXiv) | 60min | pending |
| 5 | EKF Navigation Tuning (Doc Oficial) | 30min | pending |
| 6 | EKF, UKF, PF Comparison (arXiv) | 45min | pending |
| 7 | EKF Failsafe | 20min | pending |
| 8 | Medium Tutorial (Rust EKF) | 45min | pending |

**Tempo Total Estimado:** ~5.5 horas

---

## 🔗 Links Relacionados

- [ArduPilot GitHub](https://github.com/ArduPilot/ardupilot)
- [ArduPilot Wiki](https://ardupilot.org/dev/docs/ekf.html)
- [ArduPilot Discourse](https://discuss.ardupilot.org/)