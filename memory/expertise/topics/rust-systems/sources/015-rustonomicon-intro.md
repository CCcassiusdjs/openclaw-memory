# The Rustonomicon - Introduction

**Source:** The Rustonomicon (Official Rust Documentation)
**URL:** https://doc.rust-lang.org/nomicon/
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

The "Dark Arts of Unsafe Rust" - official guide to writing unsafe code, understanding memory model, and building safe abstractions over unsafe primitives.

---

## Warning

> "THE KNOWLEDGE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF UNLEASHING INDESCRIBABLE HORRORS THAT SHATTER YOUR PSYCHE AND SET YOUR MIND ADRIFT IN THE UNKNOWABLY INFINITE COSMOS."

**This book is for those who need to write unsafe code or understand Rust's internals.**

---

## Scope

### Topics Covered

| Topic | Description |
|-------|-------------|
| **(Un)safety meaning** | What makes code safe or unsafe |
| **Unsafe primitives** | Raw pointers, unions, unchecked operations |
| **Safe abstractions** | Building safe APIs over unsafe code |
| **Subtyping and variance** | Lifetime relationships |
| **Exception safety** | Panic/unwind safety |
| **Uninitialized memory** | Working with uninit data |
| **Type punning** | Reinterpreting memory |
| **Concurrency** | Thread safety, atomics, memory ordering |
| **FFI** | Interfacing with other languages |
| **Optimization** | Performance tricks |
| **Compiler/OS/hardware** | Low-level primitives |

---

## What This Book Is NOT

- **Not a tutorial**: Assumes considerable Rust knowledge
- **Not exhaustive std reference**: Doesn't describe every API
- **Not complete**: Book is still being written

### Prerequisites

- Comfortable with systems programming
- Comfortable with Rust basics
- Read The Book first if new to Rust

---

## Safe vs Unsafe

### The Boundary

**Safe Rust:**
- Memory safety guaranteed by compiler
- No undefined behavior
- Type system enforces invariants

**Unsafe Rust:**
- Compiler trusts you
- No safety guarantees
- Can cause undefined behavior
- Used to build safe abstractions

### Why Unsafe Exists

> "Unsafe blocks and privacy allow us to dip into raw pointer manipulation to build these zero cost abstractions."

**This is the foundation for all other abstractions.**

---

## Key Concepts Preview

### Undefined Behavior

Actions that cause programs to behave unpredictably:
- Accessing uninitialized memory
- Null pointer dereference
- Data races
- Violating aliasing rules

### Safety Invariants

When writing unsafe code, you must:
- Document what invariants you're maintaining
- Ensure safe API can't violate them
- Minimize unsafe surface area

### The Safety Contract

```rust
/// # Safety
/// - ptr must be valid for reads
/// - ptr must be properly aligned
/// - ptr must point to initialized T
pub unsafe fn read<T>(ptr: *const T) -> T {
    // Implementation
}
```

**Safety documentation is required for all unsafe functions.**

---

## Variance and Subtyping

### Why It Matters

Lifetimes and references have subtyping relationships:
- `&'static str` is a subtype of `&'a str`
- Variance determines when substitution is safe
- Critical for understanding lifetime inference

### Types of Variance

| Variance | Meaning |
|----------|---------|
| Covariant | Can accept subtypes |
| Contravariant | Can accept supertypes |
| Invariant | Can't accept other types |

---

## Exception Safety

### Panic Safety

When code panics:
- Stack unwinds
- Destructors run
- Invariants might be violated

**Unsafe code must handle panics correctly.**

---

## FFI (Foreign Function Interface)

### Calling C from Rust

```rust
extern "C" {
    fn strlen(s: *const c_char) -> size_t;
}
```

### Calling Rust from C

```rust
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## Key Takeaways

1. **Unsafe is powerful**: Foundation for safe abstractions
2. **Safety contract**: Document all invariants
3. **Minimize unsafe**: Small surface area, well-tested
4. **Variance matters**: Understand lifetime subtyping
5. **Exception safety**: Handle panics correctly
6. **FFI bridge**: Interface with C and other languages
7. **This is advanced**: Requires solid Rust foundation

---

## Cross-References

- Related to: [[007-unsafe-rust-intro]] (unsafe basics)
- Related to: [[008-ffi]] (FFI details)
- Related to: [[005-lifetimes]] (variance)
- Related to: [[012-zero-cost-abstractions-boats]] (unsafe as foundation)