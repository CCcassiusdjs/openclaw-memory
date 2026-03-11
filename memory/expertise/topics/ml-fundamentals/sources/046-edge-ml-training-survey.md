# Training Machine Learning Models at the Edge: A Survey

**Fonte:** arXiv:2403.02619  
**Autores:** Aymen Rayane Khouas et al.  
**Data:** Outubro 2024 (v3)  
**Tipo:** Survey Paper (Acadêmico)

---

## 📋 Resumo Executivo

Survey sobre treinamento de modelos de ML no edge (edge learning). Explora abordagens de otimização para treinamento em dispositivos edge, com foco especial em federated learning. Sintetiza conhecimento existente, identifica desafios e destaca tendências futuras.

---

## 🔑 Conceitos-Chave

### Edge Computing + ML
- **Inference at edge** - Bem estabelecido
- **Training at edge** - Menos explorado
- **Edge learning** - Otimização de treinamento em dispositivos edge

### Por que Edge Learning?
1. **Privacy** - Dados permanecem no dispositivo
2. **Latency** - Sem necessidade de enviar dados para cloud
3. **Bandwidth** - Reduz uso de rede
4. **Personalization** - Modelos específicos por dispositivo
5. **Offline capability** - Funciona sem conectividade

---

## 📐 Métodos de Edge Learning

### Distributed Learning
1. **Federated Learning** - Treinamento distribuído sem compartilhar dados
2. **Split Learning** - Divide modelo entre edge e cloud
3. **Distributed SGD** - Gradientes distribuídos

### On-Device Training
1. **Model compression** - Modelos menores para dispositivos
2. **Quantization-aware training** - Treina com quantização
3. **Knowledge distillation** - Transfere conhecimento de modelo maior

### Optimization Techniques
1. **Gradient compression** - Reduz tamanho dos gradientes
2. **Local updates** - Múltiplas atualizações locais antes de sync
3. **Asynchronous training** - Sem barreira de sincronização

---

## 🛠️ Frameworks e Ferramentas

### Federated Learning
- TensorFlow Federated (TFF)
- PySyft
- FATE
- Flower

### Edge ML Platforms
- TensorFlow Lite
- PyTorch Mobile
- ONNX Runtime
- Core ML (Apple)

### Simulation Tools
- NS-3 para redes
- EdgeCloudSim
- iFogSim

---

## ⚠️ Desafios

### Computacionais
1. **Limited compute** - Dispositivos têm recursos limitados
2. **Memory constraints** - Modelos grandes não cabem
3. **Battery** - Treinamento consome muita energia

### Comunicação
1. **Bandwidth limited** - Redes edge são lentas
2. **Intermittent connectivity** - Conexões instáveis
3. **Heterogeneous devices** - Dispositivos com capacidades diferentes

### Dados
1. **Non-IID data** - Dados não distribuídos uniformemente
2. **Unbalanced data** - Quantidades diferentes por dispositivo
3. **Privacy constraints** - Dados não podem sair do dispositivo

---

## 📊 Métricas de Avaliação

1. **Accuracy** - Precisão do modelo
2. **Communication cost** - Bytes transmitidos
3. **Energy consumption** - Joules consumidos
4. **Training time** - Tempo até convergência
5. **Memory footprint** - Memória utilizada

---

## 💡 Insights Principais

1. **Federated learning domina** - Maioria dos estudos foca em FL
2. **Communication bottleneck** - Principal desafio
3. **Heterogeneity matters** - Dispositivos diferentes = desafios diferentes
4. **Privacy vs Performance** - Trade-off fundamental
5. **Simulation essential** - Ferramentas de simulação críticas para pesquisa

---

## 📝 Anotações de Estudo

- Survey focado em treinamento, não inference
- Ênfase em federated learning
- Taxonomia clara de métodos
- Guias para comparação de técnicas
- Frameworks e ferramentas listadas

**Tempo de leitura:** ~30 minutos  
**Relevância:** ⭐⭐⭐⭐ (Importante para ML distribuído)  
**Próximos passos:** Explorar TensorFlow Federated e Flower