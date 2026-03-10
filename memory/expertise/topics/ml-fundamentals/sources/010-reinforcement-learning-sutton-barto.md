# Reinforcement Learning: An Introduction

**Fonte:** Richard S. Sutton & Andrew G. Barto
**Editora:** MIT Press
**Ano:** 2018 (2nd Edition)
**Páginas:** 526
**ISBN:** 9780262039246
**URL:** https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf

---

## Sobre o Livro

Este é o **livro de referência** em Reinforcement Learning (RL), amplamente considerado a "bíblia" da área. Escrito por dois dos pioneiros do campo, cobre desde os fundamentos até algoritmos modernos de deep RL.

---

## Estrutura do Livro

### Parte 1: Tabular Solution Methods
1. **Introduction**
   - O que é reinforcement learning
   - Exemplos e aplicações
   - História do campo

2. **Multi-armed Bandits**
   - Exploração vs. exploração
   - Algoritmos ε-greedy, UCB, gradient bandit
   - Regret bounds

3. **Finite Markov Decision Processes**
   - MDPs: estados, ações, transições, recompensas
   - Policies e value functions
   - Bellman equations
   - Optimal policies

4. **Dynamic Programming**
   - Policy evaluation
   - Policy iteration
   - Value iteration
   - Generalized Policy Iteration (GPI)

5. **Monte Carlo Methods**
   - MC prediction
   - MC control
   - Off-policy learning
   - Importance sampling

6. **Temporal-Difference Learning**
   - TD prediction
   - TD(0), TD(λ)
   - Sarsa, Q-learning, Expected Sarsa
   - Maximization bias

7. **n-step Bootstrapping**
   - n-step TD
   - n-step Sarsa
   - n-step off-policy learning

8. **Planning and Learning with Tabular Methods**
   - Models and planning
   - Dyna architecture
   - Prioritized sweeping

### Parte 2: Approximate Solution Methods
9. **On-policy Prediction with Approximation**
   - Value function approximation
   - Linear methods
   - Feature construction

10. **On-policy Control with Approximation**
    - Episodic semi-gradient control
    - Average reward setting

11. **Off-policy Methods with Approximation**
    - Off-policy divergence
    - The deadly triad
    - Gradient-TD methods

12. **Eligibility Traces**
    - TD(λ) forward view
    - Backward view
    - Online TD(λ)

13. **Policy Gradient Methods**
    - REINFORCE
    - Actor-Critic
    - Policy gradient theorem

### Parte 3: Looking Deeper
14. **Psychology**
    - Connections to psychology
    - Habitual vs. goal-directed behavior

15. **Neuroscience**
    - Dopamine and reward prediction error
    - Basal ganglia and RL

16. **Applications and Case Studies**
    - Game playing (AlphaGo, etc.)
    - Robotics
    - Business applications

---

## Conceitos-Chave

### MDPs (Markov Decision Processes)
- **Estados (S)**: Representações do ambiente
- **Ações (A)**: Decisões que o agente pode tomar
- **Transições (P)**: Probabilidade de ir de s para s' com ação a
- **Recompensas (R)**: Sinal de feedback escasso e atrasado

### Value Functions
- **State-value function V(s)**: Valor esperado acumulado de um estado
- **Action-value function Q(s,a)**: Valor esperado acumulado de uma ação
- **Bellman Equations**: Relações de recursão para value functions

### Exploration vs. Exploitation
- **ε-greedy**: Explora com probabilidade ε
- **UCB (Upper Confidence Bound)**: Balanço otimista
- **Thompson Sampling**: Probabilistic matching

### Temporal Difference (TD) Learning
- **TD(0)**: Bootstrapping de um passo
- **TD(λ)**: Multi-step returns com eligibility traces
- **Bootstrapping**: Atualizar estimativas com outras estimativas

### Policy Gradient
- **REINFORCE**: Gradient Monte Carlo
- **Actor-Critic**: Separa policy (actor) e value (critic)
- **Policy Gradient Theorem**: Derivada da recompensa esperada

---

## Algoritmos Principais

| Algoritmo | Tipo | Características |
|-----------|------|----------------|
| **Q-learning** | Off-policy TD | Converge para Q* |
| **Sarsa** | On-policy TD | Converge para Qπ |
| **Expected Sarsa** | On-policy TD | Menos variância |
| **Dyna-Q** | Model-based + TD | Planning + learning |
| **REINFORCE** | Policy gradient | Monte Carlo |
| **Actor-Critic** | Policy gradient | Actor + Critic |

---

## Diferenciais do Livro

1. **Autoridade**: Os autores são pioneiros do campo
2. **Cobertura Completa**: Desde tabular até deep RL
3. **Fundamentos Matemáticos**: Provas rigorosas
4. **Conexões Interdisciplinares**: Psychology, Neuroscience
5. **Gratuito**: Disponível online oficialmente

---

## Citações Notáveis

> "Reinforcement learning is learning what to do—how to map situations to actions—so as to maximize a numerical reward signal."

> "The reinforcement learning problem is meant to be a straightforward framing of the problem of learning from interaction to achieve a goal."

---

## Status
- [x] Leitura do sumário completada
- [ ] Leitura completa do livro (pendente)
- [ ] Exercícios resolvidos (pendente)

---

## Próximos Passos
1. Estudar capítulos 1-6 (Tabular Methods)
2. Focar em TD Learning e Q-learning
3. Compreender Policy Gradient (capítulo 13)

---

*Fonte lida em: 2026-03-10*