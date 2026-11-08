# Focused literature review: autonomous safety-verification cascades

Reviewed 2026-11-08. This is a focused review of the four directly named neighboring works, not an exhaustive novelty search.

## Closest precedent: contagion in agent systems

Wu et al., *Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery*, arXiv:2609.18460 (2026), distinguish spontaneous behavioral mutation from contagion after an unsafe trajectory is passed to another session. Their empirical study injects a frozen unsafe trajectory into recipient routes and measures conditional susceptibility across 20 executable scenarios. The paper explicitly states that this design does **not** establish natural rare-event rates or demonstrate an autonomous cascade. The conceptual overlap is direct: a local event, agent-to-agent transmission, and collective failure. The differentiating hypothesis in this repository is narrower and unverified: an injected *safety objection* might cause honest recipients to author additional verification requests, rather than recipients adopting a supplied unsafe strategy. This distinction alone does not establish novelty.

Primary source: [arXiv:2609.18460](https://arxiv.org/abs/2609.18460).

## Cost-constrained runtime monitoring

Hua et al., *Combining Cost-Constrained Runtime Monitors for AI Safety*, NeurIPS 2025, optimize which monitors and interventions to invoke under an average-case cost budget, using monitor characteristics and likelihood ratios. They report a code-review setting where combining monitors can Pareto-dominate either monitor alone. This makes budgeted verification allocation an established problem and rules out presenting a better queue schedule as the sole contribution. It does not, based on the paper's stated problem, model agents recursively authoring new verification obligations in response to earlier objections.

Primary sources: [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ed56a654ddb681841fdb2184463c253e-Abstract-Conference.html); [OpenReview paper PDF](https://openreview.net/pdf?id=hVR3023UP2).

## Escalation capacity and flooding

Turan, *Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human*, arXiv:2606.08919 (2026), studies selective escalation under asymmetric costs and a reviewer whose effectiveness declines with load. The paper reports an inverted-U relation between escalation and realized safety in its modeled setting and discusses a flooding attack. This is close prior art for the claim that excessive safety escalation can reduce safety/availability. The proposed cascade hypothesis must therefore establish *endogenous agent-generated propagation* as the mechanism, rather than rediscovering that flooding or high load can overwhelm oversight.

Primary source: [arXiv:2606.08919](https://arxiv.org/abs/2606.08919).

## Coordination verification

Xia et al., *TraceFix: Repairing Agent Coordination Protocols with TLA+ Counterexamples*, arXiv:2605.07935 / CAIS 2026, synthesize a coordination protocol, model-check it with TLC, and repair failures using counterexamples. This makes protocol correctness, deadlock, and liveness in multi-agent workflows established concerns. TraceFix focuses on verifying protocol structures and runtime conformance, rather than measuring whether model-generated safety objections propagate across otherwise compliant reviewers.

Primary source: [arXiv:2605.07935](https://arxiv.org/abs/2605.07935); [project page](https://snr.rutgers.edu/focus/agentic.html).

## Implications for the experiment

The experimental unit cannot be a synthetic queue event. It must be a model-authored message that creates a new child request, followed by an actual model response to that request. A path of depth two is not automatically a safety cascade: it may be an ordinary checklist (for example, checking a second required authorization predicate), duplicate wording, or a fixed-workflow artifact. The study must retain the complete prompt/response graph and classify each edge by whether it introduces a distinct concern, depends on the seed, is policy relevant, and could change the action's authorization.

The empirical claim, if any, must be limited to the tested model, prompt, task distribution, communication topology, and evidence API. Distinct role prompts executed by the same checkpoint are not independent agents or independent replications. A finite pilot can show an observed behavior or lack of observation, but not establish a branching-process phase transition or a general reproduction threshold.

## Open review items

- Search for related work on recursive debate/critique, verification loops, escalation contagion, workflow deadlock, and endogenous alarms in non-LLM distributed systems.
- Inspect citations and subsequent work from Wu et al. and Turan; verify publication status and any benchmark/code releases.
- Check whether multi-agent workflow studies report model-generated follow-up requests as an outcome, rather than only injected context or scripted task queues.
- Compare any proposed intervention against established selective classification, deduplication, semantic caching, escalation limits, and policy monitors.

