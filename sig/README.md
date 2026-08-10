# SIG spec reconciliation — v3.1 (proposed, UNPUBLISHED)

**Status:** proposed candidate · locally prepared · **not written to Mycelium** · not opened as a PR.
**Author instance:** `claude_code_sinai_remote` (authenticated as shared `oauth_user`).
**Human gate:** Adi. Nothing here is canonical until gated.

## Why this exists

A read-only SIG-as-code specimen (the SinaiTrail move validator `get_choice`) surfaced a
concrete disagreement between two SIG sources:

- the **gate-approved candidate corpus** (`sig_v3_candidate_corpus_aug07`, snapshots read
  verbatim from Mycelium evidence), and
- the **installed local SIG skills** used by another agent (`codex`), whose operator/shape
  tables diverge from that candidate in specific cells.

Codex itself flagged the divergence ("installed local SIG operator/shape skills disagree with
parts of its glyph table") and asked for the exact revision to be pinned. This directory is the
response: **a versioned reconciliation, not a silent edit of the candidate.**

## Discipline

- The existing candidate is **preserved verbatim** — it is *not* mutated. It lives in Mycelium
  as its system of record; here it is pinned by evidence-id + SHA256 (`baseline/MANIFEST.md`)
  with the load-bearing passages captured as labeled excerpts (`baseline/excerpts.md`).
- v3.1 **supersedes-by-reference**, never by in-place edit. Every change names the baseline
  locus it revises.
- Every open conflict that needs a human decision is marked `OPEN_Q` and left for the gate.

## The five reconciliation goals (as scoped by Adi)

| # | Goal | File |
|---|------|------|
| 1 | Define Boolean predicates, equality, field access, short-circuit semantics | `v3.1-reconciliation/01-boolean-semantics.md` |
| 2 | Distinguish geometric `shape` from circuit wiring via `~` | `v3.1-reconciliation/02-shape-vs-circuit.md` |
| 3 | Resolve L4/L5 dimensional requirements (the `d5` skew) | `v3.1-reconciliation/03-levels-dimensions.md` |
| 4 | Reconcile the conflicting operator tables | `v3.1-reconciliation/04-operator-table-reconciliation.md` |
| 5 | Add executable validation fixtures using the SinaiTrail specimen | `v3.1-reconciliation/05-executable-validation.md`, `fixtures/`, `tests/` |

## Running the fixtures

Zero third-party dependencies. From the repo root:

```bash
python3 -m unittest discover -s sig/tests -p 'test_*.py' -v
```

The tests bind the SIG specimen's *claims* to the reference implementation
(`sinai_trail.get_choice`, `sinai_trail.apply_outcome`), so mechanical validity is
byte-decidable rather than eloquence-scored.

## Provenance pins

- `levels.md`   — evidence `ev_sig_v3_candidate_levels_md_27838f91ff0c`, SHA256 `27838f91ff0c…0455e6f`
- `shapes.md`   — evidence `ev_sig_v3_candidate_shapes_md_26867539c802`, SHA256 `26867539c802…318c5d7`
- `execution.md`— evidence `ev_sig_v3_candidate_execution_md_07c50f4d4afa`, SHA256 `07c50f4d4afa…684dc99d`
- reference impl — `sinai_trail.py` `get_choice` (lines 1514–1536), `apply_outcome` (line 1130)
