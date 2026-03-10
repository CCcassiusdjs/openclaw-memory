# Reinforcement Learning: An Overview (arXiv:2412.05265)

**Fonte:** https://arxiv.org/abs/2412.05265
**Autor:** Kevin Murphy
**Ano:** 2024
**Status:** Completed

---

## Resumo

Survey abrangente e atualizado cobrindo todo o campo de (deep) reinforcement learning e tomada de decisão sequencial.

---

## Estrutura

### Tópicos Cobertos

1. **Value-Based Methods**
   - Dynamic Programming
   - Q-Learning e variants
   - DQN, Double DQN, Dueling DQN
   - Rainbow e extensions

2. **Policy-Based Methods**
   - REINFORCE
   - Actor-Critic (A2C, A3C)
   - PPO, TRPO
   - SAC, TD3

3. **Model-Based Methods**
   - World models
   - MBPO, Dreamer
   - Model-predictive control

4. **Multi-Agent RL**
   - Cooperative settings
   - Competitive settings
   - Mixed motives

5. **LLMs and RL**
   - RLHF (RL from Human Feedback)
   - Constitutional AI
   - Preference learning
   - Fine-tuning strategies

6. **Other Topics**
   - Offline RL
   - Hierarchical RL
   - Intrinsic reward
   - Curiosity-driven exploration

---

## Value-Based Methods

### Dynamic Programming Foundation
- Policy Evaluation
- Policy Iteration
- Value Iteration
- Generalized Policy Iteration

### Q-Learning
```
Q(s, a) ← Q(s, a) + α[r + γ max_a' Q(s', a') - Q(s, a)]
```

### DQN Extensions
- **Double DQN**: Reduces overestimation bias
- **Dueling DQN**: Separates value and advantage streams
- **Prioritized Experience Replay**: Sample important transitions more
- **Noisy Networks**: Exploration via noisy parameters

### Rainbow
Combinação de todas as extensões DQN.

---

## Policy-Based Methods

### Policy Gradient Theorem
```
∇J(θ) = E_{τ ~ π_θ} [∇log π_θ(a|s) Q^π(s, a)]
```

### REINFORCE
```
θ ← θ + α G_t ∇log π_θ(a_t|s_t)
```
- Usa retorno real G_t como estimativa de Q
- Alta variância, mas unbiased

### Actor-Critic
- Actor: Policy network π_θ(a|s)
- Critic: Value network V_φ(s) ou Q_φ(s, a)
- Critic reduz variância do policy gradient

### PPO (Proximal Policy Optimization)
- Constrained policy update
- Clipped objective para estabilidade
- Amplamente usado na prática

### SAC (Soft Actor-Critic)
- Entropy regularization
- Off-policy learning
- Sample-efficient

---

## Model-Based Methods

### World Models
- Learn environment dynamics: s' = f(s, a)
- Plan using model
- Sample-efficient quando modelo é preciso

### Dreamer
- Latent dynamics model
- Imagination-based training
- State-of-the-art em vários benchmarks

---

## LLMs and RL

### RLHF Pipeline
1. Pre-train language model
2. Train reward model from human preferences
3. Optimize policy with PPO against reward model

### Constitutional AI
- Define principles via constitution
- Self-critique and revision
- Reduce harmful outputs

### Code Snippets (Training LLMs with RL)
```python
# Simplified RLHF loop
for epoch in range(num_epochs):
    # Generate responses
    responses = policy_model.generate(prompts)
    
    # Score with reward model
    rewards = reward_model.score(prompts, responses)
    
    # Compute policy gradient loss
    loss = compute_ppo_loss(policy_model, rewards, responses)
    
    # Update policy
    optimizer.step(loss)
```

---

## Offline RL

- Learn from fixed dataset (no exploration)
- Challenge: Distribution shift
- Methods: BCQ, CQL, IQL

---

## Hierarchical RL

- Temporal abstraction
- Options framework
- Feudal RL
- HAMs (Hierarchical Abstract Machines)

---

## Intrinsic Reward

- Curiosity-driven exploration
- Intrinsic motivation
- Information gain
- Novelty-based rewards

---

## Conceitos Aprendidos

1. **Taxonomia Completa**: Value-based, policy-based, model-based
2. **Deep RL Algorithms**: DQN variants, PPO, SAC, Dreamer
3. **Multi-Agent RL**: Cooperative, competitive, mixed
4. **LLM Fine-tuning**: RLHF, Constitutional AI
5. **Advanced Topics**: Offline RL, hierarchical RL, intrinsic reward
6. **Modern State-of-the-Art**: Current best practices e algorithms

---

*Atualizado em: 2026-03-10*