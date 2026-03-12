# Monitoring Machine Learning Systems - Made With ML

**Fonte:** https://madewithml.com/courses/mlops/monitoring/
**Autor:** Goku Mohandas (Made With ML)
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Curso abrangente sobre monitoramento de sistemas ML em produção. Explica os tipos de drift (data, target, concept), técnicas de detecção (KS test, Chi-squared, multivariate), e abordagens para identificar problemas antes da degradação de performance.

---

## 🎯 Motivação

**Diferença fundamental ML vs Software Tradicional:**
- Software tradicional: Funciona como definido, work done após deployment
- ML: Probabilístico, sujeito a degradação natural, dados diferentes do training

**Conclusão:** Não tentar evitar drift, mas entender e mitigar.

---

## 📊 Camadas de Monitoramento

### 1. System Health
- **Latência, throughput, error rates**
- **CPU/GPU utilization, memory**
- Ferramentas: Grafana, Datadog, dashboards nativos de cloud

### 2. Performance
- **Métricas de avaliação:** accuracy, precision, f1, etc.
- **Métricas de negócio:** ROI, click rate, etc.

**Important:** Não apenas métricas cumulativas, mas também **sliding windows**:
- Cumulativa pode esconder problemas recentes
- Sliding window mais indicativo de saúde atual

### 3. Delayed Outcomes
Quando ground-truth não está disponível imediatamente:
- **Approximate signal:** Labels intermediários (ex: tags do autor vs verified labels)
- **Subset labeling:** Label subset representativo para estimar performance

### 4. Importance Weighting
Quando nenhum feedback disponível:
- **Slicing functions:** Capturar distribution shifts
- Aplicar slices ao labeled dataset → criar matrizes
- Aplicar slices ao production data → aproximar performance
- **Assumption:** Slices capturam causas de drift

---

## 🔍 Tipos de Drift

| Entity | Description | Drift Type |
|--------|-------------|------------|
| X (features) | Input features | Data drift: P(X) ≠ P_ref(X) |
| y (labels) | Ground-truth | Target drift: P(y) ≠ P_ref(y) |
| P(y|X) | Relationship | Concept drift: P(y|X) ≠ P_ref(y|X) |

### Data Drift (Covariate Shift)
- Distribuição de production diferente de training
- Causas: Mudanças naturais, missing data, pipeline errors, schema changes
- **Training-serving skew:** Workflows diferentes para training e serving
- **Solução:** Feature store para mesma fonte

### Target Drift
- Shift nas distribuições de outcomes
- Pode incluir adição/remoção de classes
- Mitigação: Inter-pipeline communication sobre changes

### Concept Drift
- Mudança na relação entre X e y
- Patterns:
  - **Gradual:** Ao longo do tempo
  - **Abrupt:** Evento externo súbito
  - **Periodic:** Eventos recorrentes

---

## 🕵️ Locating Drift

### Constraints
- **Reference window:** Subset do training data para comparação
- **Test window:** Production data para detectar drift

### Approaches
- **Fixed window:** Subset fixo do training
- **Sliding window:** Production data desliza sobre tempo

**Tools:** Scikit-multiflow para concept drift detection em streaming data

---

## 📏 Measuring Drift

### Expectations (Rule-based)
- Great Expectations para validar:
  - Missing values
  - Data types
  - Value ranges
- Validação em production data

### Univariate Drift Tests

#### Kolmogorov-Smirnov (KS) Test
- Para features contínuas
- Mede distância máxima entre CDFs
- Low p-value = distribuições diferentes

```python
from alibi_detect.cd import KSDrift

# Reference data
ref = df["num_tokens"][0:200].to_numpy()

# Initialize detector
detector = KSDrift(ref, p_val=0.01)

# Predict drift
detector.predict(test_data, return_p_val=True)
```

#### Chi-squared Test
- Para features categóricas
- Compara frequências entre reference e production
- Útil para target distribution, class distribution

```python
from alibi_detect.cd import ChiSquareDrift

# Reference data
ref = df["category"][0:200].to_numpy()

# Initialize detector
detector = ChiSquareDrift(ref, p_val=0.01)

# Predict drift
detector.predict(test_data, return_p_val=True)
```

### Multivariate Drift
- Mais complexo para dados multivariados
- Abordagem: **Reduce and measure** (paper: Failing Loudly)
- Técnicas:
  - Dimensionality reduction (PCA, UMAP)
  - Embedding-based drift detection

---

## 🛠️ Solutions for Drift

### Prevention
- Feature store para evitar training-serving skew
- Inter-pipeline communication sobre schema changes
- Proper data validation na entrada

### Detection
- Monitor data drift, target drift, concept drift
- Use multiple window sizes
- Set appropriate thresholds

### Reaction
- **Retrain** quando drift significativo
- **Rollback** para modelo anterior se necessário
- **Alert** teams para investigação

---

## 💡 Insights Principais

1. **ML é diferente de software:** Degradation natural é esperado
2. **Performance não é suficiente:** Delayed outcomes, importance weighting
3. **Drift é inevitável:** Entender tipos e patterns é essencial
4. **Sliding windows > Cumulativas:** Capturam problemas mais rápido
5. **KS test para contínuas, Chi-squared para categóricas**
6. **Feature store evita training-serving skew**

---

## 📚 Referências

1. Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift
2. Scikit-multiflow documentation
3. Great Expectations documentation
4. Alibi Detect library

---

## 📝 Tags

`#monitoring` `#drift-detection` `#mlops` `#production-ml` `#concept-drift` `#data-drift`