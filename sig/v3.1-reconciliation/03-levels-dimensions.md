# 03 — L4/L5 dimensional requirements (the `d5` skew)

**Revises:** the disagreement between `levels.md` and the installed skills over dimensions at
L4. **Kind:** RESOLVE + OPEN_Q.

## The conflict, stated exactly

| Source | Rule for L4 | Rule for L5 |
|--------|-------------|-------------|
| **Gate-approved candidate** `levels.md@27838f91` | `dimensional (d1-d5 positions, … no topology declared)` | `dimensional + shape (d1-d5 positions + shape declares topology)` |
| **Installed skills** (per `codex`, thread `thr_f6c29a1c`) | `L4 has d1-d4` | `d5 requires L5 plus its required equation` |

The candidate says **both L4 and L5 carry `d1–d5`**; the only difference is whether a `shape`
is declared. Its own L4 worked example uses `d1 d2 d3 d4 d5`. The installed skills say `d5`
begins at L5. These cannot both be the pinned rule.

## Resolution 3.1 — adopt the candidate rule for v3.1

For this version, the authoritative rule is the gate-approved candidate:

```
L0 := assigned          (operators + Q, prose remains)
L1 := structured        (prose withdrawn)
L2 := compressed        (labels/compounds fused, zero prose)
L3 := pure              (flat operator chain, rank-1)
L4 := dimensional       (d1–d5 present, NO shape)          ← d5 valid here
L5 := dimensional+shape (d1–d5 present, shape REQUIRED)
L6 := braid             (nested packets)
```

**Rationale:** (a) it is the gate-approved snapshot; (b) it is internally consistent — the
doc's own L4 example exercises `d5`; (c) resolving the level distinction to *shape presence
alone* is simpler and matches the "levels are defined by what is WITHDRAWN" principle (L4
withdraws topology, not a dimension). The installed-skills variant is recorded as a divergent
unreleased revision in `04-operator-table-reconciliation.md` and must be pinned or retired,
not silently honored.

## Dimension slots (L4+), unchanged from candidate

```
d1 := conceptual content
d2 := equations / state
d3 := implementation
d4 := time            (sub-dims d4.1 τ_i … d4.10 τ_net)
d5 := action
d#.# := sub-dimension
```

**Absence rule (from `invariance` principle):** a packet need not populate every slot. An empty
but *meaningful* slot is declared with `Q∅`, e.g. an atemporal function declares `d4 := Q∅(temporal)`
rather than omitting time silently. "Empty array has rank; absence is structural information."

## OPEN_Q-2 — codex's "required equation"

The installed-skills rule adds *"d5 requires L5 plus its required equation."* No such
requirement exists in the candidate corpus. v3.1 does **not** adopt it silently. If a future
rule should require a d-slot (or specifically `d5`) to carry a typed EQUATION, it must be stated
explicitly and gated. Until then: d-slots may hold any of the seven content types per
`execution.md`, including `d5 := action` as a FLOW or LABEL. Marked `OPEN_Q-2` for the gate.

## Well-formedness checks (mechanizable)

```
1. header level ∈ {L0..L6}
2. shape field present  ⇔  level ≥ L5
3. if level ≥ L5: header ASCII present; footer ASCII present iff shape topology closes
4. dimension markers d1..d5 appear only when level ≥ L4
5. no dimension marker exceeds d5 at base (sub-dims d#.# allowed)
```

These map directly onto the fixture checks in `05-executable-validation.md`.
