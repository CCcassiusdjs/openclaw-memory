# The Embedded Rust Book - Introduction

**Source:** Rust Embedded Working Group - "The Embedded Rust Book"
**URL:** https://docs.rust-embedded.org/book/
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Official introductory book about using Rust on "bare metal" embedded systems (microcontrollers), covering setup, best practices, and ARM Cortex-M examples.

---

## Who Embedded Rust is For

> "Everyone who wants to do embedded programming while taking advantage of higher-level concepts and safety guarantees the Rust language provides."

### Target Audience

- Embedded developers wanting Rust's safety
- Rust developers wanting embedded skills
- Anyone curious about bare-metal programming

---

## Scope

### Goals

1. **Get developers up to speed** with embedded Rust setup
2. **Share best practices** for using Rust language features correctly
3. **Serve as a cookbook** for common patterns (C + Rust, etc.)

### Architecture Focus

- Uses **ARM Cortex-M** for all examples
- Concepts apply across architectures
- Explains architecture-specific details where needed

---

## Prerequisites

### Rust Knowledge Required

- Comfortable with Rust programming
- Written, run, and debugged Rust applications
- Familiar with Rust 2018+ idioms

### Embedded Knowledge Required

- Cross-compilation concepts
- Memory-mapped peripherals
- Interrupts
- Common interfaces (I2C, SPI, Serial)

---

## Related Resources

| Topic | Resource | Description |
|-------|----------|-------------|
| Rust Basics | [Rust Book](https://doc.rust-lang.org/book/) | If new to Rust |
| Embedded Intro | [Discovery Book](https://docs.rust-embedded.org/discovery/) | If new to embedded |
| Advanced | [Embedonomicon](https://docs.rust-embedded.org/embedonomicon/) | Nitty gritty details |
| FAQ | [embedded FAQ](https://docs.rust-embedded.org/faq.html) | Common questions |
| Google | [Comprehensive Rust: Bare Metal](https://google.github.io/comprehensive-rust/bare-metal.html) | 4-day class |

---

## Recommended Hardware

### STM32F3DISCOVERY

- Based on ARM Cortex-M architecture
- Used for all examples in the book
- Peripherals vary between vendors/families
- Same core architecture across most Cortex-M

---

## Key Concepts (Preview)

### Memory-Mapped Peripherals

```rust
// Example: GPIO register access
const GPIO_BASE: usize = 0x4002_0000;

#[repr(C)]
struct GpioRegisters {
    moder: u32,
    otyper: u32,
    ospeedr: u32,
    pupdr: u32,
    // ...
}
```

### Interrupts

- Hardware signals that pause main execution
- Need careful handling for safety
- Rust's ownership model helps

### Cross-Compilation

```bash
# Add target
rustup target add thumbv7em-none-eabihf

# Build for embedded
cargo build --target thumbv7em-none-eabihf
```

---

## Book Structure

### How to Read

1. **Front-to-back recommended**
2. Later chapters build on earlier concepts
3. Topics revisited with more depth

### Hardware Setup

1. Purchase STM32F3DISCOVERY board
2. Install toolchain
3. Follow examples step-by-step

---

## Why Rust for Embedded?

### Safety Guarantees

| Feature | Embedded Benefit |
|---------|------------------|
| Ownership | No use-after-free |
| Borrow checker | No data races |
| No null | No null pointer deref |
| No GC | Deterministic timing |
| Type system | Encode hardware invariants |

### Zero-Cost Abstractions

- High-level code compiles to efficient assembly
- Iterator chains → tight loops
- No runtime penalty for safety

### Interoperability

- C FFI for existing codebases
- Gradual migration possible
- Safe wrappers around unsafe hardware access

---

## Key Takeaways

1. **Embedded Rust** = bare metal + Rust safety
2. **Cortex-M** is the reference architecture
3. **Cross-compilation** via rustup targets
4. **Memory-mapped I/O** is the hardware interface
5. **Safety + performance** is the key value proposition
6. **Book is front-to-back** sequential reading
7. **STM32F3DISCOVERY** recommended for examples

---

## Cross-References

- Related to: [[007-unsafe-rust-intro]] (unsafe for hardware)
- Related to: [[008-ffi]] (C interop)
- Related to: [[013-rust-kernel-docs]] (kernel Rust)
- Related to: [[001-rust-book-ownership]] (ownership model)