# Edge AI: Evaluation of Model Compression Techniques for CNNs

**Source:** arXiv (2409.02134v1)
**Authors:** Samer Francy, Raghubir Singh (University of Bath)
**Year:** 2024
**Category:** Model Compression Survey
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for understanding compression techniques)

---

## Summary

This paper evaluates model compression techniques on ConvNeXt models for image classification using CIFAR-10. It compares structured pruning, unstructured pruning, and dynamic quantization methods for reducing model size and computational complexity while maintaining accuracy.

---

## Key Concepts

### Edge AI Overview
- **IoT Architecture:** 3 layers (Perceptual → Network → Application)
- **Advantages of Edge AI:**
  - Low latency (real-time processing)
  - Privacy and data security (no cloud transmission)
  - Bandwidth optimization
  - Reduced network dependence

### CNN Architecture Components
1. **Input Image:** Pixel-based representation
2. **Convolutional Layer:** Feature extraction using sliding filters (3x3, 5x5)
3. **Pooling Layer:** Spatial reduction (max/average pooling)
4. **Activation Function:** Non-linear transformation (ReLU)
5. **Fully Connected Layer:** Classification

### Resource Imbalance in CNNs
- **Convolutional Layers:** 2M params, 1.33 GOPS (compute-heavy)
- **Fully Connected Layers:** 59M params, 0.12 GOPS (memory-heavy)
- This imbalance drives different compression strategies

### CNN Applications on Edge
| Domain | Models Used | Use Case |
|--------|------------|----------|
| Surveillance | VGGFace, YOLOX, DenseNet | Facial recognition, video analysis |
| Manufacturing | Faster R-CNN | Defect detection |
| Agriculture | GoogLeNet, YOLOX | Disease/pest detection |
| Healthcare | VGG, MobileNet, ResNet | Medical diagnosis |
| Autonomous Vehicles | AlexNet, Faster R-CNN | Object detection, ADAS |

---

## Compression Techniques Evaluated

### 1. Structured Pruning
- Removes entire channels/filters
- **Result:** Up to 75% model size reduction
- Maintains accuracy with fine-tuning

### 2. Unstructured Pruning
- Removes individual weights
- Higher compression but less hardware-friendly
- Limited reduction in computational complexity

### 3. Dynamic Quantization
- Reduces precision of weights/activations
- **Result:** Up to 95% parameter reduction
- Best when combined with pruning

### 4. Combined: OTOV3 Pruning + Quantization
- **Results:**
  - 89.7% size reduction
  - 95% reduction in parameters and MACs
  - 3.8% accuracy increase (after fine-tuning)
  - Edge deployment: 92.5% accuracy, 20ms inference time

---

## Key Findings

1. **Fine-tuning improves compression** - Pre-trained models compress better
2. **Structured pruning is hardware-friendly** - Better for edge deployment
3. **Combination techniques work best** - Pruning + quantization synergy
4. **Edge deployment is viable** - Demonstrated on actual hardware

---

## Practical Implications

- For edge deployment: Use structured pruning + dynamic quantization
- Always fine-tune after compression
- ConvNeXt models respond well to compression
- 20ms inference time achievable on edge devices

---

## Related Work Referenced

- CNN evolution from LeCun (1989) to modern architectures
- VGG, ResNet, DenseNet, MobileNet families
- YOLO for real-time object detection

---

## Next Steps

- [ ] Read original OTOV3 paper for pruning details
- [ ] Compare with TensorFlow Lite quantization
- [ ] Study ONNX Runtime optimizations