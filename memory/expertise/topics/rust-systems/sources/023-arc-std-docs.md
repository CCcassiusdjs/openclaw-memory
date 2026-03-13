# Arc<T> - std::sync

**Source:** Rust Standard Library - std::sync::Arc
**URL:** https://doc.rust-lang.org/stable/std/sync/struct.Arc.html
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

`Arc<T>` (Atomically Reference Counted) provides thread-safe shared ownership. Multiple threads can own the same data safely through atomic reference counting.

---

## Key Concepts

### Thread-Safe Reference Counting

- **Arc** = Atomically Reference Counted
- Uses atomic operations for reference count
- Thread-safe version of `Rc<T>`
- Higher overhead than `Rc` (atomic operations cost more)

### Shared Ownership

```rust
use std::sync::Arc;
use std::thread;

let data = Arc::new(vec
![1, 2, 3])
;

for _ in 0..10 {
    let data = Arc::clone(&data);
    thread::spawn(move || {
        println!("{:?}", data);
    });
}
```

### Mutation with Arc

Arc provides shared immutable access by default. To mutate:

**Option 1: Mutex/RwLock**
```rust
let data = Arc::new(Mutex::new(vec
![1, 2, 3]))
;
```

**Option 2: make_mut (Clone-on-Write)**
```rust
let mut data = Arc::new(vec
![1, 2, 3])
;
Arc::make_mut(&mut data).push(4);  // Clones only if needed
```

**Option 3: get_mut (Exclusive Access)**
```rust
let mut data = Arc::new(5);
if let Some(data) = Arc::get_mut(&mut data) {
    *data = 10;  // Only works if ref count = 1
}
```

---

## Thread Safety

### Send and Sync

```rust
// Arc<T> implements Send + Sync when T: Send + Sync
Arc<T> is Send + Sync when T: Send + Sync
```

**Why Arc<RefCell<T>> is NOT thread-safe:**
- RefCell uses non-atomic borrow tracking
- RefCell is not Sync
- Therefore Arc<RefCell<T>> is not Send or Sync

**The solution:** `Arc<Mutex<T>>` or `Arc<RwLock<T>>`

---

## Weak<T> for Breaking Cycles

```rust
use std::sync::{Arc, Weak};

let strong = Arc::new(5);
let weak: Weak<i32> = Arc::downgrade(&strong);

// Upgrade to Arc (returns None if dropped)
if let Some(arc) = weak.upgrade() {
    println!("{}", *arc);
}
```

**Use case:** Parent-child relationships in trees (child holds Weak to parent)

---

## Key Methods

| Method | Description |
|--------|-------------|
| `Arc::new(T)` | Create new Arc |
| `Arc::clone(&Arc)` | Increment ref count |
| `Arc::downgrade(&Arc)` | Create Weak pointer |
| `Arc::get_mut(&mut Arc)` | Get mutable ref if ref count = 1 |
| `Arc::make_mut(&mut Arc)` | Clone-on-write semantics |
| `Arc::strong_count(&Arc)` | Number of Arc references |
| `Arc::weak_count(&Arc)` | Number of Weak references |

---

## Arc vs Rc

| Feature | Arc<T> | Rc<T> |
|---------|--------|-------|
| Thread-safe | Yes | No |
| Atomic ops | Yes | No |
| Performance | Lower | Higher |
| Use case | Multi-threaded | Single-threaded |

---

## Key Takeaways

1. **Thread-safe shared ownership**: Multiple threads, same data
2. **Atomic ref counting**: Uses atomic operations
3. **Combine with Mutex**: `Arc<Mutex<T>>` for mutation
4. **Weak breaks cycles**: Use Weak for parent-child relationships
5. **More overhead than Rc**: Use Rc when thread-safety not needed

---

## Cross-References

- Related to: [[006-shared-state-concurrency]] (shared state)
- Related to: [[019-mutex-std-docs]] (Mutex for mutation)
- Related to: [[010-concurrency-patterns-beyond-locks]] (alternatives)