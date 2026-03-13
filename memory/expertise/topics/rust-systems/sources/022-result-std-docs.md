# Result<T, E> - std::result

**Source:** Rust Standard Library - std::result::Result
**URL:** https://doc.rust-lang.org/stable/std/result/enum.Result.html
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

`Result<T, E>` represents either success (`Ok(T)`) or failure (`Err(E)`). Core type for error handling in Rust.

---

## Variants

```rust
pub enum Result<T, E> {
    Ok(T),  // Success
    Err(E), // Error
}
```

---

## Key Methods

### Querying

| Method | Returns | Description |
|--------|---------|-------------|
| `is_ok()` | bool | True if Ok |
| `is_err()` | bool | True if Err |
| `is_ok_and(f)` | bool | True if Ok and f(value) |
| `is_err_and(f)` | bool | True if Err and f(error) |

### Conversion

| Method | From | To |
|--------|------|-----|
| `ok()` | Result<T, E> | Option<T> |
| `err()` | Result<T, E> | Option<E> |
| `as_ref()` | &Result<T, E> | Result<&T, &E> |
| `as_mut()` | &mut Result<T, E> | Result<&mut T, &mut E> |

### Transformation

| Method | Behavior |
|--------|----------|
| `map(f)` | Apply f to Ok, Err unchanged |
| `map_err(f)` | Apply f to Err, Ok unchanged |
| `map_or(default, f)` | Apply f or return default |
| `map_or_else(default_fn, f)` | Lazy default |
| `inspect(f)` | Call f on Ok, return original |
| `inspect_err(f)` | Call f on Err, return original |

### Extraction

| Method | Behavior |
|--------|----------|
| `expect(msg)` | Panic with message if Err |
| `unwrap()` | Panic if Err |
| `unwrap_or(default)` | Return default if Err |
| `unwrap_or_else(f)` | Compute default if Err |
| `unwrap_or_default()` | Use Default trait |
| `unwrap_unchecked()` | UB if Err (unsafe) |

---

## The ? Operator

```rust
fn read_file() -> Result<String, io::Error> {
    let mut file = File::open("path")?;  // Returns Err if error
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;  // Returns Err if error
    Ok(contents)
}
```

**`?`** automatically propagates errors to the caller.

---

## Combinators

### and / or

```rust
Ok(1).and(Ok(2));    // Ok(2)
Ok(1).and(Err(e));   // Err(e)
Err(e).and(Ok(2));   // Err(e)

Ok(1).or(Ok(2));     // Ok(1)
Err(e).or(Ok(2));    // Ok(2)
```

### and_then / or_else

```rust
Ok(1).and_then(|x| Ok(x + 1));  // Ok(2)
Err(e).and_then(|x| Ok(x + 1)); // Err(e)

Err(e).or_else(|e| Ok(2));      // Ok(2)
```

---

## Key Takeaways

1. **Result replaces exceptions**: Explicit error handling
2. **? operator**: Propagate errors automatically
3. **Combinators**: map, and_then, or_else for chaining
4. **Pattern matching**: match on Ok/Err for control flow
5. **Prefer ? over unwrap()**: Better error propagation

---

## Cross-References

- Related to: [[021-option-std-docs]] (Option vs Result)
- Related to: [[001-rust-book-ownership]] (ownership)
- Related to: [[009-async-book-intro]] (async error handling)