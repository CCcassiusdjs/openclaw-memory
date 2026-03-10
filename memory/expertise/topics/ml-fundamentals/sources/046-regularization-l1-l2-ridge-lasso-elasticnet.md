# Regularization Techniques: L1, L2, Ridge, LASSO, ElasticNet

**Fonte:** https://www.analyticsvidhya.com/blog/2021/07/prevent-overfitting-using-regularization-techniques/
**Data:** 2026-03-10
**Status:** Completed

---

## Resumo

Regularização é técnica para prevenir overfitting penalizando coeficientes grandes. L1 (LASSO) e L2 (Ridge) são as duas normas principais.

---

## Overfitting e Regularização

### O Problema do Overfitting
- Modelo aprende "b demais" nos dados de treino
- Aprende detalhes E ruído
- Performance ruim em dados novos

### Causas de Overfitting
- Dataset pequeno demais
- Dados com muito ruído
- Treinamento por tempo excessivo
- Modelo muito complexo

### Sintomas
- RMSE treino muito menor que RMSE teste
- Alta variância entre treino e teste
- Modelo não generaliza

### Regularização como Solução
- Penaliza coeficientes inflacionados
- Adiciona termo de penalização à função de custo
- Não descarta features (diferente de feature selection)

---

## L1 Regularization (LASSO)

### Definição
**L**east **A**bsolute **S**hrinkage and **S**election **O**perator

### Fórmula
```
Cost = RSS + α * Σ|β_j|
```

Onde:
- RSS = Residual Sum of Squares
- α = parâmetro de regularização
- β_j = coeficientes do modelo

### Características
- Usa valor absoluto dos coeficientes
- **Pode zerar coeficientes** (feature selection!)
- Esparsidade: produz modelos esparsos
- Bom quando poucas features são relevantes

### Quando Usar
- Feature selection é desejada
- Suspeita de features irrelevantes
- Interpretabilidade é importante

---

## L2 Regularization (Ridge)

### Definição
Regularização Ridge (Tikhonov regularization)

### Fórmula
```
Cost = RSS + α * Σβ_j²
```

### Características
- Usa quadrado dos coeficientes
- **Não zera coeficientes**, mas reduz para próximo de zero
- Distribui peso entre features correlacionadas
- Bom quando muitas features contribuem

### Quando Usar
- Muitas features correlacionadas
- Não se quer descartar features
- Multicolinearidade é problema

---

## Comparação L1 vs L2

| Característica | L1 (LASSO) | L2 (Ridge) |
|----------------|------------|------------|
| **Penalidade** | Σ\|β_j\| | Σβ_j² |
| **Zerar coeficientes** | Sim | Não |
| **Esparsidade** | Alta | Baixa |
| **Feature selection** | Automática | Não |
| **Features correlacionadas** | Seleciona uma | Distribui peso |
| **Geometria** | Diamante | Círculo |
| **Derivabilidade** | Não (em zero) | Sim |

---

## ElasticNet

### Definição
Combinação de L1 e L2

### Fórmula
```
Cost = RSS + α₁ * Σ|β_j| + α₂ * Σβ_j²
```

Ou, equivalentemente:
```
Cost = RSS + α * (λ * Σ|β_j| + (1-λ) * Σβ_j²)
```

Onde λ é o parâmetro de mixagem (l1_ratio em sklearn).

### Características
- Combina benefícios de L1 e L2
- L1: esparsidade e feature selection
- L2: estabilidade com features correlacionadas

### Quando Usar
- Features correlacionadas E deseja-se feature selection
- Melhor que LASSO quando há correlação entre features

---

## Implementação em Python

### LASSO Regression
```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)  # α controla força da regularização
lasso.fit(X_train, y_train)

# Predição
y_pred = lasso.predict(X_test)

# Coeficientes (alguns podem ser zero)
print(lasso.coef_)
```

### Ridge Regression
```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=0.1)
ridge.fit(X_train, y_train)

# Predição
y_pred = ridge.predict(X_test)

# Coeficientes (nenhum é exatamente zero)
print(ridge.coef_)
```

### ElasticNet
```python
from sklearn.linear_model import ElasticNet

# l1_ratio = 0.5: mistura igual de L1 e L2
enet = ElasticNet(alpha=0.1, l1_ratio=0.5)
enet.fit(X_train, y_train)

y_pred = enet.predict(X_test)
```

---

## Hyperparameter Tuning

### Cross-Validation
```python
from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV

# LASSO com CV
lasso_cv = LassoCV(cv=5)  # Encontra melhor α automaticamente
lasso_cv.fit(X_train, y_train)

# Ridge com CV
ridge_cv = RidgeCV(cv=5)
ridge_cv.fit(X_train, y_train)

# ElasticNet com CV
enet_cv = ElasticNetCV(cv=5, l1_ratio=[0.1, 0.5, 0.9])
enet_cv.fit(X_train, y_train)
```

---

## Interpretação Geométrica

### L1 (LASSO)
- Contorno de custo forma um **diamante**
- Interseção com elipse RSS tende a ocorrer nos vértices
- Vértices correspondem a coeficientes zero
- Resultado: esparsidade

### L2 (Ridge)
- Contorno de custo forma um **círculo**
- Interseção com elipse RSS pode ocorrer em qualquer ponto
- Coeficientes são reduzidos mas não zerados
- Resultado: shrinkage sem esparsidade

---

## Boas Práticas

### Escolha de α
- α pequeno: pouca regularização (pode overfitting)
- α grande: muita regularização (pode underfitting)
- Usar **cross-validation** para encontrar melhor valor

### Diagnóstico
```python
# Calcular RMSE
from sklearn.metrics import mean_squared_error
import numpy as np

train_rmse = np.sqrt(mean_squared_error(y_train, model.predict(X_train)))
test_rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))

print(f"Train RMSE: {train_rmse:.4f}")
print(f"Test RMSE: {test_rmse:.4f}")

# Se train_rmse << test_rmse → overfitting
# Se train_rmse ≈ test_rmse → bom fit
# Se ambos altos → underfitting
```

### Quando Regularizar
- RMSE treino muito menor que teste
- Muitas features (alta dimensionalidade)
- Features correlacionadas (multicolinearidade)
- Poucos dados de treino

---

## Conceitos Aprendidos

1. **Regularização**: Penalizar coeficientes grandes para prevenir overfitting
2. **L1 (LASSO)**: Valor absoluto, produz esparsidade, feature selection
3. **L2 (Ridge)**: Quadrado, shrinkage sem zerar, estabilidade
4. **ElasticNet**: Combinação de L1 e L2, melhor de ambos
5. **Hyperparameter α**: Controla força da regularização
6. **Diagnóstico**: Comparar RMSE treino vs teste

---

*Atualizado em: 2026-03-10*