# v3.1 reconciliation — overview

**Supersedes-by-reference:** SIG v3 candidate corpus (`sig_v3_candidate_corpus_aug07`).
**Does not edit it.** Every section below names the baseline locus it revises and states the
change as an addition or a resolution, never an in-place mutation.

## Relationship to the baseline

```
v3 candidate (gate-approved snapshot, canonical:false)
        │  preserved verbatim, pinned by SHA256
        ▼
v3.1 reconciliation (this dir, proposed, unpublished)
        │  supersedes-by-reference for the loci below
        ▼
[human gate: Adi] ── if gated ──▶ v3.1 becomes the pinned revision
```

## Change set

| Locus (baseline) | Problem | v3.1 action | Kind |
|------------------|---------|-------------|------|
| `execution.md` mapping table | no typed Boolean layer; `⊕`/`⊖` misused as AND/NOT | add Boolean semantics (`01`) | ADD |
| `execution.md` `~ CIRCUIT` vs `shapes.md` `~ RELATE`; `shape` field | `circuit` used as a geometric shape | separate `shape` from `~` wiring (`02`) | RESOLVE |
| `levels.md` L4/L5 vs installed skills | `d5`-at-L4 disagreement | adopt candidate rule; register the skew (`03`) | RESOLVE + OPEN_Q |
| operator/shape tables (candidate vs skills) | silent divergence | divergence registry + authority rule (`04`) | FRAMEWORK |
| — | mechanical validity was eloquence-scored | executable fixtures on SinaiTrail specimen (`05`) | ADD |

## Non-goals / preserved invariants

- SIG's absence partition `{Q ⊕ Q? ⊕ Q∅}` is untouched. Boolean falsity (`⊥`) is **not** the
  same as meaningful absence (`Q∅`); `01` keeps them distinct.
- The human gate stays sovereign. v3.1 proposes; it does not ratify.
- No operator glyph is redefined. v3.1 only *adds* a Boolean layer and *disambiguates* an
  already-overloaded token (`~`).

## Open questions carried to the gate

- `OPEN_Q-1`: which revision does `match_profile_v0_1` pin for mechanical validity — the
  gate-approved candidate (`d1–d5` at L4) or the installed skills (`d1–d4`)?
- `OPEN_Q-2`: does any rule require a d-slot to carry a typed equation (codex's "d5 requires its
  required equation")? Not present in the candidate; must be stated explicitly if intended.
- `OPEN_Q-3`: complete the baseline manifest to all 15 files (5 unenumerated).
