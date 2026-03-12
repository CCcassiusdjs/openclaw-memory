# Language Models are Few-Shot Learners (GPT-3 Paper)

**Source ID:** 016
**Type:** Research Paper (ArXiv)
**Authors:** Tom B. Brown, Benjamin Mann, Nick Ryder, et al. (OpenAI)
**URL:** https://arxiv.org/abs/2005.14165
**Published:** 2020
**Read Date:** 2026-03-12

---

## 📖 Summary

This landmark paper introduced GPT-3, a 175 billion parameter autoregressive language model that demonstrated that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes reaching competitiveness with prior state-of-the-art fine-tuning approaches.

### Core Contribution
- **Scale matters:** 175B parameters (10x larger than any previous non-sparse LM)
- **Few-shot learning:** Tasks specified purely via text interaction, no gradient updates
- **In-context learning:** Model learns tasks from examples in the prompt

---

## 🔑 Key Concepts Learned

### 1. Scaling Hypothesis
The paper validates that increasing model scale dramatically improves:
- Task-agnostic performance
- Few-shot learning capabilities
- Generalization to unseen tasks

### 2. Few-Shot Learning Paradigm
| Approach | Examples | Gradient Updates |
|----------|----------|------------------|
| Zero-shot | 0 | No |
| One-shot | 1 | No |
| Few-shot | 10-100 | No |
| Fine-tuning | Thousands | Yes |

GPT-3 achieves strong performance without any gradient updates.

### 3. In-Context Learning
- Model uses attention mechanism to reference examples in prompt
- No weight updates needed
- Task specification through text interaction only

---

## 📊 Model Details

| Model Variant | Parameters | Layers | d_model | Attention Heads |
|---------------|------------|--------|---------|------------------|
| GPT-3 Small | 125M | 12 | 768 | 12 |
| GPT-3 Medium | 350M | 24 | 1024 | 16 |
| GPT-3 Large | 760M | 24 | 1536 | 16 |
| GPT-3 XL | 1.3B | 24 | 2048 | 32 |
| GPT-3 2.7B | 2.7B | 32 | 2560 | 32 |
| GPT-3 6.7B | 6.7B | 32 | 4096 | 32 |
| GPT-3 13B | 13B | 40 | 5140 | 40 |
| **GPT-3 175B** | **175B** | **96** | **12288** | **96** |

---

## 🎯 Task Performance

### Strong Performance On
- Translation (BLEU scores competitive with supervised systems)
- Question-answering
- Cloze tasks
- On-the-fly reasoning (3-digit arithmetic, novel words)
- News article generation (human evaluators struggle to distinguish)

### Identified Limitations
- Some datasets where few-shot learning still struggles
- Methodological issues with training on web corpora
- Weakness in certain reasoning tasks
- Contamination concerns

---

## 🔬 Key Insights

### Why GPT-3 Matters
1. **Demonstrated scaling laws:** Performance continues improving with scale
2. **Meta-learning:** Model learns to learn from examples in context
3. **Zero task-specific fine-tuning:** Everything via text interaction
4. **Broader impacts:** Human-level text generation raises societal concerns

### Architecture Notes
- Same architecture as GPT-2 (decoder-only transformer)
- Pre-training on massive dataset (WebText-derived)
- No architectural innovations, just scale

---

## 📈 Scaling Laws Observations

The paper validates earlier scaling laws research:
- Performance improves predictably with model size
- Larger models need less data for same performance
- Few-shot capability emerges primarily at scale

---

## 🔗 Related Works

- **GPT-2** - Previous OpenAI model (1.5B parameters)
- **Scaling Laws** - Kaplan et al. 2020
- **BERT** - Encoder-only alternative
- **T5** - Encoder-decoder approach

---

**Relevância:** ★★★★★ (Foundational LLM Paper)
**Status:** `completed`
**Reading Time:** Paper ~40 pages, Abstract review ~10 minutes