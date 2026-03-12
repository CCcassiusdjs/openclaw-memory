# TPU: Tensor Processing Unit & Edge TPU

**Fonte:** Gateworks, Google Coral, Wikipedia
**Link:** https://www.gateworks.com/choosing-the-right-ai-accelerator-npu-or-tpu-for-edge-and-cloud-applications/
**Tipo:** Technical Overview

---

## Resumo Executivo

TPU (Tensor Processing Unit) é um hardware accelerator desenvolvido pelo Google para acelerar workloads de TensorFlow. Usa 8-bit integers para computação rápida e systolic arrays para matrix multiplication. Edge TPU é a versão para dispositivos edge com 4 TOPS.

---

## O Que é TPU

### Definição
- Hardware accelerator do Google
- Otimizado para TensorFlow
- Usa lower precision 8-bit integers
- Systolic arrays para matrix operations
- Bom para deep learning training e inference

### Cloud TPU vs Edge TPU

| Aspecto | Cloud TPU | Edge TPU |
|---------|-----------|----------|
| Potência | High-power | Low-power |
| Uso | Training, large-scale inference | Inference only |
| TOPS | Muito alto | 4 TOPS |
| Formato | Cloud/Server | USB/M.2/SoM |

---

## Edge TPU (Google Coral)

### Especificações
- **Performance**: 4 TOPS
- **Power**: 2 watts
- **Efficiency**: 2 TOPS/watt
- **Precision**: INT8 fixed-point
- **Interface**: USB 2.0, PCIe, M.2

### Form Factors
- USB Accelerator
- M.2 module
- System-on-Module (SoM)
- Dev Board

### Software
- TensorFlow Lite models
- Compiled for Edge TPU
- Coral SDK

---

## Casos de Uso

### Cloud TPU
- Large-scale model training
- Video/image processing
- Deep learning research
- Batch inference

### Edge TPU
- Real-time object detection
- Image classification
- Smart cameras
- Drones
- Robotics
- Industrial IoT

---

## NPU vs TPU

| Critério | NPU | TPU |
|----------|-----|-----|
| Best For | Real-time inference edge | Deep learning cloud |
| Power Efficiency | Excellent (battery-powered) | Moderate |
| Use Case | Classification, speech, anomaly | Large-scale training |
| Performance | Low-latency real-time | High throughput |
| Ecosystem | TensorFlow, PyTorch, etc. | TensorFlow primarily |
| Integration | SoCs (NXP, etc.) | Standalone cards/cloud |

---

## Google Coral Ecosystem

### Produtos
- Coral USB Accelerator
- Coral Dev Board
- Coral System-on-Module
- M.2 Accelerator

### Workflow
1. Train model in TensorFlow/Keras
2. Convert to TensorFlow Lite
3. Compile for Edge TPU
4. Deploy on Coral device

---

## Benchmarks Edge TPU

### Image Classification
- MobileNet V2: ~7ms inference
- EfficientNet: ~10ms inference
- Inception V3: ~15ms inference

### Object Detection
- MobileNet SSD: ~12ms inference
- EfficientDet: ~20ms inference

### Note
- Benchmarks variam por modelo e input size
- Pre-compiled models disponíveis no Coral Model Zoo

---

## Vantagens

### Edge TPU
- Baixo consumo (2W)
- Alta eficiência (2 TOPS/watt)
- Privacidade (inference local)
- Baixa latência
- Funciona offline

### Cloud TPU
- Escalabilidade
- Alta performance
- Integrado com Google Cloud
- Ideal para training

---

## Limitações

### Edge TPU
- Inference only (não treina)
- TensorFlow Lite only
- Modelo precisa ser compilado
- Operações limitadas suportadas

### Cloud TPU
- Alto custo
- Vendor lock-in (Google)
- Power consumption

---

## Citações Importantes

> "Edge TPU can perform 4 trillion (fixed-point) operations per second (4 TOPS), using only 2 watts of power."

> "TPUs leverage systolic arrays, providing high-performance matrix multiplication operations."

---

## Conexões com Edge AI

Edge TPU é **plataforma de referência** para:
- Inferência TensorFlow Lite em edge
- Smart cameras e IoT
- Drones e robotics
- Aplicações com restrição de energia

### Relevância
- ★★★★☆ Plataforma Google para Edge AI
- Alternativa a NPUs vendors-specific
- Ecosystem completo (hardware + software)

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★☆ (Hardware Google para Edge AI)