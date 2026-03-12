# How to Detect Model Drift in MLOps Monitoring

**Fonte:** https://towardsdatascience.com/how-to-detect-model-drift-in-mlops-monitoring-7a039c22eaf9/
**Autor:** Towards Data Science
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Artigo sobre detecção de model drift em sistemas ML em produção. Explica os tipos de drift, técnicas estatísticas para medição, e um processo de 4 passos para identificar causas de drift.

---

## 🎯 Problema: Drift em Produção

**ML models são únicos**: Performance pode flutuar ao longo do tempo devido a mudanças nos dados de entrada após deployment.

**Desafio**: Labels (ground truth) nem sempre estão disponíveis em tempo real para calcular métricas de performance.

**Solução**: Monitorar mudanças nas distribuições de features e predictions como leading indicator de problemas de performance.

---

## 📊 Tipos de Drift

| Tipo | Definição | Exemplo |
|------|-----------|---------|
| **Concept Drift** | Mudança em P(Y\|X) | Renda que era creditworthy não é mais |
| **Prediction Drift** | Mudança em P(Ŷ\|X) | Mais aplicações credit-worthy em área rica |
| **Label Drift** | Mudança em P(Y) | Mudança na distribuição de outputs |
| **Feature Drift** | Mudança em P(X) | Renda de todos aumenta 5%, fundamentos iguais |

### Concept Drift
- Discrepância entre decision boundary real e aprendida
- Necessita re-learning para manter accuracy
- Performance drift é o indicador mais forte (se ground truth disponível)
- Na ausência de ground truth, prediction drift e feature drift são proxies

---

## 🔧 Técnicas para Medir Drift

### Abordagem Estatística

| Técnica | Descrição | Uso |
|---------|-----------|-----|
| **PSI (Population Stability Index)** | Medida de estabilidade entre duas populações | Popular em serviços financeiros |
| **KL Divergence** | Mede diferença entre distribuições | Assimétrico, comum em ML |
| **JS Divergence** | Similaridade entre distribuições (baseado em KL) | Simétrico, sempre finito |
| **KS Test** | Teste não-paramétrico de igualdade de distribuições | Comparar amostras |

### Abordagem Baseada em Modelo
- Usa ML para determinar similaridade
- Mais precisa, mas menos interpretável
- Difícil de explicar para stakeholders

---

## 🎯 Processo de Detecção de Drift (4 Passos)

### Passo 1: Identificar Prediction Drift
- Comparar outputs em tempo real com baseline (training set)
- Usar JS-Divergence + conhecimento de domínio para thresholds

### Passo 2: Drill Down em Features
- Identificar features com drift usando JS-Divergence
- Usar explainability para feature importance
- Focar apenas em features com impacto (filtrar spurious drift)

### Passo 3: Comparar Distribuições
- Visualizar diferenças nas distribuições
- Formar intuição sobre necessidade de retraining

### Passo 4: Analisar Performance
- Analisar slice afetado para insights de performance
- Correlacionar drift com métricas de negócio

---

## 📝 Causas de Drift

1. **Mudança real na distribuição de dados**
   - Externalidades, mudanças de mercado
   - Necessita novo modelo com training set atualizado

2. **Mudança no ground truth ou input distribution**
   - Preferências de clientes mudam (ex: pandemia)
   - Produto lançado em novo mercado

3. **Mudança de conceito**
   - Competidor lança novo serviço
   - Regulamentações mudam

4. **Data integrity issues**
   - Requer investigação humana

5. **Data engineering bugs**
   - Valores trocados (ex: debt-to-income e age)

6. **Dados incorretos na fonte**
   - Bug no frontend aceita campo vazio

---

## 💡 Insights Principais

1. **Drift é inevitável**: Modelos em produção degradam com tempo
2. **Performance metrics precisam de labels**: Nem sempre disponíveis em tempo real
3. **Feature drift é leading indicator**: Pode antecipar problemas de performance
4. **JS-Divergence é recomendado**: Simétrico, finito, bem comportado
5. **Feature importance filta spurious drift**: Nem todo drift importa
6. **4-step process é prático**: Identificar → Drill down → Comparar → Analisar

---

## 📚 Referências

1. A Survey on Concept Drift Adaptation - Joao Gama et al.
2. Population Stability Index (PSI)
3. KL Divergence - Wikipedia
4. Jensen-Shannon Divergence - Wikipedia
5. Kolmogorov-Smirnov Test - Wikipedia

---

## 📝 Tags

`#model-drift` `#monitoring` `#mlops` `#data-drift` `#concept-drift` `#production-ml`