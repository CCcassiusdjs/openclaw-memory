# Zero-Cost Abstractions in Rust: Power Without the Price

**Source:** DockYard Blog - "Zero-Cost Abstractions in Rust"
**URL:** https://dockyard.com/blog/2025/04/15/zero-cost-abstractions-in-rust-power-without-the-price
**Author:** DockYard
**Date:** April 2025
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Comprehensive guide to Rust's zero-cost abstractions, explaining how high-level code compiles to low-level, efficient machine code without runtime overhead.

---

## What Are Zero-Cost Abstractions?

### Bjarne Stroustrup's Definition

> "What you don't use, you don't pay for. And further: What you do use, you couldn't hand code any better."

### Three Requirements

1. **No global costs**: Don't burden programs that don't use the feature
2. **Optimal performance**: Compile to best possible implementation
3. **Better UX**: Must actually improve developer experience

---

## Zero-Cost Abstractions in Rust

### 1. Iterators

```rust
let numbers = vec
![1, 2, 3, 4, 5]
;
let doubled_sum: i32 = numbers.iter().map(|x| x * 2).sum();
```

**What happens:**
- `.iter()` creates iterator
- `.map(|x| x * 2)` transforms
- `.sum()` aggregates
- Compiler unrolls to:

```rust
let mut sum = 0;
sum += 1 * 2;
sum += 2 * 2;
// ... etc
```

**No iterator object at runtime - just tight loops**

### 2. Closures

```rust
let base = 10;
let add_base = |x| x + base;
let result = add_base(5);
```

**Compiler inlines:**
```rust
let result = 5 + 10;
```

**No function call overhead in release builds**

### 3. Option/Result

```rust
let maybe_number: Option<i32> = Some(42);
let doubled = maybe_number.map(|x| x * 2).unwrap_or(0);
```

**Compiles to:**
```rust
let doubled;
if let Some(value) = maybe_number {
    doubled = value * 2;
} else {
    doubled = 0;
}
```

**No Option object at runtime - just branches**

### 4. Smart Pointers (Box)

```rust
struct Node {
    value: i32,
    child: Option<Box<Node>>,
}
```

**Box benefits:**
- Solves recursive size issues
- Zero-cost abstraction over raw pointer
- Ownership ensures no leaks

---

## Bonus: Pattern Matching

```rust
fn describe_number(x: i32) -> &'static str {
    match x {
        0 => "zero",
        1..=10 => "small",
        _ => "other",
    }
}
```

**Compiles to optimized if/else branches - no runtime cost**

---

## How Rust Achieves This

### Compile-Time Optimization

1. **Analysis**: Compiler understands code semantics
2. **Transformation**: Rewrites abstractions to optimal form
3. **Inlining**: Embeds function bodies at call sites
4. **Monomorphization**: Generates specialized code for each generic type

### No Runtime Overhead

| Language | Overhead |
|----------|----------|
| Python | Interpreter step-by-step |
| Java | JVM layers, GC pauses |
| Go | GC pauses |
| **Rust** | **None - compile-time only** |

### Inlining & Monomorphization

**Inlining**: Function body replaces call
```rust
// Before
let x = add(1, 2);
// After inlining
let x = 1 + 2;
```

**Monomorphization**: Specialized generics
```rust
// Generic
fn id<T>(x: T) -> T { x }
// Compiler generates:
fn id_i32(x: i32) -> i32 { x }
fn id_f64(x: f64) -> f64 { x }
```

**No runtime type checks - each type gets optimized code**

---

## Performance Benefits

### Benchmarks (Approximate)

| Operation | Rust | Python | JavaScript |
|-----------|------|--------|------------|
| Sum 1M numbers (iterator) | ~1ms | ~10-15ms | ~6-8ms |
| Closure call | Inlined | ~50ns | ~20ns |
| Pattern match | Branchless | ~10ns | N/A |

### Why Rust is Faster

1. **No interpreter**: Direct machine code
2. **No GC**: Predictable memory management
3. **Compile-time optimization**: LLVM backend
4. **Monomorphization**: No virtual dispatch overhead

---

## Practical Use Cases

### REST API with Axum

```rust
use axum::{routing::get, Router, Json};
use serde::Serialize;

#[derive(Serialize)]
struct Product { id: i32, name: String, price: f64 }

async fn get_products() -> Json<Vec<Product>> {
    let products = vec
![/* ... */]
;
    Json(products.into_iter().filter(|p| p.price > 50.0).collect())
}
```

**`.into_iter().filter()` runs at raw loop speed - scales to thousands of requests**

### Data Processing Pipeline

```rust
let error_count: i32 = logs.iter()
    .filter(|log| log.contains("ERROR"))
    .map(|_| 1)
    .sum();
```

**Chain operations compile to single pass over data**

---

## Key Takeaways

1. **Zero-cost = compile-time**: Abstractions disappear at runtime
2. **Iterators = raw loops**: Chained operations fuse into single pass
3. **Closures = inline**: No function call overhead
4. **Option/Result = branches**: No runtime objects
5. **Monomorphization**: Generics have zero overhead
6. **No GC**: Predictable performance for real-time systems

---

## Cross-References

- Related to: [[004-stack-and-heap]] (memory allocation)
- Related to: [[001-rust-book-ownership]] (ownership model)
- Related to: [[009-async-book-intro]] (async zero-cost)
- Related to: [[012-zero-cost-abstractions-boats]] (philosophy)