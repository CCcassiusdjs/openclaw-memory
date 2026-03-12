# Lifetimes - Validating References

**Source:** https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
**Category:** Lifetimes & Borrow Checker
**Priority:** ★★★★★ Essencial
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

Lifetimes são genéricos que garantem que references são válidas pelo tempo necessário. O borrow checker compara scopes para garantir que todas as borrows são válidas. Previne dangling references em compile-time.

---

## Conceitos-Chave

### 1. O Problema: Dangling References
```rust
fn main() {
    let r;

    {
        let x = 5;
        r = &x;  // ERROR: x não vive o suficiente
    }

    println!("r: {r}");  // r referencia memória desalocada
}
```

**Erro:**
```
error[E0597]: `x` does not live long enough
 --> src/main.rs:6:13
  |
5 | let x = 5;
  |     - binding `x` declared here
6 | r = &x;
  |      ^^ borrowed value does not live long enough
7 | }
  | - `x` dropped here while still borrowed
```

### 2. Borrow Checker
O borrow checker compara scopes das variáveis:

```rust
fn main() {
    let r;                // ---------+-- 'a
                          //          |
    {                     //          |
        let x = 5;        // -+-- 'b  |
        r = &x;           //  |       |
    }                     // -+       |
                          //          |
    println!("r: {r}");   //          |
}                         // ---------+
```

- `'a` = lifetime de `r`
- `'b` = lifetime de `x`
- `'b` é menor que `'a` → **ERRO!**

**Solução:**
```rust
fn main() {
    let x = 5;            // ----------+-- 'b
                          //           |
    let r = &x;           // --+-- 'a  |
                          //   |       |
    println!("r: {r}");   //   |       |
                          // --+       |
}                         // ----------+
```

Agora `'b` é maior que `'a` → **OK!**

### 3. Lifetime Annotation Syntax
```rust
&i32        // reference sem lifetime explícito
&'a i32     // reference com lifetime 'a
&'a mut i32 // mutable reference com lifetime 'a
```

**Sintaxe:**
- Começa com apóstrofo `'`
- Geralmente lowercase e curto (`'a`, `'b`)
- Colocado após o `&`

### 4. Generic Lifetimes in Functions
```rust
// ERRO: Rust não sabe qual reference é retornada
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}
```

**Erro:**
```
error[E0106]: missing lifetime specifier
 --> src/main.rs:9:33
  |
9 | fn longest(x: &str, y: &str) -> &str {
  |           ----  ---- ^ expected named lifetime parameter
```

**Solução:**
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

**O que isso significa:**
- Para algum lifetime `'a`
- `x` e `y` vivem pelo menos `'a`
- O retorno vive pelo menos `'a`
- Lifetime concreto = **menor** dos dois

### 5. Lifetime Elision Rules
O Rust tem regras para inferir lifetimes automaticamente:

**Regras:**
1. Cada parâmetro de reference recebe seu próprio lifetime
2. Se há exatamente um input lifetime, ele é atribuído a todos os outputs
3. Se há `&self` ou `&mut self`, seu lifetime é atribuído a todos os outputs

**Exemplos:**
```rust
// Regra 1 & 2: Um parâmetro
fn first_word(s: &str) -> &str { ... }
// Elided to:
fn first_word<'a>(s: &'a str) -> &'a str { ... }

// Regra 1: Múltiplos parâmetros (precisa de annotation)
fn longest(x: &str, y: &str) -> &str { ... }  // ERRO!

// Regra 3: Métodos
impl MyStruct {
    fn method(&self, s: &str) -> &str { ... }
    // Elided to:
    fn method<'a, 'b>(&'a self, s: &'b str) -> &'a str { ... }
}
```

### 6. Structs com Lifetimes
```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().expect("Could not find a '.'");
    let i = ImportantExcerpt {
        part: first_sentence,
    };
}
```

**Regra:** Struct que contém references precisa de lifetime annotation.

### 7. Lifetime Subtyping
```rust
// 'a: 'b significa "'a vive pelo menos tanto quanto 'b"
fn longest<'a>(x: &'a str, y: &str) -> &'a str {
    x  // y não tem relação com retorno, sem lifetime
}
```

### 8. Static Lifetime
```rust
// 'static: vive durante todo o programa
let s: &'static str = "I have a static lifetime.";
```

String literals têm lifetime `'static` porque estão no binário.

---

## Padrões Importantes

### Pattern: Function Returns Reference to Input
```rust
fn get_first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}
// Elided: fn get_first_word<'a>(s: &'a str) -> &'a str
```

### Pattern: Multiple References, Return One
```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
// Lifetime do retorno = menor dos dois
```

### Pattern: Struct Holding References
```rust
struct Parser<'a> {
    input: &'a str,
    position: usize,
}
```

### Pattern: Lifetime Annotations em impl
```rust
impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }

    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part
    }
}
```

---

## Insights para Systems Programming

1. **Compile-time Guarantee:** Lifetimes são verificados em compile-time, sem runtime cost
2. **No Dangling Pointers:** Rust garante que references nunca apontam para memória inválida
3. **Zero-cost Abstraction:** Lifetime annotations não afetam o código gerado
4. **Borrow Checker:** Analisa scopes para garantir validade
5. **Elision Rules:** Maioria das funções não precisam de annotations explícitas
6. **Struct Holding References:** Precisam de lifetime parameters

---

## Common Errors

### Error: Return Reference from Created Value
```rust
fn longest<'a>(x: &str, y: &str) -> &'a str {
    let result = String::from("really long string");
    result.as_str()  // ERROR: retorna reference para valor local
}
```

**Solução:** Retorne owned value:
```rust
fn longest(x: &str, y: &str) -> String {
    String::from("really long string")
}
```

### Error: Reference Outlives Data
```rust
fn main() {
    let string1 = String::from("long string is long");
    let result;
    {
        let string2 = String::from("xyz");
        result = longest(string1.as_str(), string2.as_str());
    }
    println!("The longest string is {result}");  // ERROR: string2 morto
}
```

---

## Próximos Passos

1. Estudar Non-Lexical Lifetimes (NLL)
2. Ver como closures capturam references
3. Entender Higher-Ranked Trait Bounds (HRTBs)

---

**Conceitos aprendidos:** 6
- Dangling references prevention
- Borrow checker
- Lifetime annotation syntax ('a)
- Lifetime elision rules
- Structs with lifetimes
- 'static lifetime