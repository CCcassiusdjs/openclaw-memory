# LLMs From Scratch - Sebastian Raschka

**Source ID:** 011
**Type:** Book + GitHub Repository
**Author:** Sebastian Raschka
**URL:** https://github.com/rasbt/LLMs-from-scratch
**Book:** Build A Large Language Model (From Scratch) - Manning 2024
**ISBN:** 978-1633437166
**Read Date:** 2026-03-12

---

## 📖 Summary

This is the official code repository for Sebastian Raschka's comprehensive book "Build A Large Language Model (From Scratch)". The repository provides step-by-step implementation of a GPT-like LLM in PyTorch, covering everything from tokenization to instruction finetuning.

### Core Value Proposition
- Implement LLMs from scratch in PyTorch (no external LLM libraries)
- Mirror the approach used in large-scale foundational models like ChatGPT
- Educational focus: small-but-functional models for learning
- Includes code for loading pretrained weights for finetuning

---

## 🏗️ Book Structure

### Chapter Organization

| Chapter | Title | Main Code | Key Topics |
|---------|-------|-----------|------------|
| 1 | Understanding LLMs | No code | LLM landscape overview |
| 2 | Working with Text Data | `ch02.ipynb` | Tokenization, dataloaders |
| 3 | Coding Attention Mechanisms | `ch03.ipynb` | Self-attention, multi-head |
| 4 | Implementing GPT Model | `ch04.ipynb` | GPT architecture, KV cache |
| 5 | Pretraining | `ch05.ipynb` | Training loop, generation |
| 6 | Finetuning for Classification | `ch06.ipynb` | Classification head |
| 7 | Instruction Finetuning | `ch07.ipynb` | Instruction tuning, DPO |

### Appendix Materials
- **Appendix A:** Introduction to PyTorch
- **Appendix B:** References and Further Reading
- **Appendix C:** Exercise Solutions
- **Appendix D:** Training Loop Enhancements
- **Appendix E:** Parameter-efficient Finetuning with LoRA

---

## 🔑 Key Concepts Learned

### 1. LLM Mental Model
The book follows a clear progression:
1. Text Data Preparation (tokenization, embeddings)
2. Attention Mechanisms (self-attention, multi-head)
3. GPT Architecture (decoder-only transformer)
4. Pretraining (next-token prediction)
5. Finetuning (classification, instruction following)

### 2. Architecture Components Covered

#### Core Components
- **Tokenization:** BPE implementation from scratch
- **Embeddings:** Token + positional embeddings
- **Attention:** Self-attention, multi-head attention, causal masking
- **Transformer Block:** Attention + FFN + LayerNorm + Residual
- **GPT Model:** Stack of transformer blocks + output head

#### Advanced Topics (Bonus Material)
- **KV Cache:** Memory optimization for inference
- **Grouped-Query Attention (GQA):** Efficient attention variant
- **Multi-Head Latent Attention (MLA):** DeepSeek's attention
- **Sliding Window Attention:** Long context handling
- **Mixture-of-Experts (MoE):** Sparse activation for scaling

### 3. Implementation Patterns

```python
# Mental model from the book
LLM = [
    Tokenization (BPE),
    Embedding Layer,
    N × TransformerBlock(
        MultiHeadAttention + LayerNorm + Residual,
        FeedForward + LayerNorm + Residual
    ),
    Output Layer
]
```

### 4. Training Pipeline
1. **Data preparation:** Text → tokens → dataloader
2. **Model:** GPT architecture initialization
3. **Pretraining:** Next-token prediction loss
4. **Generation:** Autoregressive sampling
5. **Finetuning:** Classification or instruction following

---

## 📚 Bonus Materials

### BPE Tokenization
- `bpe-from-scratch-simple.ipynb` - Minimal BPE implementation
- Comparing various BPE implementations

### Attention Variants
- Efficient multi-head attention implementations
- KV cache implementation
- Grouped-Query Attention (GQA)
- Multi-Head Latent Attention (MLA)
- Sliding Window Attention
- Gated DeltaNet

### Model Architectures from Scratch
- **Llama 3.2:** `standalone-llama32.ipynb`
- **Qwen3:** Dense and MoE variants
- **Gemma 3:** Latest architecture
- **Olmo 3:** Open model implementation
- **Tiny Aya:** Compact model
- **Qwen3.5:** Updated variant

### Training Enhancements
- Alternative weight loading methods
- Learning rate schedulers
- Hyperparameter optimization
- Memory-efficient weight loading
- Performance tips for faster training

### Finetuning Techniques
- Classification finetuning
- Instruction finetuning
- DPO (Direct Preference Optimization)
- LoRA (Low-Rank Adaptation)

---

## 🎯 Practical Applications

### What You Can Build
1. **Custom LLM from scratch** - Educational small model
2. **Finetuned classifier** - Text classification with pretrained weights
3. **Instruction-tuned model** - ChatGPT-like assistant
4. **DPO-aligned model** - Preference-optimized responses

### Code Organization
- Main notebooks: `chXX/01_main-chapter-code/`
- Bonus materials: `chXX/02_bonus_...`
- Exercise solutions: `exercise-solutions.ipynb`
- Summary scripts: `gpt.py`, `gpt_train.py`, `gpt_generate.py`

---

## 🔬 Deep Insights

### Why This Approach Matters
1. **Transparency:** Every component is visible and understandable
2. **Educational:** Learn by doing, not by using black boxes
3. **Transferable:** Concepts apply to any LLM framework
4. **Practical:** Can finetune real models after understanding

### Key Takeaways
- GPT architecture nearly unchanged since 2018
- Tokenization is critical for performance
- Attention is the core innovation of transformers
- Pretraining + finetuning is the dominant paradigm
- KV cache essential for efficient inference

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Chapters | 7 main + 5 appendices |
| Main Notebooks | 7 |
| Bonus Notebooks | 30+ |
| Exercise Solutions | Per chapter |
| Video Course | 17h 15m companion |
| Model Implementations | Llama, Qwen, Gemma, Olmo |

---

## 🔗 Related Resources

### Sequel Book
- **Build A Reasoning Model (From Scratch)** - Focuses on reasoning capabilities
- Implements inference-time scaling, RL, distillation
- GitHub: `rasbt/reasoning-from-scratch`

### Companion Materials
- PyTorch in One Hour book (prerequisite)
- Test Yourself PDF (170 pages, quiz questions)
- Manning Forum for discussion

---

## 📝 Notes

- **Prerequisites:** Python programming, basic PyTorch helpful
- **Hardware:** Runs on conventional laptops, auto-uses GPU
- **No external LLM libraries:** Pure PyTorch implementation
- **Exercises:** Solutions provided in Appendix C
- **Active maintenance:** Regular updates on GitHub

---

## 🎓 Concepts to Explore Further

1. **KV Cache Implementation** - Memory optimization for inference
2. **Grouped-Query Attention** - Efficient attention for modern LLMs
3. **Direct Preference Optimization** - Alignment without RLHF
4. **LoRA Implementation** - Parameter-efficient finetuning
5. **Llama Architecture Differences** - How it differs from GPT

---

**Relevância:** ★★★★★ (Foundational Resource)
**Status:** `completed`
**Reading Time:** Full book ~40 hours, Repository ~4 hours exploration