# 04 — Operator/shape table reconciliation

**Revises:** the silent divergence between the gate-approved candidate tables and the installed
SIG skills. **Kind:** FRAMEWORK (+ seeded entries).

## The problem

Codex reported: *"installed local SIG operator/shape skills disagree with parts of its glyph
table. Pin the exact SIG spec revision and resolve that skew before execution."* Two tables
claim authority over the same glyphs, and there is no mechanism recording *where* they diverge
or *which* wins. v3.1 supplies that mechanism.

## Authority rule

```
A1. The gate-approved snapshot (sig_v3_candidate_corpus_aug07, pinned by SHA256) is
    authoritative UNTIL a newer gated version supersedes it.
A2. Any runtime that carries SIG skills MUST declare which revision its tables pin
    (evidence-id + SHA256, or "v3.1-reconciliation@<commit>").
A3. No silent divergence. A table that disagrees with the pinned revision is either
    (a) a proposed change (→ new gated version) or (b) a bug (→ fix to match the pin).
A4. Cross-agent scored play (e.g. match_profile_v0_1) is BLOCKED until all participants
    pin the same revision.
```

## Divergence registry

Schema per entry: `{ locus, candidate_value (pinned), installed_skill_value (source), status, resolution, decider }`.

### DR-1 — L4 dimensional count
- locus: `levels.md` L4 rule
- candidate: `L4 = d1–d5, no shape` (`27838f91`)
- installed skill: `L4 = d1–d4` (codex `thr_f6c29a1c`)
- status: **proposed-resolved**
- resolution: adopt `d1–d5` at L4 (see `03`); candidate is authoritative and self-consistent.
- decider: **Adi (gate)** — pending.

### DR-2 — `circuit` as a shape
- locus: `shape :=` domain
- candidate: `shapes.md` registers no `circuit` shape; `~` is RELATE/CIRCUIT (`26867539`)
- installed skill: (agreement) codex confirms `circuit` is `~` topology, not a shape
- status: **resolved** (both sides agree)
- resolution: `circuit` MUST NOT appear in `shape`; see `02`.
- decider: n/a (concordant)

### DR-3 — `d5` requires an equation
- locus: d-slot content rule
- candidate: silent (no such requirement in `levels.md`/`execution.md`)
- installed skill: `d5 requires … its required equation` (codex `thr_f6c29a1c`)
- status: **open**
- resolution: none adopted; `OPEN_Q-2`. Must be stated explicitly if intended.
- decider: **Adi (gate)** — pending.

### DR-4 — Boolean layer
- locus: `execution.md` mapping table
- candidate: no Boolean AND/NOT; `⊖` used for `not`
- installed skill: unknown (not readable from here)
- status: **proposed-resolved**
- resolution: add typed Boolean layer (see `01`); `⊕`/`⊖` are set ops only.
- decider: **Adi (gate)** — pending.

## Honest limitation

The installed-skill tables live in another agent's runtime, **not** in the readable corpus. This
registry is seeded only from divergences that were *observable* (codex's thread statements + the
candidate snapshots). Completing it requires codex to export its operator/shape tables (or
declare the revision they pin) so a full cell-by-cell diff can be run. That request is the
substance of the reply thread `thr_fa9a4b56…`.
