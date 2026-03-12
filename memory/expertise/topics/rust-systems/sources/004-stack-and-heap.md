# The Stack and the Heap

**Source:** https://doc.rust-lang.org/1.22.0/book/first-edition/the-stack-and-the-heap.html
**Category:** Memory Management
**Priority:** ★★★★★ Fundamental
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

Stack e Heap são abstrações para gerenciamento de memória. Stack é rápido mas limitado (local a função). Heap é mais lento mas flexível (ilimitado, globalmente acessível). Rust stack-allocate por default.

---

## Conceitos-Chave

### 1. Comparação Stack vs Heap

| Característica | Stack | Heap |
|----------------|-------|------|
| Velocidade | Muito rápido | Mais lento |
| Alocação | Automática (stack frame) | Explícita (Box::new) |
| Tamanho | Limitado | Praticamente ilimitado |
| Escopo | Local à função | Globalmente acessível |
| Desalocação | Automática (fim do escopo) | Via Drop trait |

### 2. Stack Frames
```rust
fn main() {
    let x = 42;  // Stack frame alocado para main()
}  // Stack frame desalocado automaticamente
```

**Como funciona:**
1. Função chamada → Stack frame alocado
2. Variáveis locais → Dentro do stack frame
3. Função termina → Stack frame desalocado (tudo de uma vez)

**Por que é rápido:**
- Alocação: "grab the memory all at once"
- Desalocação: "get rid of it very fast too"

### 3. Stack Growth (LIFO)
```
fn foo() {
    let y = 5;
    let z = 100;
}

fn main() {
    let x = 42;
    foo();
}
```

**Memory Layout:**
```
Address    Name    Value
---------------------------------
2          z       100
1          y       5
0          x       42       ← main()'s frame
```

**Importante:** Stack cresce para cima (endereços maiores). Como pratos empilhados: Last In, First Out (LIFO).

### 4. Heap Allocation com Box<T>
```rust
fn main() {
    let x = Box::new(5);
    let y = 42;
}
```

**Memory Layout:**
```
Address              Name    Value
-----------------------------------------
(2^30) - 1           5       ← Heap
...                  ...     ...
1                    y       42
0                    x       → (2^30) - 1
```

**Key Points:**
- `x` no stack contém um pointer para o heap
- Valor `5` está no heap (endereço alto)
- Heap cresce do "outro lado" da memória

### 5. Heap Fragmentation
```
Address              Name    Value
-----------------------------------------
(2^30) - 1           5       ← Alocado
(2^30) - 2           -       ← Livre (hole)
(2^30) - 3           -       ← Livre (hole)
(2^30) - 4           42      ← Alocado
...                  ...     ...
2                    z       → (2^30) - 4
1                    y       42
0                    x       → (2^30) - 1
```

**Fragmentação:** Heap pode ter "buracos" devido a alocação/desalocação em qualquer ordem.

### 6. Drop Trait
```rust
fn main() {
    let x = Box::new(5);
}  // x sai do escopo → Drop::drop(&mut x) → libera memória do heap
```

**RAII:** Rust garante que `Box<T>` libera memória do heap quando sai do escopo.

### 7. Arguments and Borrowing
```rust
fn foo(i: &i32) {
    let z = 42;
}

fn main() {
    let x = 5;
    let y = &x;
    foo(y);
}
```

**Memory Layout:**
```
Address    Name    Value
---------------------------------
3          z       42
2          i       → 0      ← Copy do reference
1          y       → 0      ← Reference para x
0          x       5
```

**Key Points:**
- Arguments são copiados no stack frame
- References são pointers (copiados como valores)
- Borrowing NÃO aloca nova memória - apenas pointer

---

## Exemplo Complexo Completo

```rust
fn foo(x: &i32) {
    let y = 10;
    let z = &y;
    baz(z);
    bar(x, z);
}

fn bar(a: &i32, b: &i32) {
    let c = 5;
    let d = Box::new(5);
    let e = &d;
    baz(e);
}

fn baz(f: &i32) {
    let g = 100;
}

fn main() {
    let h = 3;
    let i = Box::new(20);
    let j = &h;
    foo(j);
}
```

**Memory at deepest point (inside baz called from bar):**
```
Address              Name    Value
-----------------------------------------
(2^30) - 1           20      ← Heap (from main)
(2^30) - 2           5       ← Heap (from bar)
...                  ...     ...
12                   g       100
11                   f       → (2^30) - 2
10                   e       → 9
9                    d       → (2^30) - 2
8                    c       5
7                    b       → 4
6                    a       → 0
5                    z       → 4
4                    y       10
3                    x       → 0
2                    j       → 0
1                    i       → (2^30) - 1
0                    h       3
```

---

## Comparação com Outras Linguagens

| Language | Default Allocation | Memory Management |
|----------|-------------------|-------------------|
| Rust | Stack | Manual + Drop (RAII) |
| Go | Heap | Garbage Collector |
| Java | Heap | Garbage Collector |
| C | Stack/Heap (manual) | Manual (malloc/free) |
| C++ | Stack/Heap (manual) | Manual + RAII |

**Rust vs GC languages:**
- GC languages heap-allocate por default (boxing)
- Rust stack-allocates por default
- GC precisa de runtime, Rust é zero-cost

---

## Insights para Systems Programming

1. **Stack is always faster:** Prefer stack quando possível
2. **Box<T> for heap:** Use `Box::new()` para dados que precisam sobreviver ao escopo
3. **Drop is automatic:** Rust garante limpeza via RAII
4. **References are cheap:** Apenas copiam pointer (8 bytes)
5. **Heap fragmentation:** Entenda que heap pode ter "buracos"
6. **LIFO order:** Stack é Last In First Out

---

## Padrões Importantes

### Pattern: Prefer Stack
```rust
// BOM: Stack allocation
let x = 42;  // i32 no stack

// NECESSÁRIO: Heap allocation
let x = Box::new(42);  // i32 no heap
```

### Pattern: Ownership Transfer
```rust
fn create_data() -> Box<i32> {
    let x = Box::new(42);
    x  // Ownership transferido para caller
}
```

### Pattern: Borrowing Avoids Copy
```rust
fn process(data: &BigStruct) {
    // Apenas pointer passado (8 bytes)
    // Nenhuma alocação nova
}
```

---

## Próximos Passos

1. Estudar Smart Pointers (Box, Rc, Arc)
2. Entender Drop trait em detalhes
3. Ver como Vec<T> gerencia heap

---

**Conceitos aprendidos:** 5
- Stack frames e LIFO
- Heap allocation com Box<T>
- Memory fragmentation
- Drop trait e RAII
- References como pointers baratos