# A Comprehensive Overview of Large Language Models

**Fonte:** https://arxiv.org/abs/2307.06435
**Autores:** Humza Naveed et al.
**Ano:** 2023 (atualizado 2024)
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Survey abrangente que cobre todo o ecossistema de LLMs: desde fundamentos até aplicações avançadas. Organiza o campo em 7 branches: Pre-Training, Fine-Tuning, Efficient LLMs, Inference, Evaluation, Applications, Challenges.

---

## 🔑 Conceitos-Chave

### Tokenização
- **WordPiece**: Usado em BERT
- **Byte Pair Encoding (BPE)**: Padrão em GPT-2 e modelos modernos
- **UnigramLM**: Alternativa probabilística

### Position Encoding
- **Alibi**: Bias temporal que favorece tokens recentes
- **RoPE (Rotary Position Embedding)**: Codificação rotacional que decai com distância
- **Absolute vs Relative**: Trade-offs entre posições fixas e relativas

### Attention Mechanisms
- **Self-Attention**: Q, K, V do mesmo bloco (encoder ou decoder)
- **Cross-Attention**: Encoder outputs como queries, decoder como K, V
- **Sparse Attention**: Janelas deslizantes para O(n²) → O(n log n)
- **Flash Attention**: Tiling para minimizar HBM ↔ SRAM transfers

### Activation Functions
- **ReLU**: `max(0, x)` - simples mas pode ter "dead neurons"
- **GeLU**: Combina ReLU + dropout + zoneout
- **GLU (Gated Linear Unit)**: `(xW + b) ⊗ σ(xV + c)` - gating mechanism

### LLM Evolution Timeline
- **Pre-PLM Era**: Task-specific models supervisionados
- **PLM Era**: Self-supervised pre-training (BERT, GPT-2)
- **LLM Era**: Modelos 10B+ parâmetros (GPT-3, LLaMA, etc.)

---

## 🏗️ Arquiteturas de LLMs

### Encoder-Only (BERT-style)
- Bidirecional, masked language modeling
- Ideal para: classification, NER, QA extraction
- Exemplos: BERT, RoBERTa, ALBERT

### Decoder-Only (GPT-style)
- Unidirecional, causal language modeling
- Ideal para: generation, completion, chat
- Exemplos: GPT-3, LLaMA, Mistral

### Encoder-Decoder (T5-style)
- Bidirecional encoding + unidirecional decoding
- Ideal para: translation, summarization
- Exemplos: T5, BART

---

## 📊 Training Strategies

### Pre-Training Objectives
- **Causal Language Modeling (CLM)**: Prever próximo token
- **Masked Language Modeling (MLM)**: Prever tokens mascarados
- **Prefix Language Modeling**: Combinação de MLM + CLM

### Fine-Tuning Approaches
- **Instruction Tuning**: Dados de instruções manualmente criados
- **RLHF**: Reinforcement Learning from Human Feedback
- **Constitutional AI**: Self-improvement sem humanos
- **DPO**: Direct Preference Optimization

### Efficient Fine-Tuning
- **LoRA**: Low-Rank Adaptation
- **Prefix Tuning**: Embeddings treináveis no prefixo
- **Prompt Tuning**: Soft prompts aprendidos
- **Adapters**: Camadas pequenas inseridas

---

## 🔧 Efficient LLMs

### Quantization
- **PTQ (Post-Training Quantization)**: Sem retraining
- **QAT (Quantization-Aware Training)**: Treino com quantização
- **INT8**: ~8x compressão, perda mínima
- **INT4**: ~16x compressão, perda aceitável para inference

### Pruning
- Remove pesos menos importantes
- Structured vs Unstructured pruning
- Movement pruning para BERT

### Context Length Optimization
- **ALiBi**: Extrapolation natural para sequências longas
- **RoPE interpolation**: Position interpolation para contextos extendidos
- **Flash Attention**: Efficient attention computation

---

## 📈 Scaling Laws

### Key Findings (Kaplan et al.)
- Performance scales predictably com compute, data, params
- **Compute budget**: `N ∝ C^0.73` (parâmetros)
- **Data budget**: `D ∝ C^0.27` (tokens)
- **Optimal**: ~300B tokens para 175B params

### Chinchilla Scaling (Hoffmann et al.)
- Original scaling era sub-ótimo
- Modelos deveriam ser menores, treinar em mais dados
- **Revised**: `N ∝ C^0.5`, `D ∝ C^0.5`

---

## 🎯 Model Categories

### General Purpose
- GPT-3, GPT-4, LLaMA, LLaMA-2, Mistral
- Treinados em corpora diversificados

### Code-Specialized
- Codex, StarCoder, CodeGen
- Fine-tuned em código

### Scientific
- Galactica, BloombergGPT (finance)
- Domain-specific pre-training

### Dialog
- ChatGPT, Claude, Vicuna
- Instruction-tuned para conversação

---

## 🔮 Emerging Abilities

### In-Context Learning
- Few-shot learning sem weight updates
- Emergente em ~10B+ parâmetros

### Chain-of-Thought
- Decomposição de problemas complexos
- "Let's think step by step"

### Tool Use
- Function calling
- Retrieval augmentation (RAG)
- Code execution

---

## 💡 Insights Principais

1. **Decoder-only dominou**: GPT-style venceu por eficiência e qualidade
2. **Scale é tudo**: Leis de scaling previsíveis governam performance
3. **Efficiency é crítico**: Quantização, pruning, PEFT são essenciais
4. **Alignment importa**: RLHF/DPO para modelos úteis e seguros
5. **Context é limitante**: Flash Attention, RoPE interpolation são soluções

---

## 📚 Fontes Secundárias Citadas

1. Vaswani et al. (2017) - Attention Is All You Need
2. Brown et al. (2020) - GPT-3 Paper
3. Hoffmann et al. (2022) - Chinchilla Scaling
4. Su et al. (2021) - RoFormer (RoPE)
5. Hu et al. (2021) - LoRA

---

## 🔗 Próximos Passos

- [ ] Ler papers específicos sobre RoPE (RoFormer)
- [ ] Aprofundar em Flash Attention
- [ ] Estudar Chinchilla scaling em detalhes
- [ ] Revisar papers de PEFT (LoRA, Prefix Tuning)

---

## 📝 Tags

`#survey` `#llm-overview` `#transformer-architecture` `#training-strategies` `#efficient-llms` `#scaling-laws`