# 005 - Rotary Embeddings: A Relative Revolution (RoPE)

**Fonte:** https://blog.eleuther.ai/rotary-embeddings/
**Autor:** EleutherAI (Biderman, Black, Foster, Gao, et al.)
**Tipo:** Blog Post (Technical Explanation)
**Relevância:** ★★★★★ (RoPE Essencial)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo Executivo

Rotary Positional Embedding (RoPE) é um método de codificação posicional que unifica abordagens absolutas e relativas. Desenvolvido por Jianlin Su, tornou-se o padrão em LLMs modernos (LLaMA, GPT-NeoX, Mistral). Funciona tanto para attention vanilla quanto para variantes eficientes (Performer, etc.).

---

## 🎯 O Problema das Posições

### Limitações dos Métodos Existentes

| Método | Vantagem | Limitação |
|--------|----------|-----------|
| **Absolute Learned** | Simples | Não generaliza para sequências longas |
| **Sinusoidal** | Sem parâmetros | Aditivo, não captura bem relações |
| **T5 Relative Bias** | Funciona bem | Requer matriz N×N, não funciona com attention eficiente |

### O Desafio
- Dot products **não preservam** posição absoluta
- Dot products **preservam** posição relativa
- Precisamos codificar posição absoluta de forma que seja **relativamente preservada**

---

## 💡 A Solução: RoPE

### Intuição Geométrica
- Dot product: **q · k = |q| |k| cos(θqk)**
- RoPE: representa embeddings como **números complexos**
- Posições são **rotações puras** aplicadas aos embeddings
- Rotação preserva **ângulo relativo** entre vetores

### Propriedade Fundamental
Se rotacionamos tanto q quanto k pelo mesmo ângulo adicional:
- **Posição absoluta muda**
- **Posição relativa preservada**
- **Ângulo entre vetores inalterado**
- **Dot product inalterado**

### Fórmula Matemática
```
RoPE(x, m) = x · e^(imθ)

⟨RoPE(q_j, m), RoPE(k_j, n)⟩ = q_j k_j e^(i(m-n)θ) = RoPE(q_j k_j, m-n)
```

**Resultado:** O inner product depende apenas da **diferença de posição** (m - n)!

---

## 🧮 Derivação Completa

### Objetivo
Encontrar f(x, ℓ) tal que:
```
⟨f(q, m), f(k, n)⟩ = g(q, k, m - n)
```

### Condições Iniciais
- f(x, 0) = x (posição zero = embedding original)
- R_f independe de m (magnitude preservada)
- Θ_f(x, m) = Θ(x) + mθ (fase = fase original + rotação posicional)

### Solução Final
```
f(q, m) = Σ q_j e^(imθ_j) eⱼ
```

### Forma Matricial (Implementação)
```
f(q, m) = Θ_m · Q_m = Θ_m · W_q · X_m
```

Onde Θ_m é matriz de rotação:
```
M_j = [cos(mθ_j)  -sin(mθ_j)]
      [sin(mθ_j)   cos(mθ_j)]
```

---

## 🔄 Comparação com Sinusoidal

| Aspecto | Sinusoidal (Original) | RoPE |
|---------|----------------------|------|
| **Operação** | Aditiva | Multiplicativa |
| **Coordenadas** | Individual | Pares (complexos) |
| **Posição** | Absoluta | Relativa (via rotação) |
| **Generalização** | Limitada | Melhor para sequências longas |
| **Eficiência** | Aplicada uma vez | Aplicada por camada |

---

## ⚙️ Implementação

### PyTorch (GPT-NeoX)
```python
class Rotary(torch.nn.Module):
    def __init__(self, dim, base=10000):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)
    
    def forward(self, x, seq_dim=1):
        seq_len = x.shape[seq_dim]
        t = torch.arange(seq_len, device=x.device).type_as(self.inv_freq)
        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        return emb.cos(), emb.sin()

def rotate_half(x):
    x1, x2 = x[..., :x.shape[-1]//2], x[..., x.shape[-1]//2:]
    return torch.cat((-x2, x1), dim=-1)

def apply_rotary_pos_emb(q, k, cos, sin):
    return (q * cos) + (rotate_half(q) * sin), \
           (k * cos) + (rotate_half(k) * sin)
```

### Complexidade Computacional
- **Overhead**: 4-5x vs positional embeddings aditivos (sem otimização)
- **Com otimização (fusing)**: 2-2.5x vs aditivos
- **Overhead total no modelo**: 1-3% (matriz multiplications dominam)

---

## 📊 Resultados Experimentais

### GPT-NeoX 125M (OpenWebText2)
| Método | Val Loss | Perplexity |
|--------|----------|------------|
| Learned Absolute | 2.809 | 16.59 |
| T5 RPE | 2.801 | 16.46 |
| **RoPE** | **2.759** | **15.78** |

**Melhoria:** ~2% em loss vs T5 RPE, ~3% vs learned absolute

### Mesh Transformer JAX 1.4B (Pile)
| Método | Val Loss | Perplexity |
|--------|----------|------------|
| Learned Absolute | 2.240 | 9.393 |
| T5 RPE | 2.223 | 9.234 |
| **RoPE** | **2.173** | **8.784** |

**Melhoria:** ~2% em loss, escala para bilhões de parâmetros

### Performer (Efficient Attention)
- RoPE funciona com attention eficiente (Performer, Linear Attention)
- T5 RPE **não funciona** (requer matriz N×N)
- Melhoria significativa em convergência

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Rotação Complexa** | Embeddings tratados como números complexos |
| **Ângulo Relativo** | Posição codificada como rotação preserva diferença |
| **Matriz de Rotação** | Aplicada por bloco (pares de dimensões) |
| **Per-Layer Application** | RoPE aplicado em cada camada, não apenas input |
| **Base Frequency** | θ_j = 1/(base^(2j/d)), base=10000 típico |

---

## 🔗 Extensões e Variantes

### Multi-dimensional RoPE
- Divide embeddings em múltiplos grupos
- Cada grupo com frequência independente
- Útil para dados multidimensionais (imagens, música)

### Implementações
- **GPT-NeoX**: Primeiro modelo grande-scale com RoPE
- **LLaMA**: Usa RoPE por padrão
- **Mistral**: Usa RoPE
- **x-transformers**: Biblioteca lucidrains

---

## 📝 Notas Pessoais

- RoPE é agora o padrão de fato para LLMs modernos
- Substitui tanto positional embeddings absolutos quanto T5 RPE
- Funciona com attention eficiente (grande vantagem)
- Overhead computacional mínimo
- Extensível para múltiplas dimensões

### Por que RoPE Funciona?
1. **Preserva magnitude**: Rotação não altera |q| ou |k|
2. **Preserva diferença**: Ângulo relativo inalterado por shift absoluto
3. **Primeiros princípios**: Derivado matematicamente, não empírico

### Quando Usar RoPE?
- ✅ Sempre para modelos auto-regressivos
- ✅ Attention eficiente (Performer, Linear Attention)
- ✅ Sequências longas (melhor generalização)
- ✅ Multi-dimensional data (variantes)

---

## 🎯 Próxima Fonte

Ler **"A Survey on Mixture of Experts in LLMs"** para entender sparse activation em LLMs.