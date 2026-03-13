# Mutex<T> - std::sync

**Source:** Rust Standard Library - std::sync::Mutex
**URL:** https://doc.rust-lang.org/stable/std/sync/struct.Mutex.html
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Mutual exclusion primitive for protecting shared data. Blocks threads until lock is available. Uses RAII guards for automatic unlock.

---

## Key Concepts

### Basic Usage

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let data = Arc::new(Mutex::new(0));
let data_clone = Arc::clone(&data);

thread::spawn(move || {
    let mut data = data_clone.lock().unwrap();
    *data += 1;
});
```

### RAII Guard Pattern

- `lock()` returns `MutexGuard<T>` that unlocks on drop
- Lock is released automatically when guard goes out of scope
- Prevents forgetting to unlock

### Poisoning

- If thread panics while holding lock, mutex becomes "poisoned"
- Subsequent `lock()` returns `Err(PoisonError)`
- `PoisonError::into_inner()` allows recovering guard anyway
- `is_poisoned()` and `clear_poison()` for manual recovery

---

## Key Methods

| Method | Returns | Behavior |
|--------|---------|----------|
| `new(T)` | Mutex<T> | Create unlocked mutex |
| `lock()` | LockResult<MutexGuard> | Block until acquired |
| `try_lock()` | TryLockResult<MutexGuard> | Non-blocking attempt |
| `is_poisoned()` | bool | Check if poisoned |
| `clear_poison()` | () | Clear poisoned state |
| `into_inner()` | LockResult<T> | Consume mutex |

---

## Key Takeaways

1. **RAII pattern**: Lock automatically released on drop
2. **Poisoning**: Thread panic marks mutex as poisoned
3. **Block until available**: `lock()` blocks, `try_lock()` doesn't
4. **Arc<Mutex<T>>**: Common pattern for shared state
5. **Avoid deadlock**: Don't lock twice in same thread

---

## Cross-References

- Related to: [[006-shared-state-concurrency]] (shared state)
- Related to: [[010-concurrency-patterns-beyond-locks]] (alternatives)
- Related to: [[009-async-book-intro]] (async mutex)