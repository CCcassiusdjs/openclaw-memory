# Federated Learning Architectures for Privacy-Preserving AI

**Source:** MDPI Electronics (2025)
**Authors:** Zhan, Huang, Luo, Zheng, Gao, Chao
**Year:** 2025
**Category:** Federated Learning Survey
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for privacy-preserving edge AI)

---

## Summary

Comprehensive review of federated learning (FL) architectures for cloud-edge-end collaboration. Addresses privacy preservation, device heterogeneity, communication constraints, and security threats in resource-constrained environments.

---

## Key Concept: Cloud-Edge-End Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        CLOUD                            │
│     Large-scale compute & storage                      │
│     Complex model training                              │
│     Massive data analysis                               │
└─────────────────────────┬───────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     EDGE        │ │     EDGE        │ │     EDGE        │
│  Base stations  │ │  Roadside units │ │  Micro data ctrs│
│  Low latency    │ │  Real-time srv  │ │  Flexible deploy │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│      END        │ │      END        │ │      END        │
│  IoT sensors    │ │  Wearables      │ │  Smart vehicles │
│  Lightweight AI │ │  Edge inference │ │  Local training │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Layer Definitions

| Layer | Role | Resources | Use Case |
|-------|------|-----------|----------|
| **Cloud** | Central intelligence | Massive compute/storage | Complex training, big data |
| **Edge** | Regional processing | Limited but flexible | Low-latency services |
| **End** | Data collection | Minimal resources | Lightweight AI, sensing |

---

## Federated Learning Fundamentals

### What is FL?

> "Collaborative training of ML models without transferring raw data to a central server."

### Key Properties

1. **Data Privacy:** Raw data stays local
2. **Distributed Training:** Model updates aggregated centrally
3. **Collaborative Learning:** Multiple participants improve model together
4. **Heterogeneous Support:** Works with different devices/data

### FL Training Cycle

```
1. Initialize global model on server
2. Distribute model to clients
3. Each client trains locally on private data
4. Clients send model updates (not data) to server
5. Server aggregates updates (FedAvg, etc.)
6. Repeat until convergence
```

---

## Technical Challenges

### 1. Data Heterogeneity (Non-IID)

| Challenge | Impact |
|-----------|--------|
| Non-IID data distribution | Model divergence |
| Unbalanced data volume | Bias toward large clients |
| Concept drift | Model outdated locally |

### 2. Device Heterogeneity

| Challenge | Impact |
|-----------|--------|
| Variable compute power | Stragglers |
| Different memory sizes | Model size limits |
| Intermittent connectivity | Training interruptions |

### 3. Communication Constraints

| Challenge | Impact |
|-----------|--------|
| Bandwidth limitations | Slow convergence |
| Unreliable networks | Lost updates |
| Latency variation | Asynchronous issues |

### 4. Security Threats

| Threat | Description |
|--------|-------------|
| Model poisoning | Malicious updates |
| Data poisoning | Corrupted local data |
| Inference attacks | Reconstruct training data |
| Byzantine clients | Arbitrary behavior |

---

## Trustworthy AI Pillars

### 1. Robustness
- Handle adversarial attacks
- Tolerate noisy data
- Resist model poisoning

### 2. Fairness
- Equitable treatment across clients
- Avoid bias toward large participants
- Handle imbalanced participation

### 3. Explainability
- Understand model decisions
- Interpret local vs. global contributions
- Debug federated training

---

## Lightweight FL Framework

### Optimization Strategies

| Strategy | Description |
|----------|-------------|
| **Model compression** | Reduce communication overhead |
| **Gradient sparsification** | Only send significant updates |
| **Knowledge distillation** | Train smaller student models |
| **Split learning** | Divide model across layers |
| **Hierarchical FL** | Multi-level aggregation |

### Communication Efficiency

- **Periodic averaging:** Aggregate every K steps
- **Gradient compression:** Quantization, sparsification
- **Adaptive communication:** Skip unnecessary rounds

---

## Applications

| Domain | Use Case | FL Benefit |
|--------|----------|------------|
| **Healthcare** | Multi-hospital diagnosis | Patient data privacy |
| **Autonomous vehicles** | Collaborative perception | Driving data privacy |
| **Smart manufacturing** | Quality prediction | Proprietary process protection |
| **Finance** | Fraud detection | Customer data privacy |
| **Smart cities** | Traffic management | Citizen privacy |

---

## Future Research Directions

1. **Personalized FL:** Models adapted to individual clients
2. **Cross-silo FL:** Enterprise collaboration
3. **FL on LLMs:** Federated fine-tuning
4. **Vertical FL:** Feature-partitioned learning
5. **Decentralized FL:** No central server
6. **FL + Edge AI:** On-device training and inference

---

## Key Insights

1. **Privacy by design:** Data never leaves device
2. **Heterogeneity is the norm:** Plan for diverse devices
3. **Communication is expensive:** Compress, sparsify, adapt
4. **Security is multi-layered:** Robustness, fairness, explainability
5. **Lightweight is essential:** Edge devices have constraints

---

## Quotes

> "FL has emerged as a promising paradigm for enabling collaborative training of machine learning models while preserving data privacy."

> "The massive heterogeneity of data and devices, communication constraints, and security threats pose significant challenges."

> "6G core lies in the shift from 'connecting everything' to 'connecting intelligence'."

---

## Next Steps

- [ ] Study FedAvg and FedProx algorithms
- [ ] Explore model compression for FL
- [ ] Review differential privacy in FL
- [ ] Analyze split learning architecture