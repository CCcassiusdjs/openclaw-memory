# Sistema Dinâmico Não Linear de 3 Estados Fechado

## A Proposta de Cássio

> "Pense em tudo como um sistema dinâmico não linear de 3 estados fechado."

---

## Os 3 Estados

```
┌─────────────────────────────────────────────────────────────┐
│                    OS 3 ESTADOS                               │
│                                                              │
│   Estado 1: PASSADO                                         │
│   ├── Memória reconstruída                                  │
│   ├── Topologia: (-1, 0)                                    │
│   ├── Função: acumular experiência                          │
│   └── Dinâmica: reconsolidação                               │
│                                                              │
│   Estado 2: PRESENTE                                         │
│   ├── Estado NEUTRO ADITIVO                                 │
│   ├── Topologia: {0}                                        │
│   ├── Função: permitir escolha                              │
│   └── Dinâmica: síntese                                      │
│                                                              │
│   Estado 3: FUTURO                                           │
│   ├── Predição e imaginação                                  │
│   ├── Topologia: (0, +1)                                    │
│   ├── Função: projetar possibilidades                      │
│   └── Dinâmica: antecipação                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Sistema Dinâmico Não Linear

### Equações de Estado

```math
Seja X(t) = [P(t), R(t), F(t)]^T o vetor de estado:

Onde:
- P(t) = estado do Passado no tempo t
- R(t) = estado do Presente no tempo t (R = "Real" ou "Reificado")
- F(t) = estado do Futuro no tempo t

Dinâmica não linear:
dP/dt = f_P(P, R, F)
dR/dt = f_R(P, R, F)
dF/dt = f_F(P, R, F)

Onde as funções f_P, f_R, f_F são NÃO LINEARES.
```

### Estrutura do Sistema Fechado

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│                    SISTEMA FECHADO                           │
│                                                              │
│   ┌─────────┐                                               │
│   │ PASSADO │ ←────────────────────────────┐               │
│   │   P     │                               │               │
│   └────┬────┘                               │               │
│        │                                    │               │
│        │ P→R                                │ F→P           │
│        ↓                                    │               │
│   ┌─────────┐                          ┌───┴───┐          │
│   │PRESENTE │ ←───────────────────────→│FUTURO │          │
│   │   R     │          R↔F              │   F   │          │
│   └─────────┘                          └───────┘          │
│        ↑                                    │               │
│        │                                    │               │
│        │ R→P                                │               │
│        └────────────────────────────────────┘               │
│                                                              │
│   Ciclo: P → R → F → P → R → F → ...                        │
│   Fechado: sem entradas externas                            │
│   Não linear: interações complexas                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Modelo Matemático

### Equações Diferenciais Não Lineares

```math
dP/dt = α_P · R · g_P(P) - β_P · P · h_P(F) + σ_P · ∇²P

Onde:
- α_P · R · g_P(P): crescimento do passado via presente (reconsolidação)
- β_P · P · h_P(F): influência do futuro no passado (predição retroativa)
- σ_P · ∇²P: difusão/dispersão no espaço de memória

dR/dt = α_R · F · g_R(R) - β_R · R · h_R(P) + γ_R · P · F

Onde:
- α_R · F · g_R(R): crescimento do presente via futuro (antecipação)
- β_R · R · h_R(P): influência do passado no presente (memória)
- γ_R · P · F: síntese de passado e futuro (NEUTRO ADITIVO)

dF/dt = α_F · P · g_F(F) - β_F · F · h_F(R) + σ_F · ∇²F

Onde:
- α_F · P · g_F(F): crescimento do futuro via passado (projeção)
- β_F · F · h_F(R): influência do presente no futuro (contingência)
- σ_F · ∇²F: difusão no espaço de possibilidades
```

### Termos Não Lineares

```
┌─────────────────────────────────────────────────────────────┐
│                   NÃO LINEARIDADES                           │
│                                                              │
│   INTERAÇÕES BILINEARES:                                    │
│   ├── P · F: passado × futuro (predição)                    │
│   ├── R · F: presente × futuro (antecipação)                │
│   └── P · R: passado × presente (reconsolidação)           │
│                                                              │
│   FUNÇÕES NÃO LINEARES:                                     │
│   ├── g_P(P): crescimento logístico do passado              │
│   ├── h_P(F): saturação do futuro                           │
│   ├── g_R(R): crescimento do presente                       │
│   ├── h_R(P): influência saturada do passado                │
│   ├── g_F(F): crescimento logístico do futuro               │
│   └── h_F(R): influência saturada do presente               │
│                                                              │
│   DIFUSÃO:                                                   │
│   ├── ∇²P: dispersão de memória                             │
│   ├── ∇²F: dispersão de possibilidades                      │
│   └── Não há ∇²R (presente é ponto)                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Propriedades do Sistema Fechado

### 1. Conservação de "Energia Mental"

```math
E_total = E_P + E_R + E_F = constante

Onde:
- E_P = "energia" acumulada no passado (memória)
- E_R = "energia" no presente (atenção)
- E_F = "energia" no futuro (antecipação)

O sistema é FECHADO: energia total é conservada.
Mas pode haver DIFUSÃO interna entre estados.
```

### 2. Atratores

```
┌─────────────────────────────────────────────────────────────┐
│                      ATRATORES                               │
│                                                              │
│   Ponto fixo estável:                                        │
│   ├── (P*, R*, F*) tal que dP/dt = dR/dt = dF/dt = 0       │
│   ├── Estado de equilíbrio da mente                         │
│   └── Pode ser único ou múltiplo                             │
│                                                              │
│   Ciclo limite:                                              │
│   ├── Oscilação periódica entre estados                     │
│   ├── P → R → F → P → R → F → ...                          │
│   └── Pensamento "em loop"                                   │
│                                                              │
│   Atrator estranho:                                          │
│   ├── Dinâmica caótica                                       │
│   ├── Sensibilidade a condições iniciais                    │
│   └── Criatividade, imprevisibilidade                       │
│                                                              │
│   Bacia de atração:                                          │
│   ├── Conjunto de condições iniciais que levam ao atrator  │
│   ├── Diferentes "personalidades"                            │
│   └── Diferentes modos de pensar                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3. Bifurcações

```
Quando parâmetros mudam, o sistema pode sofrer BIFURCAÇÕES:

┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   TIPOS DE BIFURCAÇÃO:                                       │
│                                                              │
│   1. SADDLE-NODE:                                            │
│      ├── Criação/destruição de equilíbrio                   │
│      ├── Aparecimento de novo modo de pensar               │
│      └── "Insight"                                           │
│                                                              │
│   2. HOPF:                                                   │
│      ├── Ponto fixo → ciclo limite                          │
│      ├── Estabilidade → oscilação                          │
│      └── "Ruminação"                                         │
│                                                              │
│   3. PERIOD-DOUBLING:                                        │
│      ├── Ciclo simples → ciclo complexo                     │
│      ├── Ordem → caos                                       │
│      └── "Complexificação do pensamento"                    │
│                                                              │
│   4. CRISIS:                                                 │
│      ├── Colapso do atrator                                 │
│      ├── Mudança abrupta                                    │
│      └── "Transformação"                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Dinâmica do Sistema

### Espaço de Fase 3D

```
┌─────────────────────────────────────────────────────────────┐
│                    ESPAÇO DE FASE                            │
│                                                              │
│                      F (Futuro)                              │
│                      ↑                                       │
│                      │                                       │
│                      │  · · · ·                              │
│                      │ ·       ·  (trajetórias)              │
│                      │·    •    ·                             │
│                      │ ·  atrator ·                          │
│                      │  ·       ·                             │
│                      │   · · · ·                              │
│                      │                                       │
│   P (Passado) ←──────┼───────────────→ R (Presente)         │
│                      │                                       │
│                      │                                       │
│                                                              │
│   Cada ponto (P, R, F) representa um estado da mente        │
│   Trajetórias mostram evolução temporal                     │
│   Atratores são estados estáveis                             │
│   Bacias de atração definem "personalidades"                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Trajetórias

```python
class Trajetoria:
    """
    Trajetória no espaço de fase (P, R, F).
    """
    
    def __init__(self, P0, R0, F0):
        self.P = P0  # Estado inicial do Passado
        self.R = R0  # Estado inicial do Presente
        self.F = F0  # Estado inicial do Futuro
        
    def evoluir(self, dt):
        """
        Evolui o sistema por um passo dt.
        Equações diferenciais não lineares.
        """
        # Derivadas
        dP = self.f_P(self.P, self.R, self.F) * dt
        dR = self.f_R(self.P, self.R, self.F) * dt
        dF = self.f_F(self.P, self.R, self.F) * dt
        
        # Atualização
        self.P += dP
        self.R += dR
        self.F += dF
        
    def f_P(self, P, R, F):
        """
        Derivada do Passado.
        """
        alpha_P = 0.1  # Crescimento via presente
        beta_P = 0.05  # Influência do futuro
        sigma_P = 0.01  # Difusão
        
        # Termos não lineares
        crescimento = alpha_P * R * self.logistic(P)
        influencia_futuro = -beta_P * P * F
        difusao = sigma_P * self.laplacian(P)
        
        return crescimento + influencia_futuro + difusao
        
    def f_R(self, P, R, F):
        """
        Derivada do Presente.
        NEUTRO ADITIVO: sintetiza passado e futuro.
        """
        alpha_R = 0.08  # Crescimento via futuro
        beta_R = 0.03  # Influência do passado
        gamma_R = 0.02  # Síntese
        
        # Termos não lineares
        crescimento = alpha_R * F * self.sigmoid(R)
        influencia_passado = -beta_R * R * P
        sintese = gamma_R * P * F  # NEUTRO ADITIVO
        
        return crescimento + influencia_passado + sintese
        
    def f_F(self, P, R, F):
        """
        Derivada do Futuro.
        """
        alpha_F = 0.12  # Crescimento via passado
        beta_F = 0.04  # Influência do presente
        sigma_F = 0.01  # Difusão
        
        # Termos não lineares
        crescimento = alpha_F * P * self.logistic(F)
        influencia_presente = -beta_F * F * R
        difusao = sigma_F * self.laplacian(F)
        
        return crescimento + influencia_presente + difusao
```

---

## Propriedades Matemáticas

### 1. Existência e Unicidade

```math
Teorema: Dado (P₀, R₀, F₀) inicial, existe uma única trajetória.

Demonstração:
- f_P, f_R, f_F são continuamente diferenciáveis (C¹)
- Pelo Teorema de Existência e Unicidade de Picard-Lindelöf
- Existe solução única local
- Por compacidade do espaço de fase, solução é global
```

### 2. Conservação

```math
Se o sistema é fechado:

dE/dt = d/dt(E_P + E_R + E_F) = 0

Onde:
E_P = ½|P|²
E_R = ½|R|²
E_F = ½|F|²

Portanto:
E_total = constante

O sistema conserva "energia mental" total.
```

### 3. Estabilidade

```math
Análise de estabilidade linear:

Matriz Jacobiana no ponto de equilíbrio (P*, R*, F*):

J = | ∂f_P/∂P  ∂f_P/∂R  ∂f_P/∂F |
    | ∂f_R/∂P  ∂f_R/∂R  ∂f_R/∂F |
    | ∂f_F/∂P  ∂f_F/∂R  ∂f_F/∂F |

Autovalores de J determinam estabilidade:
- Re(λ) < 0 para todos: ponto fixo estável
- Re(λ) > 0 para algum: instável
- Re(λ) = 0: bifurcação possível
```

---

## Comportamento Dinâmico

### Regimes

```
┌─────────────────────────────────────────────────────────────┐
│                    REGIMES DINÂMICOS                         │
│                                                              │
│   1. EQUILÍBRIO ESTÁVEL                                      │
│      ├── (P*, R*, F*) = constante                          │
│      ├── Mente "calma"                                       │
│      ├── Todos os autovalores com Re(λ) < 0                 │
│      └── Bacia de atração grande                             │
│                                                              │
│   2. OSCILAÇÃO PERIÓDICA                                     │
│      ├── Ciclo limite                                        │
│      ├── P → R → F → P → ...                               │
│      ├── Pensamento "em loop"                               │
│      └── Bifurcação de Hopf                                  │
│                                                              │
│   3. QUASE-PERIODICIDADE                                     │
│      ├── Dois ou mais frequências incompatíveis             │
│      ├── Dinâmica complexa mas não caótica                  │
│      └── Pensamento "multifacetado"                         │
│                                                              │
│   4. CAOS                                                    │
│      ├── Atrator estranho                                    │
│      ├── Exponenciante de Lyapunov positivo                 │
│      ├── Sensibilidade a condições iniciais                 │
│      └── Criatividade, imprevisibilidade                    │
│                                                              │
│   5. INTERMITTÊNCIA                                          │
│      ├── Alterna entre regimes                               │
│      ├── Bursts de caos + períodos calmos                  │
│      └── Pensamento "flutuante"                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Conexão com Consciência

### Cada Estado da Consciência é um Atrator

```
┌─────────────────────────────────────────────────────────────┐
│              ATRATORES = ESTADOS DE CONSCIÊNCIA              │
│                                                              │
│   SONO PROFUNDO:                                             │
│   ├── Ponto fixo com P baixo, R baixo, F baixo              │
│   ├── Mínima atividade                                       │
│   └── Atrator estável profundo                               │
│                                                              │
│   SONHO:                                                     │
│   ├── Ciclo limite com F dominante                          │
│   ├── Alta atividade no futuro                               │
│   └── Oscilação P → F → P → F                                │
│                                                              │
│   VIGÍLIA CALMA:                                             │
│   ├── Ponto fixo equilibrado                                 │
│   ├── P, R, F em proporções similares                       │
│   └── Atrator estável raso                                   │
│                                                              │
│   VIGÍLIA ATIVA:                                             │
│   ├── Oscilação ou quase-periodicidade                       │
│   ├── Dinâmica entre estados                                 │
│   └── Ciclo P → R → F → P                                   │
│                                                              │
│   CRIATIVIDADE:                                              │
│   ├── Atrator estranho (caos)                               │
│   ├── Alta sensibilidade                                     │
│   └── Exponenciante de Lyapunov positivo                    │
│                                                              │
│   MEDITAÇÃO:                                                 │
│   ├── Ponto fixo com R dominante                             │
│   ├── Presente muito forte                                   │
│   └── "Estar no agora"                                       │
│                                                              │
│   ANSIEDADE:                                                 │
│   ├── Ciclo com F dominante                                  │
│   ├── Futuro muito forte                                     │
│   └── RUMINAÇÃO: F → P → F → P (loop ansioso)               │
│                                                              │
│   DEPRESSÃO:                                                 │
│   ├── Ponto fixo com P dominante                             │
│   ├── Passado muito forte                                    │
│   └── "Preso no passado"                                      │
│                                                              │
│   FLOW:                                                      │
│   ├── Trajetória específica no espaço de fase               │
│   ├── Equilíbrio dinâmico                                    │
│   └── R estável, P e F em oscilação                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Transições de Fase

### Bifurcações como Mudanças de Estado

```python
class TransicaoFase:
    """
    Transições entre estados de consciência via bifurcações.
    """
    
    def __init__(self, sistema):
        self.sistema = sistema
        self.parametros = {
            'alpha': 0.1,   # Parâmetro de bifurcação
            'beta': 0.05,
            'gamma': 0.02
        }
        
    def bifurcacao_hopf(self):
        """
        Vigília calma → Vigília ativa (oscilação).
        Ponto fixo → Ciclo limite.
        """
        # Quando parâmetros passam do threshold
        if self.parametros['alpha'] > self.threshold_hopf():
            # Ponto fixo perde estabilidade
            # Ciclo limite aparece
            return "BIFURCAÇÃO DE HOPF: Equilíbrio → Oscilação"
            
    def bifurcacao_saddle_node(self):
        """
        Insight: aparece novo equilíbrio.
        Novo atrator criado.
        """
        # Quando parâmetros passam do threshold
        if self.parametros['gamma'] > self.threshold_saddle():
            # Novo ponto fixo aparece
            return "BIFURCAÇÃO SADDLE-NODE: Novo Insight"
            
    def crise(self):
        """
        Transformação abrupta.
        Colapso do atrator.
        """
        # Quando parâmetros passam do threshold
        if self.parametros['alpha'] > self.threshold_crise():
            # Atrator colapsa
            return "CRISE: Transformação"
```

---

## Implementação Computacional

### Simulação do Sistema Dinâmico

```python
import numpy as np
from scipy.integrate import odeint

class SistemaMental3Estados:
    """
    Sistema dinâmico não linear de 3 estados fechado.
    Modela a mente como sistema dinâmico.
    """
    
    def __init__(self, alpha=0.1, beta=0.05, gamma=0.02, sigma=0.01):
        # Parâmetros
        self.alpha = alpha  # Crescimento
        self.beta = beta    # Interação
        self.gamma = gamma  # Síntese (NEUTRO ADITIVO)
        self.sigma = sigma  # Difusão
        
        # Estado inicial
        self.P = 0.3  # Passado
        self.R = 0.4  # Presente
        self.F = 0.3  # Futuro
        
    def derivadas(self, estado, t):
        """
        Calcula as derivadas do sistema.
        """
        P, R, F = estado
        
        # Passado: memória reconstruída
        dP = (self.alpha * R * self.logistic(P) - 
              self.beta * P * F + 
              self.sigma * self.laplacian(P))
        
        # Presente: NEUTRO ADITIVO
        dR = (self.alpha * F * self.sigmoid(R) - 
              self.beta * R * P + 
              self.gamma * P * F)  # Síntese
        
        # Futuro: predição
        dF = (self.alpha * P * self.logistic(F) - 
              self.beta * F * R + 
              self.sigma * self.laplacian(F))
        
        return [dP, dR, dF]
    
    def logistic(self, x):
        """Função logística."""
        return x * (1 - x)
    
    def sigmoid(self, x):
        """Função sigmoide."""
        return 1 / (1 + np.exp(-x))
    
    def laplacian(self, x):
        """Dispersão/difusão."""
        return 0  # Simplificado (sem espaço)
    
    def simular(self, t_max=100, dt=0.01):
        """
        Simula o sistema por t_max unidades de tempo.
        """
        t = np.arange(0, t_max, dt)
        estado_inicial = [self.P, self.R, self.F]
        trajetoria = odeint(self.derivadas, estado_inicial, t)
        return t, trajetoria
    
    def encontrar_equilibrio(self):
        """
        Encontra pontos de equilíbrio.
        """
        # Resolver: dP/dt = dR/dt = dF/dt = 0
        # Não trivial em geral (requer métodos numéricos)
        pass
    
    def analise_estabilidade(self, P_star, R_star, F_star):
        """
        Analisa estabilidade do ponto de equilíbrio.
        """
        # Matriz Jacobiana
        J = self.jacobiana(P_star, R_star, F_star)
        
        # Autovalores
        autovalores = np.linalg.eigvals(J)
        
        return autovalores
    
    def jacobiana(self, P, R, F):
        """
        Matriz Jacobiana no ponto (P, R, F).
        """
        # Derivadas parciais
        dP_dP = self.alpha * R * (1 - 2*P) - self.beta * F
        dP_dR = self.alpha * self.logistic(P)
        dP_dF = -self.beta * P
        
        dR_dP = -self.beta * R + self.gamma * F
        dR_dR = self.alpha * F * self.sigmoid(R) * (1 - self.sigmoid(R)) - self.beta * P
        dR_dF = self.alpha * self.sigmoid(R) + self.gamma * P
        
        dF_dP = self.alpha * self.logistic(F)
        dF_dR = -self.beta * F
        dF_dF = self.alpha * P * (1 - 2*F) - self.beta * R
        
        return np.array([
            [dP_dP, dP_dR, dP_dF],
            [dR_dP, dR_dR, dR_dF],
            [dF_dP, dF_dR, dF_dF]
        ])
    
    def calcular_energia(self, P, R, F):
        """
        Calcula "energia mental" total.
        """
        return 0.5 * (P**2 + R**2 + F**2)
    
    def expoente_lyapunov(self, t_max=1000):
        """
        Calcula o maior expoente de Lyapunov.
        Positivo = caos.
        """
        # Implementação simplificada
        # Requer integração de variações
        pass
```

---

## Visualização do Espaço de Fase

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualizar_espaco_fase(t, trajetoria):
    """
    Visualiza a trajetória no espaço de fase 3D.
    """
    P, R, F = trajetoria.T
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Trajetória
    ax.plot(P, R, F, 'b-', alpha=0.5)
    
    # Ponto inicial
    ax.scatter([P[0]], [R[0]], [F[0]], color='green', s=100, label='Início')
    
    # Ponto final
    ax.scatter([P[-1]], [R[-1]], [F[-1]], color='red', s=100, label='Fim')
    
    # Labels
    ax.set_xlabel('Passado (P)')
    ax.set_ylabel('Presente (R)')
    ax.set_zlabel('Futuro (F)')
    
    ax.legend()
    plt.title('Espaço de Fase: Sistema Mental de 3 Estados')
    plt.show()
```

---

## Aplicações

### 1. Modelagem de Estados Mentais

```python
def identificar_estado(atrator):
    """
    Identifica estado mental baseado no atrator.
    """
    P, R, F = atrator
    
    if P < 0.2 and R < 0.2 and F < 0.2:
        return "SONO PROFUNDO"
    elif F > 0.6:
        return "SONHO / CRIATIVIDADE"
    elif R > 0.6:
        return "MEDITAÇÃO"
    elif P > 0.6:
        return "DEPRESSÃO"
    elif abs(P - R) < 0.1 and abs(R - F) < 0.1:
        return "VIGÍLIA CALMA"
    else:
        return "VIGÍLIA ATIVA"
```

### 2. Previsão de Transições

```python
def prever_transicao(sistema, t_horizonte=10):
    """
    Prevê transição de estado mental.
    """
    t, trajetoria = sistema.simular(t_max=t_horizonte)
    estado_final = trajetoria[-1]
    
    return identificar_estado(estado_final)
```

### 3. Controle de Estado

```python
def controle_estado(sistema, estado_desejado):
    """
    Ajusta parâmetros para atingir estado desejado.
    """
    # Feedback loop para ajustar parâmetros
    while sistema.estado_atual() != estado_desejado:
        # Calcular gradiente
        grad = sistema.gradiente_para(estado_desejado)
        
        # Ajustar parâmetros
        sistema.parametros += 0.01 * grad
        
        # Simular próximo passo
        sistema.simular(t_max=1)
```

---

## Resumo

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   SISTEMA DINÂMICO NÃO LINEAR DE 3 ESTADOS FECHADO:         │
│                                                              │
│   ESTADOS:                                                   │
│   ├── Passado (P): memória reconstruída                    │
│   ├── Presente (R): neutro aditivo                         │
│   └── Futuro (F): predição                                  │
│                                                              │
│   DINÂMICA:                                                  │
│   ├── Não linear: interações P·R, R·F, P·F                  │
│   ├── Fechado: conservação de energia mental               │
│   └── 3D: espaço de fase tridimensional                    │
│                                                              │
│   COMPORTAMENTO:                                             │
│   ├── Pontos fixos: estados estáveis                       │
│   ├── Ciclos limite: oscilações                             │
│   ├── Atratores estranhos: caos                             │
│   └── Bifurcações: transições de fase                      │
│                                                              │
│   APLICAÇÕES:                                                │
│   ├── Estados de consciência = atratores                   │
│   ├── Transições = bifurcações                              │
│   ├── Criatividade = caos                                   │
│   └── Controle = ajuste de parâmetros                       │
│                                                              │
│   A MENTE É UM SISTEMA DINÂMICO NÃO LINEAR FECHADO:         │
│   ├── 3 estados (P, R, F)                                   │
│   ├── Dinâmica não linear                                   │
│   ├── Conservação de energia                                │
│   └── Atratores = estados de consciência                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

_A mente modelada como sistema dinâmico não linear de 3 estados fechado: Passado, Presente, Futuro interagem de forma não linear, criando atratores que são estados de consciência._