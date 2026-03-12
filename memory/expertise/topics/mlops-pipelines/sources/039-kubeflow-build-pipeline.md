# Kubeflow Pipelines: Build a Pipeline

**Fonte:** https://www.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/build-pipeline/
**Autor:** Kubeflow Documentation
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Documentação oficial do Kubeflow para criação de pipelines ML. Explica conceitos de components, pipeline graph, data passing, e best practices para design de pipelines escaláveis.

---

## 🎯 O que é Kubeflow Pipeline?

**Definição:** Definição portável e escalável de um workflow ML, baseado em containers.

**Componentes:**
- Input parameters
- Lista de steps (cada step = instância de componente)
- Dependencies entre steps

**Uso:**
- Orquestrar workflows ML repetíveis
- Acelerar experimentação com diferentes hyperparameters

---

## 🏗️ Pipeline Components

### Definição
Aplicação containerizada que executa um step do pipeline.

### Component Specification
| Elemento | Descrição |
|----------|-----------|
| **Interface** | Inputs e outputs |
| **Implementation** | Container image + command |
| **Metadata** | Nome, descrição |

### Tipos de Components

#### 1. Container-based
- Container image + command
- Flexível: qualquer linguagem
- Requer component specification YAML

#### 2. Python Function-based
- Função Python vira componente automaticamente
- SDK gera specification
- Mais simples para Python developers

---

## 📊 Pipeline Graph

### Dependências de Dados

```
ingest_data → generate_statistics → train_model
                    ↑                  ↑
                    └──────────────────┘
                          (depends on)
```

### Exemplo: Pipeline de ML

| Step | Dependência | Descrição |
|------|-------------|-----------|
| Ingest Data | Pipeline args | Carrega dados de fonte externa |
| Generate Statistics | Ingest Data | Gera estatísticas do dataset |
| Preprocess Data | Ingest Data | Transforma dados |
| Train Model | Preprocess + Statistics | Treina modelo |

**Paralelismo:** Steps independentes rodam em paralelo.

---

## 🎨 Design Best Practices

### Single Responsibility
- Cada componente = uma responsabilidade
- Facilita teste e reuso

### Reuse Prebuilt Components
- Kubeflow fornece componentes comuns
- Economiza tempo de desenvolvimento

### Debugging Considerations
- Pipeline armazena inputs/outputs de cada step
- Artifacts disponíveis para debugging
- Lineage tracking

### Composability
- Steps conectados via outputs
- Dependências definem grafo

---

## 🔄 Data Passing Between Components

### Input Passing
| Tipo | Método |
|------|--------|
| **Small inputs** | Passados por valor (CLI args) |
| **Large inputs** | Passados como file paths |

### Output Passing
- Outputs escritos em paths fornecidos pelo Kubeflow
- Python function-based components handle automaticamente

---

## 🐍 Python Function-based Components

### Exemplo Básico

```python
def merge_csv(file_path: comp.InputPath('Tarball'),
              output_csv: comp.OutputPath('CSV')):
    import glob
    import pandas as pd
    import tarfile

    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    df = pd.concat([
        pd.read_csv(csv_file, header=None)
        for csv_file in glob.glob('data/*.csv')
    ])
    df.to_csv(output_csv, index=False, header=False)
```

### InputPath e OutputPath
- Decorators para inputs/outputs
- Kubeflow fornece paths automaticamente

### Criação de Component

```python
create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    base_image='python:3.7',
    packages_to_install=['pandas==1.1.4']
)
```

---

## 📦 Reusing Prebuilt Components

### Web Download Component

```python
web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml'
)
```

### Uso no Pipeline

```python
def my_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    merge_csv_task = create_step_merge_csv(file=web_downloader_task.outputs['data'])
```

---

## 🚀 Compiling and Running

### Option 1: UI Upload

```bash
# Compile
kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml'
)
```

### Option 2: SDK Client

```python
client = kfp.Client()
client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={'url': 'https://...'}
)
```

---

## 💡 Insights Principais

1. **Container-based = flexível**: Qualquer linguagem, qualquer runtime
2. **Python function-based = simples**: SDK gera specification
3. **Data dependencies = DAG**: Steps executam em paralelo quando possível
4. **Artifacts = debugging**: Inputs/outputs armazenados para inspeção
5. **Reuse components**: Economiza desenvolvimento

---

## 📝 Tags

`#kubeflow` `#pipelines` `#mlops` `#containers` `#workflow` `#python-components`