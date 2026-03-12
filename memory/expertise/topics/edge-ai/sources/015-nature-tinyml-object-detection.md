# Deploying TinyML for Energy-Efficient Object Detection in Low-Power Edge AI Systems

**Fonte:** Nature Scientific Reports, 2025
**Link:** https://www.nature.com/articles/s41598-025-27818-9
**Tipo:** Research Paper

---

## Resumo Executivo

Este paper propõe um framework end-to-end para deploy de detecção de objetos em tempo real em MCUs de baixo consumo. Combina MobileNetV2 quantizado com comunicação TCP/UDP adaptativa.

---

## Problema Endereçado

Deploy de modelos de visão computacional em MCUs com:
- 256 KB SRAM
- 1 MB Flash
- ~64 MHz CPU
- < 1mW consumo

---

## Metodologia

### Dataset
- **Visual Wake Words (VWW)**: Detecção binária de presença humana
- ~115K imagens treino, 8K validação
- Subset balanceado: 20K treino, 4K valid, 1K teste

### Hardware
- MCU ARM Cortex-M4 @ 64MHz
- 256 KB SRAM
- 1 MB Flash
- 3.3V operação
- Câmera integrada

### Arquitetura
- **MobileNetV2** com width multiplier ajustável
- Input resolutions: 96x96, 160x160, 224x224
- Transfer learning do ImageNet

---

## Técnicas de Compressão Avaliadas

| Técnica | Resultado |
|---------|-----------|
| **8-bit Quantization** | ✅ Mais efetiva - 3-4x redução tamanho, mínima perda |
| **Pruning** | ⚠️ Benefícios limitados em MCUs restritos |
| **Knowledge Distillation** | ⚠️ Melhorias mínimas em accuracy/eficiência |

### Quantização
- Post-training quantization
- Float32 → Int8
- Redução 3-4x no tamanho
- Perda mínima de acurácia
- framework: TensorFlow Lite Micro

---

## Resultados Principais

### Trade-offs Identificados
1. **Resolução vs Memória**: Imagens menores reduzem footprint mas impactam acurácia
2. **Width Multiplier**: Menos filtros = menos memória, menos acurácia
3. **Latência vs Confiabilidade**: TCP confiável, UDP baixa latência

### Métricas em MCU
- Modelo quantizado: ~300KB Flash
- Inferência: <100ms
- Energia: proporcional à complexidade do modelo
- Memória SRAM: ~100KB runtime

---

## Framework de Deploy

```
[Camera] → [MCU + MobileNetV2 Quantized] → [TCP/UDP] → [Host]
                                        ↓
                              Detecção Local
                              (sem cloud)
```

### Comunicação Dual-Mode
- **TCP**: Confiabilidade garantida (aplicações críticas)
- **UDP**: Baixa latência (aplicações tempo real)

---

## TensorFlow Lite Micro

Pipeline de deploy:
1. Treinar MobileNetV2 com transfer learning
2. Aplicar 8-bit quantization
3. Converter para .tflite
4. Compilar para MCU específico
5. Deploy + monitoramento

---

## Lições Aprendidas

### O Que Funciona
- Quantização Int8 é essencial para MCU deploy
- Transfer learning acelera desenvolvimento
- Input resolution 160x160 é sweet spot
- VWW dataset adequado para benchmarks

### O Que Não Funciona
- Pruning estruturado tem ganhos marginais
- Knowledge distillation não compensa overhead
- Modelos sem otimização excedem memória MCU

---

## Conexões com Edge AI

Este paper demonstra:
1. **Viabilidade prática** de TinyML em produção
2. **Framework reproduzível** end-to-end
3. **Métricas reais** de energia e latência
4. **Abordagem sistemática** de otimização

### Aplicabilidade
- Smart home (presença humana)
- Segurança (vigilância)
- Industrial (detecção de anomalias)
- Wearables (reconhecimento visual)

---

## Limitações do Paper
- Não compara com MCUNet ou MobileNetV3
- Não usa quantization-aware training (QAT)
- Dataset VWW é simplificado (binary classification)

---

## Citações Importantes

> "8-bit post-training quantization proved most effective, reducing model size by 3-4x while maintaining minimal accuracy loss."

> "Pruning and knowledge distillation demonstrate limited benefits under stringent memory and energy constraints."

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Framework prático de deploy TinyML)