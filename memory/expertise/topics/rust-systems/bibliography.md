# Rust Systems Programming - Bibliografia Completa

**Status:** researching
**Created:** 2026-03-12
**Last Updated:** 2026-03-12

---

## Organização por Categoria

As fontes estão organizadas por relevância e categoria para facilitar o estudo sistemático.

---

## 1. Documentação Oficial e Livros Fundamentais

### 1.1 The Rust Programming Language (The Book)
- **URL:** https://doc.rust-lang.org/book/
- **Tipo:** Livro oficial
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Linguagem completa, ownership, borrowing, lifetimes, traits, generics
- **Capítulos-chave:** Ch 4 (Ownership), Ch 10 (Generics/Lifetimes), Ch 15-20 (Advanced)

### 1.2 Rust By Example
- **URL:** https://doc.rust-lang.org/rust-by-example/
- **Tipo:** Tutorial interativo
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Exemplos práticos de todos os conceitos

### 1.3 The Rustonomicon (Unsafe Rust)
- **URL:** https://doc.rust-lang.org/nomicon/
- **Tipo:** Livro avançado
- **Prioridade:** ★★★★☆ Avançado
- **Conteúdo:** Unsafe Rust, FFI, memory layout, undefined behavior

### 1.4 The Embedded Rust Book
- **URL:** https://docs.rust-embedded.org/book/
- **Tipo:** Livro especializado
- **Prioridade:** ★★★★☆ Sistemas Embarcados
- **Conteúdo:** no_std, bare metal, microcontroladores

---

## 2. Memory Management & Ownership

### 2.1 Stack and Heap
- **URL:** https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html#the-stack-and-the-heap
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★★ Fundamental
- **Conteúdo:** Diferença entre stack e heap, ownership model

### 2.2 The Stack and the Heap (First Edition)
- **URL:** https://doc.rust-lang.org/1.22.0/book/first-edition/the-stack-and-the-heap.html
- **Fonte:** Rust Documentation
- **Prioridade:** ★★★★☆ Complementar
- **Conteúdo:** Explicação detalhada do modelo de memória

### 2.3 Heap Allocations - The Rust Performance Book
- **URL:** https://nnethercote.github.io/perf-book/heap-allocations.html
- **Fonte:** Rust Performance Book
- **Prioridade:** ★★★★☆ Otimização
- **Conteúdo:** Box<T>, Rc/Arc, alocação de heap e otimização

### 2.4 Memory Management in Rust: Stack vs. Heap
- **URL:** https://medium.com/@chenymj23/memory-whether-to-store-on-the-heap-or-the-stack-4ff33b2c1e5f
- **Fonte:** Medium
- **Prioridade:** ★★★☆☆ Tutorial
- **Conteúdo:** RODATA, heap, stack, Strings

---

## 3. Lifetimes & Borrow Checker

### 3.1 Validating References with Lifetimes
- **URL:** https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Lifetime syntax, lifetime elision, annotations

### 3.2 Lifetimes - Rust By Example
- **URL:** https://doc.rust-lang.org/rust-by-example/scope/lifetime.html
- **Fonte:** Rust By Example
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Exemplos práticos de lifetimes

### 3.3 Deep Dive into Rust Lifetimes
- **URL:** https://leapcell.io/blog/deep-dive-into-rust-lifetimes
- **Fonte:** Leapcell Blog
- **Prioridade:** ★★★★☆ Avançado
- **Conteúdo:** Borrow checker, memory management

### 3.4 The Borrow Checker Within (NLL)
- **URL:** https://smallcultfollowing.com/babysteps/blog/2024/06/02/the-borrow-checker-within/
- **Fonte:** Baby Steps Blog (Niko Matsakis)
- **Prioridade:** ★★★★☆ Internals
- **Conteúdo:** Non-lexical lifetimes, borrow checker internals

### 3.5 Inside the Borrow Checker: How Rust Validates Lifetimes in MIR
- **URL:** https://medium.com/@bugsybits/inside-the-borrow-checker-how-rust-validates-lifetimes-in-mir-721dce48a8ab
- **Fonte:** Medium
- **Prioridade:** ★★★☆☆ Internals
- **Conteúdo:** MIR, borrow checker implementation

---

## 4. Concurrency & Parallelism

### 4.1 Shared-State Concurrency
- **URL:** https://doc.rust-lang.org/book/ch16-03-shared-state.html
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Mutex<T>, Arc<T>, RwLock

### 4.2 Rust Atomics and Locks (Mara Bos)
- **URL:** https://mara.nl/atomics/
- **Fonte:** Book by Mara Bos
- **Prioridade:** ★★★★★ Livro
- **Conteúdo:** Atomics, memory ordering, locks, low-level concurrency

### 4.3 Rust Concurrency: 10 Patterns Beyond Locks
- **URL:** https://medium.com/@Nexumo_/rust-concurrency-10-patterns-beyond-locks-e1598e78e65e
- **Fonte:** Medium
- **Prioridade:** ★★★★☆ Padrões
- **Conteúdo:** Channels, atomics, ownership handoff, Rayon, ArcSwap

### 4.4 Concurrency - The Embedded Rust Book
- **URL:** https://docs.rust-embedded.org/book/concurrency/
- **Fonte:** Embedded Rust Book
- **Prioridade:** ★★★★☆ Embedded
- **Conteúdo:** Critical sections, mutex, SMP

---

## 5. Async Rust

### 5.1 Async Book
- **URL:** https://rust-lang.github.io/async-book/
- **Fonte:** Rust Async Working Group
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Futures, async/await, executors

### 5.2 Tokio Documentation
- **URL:** https://tokio.rs/tokio/tutorial
- **Fonte:** Tokio
- **Prioridade:** ★★★★★ Runtime
- **Conteúdo:** Async runtime, tasks, I/O

---

## 6. FFI (Foreign Function Interface)

### 6.1 FFI - The Rust Programming Language
- **URL:** https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html#using-extern-functions-to-call-external-code
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★☆ FFI
- **Conteúdo:** extern "C", calling conventions

### 6.2 FFI - Rust By Example
- **URL:** https://doc.rust-lang.org/rust-by-example/std_misc/ffi.html
- **Fonte:** Rust By Example
- **Prioridade:** ★★★★☆ FFI
- **Conteúdo:** Exemplos de FFI com C

### 6.3 FFI - The Rustonomicon
- **URL:** https://doc.rust-lang.org/nomicon/ffi.html
- **Fonte:** The Rustonomicon
- **Prioridade:** ★★★★☆ Avançado
- **Conteúdo:** Callbacks, wrappers, safety

### 6.4 std::ffi - Rust
- **URL:** https://doc.rust-lang.org/std/ffi/index.html
- **Fonte:** std Documentation
- **Prioridade:** ★★★☆☆ Referência
- **Conteúdo:** CString, CStr, OsString, FFI types

---

## 7. Error Handling

### 7.1 Recoverable Errors with Result
- **URL:** https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Result<T, E>, ? operator

### 7.2 Error Handling Best Practices in Rust
- **URL:** https://medium.com/@Murtza/error-handling-best-practices-in-rust-a-comprehensive-guide-to-building-resilient-applications-46bdf6fa6d9d
- **Fonte:** Medium
- **Prioridade:** ★★★☆☆ Best Practices
- **Conteúdo:** Result vs Option, error propagation

---

## 8. Zero-Cost Abstractions & Performance

### 8.1 Zero-Cost Abstractions in Rust
- **URL:** https://dockyard.com/blog/2025/04/15/zero-cost-abstractions-in-rust-power-without-the-price
- **Fonte:** DockYard Blog
- **Prioridade:** ★★★★☆ Performance
- **Conteúdo:** High-level features, no runtime overhead

### 8.2 Zero Cost Abstractions (without.boats)
- **URL:** https://without.boats/blog/zero-cost-abstractions/
- **Fonte:** without.boats
- **Prioridade:** ★★★★☆ Deep Dive
- **Conteúdo:** Ownership, borrowing, iterators, closures

### 8.3 The Rust Performance Book
- **URL:** https://nnethercote.github.io/perf-book/
- **Fonte:** Nicholas Nethercote
- **Prioridade:** ★★★★★ Otimização
- **Conteúdo:** Profiling, optimization, benchmarking

---

## 9. Generics & Traits

### 9.1 Generic Data Types
- **URL:** https://doc.rust-lang.org/book/ch10-01-syntax.html
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★★ Essencial
- **Conteúdo:** Generics, trait bounds

### 9.2 Monomorphization - Rust Compiler Development Guide
- **URL:** https://rustc-dev-guide.rust-lang.org/backend/monomorph.html
- **Fonte:** rustc-dev-guide
- **Prioridade:** ★★★★☆ Internals
- **Conteúdo:** How generics compile to concrete code

### 9.3 Item 12: Generics vs Trait Objects - Effective Rust
- **URL:** https://www.lurklurk.org/effective-rust/generics.html
- **Fonte:** Effective Rust
- **Prioridade:** ★★★★☆ Design
- **Conteúdo:** Static vs dynamic dispatch trade-offs

---

## 10. Macros & Metaprogramming

### 10.1 Macros - The Rust Programming Language
- **URL:** https://doc.rust-lang.org/book/ch20-05-macros.html
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★☆ Metaprogramming
- **Conteúdo:** Declarative and procedural macros

### 10.2 Macros in Rust: A Tutorial with Examples
- **URL:** https://blog.logrocket.com/macros-in-rust-a-tutorial-with-examples/
- **Fonte:** LogRocket Blog
- **Prioridade:** ★★★☆☆ Tutorial
- **Conteúdo:** macro_rules!, pattern matching

### 10.3 Procedural Macros in Rust
- **URL:** https://blog.logrocket.com/procedural-macros-in-rust/
- **Fonte:** LogRocket Blog
- **Prioridade:** ★★★☆☆ Advanced
- **Conteúdo:** Derive macros, attribute macros

---

## 11. Embedded & no_std

### 11.1 no_std - The Embedded Rust Book
- **URL:** https://docs.rust-embedded.org/book/intro/no-std.html
- **Fonte:** Embedded Rust Book
- **Prioridade:** ★★★★★ Embedded
- **Conteúdo:** Bare metal, no standard library

### 11.2 Awesome Embedded Rust
- **URL:** https://github.com/rust-embedded/awesome-embedded-rust
- **Fonte:** GitHub
- **Prioridade:** ★★★★☆ Resources
- **Conteúdo:** Curated list of embedded resources

---

## 12. Rust for Linux Kernel

### 12.1 Rusty Linux: Advances in Rust for Linux Kernel Development
- **URL:** https://arxiv.org/html/2407.18431v1
- **Fonte:** arXiv
- **Prioridade:** ★★★★★ Academic
- **Conteúdo:** Memory safety in kernel, ownership model for kernel development

### 12.2 Rust — The Linux Kernel Documentation
- **URL:** https://docs.kernel.org/rust/index.html
- **Fonte:** Linux Kernel Docs
- **Prioridade:** ★★★★★ Official
- **Conteúdo:** Quick start, kernel development in Rust

### 12.3 Rust for Linux
- **URL:** https://rust-for-linux.com/
- **Fonte:** Official Site
- **Prioridade:** ★★★★☆ Project
- **Conteúdo:** Adding Rust support to Linux kernel

### 12.4 Rust for embedded Linux kernels (LWN)
- **URL:** https://lwn.net/Articles/970216/
- **Fonte:** LWN.net
- **Prioridade:** ★★★★☆ Article
- **Conteúdo:** Writing kernel code in Rust

---

## 13. Unsafe Rust

### 13.1 The Rustonomicon
- **URL:** https://doc.rust-lang.org/nomicon/
- **Fonte:** Official
- **Prioridade:** ★★★★★ Advanced
- **Conteúdo:** Unsafe Rust, undefined behavior, memory layout

### 13.2 Unsafe Rust - The Book
- **URL:** https://doc.rust-lang.org/book/ch19-01-unsafe-rust.html
- **Fonte:** The Rust Book
- **Prioridade:** ★★★★★ Essential
- **Conteúdo:** Dereferencing raw pointers, unsafe functions

---

## 14. Academic Papers

### 14.1 Rusty Linux: Advances in Rust for Linux Kernel Development
- **URL:** https://arxiv.org/html/2407.18431v1
- **Fonte:** arXiv (July 2024)
- **Prioridade:** ★★★★★ Academic
- **DOI:** 10.1145/3674805.3690756
- **Conteúdo:** Memory safety guarantees in kernel context

---

## 15. Books (Paid)

### 15.1 Rust Atomics and Locks - Mara Bos
- **URL:** https://mara.nl/atomics/
- **Preço:** ~$50
- **Prioridade:** ★★★★★ Concurrency
- **Conteúdo:** Low-level concurrency in practice

### 15.2 Programming Rust - Jim Blandy, Jason Orendorff
- **Editora:** O'Reilly
- **Preço:** ~$60
- **Prioridade:** ★★★★★ Comprehensive
- **Conteúdo:** Fast systems programming

### 15.3 The Rust Programming Language - Steve Klabnik, Carol Nichols
- **Editora:** No Starch Press
- **Preço:** ~$50
- **Prioridade:** ★★★★★ Official
- **Conteúdo:** Complete language reference

---

## Progresso de Leitura

| Categoria | Total | Lidos | Progresso |
|-----------|-------|-------|-----------|
| Documentação Oficial | 4 | 0 | 0% |
| Memory Management | 4 | 0 | 0% |
| Lifetimes & Borrow Checker | 5 | 0 | 0% |
| Concurrency | 4 | 0 | 0% |
| Async | 2 | 0 | 0% |
| FFI | 4 | 0 | 0% |
| Error Handling | 2 | 0 | 0% |
| Zero-Cost Abstractions | 3 | 0 | 0% |
| Generics & Traits | 3 | 0 | 0% |
| Macros | 3 | 0 | 0% |
| Embedded | 2 | 0 | 0% |
| Linux Kernel | 4 | 0 | 0% |
| Unsafe Rust | 2 | 0 | 0% |
| Academic | 1 | 0 | 0% |
| **TOTAL** | **43** | **0** | **0%** |

---

## Próximos Passos

1. Começar com "The Rust Programming Language" (The Book) - Capítulos 1-10
2. Ler documentação de Ownership e Borrowing
3. Praticar com Rust By Example
4. Estudar Lifetimes em profundidade
5. Avançar para Concurrency e Unsafe Rust