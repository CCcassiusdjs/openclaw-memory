# The Slice Type

**Source:** https://doc.rust-lang.org/book/ch04-03-slices.html
**Category:** Documentação Oficial
**Priority:** ★★★★★ Essencial
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

Slices são referências para uma sequência contígua de elementos de uma coleção. Não têm ownership - apenas apontam para parte dos dados. Resolvem o problema de índices que podem se tornar inválidos.

---

## Conceitos-Chave

### 1. O Problema dos Índices
```rust
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }
    s.len()
}

fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);  // word = 5
    
    s.clear();  // s agora é ""
    
    // word ainda é 5, mas s está vazio!
    // BUG: índice não está mais válido
}
```

**Problema:** O índice `5` não tem conexão com a String original.

### 2. String Slices
```rust
let s = String::from("hello world");

let hello = &s[0..5];   // "hello"
let world = &s[6..11];  // "world"
```

**Sintaxe:** `&s[starting_index..ending_index]`
- `starting_index` é o primeiro elemento
- `ending_index` é UM a mais que o último elemento

**Internalamente:** Slice armazena:
- Pointer para a posição inicial
- Length (número de elementos)

### 3. Range Syntax Sugar
```rust
let s = String::from("hello");

// Começando de 0
let slice = &s[0..2];
let slice = &s[..2];     // equivalente

// Indo até o final
let slice = &s[3..s.len()];
let slice = &s[3..];     // equivalente

// Slice completo
let slice = &s[0..s.len()];
let slice = &s[..];      // equivalente
```

### 4. Slices Resolvem o Bug
```rust
fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    &s[..]
}

fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);
    
    s.clear();  // ERROR!
    
    println!("the first word is: {word}");
}
```

**Erro:**
```
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
```

O borrow checker garante que:
- `word` é uma reference imutável ao slice de `s`
- `s.clear()` precisa de uma reference mutável
- **Não pode ter mutable e immutable ao mesmo tempo!**

### 5. String Literals são Slices
```rust
let s = "Hello, world!";
// s: &str
```

String literals são slices que apontam para dados dentro do binário. Por isso são imutáveis.

### 6. API Idiomática: `&str` em vez de `&String`
```rust
// Menos flexível
fn first_word(s: &String) -> &str { ... }

// Mais flexível (idiomático)
fn first_word(s: &str) -> &str { ... }

// Funciona com:
let my_string = String::from("hello world");
first_word(&my_string[0..6]);  // slice de String
first_word(&my_string[..]);   // slice completo
first_word(&my_string);       // reference a String

let my_literal = "hello world";
first_word(&my_literal[0..6]);  // slice de &str
first_word(my_literal);         // &str diretamente
```

### 7. Other Slices
```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];  // [2, 3]
// tipo: &[i32]
```

Arrays também suportam slices!

---

## Padrões Importantes

### Pattern: Slice Parameter
```rust
// Sempre prefira &str sobre &String em parâmetros
fn process(s: &str) -> &str { ... }
```

### Pattern: Return Slice from Function
```rust
fn find_substring(s: &str, pattern: &str) -> Option<&str> {
    // Retorna slice do input, lifetime é preservado
    s.find(pattern).map(|i| &s[i..])
}
```

### Pattern: Avoid Index Invalidation
```rust
// RUIM: usa índices
fn bad(data: &String) -> usize { ... }

// BOM: usa slice
fn good(data: &str) -> &str { ... }
```

---

## Insights para Systems Programming

1. **Compile-time Safety:** Slices previnem índices inválidos em compile-time
2. **Zero-cost:** Slices são apenas (pointer, length) em runtime
3. **Lifetime Tracking:** O compilador rastreia o lifetime do slice automaticamente
4. **Deref Coercion:** `&String` pode ser usado onde `&str` é esperado
5. **Generalized:** Slices funcionam com qualquer coleção (arrays, vectors, strings)

---

## Estrutura de Dados

```
Slice interno (fat pointer):
+---------------+---------------+
| pointer       | length        |
+---------------+---------------+
| 8 bytes       | 8 bytes       |
+---------------+---------------+
Total: 16 bytes (em arquitetura 64-bit)
```

---

## Comparação com C/C++

| Feature | C/C++ | Rust |
|---------|-------|------|
| String view | `std::string_view` (C++17) | `&str` |
| Array view | Manual pointers | `&[T]` |
| Bounds checking | Opcional | Obrigatório em debug, otimizado em release |
| Lifetime tracking | Manual | Compiler |

---

## Próximos Passos

1. Estudar Lifetimes (Ch 10)
2. Entender Deref Coercion (Ch 15)
3. Ver como slices funcionam com Iterators (Ch 13)

---

**Conceitos aprendidos:** 4
- Slice type (&str, &[T])
- Range syntax (start..end)
- Slice prevents index invalidation
- &str vs &String parameter idiom