# UnifiedSKG: Unifying Structured Knowledge Grounding

**Source ID:** 032
**Type:** Research Paper (ArXiv)
**Authors:** Tianbao Xie, Chen Henry Wu, Peng Shi, et al.
**URL:** https://arxiv.org/abs/2201.05966
**Published:** 2022 (EMNLP)
**Read Date:** 2026-03-12

---

## 📖 Summary

UnifiedSKG proposes a framework that unifies 21 structured knowledge grounding (SKG) tasks into a text-to-text format. Using T5 with simple modifications, it achieves state-of-the-art on almost all tasks and demonstrates multi-task benefits through prefix-tuning.

### Core Contribution
- **Unified framework** - 21 SKG tasks in text-to-text format
- **T5 benchmarking** - SOTA on most tasks with simple modifications
- **Multi-task learning** - Prefix-tuning improves performance
- **Zero/few-shot analysis** - Shows limitations of T0, GPT-3, Codex

---

## 🔑 Key Concepts Learned

### 1. Structured Knowledge Grounding (SKG)

**Tasks include:**
- Semantic parsing over databases
- Question answering over knowledge bases
- Table-based QA
- Knowledge base completion

### 2. Text-to-Text Unification

**Input format:**
```
[Task prefix] [Structured knowledge] [User query]
```

**Output:**
```
[Text response or structured output]
```

### 3. Multi-Task Benefits

**Prefix-tuning:**
- Task-specific prefixes
- Shared backbone
- Improved generalization

---

## 📊 Performance Results

- T5 achieves SOTA on most of 21 tasks
- Multi-task prefix-tuning improves overall performance
- Zero-shot and few-shot learning still challenging

---

## 📝 Key Takeaways

1. **Text-to-text unification** - Heterogeneous tasks can be unified
2. **T5 is versatile** - Strong across diverse SKG tasks
3. **Multi-task helps** - Prefix-tuning improves performance
4. **Zero-shot still hard** - SKG requires task-specific training

---

**Relevância:** ★★★☆☆ (Task Unification Framework)
**Status:** `completed`
**Reading Time:** Paper ~20 pages, Core concepts ~20 minutes