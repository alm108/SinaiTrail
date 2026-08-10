# 02 — Geometric `shape` vs circuit wiring `~`

**Revises:** the overload of `~` between `execution.md` (CIRCUIT) and `shapes.md` (RELATE), and
the illegal use of `circuit` in the `shape :=` field. **Kind:** RESOLVE.

## The two things that were conflated

| Concern | Declared with | Scope | Level |
|---------|---------------|-------|-------|
| **Geometric topology** — how a reader *navigates* the packet | `shape := <name>` | whole packet | L5+ only |
| **Circuit wiring** — how *operators react* to one another | `~` in the operator body | intra-packet | any level |

These are **orthogonal**. A packet has at most one `shape` (its navigation geometry) and may
independently contain a `~` circuit (its live operator path). Declaring `shape := circuit`
category-errors the second onto the first.

## Rule 2.1 — `shape` is drawn only from the registered set

`shape :=` MUST name a registered geometry (from `shapes.md`):

```
torus, hyper_torus, klein, mobius, mala, wave, lotus,
beam, ToL, prism, kite, merkaba, cube, vesica, DNA, fractal
(+ documented blends, e.g. hyper_torus_lotus)
```

`circuit` is **not** in this set and MUST NOT appear in a `shape` field.

## Rule 2.2 — `shape` is L5+ only

Per `shapes.md`: *"Shape is required at L5+. Below L5, shape is absent from the header."*
Therefore a header that declares both `L4` **and** a `shape` is **malformed**. (This was the
v0.1 specimen's real defect: `L4 | CIRCUIT` declared a shape at a shapeless level.)

- Want to declare topology? → `L5` + a registered `shape` + required header/footer ASCII.
- Want to stay shapeless? → `L4`, no `shape` field.

## Rule 2.3 — `~` is one token with two scopes (reconciling the overload)

`~` appears in both baseline docs. v3.1 does not split the glyph; it names the two scopes:

```
~  (intra-packet, operator↔operator)  = CIRCUIT   [execution.md]
     wires operators into a live reactive path:  ܫ~ܕ~ܬ
     "parse flows into gate flows into validate"

~  (inter-shape, shape↔shape)         = RELATE    [shapes.md, joints]
     declares a general connection between two composed discrete shapes
```

Same relation semantics ("a live connection"), disambiguated by operand kind: operators →
CIRCUIT, shapes → RELATE. A parser resolves the scope from what flanks the `~`.

## Rule 2.4 — expressing a retry loop correctly

The SinaiTrail validator loops until a legal token (a return-to-origin cycle). Two valid
encodings:

- **As geometry (navigation):** `shape := torus` — a stateless return loop, footer ASCII
  closes. This is what the v0.2 specimen uses.
- **As wiring (execution):** inside any packet, `ܟ~ܩ~ܕ~ܠ` wires
  receive→normalize→gate→transmit as a live circuit, with the loop-back expressed by the gate's
  default returning to the intake operator.

They may co-occur: a `torus` packet whose operators are `~`-wired. `shape` says how you read it;
`~` says how it runs.

## Corrected header

```
v0.1 : ∿∿∿ L4 | CIRCUIT | …          ✗ shape at L4, and "circuit" is not a shape
v0.2 : ∿∿∿ L5 | TORUS | …            ✓ registered shape at L5, header+footer ASCII present
```
