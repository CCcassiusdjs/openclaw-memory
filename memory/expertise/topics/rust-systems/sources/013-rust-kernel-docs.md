# Rust in the Linux Kernel - Official Documentation

**Source:** Linux Kernel Documentation - Rust
**URL:** https://docs.kernel.org/rust/index.html
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Official Linux kernel documentation for Rust support, providing entry point for kernel development in Rust.

---

## Documentation Structure

### Available Pages

| Page | Content |
|------|---------|
| **Quick Start** | Getting started with Rust in kernel |
| **General Information** | Overview and concepts |
| **Coding Guidelines** | Rust-specific kernel style |
| **Arch Support** | Architecture compatibility |
| **Testing** | Testing Rust kernel code |

---

## Key Concepts

### Rust in the Kernel

- **Official support**: Rust is a supported language for kernel development
- **Memory safety**: Ownership model prevents common bugs
- **Interoperability**: Rust code can call C, C can call Rust
- **Safety boundaries**: Unsafe Rust for low-level operations

### Quick Start

1. Install Rust toolchain
2. Configure kernel with Rust support
3. Write kernel module in Rust
4. Build and test

### Code Documentation

- Kernel generates Rust documentation (rustdoc)
- Available at: https://rust.docs.kernel.org
- Requires Rust-enabled kernel config

---

## Architecture Support

### Supported Architectures

- x86/x86_64
- ARM/ARM64
- RISC-V
- More being added

### Requirements

- LLVM/Clang toolchain
- Rust compiler (specific version)
- kernel build system integration

---

## Coding Guidelines

### Kernel Rust Style

- Follow kernel coding style
- Use `unsafe` blocks appropriately
- Document safety invariants
- Follow C ABI for FFI

---

## Key Takeaways

1. **Official support**: Rust is a first-class kernel language
2. **Memory safety**: Ownership model applies to kernel code
3. **Interoperability**: Seamless C integration
4. **Documentation**: rustdoc generated from kernel config
5. **Architecture support**: Growing list of supported architectures

---

## Cross-References

- Related to: [[007-unsafe-rust-intro]] (unsafe Rust)
- Related to: [[008-ffi]] (FFI concepts)
- Related to: [[014-rusty-linux-paper]] (academic paper)