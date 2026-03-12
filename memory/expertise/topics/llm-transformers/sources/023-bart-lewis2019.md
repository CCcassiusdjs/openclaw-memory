# BART: Denoising Sequence-to-Sequence Pre-training

**Source ID:** 023
**Type:** Research Paper (ArXiv)
**Authors:** Mike Lewis, Yinhan Liu, Naman Goyal, et al. (Facebook AI)
**URL:** https://arxiv.org/abs/1910.13461
**Published:** 2019
**Read Date:** 2026-03-12

---

## 📖 Summary

BART (Bidirectional and Auto-Regressive Transformers) is a denoising autoencoder for pre-training sequence-to-sequence models. It combines the bidirectional encoder from BERT with the autoregressive decoder from GPT, generalizing both architectures.

### Core Contribution
- **Combines BERT + GPT:** Encoder-decoder architecture
- **Denoising pre-training:** Corrupt text, learn to reconstruct
- **Generalizes previous models:** Special cases include BERT and GPT
- **Strong for generation:** Summarization, translation, dialogue

---

## 🔑 Key Concepts Learned

### 1. Architecture

```
Input → [BERT-like Encoder] → Representations → [GPT-like Decoder] → Output

Encoder: Bidirectional attention (like BERT)
Decoder: Autoregressive with cross-attention (like GPT)
```

| Component | Architecture | Key Feature |
|-----------|-------------|------------|
| Encoder | 6-12 layers | Bidirectional self-attention |
| Decoder | 6-12 layers | Autoregressive + cross-attention |
| Embeddings | Shared | Token + positional embeddings |

### 2. Pre-training Objective: Denoising

**Corruption methods:**
1. **Token masking:** Replace tokens with [MASK]
2. **Token deletion:** Remove tokens entirely
3. **Text infilling:** Insert [MASK] spans of varying length
4. **Sentence permutation:** Shuffle sentences
5. **Document rotation:** Rotate document at random position

**Best performing approach:**
- Sentence permutation + text infilling
- Reconstruct original text from corrupted input

### 3. Comparison with Other Models

| Model | Architecture | Pre-training | Generation |
|-------|--------------|--------------|------------|
| BERT | Encoder-only | Masked LM | Poor |
| GPT | Decoder-only | Next token | Good |
| BART | Encoder-Decoder | Denoising | Excellent |

---

## 📊 Performance Results

### Summarization

| Dataset | BART | Previous SOTA |
|---------|------|---------------|
| CNN/DailyMail | 44.2 ROUGE | +6 points |
| XSum | 45.1 ROUGE | +6 points |
| SAMSum | 53.0 ROUGE | +5 points |

### Question Answering

| Dataset | BART | Previous SOTA |
|---------|------|---------------|
| SQuAD | Comparable | - |
| CoQA | Improved | +2 points |

### Machine Translation

| Task | BART | Improvement |
|------|------|-------------|
| En→Ro | +1.1 BLEU | Back-translation baseline |

---

## 🔬 Key Insights

### 1. Why Encoder-Decoder for Generation

- **Encoder:** Bidirectional understanding of input
- **Decoder:** Autoregressive generation of output
- **Cross-attention:** Decoder attends to encoder representations

### 2. Denoising vs Masked LM

| Objective | Input | Target |
|-----------|-------|--------|
| MLM (BERT) | [MASK] token | Original token |
| Denoising (BART) | Corrupted text | Original text |

Denoising is more flexible and can handle various corruptions.

### 3. Generalization Property

BART can be viewed as generalizing:
- **BERT:** Encoder-only (remove decoder)
- **GPT:** Decoder-only (remove encoder)
- **Transformer:** Encoder-decoder (original architecture)

---

## 🎓 Practical Applications

### Sequence-to-Sequence Tasks

1. **Summarization:** Text → Summary
2. **Translation:** Source → Target language
3. **Question answering:** Context + Question → Answer
4. **Dialogue:** History → Response
5. **Data-to-text:** Structured data → Natural language

### Fine-tuning Process

```python
# Load pre-trained BART
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

# Fine-tune on task
for batch in dataloader:
    outputs = model(
        input_ids=batch.input_ids,
        labels=batch.target_ids
    )
    loss = outputs.loss
    loss.backward()
    optimizer.step()
```

---

## 📈 Follow-up Models

| Model | Year | Innovation |
|-------|------|------------|
| mBART | 2020 | Multilingual BART |
| BART-Large | 2019 | Larger variant |
| PEGASUS | 2020 | Gap sentence generation |

---

## 📝 Key Takeaways

1. **Combines BERT + GPT strengths** - Understanding + Generation
2. **Denoising is effective** - Learn to reconstruct
3. **Flexible architecture** - Can replace encoder or decoder
4. **Strong for generation tasks** - SOTA on summarization
5. **Encoder-decoder pattern** - Standard for seq2seq

---

## 🔗 Related Concepts

- **Sequence-to-sequence models** - Encoder-decoder architecture
- **Denoising autoencoders** - Pre-training objective
- **Transfer learning for generation** - Pre-train, fine-tune
- **Cross-attention** - Decoder attends to encoder

---

**Relevância:** ★★★★★ (Key Architecture - Encoder-Decoder LLMs)
**Status:** `completed`
**Reading Time:** Paper ~15 pages, Core concepts ~25 minutes