My assessment of the proposed NeurIPS contribution
There is one issue I would emphasize before beginning a three-month research programme: the proposed protocol is not yet demonstrably novel enough for NeurIPS.

A recent October 2026 IETF Internet-Draft already distinguishes unavailable authorization evidence from verified negative evidence. Its requirements overlap with part of our proposed decision representation. It is a work-in-progress document rather than an adopted standard, but we still need to account for it. IETF Datatracker

We also have existing external authorization research that prevents unauthorized actions through deterministic enforcement. Amazon Science

Consequently, the strongest contribution would not be the protocol alone.

I would prioritize discovering and formally characterizing the safety–availability trade-off. If we can establish a general phenomenon, show that existing mechanisms fail under meaningful assumptions, derive useful bounds, and demonstrate a method that improves the frontier, the work becomes substantially more compelling.

The benchmark could also be important. AgentDojo and τ-bench demonstrate how rigorous, reproducible environments can become major research contributions, even when they don't introduce a new foundation model. NeurIPS Proceedings

For the immediate Apart submission, though, we should extract only the first experimental question and one defensible intervention. The conference research and the hackathon project should share a foundation without pretending that a weekend experiment validates the entire proposed theory.