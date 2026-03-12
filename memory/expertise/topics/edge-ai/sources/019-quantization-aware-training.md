# Quantization Aware Training (QAT)

**Fonte:** IBM Think
**Link:** https://www.ibm.com/think/topics/quantization-aware-training
**Tipo:** Educational Resource

---

## Resumo Executivo

QAT integra quantização diretamente no treinamento, simulando efeitos de baixa precisão durante o forward pass. Diferente de PTQ (Post-Training Quantization), QAT mantém accuracy mesmo em quantização agressiva (INT8, INT4).

---

## Conceito Fundamental

### Quantização
- Converte FP32/FP16 para INT8/INT4
- Reduz memória, acelera inferência
- Introduz erro de quantização

### QAT vs PTQ

| Aspecto | QAT | PTQ |
|---------|-----|-----|
| Treinamento | Necessário | Não necessário |
| Recursos | Alto | Baixo |
| Accuracy | Alta | Pode degradar |
| Datasets | Precisa representativos | Não precisa |
| Complexidade | Alta | Baixa |

---

## Como Funciona

### Fake Quantization
- Insere operações de quantização "fakes" no grafo
- Simula comportamento de INT8 durante treinamento
- Forward: valores quantizados
- Backward: gradientes em FP

### Fórmula de Quantização
```
Q(x) = Δ · round(clip(x/Δ, l, u))
```

Onde:
- Δ = step size
- l, u = limites inferior/superior

### Straight-Through Estimator (STE)
- Gradient: Q'(x) = 1 (identity)
- Permite backprop apesar de não-diferenciabilidade
- Funciona bem exceto em quantização binária

---

## Processo de Treinamento

1. **Forward Pass**: Valores quantizados para cálculo
2. **Backward Pass**: STE passa gradientes
3. **Weight Update**: Pesos FP32 atualizados
4. **Projection**: Pesos quantizados após update
5. **Repeat**: Por centenas de epochs

---

## Frameworks

### PyTorch QAT
- Eager mode: `torch.quantization`
- FX graph mode: transformações completas
- Custom observers para fine-grained control
- Symmetric/asymmetric quantization

### TensorFlow QAT
- Keras Model Optimization Toolkit
- `apply_quantization_aware_training()` API
- Conversão para TFLite
- Foco em INT8 para mobile/edge

---

## Técnicas Avançadas

### PACT (Parameterized Clipping)
- Aprende clipping ranges durante treinamento
- Adaptive para activations

### LSQ (Learned Step Size Quantization)
- Aprende step sizes (Δ)
- Fine-tuning para cada layer

---

## Aplicações Edge

### Mobile Devices
- Hardware otimizado para INT8
- QAT enable deploy sem perda de accuracy
- Memory footprint reduzido

### IoT/Embedded
- Microcontroladores com recursos limitados
- INT8 ou até INT4 para modelos pequenos
- Inferência em tempo real

### Computer Vision
- CNNs para classificação
- MNIST: accuracy próxima ao FP original
- Object detection, segmentation

---

## Vantagens e Desvantagens

### Vantagens
- Mantém accuracy em quantização agressiva
- Melhor para modelos de longa vida
- Essencial para edge deployment

### Desvantagens
- Computacionalmente caro (centenas de epochs)
- Precisa datasets representativos
- Complexidade de implementação

---

## Comparação com PTQ

### Quando Usar QAT
- Alta accuracy necessária
- Quantização extrema (INT4)
- Modelo de produção de longo prazo
- Edge/mobile deployment crítico

### Quando PTQ é Suficiente
- Prototipagem rápida
- Accuracy não crítico
- Recursos limitados
- Modelo de curta vida

---

## Citações Importantes

> "QAT enables reliable inference on resource-constrained devices, making it essential for edge computing and mobile applications."

> "Straight-through estimator treats the quantization operation as an identity function during backpropagation."

---

## Conexões com Edge AI

QAT é **técnica fundamental** para:
- Deploy de LLMs em edge
- Quantização INT8/INT4 para MCUs
- Manutenção de accuracy em modelos edge
- Otimização para hardware específico

### Relevância
- ★★★★★ Técnica essencial para edge deployment
- Complementa pruning e distillation
- Frameworks maduros (PyTorch, TensorFlow)

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Técnica essencial para edge ML)