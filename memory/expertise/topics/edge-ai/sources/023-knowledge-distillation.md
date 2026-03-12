# Knowledge Distillation: Teacher-Student Learning

**Fonte:** IBM Think
**Link:** https://www.ibm.com/think/topics/knowledge-distillation
**Tipo:** Educational Resource

---

## Resumo Executivo

Knowledge Distillation (KD) treina um modelo menor ("student") para imitar um modelo maior ("teacher"), transferindo conhecimento e capacidades. Essential para deploy de modelos compactos em edge.

---

## Conceito Fundamental

### Definição
- **Teacher Model**: Modelo grande, complexo, pré-treinado
- **Student Model**: Modelo compacto, eficiente
- **Objetivo**: Student aprende a generalizar como teacher

### História
- Origem: "Model Compression" (Caruana et al., 2006)
- Hinton et al. (2015): "Distilling the Knowledge in a Neural Network"
- Aplicação moderna: LLMs para modelos menores

---

## Por Que Knowledge Distillation?

### Limitações de Modelos Grandes
- Lentos
- Caros computacionalmente
- Impraticáveis para edge

### Limitações de Modelos Pequenos
- Menos accurate
- Menos capacity
- Faltam emergent abilities

### Solução KD
- Captura "thought process" do teacher
- Preserva emergent abilities
- Viabiliza deploy edge

---

## Como Funciona

### Soft Targets
- Teacher gera logits (predições intermediárias)
- Probabilidade distribution sobre classes
- Mais informação que hard labels
- Exemplo: fox classificado como 80% dog, 15% fox, 5% cat

### Temperatura
- High temperature = high entropy
- Predições mais variadas = mais informação
- Útil quando teacher muito "confident"

### Distillation Loss

```
Loss_total = α * Loss_hard + β * Loss_distillation
```

- **Loss_hard**: Cross-entropy com ground truth
- **Loss_distillation**: KL divergence entre teacher e student logits
- **α, β**: Hyperparâmetros

---

## Tipos de Conhecimento

### Response-Based Knowledge
- Foco na output layer
- Student aprende logits do teacher
- Mais comum
- Simples de implementar

### Feature-Based Knowledge
- Foco em hidden layers
- Student aprende features intermediárias
- Captura feature extraction do teacher
- Mais complexo

### Relation-Based Knowledge
- Foco em relações entre partes da rede
- Captura dependências estruturais
- Mais avançado

---

## Aplicações

### Computer Vision
- Image classification
- Object detection
- Image segmentation

### NLP
- LLM distillation para modelos menores
- BERT → DistilBERT
- GPT → modelos compactos

### Speech Recognition
- Teacher-student para acoustic models
- Deploy em dispositivos móveis

---

## Casos de Sucesso

### DistilBERT
- 40% menor que BERT
- 97% da accuracy
- 60% mais rápido

### MobileBERT
- 4.3x menor
- Designed para mobile
- Comparable accuracy

### TinyBERT
- Two-stage distillation
- 14x smaller
- Comparable GLUE scores

---

## Processo de Distillation

### Pipeline
1. Treinar teacher model (grande)
2. Coletar soft targets do teacher
3. Definir student architecture (compacta)
4. Treinar student com distillation loss
5. Fine-tune se necessário
6. Deploy student em edge

### Hyperparâmetros
- Temperatura: 2-5 típico
- α (hard loss weight): 0.1-0.3
- β (distillation weight): 0.7-0.9

---

## Vantagens e Desvantagens

### Vantagens
- Compactação significativa
- Preserva mais que só accuracy
- Transfere reasoning
- Fewer training examples needed
- Explainability melhorada

### Desvantagens
- Necessita teacher treinado
- Processo two-stage
- Architecture design do student
- Pode não capturar tudo

---

## Citações Importantes

> "Knowledge distillation aims to not only replicate the outputs of teacher models, but to emulate their 'thought processes'."

> "Soft targets provide far more information per training case than hard targets alone."

> "Student models can be trained on fewer examples, using higher learning rate, than teacher."

---

## Conexões com Edge AI

Knowledge Distillation é **técnica essencial** para:
- Deploy de capacidades avançadas em edge
- Modelos compactos com performance próxima ao teacher
- Transferência de reasoning para dispositivos limitados
- Redução de latência e consumo energético

### Relevância
- ★★★★★ Técnica fundamental para edge AI
- Complementa quantização e pruning
- Enables small models with emergent abilities

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Técnica essencial para compressão)