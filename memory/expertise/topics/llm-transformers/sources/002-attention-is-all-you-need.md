# 002 - Attention Is All You Need (Paper Original)

**Fonte:** https://arxiv.org/abs/1706.03762
**Autores:** Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (Google Brain/Research)
**Ano:** 2017
**Tipo:** Paper Acadêmico
**Relevância:** ★★★★★ (Fundacional)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo Executivo

Paper seminal que introduziu a arquitetura Transformer. Propõe um modelo baseado exclusivamente em mecanismos de attention, eliminando recurrence e convolutions. Alcançou state-of-the-art em tradução automática (WMT 2014) com tempo de treinamento significativamente menor.

---

## 🎯 Contribuições Principais

### 1. Arquitetura Transformer
- **Encoder-Decoder** baseado em self-attention
- **Sem RNNs ou CNNs** - elimina necessidade de recorrência
- **Paralelização** massiva possível
- **Path length constante** entre quaisquer duas posições

### 2. Scaled Dot-Product Attention
```
Attention(Q, K, V) = softmax(QK^T / √dk) V
```
- Escalar por √dk estabiliza gradients para dk grande
- Mais eficiente que additive attention

### 3. Multi-Head Attention
```
MultiHead(Q,K,V) = Concat(head₁,...,headₕ)W^O
onde headᵢ = Attention(QWᵢ^Q, KWᵢ^K, VWᵢ^V)
```
- **h=8 heads** no modelo base
- **dk=dv=dmodel/h=64** por head
- Permite attending a informações de diferentes subespaços

---

## 🏗️ Arquitetura Detalhada

### Encoder Stack
- **N=6 layers** idênticas
- Cada layer tem 2 sub-layers:
  1. Multi-head self-attention
  2. Feed-forward network (posição-wise)
- Residual connection + LayerNorm em cada sub-layer
- **dmodel = 512**

### Decoder Stack
- **N=6 layers** idênticas
- Cada layer tem 3 sub-layers:
  1. **Masked** multi-head self-attention (impede olhar o futuro)
  2. Encoder-decoder attention (queries do decoder, K/V do encoder)
  3. Feed-forward network (posição-wise)
- Residual connection + LayerNorm em cada sub-layer

### Position-wise Feed-Forward Network
```
FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
```
- **dff = 2048** (inner-layer dimension)
- Aplicado independentemente em cada posição

### Positional Encoding
```
PE(pos,2i) = sin(pos / 10000^(2i/dmodel))
PE(pos,2i+1) = cos(pos / 10000^(2i/dmodel))
```
- Sinusoids de diferentes frequências
- Permite extrapolação para sequências mais longas
- Alternativa: learned positional embeddings (resultados similares)

---

## 📊 Comparação com RNNs e CNNs

| Camada | Complexidade/Sequência | Operações Sequenciais | Path Length |
|--------|------------------------|----------------------|-------------|
| **Self-Attention** | O(n²·d) | O(1) | O(1) |
| **Recurrent** | O(n·d²) | O(n) | O(n) |
| **Convolutional** | O(k·n·d²) ou O(n·d²) | O(1) | O(logₖ(n)) |

**Vantagens do Transformer:**
- Paralelização total (O(1) sequential ops)
- Path length constante entre qualquer par de posições
- Self-attention mais interpretável

---

## 🏋️ Training Setup

### Dados
- **WMT 2014 English-German**: ~4.5M sentence pairs
- **WMT 2014 English-French**: ~36M sentence pairs
- **Byte-pair encoding**: 37000 tokens (EN-DE), 32000 tokens (EN-FR)

### Hardware & Tempo
- **8 NVIDIA P100 GPUs**
- **Base model**: 100K steps, 12 horas
- **Big model**: 300K steps, 3.5 dias

### Optimizer
- **Adam**: β₁=0.9, β₂=0.98, ε=10⁻⁹
- **Learning rate**:
  ```
  lrate = dmodel^(-0.5) · min(step_num^(-0.5), step_num · warmup_steps^(-1.5))
  ```
- **warmup_steps = 4000**

### Regularization
- **Residual Dropout**: Pdrop = 0.1 (base), 0.3 (big)
- **Label Smoothing**: εls = 0.1

---

## 📈 Resultados

### WMT 2014 English-to-German
| Modelo | BLEU | Training Time |
|--------|------|---------------|
| **Transformer (big)** | **28.4** | 3.5 dias |
| Transformer (base) | 25.8 | 12 horas |
| Previous SOTA | ~26.0 | ~4 dias |

### WMT 2014 English-to-French
| Modelo | BLEU | Training Time |
|--------|------|---------------|
| **Transformer (big)** | **41.8** | 3.5 dias |
| Previous SOTA | ~41.0 | ~14 dias |

### Model Variations (Ablation)
- **Heads**: 8 é ótimo, menos = pior, muito mais = diminishing returns
- **dk**: Diminuir hurts quality - compatibilidade não é trivial
- **Model size**: Bigger is better
- **Dropout**: Crucial para evitar overfitting
- **Positional encoding**: Sinusoids vs learned = similar results

---

## 💡 Conceitos-Chave do Paper

| Conceito | Descrição |
|----------|-----------|
| **Self-Attention** | Atende a própria sequência - relaciona todas as posições |
| **Scaled Dot-Product** | Dot product escalado por √dk para estabilidade |
| **Multi-Head** | Múltiplas atenções em paralelo para diferentes subespaços |
| **Positional Encoding** | Sinusoids para injetar informação posicional |
| **Residual + LayerNorm** | Estabiliza treino em redes profundas |
| **Masked Attention** | Decoder não pode olhar posições futuras |

---

## 🔬 Ablation Studies

### Effect of Number of Heads (Table 3, row A)
| Heads | dk | BLEU |
|-------|----|------|
| 1 | 512 | 24.9 |
| 4 | 128 | 25.5 |
| **8** | **64** | **25.8** |
| 16 | 32 | 25.8 |
| 32 | 16 | 25.4 |

**Conclusão**: Single-head é 0.9 BLEU pior, mas muitos heads não ajuda mais.

### Effect of Model Size (Table 3, rows C, D)
- Bigger models = better
- Dropout é crucial (0.1 vs 0.0 → 1.1 BLEU difference)

---

## 🎯 English Constituency Parsing

- Transformer generaliza bem para outras tarefas
- 4-layer transformer, dmodel=1024
- **WSJ only**: 91.3 F1 (better than BerkeleyParser)
- **Semi-supervised**: 92.7 F1

---

## 📝 Notas Pessoais

### Por que Transformer Revolucionou?
1. **Paralelização**: Elimina sequential bottleneck de RNNs
2. **Long-range dependencies**: Path length O(1), não O(n) como RNNs
3. **Interpretability**: Attention weights são mais interpretáveis

### Limitações Originais
- **O(n²) complexity** no comprimento da sequência
- Memória cresce quadraticamente com sequência
- Não resolve problemas de very long sequences

### Evoluções Posteriores (não neste paper)
- **Sparse Attention**: Reduz complexidade
- **Linear Attention**: O(n) complexity
- **RoPE**: Positional encoding relativo
- **Flash Attention**: Memory-efficient implementation

---

## 🔗 Conexões com Trabalhos Posteriores

- **GPT**: Decoder-only Transformer
- **BERT**: Encoder-only Transformer (masked LM)
- **T5**: Encoder-decoder Transformer
- **Vision Transformer (ViT)**: Transformer para imagens
- **RoPE**: Evolução do positional encoding

---

## 🎯 Próxima Fonte

Ler **"A Comprehensive Overview of Large Language Models"** (survey) para visão geral de LLMs modernos.