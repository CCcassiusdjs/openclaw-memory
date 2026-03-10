# Regularization in Machine Learning: L1, L2, and Beyond

**Fonte:** Consolidado de múltiplas fontes
**Tipo:** Conceito fundamental
**Categoria:** ML Fundamentals / Regularization

---

## O Que é Regularização?

Regularização é uma técnica para **prevenir overfitting** adicionando penalidades à função de loss, restringindo a complexidade do modelo.

---

## Por Que Regularização?

### Overfitting
- **Definição**: Modelo aprende ruído ao invés de padrões
- **Sintomas**: Alto erro de treino, baixo erro de teste
- **Causas**: Modelo muito complexo, pouco dados

### Underfitting
- **Definição**: Modelo não aprende padrões suficientes
- **Sintomas**: Alto erro em ambos treino e teste
- **Causas**: Modelo muito simples

### Trade-off Bias-Variance
- **High Bias**: Underfitting, modelo simples demais
- **High Variance**: Overfitting, modelo complexo demais
- **Regularização**: Balanço ideal

---

## Regularização L1 (Lasso)

### Fórmula
```
Loss = Original_Loss + λ Σ|wᵢ|
```

### Características
- **Esparsidade**: Zera pesos pequenos
- **Feature Selection**: Automática
- **Interpretabilidade**: Mantém features importantes

### Quando Usar
- Feature selection é importante
- Alta dimensionalidade
- Interpretabilidade é prioridade

### Derivada
```
∂L/∂w = ∂Loss/∂w + λ·sign(w)
```

---

## Regularização L2 (Ridge)

### Fórmula
```
Loss = Original_Loss + λ Σwᵢ²
```

### Características
- **Pesos pequenos**: Penaliza mas não zera
- **Stabilidade**: Melhora condição numérica
- **Smoothness**: Solução mais suave

### Quando Usar
- Todas features são relevantes
- Colinearidade entre features
- Estabilidade numérica

### Derivada
```
∂L/∂w = ∂Loss/∂w + 2λw
```

---

## Elastic Net (L1 + L2)

### Fórmula
```
Loss = Original_Loss + λ₁ Σ|wᵢ| + λ₂ Σwᵢ²
```

### Características
- Combina benefícios de L1 e L2
- Esparsidade + estabilidade
- Dois hiperparâmetros para ajustar

### Quando Usar
- Features correlacionadas
- Precisa de esparsidade mas com estabilidade

---

## Comparação L1 vs L2

| Aspecto | L1 (Lasso) | L2 (Ridge) |
|---------|------------|------------|
| **Solução** | Esparsa | Densa |
| **Feature Selection** | Sim | Não |
| **Derivada** | Não-diferenciável | Diferenciável |
| **Otimização** | Coordinate descent | Closed-form ou GD |
| **Robustez** | Menos robusto a outliers | Mais robusto |
| **Colinearidade** | Seleciona uma feature | Distribui pesos |

---

## Outras Técnicas de Regularização

### Dropout (Neural Networks)
- Zera neurônios aleatoriamente durante treino
- Taxa típica: 0.2-0.5
- Previne co-adaptação de neurônios

### Batch Normalization
- Normaliza ativações em cada camada
- Reduz internal covariate shift
- Tem efeito regularizador

### Early Stopping
- Para treino quando erro de validação aumenta
- Previne overfitting
- Hiperparâmetro: patience

### Data Augmentation
- Aumenta dataset artificialmente
- Comum em computer vision
- Reduz overfitting

### Weight Decay
- Similar a L2, mas aplicado diferente em otimizadores
- AdamW: Weight decay corrigido

---

## Escolha do Parâmetro λ

### Técnicas
1. **Grid Search**: Testa valores em grade
2. **Random Search**: Testa valores aleatórios
3. **Cross-Validation**: Validação cruzada
4. **Bayesian Optimization**: Otimização inteligente

### Valores Típicos
- **L1**: λ ∈ [0.001, 1.0]
- **L2**: λ ∈ [0.001, 10.0]
- **Elastic Net**: λ₁, λ₂ ∈ [0.001, 1.0]

---

## Regularização em Frameworks

### scikit-learn
```python
# Lasso (L1)
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)

# Ridge (L2)
from sklearn.linear_model import Ridge
model = Ridge(alpha=0.1)

# Elastic Net
from sklearn.linear_model import ElasticNet
model = ElasticNet(alpha=0.1, l1_ratio=0.5)
```

### PyTorch
```python
# L2 via weight_decay
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.01)

# L1 manual
l1_loss = sum(p.abs().sum() for p in model.parameters())
loss = original_loss + lambda * l1_loss
```

### TensorFlow/Keras
```python
from tensorflow.keras import regularizers

# L1
model.add(Dense(64, kernel_regularizer=regularizers.l1(0.01)))

# L2
model.add(Dense(64, kernel_regularizer=regularizers.l2(0.01)))

# Elastic Net
model.add(Dense(64, kernel_regularizer=regularizers.l1_l2(0.01, 0.01)))
```

---

## Conceitos-Chave

### Normas
- **L1 Norm**: Σ|wᵢ| (Manhattan distance)
- **L2 Norm**: √(Σwᵢ²) (Euclidean distance)
- **L∞ Norm**: max|wᵢ|

### Lagrangiano
```
L(w, λ) = Loss(w) + λ||w||ₚ
```
- Onde ||w||ₚ é a norma-p (p=1 para L1, p=2 para L2)

### Condição de Otimalidade
```
∇w L(w*, λ) = 0
```
- Ponto de mínimo satisfaz gradiente zero

---

## Citações Notáveis

> "Regularization is the process of adding information in order to solve an ill-posed problem or to prevent overfitting."

> "L1 regularization produces sparse models, which can be useful for feature selection."

---

## Status
- [x] Conceito consolidado
- [ ] Implementação comparativa

---

## Próximos Passos
1. Implementar comparação L1 vs L2 em dataset real
2. Visualizar peso de features com diferentes λ
3. Comparar Elastic Net com L1 e L2 puros

---

*Fonte consolidada em: 2026-03-10*