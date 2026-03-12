# 010 - Decoder-Only Transformers: The Workhorse of Generative LLMs

**Fonte:** https://cameronrwolfe.substack.com/p/decoder-only-transformers-the-workhorse
**Autor:** Cameron R. Wolfe, Ph.D.
**Tipo:** Blog Post (Technical Deep Dive)
**Relevância:** ★★★★☆ (Arquitetura)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo Executivo

A arquitetura decoder-only transformer é a base de quase todos os LLMs modernos (GPT, LLaMA, Mistral). Quase idêntica ao GPT original, com pequenas modificações. Este artigo explica a arquitetura em detalhes, incluindo implementação completa em PyTorch.

---

## 🔍 Self-Attention Operation

### Conceito Fundamental
Self-attention transforma a representação de cada token baseado na relação com outros tokens da sequência.

### Passos
1. **Input**: Batch de sequências de tokens [B, T, d]
2. **Projections**: Criar Q, K, V via linear projections
3. **Attention Scores**: Q·K^T / √d
4. **Softmax**: Normalizar scores
5. **Output**: Attention matrix · V

### Fórmula
```
Attention(Q, K, V) = softmax(QK^T / √d) V
```

---

## 🎭 Masked (Causal) Self-Attention

### Diferença de Bidirectional
| Aspecto | Bidirectional | Masked (Causal) |
|---------|--------------|-----------------|
| **Attention** | Todos os tokens | Apenas tokens passados |
| **Uso** | BERT, encoders | GPT, decoders |
| **Mask** | Nenhuma | Triangular inferior |

### Implementação
```python
# Causal mask
mask = torch.tril(torch.ones(T, T)).view(1, 1, T, T)

# Apply mask
att = att.masked_fill(self.mask[:, :, :T, :T] == 0, float('-inf'))
```

### Por que Masked?
- Decoder-only LLMs são auto-regressivos
- Token gerado não pode olhar tokens futuros
- Previne "cheating" durante treinamento

---

## 🔀 Multi-Head Attention

### Motivação
- Softmax pode criar distribuição concentrada
- Limita foco em múltiplas posições
- Múltiplas heads = múltiplos "pontos de vista"

### Implementação
```python
# Q, K, V projections (all heads at once)
q, k, v = self.c_attn(x).split(self.d, dim=2)

# Reshape for H heads
q = q.view(B, T, self.H, self.d // self.H).transpose(1, 2)
k = k.view(B, T, self.H, self.d // self.H).transpose(1, 2)
v = v.view(B, T, self.H, self.d // self.H).transpose(1, 2)

# Compute attention
att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
att = att.masked_fill(self.mask[:,:,:T,:T] == 0, float('-inf'))
att = F.softmax(att, dim=-1)

# Weighted sum of values
y = att @ v

# Concatenate and project
y = y.transpose(1, 2).contiguous().view(B, T, self.d)
y = self.c_proj(y)
```

### Dimensões
- **Input/Output**: d (embedding dimension)
- **Heads**: H
- **Per-head dimension**: d // H
- **Attention matrix**: [B, H, T, T]

---

## 🧱 Decoder-Only Transformer Block

### Estrutura
```
Input
  ↓
[LayerNorm] ← Pre-norm (LLaMA style)
  ↓
[Masked Multi-Head Attention]
  ↓
[Residual Connection]
  ↓
[LayerNorm]
  ↓
[Feed-Forward Network]
  ↓
[Residual Connection]
  ↓
Output
```

### Componentes
1. **LayerNorm**: Normaliza ativações (estabilidade)
2. **Masked Multi-Head Attention**: Causal self-attention
3. **Feed-Forward Network**: FFN(x) = max(0, xW₁ + b₁)W₂ + b₂
4. **Residual Connection**: x + sublayer(x)

---

## 📊 Layer Normalization

### Motivação
Redes profundas sofrem de:
- Vanishing/exploding gradients
- Ativações instáveis

### Fórmula
```
LayerNorm(x) = γ * (x - μ) / σ + β
```

### Benefícios
- Gradientes mais estáveis
- Treino mais rápido
- Permite redes mais profundas

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Causal Mask** | Impede olhar tokens futuros |
| **Multi-Head** | Múltiplas atenções em paralelo |
| **Pre-norm vs Post-norm** | Ordem do LayerNorm |
| **Residual Connection** | x + sublayer(x) |
| **FFN** | Feed-forward network após attention |
| **Context Window** | Tamanho máximo T da sequência |

---

## 🔗 Evoluções Recentes

### LLaMA vs GPT Original
| Aspecto | GPT | LLaMA |
|---------|-----|-------|
| **Norm** | Post-norm | Pre-norm |
| **Activation** | GeLU | SwiGLU |
| **Position** | Learned | RoPE |
| **Norm Type** | LayerNorm | RMSNorm |

### RMSNorm (LLaMA)
```
RMSNorm(x) = x * (1/rms(x)) * γ
rms(x) = sqrt(1/n * Σ xᵢ²)
```
- Mais simples que LayerNorm
- Sem cálculo de média
- Eficiente e funciona bem

---

## 📝 Notas Pessoais

### Por que Decoder-Only Dominou?
1. **Simplicidade**: Uma stack vs encoder-decoder
2. **Generative por natureza**: Perfeito para LM
3. **Scaling**: Funciona bem em escala
4. **Transfer learning**: Pre-train + fine-tune

### Implementação Eficiente
- KV Cache para inferência
- Flash Attention para treino
- Fused kernels para performance

### Próximos Passos
- Flash Attention 2/3
- Sliding Window Attention (Mistral)
- Grouped-Query Attention (LLaMA 2)

---

## 🎯 Resumo do Tópico LLM & Transformers

Este tópico cobriu os fundamentos essenciais da arquitetura Transformer aplicada a LLMs:

### Fontes Lidas (10/37)
1. ✅ The Illustrated Transformer (fundacional)
2. ✅ Attention Is All You Need (paper original)
3. ✅ A Comprehensive Overview of LLMs (survey)
4. ✅ The Illustrated GPT-2 (decoder-only)
5. ✅ Rotary Embeddings / RoPE (positional encoding moderno)
6. ✅ MoE LLMs (sparse activation)
7. ✅ PEFT Fine-Tuning (LoRA, adapters)
8. ✅ Efficient Inference Survey (quantização, KV cache)
9. ✅ BPE Tokenization (tokenização)
10. ✅ Decoder-Only Transformers (arquitetura)

### Conceitos Dominados
- Self-attention e multi-head attention
- Causal/masked attention para LLMs
- RoPE vs positional embeddings absolutos
- Mixture of Experts para escala
- PEFT (LoRA) para fine-tuning eficiente
- Quantização para inferência
- BPE tokenization
- Decoder-only architecture

---

## 🎯 Próximo Passo

Continuar lendo mais fontes da bibliografia ou mover para próximo tópico "MLOps Pipelines & Automation".