# Rust Concurrency: 10 Patterns Beyond Locks

**Source:** Medium - Nexumo - "Rust Concurrency: 10 Patterns Beyond Locks"
**URL:** https://medium.com/@Nexumo_/rust-concurrency-10-patterns-beyond-locks-e1598e78e65e
**Author:** Nexumo
**Date:** September 2025
**Relevance:** ⭐⭐⭐⭐

---

## Summary

Field-tested concurrency patterns that avoid heavy locks while maintaining safety and performance in Rust applications.

---

## Core Philosophy

> "You don't need to eliminate locks forever—just beat them in the hot paths without losing Rust's safety superpower."

---

## Pattern 1: Ownership Handoff

**Concept:** Only one task mutates data → no lock needed

```rust
use std::thread;
use std::sync::mpsc;

struct Ledger { total: u64 }

fn main() {
    let (tx, rx) = mpsc::channel::<u64>();
    let handle = thread::spawn(move || {
        let mut ledger = Ledger { total: 0 };
        for delta in rx {
            ledger.total += delta;
        }
        ledger.total
    });
    
    // Many producers, no shared mutation
    for _ in 0..1_000 {
        tx.send(42).unwrap();
    }
}
```

**Benefits:**
- No Mutex overhead
- No deadlocks possible
- Single writer, multiple senders

---

## Pattern 2: Channels (mpsc)

**Concept:** Pass messages, not shared state

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

// Sender moves data
thread::spawn(move || {
    tx.send(data).unwrap();
});

// Receiver processes sequentially
while let Ok(msg) = rx.recv() {
    process(msg);
}
```

**When to use:**
- Producer-consumer patterns
- Task pipelines
- Actor systems

---

## Pattern 3: Atomics

**Concept:** Lock-free atomic operations

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

static COUNTER: AtomicUsize = AtomicUsize::new(0);

fn increment() {
    COUNTER.fetch_add(1, Ordering::SeqCst);
}
```

**Atomic Types:**
- AtomicBool
- AtomicI32/AtomicU32
- AtomicPtr
- AtomicUsize

**Ordering options:**
- Relaxed (weakest)
- Acquire/Release
- SeqCst (strongest)

---

## Pattern 4: Rayon (Data Parallelism)

**Concept:** Parallel iterators without locks

```rust
use rayon::prelude::*;

let sum: i32 = (0..1_000_000)
    .into_par_iter()
    .map(|x| x * 2)
    .sum();
```

**Benefits:**
- Work stealing scheduler
- No manual thread management
- Automatic load balancing

---

## Pattern 5: ArcSwap

**Concept:** Atomic pointer swapping for read-heavy data

```rust
use arc_swap::ArcSwap;

let config = ArcSwap::from(Arc::new(Config::default()));

// Readers (lock-free)
let current = config.load();

// Writer (atomic swap)
config.store(Arc::new(new_config));
```

**Use cases:**
- Configuration hot-reload
- Read-mostly shared state
- Zero-cost reads

---

## Pattern 6: Scoped Threads

**Concept:** Borrow data across threads safely

```rust
use std::thread;

let mut data = vec
![1, 2, 3]
;

thread::scope(|s| {
    s.spawn(|| {
        data.push(4); // Borrow allowed!
    });
});
// All scoped threads joined here
```

**Safety:**
- Compiler guarantees all threads finish
- No data races possible
- Simpler than Arc<Mutex>

---

## Pattern 7: RwLock (Read-Heavy)

**Concept:** Multiple readers OR one writer

```rust
use std::sync::RwLock;

let lock = RwLock::new(data);

// Multiple readers can hold simultaneously
let r1 = lock.read().unwrap();
let r2 = lock.read().unwrap();

// Writers need exclusive access
let mut w = lock.write().unwrap();
```

**When RwLock > Mutex:**
- Read-heavy workloads
- Writers are infrequent
- Parallel reads improve throughput

---

## Pattern 8: Once Lock / OnceCell

**Concept:** One-time initialization

```rust
use std::sync::OnceLock;

static CONFIG: OnceLock<Config> = OnceLock::new();

fn get_config() -> &'static Config {
    CONFIG.get_or_init(|| Config::load())
}
```

**Use cases:**
- Lazy static initialization
- Singleton patterns
- Thread-safe one-time setup

---

## Pattern 9: Barrier

**Concept:** Synchronize multiple threads at a point

```rust
use std::sync::Barrier;

let barrier = Arc::new(Barrier::new(4)); // 4 threads

for _ in 0..4 {
    let b = Arc::clone(&barrier);
    thread::spawn(move || {
        // Do work
        b.wait(); // All threads wait here
        // Continue together
    });
}
```

---

## Pattern 10: Condvar

**Concept:** Wait for condition with notification

```rust
use std::sync::{Mutex, Condvar};

let pair = Arc::new((Mutex::new(false), Condvar::new()));

// Waiter
let (lock, cvar) = &*pair;
let mut started = lock.lock().unwrap();
while !*started {
    started = cvar.wait(started).unwrap();
}

// Notifier
let (lock, cvar) = &*pair;
*lock.lock().unwrap() = true;
cvar.notify_all();
```

---

## Performance Comparison

| Pattern | Overhead | Use Case |
|---------|----------|----------|
| Mutex | High | General purpose |
| Ownership handoff | None | Single writer |
| Channels | Low | Message passing |
| Atomics | Very low | Counters, flags |
| RwLock | Medium | Read-heavy |
| ArcSwap | Low (read) | Config reload |
| Scoped threads | None | Borrow across threads |

---

## Key Takeaways

1. **Avoid locks in hot paths**: Use ownership, channels, atomics
2. **Match pattern to workload**: Read-heavy → RwLock, Single writer → ownership
3. **Rayon for data parallelism**: Automatic parallelization
4. **ArcSwap for config**: Zero-cost reads
5. **Scoped threads**: Simpler than Arc when lifetime known

---

## Cross-References

- Related to: [[006-shared-state-concurrency]] (Mutex, Arc basics)
- Related to: [[009-async-book-intro]] (async vs sync concurrency)
- Related to: [[005-lifetimes]] (ownership across threads)