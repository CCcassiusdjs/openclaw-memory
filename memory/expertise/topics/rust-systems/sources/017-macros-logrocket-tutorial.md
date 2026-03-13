# Macros in Rust: A Tutorial with Examples

**Source:** LogRocket Blog - "Macros in Rust: A Tutorial with Examples"
**URL:** https://blog.logrocket.com/macros-in-rust-a-tutorial-with-examples/
**Date:** 2023-2024
**Relevance:** ⭐⭐⭐⭐

---

## Summary

Comprehensive tutorial covering declarative macros (macro_rules!) and procedural macros (derive, attribute-like, function-like) with practical examples.

---

## What Are Rust Macros?

> "Macros enable you to write code that writes other code, which is known as metaprogramming."

### Macros vs Functions

| Aspect | Functions | Macros |
|--------|-----------|--------|
| Parameters | Fixed number and type | Variable number |
| Runtime cost | Function call overhead | Zero runtime cost |
| Compile time | No expansion | Expanded at compile time |
| Implementation | Rust code | Token manipulation |

### Rust vs C Macros

- **C macros**: Text substitution (preprocessor)
- **Rust macros**: Token tree transformation (hygienic)

---

## Declarative Macros (macro_rules!)

### Basic Structure

```rust
macro_rules! add {
    ($a:expr, $b:expr) => {
        {
            $a + $b
        }
    };
}

fn main() {
    add!(1, 2);  // Expands to: { 1 + 2 }
}
```

### Multiple Arms

```rust
macro_rules! add {
    ($a:expr, $b:expr) => {
        { $a + $b }
    };
    ($a:expr) => {
        { $a }
    };
}

fn main() {
    add!(1, 2);  // First arm
    add!(x);     // Second arm
}
```

---

## Token Types

| Type | Matches | Example |
|------|---------|---------|
| `item` | Items (fn, struct, module) | `fn foo() {}` |
| `block` | Block of statements | `{ stmt; expr }` |
| `stmt` | Statement | `let x = 1;` |
| `pat` | Pattern | `Some(x)` |
| `expr` | Expression | `1 + 2` |
| `ty` | Type | `i32`, `Vec<u8>` |
| `ident` | Identifier | `foo`, `bar` |
| `path` | Path | `std::mem::replace` |
| `meta` | Meta item | `#[derive(Debug)]` |
| `tt` | Token tree | Any token |
| `vis` | Visibility | `pub`, `pub(crate)` |

---

## Repetition in Macros

### Zero or More (*)

```rust
macro_rules! add_as {
    ($($a:expr),*) => {
        {
            0
            $(+ $a)*
        }
    };
}

fn main() {
    println!("{}", add_as!(1, 2, 3, 4));  // => { 0 + 1 + 2 + 3 + 4 }
}
```

### One or More (+)

```rust
macro_rules! add_as {
    ($($a:expr),+) => {
        {
            $($a)+  // No leading zero needed
        }
    };
}
```

---

## TT Muncher Pattern

### Recursive Macro Processing

```rust
macro_rules! add {
    // Base case: single argument
    ($a:expr) => {
        $a
    };
    // Two arguments
    ($a:expr, $b:expr) => {
        { $a + $b }
    };
    // Recursive case
    ($a:expr, $($b:tt)*) => {
        { $a + add!($($b)*) }
    };
}

fn main() {
    println!("{}", add!(1, 2, 3, 4));  // => 1 + add!(2, 3, 4) => ...
}
```

---

## Internal Rules

### Private Macro Rules

```rust
macro_rules! ok_or_return {
    // Internal rule (starts with @)
    (@error $a:ident, $($b:tt)*) => {
        {
            match $a($($b)*) {
                Ok(value) => value,
                Err(err) => {
                    return Err(err);
                }
            }
        }
    };

    // Public rule
    ($a:ident($($b:tt)*)) => {
        ok_or_return!(@error $a, $($b)*)
    };
}
```

Internal rules (`@rule_name`) are only callable from within the macro.

---

## Advanced Parsing: Making Structs Public

### Complete Example

```rust
macro_rules! make_public {
    (
        $(#[$meta:meta])*
        $vis:vis struct $struct_name:ident {
            $(
                $(#[$field_meta:meta])*
                $field_vis:vis $field_name:ident : $field_type:ty
            ),*$(,)+
        }
    ) => {
        $(#[$meta])*
        pub struct $struct_name {
            $(
                $(#[$field_meta:meta])*
                pub $field_name : $field_type,
            )*
        }
    };
}

fn main() {
    make_public! {
        #[derive(Debug)]
        struct Name {
            n: i64,
            t: i64,
            g: i64,
        }
    }
}
```

### Expansion Result

```rust
#[derive(Debug)]
pub struct Name {
    pub n: i64,
    pub t: i64,
    pub g: i64,
}
```

---

## Procedural Macros

### Three Types

1. **Custom derive**: `#[derive(MyTrait)]`
2. **Attribute-like**: `#[my_attr]`
3. **Function-like**: `my_macro!(input)`

### Project Setup

```toml
# Cargo.toml
[lib]
proc-macro = true

[dependencies]
syn = { version = "2.0", features = ["full"] }
quote = "1.0"
```

### Basic Structure

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::parse_macro_input;

#[proc_macro_derive(MyTrait)]
pub fn my_trait_derive(input: TokenStream) -> TokenStream {
    let ast = parse_macro_input!(input as DeriveInput);
    
    // Generate implementation
    let gen = quote! {
        // Generated code here
    };
    
    gen.into()
}
```

---

## Limitations of Macros

### Declarative Macros

- ❌ No autocompletion support
- ❌ Difficult to debug
- ❌ Limited modification capabilities
- ❌ Larger binaries
- ❌ Longer compile time

### Procedural Macros

- ❌ More complex to write
- ❌ Need separate crate
- ❌ Debugging requires special techniques
- ❌ Can slow compilation significantly

---

## Key Takeaways

1. **Declarative macros** use `macro_rules!` with pattern matching
2. **Token types** (expr, ty, ident, etc.) specify what to match
3. **Repetition** uses `$()`, separators, and `*` or `+`
4. **TT munchers** process tokens recursively
5. **Internal rules** (`@rule_name`) create private helper rules
6. **Procedural macros** operate on TokenStream → TokenStream
7. **syn + quote** are essential crates for proc macros
8. **Limitations** include compile-time overhead and debugging difficulty

---

## Cross-References

- Related to: [[014-rust-book-macros]] (official docs)
- Related to: [[011-zero-cost-abstractions-dockyard]] (macro zero-cost)
- Related to: [[004-stack-and-heap]] (compile-time vs runtime)