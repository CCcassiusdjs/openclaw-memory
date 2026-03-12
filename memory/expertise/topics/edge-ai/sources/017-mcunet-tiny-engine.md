# MCUNet: Tiny Deep Learning on IoT Devices

**Fonte:** MIT HAN Lab - NeurIPS 2020 (Spotlight)
**Link:** https://hanlab.mit.edu/projects/mcunet
**Tipo:** Research Paper

---

## Resumo Executivo

MCUNet é um framework de system-algorithm co-design que permite deep learning em microcontroladores com memória extremamente limitada. Primeira solução a alcançar >70% de acurácia no ImageNet em um MCU comercial.

---

## Problema Endereçado

Microcontroladores têm memória 2-3 ordens de magnitude menor que smartphones:
- SRAM: ~256KB (vs ~4GB em phones)
- Flash: ~1MB
- Desafio: Modelos DL não cabem na memória

---

## Arquitetura MCUNet

### Componentes
1. **TinyNAS**: Neural Architecture Search otimizado para restrições de memória
2. **TinyEngine**: Biblioteca de inferência memory-efficient

### Co-design
- TinyNAS e TinyEngine são co-designados
- Engine influencia a busca de arquitetura
- NAS considera limitações do engine

---

## TinyNAS (Neural Architecture Search)

### Abordagem Two-Stage
1. **Stage 1**: Otimiza search space para recursos disponíveis
2. **Stage 2**: Especializa arquitetura no search space otimizado

### Características
- Busca automática sob restrições (latência, energia, memória)
- Baixo custo computacional de busca
- Adapta arquitetura ao hardware específico

---

## TinyEngine (Inference Engine)

### Otimizações Principais
| Técnica | Benefício |
|---------|-----------|
| **In-place depth-wise conv** | Sobrescreve input, reduz SRAM |
| **Patch-based inference** | Opera em região pequena, 8x menos memória |
| **Operator fusion** | Elimina idas/vindas à memória |
| **SIMD programming** | Paralelismo de dados |
| **Loop unrolling/tiling** | Cache optimization |

### Comparação com Alternativas

| Engine | Speedup vs TF-Lite | Memory Reduction |
|--------|-------------------|------------------|
| TinyEngine | 1.7-3.3x | 3.4x |
| CMSIS-NN | - | - |
| TF-Lite Micro | baseline | baseline |

---

## Resultados Principais

### ImageNet no MCU
- **Primeiro a alcançar >70% top-1 accuracy** em MCU comercial
- 3.5x menos SRAM que MobileNetV2 quantizado
- 5.7x menos Flash que ResNet-18

### Visual Wake Words
- State-of-the-art accuracy
- 2.4-3.4x mais rápido que MobileNetV2
- 3.7-4.1x menor peak SRAM que ProxylessNAS

---

## Benchmarks (STM32H743)

### Latência (ms)
| Modelo | TF-Lite | CMSIS-NN | TinyEngine |
|--------|---------|----------|------------|
| mcunet-vww0 | 587 | 53 | **27** |
| mcunet-in0 | 586 | 51 | **25** |
| mcunet-in4 | OOM | OOM | **463** |

### Peak Memory (KB)
| Modelo | TF-Lite | CMSIS-NN | TinyEngine |
|--------|---------|----------|------------|
| mcunet-vww0 | 163 | 163 | **59** |
| mcunet-in0 | 161 | 69 | **49** |
| proxyless-w0.3 | 128 | 97 | **35** |

---

## MCUNetV2 (NeurIPS 2021)

### Inovação: Patch-based Inference
- Processa feature map patch por patch
- Reduz peak memory em 8x para MobileNetV2
- Permite modelos maiores no mesmo hardware

---

## MCUNetV3 (NeurIPS 2022)

### Inovação: On-Device Training
- Treino em dispositivo com <256KB memória
- Sparse updates para eficiência
- Tiny Training Engine para backpropagation

---

## Evolução do MCUNet

| Versão | Ano | Inovação |
|--------|-----|----------|
| MCUNet V1 | 2020 | TinyNAS + TinyEngine |
| MCUNet V2 | 2021 | Patch-based inference |
| MCUNet V3 | 2022 | On-device training |

---

## Aplicações Práticas

- Detecção de pessoas (person detection)
- Detecção de máscara facial
- Visual Wake Words
- ImageNet classification
- Audio wake words

---

## Código Aberto

- GitHub: mit-han-lab/tinyengine
- GitHub: mit-han-lab/mcunet
- Tutoriais de inference e training
- Modelos pré-treinados (Model Zoo)

---

## Citações Importantes

> "MCUNet is the first to achieve >70% ImageNet top1 accuracy on an off-the-shelf commercial microcontroller."

> "TinyEngine adapts the memory scheduling according to the overall network topology rather than layer-wise optimization."

> "The era of always-on tiny machine learning on IoT devices has arrived."

---

## Conexões com Edge AI

MCUNet representa o estado-da-arte em TinyML:
- Framework completo end-to-end
- System-algorithm co-design
- Performance real em hardware comercial
- Base para MCUNetV2 e V3

### Relevância
- ★★★★★ Fundamental para TinyML
- Framework de referência para deploy em MCUs
- Benchmarks reproduzíveis

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Framework TinyML de referência)