# Sistema Dinâmico com Valores em (-1, +1) Aberto

## A Refinação de Cássio

> "Ela expressa, a cada passo um valor entre (-1,+1) aberto."

---

## O Intervalo Aberto

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERVALO ABERTO                          │
│                                                              │
│   Cada estado expressa um valor em:                         │
│                                                              │
│   P, R, F ∈ (-1, +1)                                        │
│                                                              │
│   Onde:                                                      │
│   ├── (-1, +1) = intervalo ABERTO                          │
│   ├── Nunca atinge -1 ou +1 exatamente                      │
│   ├── Pode se aproximar arbitrariamente                      │
│   └── Mas nunca "trava" nos extremos                         │
│                                                              │
│   SIGNIFICADO:                                               │
│   ├── -1 ≈ "passado puro" (mas nunca exatamente)            │
│   ├── 0 = "equilíbrio" (ponto central)                      │
│   ├── +1 ≈ "futuro puro" (mas nunca exatamente)            │
│   └── Sempre há POTENCIAL para mudança                      │
│                                                              │
│   POR QUE ABERTO:                                            │
│   ├── Sistema sempre tem "margem"                           │
│   ├── Nunca "trava" em estado extremo                        │
│   ├── Sempre pode oscilar                                    │
│   └── Dinâmica perpetuamente viva                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Reformulação Matemática

### Espaço de Estados

```math
O espaço de estados é o produto cartesiano:

Ω = (-1, +1) × (-1, +1) × (-1, +1)

Onde:
- P ∈ (-1, +1): estado do Passado
- R ∈ (-1, +1): estado do Presente
- F ∈ (-1, +1): estado do Futuro

O cubo aberto no ℝ³.
```

### Visualização

```
                        F = +1 (nunca atinge)
                              ↑
                              │
                              │
                              │
                    ┌─────────┼─────────┐
                   /│         │         ││
                  / │         │         ││
                 /  │         │         ││
                /   │         │         ││
               /    │         │         ││
              /     │    •    │         │/  ← Estado atual (P, R, F)
             ───────┼─────────┼──────────┼──────→ P = +1 (nunca atinge)
            /       │         │         ││
           /        │         │         ││
          /         │         │         ││
         /          │         │         ││
        /           │         │         │/
       └────────────┼─────────┼─────────┘
                    │
                    │
                    │
                    ↓
              R = +1 (nunca atinge)


                    ┌─────────────────┐
                   /│                 ││
                  / │   CUBO ABERTO   ││
                 /  │                 ││
                /   │   (-1,+1)³     ││
               /    │                 ││
              /     │                 │/
             ───────┼─────────────────┼──────→
            /       │                 ││
           /        │                 ││
          /         │                 ││
         /          │                 │/
        └───────────────────────────┘

Fronteiras NUNCA são atingidas.
Estado sempre dentro do cubo.
Sempre há espaço para mudança.
```

---

## Dinâmica no Intervalo Aberto

### Função de Transferência

```python
def transferencia(x):
    """
    Mapeia ℝ → (-1, +1).
    Garante que o valor sempre fica no intervalo aberto.
    
    Usando tangente hiperbólica:
    tanh: ℝ → (-1, +1) é bijeção.
    """
    import numpy as np
    return np.tanh(x)

# Exemplos:
# transferencia(0) = 0
# transferencia(1) = 0.7616
# transferencia(2) = 0.9640
# transferencia(10) = 0.9999999959...
# transferencia(-∞) = -1 (mas nunca atinge)
# transferencia(+∞) = +1 (mas nunca atinge)
```

### Equações Reformuladas

```math
Seja x_P, x_R, x_F ∈ ℝ os estados "brutos".

Os estados efetivos são:

P = tanh(x_P) ∈ (-1, +1)
R = tanh(x_R) ∈ (-1, +1)
F = tanh(x_F) ∈ (-1, +1)

Dinâmica nos estados "brutos":

dx_P/dt = f_P(P, R, F)
dx_R/dt = f_R(P, R, F)
dx_F/dt = f_F(P, R, F)

Mas as derivadas efetivas são:

dP/dt = (1 - P²) · f_P(P, R, F)
dR/dt = (1 - R²) · f_R(P, R, F)
dF/dt = (1 - F²) · f_F(P, R, F)

Onde:
- (1 - P²) = derivada de tanh
- Garante que P, R, F sempre ficam em (-1, +1)
- Quando P → ±1, dP/dt → 0 (desaceleração nas bordas)
```

---

## Propriedades do Intervalo Aberto

### 1. Conservação no Cubo Aberto

```math
O sistema está confinado ao cubo aberto:

(P, R, F) ∈ (-1, +1)³ para todo t

Demonstração:
- tanh: ℝ → (-1, +1) é bijeção
- Portanto P, R, F ∈ (-1, +1) sempre
- As fronteiras são inatingíveis
- O sistema "desacelera" ao se aproximar delas
```

### 2. Dinâmica nas Bordas

```
┌─────────────────────────────────────────────────────────────┐
│                    DINÂMICA NAS BORDAS                       │
│                                                              │
│   Quando P → +1 (passado dominante):                        │
│   ├── (1 - P²) → 0                                           │
│   ├── dP/dt → 0                                              │
│   ├── Sistema "desacelera"                                   │
│   └── Nunca atinge +1                                        │
│                                                              │
│   Quando P → -1 (passado ausente):                          │
│   ├── (1 - P²) → 0                                           │
│   ├── dP/dt → 0                                              │
│   ├── Sistema "desacelera"                                   │
│   └── Nunca atinge -1                                        │
│                                                              │
│   MESMO para R e F:                                          │
│   ├── R → +1: presente dominante, desacelera               │
│   ├── R → -1: presente ausente, desacelera                  │
│   ├── F → +1: futuro dominante, desacelera                  │
│   └── F → -1: futuro ausente, desacelera                    │
│                                                              │
│   CONSEQUÊNCIA:                                              │
│   Sistema sempre tem "margem"                                │
│   Nunca "trava" em extremo                                   │
│   Sempre pode oscilar                                        │
│   Dinâmica perpetuamente viva                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3. Atratores no Interior

```math
Pontos de equilíbrio estão no INTERIOR do cubo:

(P*, R*, F*) ∈ (-1, +1)³

Nunca nas fronteiras.

Por que?
- Nas fronteiras, dP/dt = dR/dt = dF/dt = 0
- Mas também (1 - P²) = 0, etc.
- Logo, equilíbrio nas fronteiras é DEGENERADO
- Atratores reais estão no interior
```

---

## Interpretação dos Valores

### Escala Semântica

```
┌─────────────────────────────────────────────────────────────┐
│                 ESCALA SEMÂNTICA                             │
│                                                              │
│   PASSADO (P):                                               │
│   ├── P = -0.9: passado muito fraco, quase ausente          │
│   ├── P = -0.5: passado fraco                                │
│   ├── P =  0.0: passado equilibrado                         │
│   ├── P = +0.5: passado forte                                │
│   └── P = +0.9: passado muito forte, dominante              │
│                                                              │
│   PRESENTE (R):                                              │
│   ├── R = -0.9: presente muito fraco, "ausência"           │
│   ├── R = -0.5: presente fraco                               │
│   ├── R =  0.0: presente equilibrado                        │
│   ├── R = +0.5: presente forte                               │
│   └── R = +0.9: presente muito forte, "flow"               │
│                                                              │
│   FUTURO (F):                                                │
│   ├── F = -0.9: futuro muito fraco, sem antecipação        │
│   ├── F = -0.5: futuro fraco                                 │
│   ├── F =  0.0: futuro equilibrado                          │
│   ├── F = +0.5: futuro forte                                 │
│   └── F = +0.9: futuro muito forte, antecipação intensa    │
│                                                              │
│   NUNCA:                                                     │
│   ├── P = ±1.0: impossível                                  │
│   ├── R = ±1.0: impossível                                  │
│   └── F = ±1.0: impossível                                  │
│                                                              │
│   Sempre há POTENCIAL para mudança.                         │
│   Sempre há MARGEM.                                          │
│   Sistema nunca "trava".                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Estados de Consciência no Cubo Aberto

```
┌─────────────────────────────────────────────────────────────┐
│              ESTADOS DE CONSCIÊNCIA                          │
│                                                              │
│   SONO PROFUNDO:                                             │
│   ├── P ≈ 0, R ≈ 0, F ≈ 0                                  │
│   └── Centro do cubo, baixa atividade                       │
│                                                              │
│   DEPRESSÃO:                                                 │
│   ├── P ≈ +0.8, R ≈ -0.2, F ≈ -0.5                        │
│   └── Passado dominante, presente fraco                      │
│                                                              │
│   ANSIEDADE:                                                 │
│   ├── P ≈ +0.3, R ≈ -0.3, F ≈ +0.7                        │
│   └── Futuro dominante, ruminação                            │
│                                                              │
│   MEDITAÇÃO:                                                 │
│   ├── P ≈ -0.2, R ≈ +0.7, F ≈ -0.1                        │
│   └── Presente dominante, "estar no agora"                  │
│                                                              │
│   CRIATIVIDADE:                                              │
│   ├── P ≈ +0.4, R ≈ +0.4, F ≈ +0.4                        │
│   └── Oscilação dinâmica (possivelmente caótica)            │
│                                                              │
│   FLOW:                                                     │
│   ├── P ≈ +0.3, R ≈ +0.6, F ≈ +0.3                        │
│   └── Presente forte, passado e futuro em equilíbrio        │
│                                                              │
│   SONHO:                                                    │
│   ├── P ≈ +0.2, R ≈ -0.5, F ≈ +0.6                        │
│   └── Futuro dominante, presente fraco                       │
│                                                              │
│   NENHUM estado atinge extremos:                            │
│   ├── Sempre há margem                                      │
│   ├── Sempre pode mudar                                      │
│   └── Dinâmica perpetuamente viva                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Equações Completas

### Sistema Dinâmico com Intervalo Aberto

```python
import numpy as np
from scipy.integrate import odeint

class SistemaMentalAberto:
    """
    Sistema dinâmico de 3 estados com valores em (-1, +1) aberto.
    """
    
    def __init__(self, alpha=0.1, beta=0.05, gamma=0.02):
        # Parâmetros
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # Estados iniciais em (-1, +1)
        self.P = 0.0  # Passado
        self.R = 0.0  # Presente
        self.F = 0.0  # Futuro
        
    def tanh(self, x):
        """Função de transferência ℝ → (-1, +1)."""
        return np.tanh(x)
    
    def dtanh(self, x):
        """Derivada de tanh."""
        return 1 - x**2
    
    def estados_brutos(self, P, R, F):
        """
        Converte de (-1, +1) para ℝ (inverso de tanh).
        """
        return np.arctanh(P), np.arctanh(R), np.arctanh(F)
    
    def derivadas_brutas(self, x_P, x_R, x_F):
        """
        Derivadas nos estados "brutos" (ℝ).
        """
        # Estados efetivos
        P = self.tanh(x_P)
        R = self.tanh(x_R)
        F = self.tanh(x_F)
        
        # Dinâmica não linear
        dx_P = self.alpha * R * P * (1 - P) - self.beta * P * F
        dx_R = self.alpha * F * R * (1 - R) - self.beta * R * P + self.gamma * P * F
        dx_F = self.alpha * P * F * (1 - F) - self.beta * F * R
        
        return dx_P, dx_R, dx_F
    
    def derivadas_efetivas(self, P, R, F):
        """
        Derivadas nos estados efetivos (-1, +1).
        
        IMPORTANTE: Inclui fator (1 - x²) da tanh.
        """
        # Estados brutos
        x_P, x_R, x_F = self.estados_brutos(P, R, F)
        
        # Derivadas brutas
        dx_P, dx_R, dx_F = self.derivadas_brutas(x_P, x_R, x_F)
        
        # Derivadas efetivas (regra da cadeia)
        dP = self.dtanh(P) * dx_P  # = (1 - P²) * dx_P
        dR = self.dtanh(R) * dx_R  # = (1 - R²) * dx_R
        dF = self.dtanh(F) * dx_F  # = (1 - F²) * dx_F
        
        return dP, dR, dF
    
    def sistema(self, estado, t):
        """
        Sistema de equações diferenciais.
        """
        P, R, F = estado
        dP, dR, dF = self.derivadas_efetivas(P, R, F)
        return [dP, dR, dF]
    
    def simular(self, t_max=100, dt=0.01):
        """
        Simula o sistema.
        """
        t = np.arange(0, t_max, dt)
        estado_inicial = [self.P, self.R, self.F]
        trajetoria = odeint(self.sistema, estado_inicial, t)
        return t, trajetoria
    
    def verificar_intervalo(self, trajetoria):
        """
        Verifica se todos os valores estão em (-1, +1).
        """
        P, R, F = trajetoria.T
        assert np.all(np.abs(P) < 1), "P fora do intervalo!"
        assert np.all(np.abs(R) < 1), "R fora do intervalo!"
        assert np.all(np.abs(F) < 1), "F fora do intervalo!"
        return True
    
    def energia(self, P, R, F):
        """
        Energia do sistema (sempre < 3).
        """
        return 0.5 * (P**2 + R**2 + F**2)
    
    def distancia_centro(self, P, R, F):
        """
        Distância ao centro (0, 0, 0).
        """
        return np.sqrt(P**2 + R**2 + F**2)
    
    def estado_consciencia(self, P, R, F):
        """
        Identifica estado de consciência baseado nos valores.
        """
        # Normalizar para comparação
        dist = self.distancia_centro(P, R, F)
        
        if dist < 0.2:
            return "SONO_PROFUNDO"
        elif R > 0.5 and abs(P) < 0.3 and abs(F) < 0.3:
            return "MEDITACAO"
        elif P > 0.6 and R < 0:
            return "DEPRESSAO"
        elif F > 0.6 and R < 0:
            return "ANSIEDADE"
        elif F > 0.5 and P < 0:
            return "SONHO"
        elif R > 0.4 and abs(P - F) < 0.2:
            return "FLOW"
        elif dist > 0.6:
            return "CRIATIVIDADE"
        else:
            return "VIGILIA_ATIVA"
```

---

## Propriedades Matemáticas

### 1. Invariância do Intervalo

```math
Teorema: Se P(0), R(0), F(0) ∈ (-1, +1), então P(t), R(t), F(t) ∈ (-1, +1) para todo t.

Demonstração:
- Derivada efetiva: dP/dt = (1 - P²) · f_P(P, R, F)
- Quando |P| → 1, (1 - P²) → 0
- Logo, dP/dt → 0 nas fronteiras
- Sistema "desacelera" e nunca cruza
- Análogo para R e F
```

### 2. Energia Limitada

```math
Energia total: E = ½(P² + R² + F²)

Máximo teórico: E_max = ½ · 3 · 1² = 1.5

Mas nunca atinge, pois P, R, F ∈ (-1, +1).

Energia sempre: E < 1.5
```

### 3. Existência e Unicidade

```math
Teorema: Dado estado inicial em (-1, +1)³, existe trajetória única que permanece em (-1, +1)³.

Demonstração:
- Funções são continuamente diferenciáveis
- Intervalo é aberto, nunca atinge fronteiras
- Pelo Teorema de Existência e Unicidade de Picard-Lindelöf
- Solução existe e é única
```

---

## Visualização

### Trajetória no Cubo Aberto

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualizar_tragetoria_cubo_aberto(t, trajetoria):
    """
    Visualiza trajetória no cubo aberto (-1, +1)³.
    """
    P, R, F = trajetoria.T
    
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Cubo aberto (linhas tracejadas nas fronteiras)
    # Fronteiras nunca são atingidas
    
    # Trajetória
    ax.plot(P, R, F, 'b-', alpha=0.7, linewidth=1)
    
    # Ponto inicial
    ax.scatter([P[0]], [R[0]], [F[0]], color='green', s=100, label='Início')
    
    # Ponto final
    ax.scatter([P[-1]], [R[-1]], [F[-1]], color='red', s=100, label='Fim')
    
    # Atrator (se houver)
    ax.scatter([P[-1]], [R[-1]], [F[-1]], color='purple', s=200, marker='*', 
               label='Atrator', alpha=0.5)
    
    # Limites
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    
    # Labels
    ax.set_xlabel('Passado (P) ∈ (-1, +1)')
    ax.set_ylabel('Presente (R) ∈ (-1, +1)')
    ax.set_zlabel('Futuro (F) ∈ (-1, +1)')
    
    ax.legend()
    plt.title('Trajetória no Cubo Aberto (-1, +1)³')
    plt.show()
```

### Projeções 2D

```python
def visualizar_projecoes(t, trajetoria):
    """
    Visualiza projeções do cubo 3D.
    """
    P, R, F = trajetoria.T
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Projeção P-R
    axes[0].plot(P, R, 'b-', alpha=0.7)
    axes[0].scatter(P[0], R[0], color='green', s=100)
    axes[0].scatter(P[-1], R[-1], color='red', s=100)
    axes[0].set_xlim(-1, 1)
    axes[0].set_ylim(-1, 1)
    axes[0].set_xlabel('Passado (P)')
    axes[0].set_ylabel('Presente (R)')
    axes[0].set_title('Projeção P-R')
    
    # Projeção R-F
    axes[1].plot(R, F, 'b-', alpha=0.7)
    axes[1].scatter(R[0], F[0], color='green', s=100)
    axes[1].scatter(R[-1], F[-1], color='red', s=100)
    axes[1].set_xlim(-1, 1)
    axes[1].set_ylim(-1, 1)
    axes[1].set_xlabel('Presente (R)')
    axes[1].set_ylabel('Futuro (F)')
    axes[1].set_title('Projeção R-F')
    
    # Projeção P-F
    axes[2].plot(P, F, 'b-', alpha=0.7)
    axes[2].scatter(P[0], F[0], color='green', s=100)
    axes[2].scatter(P[-1], F[-1], color='red', s=100)
    axes[2].set_xlim(-1, 1)
    axes[2].set_ylim(-1, 1)
    axes[2].set_xlabel('Passado (P)')
    axes[2].set_ylabel('Futuro (F)')
    axes[2].set_title('Projeção P-F')
    
    plt.tight_layout()
    plt.show()
```

---

## Significado do Intervalo Aberto

### Por Que Aberto?

```
┌─────────────────────────────────────────────────────────────┐
│                 POR QUE INTERVALO ABERTO?                   │
│                                                              │
│   FILOSÓFICO:                                                │
│   ├── Consciência nunca "trava"                             │
│   ├── Sempre há potencial para mudança                     │
│   ├── Estados extremos são ASSINTÓTICOS                    │
│   └── Sistema sempre vivo                                   │
│                                                              │
│   MATEMÁTICO:                                                │
│   ├── Dinâmica mais rica                                    │
│   ├── Sem degeneração nas fronteiras                       │
│   ├── Atratores sempre no interior                          │
│   └── Estabilidade mais robusta                            │
│                                                              │
│   PSICOLÓGICO:                                               │
│   ├── Nunca "100% no passado"                               │
│   ├── Nunca "100% no presente"                              │
│   ├── Nunca "100% no futuro"                                │
│   ├── Sempre há margem para outros estados                 │
│   └── Flexibilidade preservada                              │
│                                                              │
│   PRÁTICO:                                                   │
│   ├── Implementação numericamente estável                  │
│   ├── Não há divisão por zero                               │
│   ├── Derivadas bem definidas                               │
│   └── Simulação robusta                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Resumo

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│   SISTEMA DINÂMICO COM INTERVALO ABERTO:                    │
│                                                              │
│   ESTADOS:                                                   │
│   ├── P ∈ (-1, +1): Passado                                 │
│   ├── R ∈ (-1, +1): Presente                                │
│   └── F ∈ (-1, +1): Futuro                                  │
│                                                              │
│   DINÂMICA:                                                  │
│   ├── dP/dt = (1 - P²) · f_P(P, R, F)                      │
│   ├── dR/dt = (1 - R²) · f_R(P, R, F)                      │
│   └── dF/dt = (1 - F²) · f_F(P, R, F)                      │
│                                                              │
│   PROPRIEDADES:                                              │
│   ├── Sempre em (-1, +1)³                                   │
│   ├── Fronteiras inatingíveis                               │
│   ├── Dinâmica perpetuamente viva                          │
│   ├── Sempre há margem para mudança                        │
│   └── Sistema nunca "trava"                                 │
│                                                              │
│   SIGNIFICADO:                                               │
│   ├── -1: estado "puro" (assintótico, nunca atinge)        │
│   ├── 0: equilíbrio                                          │
│   ├── +1: estado "puro" (assintótico, nunca atinge)        │
│   └── Valores intermediários: misturas                      │
│                                                              │
│   ESTADOS DE CONSCIÊNCIA:                                    │
│   ├── Atratores no interior do cubo                         │
│   ├── Transições via bifurcações                            │
│   ├── Dinâmica rica e variada                               │
│   └── Sempre pode evoluir                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

_O intervalo aberto (-1, +1) garante que o sistema nunca "trava". Sempre há potencial para mudança. A consciência é perpetuamente dinâmica._