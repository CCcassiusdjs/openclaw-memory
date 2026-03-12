# Safe and Unsafe Rust - The Rustonomicon

**Source:** https://doc.rust-lang.org/nomicon/
**Category:** Unsafe Rust
**Priority:** ★★★★★ Advanced
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

Rust é duas linguagens: Safe Rust e Unsafe Rust. Safe Rust garante memory safety em compile-time. Unsafe Rust permite operações que o compilador não pode verificar, mas que podem ser necessárias para FFI, low-level abstractions, ou otimizações.

---

## Conceitos-Chave

### 1. A Separação Safe/Unsafe
Rust = Safe Rust + Unsafe Rust

**Safe Rust:**
- Garante type-safety e memory-safety
- Sem dangling pointers
- Sem use-after-free
- Sem Undefined Behavior (UB)
- É o "verdadeiro" Rust

**Unsafe Rust:**
- Permite operações "extra" que Safe Rust não permite
- Tem as mesmas regras e semânticas
- Requer auditoria manual
- Responsabilidade do programador

### 2. O Papel do `unsafe` Keyword
O `unsafe` keyword serve dois propósitos:
1. **Declarar contratos não verificados** (em functions/traits)
2. **Declarar que você verificou os contratos** (em blocks/impls)

### 3. unsafe fn
```rust
// unsafe fn: caller deve verificar documentação
unsafe fn dangerous() {
    // operações que podem causar UB
}

// Caller:
unsafe {
    dangerous();  // "Eu verifiquei que é seguro chamar aqui"
}
```

### 4. unsafe trait
```rust
// unsafe trait: implementor deve verificar contratos
unsafe trait UnsafeOrd {
    fn cmp(&self, other: &Self) -> Ordering;
}

// Implementor:
unsafe impl UnsafeOrd for MyType {
    fn cmp(&self, other: &Self) -> Ordering {
        // "Eu garanto que isso é uma ordem total"
    }
}
```

### 5. unsafe block
```rust
// unsafe block: "Eu verifiquei que é seguro"
let value: i32 = unsafe {
    *ptr.offset(5)  // Eu garanto que offset está in-bounds
};
```

### 6. unsafe impl
```rust
// unsafe impl: "Eu garanto que a implementação é correta"
unsafe impl Send for MyType {}
unsafe impl Sync for MyType {}
```

---

## Funções Unsafe na Standard Library

| Função | O que faz | Por que unsafe |
|--------|-----------|----------------|
| `slice::get_unchecked` | Indexing sem bounds check | Pode violar memory safety |
| `mem::transmute` | Reinterpreta bits | Bypass type safety |
| `ptr::offset` | Pointer arithmetic | Pode causar UB se out-of-bounds |
| FFI functions | Chama código C/C++ | Outra linguagem pode fazer qualquer coisa |

---

## Unsafe Traits

| Trait | Propósito | Por que unsafe |
|-------|-----------|----------------|
| `Send` | Tipo pode ser movido para outra thread | Thread safety é crítica |
| `Sync` | Tipo pode ser compartilhado entre threads | Thread safety é crítica |
| `GlobalAlloc` | Customiza allocator global | Gerencia toda memória do programa |

---

## A Propriedade de Soundness

**Fundamental:**
```
No matter what, Safe Rust can't cause Undefined Behavior.
```

Isso significa que código Safe Rust **nunca** pode causar UB, não importa o quão mal escrito seja.

### Trust Asymmetry

**Safe Rust confia em Unsafe Rust:**
- Safe Rust assume que Unsafe Rust está correto
- Se Unsafe Rust tem bugs, Safe Rust pode causar UB

**Unsafe Rust NÃO confia em Safe Rust:**
- Unsafe Rust deve ser robusto contra Safe Rust bugado
- Exemplo: `BTreeMap` não pode confiar que `Ord` está correto

### Exemplo: BTreeMap e Ord
```rust
// BTreeMap requer Ord (ordem total)
// Mas Ord é implementado em Safe Rust!
// Então BTreeMap não pode confiar que Ord é realmente total

// Se Ord estivesse errado:
// - Safe Rust: BTreeMap pode comportar erraticamente
// - Mas NUNCA causa Undefined Behavior
// - Unsafe Rust interno defende contra Ord bugado
```

---

## unsafe trait vs safe trait

**Quando marcar trait como unsafe?**
- Se código unsafe não pode defender contra implementação bugada
- Se o contrato é crítico demais para confiar em Safe Rust

**Exemplos:**
- `Send/Sync`: Thread safety é crítica, unsafe code não pode defender
- `GlobalAlloc`: Gerencia toda memória, bugs são catastróficos
- `Ord`: Safe Rust pode ter implementação bugada, mas BTreeMap se defende

---

## Padrões Importantes

### Pattern: Safe Wrapper for Unsafe
```rust
// Unsafe internals, safe interface
pub struct MyVec<T> {
    ptr: *mut T,
    len: usize,
    cap: usize,
}

impl<T> MyVec<T> {
    pub fn push(&mut self, elem: T) {
        // safe interface wraps unsafe internals
        if self.len == self.cap {
            unsafe { self.grow(); }
        }
        unsafe {
            ptr::write(self.ptr.add(self.len), elem);
        }
        self.len += 1;
    }
}
```

### Pattern: Auditing Unsafe Blocks
```rust
// SAFETY: ptr points to valid memory for len bytes
// SAFETY: offset is within bounds
unsafe {
    ptr.copy_to(dest, len);
}
```

### Pattern: Minimizar Unsafe
```rust
// RUIM: unsafe spread everywhere
fn process() {
    unsafe { /* ... */ }
    unsafe { /* ... */ }
    unsafe { /* ... */ }
}

// BOM: unsafe em uma função pequena e auditável
fn raw_process() {
    // SAFETY: documented invariants
    unsafe { /* ... */ }
}

fn process() {
    // Safe interface
    raw_process();
}
```

---

## Insights para Systems Programming

1. **Soundness Property:** Safe Rust nunca causa UB
2. **Trust Asymmetry:** Unsafe não confia em Safe
3. **Audit Required:** Código unsafe precisa auditoria manual
4. **Minimize Unsafe:** Menos unsafe = menos bugs
5. **Safe Wrappers:** Sempre encapsular unsafe em interfaces seguras
6. **Document Safety:** Usar `// SAFETY:` comments

---

## Comparação com C/C++

| Concept | C/C++ | Rust |
|---------|-------|------|
| Safety | Opcional | Default é Safe |
| UB | Comum | Apenas em unsafe |
| Bounds checking | Manual | Automático (exceto unsafe) |
| Null pointers | Permitido | Option<T> previne |
| Data races | Comum | Compile-time prevention |

---

## Próximos Passos

1. Estudar Undefined Behavior em detalhes
2. Ver raw pointers (*const, *mut)
3. Entender FFI com C
4. Estudar memory layout e repr

---

**Conceitos aprendidos:** 5
- Safe Rust vs Unsafe Rust
- unsafe keyword (fn, trait, block, impl)
- Soundness property
- Trust asymmetry
- When to mark traits unsafe