# The Rust Programming Language - Ownership

**Source:** https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
**Category:** Documentação Oficial
**Priority:** ★★★★★ Essencial
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

Ownership é o conceito central do Rust que garante memory safety sem garbage collector. É baseado em três regras fundamentais:

1. **Cada valor tem um owner** (dono)
2. **Só pode haver um owner por vez**
3. **Quando o owner sai do escopo, o valor é dropado**

---

## Conceitos-Chave

### 1. Variable Scope
```rust
{                      // s is not valid here, not yet declared
    let s = "hello";   // s is valid from this point forward
    // do stuff with s
}                      // this scope is now over, s is no longer valid
```

### 2. String Type (Owned Data)
```rust
let s = String::from("hello");  // allocated on heap
```
- Strings podem crescer/diminuir → tamanho não conhecido em compile-time
- Precisam de alocação de heap
- `String` é owned data

### 3. Memory and Allocation
- **Stack:** tamanho fixo, cópia barata (inteiros, floats, bools, chars)
- **Heap:** tamanho dinâmico, precisa de gerenciamento

Rust resolve alocação/desalocação automaticamente:
- Quando `String` é criada: aloca memória
- Quando owner sai do escopo: `drop` é chamado automaticamente

### 4. Move Semantics
```rust
let s1 = String::from("hello");
let s2 = s1;  // s1 MOVED to s2 - s1 is now invalid!

println!("{}, world!", s1);  // ERROR: value borrowed here after move
```

**Por que move?**
- Copiar dados do heap é caro
- Rust invalida a variável anterior automaticamente
- Previne "double free" bugs

### 5. Clone (Deep Copy)
```rust
let s1 = String::from("hello");
let s2 = s1.clone();  // explicit deep copy

println!("s1 = {}, s2 = {}", s1, s2);  // Both valid!
```

### 6. Stack-Only Data: Copy Trait
Tipos que implementam `Copy`:
- Todos tipos inteiros (`i32`, `u8`, etc.)
- Tipos de ponto flutuante (`f64`, etc.)
- `bool`
- `char`
- Tuplas (se todos elementos forem `Copy`)
  - `(i32, i32)` é `Copy`
  - `(i32, String)` NÃO é `Copy`

```rust
let x = 5;
let y = x;  // x is still valid! Copy is cheap (stack-only)
```

### 7. Ownership and Functions
```rust
fn main() {
    let s = String::from("hello");  // s comes into scope
    takes_ownership(s);              // s's value moves into the function
                                     // s is no longer valid here
    
    let x = 5;                       // x comes into scope
    makes_copy(x);                    // x would move into the function
                                     // but i32 is Copy, so x is still valid
} // x goes out of scope, then s. But s was moved, so nothing happens to s.

fn takes_ownership(some_string: String) {
    println!("{}", some_string);
} // some_string goes out of scope and `drop` is called.

fn makes_copy(some_integer: i32) {
    println!("{}", some_integer);
} // some_integer goes out of scope. Nothing special happens.
```

### 8. Return Values and Scope
```rust
fn gives_ownership() -> String {
    let some_string = String::from("yours");
    some_string  // some_string is returned and moves out to the caller
}

fn takes_and_gives_back(a_string: String) -> String {
    a_string  // a_string is returned and moves out to the caller
}
```

---

## Padrões Importantes

### Taking Ownership → Returning Ownership
```rust
let s1 = gives_ownership();        // gives_ownership moves its return value into s1
let s2 = String::from("hello");    // s2 comes into scope
let s3 = takes_and_gives_back(s2); // s2 is moved into takes_and_gives_back
                                   // which also moves its return value into s3
```

### The Problem (solved by references)
```rust
fn main() {
    let s1 = String::from("hello");
    let (s2, len) = calculate_length_and_return(s1);  // Ugly workaround!
    println!("The length of '{}' is {}.", s2, len);
}

fn calculate_length_and_return(s: String) -> (String, usize) {
    let length = s.len();
    (s, length)
}
```

---

## Insights para Systems Programming

1. **Zero-cost abstraction:** Ownership é verificado em compile-time, sem runtime overhead
2. **Memory safety sem GC:** Rust previne use-after-free, double-free, dangling pointers
3. **Move semantics:** Evita cópias desnecessárias de dados do heap
4. **Copy trait:** Tipos "baratos" são copiados automaticamente
5. **RAII:** Resource Acquisition Is Initialization - recursos são limpos automaticamente ao sair do escopo

---

## Conceitos Relacionados

- Borrowing & References (Ch 4.2)
- Slices (Ch 4.3)
- Lifetimes (Ch 10)
- Smart Pointers (Ch 15)

---

## Próximos Passos

1. Estudar Borrowing & References
2. Entender Slices
3. Aprofundar em Lifetimes
4. Ver Smart Pointers (Box, Rc, Arc)

---

**Conceitos aprendidos:** 5
- Ownership model (3 regras)
- Move semantics
- Clone vs Copy
- Stack vs Heap allocation
- Function ownership transfer