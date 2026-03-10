# A Survey on Deep Semi-supervised Learning (arXiv:2103.00550)

**Fonte:** https://arxiv.org/abs/2103.00550
**Autores:** Xiangli Yang et al.
**Ano:** 2023
**Publicado:** IEEE Transactions on Knowledge and Data Engineering, 35(9)
**Status:** Completed

---

## Resumo

Survey abrangente sobre deep semi-supervised learning (SSL), cobrindo fundamentos e avanços recentes.

---

## Taxonomia de Métodos SSL

### 1. Deep Generative Methods
- **Variational Autoencoders (VAE)**
- **Generative Adversarial Networks (GAN)**
- **Flow-based models**
- Aprendem distribuição de dados, geram samples

### 2. Consistency Regularization Methods
- **Π-Model**: Perturbação de input, consistência de predição
- **Mean Teacher**: Teacher-student com EMA
- **Virtual Adversarial Training (VAT)**: Perturbação adversarial
- **Interpolation Consistency Training (ICT)**
- **MixMatch**: Combina MixUp + consistency

### 3. Graph-Based Methods
- **Label Propagation**: Propaga labels por grafo
- **Graph Neural Networks**: GNN com SSL
- **Deep Graph Infomax**: Contraste em grafos

### 4. Pseudo-Labeling Methods
- **Self-training**: Treina com predições de alta confiança
- **Noisy Student**: Iterativo com noise
- **Pseudo-Label**: Usa predições como labels

### 5. Hybrid Methods
- Combina múltiplas abordagens
- MixMatch, ReMixMatch, FixMatch

---

## 52 Métodos Representativos

### Consistency Regularization

| Método | Ano | Contribuição |
|--------|-----|--------------|
| Π-Model | 2017 | Consistency under perturbation |
| Mean Teacher | 2017 | EMA teacher model |
| VAT | 2018 | Adversarial perturbation |
| ICT | 2019 | Interpolation consistency |
| MixMatch | 2019 | MixUp + consistency + pseudo-label |

### Pseudo-Labeling

| Método | Ano | Contribuição |
|--------|-----|--------------|
| Pseudo-Label | 2013 | Classic self-training |
| Noisy Student | 2019 | Iterative with noise |
| FixMatch | 2020 | Threshold + weak/strong augmentation |

### Generative Methods

| Método | Ano | Contribuição |
|--------|-----|--------------|
| VAE | 2014 | Variational inference |
| Improved GAN | 2016 | Semi-supervised GAN |
| ACGAN | 2017 | Auxiliary classifier GAN |

---

## Loss Functions

### Supervised Loss
```
L_s = (1/n) Σ L(f(x_i), y_i)
```

### Unsupervised Loss Types

1. **Consistency Loss**
```
L_c = (1/m) Σ D(f(x_i), f(Aug(x_i)))
```
Onde D é divergência (KL, MSE, etc.)

2. **Pseudo-Label Loss**
```
L_p = (1/m) Σ L(f(x_i), ŷ_i) × 1[max(f(x_i)) > τ]
```
Onde τ é threshold de confiança

3. **Generative Loss**
```
L_g = KL(q(z|x) || p(z)) - log p(x|z)
```

---

## Conceitos Aprendidos

1. **SSL Taxonomy**: Generative, consistency, graph, pseudo-label, hybrid
2. **Consistency Regularization**: Perturbação deve manter predição
3. **Mean Teacher**: Modelo teacher EMA do student
4. **Pseudo-Labeling**: High-confidence predictions como labels
5. **FixMatch**: Threshold + weak/strong augmentation (state-of-the-art)
6. **MixMatch**: Combina MixUp, consistency, pseudo-label
7. **Graph-Based SSL**: Propagação por estrutura de grafo

---

*Atualizado em: 2026-03-10*