# Machine Learning: The Basics

**Fonte:** Alexander Jung
**Editora:** MIT Press / Cambridge University Press
**Ano:** 2022
**URL:** https://alexjungaalto.github.io/MLBasicsBook.pdf

---

## Estrutura do Livro

O livro organiza o aprendizado de máquina em torno de **três componentes fundamentais**:
1. **Data** (Dados)
2. **Model** (Modelo)
3. **Loss** (Função de Perda)

### Capítulos Principais

1. **Introduction to Machine Learning**
   - O que é ML e como se relaciona com outras áreas
   - Estatística vs. ML vs. IA
   - Taxonomia de problemas de ML

2. **Data - The Fuel for Machine Learning**
   - Tipos de dados (estruturados, não-estruturados)
   - Representação de dados
   - Feature engineering
   - Qualidade e quantidade de dados

3. **Models - The Engines for Machine Learning**
   - Modelos paramétricos vs. não-paramétricos
   - Linear models
   - Neural networks
   - Kernel methods
   - Ensemble methods

4. **Loss Functions - The Steering Wheels for ML**
   - Funções de perda para regressão (MSE, MAE)
   - Funções de perda para classificação (cross-entropy, hinge)
   - Regularização como parte da loss

5. **Supervised Learning**
   - Classificação binária e multiclasse
   - Regressão
   - Avaliação de modelos

6. **Unsupervised Learning**
   - Clustering
   - Dimensionality reduction
   - Anomaly detection

7. **Reinforcement Learning**
   - MDPs
   - Value functions
   - Policy optimization

8. **Model Selection and Validation**
   - Cross-validation
   - Hyperparameter tuning
   - Bias-variance tradeoff

---

## Conceitos-Chave

### Framework Unificado: Data-Model-Loss
- **Data**: Entrada para o processo de aprendizado
- **Model**: Estrutura paramétrica que mapeia inputs para outputs
- **Loss**: Medida de quão bem o modelo se ajusta aos dados

### Princípios Centrais
- **Empirical Risk Minimization**: Minimizar a perda empírica nos dados de treino
- **Generalization**: Capacidade do modelo de performar bem em dados não vistos
- **Regularization**: Penalização de modelos complexos para evitar overfitting

### Metodologia
- **Train-validation-test split**: Separação de dados para avaliação
- **Cross-validation**: Validação cruzada para estimativa robusta
- **Hyperparameter tuning**: Otimização de hiperparâmetros

---

## Diferenciais do Livro

1. **Framework Unificado**: Organiza todos os métodos de ML em torno do tripé Data-Model-Loss
2. **Intuição Matemática**: Foca em entender o "porquê" antes do "como"
3. **Cobertura Balanceada**: Combina teoria rigorosa com aplicações práticas
4. **Abordagem Modular**: Cada capítulo pode ser lido independentemente

---

## Comparação com Outros Livros

| Aspecto | Jung (2022) | Shalev-Shwartz (2014) |
|---------|-------------|----------------------|
| **Foco** | Prático + Teórico | Teórico rigoroso |
| **Matemática** | Moderada | Avançada |
| **Público-alvo** | Graduados | Pós-graduados |
| **Framework** | Data-Model-Loss | PAC Learning |
| **Aplicações** | Muitas | Poucas |

---

## Citações Notáveis

> "Machine learning methods can be understood as finding a model that minimizes a loss function over given data."

> "The choice of model class determines the inductive bias of the learning method."

---

## Status
- [x] Leitura do sumário completada
- [ ] Leitura completa do livro (pendente)
- [ ] Exercícios resolvidos (pendente)

---

## Próximos Passos
1. Estudar o framework Data-Model-Loss em detalhes
2. Comparar com a abordagem PAC de Shalev-Shwartz
3. Praticar com exemplos do livro

---

*Fonte lida em: 2026-03-10*