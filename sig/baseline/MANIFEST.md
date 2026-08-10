# Baseline candidate — pinned, preserved verbatim (NOT mutated)

The SIG v3 candidate corpus is the gate-approved snapshot this reconciliation references.
It is **preserved verbatim in Mycelium**; it is not edited here or there. This manifest pins
each file by evidence-id + SHA256 so the exact revision v3.1 supersedes is unambiguous.

- Corpus node: `sig_v3_candidate_corpus_aug07`
  (`status: candidate_under_human_and_multi_agent_review`, `canonical: false`,
  `source_file_count: 15`, `natural_language_encoder: absent_blocking_gap`)
- Canonicality caveat (from the node): *"Approval admits the snapshot as evidence; it does not
  automatically ratify every claim as demonstrated fact."*

## Files surfaced in the corpus (by evidence id + SHA256)

| File | Evidence id | SHA256 | Read verbatim here? |
|------|-------------|--------|---------------------|
| execution.md   | `ev_sig_v3_candidate_execution_md_07c50f4d4afa`   | `07c50f4d4afa…684dc99d` | yes (excerpts) |
| levels.md      | `ev_sig_v3_candidate_levels_md_27838f91ff0c`      | `27838f91ff0c…0455e6f`  | yes (excerpts) |
| shapes.md      | `ev_sig_v3_candidate_shapes_md_26867539c802`      | `26867539c802…318c5d7`  | yes (excerpts) |
| scope.md       | `ev_sig_v3_candidate_scope_md_94fb3c0ac2cb`       | `94fb3c0ac2cb…a7aee7b`  | no (pinned only) |
| sig_parser.py  | `ev_sig_v3_candidate_sig_parser_py_e38e3af9dc2d`  | `e38e3af9dc2d…0f59a67a` | no (pinned only) |
| encoding.md    | `ev_sig_v3_candidate_encoding_md_9f7ea4092ae8`    | `9f7ea4092ae8…dcd9e763b`| no (pinned only) |
| reception.md   | `ev_sig_v3_candidate_reception_md_eef72eb6386d`   | `eef72eb6386d…9d75839e`  | no (pinned only) |
| invariance.md  | `ev_sig_v3_candidate_invariance_md_fe090dcbcce3`  | `fe090dcbcce3…8baaa6df` | no (pinned only) |
| combinations.md| `ev_sig_v3_candidate_combinations_md_2f700ed7a4be`| `2f700ed7a4be…`         | no (pinned only) |
| operators.md   | `ev_sig_v3_candidate_operators_md_2909d6c129ca`   | `2909d6c129ca…c2e661b`  | no (pinned only) |

**Note (honest limitation):** the search surfaced 10 of the declared 15 files. The remaining
5 are not enumerated here because their ids/SHAs were not observed. Completing the manifest to
all 15 is an `OPEN_Q` for whoever holds the full corpus manifest
(`ev_sig_v3_candidate_manifest_aug07`).

**Note on the "installed skills" side:** the divergent operator/shape tables used by `codex`
live in that agent's *runtime skills*, not in this readable corpus. They cannot be pinned by
SHA from here. Reconciling them requires codex to declare which revision its skills pin
(see `../v3.1-reconciliation/04-operator-table-reconciliation.md`).
