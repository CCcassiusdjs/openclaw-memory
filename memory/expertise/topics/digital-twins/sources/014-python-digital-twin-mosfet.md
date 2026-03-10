# Digital Twin with Python: A Hands-on Example

**Fonte:** https://towardsdatascience.com/digital-twin-with-python-a-hands-on-example-2a3036124b61/
**Tipo:** Tutorial (Towards Data Science)
**Autor:** Tirthajyoti Sarkar
**Data:** 2026-03-10
**Lido:** 2026-03-10

---

## Resumo

Tutorial prático de implementação de Digital Twin em Python, usando MOSFET como objeto físico de exemplo. Demonstra como criar um DT usando classes Python, modelos analíticos e ML (Deep Neural Networks) para modelar características diferentes.

---

## Conceitos Fundamentais

### O que é um Digital Twin (Definição IBM)
> "A digital twin is a virtual model designed to accurately reflect a physical object."

### Componentes Habilitadores
1. **Sensores** - Coletam dados do objeto físico
2. **Processadores** - Inserem dados no modelo digital
3. **Modelo Digital** - Representação virtual
4. **Simulação** - Testar cenários e melhorias

### Mapeamento Python
```
┌─────────────────────┐      ┌─────────────────────┐
│   Physical Object   │◄────►│   Python Object      │
│   (MOSFET)          │      │   (Class MOSFET)     │
│                     │      │                     │
│   - Sensors         │      │   - Methods          │
│   - Data            │──────►│   - Variables        │
│   - Behavior        │      │   - Models           │
└─────────────────────┘      └─────────────────────┘
```

---

## Implementação Python

### Estrutura da Classe MOSFET

```python
class MOSFET:
    def __init__(self, params=None, terminals=None):
        # Parâmetros do MOSFET
        if params is None:
            self._params_ = {
                'BV': 20,      # Breakdown Voltage
                'Vth': 1.0,    # Threshold Voltage
                'gm': 1e-2     # Transconductance
            }
        else:
            self._params_ = params
        
        # Terminais
        if terminals is None:
            self._terminals_ = {
                'source': 0.0,
                'drain': 0.0,
                'gate': 0.0
            }
        else:
            self._terminals_ = terminals
        
        # Estado (ON/OFF)
        self._state_ = self.determine_state()
    
    def __repr__(self):
        return "Digital Twin of a MOSFET"
```

### Parâmetros do MOSFET
- **Vth (Threshold Voltage)**: Tensão limiar entre Gate e Source
- **gm (Transconductance)**: "Facilidade" de condução de corrente
- **BV (Breakdown Voltage)**: Tensão máxima antes de breakdown

---

## Modelo Analítico vs ML

### Quando Usar Analítico
- **Física bem compreendida**: Equações conhecidas
- **Dados limpos**: Sem ruído significativo
- **Relações determinísticas**: Causa-efeito claro
- **Performance crítica**: Resposta rápida necessária

### Quando Usar ML
- **Fenômenos complexos**: Física não linear, difícil de modelar
- **Dados ruidosos**: Variabilidade natural
- **Comportamento estocástico**: Aleatoriedade intrínseca
- **Trade-offs aceitáveis**: Performance vs. precisão

---

## Características Modeladas

### Característica ON-State (Analítico)
```python
def id_vd(self, vgs=None, vds=None, rounding=True):
    """
    Calcula corrente drain-source usando modelo analítico
    """
    if state == 'ON':
        if vds <= vgs - vth:
            # Região linear
            ids = self._params_['gm'] * (vgs - vth - (vds/2)) * vds
        else:
            # Região de saturação
            ids = (self._params_['gm']/2) * (vgs - vth)**2
    return ids
```

### Característica OFF-State (ML)
```python
def train_leakage(self, data=None, batch_size=5, epochs=20, learning_rate=2e-5):
    """
    Treina modelo DNN para leakage current
    """
    # Deep learning model
    model = build_model(
        num_layers=3,
        architecture=[32, 32, 32],
        input_dim=3
    )
    # Compile and train
    model_trained = compile_train_model(
        model, X_train_scaled, y_train_scaled,
        batch_size=batch_size,
        epochs=epochs,
        learning_rate=learning_rate
    )
    self.leakage_model = model_trained

def leakage(self, w_l=1e-2, vgs=None, vth=None):
    """
    Prediz leakage current usando modelo treinado
    """
    x = np.array([w_l, vgs, vth])
    ip = x.reshape(-1, 3)
    result = float(10**(-self.leakage_model.predict(ip)))
    return result
```

---

## Resultados

### Curvas I-V Characteristics
- **Gráfico Ids vs Vds**: Curvas características para diferentes Vgs
- **Regiões**: Linear e saturação bem definidas
- **Match com física**: Comportamento corresponde ao MOSFET ideal

### Modelo de Leakage
- **DNN com 3 camadas**: 32 neurônios cada
- **Entrada**: w_l, Vgs, Vth
- **Saída**: log(leakage current)
- **Treinamento**: Dados sintéticos com variabilidade

---

## Conceitos Aprendidos

- [x] **Mapeamento Physical-Digital**: Como Python classes representam objetos físicos
- [x] **Parâmetros vs Terminais**: Diferença entre características e estado atual
- [x] **Modelo híbrido**: Analítico para ON-state, ML para OFF-state
- [x] **Transconductance (gm)**: "Facilidade" de condução, inverso de resistência
- [x] **Threshold Voltage (Vth)**: Tensão que define estado ON/OFF
- [x] **Breakdown Voltage (BV)**: Limite antes de condução descontrolada
- [x] **Sub-threshold leakage**: Corrente de fuga quando OFF (fenômeno quântico)
- [x] **DNN para características não-lineares**: ML onde física é complexa
- [x] **Swappable models**: DT permite trocar analítico por ML e vice-versa
- [x] **Data-driven + Physics-guided**: Combinação de conhecimento físico e dados

---

## Insights

1. **Occam's Razor para DT**: Começar simples, adicionar complexidade gradualmente
2. **Não é tudo ML**: Conhecimento físico (analítico) ainda é valioso
3. **Swappable models**: Beleza do DT é poder trocar modelos facilmente
4. **Variabilidade é real**: Processos de fabricação introduzem variabilidade
5. **Digital Twin != Simulação**: DT tem conexão bidirecional com físico

---

## Expansão do Digital Twin

### Conexão com Sistemas Industriais
- **Upstream**: Conectar com sensores reais
- **Downstream**: Conectar com sistemas de controle
- **Integration**: Integração com PLCs, SCADA, MES

### Princípios de Design
1. **Connection**: Conectar com sistemas externos
2. **Communication**: Protocolos padronizados
3. **Co-work**: Colaboração com outros sistemas

### Data Structures
- Escolher estruturas que integram bem
- APIs bem definidas
- Formatos padronizados (JSON, Protocol Buffers)

---

## Próximos Passos

- [ ] Implementar modelo mais complexo (BJT, IGBT)
- [ ] Adicionar sensores reais via MQTT
- [ ] Conectar com banco de dados (TimescaleDB, InfluxDB)
- [ ] Implementar otimização de parâmetros
- [ ] Criar dashboard de visualização

---

## Código Completo

Disponível em: https://github.com/tirthajyoti/Digital-Twin/blob/main/MOSFET-1.ipynb

---

## Referências

- IBM Digital Twin Definition
- MOSFET Basics: electronics-tutorials.ws
- Occam's Razor Principle
- Keras Deep Learning Documentation