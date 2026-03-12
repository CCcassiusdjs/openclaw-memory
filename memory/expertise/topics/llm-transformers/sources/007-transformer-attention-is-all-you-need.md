# Attention Is All You Need - Transformer Original Paper

**Fonte:** https://arxiv.org/abs/1706.03762
**Autores:** Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
**Ano:** 2017 (Google Brain)
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

**Paper fundador da era Transformer**. Propõe arquitetura baseada exclusivamente em attention, eliminando recurrence e convolutions. Alcance SOTA em tradução automática com tempo de treinamento significativamente menor.

---

## 🎯 Contribuições Principais

### Arquitetura Novadora
- **Sem recurrence**: Elimina RNNs/LSTMs
- **Sem convolution**: Elimina CNNs
- **Apenas attention**: Self-attention como mecanismo central

### Benefícios
1. **Paralelização**: Treinamento muito mais rápido
2. **Long-range dependencies**: Conexões diretas entre todas posições
3. **Performance**: SOTA em WMT 2014

---

## 📊 Resultados

### WMT 2014 English-to-German
- **28.4 BLEU** (novo SOTA)
- +2 BLEU sobre modelos anteriores

### WMT 2014 English-to-French
- **41.8 BLEU** (novo SOTA)
- Treinado em 3.5 dias em 8 GPUs

---

## 🏗️ Arquitetura do Transformer

### Encoder (6 camadas)
1. **Multi-head self-attention**
2. **Position-wise feed-forward**
3. **Residual connections + LayerNorm**

### Decoder (6 camadas)
1. **Masked multi-head self-attention**
2. **Multi-head encoder-decoder attention**
3. **Position-wise feed-forward**
4. **Residual connections + LayerNorm**

---

## 🔑 Self-Attention Detalhado

### Fórmula
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

### Por que scaled?
- Dividir por √d_k previne gradientes extremos
- Softmax mais estável

### Multi-Head Attention
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

**Configuração paper**: 8 heads, d_k = d_v = 64

---

## 📍 Positional Encoding

### Por que necessário?
- Self-attention não tem noção de ordem
- Precisa injetar informação posicional

### Fórmula Sinusoidal
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

### Vantagens
- Extrapola para sequências mais longas
- Determinístico, não aprendido

---

## 📈 Complexidade Computacional

| Layer Type | Complexity | Sequential Ops | Max Path Length |
|------------|------------|----------------|-----------------|
| Self-Attention | O(n²·d) | O(1) | O(1) |
| Recurrent | O(n·d²) | O(n) | O(n) |
| Convolutional | O(k·n·d²) | O(1) | O(log_k(n)) |

**Insight**: Self-attention é O(1) em sequential operations!

---

## 💡 Conceitos-Chave

### 1. Scaled Dot-Product Attention
- Escalar previne saturação do softmax
- Permite gradientes saudáveis

### 2. Multi-Head Attention
- Múltiplas "representações" do input
- Cada head foca em diferentes relações

### 3. Position-wise Feed-Forward
- MLP aplicado independentemente em cada posição
- Duas transformações lineares + ReLU

### 4. Residual Connections
- Cada sub-layer tem residual + layer norm
- `output = LayerNorm(x + Sublayer(x))`

---

## 🔬 Variações Testadas

### Base Model
- d_model = 512
- 6 encoder/decoder layers
- 8 attention heads
- ~65M parâmetros

### Big Model
- d_model = 1024
- 6 layers
- 16 heads
- ~213M parâmetros

---

## 📚 Impacto

### NLP
- BERT, GPT, T5, etc. todos baseados em Transformer
- SOTA em praticamente todas tarefas de NLP

### Beyond NLP
- Vision Transformer (ViT)
- Speech Transformers
- Graph Transformers
- Reinforcement Learning

### Arquiteturas Derivadas
- **Encoder-only**: BERT, RoBERTa
- **Decoder-only**: GPT, LLaMA
- **Encoder-decoder**: T5, BART

---

## 🎓 Lessons Learned

1. **Attention é suficiente**: Não precisamos de recurrence
2. **Paralelização importa**: Treinamento muito mais rápido
3. **Scale bem**: Funciona de 65M a 175B+ parâmetros
4. **Generaliza**: Aplicável além de NMT

---

## 🔗 Próximos Passos

- [ ] Estudar variantes (Longformer, Reformer, Linformer)
- [ ] Entender Flash Attention (otimização moderna)
- [ ] Analisar scaling laws para Transformers

---

## 📝 Tags

`#transformer` `#attention` `#landmark-paper` `#vaswani` `#google` `#2017` `#foundation`