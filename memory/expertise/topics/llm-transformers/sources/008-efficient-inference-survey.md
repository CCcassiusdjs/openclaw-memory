# 008 - A Survey on Efficient Inference for LLMs

**Fonte:** https://arxiv.org/abs/2404.14294
**Autores:** Zhou, Ning, Hong, Fu, Xu, Li, Lou, Wang, Yuan, Li, Yan, Dai, Zhang, Dong, Wang
**Ano:** 2024
**Tipo:** Survey Acadêmico
**Relevância:** ★★★★★ (Inferência Essencial)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo Executivo

Survey abrangente sobre técnicas de inferência eficiente para LLMs. Organiza otimizações em três níveis: data-level, model-level e system-level. Aborda as causas fundamentais da ineficiência: tamanho do modelo, complexidade quadrática da attention e decoding auto-regressivo.

---

## 🎯 Causas da Ineficiência

### 1. Large Model Size
- Bilhões de parâmetros exigem memória e compute massivos
- Movement de pesos domina latência em batch pequeno

### 2. Quadratic Attention Complexity
- Self-attention: O(n²) onde n é comprimento da sequência
- KV cache cresce linearmente com comprimento
- Memory bandwidth bottleneck

### 3. Auto-regressive Decoding
- Token gerado sequencialmente (não pode paralelizar)
- Cada token requer forward pass completo
- Latência de geração: O(sequence_length × model_forward)

---

## 📊 Taxonomia de Otimizações

### Data-Level Optimization
| Técnica | Descrição | Benefício |
|---------|-----------|-----------|
| **Input Compression** | Comprimir prompts | Reduz tokens de input |
| **Speculative Decoding** | Draft model + verification | Paraleliza geração |
| **Adaptive Computation** | Ajusta compute por token | Economia em tokens fáceis |

### Model-Level Optimization
| Técnica | Descrição | Benefício |
|---------|-----------|-----------|
| **Quantization** | Reduzir precisão dos weights | Menos memória, mais rápido |
| **Pruning** | Remover pesos/filters não importantes | Modelo menor |
| **Knowledge Distillation** | Treinar modelo menor | Deploy mais rápido |
| **Architecture Search** | Encontrar arquitetura eficiente | Melhor performance/eficiência |

### System-Level Optimization
| Técnica | Descrição | Benefício |
|---------|-----------|-----------|
| **KV Cache Optimization** | Gerenciar cache eficientemente | Menos memória |
| **Parallelism** | Tensor/pipeline parallel | Escalar para modelos grandes |
| **Memory Management** | PagedAttention, offloading | Rodar modelos grandes em GPU pequena |

---

## 🔧 Quantização

### Tipos
| Método | Descrição | Uso |
|--------|-----------|-----|
| **PTQ (Post-Training Quantization)** | Quantiza sem retreinar | Deploy rápido |
| **QAT (Quantization-Aware Training)** | Treina com quantização | Melhor precisão |
| **AWQ** | Activation-aware weight quantization | Melhor que GPTQ |
| **GPTQ** | Optimal brain quantization | Popular para LLMs |
| **GGUF/GGML** | Formato para CPU inference | CPU + offload |

### Bits vs Performance
| Precisão | Tamanho Relativo | Speedup | Perda de Qualidade |
|----------|------------------|---------|-------------------|
| FP16 | 100% | 1× | Baseline |
| INT8 | 50% | ~1.5× | ~0.5% |
| INT4 | 25% | ~2× | ~1-2% |
| FP4/NF4 | 12.5% | ~2.5× | ~2-5% |

---

## 📝 Notas Pessoais

### Insights Principais
- Memory bandwidth é o bottleneck principal em batch pequeno
- Quantização é técnica mais madura e adotada
- Speculative decoding é promissor para latência
- KV cache optimization é crítico para sequências longas

### Quando Usar Cada Técnica
- **Quantização**: Sempre (INT8 é quase free lunch)
- **KV Cache**: Sequências longas (>1024 tokens)
- **Speculative Decoding**: Batch pequeno, latência crítica
- **Pruning**: Quando storage é limitante

---

## 🎯 Próxima Fonte

Ler **"Byte-Pair Encoding tokenization"** para entender tokenização BPE.