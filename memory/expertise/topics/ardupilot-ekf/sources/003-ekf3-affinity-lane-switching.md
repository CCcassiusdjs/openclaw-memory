# EKF3 Affinity and Lane Switching - ArduPilot Dev Docs

**Fonte:** https://ardupilot.org/dev/docs/common-ek3-affinity-lane-switching.html  
**Tipo:** Documentação Oficial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~15min

---

## 📋 Resumo Executivo

Affinity é um recurso do EKF3 que permite lanes (cores) usarem sensores não-primários. Combinado com lane switching automático, permite que o veículo use a melhor combinação de sensores disponíveis.

---

## 🎯 Conceitos Fundamentais

### Lane (Core)
- Instância do EKF usando um IMU específico
- Número de lanes = número de IMUs habilitados
- Lane primária = fornece estimativas de estado
- Lanes secundárias = atualizadas em background, disponíveis para switching

### Sensor Affinity
- Convencionalmente: cada lane usa instância primária de cada sensor
- Com affinity: lanes podem usar sensores não-primários
- Permite uso estatisticamente consistente de múltiplos sensores de qualidade

### Lane Switching
- Troca automática de lane baseada em "error score"
- Error score considera inovações de todos os sensores usados pela lane
- Veículo pode ser salvo de problemas usando sensores não-IMU também

---

## ⚙️ Configuração

### Habilitar EKF3 Affinity
```
EK3_ENABLE = 1        # Habilita EKF3
AHRS_EKF_TYPE = 3     # Usa EKF3 para controle
```

### EK3_AFFINITY (Bitmask)
Controla quais sensores têm affinity habilitado:
- Bit não habilitado → segue alocação primária padrão
- Sensores suportados: Airspeed, Barometer, GPS, Magnetometer

### EK3_ERR_THRESH
Controla sensibilidade do lane switching:
- Threshold para diferença de erro entre lane não-primária e primária
- **Valor menor** → switching mais agressivo (mais sensível)
- **Valor maior** → switching menos frequente
- ⚠️ Configuração errada pode ter consequências graves!

---

## 📊 Exemplo de Configuração

Veículo com:
- 2 Barometers
- 2 GPS
- 2 Airspeeds
- 3 Magnetometers
- 3 IMUs

**Tabela de Affinity:**

| Lane | Airspeed | Barometer | GPS | Magnetometer |
|------|----------|-----------|-----|--------------|
| Lane 1 | 2, 1 | 2, 1 | 2, 1 | 1, 2, 3 |
| Lane 2 | 2, 1 | 2, 1 | 2, 1 | 1, 2, 3 |
| Lane 3 | 2, 1 | 2, 1 | 2, 1 | 1, 2, 3 |

(Números são instâncias de sensores)

---

## 🧪 Resultados de Teste (SITL)

### Airspeed
- 2 airspeed sensors, 2 IMUs (2 lanes)
- Lane primária: airspeed falhou (valor constante)
- Velocidade aumentou → lane switch
- Segundo airspeed falhou → velocidade diminuiu → outro lane switch

### Barometer
- 2 barometers, 2 IMUs (2 lanes)
- Lane primária: barômetro falhou (pressão constante)
- Altitude aumentou → lane switch
- Segundo barômetro falhou → altitude diminuiu → outro lane switch

### GPS
- 2 GPS, 2 IMUs (2 lanes)
- GPS primário simulado com ruído aleatório ±2m/s em todos os eixos
- EKF começa a reportar erro alto consistentemente
- Lane switch quando erro cruza threshold

### Magnetometer
- 2 magnetometers, 2 IMUs (2 lanes)
- Erro simulado mudando offset do eixo Z em voo
- EKF reporta erro alto
- Lane switch quando erro cruza threshold

---

## 💡 Conceitos-Chave

### Error Score
- Erro acumulado ao longo do tempo
- Relativo à lane primária ativa
- Considera inovações de todos os sensores

### Primary Sensor
- Instância primária de cada sensor (user-modifiable)
- Pode ser alterada pelo sistema em caso de falha

### Statistically Consistent
- Maneira estatisticamente correta de usar múltiplos sensores
- Não é simples "voting" - considera covariâncias

---

## ⚠️ Avisos Importantes

1. **Affinity só funciona com EKF3** (não disponível em EKF2)
2. **EK3_ERR_THRESH mal configurado** pode causar perda do veículo
3. **Lane switching é baseado em erro acumulado**, não instantâneo
4. **Sensores não-IMU** também podem salvar o veículo (via error score)

---

## 📝 Parâmetros Relacionados

| Parâmetro | Descrição |
|-----------|-----------|
| `EK3_ENABLE` | Habilita EKF3 |
| `AHRS_EKF_TYPE` | Tipo de EKF (3 = EKF3) |
| `EK3_AFFINITY` | Bitmask de sensores com affinity |
| `EK3_ERR_THRESH` | Threshold para lane switching |
| `EK3_IMU_MASK` | Quais IMUs usar |
| `EK3_PRIMARY` | Lane primária inicial |

---

## 🔗 Links Relacionados

- [EKF Overview](https://ardupilot.org/dev/docs/extended-kalman-filter.html)
- [GitHub PR #14674](https://github.com/ArduPilot/ardupilot/pull/14674) - Implementação original