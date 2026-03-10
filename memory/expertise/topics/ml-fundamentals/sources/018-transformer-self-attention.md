# Transformer Architecture and Self-Attention (Deep Dive)

**Source:** Jay Alammar (Illustrated Transformer), Vaswani et al. (2017), Harvard NLP
**Category:** Deep Learning Architectures
**Priority:** Fundamental
**Read:** 2026-03-10

## Core Concept

**Transformers** are neural network architectures that use **self-attention** to process sequential data without recurrence, enabling parallel processing and capturing long-range dependencies.

### Key Innovation

Unlike RNNs that process sequences step-by-step:
- **Transformers process entire sequences at once**
- **Self-attention allows each position to attend to all other positions**
- **No recurrence → parallelizable → faster training**

## Architecture Overview

### High-Level Structure

```
Input → [Encoder Stack] → [Decoder Stack] → Output

Encoder Stack: 6 identical encoders
Decoder Stack: 6 identical decoders
```

### Encoder Structure

Each encoder has two sub-layers:
1. **Multi-head self-attention**
2. **Feed-forward neural network**

Plus:
- Residual connections around each sub-layer
- Layer normalization after each sub-layer

### Decoder Structure

Each decoder has three sub-layers:
1. **Masked multi-head self-attention** (can only attend to earlier positions)
2. **Encoder-decoder attention** (attends to encoder output)
3. **Feed-forward neural network**

## Self-Attention Mechanism

### Intuition

When processing a word, self-attention allows the model to:
- Look at other words in the sentence
- Determine which words are relevant
- Incorporate their information into the current word's representation

**Example:** "The animal didn't cross the street because **it** was too tired"
- "it" should attend to "animal" (what was tired?)
- Not "street" (streets don't get tired)

### Calculation Steps

For each word, create three vectors:
- **Query (Q):** What am I looking for?
- **Key (K):** What do I contain?
- **Value (V):** What information do I provide?

**Step-by-step:**

1. **Create Q, K, V:**
   ```
   Q = X @ W_Q
   K = X @ W_K
   V = X @ W_V
   ```
   Where X is the input embedding, W_Q/W_K/W_V are learned matrices.

2. **Compute attention scores:**
   ```
   scores = Q @ K^T
   ```
   Dot product of query with all keys.

3. **Scale scores:**
   ```
   scores = scores / √d_k
   ```
   Where d_k is the key dimension (typically 64).

4. **Apply softmax:**
   ```
   attention_weights = softmax(scores)
   ```
   Normalizes scores to probabilities.

5. **Compute weighted values:**
   ```
   output = attention_weights @ V
   ```
   Weighted combination of values.

**Compact formula:**
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

## Multi-Head Attention

### Why Multiple Heads?

Single attention head may focus on one type of relationship:
- Multiple heads can capture different relationships
- Each head learns different Q/K/V projections

### How It Works

1. **Split into multiple heads:**
   - 8 heads in original Transformer
   - Each head has dimension d_k = d_model / 8 = 64

2. **Apply attention in parallel:**
   ```
   head_i = Attention(Q_i, K_i, V_i)
   ```

3. **Concatenate and project:**
   ```
   MultiHead(Q, K, V) = Concat(head_1, ..., head_h) @ W_O
   ```

### Visualization

Different heads attend to different relationships:
- Head 1: Subject-verb relationships
- Head 2: Object relationships
- Head 3: Adjective-noun relationships
- etc.

## Positional Encoding

### Why Needed?

Self-attention has no notion of position:
- Permutation invariant
- Needs explicit position information

### Sinusoidal Encoding

```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Where:
- pos = position in sequence
- i = dimension index

**Properties:**
- Unique for each position
- Deterministic (no learned parameters)
- Can extrapolate to longer sequences

### Alternative: Learned Positional Embeddings

Learn position embeddings like word embeddings:
- Fixed vocabulary of positions
- Cannot extrapolate to longer sequences

## Feed-Forward Networks

Each encoder/decoder has feed-forward layer:

```
FFN(x) = max(0, xW_1 + b_1)W_2 + b_2
```

- Applied to each position independently
- Same weights across positions
- Two linear transformations with ReLU activation
- Dimension typically: d_model → 2048 → d_model

## Residual Connections & Layer Norm

### Residual Connection

```
output = LayerNorm(x + Sublayer(x))
```

**Benefits:**
- Gradient flow through skip connections
- Enables training very deep networks

### Layer Normalization

```
LayerNorm(x) = (x - μ) / σ × γ + β
```

Normalizes across features (not batch):
- μ = mean across features
- σ = std across features
- γ, β = learned parameters

## Decoder Details

### Masked Self-Attention

In decoder self-attention:
- Cannot attend to future positions
- Set future positions to -∞ before softmax

**Why?** During training, decoder should not "see" the future.

### Encoder-Decoder Attention

- **Queries:** From decoder
- **Keys, Values:** From encoder output

Allows decoder to focus on relevant parts of input sequence.

## Training

### Objective

**Cross-entropy loss:**
```
L = -Σ log P(y_t | y_{<t}, x)
```

### Teacher Forcing

During training:
- Input: Ground truth tokens shifted right
- Output: Predict next token

### Inference

During inference:
- **Autoregressive:** Generate one token at a time
- Each generated token becomes input for next step

## Key Innovations

| Innovation | Benefit |
|------------|---------|
| **Self-attention** | Capture long-range dependencies |
| **Multi-head** | Multiple representation subspaces |
| **Positional encoding** | Position awareness without recurrence |
| **Parallel processing** | Faster training than RNNs |
| **Residual connections** | Train very deep networks |

## Modern Variants

| Model | Year | Innovation |
|-------|------|------------|
| Transformer | 2017 | Original self-attention |
| BERT | 2018 | Bidirectional encoder |
| GPT | 2018 | Autoregressive decoder |
| T5 | 2020 | Text-to-text framework |
| ViT | 2020 | Vision transformer |
| LLaMA | 2023 | Efficient scaling |

## Key Takeaways

1. **Self-attention is the core** - Each position attends to all others
2. **Q, K, V abstraction** - Query what you want, Key what you offer, Value what you provide
3. **Multi-head captures different relationships** - 8 heads = 8 different "views"
4. **Positional encoding adds position** - Sinusoidal or learned
5. **Parallel processing** - No recurrence, fast training
6. **Residual connections** - Enable deep networks
7. **Layer normalization** - Stabilizes training

## References

- Vaswani et al. (2017): "Attention Is All You Need"
- Devlin et al. (2019): "BERT: Pre-training of Deep Bidirectional Transformers"
- Radford et al. (2018): "Improving Language Understanding by Generative Pre-Training"
- Dosovitskiy et al. (2021): "An Image is Worth 16x16 Words: Transformers for Image Recognition"