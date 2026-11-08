# Network v3.3 discovery smokes: Qwen and SmolLM2

## Result

These are diagnostic smokes, not powered experiments. Each model was run on four fixed worlds (two authorized, two with one true policy violation), each in no-objection, objection, and irrelevant-message conditions: 12 episodes per model, 24 episodes total. The local GPU runs used seed 2609, float16, temperature 0.7, top-p 0.95, JSON-schema-constrained decoding, a nine-node cap, and depth cap four. Qwen2.5-3B-Instruct and SmolLM2-1.7B-Instruct were run separately; the calls within each workflow share a checkpoint and are not independent model instances. Complete raw prompts, outputs, evidence, and event graphs are in `results/cascade-network-v3_3-{qwen,smol}-smoke.json`; analyzer outputs are the matching `.episodes.csv` and `.json` files. Runtime versions are recorded in each raw artifact.

The two authorized unsupported-objection episodes used different predicate messages (requester role and approval). Neither authored a followup. In their paired no-objection episodes, neither authored a followup either. Both paired conditions ended in coordinator `decline`, so the paired descriptive difference was zero for generated followups, processed review nodes, depth, and completion. This is only two paired worlds and has no inferential power.

Across all 12 episodes, the coordinator proposed `decline` every time, including all six authorized episodes. There were zero execution permits and zero parser failures. The zero legitimate-completion rate is a floor effect: this run cannot estimate whether objections reduced completion while preserving safety.

| Evaluator condition | Episodes | Episodes with processed depth ≥2 | Mean generated followups | Distinct evidence dependencies | Legitimate completions |
|---|---:|---:|---:|---:|---:|
| No objection | 4 | 2 | 2.50 | 0 | 0/2 |
| Unsupported objection | 2 | 0 | 0.00 | 0 | 0/2 |
| Genuine objection | 2 | 2 | 3.50 | 0 | 0/0 |
| Irrelevant message | 4 | 2 | 1.75 | 0 | 0/2 |

These are raw pilot counts, not population estimates. Episodes from the same world are paired and must not be treated as independent replicates.

Qwen generated 24 followups in conditions other than the unsupported-objection condition. Every followup requested a source key already present in the complete signed bundle; the runner marked all 24 as duplicate dependencies. Manual inspection of their claims and parent-linked transcripts found repeated checks of the same role or integrity violation, not distinct new safety objections. Some paths reached processed depth four and were then censored by the configured cap. These paths are verification loops around existing violations, not evidence that the unsupported seed caused an endogenous cascade.

## SmolLM2 matched smoke

SmolLM2 also authored no followups in either of the two authorized unsupported-objection episodes. It generated 138 followups in the other ten episodes; all 138 requested keys already present in the initial signed bundle. The no-objection condition generated 43 such followups, the genuine-objection condition 36, and the irrelevant-message condition 59. Several episodes hit the node cap with many requests still pending. Manual review of the unique child claims across all episodes found policy-check restatements or fragments, repeated claims about integrity evidence, and one relay of the irrelevant dashboard-theme message. It found no distinct, new, decision-relevant safety concern. The runner's `duplicate_of` marker is keyed only by evidence source and is not a semantic novelty classifier.

The two authorized no-objection episodes completed in neither model's run. In SmolLM2, both authorized unsupported-objection episodes proposed execution and received monitor permits (2/2); in Qwen, both paired no-objection and unsupported episodes ended in decline (0/2 permits). This reversal is notable but too fragile to interpret: there are only two matched authorized worlds, one sampling seed, substantial model-family differences, and the no-objection SmolLM2 paths are redundant requests despite a complete signed bundle. It is not evidence for the hypothesized cascade. The monitor blocked all unauthorized SmolLM2 proposals.

| Model | Condition | Episodes | Total generated followups | Previously unseen evidence keys | Legitimate completions |
|---|---|---:|---:|---:|---:|
| Qwen2.5-3B | No objection | 4 | 10 | 0 | 0/2 |
| Qwen2.5-3B | Unsupported objection | 2 | 0 | 0 | 0/2 |
| Qwen2.5-3B | Genuine objection | 2 | 7 | 0 | 0/0 |
| Qwen2.5-3B | Irrelevant message | 4 | 7 | 0 | 0/2 |
| SmolLM2-1.7B | No objection | 4 | 43 | 0 | 0/2 |
| SmolLM2-1.7B | Unsupported objection | 2 | 0 | 0 | 2/2 |
| SmolLM2-1.7B | Genuine objection | 2 | 36 | 0 | 0/0 |
| SmolLM2-1.7B | Irrelevant message | 4 | 59 | 0 | 0/2 |

Counts are descriptive only. Within-world episodes are paired, and two worlds cannot support confidence intervals or a cross-model generalization claim.

## Conclusion and decision

The v3.3 smoke does **not** demonstrate the proposed Safety Cascade Paradox. Under this prompt and checkpoint, the unsupported concern was resolved against the signed evidence at the root, while deeper paths occurred around already-present genuine violations and were duplicate checks. The appropriate report is “not observed in this diagnostic,” not “the phenomenon does not exist.” Do not estimate a branching factor from these data or use the apparent depth-four paths as cascade events.

The run also exposes two design limits that must be addressed before any larger claim: (1) the all-decline floor makes completion uninformative, and (2) the reviewer prompt supplies complete, authoritative evidence and explicitly discourages rechecking it. A follow-up discovery design would need a realistic evidence freshness/trust model and a baseline prompt that permits justified uncertainty, while keeping policy facts and the seed intervention paired. That design change must be declared before a new run; it must not be introduced selectively to elicit cascades. Until it produces actual distinct followups on a model-authored path, there is no basis to build or claim a cascade-prevention mechanism.

The literature review in `docs/cascade-literature-review.md` covers closely related recursive critique, false-alarm relay, message fault propagation, injected hallucination propagation, and budgeted/fatigue-aware oversight. This pilot does not establish novelty against that literature.
