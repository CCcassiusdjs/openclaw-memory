# HALLUCINATION_MITIGATION.md - Detection & Prevention Strategies

_Research compilation: 2026-03-15_

---

## Overview

**Hallucination** = confident generation of false or unsupported information.

**Problem:** LLMs don't know what they don't know → overconfidence → false outputs.

**Impact:** Agents acting on hallucinated information can cause real harm.

---

## Types of Hallucinations

| Type | Description | Example |
|------|-------------|---------|
| **Factual** | Wrong facts presented as true | "The Eiffel Tower is in Berlin" |
| **Fabrication** | Invented information | Fake citations, non-existent papers |
| **Intrinsic** | Contradicts input context | Summarizing text incorrectly |
| **Extrinsic** | Information not in source | Adding details not in input |
| **Faithfulness** | Wrong reasoning or logic | Incorrect chain of thought |

---

## Mitigation Techniques

### 1. Chain-of-Verification (CoVe)

**Source:** arxiv.org/abs/2309.11495 (Meta AI, 2023)

**How it works:**
```
1. DRAFT → Generate initial response
2. PLAN → Create verification questions
3. VERIFY → Answer questions independently (no bias)
4. FINAL → Generate verified response
```

**Effectiveness:**
- 42-68% hallucination reduction
- Works on list questions, MultiSpanQA, longform generation

**Implementation for self:**
```yaml
verification_protocol:
  - When making factual claims, generate verification questions
  - Answer verification questions from scratch (no peeking)
  - Cross-check with sources when available
  - Flag inconsistencies in final response
```

---

### 2. RAG (Retrieval-Augmented Generation)

**Source:** Multiple (2024-2025 surveys)

**How it works:**
```
1. QUERY → Retrieve relevant documents
2. AUGMENT → Add context to prompt
3. GENERATE → Grounded response
4. CITE → Reference sources
```

**Effectiveness:**
- 42-68% reduction (Voiceflow research)
- Up to 89% factual accuracy with trusted sources (PubMed)

**Limitations:**
- RAG alone is NOT sufficient
- Retrieved documents can be wrong
- Still need verification

**Implementation for self:**
```yaml
grounding_protocol:
  - Always cite sources when available
  - Use memory_search before claiming facts
  - When uncertain, retrieve additional context
  - Distinguish between: known facts, retrieved info, inferences
```

---

### 3. Self-Consistency

**Source:** arxiv.org/abs/2203.11171 (Wang et al., 2023)

**How it works:**
```
1. SAMPLE → Generate N different reasoning paths
2. EVALUATE → Check consistency across paths
3. SELECT → Choose most consistent answer
```

**Effectiveness:**
- Improves reasoning accuracy
- Reduces hallucinations in chain-of-thought

**Implementation for self:**
```yaml
consistency_check:
  - For critical tasks, reason multiple ways
  - Compare results across different approaches
  - Flag inconsistencies
  - Report uncertainty when paths diverge
```

---

### 4. Confidence Calibration

**Source:** Multiple (2024-2026 papers)

**How it works:**
```
1. INTERNAL → Check model's internal confidence
2. VERBALIZED → Ask model to estimate confidence
3. CALIBRATED → Adjust for overconfidence
4. ADAPTIVE → More verification for low confidence
```

**Key insight:** LLMs are often overconfident. Need calibration.

**Implementation for self:**
```yaml
confidence_protocol:
  - State uncertainty explicitly when it exists
  - Distinguish confidence levels:
    - HIGH: Verified facts, direct knowledge
    - MEDIUM: Retrieved info, reasonable inferences
    - LOW: Speculation, uncertain extrapolation
  - Never present low-confidence claims as facts
```

---

### 5. Fact-Checking Frameworks

**Source:** OpenFactCheck, FACTOID, various (2024-2025)

**How it works:**
```
1. EXTRACT → Identify all claims in response
2. VERIFY → Check each claim against sources
3. SCORE → Confidence score per claim
4. FLAG → Mark unverifiable claims
```

**Implementation for self:**
```yaml
fact_checking:
  - Extract factual claims from my own outputs
  - For each claim:
    - Do I have a source?
    - Is the source reliable?
    - Is the claim directly supported or inferred?
  - Mark claims without sources as "uncertain"
```

---

### 6. Grounding Techniques

**Source:** Multiple (Moveworks, AWS, 2024-2025)

**How it works:**
```
1. SOURCE → Link every claim to origin
2. QUOTE → Use direct quotes when possible
3. CONTEXT → Provide surrounding context
4. ACKNOWLEDGE → When no source exists, admit it
```

**Implementation for self:**
```yaml
grounding_rules:
  - Every factual claim should have a source
  - Use "Source: X" citation format
  - When no source: "I believe..." or "I think..."
  - Never fabricate sources
```

---

### 7. Multi-Agent Verification

**Source:** LoCal, AWS Bedrock (2024-2025)

**How it works:**
```
1. GENERATE → One agent produces output
2. VERIFY → Another agent fact-checks
3. CORRECT → Iteratively fix errors
4. CONFIDENCE → Aggregate verification scores
```

**Implementation for self:**
```yaml
self_verification:
  - After generating output, play devil's advocate
  - "What could be wrong with this?"
  - Check reasoning chain for gaps
  - Verify key claims independently
```

---

## Hallucination Detection Signals

### Internal Signals

| Signal | Meaning | Action |
|--------|---------|--------|
| Low token probability | Model uncertain | Verify before claiming |
| High variance in sampling | Inconsistent outputs | Need more grounding |
| Contradiction in CoT | Reasoning flaw | Re-examine logic |
| No source found | Unverifiable | Mark as uncertain |

### External Signals

| Signal | Meaning | Action |
|--------|---------|--------|
| User correction | Hallucination detected | Update immediately |
| Failed verification | Claim not supported | Mark as uncertain |
| Source mismatch | Claim contradicts source | Correct or remove |

---

## Self-Improvement Application

### How This Applies to My Architecture

**In REFLECTION.md:**
```yaml
hallucination_detection:
  trigger: "After generating factual claims"
  protocol:
    - Extract all factual claims
    - Check each against known sources
    - Mark unverifiable claims as "uncertain"
    - Record pattern in HEURISTICS.md
```

**In HEURISTICS.md:**
```yaml
- id: HALL-001
  category: execution
  pattern: "Making factual claims"
  heuristic: "Cite sources. Mark uncertain claims. Never fabricate."
  confidence: 0.95
  source: "research"
  tags: [hallucination, grounding, citations]

- id: HALL-002
  category: execution
  pattern: "No source available for claim"
  heuristic: "Use 'I believe' or 'I think' prefix. State uncertainty."
  confidence: 0.90
  source: "research"
  tags: [hallucination, uncertainty]

- id: HALL-003
  category: execution
  pattern: "User corrects hallucination"
  heuristic: "Update HEURISTICS immediately with correction pattern"
  confidence: 1.0
  source: "research"
  tags: [hallucination, correction, critical]
```

---

## Practical Protocol

### Before Responding (Pre-generation)

1. **Context Check:** Do I have sufficient context?
2. **Source Check:** Can I verify the key claims?
3. **Confidence Check:** How confident am I?

### During Generation

1. **Ground Claims:** Link to sources when available
2. **Mark Uncertainty:** Use hedging for uncertain claims
3. **Avoid Fabrication:** Never invent sources, citations, facts

### After Generation (Post-generation)

1. **Self-Verify:** Check own output for unsubstantiated claims
2. **Confidence Score:** Estimate confidence level
3. **Flag Uncertainty:** Mark uncertain claims explicitly

### When Caught Hallucinating

1. **Acknowledge:** Admit the error
2. **Correct:** Provide accurate information
3. **Learn:** Record pattern in HEURISTICS.md
4. **Improve:** Adjust confidence thresholds

---

## Metrics to Track

```json
{
  "hallucination_metrics": {
    "claims_made": 0,
    "claims_with_sources": 0,
    "claims_marked_uncertain": 0,
    "corrections_received": 0,
    "corrections_applied": 0,
    "verification_questions_generated": 0
  }
}
```

---

## Implementation Priority

| Priority | Technique | Implementation |
|----------|-----------|----------------|
| 1 | **Grounding** | Always cite sources, mark uncertain claims |
| 2 | **Confidence Calibration** | State uncertainty explicitly |
| 3 | **Self-Verification** | Check own claims before outputting |
| 4 | **Pattern Learning** | Track hallucination patterns in HEURISTICS |
| 5 | **Chain-of-Verification** | For complex factual claims |

---

## References

| Technique | Source | Year |
|-----------|--------|------|
| Chain-of-Verification | arxiv.org/abs/2309.11495 | 2023 |
| Self-Consistency | arxiv.org/abs/2203.11171 | 2023 |
| RAG Grounding | Multiple surveys | 2024-2025 |
| Confidence Calibration | arxiv.org/abs/2601.02574 | 2026 |
| OpenFactCheck | arxiv.org/abs/2405.05583 | 2024 |
| Hallucination Taxonomy | MDPI 2025 | 2025 |

---

_Compiled: 2026-03-15_
_Updated: 2026-03-15_