# GPT-3: Language Models are Few-Shot Learners

**Fonte:** https://arxiv.org/abs/2005.14165
**Autores:** Tom B. Brown, Benjamin Mann, Nick Ryder, et al. (OpenAI)
**Ano:** 2020
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Paper seminal do GPT-3 demonstrando que scaling up language models melhora drasticamente a performance few-shot. Modelo com 175B parâmetros, 10x maior que qualquer modelo não-esparso anterior. Mostra que few-shot learning é possível sem fine-tuning.

---

## 🎯 Contribuições Principais

### Escala Sem Precedentes
- **175 bilhões de parâmetros**
- 10x maior que modelos anteriores
- Treinado em corpora massivos da web

### Few-Shot Learning
- **Sem fine-tuning**: Tarefas especificadas via texto
- **Sem gradient updates**: Apenas inferência
- **Task-agnostic**: Mesma arquitetura para todas as tarefas

---

## 📊 Resultados

### Tarefas Testadas
- **Translation**: Tradução automática
- **Question-Answering**: QA datasets
- **Cloze Tasks**: Completar texto
- **On-the-fly reasoning**: Operações aritméticas, unscrambling

### Performance
- Competitive com SOTA fine-tuned em várias tarefas
- Few-shot GPT-3 ≈ fine-tuned BERT em alguns benchmarks
- Escala correlaciona com performance

---

## 🔬 Metodologia

### Arquitetura
- Autoregressive language model
- Transformer decoder-only
- Mesma arquitetura do GPT-2, escalada

### Training
- Dataset: Common Crawl + WebText + Books + Wikipedia
- Tokens: ~500B (filtrados para qualidade)
- Compute: Miles de petaflop/s-days

### Few-Shot Setting
1. **Zero-shot**: "Translate to French: [text]"
2. **One-shot**: Exemplo único + task
3. **Few-shot**: Vários exemplos + task

---

## 💡 Insights Principais

### Scaling Laws
- Performance aumenta consistentemente com escala
- Few-shot performance melhora mais rápido que zero-shot
- Emergent abilities em escala grande

### In-Context Learning
- Modelo aprende tarefas do prompt
- Não há atualização de pesos
- Capacidade aumenta com scale

### Limitações
- Struggle em alguns datasets
- Methodological issues com web data
- Bias e fairness concerns

---

## 📈 Implicações

### Para Field de NLP
- Fine-tuning não é necessário para muitas tarefas
- Scale é um caminho viável para melhor performance
- Few-shot learning é promissor

### Para Prática
- Prompts engineering como skill
- API-based model serving
- Lower barrier to entry (sem fine-tuning)

---

## 🔗 Papers Relacionados

1. GPT-2 (Radford et al., 2019) - Predecessor
2. BERT (Devlin et al., 2018) - Encoder-only comparison
3. Scaling Laws (Kaplan et al., 2020) - Teoria de scaling

---

## 📝 Tags

`#gpt3` `#few-shot` `#scaling` `#openai` `#language-model` `#transformer` `#landmark-paper`