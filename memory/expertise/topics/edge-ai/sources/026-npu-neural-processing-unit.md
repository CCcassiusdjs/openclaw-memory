# NPU: Neural Processing Unit

**Fonte:** Wikipedia, Gateworks
**Link:** https://en.wikipedia.org/wiki/Neural_processing_unit
**Tipo:** Reference / Technical Overview

---

## Resumo Executivo

NPU (Neural Processing Unit) é um hardware accelerator especializado para ML/AI. Projetado para operações de baixa precisão (INT4, INT8, FP8, FP16) com alta eficiência energética. Diferente de GPUs, NPUs são manycore/spatial designs otimizados para inferência.

---

## Definição

- **Nome**: Neural Processing Unit / AI Accelerator / Deep Learning Processor
- **Propósito**: Acelerar aplicações de ML/AI (inference e/ou training)
- **Design**: Manycore/spatial architectures, low-precision arithmetic, dataflow ou in-memory computing

---

## Características

### Arquitetura
- Manycore processors
- Spatial architecture
- Low-precision arithmetic (INT4, INT8, FP8, FP16)
- Dataflow architectures
- In-memory computing capability

### Métrica de Performance
- **TOPS**: Trillions of Operations Per Second
- Tipicamente INT8 additions/multiplications
- Exemplo: Hailo AI = 26 TOPS

---

## NPUs em Dispositivos

### Mobile Devices
- Apple iPhone (Neural Engine)
- Google Pixel (Tensor SoC)
- Samsung Exynos
- Qualcomm Snapdragon

### Desktop/Laptop
- Apple Silicon (Neural Engine)
- Intel Meteor Lake (VPU)
- AMD Ryzen AI (XDNA)

### Embedded/Edge
- NXP i.MX 8M Plus (NPU integrado)
- Hailo AI (M.2 card)
- Google Coral Edge TPU

---

## Comparação NPU vs CPU/GPU

| Aspecto | CPU | GPU | NPU |
|---------|-----|-----|-----|
| Precision | FP32/FP64 | FP16/FP32 | INT8/FP8 |
| Efficiency | Baixa | Média | Alta |
| Flexibility | Alta | Média | Baixa |
| Use Case | General | Graphics/Parallel | ML Inference |

---

## APIs e Software

### Framework APIs
- TensorFlow Lite with LiteRT Next (Android)
- CoreML (iOS, macOS)
- ONNX Runtime

### Vendor APIs
- AMD: Ryzen AI
- Intel: OpenVINO
- Apple: CoreML
- Qualcomm: SNPE

---

## NPU em Edge AI

### Casos de Uso
- Real-time object detection
- Speech recognition
- Anomaly detection
- Image classification
- Voice command processing

### Vantagens
- Baixo consumo energético
- Baixa latência
- Privacidade (processamento local)
- Funciona offline

### Limitações
- Menos flexível que CPU
- Treinamento geralmente em cloud
- Modelo precisa ser otimizado (quantização)

---

## Exemplo: NXP i.MX 8M Plus

- NPU integrado no SoC
- 53x mais rápido que CPU para ML inference
- Gateworks Venice SBCs
- Suporte a Python e GStreamer

---

## Exemplo: Hailo AI

- M.2 form factor
- 26 TOPS
- Mini-PCIe card
- Compatible with embedded SBCs

---

## Citações Importantes

> "NPUs handle AI tasks much more efficiently than general-purpose processors by executing specific AI operations faster and more effectively."

> "TOPS does not explicitly specify the kind of operations, it is typically INT8 additions and multiplications."

---

## Conexões com Edge AI

NPU é **hardware essencial** para:
- Inferência eficiente em edge devices
- Baixa latência para aplicações real-time
- Privacidade com processamento local
- Baixo consumo energético para IoT

### Relevância
- ★★★★★ Hardware fundamental para Edge AI
- Integração com SoCs para embedded
- APIs vendor-specific para otimização

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Hardware core para Edge AI)