# Attention Mechanisms and Transformers - D2L Chapter

**Fonte:** http://d2l.ai/chapter_attention-mechanisms-and-transformers/index.html
**Autor:** Dive into Deep Learning
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Capítulo abrangente do D2L sobre mecanismos de atenção e Transformers. Cobrem a evolução histórica desde RNNs até Transformers, explicando o fundamento teórico e implementação prática.

---

## 🏗️ Evolução de Arquiteturas

### Antes dos Transformers
- **MLP**: Perceptrons multicamadas (anos 2010)
- **CNNs**: Redes convolucionais para visão
- **RNNs/LSTMs**: Redes recorrentes para sequências
- Inovações metodológicas: ReLU, residual layers, batch normalization, dropout

### A Mudança de Paradigma
- Transformers emergiram como arquitetura dominante para NLP
- Depois estenderam para visão (ViT), speech, RL, grafos
- Pre-training + fine-tuning tornou-se padrão

---

## 🔑 Conceitos Fundamentais

### Mecanismo de Atenção
**Ideia Central**: Em vez de comprimir todo input em vetor fixo, permitir que decoder revise o input em cada passo.

**Intuição Bahdanau (2014)**:
1. Encoder produz representação de comprimento = input original
2. Decoder recebe contexto como soma ponderada das representações
3. Pesos determinam "foco" em diferentes tokens
4. Processo é diferenciável → aprendido junto com outros parâmetros

**Benefícios**:
- Melhor performance que encoder-decoder clássico
- Interpretabilidade parcial (pesos mostram alinhamento)

### Queries, Keys, Values

**Framework conceitual**:
- **Query (Q)**: O que estou procurando
- **Key (K)**: O que cada entrada oferece
- **Value (V)**: O conteúdo real de cada entrada

**Operação**:
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

### Self-Attention

**Diferença de attention clássico**:
- Q, K, V vêm do mesmo bloco
- Cada token "pergunta" sobre todos os outros tokens
- Permite capturar dependências de longa distância

---

## 📊 Comparação: CNNs vs RNNs vs Self-Attention

| Critério | CNN | RNN | Self-Attention |
|----------|-----|-----|----------------|
| Complexidade O(·) | O(k²n) | O(n²d) | O(n²d) |
| Path length | O(n/k) | O(n) | O(1) |
| Long-range dependencies | Limitado | Limitado | **Direto** |
| Parallelization | Parcial | Sequencial | **Total** |

---

## 🏛️ Arquitetura Transformer

### Componentes Principais
1. **Multi-Head Attention**: Múltiplas atenções em paralelo
2. **Positional Encoding**: Sinusoidal ou aprendido
3. **Feed-Forward Networks**: MLPs por posição
4. **Layer Normalization**: Estabiliza treinamento
5. **Residual Connections**: Facilita backpropagation

### Encoder-Only (BERT-style)
- Bidirecional
- Masked Language Modeling
- Ideal para: classification, NER, extraction

### Decoder-Only (GPT-style)
- Unidirecional (causal)
- Autoregressive
- Ideal para: generation, completion

### Encoder-Decoder (T5-style)
- Encoder bidirecional + Decoder causal
- Ideal para: translation, summarization

---

## 🔧 Detalhes Técnicos

### Scaled Dot-Product Attention
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```
- Divisão por √d_k evita gradientes extremos
- Softmax garante pesos normalizados

### Multi-Head Attention
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```
- Múltiplas "visões" do mesmo input
- Projeções lineares diferentes para cada head

### Positional Encoding
**Sinusoidal**:
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```
- Permite extrapolação para sequências mais longas
- Cada dimensão captura diferentes frequências

---

## 📈 Pre-training com Transformers

### Foundation Models
- Pre-train em corpora massivos
- Fine-tune para tarefas específicas
- BERT, GPT, T5 são exemplos

### Scalability
- Leis de scaling: performance ∝ compute, data, params
- Chinchilla: modelos ótimos têm params ≈ tokens/20
- Emergent abilities em escalas grandes

---

## 💡 Insights Principais

1. **Self-attention é O(n²)** → Custo quadrático com comprimento
2. **Posições não são nativas** → Precisam de encoding explícito
3. **Multi-head é crítico** → Captura diferentes tipos de relacionamentos
4. **Pre-training domina** → Quase todos SOTA usam pre-training
5. **Vision Transformer** → Patches como tokens, same architecture

---

## 🔗 Próximos Passos

- [ ] Ler detalhes de cada seção do D2L
- [ ] Implementar transformer from scratch
- [ ] Estudar variantes (Longformer, Reformer, etc.)

---

## 📚 Referências Citadas

1. Bahdanau et al. (2014) - Attention original
2. Vaswani et al. (2017) - Transformer original
3. Devlin et al. (2018) - BERT
4. Brown et al. (2020) - GPT-3
5. Dosovitskiy et al. (2021) - Vision Transformer

---

## 📝 Tags

`#transformer` `#attention` `#d2l` `#survey` `#architecture` `#deep-learning`