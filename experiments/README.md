# Experimental design (working draft)

The sprint's example already proposes refusal shopping, so this study extends it with false objections and independently checked evidence. All actions are simulated; no real records or services are changed.

Generate paired synthetic requests with known authorization, varying the requester, resource, policy and evidence. Sample worker decisions independently for the same request under matched prompts. Compare first decision, retry after refusal, unconditional veto, majority vote, and a deterministic evidence-checking gate. Introduce a controlled false objection and vary whether authoritative evidence is available. Evaluate unauthorized execution and authorized completion separately, with uncertainty at the scenario level. Report missing and unparseable outputs rather than silently excluding them. The evidence-checking gate is a strong baseline; a protocol with the same information must not be presented as superior without evidence.

The provided server has an RTX A5000 (24 GB), PyTorch 2.8.0+cu128, and a 28 GB workspace. A background process is installing transformers and downloading Qwen2.5-3B-Instruct under `/workspace`; inspect `/workspace/install.log` and process 491 before rerunning. No experiment results have yet been collected.
