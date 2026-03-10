# EKF Failsafe - ArduPilot Copter Docs

**Fonte:** https://ardupilot.org/copter/docs/ekf-inav-failsafe.html  
**Tipo:** Documentação Oficial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~15min

---

## 📋 Resumo Executivo

O EKF failsafe monitora a saúde do EKF para detectar problemas com a estimação de posição (geralmente causados por glitches de GPS ou erros de compass) e prevenir "flyaways".

---

## 🎯 Quando Dispara

O EKF failsafe dispara quando **qualquer duas** das "variâncias" do EKF (compass, posição ou velocidade) estão acima do threshold `FS_EKF_THRESH` por **1 segundo**.

### Variâncias
- Valores entre 0 e 1
- 0 = estimativa muito confiável
- 1 = estimativa não confiável
- Calculadas comparando resultados de múltiplos sensores

### Exemplo de Cálculo
Se GPS pula subitamente mas acelerômetro não mostra aceleração:
- Variância de posição aumenta (menos confiável)

---

## ⚠️ O Que Acontece Quando Dispara

1. **LED pisca vermelho-amarelo ou azul-amarelo** + alarme sonoro
2. **"EKF variance" aparece no HUD** do GCS

### Modos Manuais (Stabilize, Acro, AltHold)
- Nada mais acontece
- Piloto **não pode trocar para modos autônomos** até falha resolver

### Modos Autônomos (Loiter, PosHold, RTL, Guided, Auto)
- Comportamento controlado por `FS_EKF_ACTION`:
  - **0:** Apenas reporta
  - **1 (default):** Modo Land (descida controlada)
  - **2:** Modo AltHold (hover)
  - **3:** Land mesmo se em STABILIZE

### Após Failsafe
- Piloto pode retomar controle em modo manual (AltHold, Stabilize)
- Log dataflash registra erro

---

## 🔧 Ajustando Sensibilidade

### FS_EKF_THRESH

| Valor | Comportamento |
|-------|---------------|
| **0** | Desabilita EKF failsafe |
| **0.6-0.8** | Mais sensível (dispara rápido, pode disparar em manobras agressivas) |
| **0.8-1.0** | Menos sensível (flyaway vai mais longe antes de LAND) |

### Trade-off
- **Valor baixo:** Proteção rápida, mas pode disparar em manobras
- **Valor alto:** Menos falsos positivos, mas flyaway vai mais longe

---

## 📊 Logs e Diagnóstico

### NKF4 Messages
- `NKF4.SP` - Posição innovation
- `NKF4.SV` - Velocidade innovation
- `NKF4.SM` - Compass innovation

### Exemplo de Failsafe Real
Em incidente com interferência de torre de rádio:
- GPS reportou posições incorretas
- Posições e velocidades subiram acima de 0.8
- Veículo entrou em Land mode

---

## 💡 Conceitos-Chave

### Variância EKF
- Indica confiança do EKF na estimativa
- Calculada comparando sensores
- Aumenta quando sensores discordam

### Innovation
- Diferença entre predição e medição
- Alta innovation = problema com sensor

### Flyaway Prevention
- EKF failsafe é a última linha de defesa
- Preve que veículo voe para longe sem controle

---

## 🔗 Links Relacionados

- [GPS Failsafe and Glitch Protection](https://ardupilot.org/copter/docs/gps-failsafe-glitch-protection.html)
- [Land Mode](https://ardupilot.org/copter/docs/land-mode.html)
- [FS_EKF_THRESH parameter](https://ardupilot.org/copter/docs/parameters.html#fs-ekf-thresh)