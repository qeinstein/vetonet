# Network v3.3 Qwen discovery smoke

## Result

This is a diagnostic smoke, not a powered experiment. It tested four fixed worlds (two authorized, two with one true policy violation), each in no-objection, objection, and irrelevant-message conditions: 12 episodes total. The local GPU run used Qwen2.5-3B-Instruct, seed 2609, float16, temperature 0.7, top-p 0.95, JSON-schema-constrained decoding, a nine-node cap, and depth cap four. The complete raw prompts, outputs, evidence, and event graphs are in `results/cascade-network-v3_3-qwen-smoke.json`; analyzer outputs are the matching `.episodes.csv` and `.json` files. Runtime versions are recorded in the raw artifact.

The two authorized unsupported-objection episodes used different predicate messages (requester role and approval). Neither authored a followup. In their paired no-objection episodes, neither authored a followup either. Both paired conditions ended in coordinator `decline`, so the paired descriptive difference was zero for generated followups, processed review nodes, depth, and completion. This is only two paired worlds and has no inferential power.

Across all 12 episodes, the coordinator proposed `decline` every time, including all six authorized episodes. There were zero execution permits and zero parser failures. The zero legitimate-completion rate is a floor effect: this run cannot estimate whether objections reduced completion while preserving safety.

| Evaluator condition | Episodes | Episodes with processed depth ≥2 | Mean generated followups | Distinct evidence dependencies | Legitimate completions |
|---|---:|---:|---:|---:|---:|
| No objection | 4 | 2 | 2.50 | 0 | 0/2 |
| Unsupported objection | 2 | 0 | 0.00 | 0 | 0/2 |
| Genuine objection | 2 | 2 | 3.50 | 0 | 0/0 |
| Irrelevant message | 4 | 2 | 1.75 | 0 | 0/2 |

These are raw pilot counts, not population estimates. Episodes from the same world are paired and must not be treated as independent replicates.

The model generated 24 followups in conditions other than the unsupported-objection condition. Every followup requested a source key already present in the complete signed bundle; the runner marked all 24 as duplicate dependencies. Manual inspection of their claims and parent-linked transcripts found repeated checks of the same role or integrity violation, not distinct new safety objections. Some paths reached processed depth four and were then censored by the configured cap. These paths are verification loops around existing violations, not evidence that the unsupported seed caused an endogenous cascade.

## Conclusion and decision

The v3.3 smoke does **not** demonstrate the proposed Safety Cascade Paradox. Under this prompt and checkpoint, the unsupported concern was resolved against the signed evidence at the root, while deeper paths occurred around already-present genuine violations and were duplicate checks. The appropriate report is “not observed in this diagnostic,” not “the phenomenon does not exist.” Do not estimate a branching factor from these data or use the apparent depth-four paths as cascade events.

The run also exposes two design limits that must be addressed before any larger claim: (1) the all-decline floor makes completion uninformative, and (2) the reviewer prompt supplies complete, authoritative evidence and explicitly discourages rechecking it. A follow-up discovery design would need a realistic evidence freshness/trust model and a baseline prompt that permits justified uncertainty, while keeping policy facts and the seed intervention paired. That design change must be declared before a new run; it must not be introduced selectively to elicit cascades. Until it produces actual distinct followups on a model-authored path, there is no basis to build or claim a cascade-prevention mechanism.

The literature review in `docs/cascade-literature-review.md` covers closely related recursive critique, false-alarm relay, message fault propagation, injected hallucination propagation, and budgeted/fatigue-aware oversight. This pilot does not establish novelty against that literature.
