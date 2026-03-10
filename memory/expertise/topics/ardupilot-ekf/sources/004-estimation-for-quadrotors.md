# Estimation for Quadrotors - arXiv:1809.00037

**Fonte:** https://arxiv.org/abs/1809.00037  
**Autores:** Stefanie Tellex et al.  
**Tipo:** Paper Acadêmico  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~15min (abstract e seções principais)

---

## 📋 Resumo Executivo

Tutorial passo-a-passo sobre filtros de Kalman para estimação de estado em quadrotores, criado para o curso "Flying Cars" da Udacity. Deriva EKF para modelos 1D, 2D e 3D de drones.

---

## 🎯 Objetivo do Paper

O objetivo é **inferir o estado do drone** (pose, velocidade, aceleração, biases) a partir de valores de sensores e entradas de controle.

**Desafios:**
- Sensores são ruidosos
- Computação limitada a bordo (peso e custo)
- Necessidade de estimar rapidamente

---

## 📚 Conteúdo

### Derivações Matemáticas
- EKF para modelos de drones em 1D, 2D e 3D
- Notação baseada em Thrun et al. [13]
- Pseudocódigo para:
  - Bayes Filter
  - Extended Kalman Filter (EKF)
  - Unscented Kalman Filter (UKF)

### Comparação: EKF vs UKF

| Aspecto | EKF | UKF |
|---------|-----|-----|
| **Complexidade** | Mais complexo (Jacobiana) | Mais simples |
| **Precisão** | Menos preciso | Mais preciso |
| **Runtime** | Comparável | Comparável |
| **Implementação** | Linearização necessária | Sigma points |

**Conclusão do autor:** UKF é melhor em quase todos os aspectos - mais simples de implementar, mais preciso, runtime comparável.

---

## 🔑 Conceitos-Chave

### Extended Kalman Filter
- Extensão não-linear do Kalman Filter
- Lineariza modelo de transição e medição não-lineares
- Linearização ao redor do estado atual

### States Estimados
- Pose (posição e orientação)
- Velocidade
- Aceleração
- Biases (giroscópio, acelerômetro)

### Bayes Filter
- Base teórica para todos os filtros
- Predição + Atualização

### Unscented Kalman Filter
- Usa "sigma points" para representar distribuição
- Não requer cálculo de Jacobiana
- Melhor para sistemas altamente não-lineares

---

## 📖 Referências do Paper

1. Thrun et al. [13] - Base da notação e teoria
2. UKF [14] - Unscented Kalman Filter

---

## 💡 Aplicações Práticas

### No ArduPilot
- EKF é o filtro padrão para estimação de estado
- UKF não é implementado nativamente (maior custo computacional?)
- Paper serve como base teórica para entender EKF2/EKF3

### Desafios Específicos de Quadrotores
- Alta taxa de manobra
- Sistema não-linear
- Sensores ruidosos (IMU, GPS, magnetômetro)
- Necessidade de fusão de múltiplos sensores

---

## 📝 Anotações Pessoais

- Paper foca em teoria, não em implementação específica do ArduPilot
- Derivações matemáticas são acessíveis com conhecimento de álgebra linear
- UKF seria teoricamente melhor, mas EKF é padrão na indústria (mais eficiente?)
- Útil para entender fundamentos teóricos do EKF2/EKF3