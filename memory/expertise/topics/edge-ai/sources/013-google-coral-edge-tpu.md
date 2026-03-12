# Google Coral Edge TPU: Model Quantization & Compilation

**Source:** Google Coral Documentation, GitHub Issues
**Year:** 2024-2025
**Category:** Edge Hardware & Compilation
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for Edge TPU deployment)

---

## Summary

Google Coral Edge TPU is a specialized hardware accelerator for TensorFlow Lite models. Models must be quantized to INT8/UINT8 for Edge TPU acceleration. This covers the compilation and quantization requirements.

---

## Edge TPU Requirements

### Quantization Requirements

| Requirement | Description |
|-------------|-------------|
| **Tensor Parameters** | Must be quantized (8-bit fixed-point: INT8 or UINT8) |
| **Operations** | Must use TFLITE_BUILTINS_INT8 operations |
| **Input Type** | UINT8 or INT8 (configurable) |
| **Output Type** | UINT8 or INT8 (configurable) |

### Model Compatibility

- Only quantized models can use Edge TPU acceleration
- Post-training full integer quantization required
- Some operations may not be supported (check compatibility)

---

## Quantization Process

### Full Integer Quantization Code

```python
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

# Enable default optimizations
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Provide representative dataset for calibration
converter.representative_dataset = representative_dataset

# Force integer-only operations
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]

# Set input/output types for integer-only inference
converter.inference_input_type = tf.uint8  # or tf.int8
converter.inference_output_type = tf.uint8  # or tf.int8

tflite_quant_model = converter.convert()
```

### Key Parameters

| Parameter | Purpose |
|-----------|---------|
| `Optimize.DEFAULT` | Enable post-training quantization |
| `representative_dataset` | Calibration data for range estimation |
| `TFLITE_BUILTINS_INT8` | Force integer-only operations |
| `inference_input_type` | Input tensor type (uint8/int8) |
| `inference_output_type` | Output tensor type (uint8/int8) |

---

## Edge TPU Compiler

### Compilation Process

```
TensorFlow Model → TFLite Converter → Quantized TFLite → Edge TPU Compiler → Edge TPU Model
```

### Compiler Usage

```bash
edgetpu_compiler model.tflite
```

### Compiler Requirements

- Model must be fully quantized
- All operations must have integer versions
- Some operations may not compile (check logs)

---

## Supported Operations

### Commonly Supported

- Conv2D, DepthwiseConv2D
- FullyConnected (Dense)
- MaxPool, AveragePool
- ReLU, ReLU6
- Softmax
- Add, Sub, Mul, Div
- Reshape, Transpose

### Potentially Unsupported

- Transpose convolution (limited support)
- Some LSTM operations
- Custom operations
- Non-quantizable operations

---

## Edge TPU Python API

### Input Requirements

| Requirement | Description |
|-------------|-------------|
| **Input Format** | UINT8 tensors |
| **API Version** | Requires uint8 input data |
| **Converter** | TensorFlow Lite Converter v2 |

---

## Common Issues

### 1. "Model not quantized" Error

**Cause:** Model not fully quantized to INT8
**Solution:** Ensure full integer quantization with representative dataset

### 2. "Operation not supported" Error

**Cause:** Operation doesn't have integer version
**Solution:** Replace with supported operation or use CPU fallback

### 3. Input Type Mismatch

**Cause:** API expects uint8, model uses float
**Solution:** Set `inference_input_type = tf.uint8`

---

## Performance Considerations

| Metric | Edge TPU | CPU |
|--------|----------|-----|
| **Latency** | Sub-millisecond | Milliseconds |
| **Power** | ~2W | Variable |
| **Throughput** | High | Moderate |
| **Precision** | INT8 | FP32 |

---

## Workflow for Edge TPU Deployment

```
1. Train model in TensorFlow/Keras
2. Export to SavedModel format
3. Convert to TFLite with full integer quantization
4. Compile with Edge TPU Compiler
5. Deploy to Coral device
6. Run inference with Edge TPU Python API
```

---

## Key Insights

1. **Quantization is mandatory:** Edge TPU requires INT8/UINT8
2. **Calibration data matters:** Use representative dataset for quantization
3. **Not all operations supported:** Check compatibility before deployment
4. **Input/output types:** Must match API expectations
5. **Compiler validates:** Edge TPU Compiler catches unsupported operations

---

## Next Steps

- [ ] Convert a MobileNet model for Edge TPU
- [ ] Test Edge TPU vs CPU inference speed
- [ ] Explore model compatibility database
- [ ] Study quantization-aware training for Edge TPU