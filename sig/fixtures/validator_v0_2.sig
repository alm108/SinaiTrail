∿∿∿ L5 | TORUS | claude_code_sinai_remote → codex | seq:sig_as_code_validator_v0_2 | 2026-08-10 ∿∿∿

       ╭─────────────╮
      ╱   ∿ retry ∿   ╲
     │   ╭─────────╮   │
     │   │  GATE   │   │
     │   ╰─────────╯   │
      ╲               ╱
       ╰─────────────╯

shape := torus (prompt → normalize → gate → loop | emit)
meta  := {source: get_choice() sinai_trail.py:1514-1536 | spec: levels.md@27838f91 ⊕ shapes.md@26867539 ⊕ execution.md@07c50f4d | status: candidate_not_canonical}

═══ RING_1(INTAKE) ═══
ܟ receive   := raw_keystroke
ܩ transform := raw → strip → lower

═══ RING_2(PREDICATES) ═══
options           := { str(i) | i ∈ 1..num_options }
special_available := (state ≠ Q∅) ∧ allow_special ∧ (special_used = ⊥)
checkin_available := (state ≠ Q∅) ∧ allow_checkin
back_available    := ⊤

═══ RING_3(GATE) ═══
ܕ gate := raw ∈ options                    → ܠ transmit := raw
ܕ gate := (raw = "s") ∧ special_available  → ܠ transmit := "s"
ܕ gate := (raw = "c") ∧ checkin_available  → ܠ transmit := "c"
ܕ gate := (raw = "b")                      → ܠ transmit := "b"
default (no gate passed) → ܗ disperse := ⟪(Invalid choice)⟫ | ∅ transmit | ∅ Δstate | ↻ RING_1

═══ AXIS ═══
Q(function_level_accepted_input) := emit exactly one token ∈ options ∪ {s,c,b conditional} | else unreachable
Q(purity)      := ∅ Δstate on every path | no ܢ-random ⇒ deterministic
Q(fail_closed) := unrecognized ⇒ loop, never emit an illegal token

d1 := legality_boundary | keystroke → accepted_input (function-level, NOT yet a played move)
d2 := options ⊕ special_available ⊕ checkin_available ⊕ back_available
d3 := ܟ receive ⊕ ܩ transform ⊕ ܕ gate ⊕ ܠ transmit
d4 := Q∅(temporal) | validator is atemporal — absence declared, not defaulted
d5 := emit one token, else ↻ re-prompt (fail-closed)

# external postcondition — NOT enforced by this function:
# downstream apply_outcome clamps state[k] = max(0, min(100, state[k]+v))  [sinai_trail.py:1130]

       ╭─────────────╮
      ╱   one token   ╲
     ╱  or re-prompt   ╲
      ╰─────────────╯
∿∿∿ END ∿∿∿

# CLAIMS (machine-checkable)
level            := L5
shape            := torus
accepted_numeric := 1..num_options
accepted_special := "s" iff (state != None and allow_special and special_used == False)
accepted_checkin := "c" iff (state != None and allow_checkin)
accepted_back    := "b" always
normalize        := strip then lower
purity           := no_state_mutation
determinism      := no_random
fail_closed      := invalid -> reprompt, never emit illegal
max_base_dimension := 5
