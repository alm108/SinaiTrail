# 01 — Boolean predicates, equality, field access, short-circuit

**Revises:** `execution.md` mapping table (adds a layer it lacks). **Kind:** ADD.

## Motivation

The candidate `execution.md` maps `if/elif/else → ܕ GATE` and `set membership → ܚ PARTITION`,
but provides **no typed Boolean layer**. There is no AND, no OR, and `not` is mapped onto the
set operator `⊖ EXCLUDE`. A gate condition like Python's
`raw == "s" and allow_special and state and not state["special_used"]` therefore had no
faithful encoding, which is exactly why the first specimen misused `⊕` (set-COMBINE) as AND and
`⊖` (set-EXCLUDE) as NOT. v3.1 adds the missing layer.

## 1. Boolean values

```
⊤  := true
⊥  := false
```

`⊤`/`⊥` are **distinct from** the absence partition. In particular `⊥ ≠ Q∅`: false is a decided
value; `Q∅` is meaningful absence (unasked / not-submitted). A predicate resolves to `⊤` or `⊥`,
never to `Q∅`. Evaluating a predicate over `Q∅` operands is governed by §5 (short-circuit).

## 2. Predicates

A **predicate** is any expression that resolves to `⊤`/`⊥`. Predicates are the only things a
`ܕ GATE` may test. `ܕ GATE(P)` passes iff `P ⇒ ⊤`, blocks iff `P ⇒ ⊥`.

Primitive predicate forms:

```
a = b        structural equality on resolved content      (⊤ iff a and b resolve equal)
a ≠ b        negation of equality                          (≡ ¬(a = b))
x ∈ S        membership: x is an element of set S          (ܚ PARTITION test)
x ∉ S        non-membership                                (≡ ¬(x ∈ S))
```

## 3. Equality

`a = b` compares **resolved content by structure**, per `execution.md` resolution rules
(LABEL resolves to itself; SET by enumeration; EQUATION by value; etc.). Equality never
mutates and never has side effects. `=` here is the **predicate** operator; assignment stays
`:=`. The two are lexically distinct and must not be conflated.

## 4. Field access

```
r.field        named-field access on a CONTAIN (ܒ) structure
r["field"]     bracket form (identical semantics; for keys that are not bare labels)
```

Field access resolves the named member of a `ܒ CONTAIN` structure. If `r` is `Q∅`, a bare
field access `r.field` is a **fault** (there is no structure to read). Faults are not `⊥`; they
are ill-formed evaluations. §5 makes the guarded idiom safe.

## 5. Short-circuit semantics

Logical connectives, evaluated **left to right with short-circuit**:

```
P ∧ R    AND. If P ⇒ ⊥, result is ⊥ and R is NOT evaluated.
P ∨ R    OR.  If P ⇒ ⊤, result is ⊤ and R is NOT evaluated.
¬ P      NOT. ⊤ ↔ ⊥.
```

Short-circuit is **normative**, not an optimization. It is what makes guard-then-access safe:

```
(state ≠ Q∅) ∧ (state.special_used = ⊥)
```

If `state` is `Q∅`, the left conjunct is `⊥`, so `state.special_used` is **never evaluated** and
the fault in §4 cannot occur. This is the exact semantics of Python's
`state and not state["special_used"]`.

## 6. Deprecations (set operators are no longer Boolean)

| Misuse (v0.1 specimen) | Correct v3.1 form |
|------------------------|-------------------|
| `a ⊕ b` meaning "a AND b" | `a ∧ b` |
| `x ⊖ true` meaning "not x" | `¬x` |
| `missing ⊖ pass` meaning "if not missing" | `ܕ gate := (missing = ∅) → pass` |

`⊕` remains **set COMBINE** and `⊖` remains **set EXCLUDE / difference**. They carry no Boolean
meaning. A `ܕ GATE` must be fed a predicate (§2), not a set expression.

## 7. Operators unchanged; layer added

No glyph is redefined. Boolean expressions are a **content type** consumed by the existing
`ܕ GATE` operator. Suggested type-detection rule (extends `execution.md` TYPE SYSTEM): content
containing `∧ ∨ ¬ = ≠ ∈ ∉` (and not a higher-precedence marker) is typed **PREDICATE**; a
`ܕ GATE` over PREDICATE content resolves by short-circuit evaluation to `⊤`/`⊥`.

## Worked correction — the SinaiTrail guard

```
Python:  if raw == "s" and allow_special and state and not state["special_used"]:
v0.1  :  ܕ gate := raw = s ⊕ allow_special ⊕ state ⊕ (special_used ⊖ true)   ✗ (⊕/⊖ as logic)
v3.1  :  special_available := allow_special ∧ (state ≠ Q∅) ∧ (state.special_used = ⊥)
         ܕ gate := (raw = "s") ∧ special_available   → ܠ transmit := "s"     ✓
```
