# MobileNetV3: Efficient Mobile Vision CNN

**Fonte:** EmergentMind, Howard et al. 2019
**Link:** https://www.emergentmind.com/topics/mobilenetv3
**Tipo:** Survey / Architecture Overview

---

## Resumo Executivo

MobileNetV3 é uma família de CNNs eficientes para visão em dispositivos móveis. Introduz hard-swish, SE modules, e usa NAS com otimização de latência real. Referência para deploy em edge.

---

## Arquitetura

### Building Blocks
- **Inverted Residual Blocks**: Expansão 1x1 → depthwise 3x3/5x5 → SE (opcional) → projeção linear
- **Squeeze-and-Excitation (SE)**: Com reduction ratio r=4, após depthwise conv
- **Hard-swish**: h-swish(x) = x × ReLU6(x+3)/6, eficiente para quantização

### Variantes
| Variante | Params | Top-1 ImageNet | Latência CPU |
|----------|--------|----------------|--------------|
| Large 1.0 | 5.4M | 75.2% | 51-61ms (Pixel) |
| Small | 2.5M | 67.4% | ~15-19ms |
| MoGA | 5.1M | 75.9% | 11.1ms (GPU) |

---

## Design Process

### Platform-Aware NAS
- Objetivo: R(m) = Acc(m) × [Lat(m)/T]^w
- Penaliza arquiteturas lentas
- Busca kernel sizes, expansion ratios, SE placement

### NetAdapt
- Refina canais pós-NAS
- Pruning iterativo por latência medida
- Precision no target de latência

---

## Resultados Benchmarks

### ImageNet
- **Large**: 75.2% top-1, 219M MACs
- **Small**: 67.4% top-1
- Melhorias vs V2: +3.2% accuracy, -18% latência

### Tiny ImageNet / CIFAR-10
- Small: 72.54% (Tiny ImageNet), 95.49% (CIFAR-10)
- Modelo < 8MB, inferência < 0.1ms em P100

---

## Extensões Práticas

### Coordinate Attention (CA)
- Substitui SE modules
- Preserva informação espacial
- Reduz params em 22%, melhora 0.92%

### Memristor-Based Deployment
- Implementação em hardware analógico
- CIFAR-10: 90.36% accuracy
- Latência: 1.24μs vs 165.4μs (GPU)
- Energia: ~0.2μJ vs 50μJ (GPU)

### Lite R-ASPP (Segmentação)
- Decoder compacto para semantic segmentation
- Cityscapes: 72.37% mIoU, 659ms CPU

---

## Quantization-Friendly Design

### Ativações
- **ReLU6**: Clipping em 6, ideal para INT8
- **Hard-swish**: Derivado de swish, quantizável
- **Hard-sigmoid**: Eficiente para mobile DSPs

### Pruning
- Channel pruning via NetAdapt
- Mantém accuracy com menos canais

---

## Comparação com Outros Modelos

| Modelo | Params | Top-1 | Size |
|--------|--------|-------|------|
| MobileNetV3-Small | 2.5M | 67.4% | ~8MB |
| EfficientNet-B0 | 5.3M | 77.1% | ~29MB |
| ResNet-18 | 11.7M | 69.8% | ~44MB |
| ShuffleNetV2 | 2.3M | 69.4% | ~9MB |

---

## Guidelines para Deploy

1. **Pretrained weights**: Transfer learning para datasets pequenos
2. **Quantização**: 8-bit ou 16-bit sem perda significativa
3. **Data augmentation**: Moderado (RandomCrop, Flip)
4. **Batch inference**: Amortiza overhead se latência não crítica
5. **Hardware**: Preferir platforms com depthwise conv nativo (ARM NN, SNPE, TPU)

---

## Aplicações Edge

- Classification
- Object Detection (SSD/YOLO backbone)
- Semantic Segmentation (LR-ASPP decoder)
- Transfer learning em domains específicos

---

## Citações Importantes

> "MobileNetV3 significantly advanced efficient neural architecture by explicitly incorporating hardware latency and platform-specific engineering into every phase of its design."

> "Hard-swish activation improves both quantization and implementational efficiency over standard swish."

---

## Conexões com Edge AI

MobileNetV3 é **backbone padrão** para:
- Detecção de objetos em mobile/edge
- Classificação eficiente em MCUs
- Base para transfer learning

### Relevância
- ★★★★★ Arquitetura de referência para edge
- Quantization-friendly por design
- Benchmarks extensivos

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Backbone padrão para edge)