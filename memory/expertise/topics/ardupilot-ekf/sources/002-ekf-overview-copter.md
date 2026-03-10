# Extended Kalman Filter Overview - ArduPilot Copter

**Fonte:** https://ardupilot.org/copter/docs/common-apm-navigation-extended-kalman-filter-overview.html  
**Tipo:** Documentação Oficial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~20min

---

## 📋 Resumo Executivo

O EKF (Extended Kalman Filter) é o algoritmo principal de estimação de estado do ArduPilot. Fusiona dados de giroscópio, acelerômetro, bússola, GPS, airspeed e barômetro para estimar posição, velocidade e atitude.

---

## 🎯 Vantagens sobre Filtros Complementares

| Filtro | Vantagens |
|--------|-----------|
| **DCM/Inertial Nav** | Mais simples |
| **EKF** | Melhor rejeição de erros, fusão de múltiplos sensores, suporta optical flow e range finder |

- EKF rejeita medições com erros significativos
- Veículo menos suscetível a falhas de sensor único
- Permite uso de sensores opcionais (optical flow, range finder)

---

## 📊 Arquitetura Atual

- **EKF3** é o padrão (default) em versões estáveis
- **DCM** roda em background como fallback
- Múltiplos IMUs → múltiplos "cores" EKF rodando em paralelo
- Apenas um core é usado por vez (o mais saudável)

### Múltiplos Cores
- 2+ IMUs disponíveis → 2+ cores EKF
- Cada core usa IMU diferente
- Core com melhor "health" é usado
- Health = consistência dos dados do sensor

---

## 🔄 EKF2 vs EKF3

| Aspecto | EKF2 | EKF3 |
|---------|------|------|
| **Status** | Ainda disponível | Recomendado (default) |
| **Sensores extras** | Não | Beacons, Wheel Encoders, Visual Odometry |
| **1MB autopilots** | Não disponível | Único option |
| **Sensor affinity** | Não | Sim |
| **Lane switching** | Limitado | Avançado |

**Recomendação:** Usar EKF3 para novos projetos.

---

## ⚙️ Parâmetros Principais

### Seleção de EKF
```
AHRS_EKF_USE = 1      # Usa EKF (forçado em Copter)
AHRS_EKF_TYPE = 3     # EKF3 (default) ou 2 para EKF2
EK2_ENABLE = 1        # Habilita EKF2
EK3_ENABLE = 1        # Habilita EKF3
```

### IMU Mask
```
EK3_IMU_MASK = 1      # Apenas IMU1
EK3_IMU_MASK = 2      # Apenas IMU2
EK3_IMU_MASK = 3      # IMU1 + IMU2 (2 cores)
```

### Lane Primária
```
EK3_PRIMARY = 0       # Primeiro IMU no mask
EK3_PRIMARY = 1       # Segundo IMU no mask
```

---

## 🔗 Sensor Affinity

- EKF3 permite usar instâncias **não-primárias** de sensores
- Sensores suportados: Airspeed, Barometer, Compass (Magnetometer), GPS
- Veículo pode gerenciar melhor sensores de boa qualidade
- Troca de lanes automática baseada em performance

Ver: [EKF3 Affinity and Lane Switching](common-ek3-affinity-lane-switching.html)

---

## 🛰️ GPS / Non-GPS Transitions

- EKF3 suporta troca de sensores em voo
- Útil para transição entre ambientes GPS e Non-GPS
- Ver: [GPS / Non-GPS Transitions](common-non-gps-to-gps.html)

---

## ⚠️ Fallbacks

| Cenário | Comportamento |
|---------|---------------|
| EKF unhealthy | Plane/Rover → fallback para DCM |
| EKF não funde GPS | Plane/Rover → fallback para DCM |
| EKF3 falha | **NÃO** há fallback EKF3 → EKF2 |
| EKF2 falha | **NÃO** há fallback EKF2 → EKF1 |

---

## 📝 Parâmetros Comuns de Ajuste

| Parâmetro | Default | Descrição |
|-----------|---------|-----------|
| `EK3_ALT_M_NSE` | 1.0 | Ruído de altitude. Menor = mais confiança no barômetro |
| `EK3_GPS_TYPE` | 0 | Como GPS é usado (0: 3D vel + 2D pos, 1: 2D vel + 2D pos, etc.) |
| `EK3_YAW_M_NSE` | 0.5 | Peso entre GPS e Compass para heading. Menor = mais compass |

---

## 💡 Conceitos-Chave

### Core EKF
- Instância única do EKF usando um IMU específico
- Múltiplos cores = redundância

### Lane
- Sinônimo de "core" no contexto do EKF3
- Lane switching = troca de core baseado em saúde

### Sensor Affinity
- Atribuição de sensores específicos a cores específicos
- Permite uso de sensores não-primários

---

## 🔍 Notas Importantes

- Rodar EKF2 + EKF3 em paralelo pode causar problemas de performance
- Se usar ambos, reduzir número total de cores via IMU_MASK
- Plane e Rover têm fallback para DCM, Copter não
- EKF3 é obrigatório em autopilots de 1MB (limitação de espaço)