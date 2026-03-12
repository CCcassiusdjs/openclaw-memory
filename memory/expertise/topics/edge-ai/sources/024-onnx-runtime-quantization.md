# ONNX Runtime Quantization

**Fonte:** ONNX Runtime Documentation
**Link:** https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html
**Tipo:** Documentation

---

## Resumo Executivo

ONNX Runtime fornece APIs para quantização de modelos ONNX de FP32 para INT8/UINT8. Suporta dynamic quantization, static quantization, e é compatível com QAT.

---

## Tipos de Quantização

### Dynamic Quantization
- Calcula scale e zero_point para ativações **dinamicamente** durante inferência
- Maior accuracy, mas overhead computacional
- Recomendado para: RNNs, Transformers
- API: `quantize_dynamic()`

### Static Quantization
- Calcula parâmetros **offline** com calibration data
- Parâmetros escritos como constantes no modelo
- Recomendado para: CNNs
- API: `quantize_static()`
- Métodos de calibração: MinMax, Entropy, Percentile

---

## Formatos de Representação

### QOperator
- Operadores quantizados têm definições próprias
- Exemplos: QLinearConv, MatMulInteger
- Formato operator-oriented

### QDQ (Quantize-DeQuantize)
- Insere DeQuantizeLinear(QuantizeLinear(tensor))
- Simula processo de quantização/dequantização
- Formato tensor-oriented
- Compatível com QAT do PyTorch/TensorFlow

---

## Fórmula de Quantização

```
val_fp32 = scale * (val_quantized - zero_point)
```

### Asymmetric Quantization
```
scale = (data_range_max - data_range_min) / (quant_range_max - quant_range_min)
```

### Symmetric Quantization
```
scale = max(|data_range_max|, |data_range_min|) * 2 / (quant_range_max - quant_range_min)
```

---

## Data Types

| Formato | Ativações | Pesos | Notas |
|---------|-----------|-------|-------|
| U8U8 | uint8 | uint8 | Use se S8S8 tiver accuracy issues |
| U8S8 | uint8 | int8 | Performance em x86 com AVX2 |
| S8S8 | int8 | int8 | **Default**, melhor balanço |

---

## Pre-processing

Antes de quantizar:
1. **Symbolic shape inference** (transformers)
2. **Model optimization** (fusion, redundancy elimination)
3. **ONNX shape inference**

Importante: Otimização durante quantização dificulta debugging. Fazer na pre-processing.

---

## Quantization Debugging

API para comparar tensors FP32 vs quantizado:
- `create_weight_matching()`: Match pesos
- `modify_model_output_intermediate_tensors()`: Augmentar para salvar ativações
- `collect_activations()`: Coletar ativações
- `create_activation_matching()`: Match ativações

---

## GPU Quantization

### Requisitos
- Hardware com Tensor Core INT8 (T4, A100)
- TensorRT Execution Provider

### Pipeline
1. Implementar CalibrationDataReader
2. Calcular parâmetros de quantização
3. Salvar em flatbuffer
4. Rodar com TensorRT EP

---

## Transformer Models

- Otimizações específicas para attention layers
- QAttention para quantização de attention
- Usar Transformer Model Optimization Tool antes de quantizar

---

## Exemplos de Uso

### Dynamic Quantization
```python
from onnxruntime.quantization import quantize_dynamic, QuantType

model_fp32 = 'model.onnx'
model_quant = 'model.quant.onnx'
quantized_model = quantize_dynamic(model_fp32, model_quant, weight_type=QuantType.QUInt8)
```

### Static Quantization
```python
from onnxruntime.quantization import quantize_static

# Define calibration data reader
quantize_static(model_fp32, model_quant, calibration_data_reader)
```

---

## Method Selection

| Modelo | Recomendação |
|--------|--------------|
| RNNs | Dynamic quantization |
| Transformers | Dynamic quantization |
| CNNs | Static quantization |
| QAT needed | Re-treinar no framework original |

---

## Citações Importantes

> "Dynamic quantization calculates scale and zero point for activations dynamically. These calculations increase inference cost, but usually achieve higher accuracy."

> "S8S8 with QDQ is the default setting and balances performance and accuracy."

---

## Conexões com Edge AI

ONNX Runtime Quantization é **ferramenta essencial** para:
- Deploy de modelos em edge devices
- Redução de tamanho de modelo
- Aceleração de inferência em CPU/GPU
- Pipeline de otimização cross-platform

### Relevância
- ★★★★★ Ferramenta padrão para quantização ONNX
- Suporta QDQ e QOperator
- Compatível com PyTorch, TensorFlow, TensorRT

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Ferramenta padrão para quantização)