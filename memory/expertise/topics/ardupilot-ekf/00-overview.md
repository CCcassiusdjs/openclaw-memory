# ArduPilot EKF3 - Overview

**Status:** In Progress
**Última atualização:** 2026-03-10
**Fontes lidas:** 0/5

---

## Resumo

O EKF3 (Extended Kalman Filter versão 3) é o sistema de estimação de estado do ArduPilot, responsável por combinar dados de múltiplos sensores para estimar a pose do drone em tempo real.

## Conceitos-Chave

### 1. Extended Kalman Filter (EKF)
- Generalização do Kalman Filter para sistemas não-lineares
- Lineariza em torno do estado atual
- Predição + Correção em cada passo

### 2. Sensores Suportados
- **IMU:** Acelerômetro + Giroscópio (obrigatório)
- **GPS:** Posição e velocidade
- **Magnetômetro:** Orientação
- **Barômetro:** Altitude
- **Optical Flow:** Velocidade lateral
- **Range Finder:** Distância ao solo
- **GPS RTK:** Alta precisão

### 3. State Vector
O EKF3 estima:
- Posição (NED: North, East, Down)
- Velocidade (NED)
- Orientação (quaternion)
- Bias do acelerômetro
- Bias do giroscópio
- Bias do magnetômetro
- Escala do terreno

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    EKF3 ARCHITECTURE                         │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │   IMU    │───►│          │───►│  State   │              │
│  │ (100Hz)  │    │          │    │ Estimate │              │
│  └──────────┘    │          │    │          │              │
│                  │   EKF3   │    │          │              │
│  ┌──────────┐    │          │    │          │              │
│  │   GPS    │───►│          │───►│          │              │
│  │  (5Hz)   │    │          │    │          │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                         │                   │
│  ┌──────────┐                          ▼                   │
│  │ Magnet.  │───►            ┌──────────────┐              │
│  └──────────┘                │   Output:    │              │
│                              │ - Position   │              │
│  ┌──────────┐                │ - Velocity   │              │
│  │  Baro    │───►            │ - Attitude   │              │
│  └──────────┘                └──────────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Fontes

1. [ ] https://ardupilot.org/copter/docs/ekf3-estimation.html
2. [ ] https://ardupilot.org/dev/docs/ekf3.html
3. [ ] https://ardupilot.org/copter/docs/common-ekf-innovations.html
4. [ ] https://ardupilot.org/dev/docs/ekf2-and-ekf3.html
5. [ ] arXiv: drone state estimation EKF

## Próximos Passos

1. Ler documentação oficial do EKF3
2. Entender parâmetros de configuração
3. Estudar diagnósticos de inovações
4. Comparar EKF2 vs EKF3

## Conexões com Outros Tópicos

- **drone-sensors:** Sensores que alimentam o EKF
- **digital-twins:** Usar EKF para sincronizar gêmeo digital
- **ml-fundamentals:** Potencial uso de ML para tuning

---

_Este arquivo será atualizado automaticamente pelo sistema de auto-estudo._