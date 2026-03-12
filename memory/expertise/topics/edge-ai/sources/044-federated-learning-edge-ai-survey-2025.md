# Federated Learning for Edge AI: Comprehensive Survey (2025)

**Source:** https://www.preprints.org/manuscript/202512.0118
**Type:** Academic Survey (Preprints.org)
**Date:** December 2025
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

This comprehensive survey analyzes over 200 papers (2021-2025) on federated learning and Edge AI beyond centralized cloud computing. Covers cross-device, cross-silo, edge-only, decentralized, and split/hybrid designs with a unified system-of-systems perspective.

## Key Concepts

### Four Limitations of Cloud-Centric AI

1. **Latency** - Round-trip times incompatible with interactive/safety-critical applications (AR/VR, autonomous vehicles, industrial control)
2. **Bandwidth** - Expensive data uploads from massive device fleets
3. **Privacy & Regulation** - GDPR, HIPAA restrictions on cross-border data movement
4. **Robustness & Sustainability** - Single points of failure, carbon footprint concerns

### Edge AI Paradigms

| Paradigm | Focus | Key Benefit |
|----------|-------|-------------|
| **Edge AI** | Inference/training at edge | Low latency, reduced bandwidth |
| **Federated Learning** | Privacy-preserving collaboration | Data residency, no raw data sharing |
| **Federated Edge AI** | Combined approach | Privacy + performance + resource-aware |

### FL Architecture Taxonomy

1. **Centralized FL** - Single aggregator coordinating all clients
2. **Hierarchical/Multi-tier FL** - Device→edge→cloud hierarchy
3. **Edge-only/On-premise FL** - Hospital, factory, critical infrastructure
4. **Decentralized FL** - Gossip protocols, blockchain-enabled
5. **Split/Hybrid FL** - Model partitioning with edge backbones

### Cross-Layer Challenges

| Challenge | Description | Key Techniques |
|------------|-------------|---------------|
| **Statistical Heterogeneity** | Non-IID data distributions | Personalization, cluster FL, meta-learning |
| **System Heterogeneity** | Variable device capabilities | Client selection, resource-aware aggregation |
| **Stragglers** | Slow/failing clients | Async FL, staleness tolerance |
| **Communication Efficiency** | Bandwidth constraints | Compression, quantization, periodic averaging |
| **Energy Efficiency** | Battery constraints | Green FL, adaptive participation |
| **Privacy & Security** | Data/model attacks | Differential privacy, secure aggregation |
| **Trust & Byzantine Resilience** | Malicious participants | Robust aggregation, validation mechanisms |

### Hardware & Software Enablers

**Hardware:**
- Edge GPUs (NVIDIA Jetson)
- NPUs (Neural Processing Units)
- TPUs at edge
- Neuromorphic processors
- Processing-in-Memory (PIM)

**Software Frameworks:**
- TensorFlow Federated
- Flower
- FedML
- FATE
- OpenFL
- TinyFL

### Application Domains

1. **Healthcare & Wearables** - Privacy-preserving medical diagnosis
2. **Intelligent Transportation** - V2X collaboration, traffic optimization
3. **Industrial IoT** - Predictive maintenance, quality control
4. **Smart Cities** - Infrastructure monitoring, public safety

## Future Directions

### Federated Continual Learning
- Models that adapt over time without catastrophic forgetting
- Knowledge retention across federated rounds
- Lifelong learning on edge devices

### Foundation Models at Edge
- On-device adaptation of large language models
- Parameter-efficient fine-tuning (PEFT)
- LoRA, adapters, prompt tuning

### Green and Trustworthy FL
- Carbon-aware training schedules
- Energy-efficient aggregation
- Verifiable computation

### TinyML + FL Convergence
- Microcontroller-class federated learning
- Integer-only inference
- Aggressive quantization for ultra-constrained devices

## Key Takeaways

1. **Beyond Cloud** - Edge AI + FL addresses latency, bandwidth, privacy, resilience
2. **Architecture Choice** - Trade-offs between centralization, trust, and complexity
3. **Heterogeneity is Core** - Both statistical and system heterogeneity must be addressed
4. **Hardware Matters** - Accelerators and TinyML platforms enable practical deployment
5. **Applications Drive Design** - Healthcare, transportation, industrial have distinct requirements

## Related Topics

- Split computing for DNN inference
- TinyML deployment patterns
- Secure aggregation protocols
- Personalized federated learning