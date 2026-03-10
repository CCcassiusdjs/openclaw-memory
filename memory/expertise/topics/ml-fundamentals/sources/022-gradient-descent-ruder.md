# An Overview of Gradient Descent Optimization Algorithms

**Fonte:** Sebastian Ruder
**Ano:** 2016 (Atualizado)
**URL Original:** https://www.ruder.io/optimizing-gradient-descent/
**Tipo:** Artigo de revisão / Blog técnico

---

## Resumo

Este artigo apresenta uma visão abrangente dos algoritmos de otimização por gradiente descendente, desde as variantes clássicas até as mais modernas usadas em deep learning.

---

## Variantes de Gradient Descent

### 1. Batch Gradient Descent
- Usa todo o dataset para computar o gradiente
- **Vantagem**: Convergência estável
- **Desvantagem**: Lento para datasets grandes
- **Fórmula**: θ = θ - η∇θJ(θ)

### 2. Stochastic Gradient Descent (SGD)
- Usa uma amostra por iteração
- **Vantagem**: Mais rápido, permite online learning
- **Desvantagem**: Alta variância, oscilações
- **Fórmula**: θ = θ - η∇θJ(θ; x⁽ⁱ⁾; y⁽ⁱ⁾)

### 3. Mini-batch Gradient Descent
- Usa um batch pequeno de amostras
- **Vantagem**: Balance entre velocidade e estabilidade
- **Desvantagem**: Ainda requer ajuste de learning rate
- **Fórmula**: θ = θ - η∇θJ(θ; x⁽ⁱ:ⁱ⁺ⁿ⁾; y⁽ⁱ:ⁱ⁺ⁿ⁾)

---

## Desafios do Gradient Descent

### 1. Learning Rate
- Taxa muito alta → divergência
- Taxa muito baixa → convergência lenta
- Learning rate schedules: decay, step decay, exponential decay

### 2. Saddle Points e Plateaus
- Gradientes próximos de zero em regiões planas
- Saddle points mais comuns que mínimos locais em alta dimensão

### 3. Não-convexidade
- Superfícies de loss não-convexas
- Múltiplos mínimos locais

---

## Algoritmos de Otimização Modernos

### Momentum
- **Conceito**: Adiciona "momentum" ao gradiente
- **Fórmula**: vₜ = γvₜ₋₁ + η∇θJ(θ)
- **Vantagem**: Acelera convergência, reduz oscilações
- **γ tipicamente**: 0.9

### Nesterov Accelerated Gradient (NAG)
- **Conceito**: "Look-ahead" do momentum
- **Fórmula**: vₜ = γvₜ₋₁ + η∇θJ(θ - γvₜ₋₁)
- **Vantagem**: Melhor resposta à mudanças de direção

### Adagrad
- **Conceito**: Learning rate adaptativo por parâmetro
- **Fórmula**: θₜ = θₜ₋₁ - (η/√(Gₜ + ε)) ⊙ gₜ
- **Vantagem**: Adapta-se a features esparsas
- **Desvantagem**: Learning rate diminui monotonicamente

### Adadelta
- **Conceito**: Adagrad com learning rate não-monotônico
- **Vantagem**: Não requer learning rate inicial
- **Inovação**: Janela de gradientes passados

### RMSprop
- **Conceito**: Similar ao Adadelta, mas com decaimento exponencial
- **Fórmula**: E[g²]ₜ = γE[g²]ₜ₋₁ + (1-γ)g²ₜ
- **Vantagem**: Bom para dados não-estacionários

### Adam (Adaptive Moment Estimation)
- **Conceito**: Combina momentum + RMSprop
- **Fórmulas**:
  - mₜ = β₁mₜ₋₁ + (1-β₁)gₜ
  - vₜ = β₂vₜ₋₁ + (1-β₂)g²ₜ
  - θₜ = θₜ₋₁ - η(√v̂ₜ/(m̂ₜ + ε)))
- **Hiperparâmetros tipicos**: β₁=0.9, β₂=0.999, ε=10⁻⁸
- **Vantagem**: Funciona bem na prática, poucos ajustes

### AdamW
- **Conceito**: Adam com weight decay corrigido
- **Vantagem**: Melhor generalização que Adam

### AdaMax
- **Conceito**: Variante de Adam com norma infinito
- **Fórmula**: Usa L∞ em vez de L2

### Nadam
- **Conceito**: Adam com Nesterov momentum
- **Vantagem**: Combina benefícios de Adam e NAG

---

## Comparação de Algoritmos

| Algoritmo | LR Adap.? | Momentum? | Uso Recomendado |
|-----------|-----------|------------|-----------------|
| SGD | Não | Não | Convex, simples |
| Momentum | Não | Sim | Non-convex |
| NAG | Não | Sim (look-ahead) | Non-convex |
| Adagrad | Sim | Não | Sparse data |
| RMSprop | Sim | Não | Non-stationary |
| Adam | Sim | Sim | Geral, deep learning |
| AdaMax | Sim | Sim | Alternativa a Adam |
| Nadam | Sim | Sim | Alternativa a Adam |
| AdamW | Sim | Sim | Com regularização |

---

## Recomendações Práticas

### Para Deep Learning
1. **Adam** é o padrão default
2. **SGD + Momentum** para melhor generalização (se tempo permite)
3. **AdamW** quando weight decay é importante

### Ajuste de Learning Rate
1. **Learning rate scheduling**: ReduceLROnPlateau, CosineAnnealing
2. **Warmup**: Começar com LR baixo, aumentar gradualmente
3. **Fine-tuning**: LR menor para camadas pré-treinadas

### Batch Size
1. **Batch grande**: LR proporcionalmente maior
2. **Batch pequeno**: LR proporcionalmente menor
3. **Linear scaling rule**: LR ∝ batch_size

---

## Conceitos-Chave

### Gradiente
- Vetor de derivadas parciais
- Direção de maior aumento da função
- Gradiente negativo = direção de menor aumento

### Convergência
- Ponto onde ∇θJ(θ) ≈ 0
- Mínimo local vs. mínimo global
- Critérios de parada: |∇θJ(θ)| < ε

### Generalização
- Diferença entre erro de treino e teste
- Regularização melhora generalização
- Learning rate muito alto pode piorar

---

## Citações Notáveis

> "Gradient descent is the preferred way to optimize neural networks and many other machine learning algorithms."

> "Adam is currently the default choice for most deep learning applications."

---

## Status
- [x] Leitura completa (artigo consolidado)
- [ ] Implementação prática dos algoritmos

---

## Próximos Passos
1. Estudar teoria de convergência para SGD
2. Entender proof de convergência de Adam
3. Praticar com diferentes otimizadores em PyTorch/TensorFlow

---

*Fonte consolidada em: 2026-03-10*