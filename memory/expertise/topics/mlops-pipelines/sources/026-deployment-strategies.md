# ML Model Deployment Strategies - Resumo

**Fonte:** https://arshren.medium.com/machine-learning-model-deployment-strategies-985a031f6ae1
**Tipo:** Article
**Data:** 2026-03-12

---

## 🎯 Por que Deployment Strategies?

### Motivação
- ML models precisam ser atualizados frequentemente
- Monitoramento identifica data drift / concept drift
- Model decay → retrain → redeploy

### Deployment Strategy
Forma de atualizar ML Model em produção mantendo:
- Availability
- Reliability
- Minimal disruption

## 📋 Deployment Strategies

### 1. Recreate Strategy

| Aspecto | Descrição |
|---------|-----------|
| **Processo** | Stop old version → Start new version |
| **Downtime** | Sim, durante a transição |
| **Custo** | Baixo (uma instância) |
| **Risco** | Alto (downtime total) |

**Quando usar:**
- Non-critical systems
- Development/staging environments
- Low traffic periods acceptable

---

### 2. Blue-Green Deployment

| Aspecto | Descrição |
|---------|-----------|
| **Processo** | Blue (old) + Green (new) em paralelo |
| **Switch** | Router/Load balancer muda tráfego |
| **Rollback** | Instantâneo (voltar para Blue) |
| **Custo** | 2x infra durante transição |

**Como funciona:**
1. Blue (current) está servindo tráfego
2. Deploy Green (new version)
3. Test Green
4. Switch router → Green
5. Blue fica standby para rollback

**Vantagens:**
- Zero downtime
- Rollback rápido
- Test em production-like environment

**Desvantagens:**
- Custo 2x durante transição
- Database migration complexity

---

### 3. Canary Deployment

| Aspecto | Descrição |
|---------|-----------|
| **Processo** | Gradualmente shift tráfego para new version |
| **Percentages** | 1% → 10% → 50% → 100% |
| **Feedback** | Monitorar métricas a cada step |
| **Rollback** | Rápido (voltar tráfego para old) |

**Como funciona:**
1. Deploy new version ao lado de old
2. Route pequeno % do tráfego para new
3. Monitor metrics (errors, latency, business)
4. Gradualmente aumentar %
5. Se problemas → rollback imediato

**Vantagens:**
- Risk mitigation
- Real production testing
- Gradual rollout

**Desvantagens:**
- Complex routing required
- Longer deployment time
- Monitoring overhead

---

### 4. A/B Testing

| Aspecto | Descrição |
|---------|-----------|
| **Processo** | Servir versões diferentes para grupos diferentes |
| **Objetivo** | Comparar performance estatisticamente |
| **Split** | Por usuário, região, dispositivo, etc. |
| **Duration** | Tempo suficiente para significância |

**Como funciona:**
1. Deploy A (control) e B (variant)
2. Split traffic por critério
3. Collect metrics
4. Statistical analysis
5. Choose winner

**Diferença de Canary:**
- Canary = deployment risk mitigation
- A/B = feature/business decision testing

**Use Cases:**
- Model comparison
- Feature experiments
- Business metric optimization

## 📊 Comparison Matrix

| Strategy | Downtime | Rollback | Cost | Risk |
|----------|----------|----------|------|------|
| **Recreate** | Yes | Slow | Low | High |
| **Blue-Green** | No | Fast | 2x | Low |
| **Canary** | No | Fast | 1.x | Very Low |
| **A/B Testing** | No | Fast | 1.x | Low |

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Blue** | Current production version |
| **Green** | New version (candidate) |
| **Canary** | Gradual traffic shift |
| **A/B Testing** | Statistical comparison |
| **Rollback** | Revert to previous version |

## 🔗 Referências Cruzadas

- Complementa: MLOps Principles (002)
- Relacionado a: CI/CD for ML (011-015)
- Pré-requisito para: Production ML

---

**Conceitos aprendidos:** 15
**Relevância:** Alta (deployment strategies fundamentals)