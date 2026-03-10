# Gradient Descent Types (Batch, Stochastic, Mini-batch)

**Fonte:** https://ml-cheatsheet.readthedocs.io/en/latest/gradient_descent.html + https://www.ibm.com/think/topics/gradient-descent
**Data:** 2026-03-10
**Status:** Completed

---

## Resumo

Gradient Descent é o algoritmo de otimização mais usado em machine learning para minimizar funções de custo. Existem três variantes principais com diferentes trade-offs.

---

## Gradient Descent - Fundamentos

### Definição
Algoritmo de otimização que minimiza uma função iterativamente movendo-se na direção do gradiente negativo (steepest descent).

### Aplicações em ML
- Atualizar parâmetros de modelos
- Coeficientes em Linear Regression
- Weights em neural networks

### Intuição Visual
- Começa no topo de uma "montanha" (custo alto)
- Move-se na direção do gradiente negativo
- Continua até chegar ao "vale" (custo mínimo)

---

## Learning Rate

### Definição
Tamanho dos passos em cada iteração. Controla a velocidade de convergência.

### Trade-offs
| Learning Rate | Vantagens | Desvantagens |
|---------------|-----------|--------------|
| **Alto** | Passos grandes, rápido | Risco de overshooting, pode divergir |
| **Baixo** | Precisão, converge ao mínimo | Lento, computacionalmente caro |

### Prática
- Valores típicos: 0.001 a 0.1
- Learning rate scheduling: ajustar durante treinamento
- Adaptive methods (Adam, etc.) ajustam automaticamente

---

## Cost Function

### Definição
Mede "quão bom" o modelo é para um conjunto de parâmetros.

### Derivadas Parciais
Para função de custo com múltiplos parâmetros, calculamos o gradiente:

```
∇f(m,b) = [∂f/∂m, ∂f/∂b]
```

### Fórmula (MSE)
```
f(m,b) = (1/N) Σ(y_i - (mx_i + b))²

∂f/∂m = -(2/N) Σ x_i(y_i - (mx_i + b))
∂f/∂b = -(2/N) Σ (y_i - (mx_i + b))
```

---

## Três Tipos de Gradient Descent

### 1. Batch Gradient Descent

**Como funciona:**
- Calcula erro para TODOS os exemplos de treino
- Soma os gradientes
- Atualiza parâmetros uma vez por época

**Fórmula:**
```
θ = θ - η · ∇J(θ)
```
onde J é calculada sobre todo o dataset.

**Vantagens:**
- Convergência estável
- Garantido convergir ao mínimo global (convex) ou local (non-convex)
- Computacionalmente eficiente em vetorização

**Desvantagens:**
- Lento para datasets grandes
- Requer memória para todo o dataset
- Pode ficar preso em mínimos locais

**Quando usar:**
- Datasets pequenos/médios
- Convergência estável é crítica

---

### 2. Stochastic Gradient Descent (SGD)

**Como funciona:**
- Atualiza parâmetros para CADA exemplo de treino
- Uma atualização por exemplo (não por época)

**Fórmula:**
```
θ = θ - η · ∇J(θ; x^(i), y^(i))
```

**Vantagens:**
- Rápido para datasets grandes
- Pode usar online learning
- Gradientes "ruidosos" ajudam escapar de mínimos locais
- Menor uso de memória (um exemplo por vez)

**Desvantagens:**
- Alta variância nas atualizações
- Oscilações durante treinamento
- Pode overshoot o mínimo
- Convergência menos estável

**Quando usar:**
- Datasets muito grandes
- Online learning
- Quando velocidade é prioritária

---

### 3. Mini-batch Gradient Descent

**Como funciona:**
- Divide o dataset em batches de tamanho n
- Atualiza após cada batch
- Combina benefícios de batch e SGD

**Fórmula:**
```
θ = θ - η · ∇J(θ; x^(i:i+n), y^(i:i+n))
```

**Tamanhos típicos de batch:**
- 32, 64, 128, 256 (potências de 2)
- Depende de memória disponível

**Vantagens:**
- Balance entre velocidade e estabilidade
- Reduz variância das atualizações (vs SGD)
- Usa vetorização eficiente (vs SGD)
- Convergência mais suave

**Desvantagens:**
- Precisa escolher tamanho de batch
- Pode ainda oscilar

**Quando usar:**
- **Padrão da indústria** para deep learning
- Maioria dos frameworks usa mini-batch por default

---

## Comparação

| Método | Atualizações por Época | Memória | Estabilidade | Velocidade |
|-------|------------------------|---------|--------------|------------|
| Batch | 1 | Alta | Alta | Lento |
| SGD | N (dataset size) | Baixa | Baixa (oscila) | Rápido |
| Mini-batch | N/batch_size | Média | Média | Balanceado |

---

## Desafios do Gradient Descent

### 1. Local Minima e Saddle Points
- **Local minimum**: Ponto onde gradiente é zero, mas não é o mínimo global
- **Saddle point**: Ponto onde gradiente é zero em uma direção, mas não em outras

**Soluções:**
- SGD com momentum ajuda escapar
- Learning rate scheduling
- Métodos adaptativos (Adam)

### 2. Vanishing Gradients
- Gradiente diminui exponencialmente em layers anteriores
- Layers iniciais aprendem muito lentamente
- Comum em redes profundas e RNNs

**Soluções:**
- ReLU activation
- Batch normalization
- Residual connections
- Gradient clipping

### 3. Exploding Gradients
- Gradiente cresce exponencialmente
- Weights tornam-se NaN
- Instabilidade numérica

**Soluções:**
- Gradient clipping
- Weight regularization
- Arquiteturas específicas (LSTM para RNNs)

---

## Implementação Python

```python
def update_weights(m, b, X, Y, learning_rate):
    m_deriv = 0
    b_deriv = 0
    N = len(X)
    
    for i in range(N):
        # Derivadas parciais
        m_deriv += -2 * X[i] * (Y[i] - (m*X[i] + b))
        b_deriv += -2 * (Y[i] - (m*X[i] + b))
    
    # Atualização (subtração porque gradiente aponta para cima)
    m -= (m_deriv / float(N)) * learning_rate
    b -= (b_deriv / float(N)) * learning_rate
    
    return m, b
```

---

## Conceitos Aprendidos

1. **Tipos de Gradient Descent**: Batch, SGD, Mini-batch e seus trade-offs
2. **Learning Rate**: Controla passo de atualização, trade-off velocidade/precisão
3. **Cost Function**: Mede erro, gradientes guiam otimização
4. **Desafios**: Local minima, vanishing/exploding gradients
5. **Prática**: Mini-batch é padrão na indústria
6. **Derivadas Parciais**: Gradiente como vetor de derivadas parciais

---

## Próximos Passos

- [ ] Estudar métodos adaptativos (Adam, RMSprop)
- [ ] Learning rate scheduling
- [ ] Momentum e Nesterov acceleration

---

*Atualizado em: 2026-03-10*