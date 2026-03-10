# How to Build a Digital Twin - Hybrid Battery Example

**Fonte:** https://towardsdatascience.com/how-to-build-a-digital-twin-b31058fd5d3e/
**Tipo:** Tutorial (Towards Data Science)
**Autor:** Javier Marin
**Data:** 2026-03-10
**Lido:** 2026-03-10

---

## Resumo

Tutorial prático de criação de Digital Twin híbrido para baterias Li-ion. Combina modelo físico semi-empírico com Machine Learning (Neural Network) para melhorar previsões de degradação de capacidade.

---

## Conceitos Fundamentais

### Digital Twin Definition
> "A digital twin is a virtual object that represents a subsystem. This twin is expected to respond to input variables in the same way that its physical twin does."

### Princípio Básico
1. **Virtual Object** - Representação digital do físico
2. **Model Integration** - Modelo que simula comportamento físico
3. **Response Match** - Twin responde como o físico

### Virtual System vs Digital Twin
- **Virtual System**: Sistema completo de subsistemas virtualizados
- **Digital Twin**: Objeto virtual de um único subsistema

---

## Modelo de Bateria Li-ion

### Física da Degradação
- Baterias Li-ion degradam após ciclos de carga/descarga
- **End-of-life**: Quando capacidade atinge 80% da nominal
- Degradação depende de: tempo de descarga, profundidade de ciclo, estado de carga médio, temperatura

### Modelo Semi-Empírico

**Equação 1 - Capacidade:**
```
C = C₀ - fd(i) * i
```
Onde:
- C = Capacidade atual
- C₀ = Capacidade inicial
- fd = Taxa de degradação linearizada
- i = Ciclo de carga/descarga

**Equação 2 - Taxa de Degradação:**
```
fd = f(t, δ, σ, Tc)
```
Onde:
- t = Tempo de descarga
- δ = Profundidade do ciclo
- σ = Estado de carga médio
- Tc = Temperatura da célula

---

## Dados Experimentais

### Dataset NASA Ames PCoE
- Dados de ciclos de carga/descarga
- Bateria número 5 usada como exemplo
- Feature principal: Capacidade vs. Ciclos

### Comparação Modelo vs. Real
- **MAE (Mean Absolute Error)**: 0.004
- Modelo captura tendência geral
- Diferenças sutis nas primeiras etapas

---

## Hybrid Digital Twin

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    HYBRID DIGITAL TWIN                        │
│                                                               │
│   ┌─────────────────┐       ┌─────────────────┐             │
│   │ Physical Model  │──────►│  NN Correction  │             │
│   │ (Semi-empirical)│       │  (Δ = Real -    │             │
│   │                 │       │   Model)         │             │
│   └─────────────────┘       └─────────────────┘             │
│           │                        │                        │
│           └────────────────────────┘                        │
│                        ▼                                      │
│              ┌─────────────────┐                              │
│              │ Digital Twin    │                              │
│              │ = Model + Δ_NN  │                              │
│              └─────────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

### Implementação Python

**Dados de Entrada/Saída:**
```python
# Input: capacidade simulada pelo modelo
X_in = dfb['C. Capacity']

# Output: diferença entre experimental e simulado
X_out = dfb['Capacity'] - dfb['C. Capacity']
```

**Neural Network:**
```python
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(1,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

model.compile(
    optimizer=SGD(learning_rate=0.001),
    loss='mse',
    metrics=['mae']
)

history = model.fit(
    X_in_train,
    X_out_train,
    shuffle=True,
    epochs=100,
    batch_size=20,
    validation_data=(X_in_test, X_out_test)
)
```

### Resultado Final
```python
# Digital Twin = Physical Model + NN Correction
X_twin = X_in + model.predict(X_in).reshape(-1)
```

---

## Vantagens do Hybrid DT

### vs. Modelo Puramente Matemático
- **Precisão melhorada**: NN aprende diferenças não capturadas pelo modelo
- **Generalização**: Melhor que ML puro com menos dados
- **Física + Dados**: Combina conhecimento físico com dados reais

### vs. ML Puro
- **Menos dados**: Modelo físico fornece base, ML ajusta
- **Extrapolation**: Melhor para fora do range de treinamento
- **Interpretabilidade**: Física ainda é compreensível

---

## Conceitos Aprendidos

- [x] **Hybrid Digital Twin** - Combina modelo físico com ML
- [x] **Semi-empirical model** - Equações baseadas em física + ajustes empíricos
- [x] **NN correction** - Neural network aprende diferença (real - modelo)
- [x] **Li-ion degradation** - Degradação depende de múltiplos fatores
- [x] **End-of-life (80%)** - Critério padrão para bateria EOL
- [x] **NASA Ames PCoE Dataset** - Dados públicos para battery aging
- [x] **MAE metric** - Mean Absolute Error para avaliação
- [x] **Model + Δ structure** - Estrutura: Physical Model + Neural Correction

---

## Insights

1. **Menos dados necessários**: Hybrid DT precisa de menos dados que ML puro
2. **Física é base**: Modelo físico captura comportamento geral, ML refina
3. **Preditivo**: DT permite fazer predições sobre vida útil
4. **Incremental**: Pode adicionar mais dados experimentais para melhorar

---

## Predição

Com o Hybrid DT, podemos:
- Predizer capacidade futura
- Estimar vida útil restante
- Otimizar ciclos de uso
- Planejar substituição preventiva

---

## Código e Dados

- **Código**: https://github.com/Javihaus/Digital-Twin-in-python
- **Dados**: NASA Li-ion Battery Aging Datasets

---

## Referências

- Chu et al. (2018) - Battery Life Assessment
- Laresgoiti et al. (2015) - Battery Degradation Modeling
- NASA Ames PCoE - Li-ion Battery Aging Datasets