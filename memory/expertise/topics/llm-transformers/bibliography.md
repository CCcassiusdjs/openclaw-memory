# LLM & Transformers Architecture - Bibliografia

**Topic ID:** llm-transformers
**Priority:** 1
**Status:** researching
**Created:** 2026-03-12
**Last Updated:** 2026-03-12

---

## 📚 Fontes Organizadas por Relevância

### 🔴 ESSENCIAL (Papers Fundamentais)

#### 1. "Attention Is All You Need" - Paper Original do Transformer
- **URL:** https://arxiv.org/abs/1706.03762
- **Autores:** Vaswani et al. (Google Brain)
- **Ano:** 2017
- **Status:** `pending`
- **Relevância:** ★★★★★ (Fundacional)
- **Descrição:** Paper seminal que introduziu a arquitetura Transformer, mecanismo de self-attention e codificação posicional. Base de todos os LLMs modernos.

#### 2. "The Illustrated Transformer" - Visual Guide
- **URL:** https://jalammar.github.io/illustrated-transformer/
- **Autor:** Jay Alammar
- **Status:** `pending`
- **Relevância:** ★★★★★ (Didático Essencial)
- **Descrição:** Explicação visual clara da arquitetura Transformer. Ideal para entender conceitos antes de mergulhar no paper original.

#### 3. "A Comprehensive Overview of Large Language Models"
- **URL:** https://arxiv.org/pdf/2307.06435
- **Ano:** 2023
- **Status:** `pending`
- **Relevância:** ★★★★★ (Survey Completo)
- **Descrição:** Survey abrangente sobre LLMs, cobrindo treinamento, fine-tuning, arquiteturas e aplicações.

---

### 🟠 ARQUITETURA E COMPONENTES

#### 4. "The Illustrated GPT-2" - Decoder-Only Transformers
- **URL:** https://jalammar.github.io/illustrated-gpt2/
- **Autor:** Jay Alammar
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Arquitetura GPT)
- **Descrição:** Explicação visual da arquitetura GPT-2, modelo decoder-only que se tornou base para LLMs modernos como GPT-3/4.

#### 5. "Decoder-Only Transformers: The Workhorse of Generative LLMs"
- **URL:** https://cameronrwolfe.substack.com/p/decoder-only-transformers-the-workhorse
- **Autor:** Cameron R. Wolfe
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Arquitetura Moderna)
- **Descrição:** Análise profunda de por que decoder-only transformers se tornaram dominantes em LLMs generativos.

#### 6. "Towards Smaller, Faster Decoder-Only Transformers"
- **URL:** https://arxiv.org/abs/2404.14462
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Otimização)
- **Descrição:** Paper sobre variantes de arquitetura decoder-only para eficiência: ParallelGPT, LinearlyCompressedGPT, ConvCompressedGPT.

#### 7. "How Powerful are Decoder-Only Transformer Neural Models?"
- **URL:** https://arxiv.org/abs/2305.17026
- **Ano:** 2023
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Teoria)
- **Descrição:** Prova de que transformers decoder-only são Turing-completos sob certertas condições.

---

### 🟡 BERT E ENCODER-ONLY MODELS

#### 8. "BERT (language model)" - Wikipedia Overview
- **URL:** https://en.wikipedia.org/wiki/BERT_(language_model)
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Referência Rápida)
- **Descrição:** Visão geral do BERT, primeiro modelo encoder-only de grande escala usando masked language modeling.

#### 9. "Fine-Tuning BERT with Masked Language Modeling"
- **URL:** https://www.analyticsvidhya.com/blog/2022/09/fine-tuning-bert-with-masked-language-modeling/
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Prático)
- **Descrição:** Tutorial sobre fine-tuning de BERT usando MLM.

#### 10. "BPDec: Unveiling the Potential of Masked Language Modeling Decoder"
- **URL:** https://arxiv.org/abs/2401.15861
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Avançado)
- **Descrição:** Melhorias no decoder MLM para pretraining de BERT.

---

### 🟢 TOKENIZAÇÃO E EMBEDDINGS

#### 11. "Byte Pair Encoding (BPE) in Large Language Models"
- **URL:** https://vizuara.substack.com/p/understanding-byte-pair-encoding
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Fundacional)
- **Descrição:** Explicação detalhada de BPE, algoritmo de tokenização usado em GPT-2 e modelos subsequentes.

#### 12. "Theoretical Analysis of Byte-Pair Encoding"
- **URL:** https://arxiv.org/abs/2411.08671
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Teoria)
- **Descrição:** Análise teórica formal do algoritmo BPE.

#### 13. "Byte-Pair Encoding tokenization - Hugging Face LLM Course"
- **URL:** https://huggingface.co/learn/llm-course/en/chapter6/5
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Prático)
- **Descrição:** Tutorial oficial do Hugging Face sobre tokenização BPE.

#### 14. "minbpe" - Implementação Minimalista de BPE
- **URL:** https://github.com/karpathy/minbpe
- **Autor:** Andrej Karpathy
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Código)
- **Descrição:** Implementação limpa e minimalista de BPE por Karpathy.

---

### 🔵 POSITION ENCODING

#### 15. "RoFormer: Enhanced Transformer with Rotary Position Embedding"
- **URL:** https://arxiv.org/abs/2104.09864
- **Ano:** 2021
- **Status:** `pending`
- **Relevância:** ★★★★★ (RoPE Original)
- **Descrição:** Paper que introduziu RoPE (Rotary Position Embedding), agora padrão em LLMs modernos como LLaMA.

#### 16. "Rotary Embeddings: A Relative Revolution" - EleutherAI Blog
- **URL:** https://blog.eleuther.ai/rotary-embeddings/
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Didático)
- **Descrição:** Explicação clara de RoPE e por que funciona melhor que position embeddings absolutos.

#### 17. "Inside RoPE: Rotary Magic into Position Embeddings"
- **URL:** https://learnopencv.com/rope-position-embeddings/
- **Ano:** 2025
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Tutorial)
- **Descrição:** Tutorial visual sobre RoPE.

---

### 🟣 MIXTURE OF EXPERTS (MoE)

#### 18. "A Survey on Mixture of Experts in Large Language Models"
- **URL:** https://arxiv.org/pdf/2407.06204
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★★ (Survey MoE)
- **Descrição:** Survey completo sobre MoE em LLMs, cobrindo sparse activation, routing e arquiteturas modernas.

#### 19. "Mixture-of-Experts (MoE) LLMs" - Cameron Wolfe
- **URL:** https://cameronrwolfe.substack.com/p/moe-llms
- **Ano:** 2025
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Didático)
- **Descrição:** Explicação detalhada de MoE com exemplos de Grok-1 e outros modelos.

#### 20. "A Visual Guide to Mixture of Experts (MoE)"
- **URL:** https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-mixture-of-experts
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Visual)
- **Descrição:** Guia visual intuitivo sobre como MoE funciona.

---

### 🟤 FINE-TUNING E PEFT

#### 21. "Parameter-Efficient Fine-Tuning using 🤗 PEFT"
- **URL:** https://huggingface.co/blog/peft
- **Status:** `pending`
- **Relevância:** ★★★★★ (Prático Essencial)
- **Descrição:** Tutorial oficial do Hugging Face sobre PEFT, LoRA e fine-tuning eficiente.

#### 22. "Practical Guide to Fine-tune LLMs with LoRA"
- **URL:** https://medium.com/@manindersingh120996/practical-guide-to-fine-tune-llms-with-lora-c835a99d7593
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Tutorial)
- **Descrição:** Guia prático de implementação de LoRA usando a biblioteca PEFT.

#### 23. "Efficient Fine-Tuning with LoRA: A Guide to Optimal Parameter Selection"
- **URL:** https://www.databricks.com/blog/efficient-fine-tuning-lora-guide-llms
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Otimização)
- **Descrição:** Guia da Databricks sobre seleção de parâmetros para LoRA.

#### 24. "Fine Tuning LLM: PEFT — LoRA & QLoRA — Part 1"
- **URL:** https://abvijaykumar.medium.com/fine-tuning-llm-parameter-efficient-fine-tuning-peft-lora-qlora-part-1-571a472612c4
- **Ano:** 2023
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Introdução)
- **Descrição:** Introdução a PEFT, LoRA e QLoRA.

---

### ⚫ QUANTIZATION E INFERENCE

#### 25. "A Survey on Efficient Inference for Large Language Models"
- **URL:** https://arxiv.org/abs/2404.14294
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★★★ (Survey Inferência)
- **Descrição:** Survey completo sobre otimização de inferência: data-level, model-level e system-level.

#### 26. "LLMs on CPU: The Power of Quantization with GGUF, AWQ, & GPTQ"
- **URL:** https://www.ionio.ai/blog/llms-on-cpu-the-power-of-quantization-with-gguf-awq-gptq
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Prático)
- **Descrição:** Comparação prática de técnicas de quantização para inferência em CPU.

#### 27. "Quantized Local LLMs: 4-bit vs 8-bit Performance Analysis"
- **URL:** https://www.sitepoint.com/quantized-local-llms-4bit-vs-8bit-analysis/
- **Ano:** 2025
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Benchmark)
- **Descrição:** Análise de performance comparando Q4_K_M, Q8_0, GPTQ, AWQ e EXL2.

#### 28. "Simplifying Quantization in LLMs: GGUF, GPTQ, AWQ and More"
- **URL:** https://medium.com/@anand_sahu/simplifying-quantization-in-llms-gguf-gptq-awq-and-more-4c472722e28c
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Visão Geral)
- **Descrição:** Overview de técnicas de quantização para LLMs.

---

### 📖 LIVROS E CURSOS

#### 29. "Build a Large Language Model (From Scratch)" - Sebastian Raschka
- **URL:** https://github.com/rasbt/LLMs-from-scratch
- **Status:** `pending`
- **Relevância:** ★★★★★ (Livro/Código)
- **Descrição:** Livro e repositório para implementar LLMs do zero em PyTorch.

#### 30. "Natural Language Processing with Transformers" - O'Reilly Book
- **URL:** https://www.oreilly.com/library/view/natural-language-processing/9781098136789/
- **Ano:** 2022
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Livro)
- **Descrição:** Livro da O'Reilly sobre NLP com Transformers usando Hugging Face.

#### 31. "Understanding Large Language Models – A Transformative Reading List"
- **URL:** https://sebastianraschka.com/blog/2023/llm-reading-list.html
- **Ano:** 2023
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Curadoria)
- **Descrição:** Lista de leituras selecionadas por Sebastian Raschka sobre LLMs.

#### 32. "LLM Course" - Maxime Labonne
- **URL:** https://github.com/mlabonne/llm-course
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Curso)
- **Descrição:** Curso com roadmaps e notebooks Colab para aprender LLMs.

---

### 🎓 SLIDES E MATERIAL ACADÊMICO

#### 33. "Introduction to Deep Learning - Transformers and LLMs" - CMU
- **URL:** https://deeplearning.cs.cmu.edu/F23/document/slides/lec19.transformersLLMs.pdf
- **Ano:** 2023
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Acadêmico)
- **Descrição:** Slides do curso de Deep Learning da CMU sobre Transformers e LLMs.

#### 34. "Transformers and Large Language Models" - Stanford CS124
- **URL:** https://web.stanford.edu/class/cs124/lec/LLM2024.pdf
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Acadêmico)
- **Descrição:** Slides de Stanford sobre Transformers e LLMs.

#### 35. "The Transformer Architecture: Part I" - UPenn CIS 7000
- **URL:** https://llm-class.github.io/slides/Lecture%205%20-%20The%20Transformer%20Architecture%20-%20Part%20I.pdf
- **Ano:** 2024
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Acadêmico)
- **Descrição:** Slides detalhados sobre a arquitetura Transformer.

---

### 🔧 DOCUMENTAÇÃO E TUTORIAIS

#### 36. "Introduction to Large Language Models" - Google ML
- **URL:** https://developers.google.com/machine-learning/resources/intro-llms
- **Status:** `pending`
- **Relevância:** ★★★☆☆ (Oficial)
- **Descrição:** Módulo de curso do Google sobre LLMs: tokens, n-grams, Transformers, fine-tuning.

#### 37. "Dive into Deep Learning - Attention Mechanisms and Transformers"
- **URL:** http://d2l.ai/chapter_attention-mechanisms-and-transformers/index.html
- **Status:** `pending`
- **Relevância:** ★★★★☆ (Didático)
- **Descrição:** Capítulo do D2L sobre attention e Transformers com código.

---

## 📊 Estatísticas da Bibliografia

| Categoria | Quantidade |
|-----------|------------|
| Papers ArXiv | 12 |
| Blog Posts | 10 |
| Tutoriais | 6 |
| Livros/Cursos | 4 |
| Slides Acadêmicos | 3 |
| Documentação Oficial | 2 |
| **Total** | **37** |

---

## 🎯 Próximos Passos

1. ✅ Bibliografia criada
2. ⏳ Ler fontes por ordem de relevância
3. ⏳ Extrair conceitos-chave de cada fonte
4. ⏳ Criar resumos em `sources/`
5. ⏳ Atualizar `progress.json`

---

## 📝 Notas

- Priorizar papers ★★★★★ primeiro
- Focar em entender: Attention, Self-Attention, Positional Encoding, Tokenização
- Praticar com código: implementações minimalistas (minbpe, LLMs-from-scratch)
- Documentar insights em cada fonte lida