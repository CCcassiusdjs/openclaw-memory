# L2 Regularization (Google ML Crash Course)

**Fonte:** https://developers.google.com/machine-learning/crash-course/overfitting/regularization
**Data:** 2026-03-10
**Status:** Completed

---

## Resumo

L2 regularization é técnica para reduzir complexidade do modelo e prevenir overfitting penalizando weights grandes.

---

## Fórmula L2

### Definição
```
L2 regularization = w₁² + w₂² + ... + wₙ²
```

### Loss Function com L2
```
minimize(Loss + λ × Complexity)
```

Onde:
- **Loss**: Função de perda do modelo
- **λ (lambda)**: Regularization rate
- **Complexity**: Soma dos quadrados dos weights

---

## Como Funciona

### Penalização de Weights Grandes
- Weights próximos de zero têm pouco impacto
- Weights grandes são fortemente penalizados

### Exemplo de Cálculo

| Weight | Valor | Valor² |
|--------|-------|--------|
| w₁ | 0.2 | 0.04 |
| w₂ | -0.5 | 0.25 |
| w₃ | 5.0 | 25.0 |
| w₄ | -1.2 | 1.44 |
| w₅ | 0.3 | 0.09 |
| w₆ | -0.1 | 0.01 |
| **Total** | - | **26.83** |

**Observação:** 
- w₃ sozinho contribui ~93% da complexidade total
- Os outros 5 weights contribuem apenas ~7%

### Efeito no Modelo
- Encoraja weights próximos de zero
- **Nunca** zera weights completamente
- Todos os features continuam contribuindo

---

## Regularization Rate (Lambda)

### Definição
Escalar que controla o impacto da regularização no treinamento.

### Alto λ (Regularization Rate)
- ✅ Reduz overfitting
- ✅ Produz distribuição normal de weights
- ✅ Mean weight = 0
- ⚠️ Pode causar underfitting se muito alto

### Baixo λ (Regularization Rate)
- ⚠️ Aumenta risco de overfitting
- ⚠️ Produz distribuição flat de weights
- ⚠️ Mean pode não ser zero
- ✅ Modelo mais complexo

### Escolha do λ Ideal
- É **data-dependent**
- Requer tuning (hyperparameter search)
- Cross-validation recomendado

---

## Early Stopping (Alternativa)

### Definição
Método de regularização que para treinamento antes de convergência completa.

### Quando Usar
- Quando loss no validation set começa a aumentar
- Alternativa rápida à regularização baseada em complexidade

### Características
- Aumenta training loss
- Pode diminuir test loss
- Raramente é ótimo, mas é rápido

---

## Equilíbrio Learning Rate vs Regularization Rate

### Relação Oposta
- **High learning rate**: Puxa weights **longe** de zero
- **High regularization rate**: Puxa weights **em direção** a zero

### Encontrando Equilíbrio

| Cenário | Problema | Solução |
|---------|----------|---------|
| λ alto, η baixo | Weaks weights, modelo ruim | Diminuir λ ou aumentar η |
| η alto, λ baixo | Strong weights, overfitting | Aumentar λ ou diminuir η |
| Equilíbrio | Generalização adequada | ✓ Ideal |

### Desafio
- Mudar learning rate requer retuning regularization rate
- Encontrar equilíbrio é iterativo e desafiador

---

## Comparação L2 vs L1

| Característica | L1 (LASSO) | L2 (Ridge) |
|----------------|------------|------------|
| **Fórmula** | Σ\|wᵢ\| | Σwᵢ² |
| **Zera weights** | Sim | Não |
| **Geometria** | Diamante | Círculo |
| **Feature selection** | Sim | Não |
| **Uso** | Sparse models | Shrink weights |

---

## Implementação

### TensorFlow/Keras
```python
import tensorflow as tf

# L2 regularization em layers
model = tf.keras.Sequential([
    tf.keras.layers.Dense(
        64, 
        activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(0.01)
    ),
    tf.keras.layers.Dense(1)
])

# O regularization rate λ = 0.01
```

### PyTorch
```python
import torch
import torch.nn as nn

# L2 regularization via weight_decay no optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)
# weight_decay = λ
```

### scikit-learn
```python
from sklearn.linear_model import Ridge

# Ridge = Linear Regression com L2
model = Ridge(alpha=1.0)  # alpha = λ
model.fit(X_train, y_train)
```

---

## Histograma de Weights

### Alto λ
```
     |
     |      ▓▓▓
     |     ▓▓▓▓▓
     |    ▓▓▓▓▓▓▓
     |   ▓▓▓▓▓▓▓▓▓
     |  ▓▓▓▓▓▓▓▓▓▓▓
     +----|-----|---->
        -0.5  0  0.5
    
    Distribuição normal, mean=0
```

### Baixo λ
```
     |
     |  ▓        ▓
     |  ▓        ▓
     |  ▓        ▓
     |  ▓        ▓
     |  ▓▓▓▓▓▓▓▓▓▓
     +----|-----|---->
        -1   0   1
    
    Distribuição flat
```

---

## Conceitos Aprendidos

1. **L2 Regularization**: Penaliza weights grandes, nunca zera
2. **Regularization Rate (λ)**: Controla força da regularização
3. **Learning Rate vs λ**: Opostos, precisam de equilíbrio
4. **Early Stopping**: Alternativa rápida de regularização
5. **Weight Distribution**: Alto λ → normal com mean=0
6. **Feature Retention**: L2 mantém todos os features contribuindo

---

*Atualizado em: 2026-03-10*