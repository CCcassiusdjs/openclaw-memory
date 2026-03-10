# Azure Digital Twins - Overview

**Fonte:** https://learn.microsoft.com/en-us/azure/digital-twins/overview  
**Tipo:** Documentação Oficial  
**Lido em:** 2026-03-10  
**Tempo de leitura:** 15 min

---

## 📋 Resumo Executivo

Azure Digital Twins é uma plataforma PaaS (Platform as a Service) que permite criar **twin graphs** baseados em modelos digitais de ambientes inteiros - edifícios, fábricas, fazendas, redes de energia, ferrovias, estádios, até cidades inteiras.

---

## 🏗️ Arquitetura Principal

### Componentes da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                    AZURE DIGITAL TWINS                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Models    │  │ Twins Graph │  │   Query API        │  │
│  │   (DTDL)    │  │  (Live State)│  │   (Insights)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ▲                   ▲                      │
         │                   │                      ▼
    ┌────┴────┐         ┌────┴────┐         ┌──────────────┐
    │IoT Hub  │         │Event    │         │Downstream    │
    │Devices  │         │System   │         │Services      │
    └─────────┘         └─────────┘         └──────────────┘
```

### Elementos Principais

1. **Models (DTDL)** - Digital Twins Definition Language
   - JSON-like language para definir tipos de entidades
   - Descreve: state properties, components, relationships
   - Vocabulário especializado para seu domínio

2. **Twin Graph** - Grafo de gêmeos digitais
   - Representa entidades específicas (Building 1, Building 2...)
   - Conectados via relationships formando grafo conceitual
   - Estado sempre atualizado com mundo real

3. **Query API** - API de consulta poderosa
   - Busca por valores de propriedades
   - Filtros por relacionamentos
   - Combinações complexas de queries

---

## 🔧 Funcionalidades Principais

### 1. Modelagem de Ambiente
- Definir tipos customizados (Building, Floor, Elevator)
- Usar ontologias pré-existentes da indústria
- DTDL v2 compatível com IoT Plug and Play

### 2. Contextualização de Dados IoT
- Conectar IoT Hub para dispositivos
- REST APIs para sistemas de negócio
- Sistema de eventos rico para processamento

### 3. Query e Insights
- Query API para extração de insights
- Linguagem específica para queries complexas
- Histórico de dados via Azure Data Explorer

### 4. Visualização 3D
- 3D Scenes Studio (preview)
- Mapear elementos 3D para digital twins
- Interface low-code para construção

### 5. Integração com Serviços Azure
- Event routes para Event Hubs, Event Grid, Service Bus
- Azure Data Explorer para análise histórica
- Azure Data Lake para armazenamento
- Azure Synapse Analytics para analytics
- Logic Apps para workflows

---

## 📊 Modelo de Dados (DTDL)

### Estrutura Básica
```json
{
  "@id": "dtmi:example:Building;1",
  "@type": "Interface",
  "contents": [
    {
      "@type": "Property",
      "name": "temperature",
      "schema": "double"
    },
    {
      "@type": "Relationship",
      "name": "contains",
      "target": "dtmi:example:Floor;1"
    }
  ]
}
```

### Tipos de Conteúdo
- **Property** - Estado do twin (temperatura, status)
- **Relationship** - Conexões entre twins
- **Component** - Sub-entidades
- **Telemetry** - Dados de sensores

---

## 🔄 Fluxo de Dados

```
IoT Devices → IoT Hub → Azure Digital Twins → Event Routes
                                          ↓
                               ┌──────────────────────┐
                               │   Azure Functions     │
                               │   (Processamento)     │
                               └──────────────────────┘
                                          ↓
                               ┌──────────────────────┐
                               │  Downstream Services │
                               │  (Data Lake, ADX)    │
                               └──────────────────────┘
```

---

## 💡 Casos de Uso

1. **Gestão de Edifícios** - Monitoramento, otimização de energia
2. **Manufatura** - Fábricas inteligentes, predição de falhas
3. **Cidades Inteligentes** - Tráfego, energia, infraestrutura
4. **Energia** - Redes elétricas, otimização de grid
5. **Ferrovias** - Monitoramento de ativos, manutenção preditiva

---

## 🔑 Conceitos-Chave Aprendidos

| Conceito | Descrição |
|----------|-----------|
| **DTDL** | Digital Twins Definition Language - JSON-like para modelos |
| **Twin Graph** | Grafo de entidades conectadas com estado live |
| **Event Routes** | Rotas de eventos para serviços downstream |
| **Data History** | Histórico de dados no Azure Data Explorer |
| **3D Scenes Studio** | Visualização 3D low-code |

---

## 📝 Notas para Implementação

- DTDL v2 é compatível com IoT Plug and Play
- Azure Digital Twins Explorer para visualização do grafo
- Azure Functions para processamento customizado
- Event Grid/Event Hubs/Service Bus para egress de dados
- Integração com Azure Data Explorer para queries históricas

---

## 🔗 Links Relacionados

- [DTDL v3 Spec](https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v3/DTDL.v3.md)
- [Query Language](concepts-query-language)
- [Models Concepts](concepts-models)
- [3D Scenes Studio](concepts-3d-scenes-studio)