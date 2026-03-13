# Tokio Runtime - Async Platform

**Source:** Tokio Documentation
**URL:** https://docs.rs/tokio/latest/tokio/
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Tokio is an event-driven, non-blocking I/O platform for writing async Rust applications. Provides runtime, task scheduler, I/O driver, and async primitives.

---

## Core Components

### 1. Runtime
- Task scheduler (work-stealing)
- I/O driver (epoll, kqueue, IOCP)
- High-performance timer

### 2. Tasks
- `tokio::spawn` for scheduling
- `JoinHandle` for awaiting results
- `spawn_blocking` for CPU-bound work

### 3. Sync Primitives
- Channels: oneshot, mpsc, watch, broadcast
- Async Mutex (non-blocking)
- Barrier for multi-task sync

### 4. Time
- `sleep()` for delays
- `timeout()` for deadlines
- `interval()` for periodic work

### 5. Async I/O
- TCP/UDP sockets
- Filesystem operations
- Process and signal management

---

## Feature Flags

| Flag | Purpose |
|------|---------|
| `full` | Enable all features |
| `rt` | Single-threaded scheduler |
| `rt-multi-thread` | Multi-threaded scheduler |
| `sync` | Channels, mutex, barrier |
| `time` | Sleep, timeout, interval |
| `net` | TCP, UDP, Unix sockets |
| `fs` | Async filesystem |
| `macros` | `#[tokio::main]`, `#[tokio::test]` |

---

## Thread Types

### Core Threads
- Run async code
- One per CPU core by default
- Swapping only at `.await` points

### Blocking Threads
- Spawned on demand for blocking code
- Use `spawn_blocking()` for CPU-bound work
- Large upper limit (unlike core threads)

---

## Key Takeaways

1. **#[tokio::main]** macro sets up runtime
2. **Core vs blocking**: IO in core, CPU in blocking
3. **Work-stealing scheduler**: Efficient task distribution
4. **Feature flags**: Compile only what you need
5. **WASM support**: Limited but available

---

## Cross-References

- Related to: [[009-async-book-intro]] (async fundamentals)
- Related to: [[010-concurrency-patterns-beyond-locks]] (concurrency)
- Related to: [[006-shared-state-concurrency]] (sync primitives)