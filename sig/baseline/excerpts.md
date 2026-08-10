# Baseline excerpts — verbatim, load-bearing passages

These are exact excerpts captured from the Mycelium evidence reads. Each is a **subset** of the
pinned file (see `MANIFEST.md`); the full-file SHA256 remains the authority. Nothing is
paraphrased. These are the passages v3.1 revises or depends on.

---

## levels.md — `27838f91ff0c` — the level ladder and the L4/L5 rule

```
L0 := assigned (operators and Q assigned, prose remains)
L1 := structured (prose withdrawn, structure tokens replace relationships)
L2 := compressed (labels shortened, compounds fused, zero prose)
L3 := pure (operators only, flat chain, pipe-separated)
L4 := dimensional (d1-d5 positions, operator-typed, no topology declared)
L5 := dimensional + shape (d1-d5 positions + shape declares topology)
L6 := braid (nested packets, meta-reference, recursion)
```

```
═══ DIMENSION STRUCTURE (L4+) ═══
At L4 and above, content is organized into five dimension slots.
d1 := conceptual content
d2 := equations / state
d3 := implementation
d4 := time
d5 := action
```

```
## L4 := dimensional_open
d1-d5 vectors present, shape NOT declared
## L5 := dimensional_declared
d1-d5 vectors + shape REQUIRED
```

> **Load-bearing fact:** both L4 and L5 carry **d1–d5**. The L4/L5 distinction is the *shape
> declaration*, not the dimension count. The doc's own L4 example uses `d1 d2 d3 d4 d5`.

---

## shapes.md — `26867539c802` — the registered shape set and `~ RELATE`

Registered shapes (from the ASCII-footer rules and the shape-selection table):

```
Footer ASCII required (topology closes):
  torus, hyper_torus, klein, mobius, mala, wave, lotus
Footer ASCII not used (topology terminates or non-path):
  beam, ToL, prism, kite, merkaba, cube, vesica, DNA, fractal
```

```
Shape is required at L5+. Below L5, shape is absent from
the header (see encoding.md). When shape is declared, all
shape rules apply.
```

`~` as a joint between shapes (composition section):

```
| ~ | RELATES | Shapes have a connection (general) |
~ RELATE is added to the structure token vocabulary
(vocab ID to be assigned in encoding.md).
```

> **Load-bearing fact:** `circuit` is **not** in the registered shape set. `~` is a relation
> token, not a geometry.

---

## execution.md — `07c50f4d4afa` — modifiers, `~ CIRCUIT`, and the Python map

Operator modifiers:

```
  !   EAGER. Execute on receipt. Do not wait for a query.
  -*  INVERSE. Flip the operator's behavior. The verb reverses.
  ~   CIRCUIT. Declare a reactive connection. The operator is
      wired to other operators in a live path.
      ܫ~ܕ~ܬ = parse flows into gate flows into validate.
      Circuit is the topology of execution — how operators
      connect to each other as a live system.
```

Python→SIG mapping table (note: **no Boolean-AND / NOT row exists**):

```
| function parameters / input() | ܟ RECEIVE          |
| if/elif/else                  | ܕ GATE             |
| not / except / filter out     | ⊖ EXCLUDE          |
| dict / set / list             | ܒ CONTAIN          |
| set membership check          | ܚ PARTITION        |
| str transforms / state change | ܩ TRANSFORM        |
| assert / validation check     | ܬ VALIDATE         |
| return                        | ܠ TRANSMIT         |
| for / while                   | ܣ CYCLE            |
| function call                 | ܙ CALL             |
| try/except                    | ܕ GATE ⊕ ܕ-* CLOSE |
| None as meaningful absence    | Q∅                 |
```

```
ܕ  GATE — pass or block. When activated, evaluate the gate
   condition. Content either passes or does not. Binary
   decision at a boundary.
   -*: CLOSE — shut the gate. Block unconditionally.
```

> **Load-bearing facts:** (a) `~ CIRCUIT` is an execution-topology *modifier*, the same glyph
> `shapes.md` uses as the `RELATE` *joint* — one token, two scopes. (b) The mapping table has
> **no Boolean layer**: `⊕` is set-COMBINE and `⊖` is set-EXCLUDE, neither is a typed Boolean
> connective. That gap is what forced the `⊕`/`⊖`-as-logic misuse v3.1 fixes.
