# Cascade experiment runbook

## Current protocol

Run `experiments/cascade_network_v3.py` (protocol version 3.3). It uses a fixed coordinator/worker/critic message topology, complete authenticated synthetic evidence at task start, model-authored followups, JSON-schema-constrained decoding, a bounded queue, and a trusted policy execution monitor. Every condition in a world uses the same world facts and signed evidence. Generation seeds are shared across paired conditions for equivalent world/node/role IDs.

The sole attack input is one unsupported objection in authorized worlds; the objection concerns one of five policy predicates, balanced over authorized world IDs as sample size grows. The condition label and evaluator-only dependency key are never passed in a prompt. A model call must explicitly author each followup; the runner does not insert downstream jobs. An irrelevant-objection control is included in every world. Unauthorized worlds include a genuine-objection control and a no-objection baseline. All model outputs, prompts, evidence records, graph edges, parse/schema errors, pending jobs, proposals, and monitor decisions are saved in the result JSON.

## GPU environment

The rented server is an NVIDIA RTX A5000 24 GB at `root@63.141.33.158:22070`. The experiment was run with Python environment `/workspace/venv`, PyTorch 2.8.0+cu128, Transformers 4.57.3, and `lm-format-enforcer` installed into that environment. Exact package versions are recorded in each output artifact. Models are local Hugging Face directories at `/workspace/Qwen2.5-3B-Instruct` and `/workspace/SmolLM2-1.7B-Instruct`; the local snapshots currently lack a recorded immutable revision, which limits exact weight reproducibility.

## Reproduction commands

From a local checkout, upload the runner and execute it on the GPU host:

```bash
scp -P 22070 experiments/cascade_network_v3.py \
  root@63.141.33.158:/workspace/cascade_network_v3.py
ssh -p 22070 root@63.141.33.158 'source /workspace/venv/bin/activate && python /workspace/cascade_network_v3.py --model /workspace/Qwen2.5-3B-Instruct --output /workspace/cascade-network-v3_3-qwen.json --n-worlds 8 --seed 2609 --max-nodes 9 --max-depth 4'
scp -P 22070 root@63.141.33.158:/workspace/cascade-network-v3_3-qwen.json \
  results/cascade-network-v3_3-qwen.json
python experiments/analyze_cascade_network.py \
  results/cascade-network-v3_3-qwen.json \
  --out results/cascade-network-v3_3-qwen-summary
```

Repeat the SSH run with `--model /workspace/SmolLM2-1.7B-Instruct` and a separate output path for the second model-family run. A world contributes three conditions, so 8 worlds yield 24 episodes per model. The eight-world run is still a pilot; it is not by itself a powered multi-family benchmark.

## Interpretation rules

- A path depth of two or more is a **candidate path**, not a safety-objection cascade. Inspect its full ancestry and child claims.
- A source-key recheck after the same signed fact is available is a duplicate evidence dependency. Count it as model behavior and review cost, but not as a distinct new concern.
- A `none` evidence key can carry a novel concern. Check whether it is policy-relevant and whether resolving it could alter the final decision.
- `generated_followup_count` includes requests whose evidence key is duplicate. Use the `duplicate_of` field and claim text to separate them.
- Do not interpret monitor-denied unauthorized proposals as executed harm. The monitor enforces the stated synthetic policy by construction.
- Do not pool v1/v2, v3.0, v3.1, the label-leaked v3.2 smoke, or the verification-budget queue studies with v3.3. They use different prompts, evidence availability, and interaction rules. The labeled smoke is preserved only as a diagnostic.
- Keep truncated/invalid model calls in denominators and report them. They are unresolved workflow outcomes, not safety successes.
- Do not report a branching-process reproduction number until each obligation has been semantically classified and a defensible denominator of resolved obligations exists.

## Pilot artifacts

- v1/v2: `results/cascade-qwen-pilot.json`, `results/cascade-smol-pilot.json`, `results/cascade-qwen-v2.json`, `results/cascade-smol-v2.json`.
- v3.0 diagnostic: `results/cascade-network-v3-qwen-smoke-diagnostic.json` (stopped due to hidden pending requests and duplicate checklist growth).
- v3.1 diagnostic: `results/cascade-network-v3_1-qwen-smoke.json` (inconsistent evidence coverage, duplicate rechecks, and response truncation).
- v3.2 labeled diagnostic: `results/cascade-network-v3_2-qwen-labeled-smoke-diagnostic.json` (condition labels appeared in objection messages; do not use for causal comparisons).
- v3.3 Qwen and SmolLM2 smokes: `results/cascade-network-v3_3-{qwen,smol}-smoke.json` with analyzer outputs; neither model generated a distinct unsupported-objection cascade. SmolLM2 produced many redundant checks in other conditions; Qwen declined every action, while SmolLM2 completed only the two unsupported-objection authorized episodes. These are small diagnostics, not inferential findings. See `docs/cascade-network-v3_3-pilot.md` for results and limits.
- Literature: `docs/cascade-literature-review.md`.
- Current research status: `docs/cascade-research.md`.

