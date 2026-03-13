# Option<T> - std::option

**Source:** Rust Standard Library - std::option::Option
**URL:** https://doc.rust-lang.org/stable/std/option/enum.Option.html
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

`Option<T>` represents an optional value: either `Some(T)` or `None`. Core type for nullable values in Rust (no null pointer).

---

## Variants

```rust
pub enum Option<T> {
    None,
    Some(T),
}
```

---

## Key Methods

### Querying

| Method | Returns | Description |
|--------|---------|-------------|
| `is_some()` | bool | True if Some |
| `is_none()` | bool | True if None |
| `is_some_and(f)` | bool | True if Some and f(value) |
| `is_none_or(f)` | bool | True if None or f(value) |

### Extraction

| Method | Behavior |
|--------|----------|
| `expect(msg)` | Panic with message if None |
| `unwrap()` | Panic if None |
| `unwrap_or(default)` | Return default if None |
| `unwrap_or_else(f)` | Compute default if None |
| `unwrap_or_default()` | Use Default trait |
| `unwrap_unchecked()` | UB if None (unsafe) |

### Transformation

| Method | Result |
|--------|--------|
| `map(f)` | Apply f to Some, None stays None |
| `map_or(default, f)` | Apply f or return default |
| `map_or_else(default_fn, f)` | Lazy default |
| `inspect(f)` | Call f on Some, return original |
| `as_ref()` | Option<&T> |
| `as_mut()` | Option<&mut T> |

### Conversion

| Method | From | To |
|--------|------|-----|
| `ok_or(err)` | Option<T> | Result<T, E> |
| `transpose()` | Option<Result<T, E>> | Result<Option<T>, E> |
| `flatten()` | Option<Option<T>> | Option<T> |

---

## Iterator Adapters

```rust
// Option<T> implements Iterator
let x: Option<i32> = Some(5);
for val in x {
    println!("{}", val);  // Prints 5
}

// or_none() creates iterator from Option
let iter = opt.into_iter();  // 0 or 1 elements
```

---

## Combinators

### and / or

```rust
Some(1).and(Some(2));  // Some(2)
Some(1).and(None);    // None
None.and(Some(2));    // None

Some(1).or(Some(2));  // Some(1)
None.or(Some(2));     // Some(2)
```

### and_then / or_else

```rust
Some(1).and_then(|x| Some(x + 1));  // Some(2)
None.and_then(|x| Some(x + 1));     // None

None.or_else(|| Some(2));  // Some(2)
```

### filter

```rust
Some(4).filter(|x| x % 2 == 0);  // Some(4)
Some(3).filter(|x| x % 2 == 0);  // None
```

---

## Key Takeaways

1. **No null**: Option replaces null pointers
2. **Pattern matching**: `match` or combinators
3. **Zero-cost**: Compiles to efficient branches
4. **Chaining**: `map`, `and_then`, `filter`
5. **Safe extraction**: Prefer `?` or `unwrap_or` over `unwrap()`

---

## Cross-References

- Related to: [[011-zero-cost-abstractions-dockyard]] (zero-cost)
- Related to: [[001-rust-book-ownership]] (ownership)
- Related to: [[005-lifetimes]] (lifetime of optional refs)