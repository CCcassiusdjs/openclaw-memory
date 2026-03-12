# Federated Learning for Edge AI

**Fonte:** MDPI Electronics, IntechOpen, arXiv
**Link:** https://www.mdpi.com/2079-9292/14/13/2512
**Tipo:** Survey / Research Paper

---

## Resumo Executivo

Federated Learning (FL) é um framework de ML que permite treinamento distribuído sem compartilhar dados raw. Edge devices treinam localmente e enviam apenas model updates (weights/gradients) para um aggregator central. Preserva privacidade e é ideal para Edge AI.

---

## Conceito Fundamental

### Definição
- Treinamento colaborativo de ML
- Dados permanecem no dispositivo
- Apenas updates são transmitidos
- Aggregation central produz modelo global

### Arquitetura FL

```
[Edge Device 1] --weights--> [Central Server] <--weights-- [Edge Device N]
       |                              |
   Local Data                  Aggregation
       |                              |
   Local Train <--updated model------|
```

---

## Motivação

### Problemas Tradicionais
- Dados sensíveis não podem ser compartilhados
- Regulations (GDPR, HIPAA)
- Bandwidth limitations
- Latência de cloud

### Solução FL
- Dados nunca deixam o dispositivo
- Privacy-preserving por design
- Reduz bandwidth requirements
- Permite personalização local

---

## Tipos de FL

### Horizontal FL
- Mesmas features, diferentes samples
- Exemplo: usuários diferentes, mesmo app
- Mais comum

### Vertical FL
- Features diferentes, mesmos samples
- Exemplo: empresas com dados complementares
- Mais complexo

### Federated Transfer Learning
- Features e samples diferentes
- Usa transfer learning para alinhar

---

## Aggregation Methods

### FedAvg (Federated Averaging)
- Média ponderada dos updates
- Mais comum
- Simples e efetivo

### FedProx
- Regularization para heterogeneidade
- Melhor para devices não-IID

### FedSGD (Federated SGD)
- Gradient averaging
- Mais communication overhead

---

## Privacy Techniques

### Differential Privacy (DP)
- Adiciona ruído aos updates
- Garante privacy formal
- Trade-off: accuracy vs privacy

### Secure Aggregation
- Criptografia dos updates
- Server não vê updates individuais
- Aggregation criptografada

### Homomorphic Encryption
- Computação em dados criptografados
- Alto overhead computacional
- Privacy máxima

---

## Desafios em Edge

### Resource Constraints
- Computação limitada
- Bateria
- Memória

### Heterogeneity
- Devices diferentes
- Dados não-IID
- Conectividade variável

### Communication
- Bandwidth limitada
- Latência
- Intermittent connectivity

---

## Otimizações

### Communication Efficiency
- Compression de gradients
- Sparse updates
- Local epochs múltiplas

### Lightweight Models
- Model pruning
- Knowledge distillation
- Quantization

### Adaptive Offloading
- Offload parcial para cloud
- Dynamic resource allocation
- Energy-aware scheduling

---

## Aplicações Edge AI

### Healthcare
- Treinamento em dados médicos locais
- HIPAA compliance
- Wearables

### IoT Industrial
- Anomaly detection local
- Predição de falhas
- Privacy de dados industriais

### Mobile Devices
- Keyboard prediction
- Voice assistant improvement
- Photo organization

### Smart Cities
- Traffic prediction
- Energy optimization
- Privacy de dados públicos

---

## FedAvg Algorithm

```
1. Server inicializa modelo global w_0
2. Para cada round t:
   a. Server seleciona subset de clients K
   b. Server envia w_t para clients
   c. Cada client k:
      - Treina localmente por E epochs
      - Calcula update Δw_k
      - Envia Δw_k para server
   d. Server agrega:
      w_{t+1} = w_t + Σ (n_k/n) * Δw_k
```

---

## Segurança

### Threats
- Poisoning attacks
- Backdoor attacks
- Inference attacks
- Byzantine clients

### Defesas
- Robust aggregation
- Anomaly detection
- Trusted execution environments
- Client verification

---

## Trustworthy AI em FL

### Robustness
- Resiliente a adversários
- Handling data poisoning
- Byzantine fault tolerance

### Fairness
- Equidade entre participantes
- Não discriminação
- Balanced contribution

### Explainability
- Interpretable local models
- Global model explanation
- Attribution methods

---

## Citações Importantes

> "FL enables decentralised model training without sharing raw data."

> "Federated learning utilizes the modified FedAvg algorithm, supported by differential privacy and homomorphic encryption."

> "Training is conducted locally on edge devices, and only model updates are transmitted to a central aggregator."

---

## Conexões com Edge AI

Federated Learning é **paradigma essencial** para:
- Treinamento distribuído em edge
- Privacy-preserving AI
- Compliance com regulations
- Personalização local

### Relevância
- ★★★★★ Paradigma fundamental para Edge AI
- Habilita colaboração sem compartilhar dados
- Integração com TinyML para treinamento em MCUs

---

**Data de Leitura:** 2026-03-12
**Relevância:** ★★★★★ (Paradigma fundamental para Edge AI distribuído)