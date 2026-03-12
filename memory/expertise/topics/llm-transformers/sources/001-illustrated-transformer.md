# 001 - The Illustrated Transformer

**Fonte:** https://jalammar.github.io/illustrated-transformer/
**Autor:** Jay Alammar
**Tipo:** Blog Post (Visual Guide)
**Relevância:** ★★★★★ (Fundacional)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo

Este é o artigo didático fundamental sobre Transformers. Explica visualmente a arquitetura proposta no paper "Attention Is All You Need", sendo amplamente utilizado em cursos de Stanford, Harvard, MIT, CMU e Princeton.

---

## 🏗️ Arquitetura do Transformer

### Estrutura Geral
- **Encoder**: Stack de 6 encoders idênticos (não compartilham pesos)
- **Decoder**: Stack de 6 decoders idênticos
- **Fluxo**: Input → Encoders → Decoders → Output

### Encoder Components
Cada encoder tem 2 sub-layers:
1. **Self-Attention Layer**: Permite olhar outras palavras da sequência
2. **Feed-Forward Network**: Mesma rede aplicada independentemente em cada posição

### Decoder Components
Cada decoder tem 3 sub-layers:
1. **Masked Self-Attention**: Só pode olhar posições anteriores
2. **Encoder-Decoder Attention**: Queries do decoder, Keys/Values do encoder
3. **Feed-Forward Network**: Similar ao encoder

---

## 🔍 Self-Attention Mechanism

### Conceito Intuitivo
- Self-attention permite ao modelo relacionar palavras na mesma sentença
- Exemplo: "The animal didn't cross the street because **it** was too tired"
  - "it" é conectado a "animal" via self-attention

### Cálculo Vetorial
Para cada palavra, cria-se 3 vetores:
- **Query (Q)**: O que estou procurando
- **Key (K)**: O que eu ofereço
- **Value (V)**: O conteúdo real

### Passos do Self-Attention
1. Criar Q, K, V para cada palavra (multiplicar embedding por WQ, WK, WV)
2. Calcular score: dot product de Q com cada K
3. Dividir por √dk (estabilidade numérica)
4. Aplicar softmax (normalizar scores)
5. Multiplicar V pelos scores softmax
6. Somar os vetores ponderados → resultado

### Fórmula Matricial
```
Attention(Q, K, V) = softmax(QK^T / √dk) V
```

---

## 🎭 Multi-Head Attention

### Por que Múltiplas Cabeças?
1. **Múltiplas perspectivas**: Cada head pode focar em diferentes relações
2. **Subespaços de representação**: Diferentes projeções do embedding

### Implementação
- Paper original: 8 attention heads
- Cada head tem seus próprios WQ, WK, WV
- Saídas concatenadas e multiplicadas por WO

### Dimensões
- Embedding: 512
- Q/K/V por head: 64 (512/8 heads)
- Mantém complexidade similar ao single-head

---

## 📍 Positional Encoding

### Problema
- Transformer não tem noção de ordem/posição por si só
- Processa todas as posições em paralelo

### Solução
- Adiciona vetor posicional ao embedding
- Usa funções seno/cosseno:
  - PE(pos, 2i) = sin(pos / 10000^(2i/dmodel))
  - PE(pos, 2i+1) = cos(pos / 10000^(2i/dmodel))

### Vantagens
- Modelo pode aprender a atender por posição relativa
- Extrapoliza para sequências mais longas que as vistas no treino

---

## 🔄 Residual Connections & Layer Norm

### Arquitetura
Cada sub-layer tem:
1. **Residual connection**: x + Sublayer(x)
2. **Layer normalization**: LayerNorm(x + Sublayer(x))

### Benefícios
- Gradient flow mais suave
- Treino mais estável
- Permite redes mais profundas

---

## 🎯 Decoder Details

### Masked Self-Attention
- Positions futuras são mascaradas (set to -∞)
- Impede que o decoder "olhe" o futuro durante treino

### Encoder-Decoder Attention
- **Queries**: Vêm do decoder
- **Keys/Values**: Vêm do output do encoder
- Permite decoder focar em partes relevantes do input

---

## 📊 Output: Linear & Softmax

### Processo
1. Decoder output: vetor de floats (dimensão dmodel)
2. **Linear layer**: projeta para vocabulário (logits)
3. **Softmax**: converte em probabilidades
4. **Argmax**: seleciona palavra de maior probabilidade

### Treino
- Loss: Cross-entropy entre distribuição predita e target
- Backpropagation ajusta todos os pesos
- Teacher forcing: input real durante treino

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Self-Attention** | Mecanismo que permite relacionar palavras na mesma sequência |
| **Multi-Head** | Múltiplas atenções em paralelo para diferentes representações |
| **Positional Encoding** | Adiciona informação posicional ao embedding |
| **Encoder-Decoder Attention** | Decoder consulta encoder para informações relevantes |
| **Residual + LayerNorm** | Estabiliza treino em redes profundas |
| **Masked Attention** | Impede olhar o futuro no decoder |

---

## 🔗 Conexões com Tópicos Relacionados

- **Attention Is All You Need** (paper original)
- **GPT-2/3** (decoder-only Transformers)
- **BERT** (encoder-only Transformers)
- **RoPE** (evolução do positional encoding)

---

## 📝 Notas Pessoais

- Este artigo é didaticamente excelente para entender o básico
- A explicação visual de Q/K/V é muito clara
- Multi-head attention explicado de forma intuitiva
- Posicional encoding: sin/cos é uma abordagem, RoPE (estudado depois) é mais moderna
- Próximo passo: ler paper original para detalhes matemáticos completos

---

## 🎯 Próxima Fonte

Ler **"Attention Is All You Need"** (paper original) para detalhes matemáticos completos.