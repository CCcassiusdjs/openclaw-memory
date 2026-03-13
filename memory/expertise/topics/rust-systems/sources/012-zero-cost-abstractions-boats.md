# Zero Cost Abstractions - without.boats

**Source:** without.boats Blog - "Zero Cost Abstractions"
**URL:** https://without.boats/blog/zero-cost-abstractions/
**Author:** without.boats (Rust lang team member)
**Date:** May 2019
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

Philosophical deep-dive into zero-cost abstractions from a Rust language designer's perspective, exploring what makes abstractions truly "zero-cost."

---

## The Three Requirements

### Stroustrup's Definition

> "What you don't use, you don't pay for. And further: What you do use, you couldn't hand code any better."

### The Hidden Third Requirement

**Improve users' experience**

> "The point of abstraction is to provide a new tool, assembled from lower level components, which enable users to more easily write the programs they want to write."

An abstraction must:
1. Be better than handwriting the low-level code
2. Be competitive with non-zero-cost alternatives
3. Actually solve a user problem

---

## Great Zero-Cost Abstractions in Rust

### 1. Ownership and Borrowing

**The biggest win:**
- Guaranteed memory safety
- No garbage collector
- Thread safety by default
- Zero runtime cost

> "This is Rust's original, huge success story."

### 2. Iterator and Closure APIs

**Classic example:**
- `map`, `filter`, `for` loops
- Compile to handwritten C equivalents
- Functional style with C performance

> "The fact that you can write map, filter, iterative for loops, and so on over slices and be optimized to the equivalent of some handwritten C is absolutely astounding."

### 3. Async/await and Futures

**The evolution:**
- Early futures: Zero-cost but bad UX
- Added pinning: Better ergonomics
- Async/await: Great UX + zero-cost

> "By adding pinning to support async/await, references across awaits, and so on, we've made a product that I really think will solve users' problems."

### 4. Unsafe and Module Boundary

**The foundation:**

> "Underlying all of these, and every one of Rust's success stories, is the notion of unsafe blocks and privacy that allow us to dip into raw pointer manipulation to build these zero cost abstractions."

**This is the "mother of all zero cost abstractions in Rust"**

---

## Where We Haven't Succeeded

### Trait Objects (Dynamic Dispatch)

**The problem:**
- Object safety is restrictive
- Sized/unsized types confusion
- Bad ergonomics around coercions
- "Usually pretty annoyed when I have to use them"

**Not yet a good zero-cost abstraction for dynamic polymorphism**

---

## Creating Zero-Cost Abstractions is Hard

### Why It's Difficult

1. **Technical challenge**: Must actually compile to optimal code
2. **UX challenge**: Must be better than alternatives
3. **Balance**: Zero-cost but non-zero-cost alternatives must be competitive
4. **Luck**: Some problems don't have great solutions yet

### The async/await Experience

> "Having been involved in what I think is going to be one of those success stories - async/await of course - it feels like holding fire in your hands."

> "Last September I commented to a friend that I was worried I would never do any work as good as the work I had just done (in reference to the Pin API)."

**Creating excellent zero-cost abstractions is rare and precious**

---

## Key Insights

### The UX Factor

Zero-cost abstractions compete with TWO alternatives:
1. **Handwriting code**: Must be ergonomically better
2. **Non-zero-cost abstractions**: Must be worth the overhead

**Rust's approach:** Make non-zero-cost unpleasant, pushing users to zero-cost

> "I think to some extent Rust has tried to cheat this by making non-zero cost abstractions actively unpleasant to write."

**Author's view:** This is a mistake that hurts overall language UX

### The Achievement

When done right, zero-cost abstractions are:

> "Incredibly difficult and incredibly awesome."

---

## The Philosophy

### What Makes Abstractions Zero-Cost

| Requirement | Meaning |
|-------------|---------|
| No global costs | Don't burden non-users |
| Optimal performance | Can't hand-code better |
| Improve UX | Actually solve problems |

### The Foundation

**Unsafe + privacy = building block for all other abstractions**

- Safe code wraps unsafe
- Module boundary controls visibility
- Abstraction encapsulates complexity

---

## Key Takeaways

1. **Three requirements**: No global costs, optimal performance, improve UX
2. **Ownership/borrowing**: Rust's biggest success
3. **Iterators/closures**: Astounding optimization
4. **Async/await**: Fixed UX to match zero-cost promise
5. **Unsafe**: Foundation for all abstractions
6. **Trait objects**: Still a work in progress
7. **Creating them is hard**: Rare achievement, feels like "holding fire"

---

## Cross-References

- Related to: [[001-rust-book-ownership]] (ownership fundamentals)
- Related to: [[005-lifetimes]] (borrowing mechanism)
- Related to: [[007-unsafe-rust-intro]] (unsafe foundation)
- Related to: [[011-zero-cost-abstractions-dockyard]] (practical guide)