# EKF2 vs EKF3 Discussion - ArduPilot Discourse

**Fonte:** https://discuss.ardupilot.org/t/whats-the-difference-between-ekf2-ekf3/86094  
**Tipo:** Discussão da Comunidade  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~5min

---

## 📋 Resumo Executivo

Discussão comunitária sobre as diferenças entre EKF2 e EKF3. Principais pontos já cobertos na documentação oficial.

---

## 💡 Pontos Principais

### EKF2
- 24 estados
- Biblioteca AP_NavEKF2
- Mais estável, testado por mais tempo
- Recomendado para usuários que querem estabilidade

### EKF3
- Mais recursos: beacons, wheel encoders, visual odometry
- Sensor affinity e lane switching
- Único option para autopilots de 1MB
- Default em versões estáveis modernas

---

## 🔗 Links Relacionados

- [EKF Overview Documentation](https://ardupilot.org/dev/docs/extended-kalman-filter.html)
- [EKF3 Affinity](https://ardupilot.org/dev/docs/common-ek3-affinity-lane-switching.html)