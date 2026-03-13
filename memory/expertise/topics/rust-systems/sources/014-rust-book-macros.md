# Macros - The Rust Programming Language

**Source:** The Rust Book Chapter 20 - "Macros"
**URL:** https://doc.rust-lang.org/book/ch20-05-macros.html
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Official Rust documentation covering declarative macros (macro_rules!) and procedural macros (derive, attribute-like, function-like).

---

## Why Macros?

### Macros vs Functions

| Aspect | Functions | Macros |
|--------|-----------|--------|
| Parameters | Fixed number and type | Variable number |
| Expansion | Runtime | Compile-time |
| Traits | Can't implement traits | Can implement traits |
| Complexity | Simple | Complex (code writing code) |

### Key Differences

1. **Metaprogramming**: Macros write code at compile time
2. **Variable arguments**: println!("hello") or println!("hello {}", name)
3. **Compile-time**: Can implement traits before runtime

---

## Declarative Macros (macro_rules!)

### Definition Pattern

```rust
#[macro_export]
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}
```

### Pattern Syntax

| Symbol | Meaning |
|--------|---------|
| `$()` | Capture group |
| `$x` | Macro variable |
| `expr` | Expression type |
| `,` | Separator |
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |

### Example: vec! Expansion

```rust
// Input
vec
![1, 2, 3]

;
// Expands to
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

---

## Procedural Macros

### Three Types

1. **Custom derive**: `#[derive(HelloMacro)]`
2. **Attribute-like**: `#[route(GET, "/")]`
3. **Function-like**: `my_macro!(input)`

### Structure

```rust
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
    // Transform input to output
}
```

**Key point**: All procedural macros take TokenStream and produce TokenStream

---

## Custom Derive Macros

### Creating a Derive Macro

**1. Define trait:**
```rust
pub trait HelloMacro {
    fn hello_macro();
}
```

**2. Create derive crate:**
```toml
# Cargo.toml
[lib]
proc-macro = true

[dependencies]
syn = "2.0"
quote = "1.0"
```

**3. Implement macro:**
```rust
use proc_macro::TokenStream;
use quote::quote;

#[proc_macro_derive(HelloMacro)]
pub fn hello_macro_derive(input: TokenStream) -> TokenStream {
    let ast = syn::parse(input).unwrap();
    impl_hello_macro(&ast)
}

fn impl_hello_macro(ast: &syn::DeriveInput) -> TokenStream {
    let name = &ast.ident;
    let gen = quote! {
        impl HelloMacro for #name {
            fn hello_macro() {
                println!("Hello, Macro! My name is {}!", stringify!(#name));
            }
        }
    };
    gen.into()
}
```

**4. Use the derive:**
```rust
use hello_macro::HelloMacro;
use hello_macro_derive::HelloMacro;

#[derive(HelloMacro)]
struct Pancakes;

fn main() {
    Pancakes::hello_macro();
    // Output: Hello, Macro! My name is Pancakes!
}
```

---

## Key Crates for Procedural Macros

| Crate | Purpose |
|-------|---------|
| `proc_macro` | TokenStream type (built-in) |
| `syn` | Parse Rust code into AST |
| `quote` | Generate Rust code from AST |

---

## Macro Definition Rules

1. **Must be defined before use**: Unlike functions
2. **Separate crate required**: Procedural macros need their own crate
3. **Complex syntax**: Writing code that writes code is harder
4. **Harder to debug**: Indirection makes errors unclear

---

## Best Practices

### When to Use Macros

- **Variable arguments**: Can't express with functions
- **Compile-time code generation**: Derive implementations
- **DSL creation**: Domain-specific syntax
- **Reducing boilerplate**: Repetitive patterns

### When to Use Functions Instead

- **Simple logic**: Functions are clearer
- **Type safety**: Functions have better type checking
- **Debugging**: Easier to trace and debug
- **Readability**: Functions are more self-documenting

---

## Key Takeaways

1. **Metaprogramming**: Macros write code at compile time
2. **Declarative macros**: Pattern matching on code structure
3. **Procedural macros**: TokenStream → TokenStream transformation
4. **Derive macros**: Auto-implement traits
5. **syn + quote**: Core crates for procedural macros
6. **Definition before use**: Macros must be in scope before calling
7. **Complex but powerful**: More capability, more complexity

---

## Cross-References

- Related to: [[001-rust-book-ownership]] (ownership model)
- Related to: [[011-zero-cost-abstractions-dockyard]] (macro performance)
- Related to: [[004-stack-and-heap]] (compile-time vs runtime)