# Machine Learning Fundamentals - Síntese de Conhecimento

**Tópico:** Machine Learning Fundamentals  
**Status:** Completed  
**Data de Conclusão:** 2026-03-11  
**Total de Fontes:** 48/48  
**Horas de Estudo:** ~15 horas

---

## 🎯 Visão Geral

Machine Learning é um campo que estuda algoritmos que aprendem padrões a partir de dados. Fundamenta-se em teoria estatística, otimização e teoria da computação para criar sistemas que melhoram com experiência.

---

## 📐 Fundamentos Teóricos

### Statistical Learning Theory

#### PAC Learning
- **Probably Approximately Correct** - Framework para aprender conceitos
- Um conceito é PAC-learnable se existe algoritmo que com probabilidade ≥ 1-δ produz hipótese com erro ≤ ε
- Sample complexity: m(ε, δ) samples necessárias

#### VC Dimension
- **Vapnik-Chervonenkis Dimension** - Medida de capacidade de uma classe de hipóteses
- VC(H) = cardinalidade máxima de pontos que H pode "shatter"
- Shattering: para qualquer rotulação dos pontos, existe hipótese que a realiza
- Sample complexity: m = O((d/ε) log(1/δ)) onde d = VC(H)

#### Rademacher Complexity
- Medida de complexidade data-dependent
- Captura a capacidade de uma classe de funções em se ajustar a ruído aleatório
- Rademacher bound: R(h) ≤ R̂(h) + O(R_n(ℋ))
- Mais refinada que VC dimension

### Bias-Variance Tradeoff

**Decomposição do MSE:**
```
E[(ŷ - y)²] = Bias² + Variance + Irreducible Error
```

- **Bias** - Erro sistemático (underfitting)
- **Variance** - Sensibilidade a ruído (overfitting)
- **Tradeoff** - Modelos complexos: low bias, high variance

**Double Descent:**
- Modern deep learning desafia o tradeoff clássico
- Performance melhora após passar pelo ponto de interpolação

---

## 🧠 Deep Learning

### Arquiteturas Principais

#### CNNs (Convolutional Neural Networks)
- Convolução local + pooling hierárquico
- Receptive field cresce com profundidade
- Feature hierarchy: edges → textures → parts → objects

#### Transformers
- Self-attention: Attention(Q, K, V) = softmax(QK^T/√d)V
- Multi-head attention
- Positional encoding (sin/cos ou learned)
- Escala melhor que RNNs para sequências longas

#### RNN/LSTM/GRU
- Processamento sequencial
- LSTM: gates (forget, input, output)
- GRU: gates simplificados (reset, update)
- Vanishing gradient mitigado por gating

### Activation Functions

| Function | Formula | Pros | Cons |
|----------|---------|------|------|
| **Sigmoid** | σ(x) = 1/(1+e^(-x)) | Smooth, (0,1) | Vanishing grad |
| **Tanh** | tanh(x) | Zero-centered | Vanishing grad |
| **ReLU** | max(0, x) | Fast, sparse | Dead neurons |
| **Leaky ReLU** | max(αx, x) | No dead neurons | Hyperparameter α |
| **GELU** | xΦ(x) | Smooth, performs | Complex |
| **Swish** | x·σ(x) | Smooth, performs | More compute |

### Weight Initialization

- **Xavier/Glorot** - Para tanh/sigmoid: Var(W) = 2/(n_in + n_out)
- **He/Kaiming** - Para ReLU: Var(W) = 2/n_in
- **Goal** - Preserve variance through layers

### Backpropagation

1. Forward pass: compute activations
2. Compute loss: L(y, ŷ)
3. Backward pass: compute gradients via chain rule
4. Update: θ ← θ - α∇L

**Computational graph:** Automatic differentiation

---

## ⚙️ Otimização

### Gradient Descent Variants

| Method | Update Rule | Pros | Cons |
|--------|-------------|------|------|
| **Batch GD** | θ ← θ - α∇L(θ) | Stable | Slow, memory |
| **SGD** | θ ← θ - α∇L_i(θ) | Fast, online | Noisy |
| **Mini-batch** | θ ← θ - α∇L_B(θ) | Best of both | Hyperparameter |

### Momentum

- **Classical:** v ← βv + ∇L, θ ← θ - αv
- **Nesterov:** v ← βv + ∇L(θ - αβv), θ ← θ - αv
- Lookahead: antecipa onde estará

### Adam

```
m ← β₁m + (1-β₁)∇L     # First moment
v ← β₂v + (1-β₂)(∇L)²  # Second moment
m̂ ← m/(1-β₁ᵗ)          # Bias correction
v̂ ← v/(1-β₂ᵗ)
θ ← θ - α·m̂/(√v̂ + ε)
```

**AdamW:** Weight decay decoupled from gradient update

### Learning Rate Scheduling

- **Step decay:** α ← α·γ a cada k epochs
- **Exponential decay:** α ← α₀·γ^t
- **Polynomial decay:** α ← α₀·(1 - t/T)^p
- **Cosine annealing:** α ← α_min + ½(α_max - α_min)(1 + cos(πt/T))
- **Warmup:** Gradualmente aumentar α no início

---

## 🛡️ Regularização

### L1/L2 Regularization

- **L1 (Lasso):** L + λ||θ||₁ → Esparsidade, feature selection
- **L2 (Ridge):** L + λ||θ||₂ → Weight shrinkage, smoothness
- **ElasticNet:** L + λ₁||θ||₁ + λ₂||θ||₂ → Combines both

### Dropout

- Randomly zero activations with probability p
- Training: scale by 1/(1-p)
- Inference: use all activations (no dropout)
- Ensemble effect: trains exponential number of subnetworks

### Batch Normalization

```
μ_B = mean(x_B)
σ²_B = var(x_B)
x̂ = (x - μ_B) / √(σ²_B + ε)
y = γ·x̂ + β
```

- Reduces internal covariate shift
- Allows higher learning rates
- Acts as regularizer

### Early Stopping

- Stop when validation loss increases
- Number of epochs is hyperparameter
- Simple but effective

---

## 🌳 Algoritmos Clássicos

### Decision Trees

- **ID3:** Information gain (entropy)
- **C4.5:** Gain ratio, handles continuous attributes
- **CART:** Gini impurity, binary splits
- **Pruning:** Reduce overfitting (pre/post)

### Ensemble Methods

**Bagging (Bootstrap Aggregating):**
- Train multiple models on bootstrap samples
- Average predictions (regression) or vote (classification)
- Reduces variance

**Random Forest:**
- Bagging + random feature selection
- Each tree sees random subset of features at each split
- Further reduces correlation

**Boosting:**
- Sequential training of weak learners
- Each model corrects errors of previous
- AdaBoost, Gradient Boosting, XGBoost, LightGBM, CatBoost

### SVM (Support Vector Machines)

- **Maximum margin:** Maximiza distância ao hyperplane
- **Kernel trick:** Φ(x) implicitamente via kernel K(x, x')
- **Kernels:** Linear, Polynomial, RBF, Sigmoid
- **Hinge loss:** max(0, 1 - y·f(x))

---

## 📊 Avaliação e Validação

### Cross-Validation

- **k-fold:** Divide em k partes, treina em k-1, testa em 1
- **Stratified:** Mantém proporção de classes
- **LOOCV:** Leave-one-out (k = n)
- **Nested:** Inner loop for hyperparameter selection

### Metrics

| Task | Metric | Formula |
|------|--------|---------|
| Classification | Accuracy | (TP+TN)/(TP+TN+FP+FN) |
| Classification | Precision | TP/(TP+FP) |
| Classification | Recall | TP/(TP+FN) |
| Classification | F1 | 2·P·R/(P+R) |
| Regression | MSE | mean((y-ŷ)²) |
| Regression | MAE | mean(|y-ŷ|) |
| Regression | R² | 1 - SS_res/SS_tot |

---

## 🔄 Reinforcement Learning

### MDP Formalism

- **State space:** S
- **Action space:** A
- **Reward function:** R(s, a, s')
- **Transition probability:** P(s'|s, a)
- **Discount factor:** γ ∈ [0, 1)

### Value Functions

- **State value:** V^π(s) = E[Σ γ^t r_t | s_0 = s]
- **Action value:** Q^π(s, a) = E[Σ γ^t r_t | s_0 = s, a_0 = a]
- **Optimal value:** V* = max_π V^π

### Bellman Equations

```
V^π(s) = Σ_a π(a|s) [R(s,a) + γ Σ_s' P(s'|s,a) V^π(s')]
Q^π(s,a) = R(s,a) + γ Σ_s' P(s'|s,a) Σ_a' π(a'|s') Q^π(s',a')
```

### Key Algorithms

- **Value Iteration:** Iteratively apply Bellman optimality
- **Policy Iteration:** Evaluate policy, improve, repeat
- **Q-Learning:** Off-policy TD learning
- **Policy Gradient:** Gradient ascent on policy parameters

---

## 🔬 Tópicos Avançados

### Semi-Supervised Learning

- **Consistency regularization:** Predictions should be consistent under perturbations
- **Pseudo-labeling:** Use confident predictions as labels
- **MixMatch:** Combine consistency + pseudo-labeling + MixUp
- **FixMatch:** Weak augmentation for pseudo-labels, strong for consistency

### Spurious Correlations

- **Definition:** ⟨y, a⟩ - label y correlates with spurious attribute a in training, but not in test
- **Clever Hans effect:** Models learn shortcuts instead of concepts
- **Group DRO:** Minimize worst-group loss
- **Detection:** Analyze latent representations

### Edge ML Training

- **Federated Learning:** Distributed training without sharing data
- **On-device training:** Train locally, constrained by compute/memory
- **Communication-efficient:** Gradient compression, local updates

---

## 💡 Insights Principais

1. **Theory matters** - PAC learning, VC dimension, Rademacher explicam generalização
2. **Optimization is central** - Adam/AdamW são padrão, mas SGD+momentum ainda competitive
3. **Regularization essential** - Dropout, BN, L2, early stopping previnem overfitting
4. **Ensembles powerful** - Boosting e RF dominam tabular data
5. **Architectures evolve** - CNNs → Transformers para muitos domínios
6. **RL foundation** - MDPs e Bellman equations são base
7. **Simplicity bias dangerous** - Models learn spurious correlations

---

## 📚 Referências Principais

1. Understanding Machine Learning (Shalev-Shwartz & Ben-David)
2. Reinforcement Learning: An Introduction (Sutton & Barto)
3. An Overview of Gradient Descent Optimization Algorithms (Ruder)
4. A Survey on Deep Semi-supervised Learning (arXiv:2103.00550)
5. A Comprehensive Survey on Spurious Correlations (arXiv:2402.12715)
6. Training ML Models at the Edge: A Survey (arXiv:2403.02619)

---

## 🎓 Lições Aprendidas

1. **Bias-Variance é real** - Mas double descent desafia intuição
2. **Adam é robusto** - Mas SGD+momentum pode generalizar melhor
3. **BatchNorm helps** - Mas LayerNorm pode ser melhor para Transformers
4. **Transfer learning works** - Pre-training em dados grandes ajuda
5. **Data > Architecture** - Mais dados > arquitetura sofisticada
6. **Spurious correlations everywhere** - Cuidado com shortcuts
7. **Federated learning promising** - Privacidade + ML = edge training

---

## ✅ Tópicos Relacionados

- [x] PAC Learning, VC Dimension
- [x] Rademacher Complexity
- [x] Bias-Variance Tradeoff
- [x] Deep Learning Architectures (CNN, Transformer, LSTM/GRU)
- [x] Activation Functions
- [x] Weight Initialization
- [x] Backpropagation
- [x] Optimization (SGD, Momentum, Adam, AdamW)
- [x] Learning Rate Scheduling
- [x] Regularization (L1/L2, Dropout, BatchNorm, Early Stopping)
- [x] Decision Trees
- [x] Ensemble Methods (Bagging, Boosting, Random Forest)
- [x] SVM
- [x] Cross-Validation
- [x] Reinforcement Learning (MDP, Value Functions, Bellman)
- [x] Semi-Supervised Learning
- [x] Spurious Correlations
- [x] Edge ML Training

---

**Completado em:** 2026-03-11  
**Próxima revisão:** Revisitar em 3 meses para atualizações