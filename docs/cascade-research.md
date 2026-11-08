# Safety-cascade research status

## Current question

Can one unsupported safety objection induce otherwise compliant language-model reviewers to create new verification obligations over multiple interaction generations, reducing completion of a legitimate action? Every downstream obligation must appear in a model response; a scripted queue is not evidence for the claim.

This question supersedes verification-budget allocation as the central research direction. Earlier VetoNet queue and allocation results remain in `results/` as historical baselines and must not be presented as evidence for an endogenous cascade.

## Discovery evidence to date

### Version 1 pilot

One episode per condition and model. This pilot was schema-sensitive and is not interpretable as a cascade test. Qwen generated one child for the unsupported objection, whose evidence lookup resolved the approval concern; malformed or contradictory outputs occurred in other conditions. SmolLM2 also produced malformed or contradictory responses. Details remain in `docs/cascade-discovery-pilot.md`.

### Version 2 pilot

Four fixed-world episodes per condition and model, with JSON examples and exact-key evidence lookup. Full raw trajectories are `results/cascade-qwen-v2.json` and `results/cascade-smol-v2.json`.

Qwen generated no depth-two path in the four unsupported-objection episodes. One depth-two path occurred in the no-objection baseline: an ordinary authorization checklist led from the `change_window` fact to the separate `environment` fact. This is not an objection cascade. The unsupported concern generated one or two first-level checks; those branches then stopped. SmolLM2 produced no depth-two paths in any condition and failed the strict response schema on several branches. Its output cannot count as evidence of resolution. The pilot has four episodes per condition and a single artificial world, so it neither establishes the phenomenon nor rules it out.

## Current experiment

`experiments/cascade_network_v3.py` provides a structured-decoding interactive workflow with coordinator, worker, and critic roles; shared agent messages; model-generated follow-up requests; a synthetic evidence service; and a trusted execution monitor. Version 3.3 supplies the same signed evidence snapshot to each role and paired condition, so missing policy facts cannot explain added review. A child node is created only from a generated `followups` item. Evaluator condition labels and objection-dependency labels are excluded from prompts and structured task context. The monitor enforces authorization plus an empty review queue; it does not classify objections. One model's calls across roles are distinct contexts, not independent model instances.

The current runner is still a discovery instrument. It uses a single deployment policy, one GPU-local model per run, synthetic evidence, at most five generated follow-ups per call, and a bounded depth/node count. It can reveal whether actual model outputs contain multi-hop request paths in this setup. It cannot establish a general epidemic threshold or a NeurIPS-level contribution. Duplicate keys are logged, not suppressed in the exploratory path; semantic novelty and policy relevance require trajectory review.

### v3.3 model-family smokes: target effect not observed

Neutral-message Qwen2.5-3B and SmolLM2-1.7B smokes each ran 12 episodes over four paired worlds. Both authorized unsupported objections (role and approval variants) produced no followups in either model, as did their paired no-objection runs. Qwen's 24 generated followups elsewhere all queried source keys in the initial signed bundle and were repeated checks around existing violations. SmolLM2 generated 138 followups in the other conditions, also using already available keys; manual review found check restatements/fragments and one unrelated-message relay, but no new decision-relevant safety concern. Qwen's coordinator declined all episodes (completion floor). SmolLM2 completed both unsupported-objection authorized episodes but none of the two paired no-objection episodes, an unexpected two-world/single-seed reversal that cannot support an inference. These are negative diagnostics for the tested prompts/checkpoints, not evidence cascades cannot occur. See `docs/cascade-network-v3_3-pilot.md` and the raw/analyzer outputs `results/cascade-network-v3_3-{qwen,smol}-smoke*`.

The first Qwen v3 smoke exposed a protocol-design artifact: reviewers did not see sibling requests already waiting in the queue, and could repeatedly emit the same known policy checks. The run was stopped after five partial episodes were saved to `results/cascade-network-v3-qwen-smoke-diagnostic.json`. The v3.1 run exposed inconsistent evidence coverage, condition-sensitive completion, repeated review of already-verified facts, one genuine-violation path composed entirely of duplicate role checks, and two truncated JSON responses. Its six episodes are in `results/cascade-network-v3_1-qwen-smoke.json`. Neither smoke establishes the target phenomenon. A v3.2 labeled smoke then exposed evaluator-condition leakage in wording (“unsupported concern,” “genuine policy concern,” and “unrelated concern”), so `results/cascade-network-v3_2-qwen-labeled-smoke-diagnostic.json` is preserved but excluded from inference. Version 3.3 removes those labels and varies the unsupported objection across authorization predicates. It is a prompt-confound correction, not evidence that cascades exist.

## Decision rule

1. Keep the v3.3 result as a null discovery pilot and do not report the duplicate paths as safety cascades.
2. Do not design or claim a cascade defense without observing at least one distinct, model-authored, multi-generation safety-objection path under a valid control.
3. Any future discovery run needs a preregistered evidence-freshness/trust model and a prompt that avoids the all-decline floor without forcing execution. It must preserve paired worlds and use real model-generated followups. Do not tune prompts selectively to obtain the hypothesized effect.

## Literature and novelty boundary

The closest identified work is Wu et al., *Collective Loss of Control in LLM Agent Systems* (2026). It models mutation, transmission, and recovery and experimentally measures recipients' susceptibility to an injected unsafe trajectory. Its authors explicitly state that the study does not demonstrate a naturally unfolding autonomous cascade. This is a close precedent and narrows any possible contribution to empirical, safety-seeking escalation behavior—not cascades in general.

Hua et al. (NeurIPS 2025) optimize cost-constrained combinations of runtime monitors; Turan (2026) studies escalation capacity, fatigue, and flooding; Xia et al. (2026) synthesize and model-check multi-agent coordination protocols. These works make resource exhaustion, bounded monitoring, and protocol verification established adjacent areas. See `docs/cascade-literature-review.md` for sources and positioning. No novelty claim is justified by the current experiments.
