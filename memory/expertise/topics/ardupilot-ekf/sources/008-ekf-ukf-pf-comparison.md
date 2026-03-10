# EKF vs UKF vs PF for Quadrotor Position - arXiv:2509.13243

**Fonte:** https://arxiv.org/abs/2509.13243  
**Autores:** Ahmed Elgohary  
**Tipo:** Paper Acadêmico  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~10min (abstract)

---

## 📋 Resumo Executivo

Este estudo compara EKF, UKF e Particle Filter para estimação de posição de quadrotores em condições de vento turbulento (modelo Von Karman). Destaca trade-offs entre precisão, eficiência computacional e suavização.

---

## 🎯 Motivação

- Desastres naturais (furacões, tufões) exigem resposta rápida
- Drones governamentais grandes custam milhões
- Drones menores carecem de autonomia em ventos turbulentos
- Filtros avançados podem melhorar controle e adaptabilidade

---

## 📊 Comparação de Filtros

### Extended Kalman Filter (EKF)
- **Abordagem:** Linearização via expansão em série de Taylor
- **Vantagem:** Computacionalmente mais rápido
- **Desvantagem:** Dificuldade em sistemas altamente não-lineares
- **Jacobiana:** Requer cálculo de matrizes Jacobianas

### Unscented Kalman Filter (UKF)
- **Abordagem:** Sigma points (não requer Jacobiana)
- **Vantagem:** Melhor performance em sistemas não-lineares
- **Equilíbrio:** Balanceado entre precisão e custo computacional
- **Resultado:** Melhor captura de distúrbios de vento dinâmicos

### Particle Filter (PF)
- **Abordagem:** Grande número de partículas
- **Vantagem:** Lida com ruído não-Gaussiano e não-linearidades severas
- **Desvantagem:** Alto custo computacional devido à dimensionalidade
- **Problema:** Ineficiente em alta dimensionalidade de estados

---

## 🔧 Otimização com Algoritmo Genético

Parâmetros otimizados:
- **Matriz Q:** Covariância do ruído de processo
- **Matriz R:** Covariância do ruído de medição
- **Parâmetros UKF:** alpha, beta, kappa

---

## 📈 Resultados Principais

| Filtro | Precisão | Custo Computacional | Suavização |
|--------|----------|---------------------|------------|
| **EKF** | Menor | Mais rápido | Menor |
| **UKF** | Superior | Balanceado | Superior |
| **PF** | Robusto | Alto custo | Boa |

### Conclusão do Autor
> "UKF emerged as a balanced approach, achieving superior performance in capturing dynamic wind disturbances."

---

## 💡 Conceitos-Chave

### Von Karman Turbulence
- Modelo de turbulência atmosférica
- Usado para simular condições de furacão

### Sigma Points (UKF)
- Representam distribuição sem linearização
- Evitam erros de truncamento da Jacobiana

### Genetic Algorithm Tuning
- Otimização automática de parâmetros Q, R
- Melhora precisão sem ajuste manual

---

## 📝 Anotações Pessoais

- Paper foca em condições extremas (furacões)
- UKF é a escolha balanceada para não-linearidade
- PF é caro demais para sistemas de tempo real
- GA para tuning é interessante mas não prático para produção
- Justifica por que ArduPilot usa EKF (custo computacional menor)
- UKF seria ideal mas custo computacional é problema para hardware embarcado