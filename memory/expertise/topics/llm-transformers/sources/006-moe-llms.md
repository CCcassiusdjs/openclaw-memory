# 006 - Mixture-of-Experts (MoE) LLMs

**Fonte:** https://cameronrwolfe.substack.com/p/moe-llms
**Autor:** Cameron R. Wolfe
**Tipo:** Blog Post (Technical Deep Dive)
**Relevância:** ★★★★★ (MoE Essencial)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo Executivo

Mixture-of-Experts (MoE) permite escalar modelos massivamente sem aumentar proporcionalmente o custo computacional. Cada token é processado apenas por um subconjunto de experts (ex: 2 de 8), resultando em modelos com muitos parâmetros mas custo de inferência similar a modelos menores.

---

## 🏗️ Arquitetura MoE

### Modificação do Transformer
- **Padrão**: Feed-forward network (FFN) única
- **MoE**: Múltiplas FFNs independentes (experts)
- Cada token é "roteado" para K experts (tipicamente K=2)

### Estrutura
```
Expert Layer:
- N experts (ex: 8)
- Router network (linear + softmax)
- Top-K selection
- Weighted average output
```

### Interleaved MoE
- Nem toda camada precisa ser MoE
- Stride P: toda P-ésima camada é MoE
- Comum: P=2, P=4, P=6
- Balanceia performance vs. eficiência

---

## 🔀 Routing Mechanism

### Processo de Roteamento
1. **Linear transform**: Token → scores para cada expert
2. **Softmax**: Converte em probabilidades
3. **Top-K selection**: Seleciona K experts com maior probabilidade
4. **Weighted output**: Combina outputs dos experts selecionados

### Fórmula
```
output = Σ (prob_i × expert_i(token))  para i ∈ top-k experts
```

### Routing Collapse (Problema)
- Router tende a selecionar sempre os mesmos experts
- Auto-reinforcing: experts favorecidos treinam mais
- Resultado: uso desbalanceado dos experts

---

## ⚖️ Load Balancing

### Importance Loss (Original)
```
Importance_i = Σ p_i(t) para todos tokens t no batch
L_importance = CV²(Importance)  # coefficient of variation squared
```
- Penaliza distribuição desbalanceada de importância
- Não garante balanceamento de tokens

### Load Balancing Loss (Switch Transformer)
```
L_aux = α × Σ(f_i × P_i)
f_i = fração de tokens roteados ao expert i
P_i = fração de probabilidade do router para expert i
```
- Combina importância e load balancing
- Minimizado quando distribuição é uniforme

### Router Z-Loss (ST-MoE)
```
L_z = (1/B) × Σ (logits)²
```
- Regulariza magnitude dos logits
- Previne instabilidade numérica no softmax
- Usado em conjunto com load balancing loss

---

## 📊 Expert Capacity

### Definição
```
expert_capacity = (tokens_per_batch / num_experts) × capacity_factor
```

### Capacity Factor
- **1.0**: Balanceamento perfeito
- **>1.0**: Buffer para imbalance
- Comum: 1.25 (treino), 2.0 (inferência)

### Token Dropping
- Se tokens > capacity → overflow
- Tokens excedentes passam via residual connection
- Sem computação no expert

---

## 🔗 Shared vs Routed Experts

### Shared Experts (Inovação Recente)
- Alguns experts processam **todos** os tokens
- Reduz informação redundante entre experts
- Exemplo: DeepSeek-v3, Mixtral

### Routed Experts
- Selecionados dinamicamente pelo router
- Processam apenas tokens roteados

### Output Final
```
output = shared_output + routed_output
```

---

## ✅ Benefícios do MoE

### Escalabilidade Eficiente
- **Parâmetros totais**: Grandes (ex: 47B)
- **Parâmetros ativos**: Menores (ex: 13B)
- **Inferência**: Similar a modelo denso menor

### Treinamento Mais Rápido
- Switch Transformer: 7× speedup
- Custo fixo por token
- Melhor utilização de hardware

### Performance
- Superam modelos densos maiores
- Melhor em code, math, multilingual

---

## ❌ Desvantagens do MoE

### Instabilidade no Treino
- Sensível a hyperparâmetros
- Router collapse
- Dificuldade de convergência

### Fine-tuning Desafiador
- Propenso a overfitting
- Menos parâmetros ativos por batch
- Requer técnicas especiais

### Precisão Sensível
- Low/mixed precision pode causar problemas
- Logits grandes → round-off errors
- FP32 necessário no router

### Memory Footprint
- Todos parâmetros precisam estar em GPU
- Requer mais VRAM que modelo denso do mesmo tamanho ativo

---

## 🔬 Mixtral 8×7B

### Especificações
| Parâmetro | Valor |
|-----------|-------|
| Total params | 47B |
| Active params | 13B |
| Experts per layer | 8 |
| Active experts | 2 |
| Context length | 32K |
| Layers with MoE | All |

### Arquitetura Base (Mistral-7B)
- **Grouped-Query Attention (GQA)**: Compartilha K/V entre grupos de heads
- **Sliding Window Attention (SWA)**: Janela fixa para eficiência
- **RoPE**: Rotary position embedding

### Performance
- Supera LLaMA-2-70B em vários benchmarks
- Excelente em code e math
- Multilingual forte

### Routing Analysis
- Experts não são especializados por tópico
- Mas seguem padrões sintáticos:
  - Tokens de indentação → mesmo expert
  - Sequências consecutivas → mesmo expert
  - "self" em Python → mesmo expert

---

## 🚀 Grok

### Grok-1
| Parâmetro | Valor |
|-----------|-------|
| Total params | 314B |
| Active params | ~70-80B |
| Weights active | 25% |

### Grok-1.5
- Context length: 128K tokens
- Melhor em math e coding
- Needle-in-haystack: perfeito

### Grok-2
- Reasoning melhorado
- Chatbot Arena melhor score
- Distilled version: Grok-2-mini

---

## 🏗️ DBRX

### Especificações
- Open LLM da Databricks/Mosaic
- Base model + Instruct model
- Arquitetura MoE moderna

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Expert** | FFN independente no MoE layer |
| **Router** | Rede que seleciona experts (linear + softmax) |
| **Top-K** | Número de experts ativos por token |
| **Active params** | Parâmetros usados por token (não total) |
| **Capacity factor** | Buffer para desbalanceamento |
| **Shared experts** | Experts que processam todos tokens |
| **Routing collapse** | Problema de seleção não-balanceada |
| **Load balancing loss** | Regularização para usar todos experts |

---

## 📝 Notas Pessoais

- MoE é padrão para modelos muito grandes (GPT-4, Grok, Mixtral)
- Key insight: separar total params de active params
- Routing ainda é área de pesquisa ativa
- Shared experts é tendência moderna (DeepSeek-v3)
- Trade-off: mais VRAM vs. inferência mais rápida

### Quando Usar MoE?
- ✅ Modelos muito grandes (scale law benefits)
- ✅ Inferência em batch grande
- ✅ Pre-training massivo
- ❌ Fine-tuning em dataset pequeno
- ❌ Ambientes com VRAM limitada

---

## 🎯 Próxima Fonte

Ler **"Parameter-Efficient Fine-Tuning using PEFT"** para entender fine-tuning eficiente.