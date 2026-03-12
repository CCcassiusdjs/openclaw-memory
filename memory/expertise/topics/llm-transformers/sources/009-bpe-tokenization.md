# 009 - Byte-Pair Encoding (BPE) Tokenization

**Fonte:** https://huggingface.co/learn/llm-course/en/chapter6/5
**Autor:** Hugging Face NLP Course
**Tipo:** Tutorial
**Relevância:** ★★★★☆ (Tokenização)
**Status:** `completed`
**Lido em:** 2026-03-12

---

## 📋 Resumo

BPE (Byte-Pair Encoding) é o algoritmo de tokenização mais utilizado em LLMs modernos (GPT, GPT-2, RoBERTa, BART, DeBERTa). Começa com caracteres individuais e aprende merges (fusões) iterativamente baseado na frequência.

---

## 🔄 Algoritmo de Treinamento

### Passos
1. **Normalização**: Lowercase, strip accents, etc.
2. **Pre-tokenização**: Divide em palavras
3. **Vocabulário base**: Todos os caracteres únicos
4. **Merges iterativos**: Encontra par mais frequente e merge

### Exemplo de Treinamento
```
Corpus: "hug" (10), "pug" (5), "pun" (12), "bun" (4), "hugs" (5)

Vocab inicial: ["b", "g", "h", "n", "p", "s", "u"]

Passo 1: ("u", "g") → "ug"  (20 ocorrências)
Vocab: [..., "ug"]

Passo 2: ("u", "n") → "un"  (16 ocorrências)
Vocab: [..., "un"]

Passo 3: ("h", "ug") → "hug" (15 ocorrências)
Vocab: [..., "hug"]

...continua até tamanho desejado
```

---

## 🎯 Tokenização

### Processo
1. Pre-tokenizar texto em palavras
2. Separar cada palavra em caracteres
3. Aplicar merge rules na ordem aprendida

### Exemplo
```
Merges: ("u", "g") → "ug", ("u", "n") → "un", ("h", "ug") → "hug"

"bug" → ["b", "ug"]
"mug" → ["[UNK]", "ug"]  # "m" não está no vocab
"thug" → ["[UNK]", "hug"]
"unhug" → ["un", "hug"]
```

---

## 📊 Byte-Level BPE

### Inovação do GPT-2
- Em vez de caracteres Unicode, usa **bytes**
- Vocabulário base: 256 (todos os bytes)
- Nunca gera token [UNK]
- Qualquer texto pode ser tokenizado

### Vantagens
- Vocabulário pequeno e fixo
- Cobertura completa de caracteres
- Sem tokens desconhecidos

---

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Merge Rule** | Regra de fusão aprendida (par → novo token) |
| **Vocabulary Size** | Tamanho final do vocabulário |
| **Base Vocabulary** | Conjunto inicial de tokens (caracteres ou bytes) |
| **[UNK] Token** | Token para caracteres não vistos |
| **Byte-Level BPE** | Usa bytes em vez de caracteres |
| **Subword Tokenization** | Divide em unidades menores que palavras |

---

## 🔧 Implementação (Conceitual)

```python
# Calcular frequência de pares
def compute_pair_freqs(splits):
    pair_freqs = defaultdict(int)
    for word, freq in word_freqs.items():
        split = splits[word]
        if len(split) == 1:
            continue
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            pair_freqs[pair] += freq
    return pair_freqs

# Merge par
def merge_pair(a, b, splits):
    for word in word_freqs:
        split = splits[word]
        if len(split) == 1:
            continue
        i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                split = split[:i] + [a + b] + split[i + 2:]
            else:
                i += 1
        splits[word] = split
    return splits

# Tokenizar novo texto
def tokenize(text):
    pre_tokenized = pre_tokenize(text)
    splits = [[c for c in word] for word in pre_tokenized]
    for pair, merge in merges.items():
        for split in splits:
            i = 0
            while i < len(split) - 1:
                if split[i] == pair[0] and split[i + 1] == pair[1]:
                    split = split[:i] + [merge] + split[i + 2:]
                else:
                    i += 1
    return sum(splits, [])
```

---

## 📝 Notas Pessoais

### Por que BPE?
- **Flexibilidade**: Lida com palavras raras via subwords
- **Eficiência**: Vocabulário menor que word-level
- **Generalização**: Palavras similares compartilham subwords
- **Universalidade**: Qualquer texto pode ser tokenizado

### Comparação com Outros Métodos
| Método | Vocab Size | OOV | Exemplo |
|--------|------------|-----|---------|
| **Word-level** | Grande | Sim | "running" → [UNK] |
| **Character-level** | Pequeno | Não | "running" → ["r","u","n","n","i","n","g"] |
| **BPE** | Médio | Não | "running" → ["run", "ning"] |
| **Byte-level BPE** | Fixo (256+) | Não | Qualquer texto |

### Uso em LLMs Modernos
- **GPT-2/3/4**: Byte-level BPE
- **LLaMA**: SentencePiece BPE
- **Mistral**: SentencePiece BPE
- **Claude**: BPE variant

---

## 🎯 Próxima Fonte

Ler **"Decoder-Only Transformers: The Workhorse of Generative LLMs"** para completar arquitetura.