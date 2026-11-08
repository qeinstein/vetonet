# VetoNet research pilot

A preliminary study of how refusals, evidence and delegation affect safety and legitimate completion. The current results are synthetic pilots, not evidence that the protocol outperforms an equally informed policy gate. See [the working paper](main.pdf), [experimental details](experiments/README.md), and [literature notes](docs/literature-notes.md).

## Reproduce analysis

The analysis and prototype use Python 3.10 or later and the standard library. From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 experiments/analyze_pilot.py results/qwen25_3b_pilot.json
python3 experiments/analyze_pilot.py results/smol_original.json anchored
python3 experiments/analyze_context.py results/qwen_context.json results/smol_context.json
python3 experiments/objection_replay.py results/smol-forced-original.json --output /tmp/vetonet-replay.json
python3 experiments/evidence_stress.py --output /tmp/vetonet-evidence.json
```

The GPU pilot uses PyTorch, transformers 4.57.3, accelerate, CUDA and local model weights. Run `python experiments/run_model.py --help` or `python experiments/context_propagation.py --help` for arguments. Model weights are not included. Stored raw outputs use local server paths as model identifiers; the original downloads did not record immutable Hugging Face revisions, so exact weight-level reproduction is not established. Sampling can differ across hardware and library versions. The forced-choice score is a measurement sensitivity analysis and the samples are not interactive agent trajectories.

Compile the draft with `pdflatex main.tex` twice; `images/protocol.tex` is the source for the diagram. The PDF is currently a working draft with a placeholder author and is not verified against the official sprint template. Do not deploy the in-memory ledger as an authorization system: it does not authenticate sources or atomically bind state to execution.
