# Neural Architecture Search para TinyML

**Fonte:** embedUR + MIT HAN Lab
**Link:** https://www.embedur.ai/optimizing-tinyml-with-neural-architecture-search-a-practical-guide-for-edge-ai/
**Tipo:** Technical Guide

---

## Resumo Executivo

NAS otimiza automaticamente arquiteturas para dispositivos edge. Para TinyML, NAS considera memória, latência e energia como constraints, não apenas accuracy.

---

## Frameworks NAS para TinyML

### TinyTNAS (Aug 2024)
- **Foco**: Desenvolvedores com recursos limitados
- **Algoritmo**: Evolutionary algorithms
- **Constraints**: Flash, SRAM, computational load
- **Performance**: 50 iterações em 10 min (Intel i7, sem GPU)
- **Resultado**: 93.1% F-score em MIT-BIH, 82 kB Flash
- **Melhoria**: 12x sobre modelos manuais
- **Output**: .tflite files (TF Lite Micro ready)

### μNAS (Mar 2025)
- **Foco**: Deployments de extrema baixa memória
- **Algoritmo**: Evolutionary + Bayesian optimization
- **Memory**: Peak SRAM < 64 kB
- **Resultado**: 95.4% accuracy em keyword spotting
- **Hardware**: Cortex-M4, 64 kB RAM, 12 ms execução
- **Integração**: TFLite Micro + CMSIS-NN

### Once-For-All (OFA) + CompOFA
- **Conceito**: Super-network pré-treinada
- **Extração**: Subnetworks otimizadas para hardware específico
- **Resultado**: 89.4% CIFAR-100 em ARM Cortex-M7
- **Latência**: 34 ms, 2x mais rápido que MobileNetV2
- **Pipeline**: PyTorch → ONNX → microTVM ou TFLite

### ProxylessNAS-MCU
- **Inovação**: Search-on-device
- **Método**: Busca no próprio microcontrolador
- **Métricas**: Latência real e consumo energético
- **Benefício**: 3.6x redução de SRAM + melhor accuracy
- **Uso**: Produção-ready, confiabilidade

### NATS-Bench (Micro-NAS Benchmark)
- **Catálogo**: 48,000+ arquiteturas pré-testadas
- **Uso**: Prototipagem rápida, pesquisa
- **Flash**: Top modelos < 200 kB
- **Benefício**: Elimina ciclos de treinamento

---

## Comparação de Frameworks

| Framework | Método | SRAM Target | Flash Target | Use Case |
|-----------|--------|-------------|--------------|----------|
| TinyTNAS | Evolutionary | Flexible | < 100 kB | Rapid prototype |
| μNAS | Evo + Bayesian | < 64 kB | < 200 kB | Extreme memory |
| OFA | Super-network | Flexible | Flexible | Multi-hardware |
| ProxylessNAS | On-device | Minimized | Optimized | Production |
| NATS-Bench | Benchmark | Varies | < 200 kB | Research |

---

## Pipeline de Deploy

### Design Flow
1. **Definir constraints**: SRAM, Flash, latência, energia
2. **Selecionar framework**: Baseado no hardware alvo
3. **Executar NAS**: Busca automática
4. **Exportar modelo**: TFLite/ONNX
5. **Otimizar backend**: CMSIS-NN, TinyEngine
6. **Deploy**: MCU target

### Integrações
- TensorFlow Lite Micro
- microTVM (TVM para MCUs)
- CMSIS-NN (backend otimizado)
- TinyEngine (MCUNet)

---

## Benefícios do NAS

### Otimização Multi-Objetivo
- Accuracy **and** latency
- Memory **and** energy
- Flash **and** SRAM

### vs Design Manual
- Explora espaço de design maior
- Encontra soluções não-óbvias
- Reduz tempo de desenvolvimento
- Melhora eficiência (até 12x)

---

## Casos de Uso

### Keyword Spotting
- μNAS: 95.4% accuracy, 64 kB RAM, 12 ms
- Aplicação: Voice assistants, wake words

### Image Classification
- OFA: 89.4% CIFAR-100, Cortex-M7, 34 ms
- Aplicação: Object detection, classification

### Anomaly Detection
- TinyTNAS: MIT-BIH arrhythmia detection
- Aplicação: Healthcare, industrial monitoring

---

## Citações Importantes

> "TinyTNAS achieves 93.1% F-score on MIT-BIH using 82 kB Flash, a 12-fold improvement over manually designed models."

> "μNAS delivered 95.4% accuracy in keyword spotting using just 64 kB RAM, executing in only 12 ms."

> "NAS allows for the optimization of multiple objectives simultaneously: accuracy, latency, and model size."

---

## Conexões com Edge AI

NAS para TinyML é **essencial** para:
- Otimização automática de arquiteturas
- Design para hardware específico
- Trade-offs accuracy vs resources
- Redução de tempo de desenvolvimento

### Relevância
- ★★★★★ Técnica fundamental para Edge AI
- Automatiza o que seria meses de design manual
- Frameworks maduros e prontos para deploy

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (NAS para Edge AI)