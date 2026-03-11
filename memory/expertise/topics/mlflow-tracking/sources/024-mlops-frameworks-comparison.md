# MLOps Frameworks Comparison - Avaliação Empírica

**Fonte:** PAPER-001 - An Empirical Evaluation of Modern MLOps Frameworks  
**URL:** https://arxiv.org/abs/2601.20415  
**Tipo:** Paper Acadêmico  
**Data:** Janeiro 2026  
**Status:** completed

---

## Resumo

Avaliação empírica comparativa de frameworks MLOps: MLflow, Metaflow, Apache Airflow e Kubeflow Pipelines. Implementa dois cenários ML (MNIST digit classifier e IMDB sentiment classifier com BERT) avaliando: facilidade de instalação, flexibilidade de configuração, interoperabilidade, complexidade de instrumentação de código, interpretabilidade de resultados e documentação.

---

## Conceitos-Chave

### MLflow Features (Sec 2.1)
- **Tracking**: Registro e consulta de experimentos (código, dados, configuração, resultados)
- **Projects**: Organização de código ML em projetos reutilizáveis e reprodutíveis
- **Models**: Formato padronizado para empacotamento e versionamento de modelos
- **Model Registry**: Store centralizado com versionamento, stage transitions, annotations

### Arquitetura MLflow
- Modular: gerenciamento flexível de dados, modelos e parâmetros
- Armazenamento: filesystem local ou S3, GCS, Azure Blob
- Integração Databricks: versão comercial com colaboração multi-usuário, controle de acesso centralizado, monitoramento em escala
- Adoção empresarial: Microsoft, Meta, Toyota, Accenture

### Comparação com Outros Frameworks

| Framework | Origem | Foco | Estrelas GitHub | Contribuidores |
|-----------|--------|------|-----------------|----------------|
| MLflow | Databricks | Lifecycle completo | 20.700+ | 850+ |
| Metaflow | Netflix | Workflows DS/ML | 8.900+ | 110+ |
| Airflow | Airbnb/Apache | Orquestração DAGs | - | - |
| Kubeflow | Google/CNCF | Pipelines Kubernetes | - | - |

### Metaflow Features (Sec 2.2)
- **Workflow definition**: Pipelines em Python com @step decorator
- **Data management**: Persistência automática entre steps
- **Execution**: Local ou AWS Batch/Step Functions/Kubernetes
- **Versioning**: Cada execução gera versão única com inputs, outputs, metadata
- **Visualization**: Interface web para visualizar grafo de execução

### Apache Airflow Features (Sec 2.3)
- **DAG definition**: Workflows em Python com dependencies
- **Scheduling**: Cron expressions + queue system
- **Orchestration**: Amplamente usado em data engineering

---

## Critérios de Avaliação

1. **Ease of Installation**: Facilidade de instalação inicial
2. **Configuration Flexibility**: Flexibilidade de configuração
3. **Interoperability**: Capacidade de integração com outras ferramentas
4. **Code Instrumentation Complexity**: Complexidade para instrumentar código
5. **Result Interpretability**: Facilidade de interpretar resultados
6. **Documentation**: Qualidade da documentação

---

## Cenários de Teste

1. **MNIST Digit Classifier**: Classificação de dígitos manuscritos
2. **IMDB Sentiment Classifier**: Análise de sentimento com BERT

---

## Insights para MLflow Users

### Pontos Fortes do MLflow
- Modular architecture (tracking, projects, models, registry separados)
- Grande comunidade e suporte empresarial (Databricks)
- Flexibilidade de storage (local, S3, GCS, Azure)
- Adoção consolidada em grandes empresas

### Comparação Metaflow vs MLflow
- Metaflow foca em workflow definition com Python decorators
- MLflow foca em lifecycle management (tracking + registry)
- Metaflow otimizado para AWS; MLflow mais agnóstico de cloud

### Shift Left em MLOps
- Integrate validation, testing, quality control early in development
- Data quality e versioning como first-class citizens
- Continuous validation e early error detection

---

## Conceitos Adicionados

- MLOps Frameworks Comparison
- Shift Left Approach in ML
- Metaflow @step decorator
- Apache Airflow DAGs
- MLflow vs Metaflow vs Airflow vs Kubeflow
- Enterprise MLOps Adoption Patterns

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 20 min