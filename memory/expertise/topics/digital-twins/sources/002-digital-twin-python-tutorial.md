# How to Build a Digital Twin - Python Tutorial

**Fonte:** https://towardsdatascience.com/how-to-build-a-digital-twin-b31058fd5d3e/  
**Tipo:** Tutorial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** 20 min

---

## 📋 Resumo Executivo

Tutorial prático que demonstra como criar um **Digital Twin híbrido** em Python usando um modelo matemático semi-empírico combinado com Machine Learning (Neural Network). O caso de uso é uma bateria de íon-lítio com previsão de degradação.

---

## 🎯 Conceitos Fundamentais

### O que é um Digital Twin?

> "Um objeto virtual que representa um subsistema. Este 'twin' deve responder a variáveis de entrada da mesma forma que seu 'physical twin'."

**Características principais:**
- Replica ativos físicos no mundo virtual
- Modelo que simula comportamento "físico" em contexto digital
- Pode ser qualquer coisa modelável: bateria, bomba, pessoa, cidade

### Tipos de Digital Twins

1. **Puros (Modelo Físico)** - Apenas modelo matemático
2. **Data-Driven (ML)** - Apenas dados experimentais + ML
3. **Híbridos** - Modelo físico + ML para refinamento

---

## 🔬 Caso de Uso: Bateria Li-ion

### Física do Problema

**Degradação de baterias Li-ion:**
- Após ciclos de carga-descarga, células degradam
- Redução da capacidade de carga
- End-of-life: 80% da capacidade máxima nominal

### Modelo Semi-Empírico

**Equação 1 - Vida útil da bateria:**
```
L = L' * (1 - f_d)
```
Onde:
- L = vida útil da bateria
- L' = vida útil inicial
- f_d = taxa de degradação linearizada

**Equação 2 - Taxa de degradação:**
```
f_d(t, δ, σ, T_c) = k * exp(...)
```
Onde:
- t = tempo de descarga
- δ = profundidade do ciclo de descarga
- σ = estado médio de carga do ciclo
- T_c = temperatura da célula
- k = constante empírica (0.13)

---

## 🛠️ Implementação em Python

### Arquitetura do Hybrid Digital Twin

```
┌─────────────────────────────────────────────────────────┐
│              HYBRID DIGITAL TWIN                        │
│                                                         │
│  ┌─────────────────┐      ┌─────────────────────┐      │
│  │  Mathematical   │      │    Neural Network   │      │
│  │     Model       │──────│   (Correction)     │      │
│  │  (Semi-empirical)│      │                     │      │
│  └─────────────────┘      └─────────────────────┘      │
│          │                          │                  │
│          └──────────┬───────────────┘                  │
│                     ▼                                   │
│          ┌─────────────────┐                            │
│          │  Digital Twin   │                            │
│          │   Output        │                            │
│          └─────────────────┘                            │
└─────────────────────────────────────────────────────────┘
```

### Código Principal

**Inputs e Outputs:**
```python
# Define inputs and outputs
# input: the simulation capacity
X_in = (dfb['C. Capacity'])
# output: difference between experimental values and simulation
X_out = (dfb['Capacity']) - (dfb['C. Capacity'])
X_in_train, X_in_test, X_out_train, X_out_test = train_test_split(
    X_in, X_out, test_size=0.33
)
```

**Neural Network:**
```python
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(1,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

# Compilation
epochs = 100
loss = 'mse'
model.compile(
    optimizer=SGD(learning_rate=0.001),
    loss=loss,
    metrics=['mae']  # Mean Absolute Error
)

history = model.fit(
    X_in_train,
    X_out_train,
    shuffle=True,
    epochs=epochs,
    batch_size=20,
    validation_data=(X_in_test, X_out_test),
    verbose=1
)
```

**Digital Twin Final:**
```python
# Our digital twin by improving our model with experimental data
X_twin = X_in + model.predict(X_in).reshape(-1)
```

---

## 📊 Resultados

### Comparação de Modelos

| Modelo | MAE | Características |
|--------|-----|-----------------|
| Modelo Matemático | 0.004 | Semi-empírico, generalizável |
| Digital Twin Híbrido | Menor | Refinado com dados experimentais |
| ML Puro | - | Menos generalizável, precisa mais dados |

### Vantagens do Hybrid Twin

1. **Sobre Modelo Matemático Puro:**
   - Pode ser melhorado com dados experimentais
   - Adapta-se a diferenças entre modelo e realidade

2. **Sobre ML Puro:**
   - Mais generalizável
   - Precisa de menos dados para treinar
   - Aplicável a outras baterias com melhor precisão

---

## 📝 Lições Aprendidas

### Quando Usar Cada Abordagem

| Cenário | Abordagem Recomendada |
|---------|----------------------|
| Dados abundantes | ML Puro pode funcionar |
| Modelo físico conhecido | Modelo matemático + refinamento |
| Poucos dados | Hybrid Twin (físico + ML) |
| Generalização necessária | Hybrid Twin |

### Processo de Criação

1. **Criar modelo físico/matemático** - Base teórica
2. **Comparar com dados experimentais** - Validar
3. **Usar ML para correção** - Refinar diferenças
4. **Combinar modelos** - Digital Twin final

---

## 🔗 Recursos

- **Código:** https://github.com/Javihaus/Digital-Twin-in-python
- **Dados:** [NASA Li-ion Battery Aging Datasets](https://data.nasa.gov/dataset/Li-ion-Battery-Aging-Datasets/uj5r-zjdb)
- **Libraries:** Keras, Plotly

---

## 📚 Referências Citadas

1. B. Xu et al. (2018). Modeling of Lithium-Ion Battery Degradation for Cell Life Assessment. IEEE Transactions on Smart Grid.
2. I. Laresgoiti et al. (2015). Modeling mechanical degradation in lithium ion batteries during cycling. Journal of Power Sources.

---

## 💡 Aplicações Práticas

Este padrão de Hybrid Digital Twin pode ser aplicado para:
- Previsão de vida útil de equipamentos
- Monitoramento de ativos industriais
- Otimização de processos manufatureiros
- Sistemas de manutenção preditiva
- Gestão de frotas de veículos elétricos