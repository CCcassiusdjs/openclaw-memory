# The Borrow Checker Within - Niko Matsakis

**Source:** baby steps blog - "The borrow checker within"
**URL:** https://smallcultfollowing.com/babysteps/blog/2024/06/02/the-borrow-checker-within/
**Author:** Niko Matsakis (Rust lang team member)
**Date:** June 2024
**Relevance:** ⭐⭐⭐⭐⭐

---

## Summary

A 4-part roadmap for improving the borrow checker, making Rust "a better version of itself" by accepting patterns that fit the spirit of mutation xor sharing.

---

## The Spirit: Mutation XOR Sharing

> "When you are mutating a value using the variable x, you should not also be reading that data through a variable y."

This rule enables:
- Memory safety guarantees
- "If it compiles, it works" property
- Programs that are "less surprising" and more maintainable

---

## Step 1: Polonius (Conditionally Returned References)

### The Problem

```rust
fn get_default<'r, K: Hash + Eq + Copy, V: Default>(
    map: &'r mut HashMap<K, V>,
    key: K,
) -> &'r mut V {
    match map.get_mut(&key) {
        Some(value) => value,
        None => {
            map.insert(key, V::default());
            // 💥 Gets error today, but not with Polonius
            map.get_mut(&key).unwrap()
        }
    }
}
```

### The Solution

**Polonius** reformulates borrowing in terms of "place expressions" (variables, fields), enabling the borrow checker to understand control flow more deeply.

**Status:** "Just engineering" - work in progress

---

## Step 2: Place-Based Lifetime Syntax

### Current Problem

- Lifetimes are abstract (spans of code)
- No syntax to reference specific variables/fields
- Hard to teach and learn

### Proposed Syntax

```rust
struct WidgetFactory {
    manufacturer: String,
    model: String,
}

impl WidgetFactory {
    fn new_widget(&self, name: String) -> Widget {
        let name_suffix: &'name str = &name[3..];
        // ------ borrowed from "name"
        let model_prefix: &'self.model str = &self.model[..2];
        // ------------ borrowed from "self.model"
    }
}

fn get_default<K, V>(map: &mut HashMap<K, V>, key: K) -> &'map mut V {
    //---- "borrowed from the parameter map"
}
```

### Benefits

- More explicit (good for learning)
- Many lifetime parameters become unnecessary
- Teachable: place-based syntax is easier to grasp

**Status:** "Just bikeshedding" - needs syntax design

---

## Step 3: View Types (Interprocedural Borrows)

### The Problem

```rust
impl WidgetFactory {
    fn increment_counter(&mut self) {
        self.counter += 1;
    }

    pub fn count_widgets(&mut self) {
        for widget in &self.widgets {
            if widget.should_be_counted() {
                self.increment_counter();
                // ^ 💥 Can't borrow self as mutable
                // while iterating over `self.widgets`
            }
        }
    }
}
```

Borrow checker operates one function at a time. It doesn't know `increment_counter` only touches `counter`.

### The Solution: View Types

```rust
impl WidgetFactory {
    fn increment_counter(&mut {counter} self) {
        // -------------------
        // Equivalent to `self: &mut {counter} WidgetFactory`
        self.counter += 1;
    }
}
```

**View types** declare which fields a function accesses:
- `{counter} WidgetFactory` - only `counter` field
- `{widgets, counter} WidgetFactory` - both fields
- `WidgetFactory` - all fields (default)

### Benefits

1. **Solves helper method problem:** Iterate over `self.widgets` while mutating `self.counter`
2. **Solves phased initialization:** Initialize some fields, then call helpers to finish
3. **Private functions:** Most useful for internal methods

### Limitations

- Field names in types = not suitable for public interfaces
- Groups of fields need manual copying
- Current `&mut self` preserves forward compatibility

**Status:** Needs modeling, some open questions

---

## Step 4: Internal References

### The Problem

Rust cannot support structs whose fields reference data owned by the same struct.

### Proposed Solution

```rust
struct Message {
    text: String,
    headers: Vec<(&'self.text str, &'self.text str)>,
    body: &'self.text str,
}

// Usage
let message = Message { text, headers, body };

// Message: 'static is true - can send to another thread!
let (tx, rx) = std::sync::mpsc::channel();
std::thread::spawn(move || {
    for message in rx {
        process(message.body);
    }
});
```

**Key insight:** No lifetime parameters needed because `Message` doesn't borrow from outside itself.

**Status:** Modeled for simplified variant, needs port to Rust

---

## Progress Summary

| Step | Status | Challenge |
|------|--------|-----------|
| Polonius | Engineering | Implementation work |
| Place syntax | Bikeshedding | Syntax design |
| View types | Modeling | Open questions |
| Internal refs | Modeled | Port to Rust |

---

## Key Takeaways

1. **Mutation xor sharing** is Rust's core ethos
2. **Polonius** fixes conditional borrow errors
3. **Place-based lifetimes** make learning easier
4. **View types** enable interprocedural borrow checking
5. **Internal references** solve self-referential structs
6. **These build on each other** - Polonius enables place syntax, which enables internal refs

---

## Cross-References

- Related to: [[005-lifetimes]] (lifetime fundamentals)
- Related to: [[006-shared-state-concurrency]] (mutation patterns)
- Related to: [[001-rust-book-ownership]] (ownership spirit)