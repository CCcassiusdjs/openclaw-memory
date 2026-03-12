# References and Borrowing

**Source:** https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html
**Category:** Documentação Oficial
**Priority:** ★★★★★ Essencial
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

References permitem referenciar valores sem tomar ownership. Isso resolve o problema de ter que retornar valores quando só precisamos lê-los. O conceito de "borrowing" é fundamental para Rust: você pode pegar emprestado, mas não é seu.

---

## Conceitos-Chave

### 1. O que é uma Reference?
```rust
let s1 = String::from("hello");
let len = calculate_length(&s1);  // &s1 cria uma reference

fn calculate_length(s: &String) -> usize {
    s.len()
}  // s sai do escopo, mas NÃO é dropado (não é owner)
```

**Key points:**
- `&` cria uma reference
- Reference não é owner → não chama `drop` ao sair do escopo
- Reference é garantida apontar para valor válido durante sua vida

### 2. Borrowing
- **Definition:** Criar uma reference = "borrowing" (emprestar)
- Como na vida real: você pode pegar emprestado, mas tem que devolver
- Você não é dono do valor

### 3. References são Imutáveis por Default
```rust
fn change(some_string: &String) {
    some_string.push_str(", world");  // ERROR! Cannot modify borrowed value
}
```

### 4. Mutable References
```rust
fn main() {
    let mut s = String::from("hello");
    change(&mut s);
}

fn change(some_string: &mut String) {
    some_string.push_str(", world");  // OK!
}
```

**Restrição CRÍTICA:**
```rust
let mut s = String::from("hello");

let r1 = &mut s;
let r2 = &mut s;  // ERROR! Cannot have two mutable references at once!

println!("{}, {}", r1, r2);
```

### 5. Regra das References Mutáveis
**ONE BIG RESTRICTION:**
- Se você tem uma mutable reference, não pode ter outras references ao mesmo tempo
- Isso previne **data races** em compile-time!

**Data Race Definition:**
1. Dois ou mais pointers acessam o mesmo dado simultaneamente
2. Pelo menos um está escrevendo
3. Não há sincronização

### 6. Múltiplas References Imutáveis
```rust
let mut s = String::from("hello");

let r1 = &s;  // OK
let r2 = &s;  // OK - múltiplas imutáveis são permitidas
let r3 = &mut s;  // ERROR! Cannot have mutable while immutable exists

println!("{}, {}, and {}", r1, r2, r3);
```

### 7. Non-Lexical Lifetimes (NLL)
```rust
let mut s = String::from("hello");

let r1 = &s;
let r2 = &s;
println!("{} and {}", r1, r2);
// r1 e r2 não são mais usados depois deste ponto

let r3 = &mut s;  // OK! r1 e r2 já não são mais usados
println!("{}", r3);
```

O compilador sabe que r1 e r2 não são mais usados após o `println!`, então o escopo delas acaba ali (non-lexical).

### 8. Dangling References
Rust GARANTE que references nunca são "dangling":

```rust
fn dangle() -> &String {
    let s = String::from("hello");
    &s  // ERROR! s sai do escopo e é dropado
}  // Reference apontaria para memória liberada

// Solution: return owned value instead
fn no_dangle() -> String {
    let s = String::from("hello");
    s  // move ownership out
}
```

---

## As Regras de References

1. **Uma reference mutável OU várias imutáveis** (nunca ambas ao mesmo tempo)
2. **References sempre válidas** (sem dangling pointers)

---

## Padrões Importantes

### Pattern: Reference Scoping
```rust
let mut s = String::from("hello");

{
    let r1 = &mut s;
} // r1 sai do escopo, podemos criar nova reference

let r2 = &mut s;  // OK!
```

### Pattern: Read-Only Access
```rust
fn read_data(data: &Vec<u8>) -> usize {
    data.len()  // Múltiplas leituras OK
}
```

### Pattern: Mutable Access
```rust
fn modify_data(data: &mut Vec<u8>) {
    data.push(42);  // Apenas UMA reference mutável por vez
}
```

---

## Insights para Systems Programming

1. **Compile-time Data Race Prevention:** Rust detecta data races em compile-time, não runtime
2. **Zero-cost Abstraction:** References são apenas pointers em runtime
3. **Memory Safety:** Compiler garante que references nunca são dangling
4. **NLL (Non-Lexical Lifetimes):** Compiler é inteligente o suficiente para saber quando references não são mais usadas
5. **Imutabilidade por Default:** References são imutáveis, `&mut` é explícito

---

## Comparação com C/C++

| Feature | C/C++ | Rust |
|---------|-------|------|
| Multiple mutable pointers | ✅ Permitido | ❌ Compile error |
| Data races | ❌ Runtime crash | ✅ Compile-time error |
| Dangling pointers | ❌ Undefined behavior | ✅ Compile-time error |
| Reference validity | ❌ Manual | ✅ Compiler guarantee |

---

## Próximos Passos

1. Estudar Slices (Ch 4.3)
2. Entender Lifetimes em detalhes (Ch 10)
3. Ver como References funcionam com Structs (Ch 5)

---

**Conceitos aprendidos:** 4
- References (&T) vs Mutable References (&mut T)
- Borrowing semantics
- Data race prevention at compile-time
- Non-lexical lifetimes (NLL)
- Dangling reference prevention