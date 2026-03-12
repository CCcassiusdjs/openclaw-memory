# Model Pruning: Comprehensive Guide

**Fonte:** Datature Blog
**Link:** https://datature.io/blog/a-comprehensive-guide-to-neural-network-model-pruning
**Tipo:** Educational Article

---

## Resumo Executivo

Model pruning remove parâmetros não importantes de redes neurais para reduzir tamanho e acelerar inferência. Essential para deploy em edge devices com recursos limitados.

---

## O Que é Pruning?

- Remove parâmetros não importantes (geralmente pesos, não biases)
- Baseado na hipótese: redes têm parâmetros em excesso
- "Lottery Ticket Hypothesis": subset de parâmetros é essencial

---

## Por Que Pruning?

### Benefícios
1. **Model Size**: Redução significativa no tamanho do arquivo
2. **Inference Speed**: Pesos zerados = pass-through, menos computação
3. **Edge Deployment**: Viabiliza modelos grandes em dispositivos pequenos

### Trade-offs
- Accuracy vs Size
- Pruning ratio muito alto degrada performance
- Cada arquitetura responde diferente

---

## Tipos de Pruning

### Unstructured Pruning
- Remove pesos individuais
- Baseado em threshold de magnitude ou ativação
- Simples de implementar
- Pouco ganho de latência (cálculos ainda executados)
- Até 50% redução com <1% accuracy drop

### Structured Pruning
- Remove grupos inteiros de pesos (canais, layers, neurons)
- Reduz escala de cálculos no forward pass
- Ganho real de velocidade
- Mais preciso, mais complexo
- Pode ter consequências catastróficas se mal aplicado

---

## Escopos de Pruning

### Local Pruning
- Por camada/neuron individual
- Menos contexto global
- Mais seguro, menos impactante
- Exemplos: weight magnitude, unit magnitude, connection sensitivity

### Global Pruning
- Considera rede inteira
- Mais contexto para decisões
- Pode prejudicar layers específicas
- Exemplos: iterative magnitude pruning, optimal brain damage, optimal brain surgeon

---

## Quando Aplicar

### Train-Time Pruning
- Integrado no treinamento
- Regularização L1/L2
- Pruning masks na otimização
- Mais complexo, melhores resultados

### Post-Training Pruning
- Após modelo treinado
- Passo separado
- Mais simples de implementar
- Pode necessitar fine-tuning

---

## Resultados Empíricos

### Model Compression
- Redução linear com pruning ratio
- 90% pruning ≠ 90% size reduction (biases, activations não podados)
- Exemplos: DeepLabV3 MobileNetV3, UNet ResNet50, YOLOv8

### Inference Speed
- Redução de tempo com maior pruning
- Benefício real em structured pruning
- Crítico para aplicações real-time

### Accuracy Impact
- Alguns modelos retêm accuracy alta (DeepLabV3, UNet)
- Outros degradam rápido (YOLOv8x, YOLOv8s-seg)
- Trade-off individual por arquitetura

---

## Quando Usar Pruning

### Casos de Uso
1. **Edge Devices**: Smartphones, IoT, embedded
2. **Real-Time Apps**: Video analysis, autonomous vehicles
3. **Cloud Deployment**: Reduzir custos computacionais
4. **Multiple Models**: Múltiplos modelos no mesmo hardware

---

## Citações Importantes

> "Pruning generally is more surgical in compressing models than quantization, which bluntly removes precision from weights."

> "Structured pruning reduces the scale of calculations in forward pass, having real improvements for inference speed."

> "The Lottery Ticket Hypothesis demonstrates that networks have a specific subset of parameters essential for prediction."

---

## Conexões com Edge AI

Pruning é **técnica fundamental** para:
- Deploy em MCUs com flash/SRAM limitado
- Inferência real-time em edge
- Redução de consumo energético
- Viabilizar modelos grandes em dispositivos pequenos

### Relevância
- ★★★★★ Técnica essencial para edge ML
- Complementa quantização
- Depende de fine-tuning pós-pruning

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Técnica fundamental de compressão)