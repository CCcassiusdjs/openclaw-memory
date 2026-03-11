# Azure Digital Twins - Platform Overview

**Fonte:** Microsoft Learn Documentation  
**Autor:** Microsoft  
**Data:** Janeiro 2025  
**Tipo:** Documentação Oficial

---

## 📋 Resumo Executivo

Azure Digital Twins é uma plataforma PaaS para criar twin graphs baseados em modelos digitais de ambientes completos. Permite modelar edifícios, fábricas, fazendas, redes de energia, ferrovias, estádios e cidades inteiras. Oferece insights para otimizar operações, reduzir custos e melhorar experiências.

---

## 🔑 Conceitos-Chave

### Digital Twins Definition Language (DTDL)
- Linguagem JSON-like para definir modelos
- Descreve entidades por: propriedades de estado, componentes e relacionamentos
- Compatível com IoT Plug and Play
- Versão 2 usada em outros serviços Azure IoT

### Modelos e Twins
- **Models** - Definições de tipos (Building, Floor, Elevator)
- **Twins** - Instâncias específicas (Building 1, Building 2)
- **Graph** - Rede de twins conectados por relacionamentos

---

## 🏗️ Arquitetura de Solução

### Componentes Principais
1. **Azure Digital Twins instance** - Armazena modelos e twin graph
2. **Client apps** - Configuram modelos, criam topologia, extraem insights
3. **External compute** - Azure Functions para processamento
4. **IoT Hub** - Gerenciamento de dispositivos e streams de dados
5. **Downstream services** - Storage, analytics, workflows

### Conectividade
- IoT Hub para dispositivos IoT/Edge
- REST APIs para integrações
- Logic Apps para workflows
- Event Grid/Event Hubs/Service Bus para routing

---

## 🛠️ Funcionalidades

### Modelagem
- Ontologias pré-definidas por indústria
- Modelos customizados com DTDL
- Relacionamentos entre entidades

### Contextualização de Dados
- Live representations do mundo real
- Sincronização via IoT Hub
- Integração com sistemas de negócio

### Query API
- Busca extensiva com condições
- Valores de propriedades
- Relacionamentos e propriedades de relacionamentos
- Informações de modelo

### 3D Scenes Studio (preview)
- Visualização 3D imersiva
- Mapeamento de elementos 3D para twins
- Low-code builder
- UI interativa

---

## 📊 Integrações Azure

### Data History
- Azure Data Explorer para historização
- Query plugin para Azure Data Explorer

### Event Routes
- Azure Data Lake (storage)
- Azure Synapse Analytics (analytics)
- Logic Apps (workflows)
- Custom applications

---

## 💡 Insights Principais

1. **Graph-based modeling** - Relacionamentos são first-class citizens
2. **Live twin graph** - Representação em tempo real
3. **Event-driven architecture** - Processamento de eventos customizado
4. **Ontology support** - Vocabulários pré-definidos por indústria
5. **3D visualization** - Studio para visualização imersiva

---

## 📝 Anotações de Estudo

- Plataforma completa de DT como serviço
- DTDL é padrão aberto (compatível com outros sistemas)
- Integração nativa com ecossistema Azure
- 3D Scenes Studio é feature diferenciada
- Query API poderosa para extração de insights

**Tempo de leitura:** ~20 minutos  
**Relevância:** ⭐⭐⭐⭐⭐ (Plataforma líder de DT)  
**Próximos passos:** Explorar DTDL specs e exemplos de ontologia