# Spinning Up: Key Concepts in RL

**Fonte:** https://spinningup.openai.com/en/latest/spinningup/rl_intro.html
**Data:** 2026-03-10
**Status:** Completed

---

## Resumo

Reinforcement Learning (RL) é o estudo de agentes que aprendem por tentativa e erro. O agente interage com um ambiente, recebe recompensas, e aprende a maximizar o retorno cumulativo.

---

## Conceitos Fundamentais

### Agentes e Ambientes
- **Agent**: Toma decisões (ações)
- **Environment**: O mundo onde o agente opera
- **Observation**: Visão parcial do estado (possivelmente incompleta)
- **State**: Descrição completa do mundo
- **Reward**: Sinal numérico indicando qualidade do estado/ação
- **Return**: Soma cumulativa de recompensas

### Estados vs Observações
- **Estado s**: Descrição completa do mundo (sem informação oculta)
- **Observação o**: Descrição parcial (POMDP - Partially Observable MDP)
- **Fully observed**: Agente vê estado completo
- **Partially observed**: Agente vê apenas observação

### Action Spaces
- **Discrete**: Conjunto finito de ações (ex: jogos Atari, Go)
- **Continuous**: Ações em espaço contínuo (ex: controle de robôs)
- Importante: Alguns algoritmos só funcionam em um tipo de espaço

### Policies (Políticas)
Regra que o agente usa para escolher ações:

**Determinística:**
```
a = π(s)
```

**Estocástica:**
```
a ~ π(a|s)
```

Em deep RL, políticas são parametrizadas por θ (pesos de rede neural).

#### Stochastic Policies

**Categorical Policy** (discrete actions):
- Rede neural como classificador
- Saída: logits → softmax → probabilidades
- Amostragem: torch.multinomial() ou similar

**Diagonal Gaussian Policy** (continuous actions):
- Distribuição Normal multivariada com covariância diagonal
- Parâmetros: média μ(s) e desvio padrão σ
- Amostragem: a = μ + σ ⊙ ε, onde ε ~ N(0, I)

### Trajectories (Trajetórias)
Sequência de estados e ações:
```
τ = (s₀, a₀, s₁, a₁, ...)
```

- Estado inicial: s₀ ~ ρ₀
- Transição: s_{t+1} ~ P(s_{t+1} | s_t, a_t)
- Também chamado de "episode" ou "rollout"

### Reward e Return

**Reward Function:**
```
r = R(s, a, s')
```
(frequentemente simplificada para r(s) ou r(s, a))

**Tipos de Return:**

1. **Finite-horizon undiscounted:**
   ```
   R(τ) = Σ_{t=0}^T r_t
   ```

2. **Infinite-horizon discounted:**
   ```
   R(τ) = Σ_{t=0}^∞ γ^t r_t
   ```
   
   - γ ∈ (0, 1): discount factor
   - Convergência garantida para γ < 1
   - "Cash now is better than cash later"

### O Problema de RL

**Objetivo:** Maximizar retorno esperado

```
J(π) = E_{τ ~ π} [R(τ)]

π* = argmax_π J(π)
```

**Probabilidade de uma trajetória:**
```
P(τ | π) = ρ₀(s₀) ∏_{t=0}^{T-1} π(a_t|s_t) P(s_{t+1}|s_t, a_t)
```

---

## Value Functions

Funções que estimam valor esperado de estados/ações:

### On-Policy Value Function (V^π)
```
V^π(s) = E_{τ ~ π} [R(τ) | s₀ = s]
```
Retorno esperado começando de s e seguindo π.

### On-Policy Action-Value Function (Q^π)
```
Q^π(s, a) = E_{τ ~ π} [R(τ) | s₀ = s, a₀ = a]
```
Retorno esperado começando de s, tomando ação a, depois seguindo π.

### Optimal Value Function (V*)
```
V*(s) = max_π E_{τ ~ π} [R(τ) | s₀ = s]
```
Retorno máximo possível de s.

### Optimal Action-Value Function (Q*)
```
Q*(s, a) = max_π E_{τ ~ π} [R(τ) | s₀ = s, a₀ = a]
```
Retorno máximo de (s, a).

**Relação fundamental:**
```
V*(s) = max_a Q*(s, a)
```

---

## Bellman Equations

Auto-consistência das funções de valor:

### On-Policy Bellman Equations
```
V^π(s) = E[a ~ π(.|s)] [r(s, a) + γ E[s' ~ P] [V^π(s')]]

Q^π(s, a) = E[s' ~ P] [r(s, a) + γ E[a' ~ π(.|s')] [Q^π(s', a')]]
```

### Optimal Bellman Equations
```
V*(s) = max_a [r(s, a) + γ E[s' ~ P] [V*(s')]]

Q*(s, a) = E[s' ~ P] [r(s, a) + γ max_a' Q*(s', a')]
```

**Bellman Backup:** Lado direito da equação (reward + próximo valor).

---

## Advantage Function

Medida relativa de qualidade de uma ação:

```
A^π(s, a) = Q^π(s, a) - V^π(s)
```

- V^π(s) = valor médio esperado seguindo π
- A^π(s, a) = quanto melhor (ou pior) que a média é tomar ação a

**Importância:** Central para métodos de policy gradient.

---

## Formalismo: Markov Decision Process (MDP)

MDP é uma 5-tupla:
```
M = (S, A, R, P, ρ₀)
```

- **S**: Espaço de estados
- **A**: Espaço de ações
- **R**: Função de recompensa R(s, a, s')
- **P**: Função de transição P(s' | s, a)
- **ρ₀**: Distribuição de estados iniciais

**Propriedade de Markov:** P(s' | s, a) depende apenas de (s, a), não do histórico.

---

## Conceitos-Chave Aprendidos

1. **Agent-Environment Loop**: Interação cíclica de observação → ação → recompensa
2. **Policy Types**: Determinística vs estocástica, categorical vs Gaussian
3. **Value Functions**: V^π, Q^π, V*, Q* e suas relações
4. **Bellman Equations**: Fundamento de dynamic programming em RL
5. **Advantage Function**: Diferença entre Q e V, crucial para policy gradient
6. **MDP Formalism**: Estrutura matemática padrão para problemas de RL
7. **Discount Factor γ**: Balanceia recompensas imediatas vs futuras

---

## Próximos Passos

- [ ] Estudar policy gradient methods (REINFORCE, Actor-Critic)
- [ ] Estudar value-based methods (DQN, variants)
- [ ] Explorar model-based RL
- [ ] Praticar com implementações em PyTorch/TensorFlow

---

*Atualizado em: 2026-03-10*