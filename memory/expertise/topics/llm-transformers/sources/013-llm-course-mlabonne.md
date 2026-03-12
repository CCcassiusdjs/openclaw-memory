# LLM Course - Maxime Labonne

**Source ID:** 013
**Type:** Course + GitHub Repository
**Author:** Maxime Labonne
**URL:** https://github.com/mlabonne/llm-course
**Read Date:** 2026-03-12

---

## 📖 Summary

Comprehensive course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks. Divided into three parts: LLM Fundamentals, LLM Scientist, and LLM Engineer.

### Core Value Proposition
- **🧩 LLM Fundamentals** - Optional foundations (math, Python, neural networks)
- **🧑🔬 LLM Scientist** - Building the best possible LLMs
- **👷 LLM Engineer** - Creating LLM-based applications and deployment

---

## 🏗️ Course Structure

### Part 1: LLM Fundamentals (Optional)

#### Mathematics
- **Linear Algebra:** Vectors, matrices, determinants, eigenvalues, linear transformations
- **Calculus:** Derivatives, integrals, gradients, multivariable calculus
- **Probability & Statistics:** Distributions, hypothesis testing, MLE, Bayesian inference

#### Python
- Python basics, data types, OOP
- Data science libraries (NumPy, Pandas, Matplotlib, Seaborn)
- Machine learning (Scikit-learn, PCA, t-SNE)

#### Neural Networks
- Structure: layers, weights, biases, activations
- Training: backpropagation, loss functions, optimizers
- Regularization: dropout, L1/L2, early stopping, data augmentation

#### NLP Basics
- Text preprocessing: tokenization, stemming, lemmatization
- Feature extraction: BoW, TF-IDF, n-grams
- Word embeddings: Word2Vec, GloVe, FastText
- Sequence models: RNNs, LSTMs, GRUs

### Part 2: LLM Scientist (Building LLMs)

#### 1. The LLM Architecture
- **Evolution:** Encoder-decoder Transformers → decoder-only (GPT)
- **Tokenization:** Converting text to numbers (BPE, WordPiece)
- **Attention mechanisms:** Self-attention, multi-head attention
- **Sampling techniques:** Greedy, beam search, temperature, nucleus sampling

#### 2. Pre-training
- **Data preparation:** Massive datasets (Llama 3: 15T tokens)
  - Curation, cleaning, deduplication, filtering
- **Distributed training:**
  - Data parallel (batch distribution)
  - Pipeline parallel (layer distribution)
  - Tensor parallel (operation splitting)
- **Training optimization:**
  - Adaptive learning rates with warm-up
  - Gradient clipping
  - Mixed-precision training
  - Modern optimizers (AdamW, Lion)
- **Monitoring:** Loss, gradients, GPU stats, profiling

#### 3. Post-training Data
- **Formats:** ShareGPT, OpenAI/HF formats
- **Chat templates:** ChatML, Alpaca
- **Synthetic data generation:** Using frontier models (GPT-4o)
- **Data enhancement:**
  - Verified outputs (unit tests, solvers)
  - Rejection sampling
  - Auto-Evol, Chain-of-Thought
  - Branch-Solve-Merge, personas
- **Quality filtering:**
  - Rule-based filtering
  - Deduplication (MinHash, embeddings)
  - N-gram decontamination
  - Reward models, judge LLMs

#### 4. Supervised Fine-Tuning (SFT)
- **Training techniques:**
  - Full fine-tuning (all parameters)
  - LoRA (Low-Rank Adaptation)
  - QLoRA (4-bit quantization + LoRA)
- **Frameworks:** TRL, Unsloth, Axolotl
- **Key parameters:**
  - Learning rate + schedulers
  - Batch size, gradient accumulation
  - Epochs, optimizer (8-bit AdamW)
  - LoRA: rank (16-128), alpha (1-2x rank)
- **Distributed training:** DeepSpeed, FSDP
- **Monitoring:** Loss curves, gradient norms

#### 5. Preference Alignment
- **RLHF (Reinforcement Learning from Human Feedback):**
  - Train reward model from preferences
  - Optimize with PPO
- **DPO (Direct Preference Optimization):**
  - Simpler alternative to RLHF
  - No reward model needed
- **Other methods:**
  - ORPO (Odds Ratio Preference Optimization)
  - KTO (Kahneman-Tversky Optimization)
  - IPO (Identity Preference Optimization)

#### 6. Evaluation
- **General benchmarks:** MMLU, MMLU-Pro, GPQA, BBH
- **Chat benchmarks:** MT-Bench, AlpacaEval, Open LLM Leaderboard
- **Math & coding:** GSM8K, MATH, HumanEval, MBPP
- **Agentic benchmarks:** AgentBench, SWE-bench
- **Techniques:**
  - Few-shot prompting
  - Chain-of-Thought prompting
  - LLM-as-a-Judge

### Part 3: LLM Engineer (Applications)

#### 1. Running LLMs
- **Local inference:**
  - llama.cpp (GGUF format)
  - ExLlamaV2 (EXL2 format)
  - vLLM (production serving)
  - Ollama (easy local deployment)
- **Quantization formats:**
  - GGUF (llama.cpp)
  - GPTQ (GPU-efficient)
  - AWQ (activation-aware)
  - EXL2 (variable bitrate)

#### 2. Prompt Engineering
- **Zero-shot, Few-shot prompting**
- **Chain-of-Thought (CoT)**
- **Self-Consistency**
- **Tree-of-Thought (ToT)**
- **ReAct (Reasoning + Acting)**

#### 3. RAG (Retrieval-Augmented Generation)
- **Components:**
  - Document loader
  - Embedding model
  - Vector database
  - Retriever
  - Reranker
- **Frameworks:** LangChain, LlamaIndex, Haystack
- **Advanced:**
  - Hybrid search (BM25 + semantic)
  - Multi-query
  - Parent document retriever

#### 4. Advanced Tools
- **Function calling:** Tool use, structured outputs
- **Agents:** LLM as reasoning engine + tool access
- **Multimodal:** Vision-language models

---

## 🔧 Practical Notebooks

### Quick Tools (Colab)
| Notebook | Purpose |
|----------|---------|
| 🧐 LLM AutoEval | Auto-evaluate LLMs using RunPod |
| 🥱 LazyMergekit | Merge models in one click |
| 🦎 LazyAxolotl | Fine-tune in cloud with one click |
| ⚡ AutoQuant | Quantize in GGUF, GPTQ, EXL2, AWQ, HQQ |
| 🌳 Model Family Tree | Visualize merged model lineage |
| 🚀 ZeroSpace | Create Gradio chat interface |
| ✂️ AutoAbliteration | Abliterate models with custom datasets |
| 🧼 AutoDedup | Deduplicate datasets with Rensa |

### Fine-tuning Notebooks
| Notebook | Description |
|----------|-------------|
| Fine-tune Llama 3.1 with Unsloth | Ultra-efficient SFT |
| Fine-tune Llama 3 with ORPO | Single-stage fine-tuning |
| Fine-tune Mistral-7b with DPO | Preference optimization |
| Fine-tune Mistral-7b with QLoRA | Free-tier SFT with TRL |
| Fine-tune CodeLlama using Axolotl | End-to-end guide |

### Quantization Notebooks
| Notebook | Description |
|----------|-------------|
| Introduction to Quantization | 8-bit quantization |
| 4-bit Quantization using GPTQ | Consumer hardware deployment |
| Quantization with GGUF/llama.cpp | HF Hub upload |
| ExLlamaV2 | Fastest LLM library |

### Advanced Notebooks
| Notebook | Description |
|----------|-------------|
| Merge LLMs with MergeKit | Create models without GPU |
| Create MoEs with MergeKit | Combine experts into frankenMoE |
| Uncensor with abliteration | Fine-tuning without retraining |
| Knowledge Graphs + ChatGPT | Augment with KGs |

---

## 🔑 Key Concepts Learned

### Architecture Insights
1. **Decoder-only dominates:** GPT-style models are the standard for LLMs
2. **Tokenization matters:** BPE is most common, affects model efficiency
3. **Attention scaling:** O(n²) complexity, optimized with flash attention
4. **Sampling strategies:** Temperature, nucleus, beam search tradeoffs

### Training Pipeline
```
Pre-training (massive data)
    ↓
SFT (instruction-response pairs)
    ↓
Preference Alignment (RLHF/DPO)
    ↓
Evaluation (benchmarks)
```

### Post-training Data Flow
```
Seed Data → Synthetic Generation → Enhancement → Quality Filter → Final Dataset
```

### Fine-tuning Techniques
| Technique | Parameters Updated | Memory | Use Case |
|-----------|-------------------|--------|----------|
| Full FT | All | High | Full adaptation |
| LoRA | Adapter matrices | Low | Efficient fine-tuning |
| QLoRA | 4-bit + adapter | Very Low | Consumer hardware |

---

## 📚 Recommended Resources by Section

### Architecture
- 3Blue1Brown - Transformers visualization
- LLM Visualization (Brendan Bycroft)
- nanoGPT (Karpathy) - GPT from scratch
- Attention? Attention! (Lilian Weng)

### Pre-training
- FineWeb (Penedo et al.) - 15T token dataset
- RedPajama v2 - Quality filtering
- nanotron (Hugging Face) - Minimal training codebase
- OLMo 2 (AI2) - Open-source LLM

### Post-training
- Synthetic Data Generator (Argilla)
- LLM Datasets (curated list)
- NeMo-Curator (Nvidia)
- Distilabel (Argilla)
- Semhash - Near-deduplication

### SFT
- Unsloth tutorial
- Axolotl documentation
- TRL documentation
- LoRA insights paper

### Evaluation
- LLM AutoEval
- Open LLM Leaderboard
- MT-Bench, AlpacaEval

---

## 🎯 Practical Applications

### What You Can Build
1. **Custom fine-tuned model** - SFT + DPO on custom data
2. **Merged model** - Combine multiple experts
3. **Quantized deployment** - Run on consumer hardware
4. **RAG system** - Knowledge-augmented generation
5. **Agent** - Tool-calling LLM

### Key Takeaways
- Data quality > hyperparameter optimization
- Synthetic data enables scaling
- LoRA/QLoRA democratizes fine-tuning
- Evaluation requires multiple benchmarks
- Deployment needs quantization for efficiency

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Notebooks | 30+ |
| Sections | 3 (Fundamentals, Scientist, Engineer) |
| Colab Links | 20+ |
| Articles | 15+ |

---

## 🔗 Companion Book

**LLM Engineer's Handbook** - Co-authored by Maxime Labonne
- End-to-end LLM application design to deployment
- Available from Packt Publishing
- Course remains free, book supports author

---

## 📝 Notes

- **Prerequisites:** Python programming, basic ML
- **Hardware:** Colab notebooks run on free tier
- **Frameworks:** PyTorch, Transformers, TRL
- **Active maintenance:** Regular updates
- **Community:** GitHub discussions for Q&A

---

**Relevância:** ★★★★★ (Comprehensive Learning Path)
**Status:** `completed`
**Reading Time:** Course ~40 hours, Notebooks ~2-4 hours each