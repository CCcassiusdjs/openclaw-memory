# The Illustrated Transformer - Jay Alammar

**Fonte:** https://jalammar.github.io/illustrated-transformer/
**Autor:** Jay Alammar
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Uma das explicações visuais mais aclamadas da arquitetura Transformer. Explica conceitos complexos com diagramas claros e exemplos concretos. Referência em cursos de Stanford, Harvard, MIT, Princeton.

---

## 🏗️ Visão Geral do Transformer

### Arquitetura Encoder-Decoder
- **Encoder stack**: 6 encoders empilhados
- **Decoder stack**: 6 decoders empilhados
- Conexões entre encoder e decoder

### Encoder (cada camada)
1. **Self-attention layer**: Olha outras palavras do input
2. **Feed-forward network**: Aplicado independentemente por posição

### Decoder (cada camada)
1. **Self-attention layer**
2. **Encoder-decoder attention**: Foca em partes relevantes do input
3. **Feed-forward network**

---

## 🔑 Self-Attention Explicado

### Intuição
> "The animal didn't cross the street because it was too tired"

- O que "it" refere? Animal ou rua?
- Self-attention permite associar "it" com "animal"

### Passo a Passo

1. **Criar Q, K, V**: Multiplicar embeddings por matrizes W^Q, W^K, W^V
2. **Calcular scores**: Q · K^T (dot product)
3. **Normalizar**: Dividir por √d_k, aplicar softmax
4. **Pesar valores**: Multiplicar V pelos pesos do softmax
5. **Somar**: Output é soma ponderada

### Fórmula

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

---

## 🎭 Multi-Head Attention

### Por que múltiplas heads?
1. **Foco em posições diferentes**: Cada head pode focar em diferentes partes
2. **Múltiplos representation subspaces**: Diferentes "visões" do input

### Implementação
- Transformer usa **8 attention heads**
- Cada head tem seus próprios W^Q, W^K, W^V
- Outputs concatenados e multiplicados por W^O

### Exemplo Visual
- Head 1: Foca em "the animal"
- Head 2: Foca em "tired"
- Combinação: "it" representa animal + tired

---

## 📍 Positional Encoding

### Problema
- Self-attention não tem noção de ordem
- Precisa de informação posicional

### Solução
- Adicionar vetor posicional ao embedding
- Padrão sinusoidal aprendido

### Fórmula
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

### Vantagem
- Permite extrapolação para sequências mais longas
- Padrão determinístico

---

## 🔗 Residual Connections

### Arquitetura
```
x → LayerNorm(x + Sublayer(x))
```

### Benefícios
1. **Gradiente**: Facilita backpropagation
2. **Training stability**: Normaliza ativações
3. **Deep networks**: Permite mais camadas

---

## 🎯 Decoder Side

### Diferença do Encoder
1. **Masked self-attention**: Não pode ver tokens futuros
2. **Encoder-decoder attention**: Q do decoder, K/V do encoder

### Geração
- Decoder gera token por token
- Cada passo vê todos os tokens anteriores
- Usa encoder outputs como K/V

---

## 📊 Dimensões Típicas

| Componente | Dimensão |
|------------|----------|
| Embedding | 512 |
| Q, K, V por head | 64 |
| Número de heads | 8 |
| FFN inner | 2048 |

---

## 💡 Conceitos-Chave

1. **Self-attention é O(n²)**: Cada token atende a todos
2. **Posição não é nativa**: Precisa de encoding explícito
3. **Multi-head é crítico**: Múltiplas "visões"
4. **Residual connections**: Essenciais para deep networks
5. **Paralelização**: Todos os tokens processados simultaneamente

---

## 📚 Referências

1. Attention Is All You Need (Vaswani et al., 2017)
2. Tensor2Tensor implementation
3. Harvard NLP annotated PyTorch guide

---

## 🔗 Próximos Passos

- [ ] Ler paper original "Attention Is All You Need"
- [ ] Implementar transformer from scratch
- [ ] Estudar variantes modernas (multi-query attention, RoPE)

---

## 📝 Tags

`#transformer` `#attention` `#visual-guide` `#explained` `#architecture` `#tutorial`