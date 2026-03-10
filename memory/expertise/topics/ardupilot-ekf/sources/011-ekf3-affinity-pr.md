# EKF3 Sensor Affinity PR #14674 - GitHub

**Fonte:** https://github.com/ArduPilot/ardupilot/pull/14674  
**Autor:** harshitsankhla  
**Tipo:** Pull Request  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~10min

---

## 📋 Resumo Executivo

PR que implementa Sensor Affinity e Lane Switching baseado em erro acumulado no EKF3. Mergeado por tridge.

---

## 🎯 Principais Mudanças

### Lane Selection Logic
- **Acumulação de erro:** Cada lane EKF acumula erro relativo à lane primária
- **Core selection mais robusto:** Seleção automática do melhor core
- **XKFS message:** Nova mensagem de log para "XKF Sensor"

### Sensor Affinity
- Permite que o índice do core EKF selecione instância de GPS/baro/mag
- Alternativa ao GPS blending
- EKF lane switching usado para selecionar combinação correta de GPS e IMU

### Airspeed Changes
- Emulação de sensores reais com ruído de airspeed maior em velocidades baixas
- Airspeed offset como parâmetro SITL

### AHRS Integration
- AHRS agora sabe qual airspeed sensor está sendo usado pela lane primária
- Múltiplos airspeed sensors + airspeed affinity = possível mudança de sensor

---

## 💡 Conceitos-Chave

### Accumulated Error Lane Switching
- Erro é acumulado ao longo do tempo (não instantâneo)
- Comparação entre lanes (relativo à primária)
- Mais robusto que switching baseado em threshold instantâneo

### XKF Sensor Message
- Log de sensores usados por cada lane
- Permite debugging de qual sensor está em uso

### AHRS Awareness
- AHRS precisa saber qual sensor está ativo
- Não assume sempre o sensor primário

---

## 🔗 Links Relacionados

- [EKF3 Affinity Docs](https://ardupilot.org/dev/docs/common-ek3-affinity-lane-switching.html)
- [AP_NavEKF3 Library](https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_NavEKF3)