# Async Book - Introduction

**Source:** Rust Async Working Group - "Asynchronous Programming in Rust"
**URL:** https://rust-lang.github.io/async-book/
**Date:** 2025
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Official guide to asynchronous programming in Rust, covering async/await, futures, and runtime concepts for beginners to advanced users.

---

## Key Concepts

### What is Async Programming?

- **Concurrency within the program**: Unlike threads, async tasks are managed by the runtime, not the OS
- **Fast context switching**: No kernel involvement, very fast
- **Low memory overhead**: Tasks are lightweight compared to OS threads
- **Fine-grained control**: Scheduling, parallelism, concurrency levels

### Async vs Threads

| Aspect | Threads | Async |
|--------|---------|-------|
| Management | OS kernel | User-space runtime |
| Memory | Higher (stack per thread) | Lower (per-task state) |
| Context switch | Kernel overhead | Fast (no kernel) |
| Best for | CPU-bound | I/O-bound, many tasks |

### When to Use Async

- High concurrency (many simultaneous tasks)
- I/O-heavy workloads (networking, file I/O)
- Microcontrollers with limited memory
- Systems without OS thread support

---

## Async Fundamentals

### Async Functions

```rust
async fn say_hello() {
    println!("hello, world!");
}

#[tokio::main]
async fn main() {
    say_hello().await;
}
```

Key points:
- `async fn` defines an asynchronous function
- `await` suspends execution until the future is ready
- Async functions do nothing unless awaited

### The .await Keyword

- Suspends the current task
- Yields control to the runtime
- No blocking: other tasks can run while waiting

---

## Async Runtime

### What is a Runtime?

- A crate that manages async tasks
- Not part of the standard library
- Tokio, async-std, smol are popular choices

### Runtime Responsibilities

1. **Task scheduling**: Deciding which task runs next
2. **I/O polling**: Managing network/file operations
3. **Timer management**: Sleep, timeouts
4. **Executor**: Running futures to completion

---

## Development Status

### Current State

- Async Rust is **stable and production-ready**
- Used at major tech companies
- Some rough edges remain

### Missing Parts

- Async iterators (streams) - rough ergonomics
- Async in traits - limited support
- Async destruction - no good solution yet

### Working Group

- Async Working Group roadmap available
- Active development continues
- Contributions welcome

---

## Key Takeaways

1. **Async = user-space concurrency**: No kernel involvement
2. **Lightweight tasks**: Lower memory and faster context switching
3. **I/O focus**: Best for I/O-bound, not CPU-bound workloads
4. **Runtime required**: Must choose one (Tokio, async-std, smol)
5. **Await is essential**: Async functions don't run without `.await`

---

## Book Structure

- **Part One**: Beginner's guide (read in order)
- **Part Two**: Advanced topics (stand-alone chapters)
- Topic index and detailed index available
- FAQs included

---

## Cross-References

- Related to: [[006-shared-state-concurrency]] (concurrency patterns)
- Related to: [[007-unsafe-rust-intro]] (async and unsafe)
- Related to: [[008-ffi.md]] (async FFI considerations)