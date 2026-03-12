# Shared-State Concurrency - Mutex and Arc

**Source:** https://doc.rust-lang.org/book/ch16-03-shared-state.html
**Category:** Concurrency
**Priority:** ★★★★★ Essencial
**Read:** 2026-03-12
**Status:** completed

---

## Resumo Principal

Shared-state concurrency usa mutexes para controlar acesso a dados compartilhados entre threads. Rust garante segurança em compile-time: o type system previne esquecer de adquirir ou liberar locks. `Arc<T>` permite múltiplas threads terem ownership do mesmo dado.

---

## Conceitos-Chave

### 1. Mutex<T> - Mutual Exclusion
```rust
use std::sync::Mutex;

fn main() {
    let m = Mutex::new(5);

    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }  // Lock liberado automaticamente aqui (Drop)

    println!("m = {m:?}");
}
```

**Regras do Mutex:**
1. Deve adquirir o lock antes de acessar dados
2. Deve liberar o lock quando terminar

**Rust garante:**
- Type system força `lock()` antes de acessar dados
- `MutexGuard` libera automaticamente via `Drop` trait
- Impossível esquecer de liberar!

### 2. MutexGuard e Drop
```rust
let mut num = m.lock().unwrap();
// MutexGuard<i32> retornado
// Implementa Deref → pode usar como referência
// Implementa Drop → libera lock automaticamente

*num = 6;  // Acesso ao valor interno
// Fim do escopo → Drop libera o lock
```

### 3. Múltiplas Threads com Mutex - Problema de Ownership

```rust
// ERRO: counter é movido para cada thread
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Mutex::new(0);
    let mut handles = vec![];

    for _ in 0..10 {
        let handle = thread::spawn(move || {  // ERROR: borrow of moved value
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    // ...
}
```

**Problema:** `move` transfere ownership para uma thread, não pode mover para múltiplas.

### 4. Rc<T> Não Funciona com Threads

```rust
use std::rc::Rc;
use std::sync::Mutex;
use std::thread;

fn main() {
    let counter = Rc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Rc::clone(&counter);
        let handle = thread::spawn(move || {
            // ERROR: `Rc<Mutex<i32>>` cannot be sent between threads safely
            // trait `Send` is not implemented for `Rc<Mutex<i32>>`
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
}
```

**Problema:** `Rc<T>` NÃO é thread-safe!
- Reference count não é atômico
- Pode causar data races no contador
- Não implementa `Send`

### 5. Arc<T> - Atomic Reference Counting

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());  // Result: 10
}
```

**Arc vs Rc:**
- `Arc<T>` = Atomic Reference Counting
- Thread-safe reference counting
- Implementa `Send`
- Overhead de atomic operations

### 6. Interior Mutability Pattern

| Single Thread | Multi Thread |
|---------------|--------------|
| `RefCell<T>` | `Mutex<T>` |
| `Rc<T>` | `Arc<T>` |

**Pattern completo:**
- Single thread: `Rc<RefCell<T>>`
- Multi thread: `Arc<Mutex<T>>`

### 7. Deadlocks
Rust previne data races, mas NÃO previne deadlocks:
```rust
// Deadlock: thread A espera por lock 1 (tem lock 2)
//           thread B espera por lock 2 (tem lock 1)
```

**Solução:** 
- Sempre adquirir locks na mesma ordem
- Usar `try_lock()` com timeout
- Usar estruturas de dados lock-free

---

## Padrões Importantes

### Pattern: Thread-Safe Counter
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        }));
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
```

### Pattern: Interior Mutability
```rust
// Single-threaded
let data = Rc::new(RefCell::new(vec![1, 2, 3]));
data.borrow_mut().push(4);

// Multi-threaded
let data = Arc::new(Mutex::new(vec![1, 2, 3]));
data.lock().unwrap().push(4);
```

### Pattern: RwLock (Multiple Readers, Single Writer)
```rust
use std::sync::RwLock;

let lock = RwLock::new(5);

// Multiple readers
{
    let r1 = lock.read().unwrap();
    let r2 = lock.read().unwrap();  // OK: múltiplos readers
    println!("{}, {}", *r1, *r2);
}

// Single writer
{
    let mut w = lock.write().unwrap();  // Exclusivo
    *w += 1;
}
```

---

## Comparação de Tipos

| Type | Thread-Safe | Interior Mutability | Use Case |
|------|-------------|---------------------|----------|
| `Rc<T>` | ❌ No | ❌ No | Single-threaded shared ownership |
| `Arc<T>` | ✅ Yes | ❌ No | Multi-threaded shared ownership |
| `RefCell<T>` | ❌ No | ✅ Yes | Single-threaded mutability |
| `Mutex<T>` | ✅ Yes | ✅ Yes | Multi-threaded mutability |
| `Rc<RefCell<T>>` | ❌ No | ✅ Yes | Single-threaded mutable shared |
| `Arc<Mutex<T>>` | ✅ Yes | ✅ Yes | Multi-threaded mutable shared |

---

## Insights para Systems Programming

1. **Compile-time Safety:** Rust previne data races em compile-time
2. **RAII:** Locks são liberados automaticamente via Drop
3. **Send Trait:** Garante que tipos podem ser enviados entre threads
4. **Sync Trait:** Garante que tipos podem ser compartilhados entre threads
5. **Performance Cost:** Atomic operations têm overhead
6. **Deadlock Risk:** Rust não previne deadlocks - cuidado com múltiplos locks

---

## Atomic Types Alternativa

Para operações simples em tipos primitivos:
```rust
use std::sync::atomic::{AtomicUsize, Ordering};

let counter = AtomicUsize::new(0);
counter.fetch_add(1, Ordering::SeqCst);
```

**Vantagens:**
- Sem lock overhead
- Mais performático para operações simples

---

## Próximos Passos

1. Estudar `Send` e `Sync` traits
2. Ver `RwLock` para read-heavy workloads
3. Explorar lock-free data structures
4. Estudar atomics (Ordering)

---

**Conceitos aprendidos:** 5
- Mutex<T> e MutexGuard
- Arc<T> vs Rc<T>
- Interior mutability pattern
- Send and Sync traits
- Deadlock awareness