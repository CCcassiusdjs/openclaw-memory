# Spurious Correlations in Machine Learning: A Comprehensive Survey

**Fonte:** arXiv:2402.12715  
**Autores:** Wenqian Ye, Luyang Jiang, Eric Xie, et al.  
**Data:** Outubro 2025 (v4)  
**Tipo:** Survey Paper (Acadêmico)

---

## 📋 Resumo Executivo

Survey abrangente sobre correlações espúrias em Machine Learning. Usa a analogia do "Clever Hans" (cavalo que parecia fazer matemática mas respondia a pistas sutis) para explicar como modelos de ML dependem de features não-essenciais. Apresenta taxonomia de métodos, datasets, benchmarks e métricas.

---

## 🔑 Conceitos-Chave

### Definição Formal

**Spurious Correlation:** Associação entre label y e atributo espúrio a, onde a não é preditivo de y, mas correlacionado no conjunto de treino.

Formalmente: ⟨y, a⟩ onde:
- y ∈ 𝒴 (classe)
- a ∈ 𝒜 (atributo espúrio)
- g = (y, a) (group label)

### Por que ocorrem?

1. **Selection bias** - Datasets limitados são sub-especificados
2. **Simplicity bias** - Modelos preferem features simples mas não-preditivas
3. **Imbalanced group labels** - Over-representation de certos grupos
4. **Sampling noise** - Variações aleatórias interpretadas como correlação

### Por que ML é sensível?

1. **Inductive biases** - Arquiteturas têm pressupostos que capturam padrões espúrios
2. **Optimization (ERM)** - Minimiza loss média, ignora grupos minoritários
3. **Early learning dynamics** - Features espúrias aprendidas primeiro

---

## 📊 Framework Teórico

### ERM Problem
```
ℒ_avg(f_θ) = E_{g∼P_g} E_{(x,y,a)∼P_{x|g}} [ℓ(f_θ(x), y)]
```

### Worst-Group Error
```
ℒ_wg(f_θ) = max_{g∈𝒢} E_{(x,y,a)∼P_{x|g}} [ℓ(f_θ(x), y)]
```

### Group DRO
Minimiza o pior caso sobre todos os grupos, não a média.

---

## 🔬 Áreas Relacionadas

### Domain Generalization (DG)
- Generalização para domínios não-vistos
- Spurious correlations falham em domínios novos
- Multi-Source DG (MSDG) e Single-Source DG (SDG)

### Group Robustness
- Performance consistente entre subgrupos
- Worst-case optimization
- Benchmarks: WILDS (Waterbirds, CelebA, CivilComments)

### Shortcut Learning
- Modelos exploram correlações fáceis
- Em vez de features causais

### Simplicity Bias
- Modelos preferem padrões de baixa complexidade
- Features espúrias são mais fáceis de aprender

---

## 📈 Datasets e Benchmarks

### Waterbirds
- Classificação de pássaros
- Correlação espúria: background (água/terra) com label

### CelebA
- Atributos faciais
- Correlações espúrias entre atributos

### CivilComments
- Toxicidade em comentários
- Correlações espúrias com identity terms

---

## 🛠️ Métodos de Mitigação

1. **Group DRO** - Minimiza worst-group loss
2. **Up-weighting minority groups** - Re-balanceia grupos
3. **Two-stage training** - Identifica e corrige bias
4. **Data augmentation** - Aumenta diversidade
5. **Adversarial training** - Remove features espúrias

---

## 💡 Insights Principais

1. **Clever Hans effect** - Modelos aprendem pistas sutis, não conceitos
2. **Early learning matters** - Features espúrias aprendidas primeiro
3. **Latent space analysis** - Features espúrias persistem no espaço latente
4. **Post-hoc mitigation unreliable** - Regularizers podem suprimir sinais úteis
5. **Foundation models** - Novas oportunidades para mitigação

---

## 🔮 Desafios Futuros

1. **Limited datasets** - Escassez de dados com group labels
2. **Computational constraints** - Custo de métodos robustos
3. **Theory-practice gap** - Modelos teóricos vs deployment real
4. **Foundation models** - Como usar LLMs/VLMs para mitigação
5. **Unknown spurious attributes** - Correlações desconhecidas

---

## 📝 Anotações de Estudo

- Survey sistemático e abrangente
- Definição formal rigorosa
- Conexão clara com áreas relacionadas
- Taxonomia de métodos útil
- Benchmarks bem documentados

**Tempo de leitura:** ~40 minutos  
**Relevância:** ⭐⭐⭐⭐⭐ (Fundamental para robustness)  
**Próximos passos:** Explorar Group DRO implementations