# 05 — Executable validation fixtures (SinaiTrail specimen)

**Adds:** a byte-decidable conformance layer so mechanical validity is *tested*, not scored on
eloquence. **Kind:** ADD.

## Principle

A SIG-as-code packet makes **claims** about a function's behavior (accepted inputs, purity,
determinism, fail-closed). Those claims are only meaningful if they can be **falsified** against
a reference implementation. The SinaiTrail move validator `get_choice` (`sinai_trail.py`
1514–1536) is an ideal reference: small, deterministic, no I/O beyond `input()`, and its
legality boundary is exactly the "mechanical validity" seam `match_profile_v0_1` needs.

## Fixture format

A fixture is a `.sig` packet with a trailing machine-checkable `# CLAIMS` block:

```
# CLAIMS (machine-checkable)
accepted_numeric := 1..num_options
accepted_special := "s" iff (state ≠ Q∅ ∧ allow_special ∧ special_used = ⊥)
accepted_checkin := "c" iff (state ≠ Q∅ ∧ allow_checkin)
accepted_back    := "b" always
normalize        := strip ∘ lower
purity           := no_state_mutation
determinism      := no_random
fail_closed      := invalid → reprompt, never emit illegal
```

See `../fixtures/validator_v0_2.sig`.

## Conformance obligations (each is a test)

| Claim | How it is decided against `get_choice` |
|-------|----------------------------------------|
| `accepted_numeric` | every `"1".."num"` returns itself; `"num+1"` is rejected (loops) |
| `accepted_special` | `"s"` returned iff `allow_special ∧ state ∧ ¬special_used`; else looped |
| `accepted_checkin` | `"c"` returned iff `allow_checkin ∧ state`; else looped |
| `accepted_back` | `"b"` always returned |
| `normalize` | `" 2 " → "2"`, `"B" → "b"`, `" S " → "s"` (with special) |
| `purity` | `state` dict is byte-identical before/after the call |
| `determinism` | `get_choice` source contains no `random`; same input ⇒ same output |
| `fail_closed` | any sequence of illegal tokens followed by a legal one returns **only** the legal token; an illegal token is never returned |

## Postcondition fixture (interface contract, not an invariant of the validator)

`apply_outcome` (`sinai_trail.py:1130`) is the downstream transition that clamps the seven
bounded stats:

```
state[k] = max(0, min(100, state[k] + v))   for k in {nerve, manna, water, camp, signal, repair, gold}
```

v3.1 tests this as the **external postcondition** the validator hands off to — proving the SIG
packet was right to cite the `0 ≤ s ≤ 100` bound as an interface contract rather than an
invariant enforced inside `get_choice`.

## Test suite

`../tests/`:

- `test_get_choice_specimen.py` — the eight conformance obligations above.
- `test_apply_outcome_postcondition.py` — the clamp postcondition.
- `sig_fixture.py` — minimal parser for a `.sig` `# CLAIMS` block.
- `test_sig_fixture_conformance.py` — parses `validator_v0_2.sig` and asserts the reference
  implementation satisfies each declared claim, plus header well-formedness checks from `03`
  (shape ⇔ level ≥ L5; no base dimension exceeds d5).

Run:

```bash
python3 -m unittest discover -s sig/tests -p 'test_*.py' -v
```

Stdlib only — no third-party test runner required.
