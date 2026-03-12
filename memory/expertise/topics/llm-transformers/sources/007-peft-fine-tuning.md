# 007 - Parameter-Efficient Fine-Tuning using PEFT

**Fonte:** https://huggingface.co/blog/peft
**Autores:** Hugging Face (smangrul, sayakpaul)
**Tipo:** Blog Post (Tutorial)
**Relevância:** ★★★★★ (Fine-tuning Essencial)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo Executivo

PEFT (Parameter-Efficient Fine-Tuning) permite fine-tunar modelos grandes congelando a maioria dos parâmetros e treinando apenas uma pequena fração. Reduz drasticamente custos computacionais e de armazenamento, enquanto mantém performance comparável ao full fine-tuning.

---

## 🎯 Motivação

### Problemas do Full Fine-Tuning
1. **Custo computacional**: Modelos de bilhões de parâmetros exigem hardware caro
2. **Armazenamento**: Cada task fine-tunada = modelo completo (ex: 40GB cada)
3. **Catastrophic forgetting**: Fine-tuning pode destruir conhecimento pré-treinado
4. **Low-data regimes**: Full fine-tuning overfitting em datasets pequenos

### Solução PEFT
- **Congelar** maioria dos parâmetros do modelo pré-treinado
- **Treinar** apenas pequeno subconjunto de parâmetros
- **Resultados**: Checkpoints de poucos MB vs. GB

---

## 📊 Métodos Suportados

### 1. LoRA (Low-Rank Adaptation)
**Paper:** Hu et al., 2021

**Conceito:**
- Adiciona matrizes de baixo rank aos weights existentes
- W = W₀ + BA, onde B e D são r × d e d × r (r << d)
- Congela W₀, treina apenas B e A

**Vantagens:**
- Não adiciona latência em inferência (pode ser merged)
- Muito eficiente em memória
- Fácil de implementar

**Parâmetros:**
- `r`: Rank da adaptação (típicos: 8, 16, 32)
- `lora_alpha`: Escala da adaptação (típicos: 16, 32)
- `lora_dropout`: Regularização

### 2. Prefix Tuning
**Paper:** Liu et al., 2021

**Conceito:**
- Adiciona prefixos treináveis ao input
- Congela modelo principal
- Treina apenas embeddings do prefixo

**Vantagens:**
- Apenas 0.1% dos parâmetros treináveis
- Muito eficiente

### 3. Prompt Tuning
**Paper:** Lester et al., 2021

**Conceito:**
- Adiciona tokens virtuais treináveis
- Apenas embeddings dos prompts são treinados
- Modelo completamente congelado

**Vantagens:**
- Extremamente eficiente (menos de 0.01% params)
- Task-specific prompts pequenos

### 4. P-Tuning
**Paper:** Liu et al., 2021

**Conceito:**
- Prompt tuning com encoder (LSTM/MLP)
- Mais expressivo que prompt tuning simples
- Ainda muito eficiente

---

## 🔧 Uso com Hugging Face PEFT

### Instalação e Import
```python
from transformers import AutoModelForSeq2SeqLM
from peft import get_peft_model, LoraConfig, TaskType

model_name = "bigscience/mt0-large"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
```

### Configuração LoRA
```python
peft_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    inference_mode=False,
    r=8,              # rank
    lora_alpha=32,    # scaling
    lora_dropout=0.1  # regularization
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
# output: trainable params: 2359296 || all params: 1231940608 || trainable%: 0.19%
```

### Salvando e Carregando
```python
# Salvar
model.save_pretrained("output_dir")
# Salva apenas ~19MB vs 40GB do modelo completo

# Carregar
from peft import PeftModel, PeftConfig

peft_model_id = "user/my_peft_model"
config = PeftConfig.from_pretrained(peft_model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(config.base_model_name_or_path)
model = PeftModel.from_pretrained(model, peft_model_id)
```

---

## 📈 Benefícios Quantitativos

### Exemplo: bigscience/mt0-xxl
| Aspecto | Full Fine-Tuning | PEFT |
|---------|-----------------|------|
| **Checkpoints** | 40GB cada | ~19MB cada |
| **Treináveis** | 100% | <1% |
| **Performance** | Baseline | Compatível |
| **Hardware** | Multi-GPU | Single GPU |

### Casos de Uso Reais
- **T0_3B (3B params)**: Fine-tuning em RTX 2080 Ti (11GB)
- **OPT-6.7B**: Fine-tuning em Google Colab com INT8
- **Stable Diffusion Dreambooth**: Treino em 11GB GPU

---

## 🎯 Casos de Uso

### 1. Low-Resource Hardware
- Fine-tunar modelos grandes em GPUs consumer
- Google Colab com INT8 + PEFT
- RTX 2080 Ti / 3080 (11GB)

### 2. Multi-Task Deployment
- Um modelo base + múltiplos adapters PEFT
- Trocar adapters sem recarregar modelo
- Portabilidade máxima

### 3. Domain Adaptation
- Adaptar modelos gerais para domínios específicos
- Preservar conhecimento geral
- Checkpoints pequenos

### 4. Privacy-Preserving
- Fine-tuning em dados sensíveis
- Apenas adapter pequeno é compartilhado
- Modelo base permanece privado

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **LoRA** | Low-Rank Adaptation - matrizes pequenas treináveis |
| **Prefix Tuning** | Prefixos treináveis no input |
| **Prompt Tuning** | Embeddings de prompt treináveis |
| **Adapter** | Camadas pequenas inseridas no modelo |
| **Freeze** | Congelar pesos do modelo base |
| **Rank (r)** | Dimensão da adaptação em LoRA |
| **Alpha** | Fator de escala da adaptação |

---

## 🔗 Comparação de Métodos

| Método | Params Traináveis | Inferência Overhead | Performance |
|--------|-------------------|---------------------|-------------|
| **Full Fine-tuning** | 100% | Nenhuma | Melhor |
| **LoRA** | 0.1-1% | Zero (se merged) | Muito boa |
| **Prefix Tuning** | 0.1% | Pequena | Boa |
| **Prompt Tuning** | 0.01% | Nenhuma | Boa (scale dependente) |
| **P-Tuning** | 0.1% | Pequena | Boa |

---

## 📝 Notas Pessoais

### Por que PEFT Funciona?
- Modelos pré-treinados já têm bom conhecimento geral
- Task-specific knowledge requer poucos parâmetros
- Low-rank adaptations são suficientes para maioria das tasks

### Quando Usar PEFT?
- ✅ Fine-tuning em hardware limitado
- ✅ Múltiplas tasks no mesmo modelo
- ✅ Datasets pequenos
- ✅ Preservar conhecimento pré-treinado
- ❌ Quando precisa de máxima performance (full fine-tuning ainda é melhor em alguns casos)

### Melhores Práticas
- **r=8-16**: Bom para maioria das tasks
- **lora_alpha=2×r**: Regra comum
- **Target modules**: Linear layers (q_proj, v_proj, etc.)
- **INT8 + LoRA**: Combinação poderosa para GPUs pequenas

---

## 🎯 Próxima Fonte

Ler **"A Survey on Efficient Inference for LLMs"** para entender otimização de inferência.