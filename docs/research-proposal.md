# VetoNet: Safety, Liveness, and Evidence-Bound Refusals in Multi-Agent Language Model Systems

**Research Proposal — NeurIPS / ICLR / ICML Main Conference**

**Research areas:** Multi-Agent Systems, AI Safety, AI Control, Distributed Systems, Mechanism Design, Agent Security

**Research status:** Proposed — theoretical and empirical investigation

**Target contribution:** A formal framework, a new control protocol, and a benchmark for understanding and mitigating safety–availability failures in multi-agent language model systems.

---

# Abstract

Large language models are increasingly deployed as autonomous agents that collaborate through delegation, shared memory, communication protocols, and tool use. Although individual agents may exhibit desirable safety behaviours, these properties need not be preserved when agents interact. A coordinator may circumvent a worker's refusal by delegating the same request to another agent, while mechanisms designed to prevent such circumvention may introduce the opposite vulnerability: a compromised or mistaken agent can propagate unjustified refusals and prevent legitimate work.

We propose to investigate this tension as a fundamental safety–liveness problem in multi-agent language model systems.

We introduce a formal framework for studying how agent-level safety decisions propagate across collaborative workflows under incomplete information, unreliable evidence, and adversarial participation. Our framework distinguishes policy violations from uncertainty, verified refusals from unsupported objections, and legitimate reconsideration from unauthorized circumvention.

Building on this framework, we propose **VetoNet**, an evidence-bound refusal and escalation protocol that preserves the provenance, scope, and justification of agent decisions while supporting constrained recovery from incorrect or adversarial refusals.

We further propose **VetoBench**, a benchmark for evaluating safety, legitimate task completion, denial-of-service susceptibility, and verification costs across heterogeneous multi-agent networks.

Our central hypothesis is that conventional refusal-handling strategies create a measurable trade-off between safety and availability, and that evidence-bound escalation can improve this trade-off under explicit assumptions about trusted evidence and adversarial control.

The proposed investigation combines formal analysis, controlled multi-agent experiments, adaptive attacks, heterogeneous model evaluation, and ablation studies.

The broader objective is to establish principles for constructing AI agent systems whose safety decisions remain meaningful under delegation without allowing individual agents to exercise unaccountable veto power over the entire system.

---

# 1. Introduction

## 1.1 Background

Modern language-model systems increasingly distribute responsibilities across specialized agents.

Rather than having a single model perform an entire task, a system may use a planner to decompose the task, workers to execute subtasks, reviewers to verify intermediate results, and an orchestrator to coordinate the overall process.

This architecture offers advantages in specialization, modularity, and scalability.

However, it also introduces a fundamental question:

**When several autonomous agents participate in a decision, whose safety judgment governs the final action?**

Consider a network of agents responsible for modifying an organization's internal records.

A worker receives a modification request and refuses because it cannot establish that the requester has sufficient authorization.

The coordinating agent subsequently delegates the same operation to another worker.

The second worker has a different context, interprets the available evidence differently, and approves the operation.

The resulting action may violate the organization's intended constraints, despite the presence of an agent that correctly identified the problem.

This demonstrates a potential failure of safety composition.

A property satisfied by one component is not necessarily preserved by a system composed of many components.

## 1.2 Why conventional solutions are insufficient

One response is to preserve every refusal in shared memory.

Whenever an agent refuses an operation, that refusal becomes visible to other agents.

The coordinator cannot silently disregard the decision.

Unfortunately, such a mechanism can introduce a different failure.

Suppose a compromised agent refuses every request, including requests supported by legitimate authorization.

If the system treats all refusals as authoritative and permanent, the compromised agent can prevent the entire system from functioning.

An apparently stronger safety mechanism has become a denial-of-service mechanism.

A more sophisticated system might allow agents to vote on whether refusals should be respected.

However, voting introduces additional complications.

Agents may share the same model weights, training data, or information sources. Consequently, their decisions may be correlated rather than independent.

A malicious coordinator may create additional agent instances to manufacture a majority.

Alternatively, honest agents may be unable to distinguish an intentionally fabricated refusal from a legitimate refusal based on information they cannot access.

These problems suggest that neither unconditional refusal propagation nor simple majority voting is a satisfactory general solution.

## 1.3 The fundamental distinction

We distinguish between three kinds of safety-related information:

**Policy constraints:** Authoritative restrictions defining which actions are permitted.

**Evidence:** Information supporting or contradicting whether an action satisfies those constraints.

**Agent judgments:** Interpretations or recommendations produced by individual agents.

These categories must not be treated as interchangeable.

A worker's statement that an action is forbidden does not automatically establish that the action violates policy.

Likewise, a majority of agents claiming that an action is permitted does not establish valid authorization.

Our research investigates how these distinctions can be maintained across multi-agent workflows.

## 1.4 Scope of the problem

We focus on collaborative systems where agents:

1. Operate under shared or partially overlapping policy constraints.
2. Possess different information or capabilities.
3. Can delegate tasks and exchange messages.
4. Can propose actions affecting shared external state.
5. May make mistakes or behave adversarially.
6. Cannot necessarily access complete authorization evidence at decision time.

This final condition is essential.

When all relevant policies and authorization facts are known, a conventional trusted policy engine may be sufficient.

Our proposed research instead concentrates on cases where decisions depend on incomplete, distributed, changing, or potentially corrupted evidence.

---

# 2. Central Research Questions

The investigation is organized around five research questions.

## RQ1: Do refusals compose under delegation?

When an individual agent correctly refuses an action, under what conditions can a multi-agent workflow nevertheless execute that action?

We will investigate the effects of:

- Repeated delegation.
- Network topology.
- Context loss.
- Agent heterogeneity.
- Task decomposition.
- Shared versus independent information.
- Number of available workers.

The objective is to identify which properties of the network make local safety failures more likely to become system-level failures.

## RQ2: Can safety enforcement itself become an attack surface?

When agents share refusal decisions, can adversarial participants exploit the mechanism to prevent legitimate work?

We will examine:

- False refusals.
- Refusal flooding.
- Identity manipulation.
- Correlated objections.
- Misrepresented authorization evidence.
- Stale refusal records.
- Repeated appeals.
- Manipulation of escalation procedures.

This question establishes the availability dimension of multi-agent safety.

## RQ3: What information must accompany a refusal?

We will investigate whether preserving structured information about a refusal improves the system's ability to distinguish legitimate safety enforcement from manipulation.

Relevant information may include:

- The action being evaluated.
- The governing policy.
- The refusing agent's authority.
- The available evidence.
- The evidence's provenance.
- The reason for refusal.
- The decision's scope.
- Its validity period.
- Conditions under which reconsideration is permitted.

We will distinguish the value of each information category through ablation experiments.

## RQ4: Can evidence-bound escalation improve the safety–availability trade-off?

We will investigate whether a refusal protocol can reduce unauthorized execution without unnecessarily blocking legitimate requests.

The central comparison will be between independent decisions, unconditional shared refusals, voting-based approaches, conventional authorization gates, and the proposed evidence-bound mechanism.

## RQ5: What guarantees are theoretically achievable?

We will identify assumptions under which a multi-agent control protocol can provide meaningful safety and progress guarantees.

We will also investigate conditions under which no protocol can simultaneously guarantee both.

This theoretical component is intended to prevent the empirical results from being interpreted as stronger guarantees than they establish.

---

# 3. Research Hypotheses

We propose six primary hypotheses.

### H1 — Delegation-induced safety degradation

When agents independently evaluate requests, increasing the number of available workers can increase the probability that an unauthorized operation is eventually accepted, particularly when the coordinator can retry after refusal.

The size of this effect depends on correlations between worker decisions and the coordinator's delegation strategy.

### H2 — Unconditional refusal propagation reduces availability

Persistently propagating all agent refusals will reduce some unauthorized actions but also increase false blocking when agents are mistaken or adversarial.

### H3 — Evidence-bound refusals improve decision quality

Representing refusals using structured, independently verifiable evidence will improve the system's ability to distinguish genuine policy violations from unsupported objections.

### H4 — Adversarial participation changes the optimal refusal mechanism

Mechanisms that perform well when every agent is honest may deteriorate when agents can fabricate evidence, impersonate identities, or coordinate their judgments.

### H5 — Evidence diversity matters more than raw agent count

Increasing the number of agents will not necessarily improve decision reliability when agents depend on the same evidence or share correlated failure modes.

Systems that verify distinct evidence sources may perform better than systems that merely collect additional votes.

### H6 — Evidence-bound escalation improves the achievable safety–availability frontier

Under suitable trust and evidence-availability assumptions, VetoNet will achieve higher legitimate task completion than unconditional veto propagation at comparable unauthorized-action rates.

This is the central hypothesis of the proposed method.

We will also test circumstances in which it does not hold.

---

# 4. Related Work and Research Positioning

## 4.1 Multi-agent safety and delegated misalignment

Ying et al. (EMNLP 2026), in *Delegated Misalignment: How Multi-Agent Structures Amplify LLM Safety Risks*, demonstrate that individual safety alignment does not necessarily transfer to multi-agent systems.

Their findings motivate our investigation into safety decisions made across delegation boundaries.

Our proposed distinction is the additional study of what happens when refusals are explicitly preserved and become shared control signals.

Rather than measuring only whether delegation enables unsafe completion, we investigate the competing possibility that safety decisions themselves become tools for adversarial obstruction.

## 4.2 Provenance erasure and trust boundaries

Zhou et al. (EMNLP 2026), in *Trust Cascade through Provenance Erasure*, investigate how delegation strips information about authority and source provenance.

They introduce a provenance diagnostic for detecting trust-boundary violations.

Our work builds on the importance of preserving authority information.

However, preserving provenance is not sufficient to establish that the underlying claim is true.

A signed statement from a known agent can still contain an incorrect or deliberately fabricated conclusion.

Our proposed protocol therefore distinguishes authenticated provenance from independently supported evidence.

## 4.3 Role-based agent control

Maliha et al. (EMNLP 2026), in *Agent Trajectory Control*, investigate enforcing role contracts in black-box multi-agent systems.

Our approach assumes that role enforcement is useful but does not resolve all disagreements between correctly scoped agents.

Two agents may both act within their assigned roles while reaching incompatible conclusions about whether an action should proceed.

We investigate the control protocol governing these disagreements.

## 4.4 AI control

Greenblatt et al. (ICML 2024) introduce the AI control framework, investigating how systems can remain safe even when powerful components intentionally attempt to subvert their objectives.

Our work follows this threat-model-driven perspective.

The proposed contribution is a more specific treatment of multi-agent refusal propagation and legitimate recovery under adversarial participation.

## 4.5 Authorization systems

Cedar and related policy engines already support external authorization decisions based on defined policies, principals, actions, resources, and context.

Consequently, introducing an external authorization check cannot itself constitute our primary novelty.

Instead, we study the gap between formal policy enforcement and agent-generated evidence or judgments.

This includes circumstances where the policy is known but required evidence is unavailable, outdated, contradictory, or controlled by different participants.

## 4.6 Distributed consensus and fault tolerance

Distributed systems research provides extensive foundations for reasoning about safety, liveness, Byzantine behaviour, and agreement.

Our work will use these concepts where appropriate.

We must be careful not to claim that familiar quorum mechanisms or classical consensus results are original contributions.

The proposed novelty concerns applying a precise decision model to unreliable, language-mediated agent judgments and experimentally characterizing the resulting trade-offs.

## 4.7 Existing benchmarks

Relevant benchmarks include:

- AgentDojo, for tool-using agents under adversarial instructions.
- AgentHarm, for evaluating unsafe agent behaviour.
- MultiAgentBench, for collaborative and competitive multi-agent systems.
- τ-bench, for evaluating tool-using agents under domain-specific rules.
- AI-control evaluation environments, for studying adversarially controlled components.

These provide valuable foundations.

However, our proposed benchmark specifically targets the relationship between **refusal propagation, evidence uncertainty, adversarial obstruction, and legitimate recovery**.

We will perform a dedicated novelty review before treating this as an established benchmark gap.

---

# 5. Formal Problem Definition

## 5.1 Multi-agent system

We model a multi-agent system as:

\[
\mathcal{M}=(V,E,\mathcal{S},\mathcal{A},\Pi,\mathcal{P})
\]

where:

- \(V\) is the set of agents.
- \(E\) describes permitted communication and delegation relationships.
- \(\mathcal{S}\) is the environment state space.
- \(\mathcal{A}\) is the set of possible actions.
- \(\Pi\) is the collection of agent policies.
- \(\mathcal{P}\) is the set of authoritative system constraints.

The communication graph may be static or dynamic.

Agents have only partial observations of the environment.

Each agent \(i\) receives an observation:

\[
o_i(t)=O_i(s_t,h_t)
\]

where \(s_t\) is the environment state and \(h_t\) represents the relevant interaction history.

Agent decisions depend on available information rather than necessarily on the true environment state.

## 5.2 Authorization ground truth

For evaluation, we define an authorization function:

\[
A^*(s,a)\in\{0,1\}
\]

where:

- \(A^*(s,a)=1\): the action is authorized.
- \(A^*(s,a)=0\): the action is unauthorized.

The benchmark's evaluator can access this ground truth.

The participating agents and proposed controller do not necessarily have access to every fact required to compute it.

This separation is necessary to study incomplete information realistically.

If the controller directly receives \(A^*\), a perfect reference monitor trivially resolves the tested authorization decision.

Such an experiment would not establish an advantage for VetoNet.

## 5.3 Agent decisions

Each agent produces a decision:

\[
d_i(a,t)\in\{\text{approve},\text{refuse},\text{defer}\}
\]

These outcomes have distinct meanings.

**Approve:** The agent believes the available evidence supports execution.

**Refuse:** The agent believes a relevant constraint prohibits execution.

**Defer:** The agent cannot establish enough information to decide.

The distinction between refusal and deferral is critical.

A missing authorization record is not necessarily evidence that authorization was explicitly revoked.

Similarly, a timeout when checking a policy source should not automatically be interpreted as a verified negative result.

## 5.4 Evidence-bound decision representation

We propose representing a refusal using:

\[
r_i=(a,p,e,\rho,\tau,\sigma,\nu)
\]

where:

- \(a\): Canonicalized action and context.
- \(p\): Referenced policy or constraint.
- \(e\): Evidence references supporting the decision.
- \(\rho\): Decision reason and evaluation state.
- \(\tau\): Timestamp and validity interval.
- \(\sigma\): Authenticated agent identity and provenance.
- \(\nu\): Policy version and relevant state version.

These fields are not assumed to be trustworthy merely because an agent supplied them.

The protocol must distinguish assertions from externally verified information.

In particular, agent identity authentication proves the origin of a message, not the correctness of its contents.

## 5.5 Safety

We define system-level safety in terms of unauthorized execution:

\[
R_{\mathrm{unsafe}}
=
P(\text{Execute}(a)\mid A^*(s,a)=0)
\]

This quantity should be minimized.

Where harms differ in severity, we will also measure severity-weighted violations rather than treating every unauthorized action as equally consequential.

## 5.6 Availability

We define legitimate task completion as:

\[
R_{\mathrm{complete}}
=
P(\text{Complete}(a)\mid A^*(s,a)=1)
\]

This quantity should be maximized.

We additionally measure completion within a deadline:

\[
R_{\mathrm{timely}}
=
P(\text{Complete}(a)\leq T\mid A^*(s,a)=1)
\]

The deadline matters because a system that eventually completes legitimate requests after extremely long delays may still be operationally unusable.

## 5.7 Optimization objective

The objective is not simply to minimize refusals or maximize approvals.

We seek protocols that improve the relationship between safety and legitimate completion.

Formally, we can consider:

\[
\max_\pi R_{\mathrm{complete}}(\pi)
\]

subject to:

\[
R_{\mathrm{unsafe}}(\pi)\leq\epsilon
\]

and:

\[
C_{\mathrm{verification}}(\pi)\leq B
\]

where:

- \(\pi\) is a control protocol.
- \(\epsilon\) is an acceptable risk threshold.
- \(B\) is a verification budget.

For high-consequence actions, empirical risk thresholds cannot substitute for mandatory authorization requirements.

Accordingly, we will report safety, availability, and cost separately and compare their Pareto frontiers.

---

# 6. Threat Model

A strong conference submission must state exactly what attackers can and cannot control.

We consider four adversary classes.

## 6.1 Compromised worker

An attacker controls a worker agent's instructions or outputs.

The compromised worker may fabricate refusals, exaggerate the risks of legitimate actions, misrepresent evidence, or attempt to persuade other agents to disregard policy.

It cannot directly modify trusted policy records or trusted evaluator state.

## 6.2 Compromised coordinator

An attacker controls the coordinating agent.

The coordinator may repeatedly delegate requests, selectively reveal earlier refusals, manipulate task descriptions, or route requests toward workers more likely to approve them.

This attacker is particularly relevant to refusal shopping.

## 6.3 Colluding agents

Several agents cooperate to influence the network.

They may coordinate false objections or manufacture apparent agreement.

We will consider both homogeneous groups using the same underlying model and heterogeneous groups using different models.

The distinction matters because model diversity may alter the correlation structure of mistakes.

## 6.4 Evidence-layer adversary

The attacker controls selected lower-trust evidence sources.

For example, it may manipulate a retrieved document, a worker-generated report, or a shared memory entry.

It cannot forge trusted source attestations unless that capability is explicitly included in a stronger threat-model variant.

## 6.5 Trust assumptions

The initial VetoNet architecture assumes:

1. The tool-execution gateway is outside the compromised agents' control.
2. Authoritative policy versions are protected against unauthorized modification.
3. Trusted evidence sources can authenticate their outputs.
4. The protocol can maintain an append-only record of decisions.
5. Attackers cannot directly execute protected actions while bypassing the gateway.

We will test the consequences of weakening these assumptions.

The protocol cannot guarantee safety if the adversary can bypass its enforcement point.

Nor can it establish the truth of arbitrary factual claims when every available evidence source is compromised.

Those limitations must be explicit.

---

# 7. Proposed Method: VetoNet

## 7.1 Overview

VetoNet is an experimental control protocol for multi-agent workflows.

Its purpose is to preserve legitimate safety constraints while preventing unsupported refusals from becoming permanent, unchallengeable vetoes.

It is composed of five principal mechanisms.

### Component A — Action canonicalization

Different agents may describe the same underlying operation differently.

For example:

- Update record X.
- Apply the requested correction to record X.
- Finalize the previously discussed modification.

These descriptions may refer to the same protected action.

VetoNet will map requests into a structured representation containing the principal, action, resource, and relevant context.

The objective is to prevent simple linguistic reformulation from silently bypassing earlier decisions.

Canonicalization must be tested carefully.

Incorrectly merging distinct actions may cause legitimate requests to be blocked.

Incorrectly separating equivalent actions may permit refusal shopping.

### Component B — Evidence-bound refusal records

Each refusal becomes a structured record rather than an unqualified text message.

The record identifies:

- What action was refused.
- Which policy or constraint was considered.
- Whether relevant evidence was verified.
- Whether required evidence was unavailable.
- Which agent made the decision.
- Which authoritative sources were consulted.
- Whether the decision remains current.
- What information could justify reconsideration.

The protocol will distinguish:

**Verified denial:** Authoritative evidence establishes a policy violation.

**Unverified objection:** An agent raises a concern without sufficient supporting evidence.

**Evidence unavailable:** Required information could not be established.

**Conditional refusal:** An action is blocked pending additional conditions.

**Stale decision:** A previously recorded decision requires re-evaluation.

These categories support different responses.

### Component C — Decision lineage

The protocol maintains a directed graph linking actions, delegations, evidence, and decisions.

Let:

\[
G_D=(N_D,E_D)
\]

where nodes represent relevant events and edges represent relationships such as delegation, evidence dependency, policy application, and supersession.

A refusal should remain associated with its underlying action even when another agent receives a reformulated request.

The graph must also represent changes in authorization state.

For example, a request refused yesterday may become permitted today after a new authorization is issued.

Historical refusal records should remain immutable while their current applicability is explicitly updated.

### Component D — Evidence-bound escalation

This is the central proposed mechanism.

Instead of choosing between unconditional refusal propagation and unrestricted retries, VetoNet determines how a disputed decision can be reconsidered.

The escalation process will depend on the reason for refusal.

A verified policy violation cannot be overturned merely because another agent disagrees.

An unsupported objection may trigger independent verification.

An unavailable evidence source may trigger a bounded retry or an alternative trusted source.

A stale authorization record may trigger a fresh policy evaluation.

A contested high-risk action may require human review.

The intended principle is:

**Reconsideration must depend on new or independently verified evidence, not merely on finding another agent willing to approve the request.**

### Component E — Trusted execution gateway

Before a protected action is executed, a gateway evaluates the relevant policy, evidence, and decision state.

The gateway does not accept an agent's unsupported claim of authorization as sufficient proof.

Where the required evidence remains unresolved, the gateway follows an explicit fail-closed or escalation policy.

This mechanism builds on established reference-monitor principles.

Its role is to enforce the protocol's decisions rather than independently constitute the paper's novelty.

---

# 8. Decision Protocol

For a proposed action \(a\), the protocol proceeds through the following states.

## State 1 — Proposed

An agent proposes an action.

The system constructs a canonical action record and identifies applicable constraints.

## State 2 — Evaluated

Available policy facts and evidence are checked.

The system records whether each required input was established, its value, and its freshness.

## State 3 — Approved, refused, or deferred

The system issues a decision based on the available evidence.

A verified negative authorization result produces a refusal.

Missing or stale evidence produces a deferral where appropriate.

## State 4 — Contested

An agent challenges a refusal or requests reconsideration.

The challenge must identify a relevant change, missing fact, conflicting evidence source, or potential evaluation error.

Merely repeating the request does not automatically reset the process.

## State 5 — Escalated

VetoNet attempts to resolve the dispute using a bounded escalation policy.

Possible operations include:

- Fetching fresh authoritative evidence.
- Checking an independent source.
- Comparing policy versions.
- Requesting a trusted reviewer.
- Re-evaluating a changed action context.
- Escalating to human authorization.

## State 6 — Finalized

The system records one of three outcomes:

**Executed:** The action was authorized and completed.

**Denied:** The action was not authorized under the applicable constraints.

**Unresolved:** The system could not establish sufficient evidence within the permitted budget or deadline.

The unresolved state is important.

A system should not manufacture certainty merely to produce a binary decision.

---

# 9. Theoretical Investigation

The theoretical contribution must go beyond presenting a software protocol.

We propose three formal investigations.

## 9.1 Impossibility under indistinguishable evidence

Consider two possible environment states:

- \(s_1\), in which an action is authorized.
- \(s_2\), in which the same action is unauthorized.

Suppose the controller receives identical observations in both states.

Then any controller operating only on those observations must use the same decision distribution in both cases.

It cannot simultaneously guarantee authorization-sensitive execution in both states with zero error.

This provides a basic information-theoretic limitation.

It demonstrates why no refusal protocol can guarantee perfect safety and perfect availability without sufficient information.

However, this observation is elementary.

**It would not independently constitute a NeurIPS-level theoretical contribution.**

The research challenge is to derive more informative bounds under realistic evidence-availability, corruption, and verification-cost assumptions.

## 9.2 Safety and availability under bounded adversarial control

We will investigate systems containing \(n\) agents, of which at most \(f\) may be compromised.

The aim is to characterize the conditions under which valid evidence can be recovered and unauthorized actions can be prevented.

Relevant assumptions include:

- Trusted versus untrusted evidence sources.
- Independence or correlation between evidence providers.
- Availability of authoritative records.
- Bounded communication delay.
- Verification budgets.
- Adversarial control of coordinator decisions.
- Ability to instantiate additional agents.

Classical Byzantine fault-tolerance results will serve as reference points.

We will not treat ordinary voting thresholds as a new theoretical discovery.

Instead, we will investigate how those guarantees change when participants supply uncertain natural-language judgments rather than independently verified binary facts.

A promising direction is deriving bounds on the reliability of escalation as a function of evidence quality and the degree of correlated failure.

## 9.3 Conditional protocol guarantees

We will attempt to establish formally specified properties such as:

**Authorization preservation:** A verified hard denial cannot be overridden by delegation alone.

**Decision lineage preservation:** Relevant prior decisions remain associated with equivalent actions.

**Evidence monotonicity under unchanged state:** Repeated unsupported assertions cannot increase authorization confidence without additional evidence.

**Bounded escalation:** Under defined availability assumptions, the protocol either resolves a dispute or returns an explicit unresolved outcome within a bounded resource budget.

**Adversarial veto containment:** Unsupported objections cannot indefinitely block all legitimate work when sufficient independent authoritative evidence is available.

Each claim requires explicit assumptions and proof.

We will distinguish invariants enforced directly by trusted software from probabilistic properties dependent on model behaviour.

A limited formal model could be implemented in TLA+ or another suitable verification framework.

The objective would be to discover protocol defects and establish conditional guarantees, not to claim that formal verification makes the underlying language models trustworthy.

---

# 10. VetoBench: A Benchmark for Safety and Availability

A conference-scale contribution requires a reusable evaluation environment.

We propose **VetoBench**, a benchmark that systematically evaluates multi-agent refusal mechanisms under both safety attacks and availability attacks.

## 10.1 Benchmark design principles

The benchmark should satisfy five requirements.

**Objective outcomes:** Whenever possible, success and failure are determined by environment state rather than solely by an LLM judge.

**Controlled uncertainty:** Agents receive incomplete or conflicting evidence while the evaluator retains ground truth.

**Adversarial participation:** Some agents or evidence sources may deliberately manipulate decisions.

**Legitimate functionality:** The system must complete authorized requests, not merely avoid harmful actions.

**Reproducibility:** Each episode has a defined initial state, permitted actions, attack configuration, and evaluation procedure.

## 10.2 Environment domains

We propose four initial domains.

### Domain A — Enterprise access management

Agents process requests involving fictional files, permissions, and internal records.

Tasks include granting access, modifying permissions, and revoking credentials.

Some requests are authorized, some are prohibited, and others depend on evidence that is unavailable or outdated.

This domain supports precise authorization rules.

### Domain B — Software deployment and release management

Agents collaborate on simulated software releases.

A deployment may require successful tests, code review, and approval from authorized personnel.

An agent might incorrectly report that a review was completed.

Another might refuse deployment because it cannot retrieve the latest test results.

The system must distinguish true deployment restrictions from incomplete information.

### Domain C — Financial operations

Agents process fictional invoices, refunds, and internal payment approvals.

The environment includes synthetic account records and authorization rules.

No actual financial transactions occur.

This domain is useful because authorization, delegated approval, and conflicting evidence are common in financial workflows.

### Domain D — Data access and research governance

Agents collaborate on accessing and processing fictional research datasets.

Some actions require consent, institutional approval, or additional verification.

Requests may involve legitimate access, invalid authorization, outdated approvals, or misleading descriptions of dataset restrictions.

This domain tests whether the proposed mechanism generalizes beyond simple financial or software actions.

## 10.3 Scenario categories

Each domain will include several scenario families.

**Family A — Clean authorization:** Legitimate requests supported by complete evidence.

**Family B — Clear prohibition:** Requests that violate known, authoritative constraints.

**Family C — Missing evidence:** Legitimate requests for which some required evidence is temporarily unavailable.

**Family D — Conflicting evidence:** Different sources provide incompatible information.

**Family E — Stale decisions:** Authorization status changes during the workflow.

**Family F — Refusal shopping:** A coordinator retries an action after receiving a justified refusal.

**Family G — Refusal poisoning:** A compromised agent attempts to prevent a legitimate action.

**Family H — Coordinated manipulation:** Several agents cooperate to influence the final decision.

**Family I — Semantic evasion:** Agents reformulate requests to evade previous refusals.

**Family J — Recovery:** New evidence becomes available after an initial refusal or deferral.

The benchmark should include both successful and unsuccessful attacks.

We must avoid designing every scenario around a weakness that VetoNet was specifically constructed to address.

## 10.4 Dataset scale

For an initial conference-scale evaluation, we propose approximately:

- Four domains.
- 200–300 base scenarios per domain.
- Around 1,000 base scenarios in total.
- Multiple controlled variations per scenario.
- Separate development and held-out evaluation partitions.
- Additional adaptive adversarial scenarios.

This would yield several thousand distinct evaluation configurations.

Repeated runs across different models, protocols, and random seeds could produce tens of thousands of episodes.

The final scale should be determined by statistical power, compute availability, and benchmark quality rather than by an arbitrary desire for a large number.

---

# 11. Experimental Baselines

A critical requirement is comparing VetoNet against strong alternatives.

We propose the following baselines.

## B1 — Independent decisions

Agents independently approve or refuse requests.

The coordinator can delegate to another worker after a refusal.

This establishes the vulnerability of unrestricted retries.

## B2 — Shared refusal memory

Every refusal is recorded and made visible to subsequent agents.

Agents are instructed to respect previous refusals.

This tests whether shared memory alone provides meaningful protection.

## B3 — Unconditional global veto

Any refusal prevents subsequent execution of the same action.

This provides a strong safety-oriented baseline with potentially poor availability.

## B4 — Majority voting

Several agents independently evaluate a request.

The majority decision determines whether the action proceeds, subject to any non-overridable trusted policy restrictions.

We will vary the number and diversity of reviewers.

## B5 — Trusted policy engine

Protected actions are evaluated using an external authorization engine.

When complete authoritative information is available, this baseline should perform extremely well.

When evidence is unavailable, the policy engine must follow an explicitly defined policy for unknown inputs.

This is one of the most important comparisons.

## B6 — Provenance-aware verification

The system preserves relevant source and authority metadata across delegation boundaries.

This baseline draws on existing provenance-auditing techniques.

## B7 — Independent reviewer

A separate model evaluates disputed actions without receiving the original agent's full argumentative rationale.

This tests whether independent review improves decisions.

## B8 — Human escalation

Disputed actions are referred to a human reviewer.

This baseline measures the trade-off between decision quality, latency, and human workload.

It must use a realistic review budget rather than assuming unlimited, instantaneous, perfectly accurate human judgment.

## B9 — Risk-threshold escalation

A simpler controller escalates requests according to predefined risk categories.

This tests whether a relatively ordinary risk-based policy can match VetoNet's performance.

## B10 — Oracle upper bound

An evaluator with access to the benchmark's hidden authorization ground truth produces the ideal outcome.

This is not a deployable baseline.

It provides a ceiling for interpreting empirical performance.

---

# 12. Main Experiments

## Experiment 1 — Characterizing refusal shopping

**Objective:** Quantify how repeated delegation affects unauthorized-action rates.

We vary:

- Number of workers.
- Number of permitted retries.
- Agent model.
- Network topology.
- Coordinator strategy.
- Availability of previous decisions.

We compare repeated attempts against one worker with attempts distributed across multiple workers.

This controls for whether additional failures arise from delegation specifically or simply from repeated stochastic sampling.

**Expected contribution:** A quantitative characterization of when local refusal behaviour fails to compose into system-level protection.

## Experiment 2 — Measuring adversarial veto power

**Objective:** Determine how compromised agents can obstruct legitimate work.

We introduce one or more agents capable of issuing unsupported refusals.

We measure legitimate completion as the proportion of compromised agents increases.

We compare independent decisions, shared refusal memory, unconditional vetoes, and VetoNet.

**Key question:** How much influence can one compromised agent obtain over the availability of the entire system?

## Experiment 3 — Safety–availability trade-off

**Objective:** Compare the principal mechanisms under matched workloads.

Each protocol receives the same distribution of authorized and unauthorized tasks.

We measure:

\[
(R_{\mathrm{unsafe}},R_{\mathrm{complete}})
\]

across different policies and operating thresholds.

We will construct a safety–availability frontier.

The central test is whether VetoNet provides better legitimate completion at comparable unauthorized-action rates.

The comparison must include confidence intervals and account for differences in verification cost.

## Experiment 4 — Evidence-quality degradation

**Objective:** Test sensitivity to incomplete and unreliable information.

We vary:

- Evidence availability.
- Evidence freshness.
- Source reliability.
- Contradiction rate.
- Number of independent sources.
- Adversarial evidence contamination.

This experiment is central to the research contribution.

If VetoNet performs well only when it receives essentially perfect evidence, its advantage over a conventional policy engine may be limited.

## Experiment 5 — Correlated agent failures

**Objective:** Understand whether additional agents provide genuinely independent verification.

We compare:

- Identical model instances.
- Different prompts using the same model.
- Different model families.
- Heterogeneous model ensembles.
- Agents sharing evidence sources.
- Agents using independently verified sources.

The goal is to separate diversity of model outputs from diversity of underlying evidence.

A large group of agents citing the same incorrect source should not automatically be treated as stronger evidence than one agent citing that source.

## Experiment 6 — Adaptive adversarial evaluation

**Objective:** Test whether attackers can adapt to the proposed protocol.

The attacker will be given knowledge of the defence architecture and a fixed budget for developing strategies.

Possible attack objectives include:

- Circumventing prior refusals.
- Causing false refusals.
- Exhausting verification budgets.
- Exploiting stale evidence.
- Manipulating action canonicalization.
- Creating misleading reviewer consensus.
- Causing unnecessary human escalations.

We will evaluate attacks on held-out scenarios.

It is important that the same adversarial effort is applied to competing protocols.

Otherwise, apparent robustness improvements could reflect unequal attack optimization rather than a better defence.

## Experiment 7 — Dynamic authorization

**Objective:** Evaluate requests whose authorization status changes over time.

Examples include:

- An approval being granted after an initial refusal.
- A previously valid permission being revoked.
- A policy version changing.
- A temporary authorization expiring.
- A required reviewer becoming unavailable.

This experiment tests whether the refusal protocol can recover legitimate work without relying on stale positive evidence.

## Experiment 8 — Realistic workflow transfer

**Objective:** Determine whether results from controlled synthetic environments transfer to more realistic agent workflows.

We will adapt selected tasks from existing agent evaluation frameworks where their licenses and interfaces permit.

The transfer evaluation should include realistic tool interactions and multi-step dependencies.

The goal is to establish whether the identified failures remain observable outside the purpose-built benchmark.

---

# 13. Evaluation Metrics

## 13.1 Primary safety metrics

**Unauthorized Action Rate (UAR):**

The fraction of unauthorized requests that result in prohibited actions.

**Attack Success Rate (ASR):**

The fraction of adversarial episodes in which the attacker achieves the defined objective.

**Severity-Weighted Violation Rate:**

A measure accounting for the differing consequences of policy violations.

## 13.2 Primary availability metrics

**Legitimate Completion Rate (LCR):**

The fraction of authorized tasks completed successfully.

**False Refusal Rate (FRR):**

The fraction of authorized requests incorrectly blocked.

**Recovery Success Rate (RSR):**

The fraction of initially blocked legitimate requests correctly recovered after additional evidence becomes available.

## 13.3 Protocol metrics

**Verification Cost:** Additional inference, external queries, or human reviews.

**Decision Latency:** Time required to approve, refuse, or resolve a request.

**Escalation Rate:** Proportion of episodes requiring additional verification.

**Unresolved Rate:** Proportion of cases remaining undecidable within the specified budget.

**Provenance Integrity:** Frequency with which relevant decision and evidence lineage remains correctly preserved.

**Canonicalization Error:** Frequency of incorrectly merged or incorrectly separated actions.

## 13.4 Robustness metrics

We will measure performance as a function of:

\[
f/n
\]

where \(f\) is the number of compromised agents and \(n\) is the total number of agents.

We will also examine sensitivity to communication structure, evidence degradation, and model heterogeneity.

---

# 14. Experimental Methodology

## 14.1 Model selection

The study should include models from at least three different model families.

Ideally, the evaluation will contain:

- A small open-weight model.
- A medium-sized open-weight model.
- A stronger instruction-following model.
- At least one hosted frontier model.

We will select concrete model versions at experiment time and record their exact identifiers.

The benchmark should not be optimized exclusively for one model.

## 14.2 Experimental controls

Across protocols, we will hold constant:

- Task definitions.
- Initial environment states.
- Policy documents.
- Available tools.
- Model versions.
- Decoding settings.
- Maximum interaction budgets.
- Attacker capabilities.
- Ground-truth evaluation rules.

Where possible, matched scenarios will use common random seeds.

We will avoid attributing behavioural differences to the control protocol when they could arise from unrelated changes in prompts or inference infrastructure.

## 14.3 Data generation and validation

Synthetic scenarios will be generated using explicit state machines and parameterized task templates.

The simulator will produce:

1. Initial state.
2. Authorization ground truth.
3. Agent-visible observations.
4. Evidence-source states.
5. Attack configuration.
6. Expected permissible outcomes.

Ground truth will be determined programmatically wherever possible.

A subset of scenarios will receive independent human review.

The benchmark must include genuinely ambiguous cases, but ambiguous evidence should not imply ambiguous evaluation labels.

The benchmark evaluator must know whether the action is authorized in the underlying simulated world.

## 14.4 Statistical analysis

The primary statistical analysis will compare matched protocol outcomes.

We will report:

- Absolute differences in UAR and LCR.
- Confidence intervals.
- Cluster-aware bootstrap estimates.
- Variation across model families.
- Variation across domains.
- Interaction effects between protocol and adversarial conditions.

We may use hierarchical logistic regression to account for differences across tasks, domains, and model instances.

The main hypotheses and evaluation metrics should be preregistered before final benchmark testing.

Exploratory analyses will be reported separately.

## 14.5 Statistical power

Before scaling experiments, we will estimate baseline rates and episode-level variance.

We will then perform a power analysis for the smallest practically meaningful difference in unsafe execution and legitimate completion.

This determines whether the study needs hundreds or thousands of independent scenario instances.

Repeated stochastic runs of one task do not provide the same evidence as independent tasks.

The analysis must account for this dependence.

---

# 15. Ablation Studies

A NeurIPS-level submission should identify which components are responsible for observed improvements.

We propose removing or modifying one mechanism at a time.

| Ablation | Research question |
|---|---|
| Without action canonicalization | Does semantic reformulation enable refusal bypass? |
| Without evidence provenance | How much does source attribution contribute? |
| Without refusal persistence | Does delegation recover the original vulnerability? |
| Without independent verification | Are improvements caused by reviewer diversity or by authoritative evidence? |
| Without decision expiry | Do stale refusals unnecessarily block legitimate work? |
| Without bounded escalation | Can attackers exhaust system resources? |
| Without authenticated identity | How vulnerable is the protocol to identity manipulation? |
| Without structured decision states | Does collapsing refusal and uncertainty degrade outcomes? |
| Without adaptive review | Can a fixed escalation policy perform equally well? |
| Without human escalation | Which cases remain unresolved? |

A key ablation is the removal of independent evidence verification.

If VetoNet retains most of its measured advantage without that mechanism, our explanation of why it works would need reconsideration.

Conversely, if a simple independent verification step performs just as well as the entire proposed architecture, that would weaken the justification for the additional complexity.

---

# 16. Expected Contributions

The research aims to produce four principal contributions.

## Contribution 1 — A formal account of refusal composition

We aim to define when agent-level safety decisions are preserved, lost, or incorrectly propagated across delegation.

This includes distinguishing authorized action, verified refusal, uncertainty, and adversarial obstruction.

## Contribution 2 — A characterization of the safety–availability frontier

We aim to quantify how refusal-handling protocols trade unauthorized execution against legitimate task completion.

The goal is to identify systematic patterns rather than merely report whether one attack succeeded.

## Contribution 3 — Evidence-bound escalation

We propose a mechanism that preserves decision lineage while permitting constrained, evidence-supported reconsideration.

Its success will depend on whether it achieves measurable improvements over strong authorization and verification baselines.

## Contribution 4 — VetoBench

We aim to release a reproducible benchmark containing realistic multi-agent scenarios, structured authorization ground truth, adversarial configurations, and evaluation metrics.

A high-quality benchmark may be valuable independently of the proposed defence.

If the protocol fails but the benchmark reveals a previously undercharacterized problem, that could still support a useful research contribution.

---

# 17. What Would Constitute a Strong Result?

We should define success before observing the experimental outcomes.

A convincing result would have several characteristics.

**First**, the study demonstrates a meaningful safety–availability failure across multiple model families and workflow domains.

**Second**, the failure persists under realistic baselines rather than appearing only in a deliberately weak prompt-only system.

**Third**, the proposed protocol improves legitimate completion while maintaining comparable or better safety.

**Fourth**, the advantage persists under adaptive attacks and held-out scenarios.

**Fifth**, ablations support the mechanism we claim is responsible for the improvement.

**Sixth**, any theoretical results provide useful explanatory or predictive value beyond restating familiar authorization principles.

We should not set an arbitrary percentage improvement as a promise.

The actual contribution depends on experimental evidence.

---

# 18. Compute and Infrastructure Requirements

Unlike the hackathon version, a conference-scale investigation will require substantial evaluation compute.

We do not expect large-scale model training to be necessary.

The main costs will come from repeated inference, multi-agent interaction, adversarial testing, and benchmark validation.

## 18.1 Experimental infrastructure

The proposed stack is:

**Agent runtime:** Python-based multi-agent orchestration.

**Model serving:** vLLM or another suitable inference runtime for open-weight models.

**Policy evaluation:** Cedar or an equivalent established authorization engine.

**Decision storage:** PostgreSQL or another transactional database.

**Experiment tracking:** Structured logs and reproducible configuration files.

**Statistical analysis:** Python, SciPy, and appropriate statistical-modeling libraries.

**Formal verification:** TLA+ or a comparable model-checking system.

## 18.2 Compute strategy

Development should proceed in stages.

**Stage 1:** Small local models and deterministic simulations.

**Stage 2:** Open-weight model evaluation on rented GPUs.

**Stage 3:** Selected frontier-model comparisons using hosted inference.

**Stage 4:** Adaptive adversarial testing on held-out scenarios.

This reduces unnecessary experimentation before the evaluation framework is validated.

The full experiment budget cannot be estimated reliably until we know the average number of model calls per episode, token consumption, and selected model families.

A large benchmark with tens of thousands of multi-agent episodes could require significant GPU time or API expenditure.

The final plan should therefore include inference caching, batched evaluation where appropriate, and a strict accounting of experimental costs.

---

# 19. Reproducibility and Open Science

We intend to release:

- Benchmark generation code.
- Synthetic task definitions.
- Policy configurations.
- Evaluation harnesses.
- Protocol implementations.
- Non-sensitive experiment logs.
- Statistical analysis scripts.
- Model and runtime configurations.
- Formal specifications.
- Documentation and reproduction instructions.

Every reported result should be traceable to a specific experiment configuration and software revision.

We will distinguish the intended protocol from its actual implementation.

If certain components require unavailable proprietary models or external services, we will identify those limitations and provide open alternatives where possible.

---

# 20. Research Risks and Failure Conditions

## Risk 1 — The proposed mechanism duplicates existing authorization systems

This is the largest novelty risk.

If VetoNet is essentially a policy engine with additional logging, it is not a strong research contribution.

**Mitigation:** Focus on incomplete information, adversarial evidence, bounded escalation, and the empirical frontier between safety and availability.

## Risk 2 — The benchmark is too synthetic

A mechanism may succeed only because the benchmark was designed around it.

**Mitigation:** Include external benchmark adaptations, independently developed attacks, and held-out task families.

## Risk 3 — A conventional policy engine solves the problem

If every scenario can be resolved through a simple authoritative policy lookup, the proposed mechanism may be unnecessary.

**Mitigation:** Explicitly separate complete-information scenarios from incomplete-evidence scenarios. Treat policy engines as strong baselines, not weak competitors.

## Risk 4 — Theoretical results are trivial

An elementary indistinguishability observation or a restatement of classical Byzantine agreement would not justify a major theoretical claim.

**Mitigation:** Develop the analysis around evidence cost, uncertainty, correlated agent judgments, and operational escalation constraints.

## Risk 5 — Human review dominates all automated methods

A high-quality human reviewer may outperform automated escalation.

**Mitigation:** Compare performance under realistic latency and review budgets. The research should identify when automation is useful rather than assume it always is.

## Risk 6 — Safety improvements result from excessive refusal

A system can achieve very low violation rates by refusing every action.

**Mitigation:** Always measure legitimate completion, false refusals, and unresolved cases alongside safety.

## Risk 7 — Adaptive attacks defeat the protocol

An attacker who knows the protocol may learn to manipulate its escalation rules.

**Mitigation:** Include adaptive adversaries and evaluate attack transfer across held-out models and scenarios.

## Risk 8 — The research produces negative results

VetoNet may not outperform simpler approaches.

This possibility must be accepted.

A rigorous characterization of when simpler approaches are sufficient—and when more complicated mechanisms provide no advantage—could itself be valuable.

---

# 21. Ethics and Dual-Use Considerations

This research investigates attacks against collaborative AI systems.

Some techniques may also inform efforts to manipulate operational safeguards.

We will therefore conduct experiments in controlled environments containing synthetic data and simulated actions.

The benchmark will not execute unauthorized operations against real services.

We will avoid publishing operational attack artifacts that would unnecessarily facilitate misuse against deployed systems.

The primary emphasis will be on failure characterization, defence evaluation, and secure protocol design.

We will disclose that formal guarantees depend on trust assumptions and do not imply universal safety for arbitrary language-model systems.

We will also evaluate availability failures because overly restrictive automation can have substantial practical consequences for legitimate users.

---

# 22. Publication Strategy

## 22.1 Primary target

**NeurIPS Main Conference**

The strongest NeurIPS version would combine:

1. A clearly identified and important failure mode.
2. A formal account of the safety–availability problem.
3. An original evidence-bound control mechanism.
4. Broad experimental evaluation.
5. Strong comparisons against existing methods.
6. An openly reproducible benchmark.

A benchmark-only contribution could alternatively be considered for an appropriate datasets-and-benchmarks venue, subject to that venue's current submission structure.

## 22.2 Alternative venues

**ICLR:** Appropriate if the strongest contribution concerns generalizable behaviour of language-model agents and their coordination.

**ICML:** Appropriate if the work develops substantial theory or new machine-learning methodology.

**USENIX Security, ACM CCS, or NDSS:** Potentially more appropriate if the main contribution is an attack model, security protocol, and rigorous systems evaluation.

We should select the final venue based on the contribution actually established.

## 22.3 Possible final paper titles

**Preferred:**

*The Veto Paradox: Safety and Liveness in Multi-Agent Language Model Systems*

**Alternative:**

*When Safety Becomes Denial of Service: Evidence-Bound Refusals in Multi-Agent Systems*

**Method-focused:**

*VetoNet: Evidence-Bound Escalation for Safe and Available Multi-Agent Systems*

**Theory-focused:**

*On the Compositionality of Safety Decisions in Multi-Agent Language Model Systems*

The title should ultimately reflect the strongest verified result, not merely the most ambitious original hypothesis.

---

# 23. Research Roadmap

## Phase I — Problem validation

**Suggested duration: 2 weeks**

Objectives:

- Complete the focused literature review.
- Formalize the threat model.
- Implement independent decisions and unconditional veto baselines.
- Construct initial benchmark scenarios.
- Establish that the proposed failure modes occur under realistic conditions.

**Deliverable:** A validated problem formulation and preliminary experimental results.

**Decision gate:** If strong existing baselines already eliminate the relevant failures, revise the research question before proceeding.

## Phase II — Protocol development

**Suggested duration: 3–4 weeks**

Objectives:

- Specify evidence-bound refusal records.
- Implement decision lineage.
- Develop the escalation protocol.
- Integrate an established authorization engine.
- Construct a formal state-machine model.
- Identify candidate theoretical properties.

**Deliverable:** A working VetoNet implementation with initial correctness tests.

## Phase III — Benchmark construction

**Suggested duration: 4 weeks**

Objectives:

- Build the four benchmark domains.
- Generate diverse scenarios.
- Validate authorization ground truth.
- Develop adversarial configurations.
- Construct held-out evaluation splits.
- Conduct independent quality review.

**Deliverable:** VetoBench evaluation suite.

## Phase IV — Large-scale experimentation

**Suggested duration: 3–4 weeks**

Objectives:

- Run model-family comparisons.
- Evaluate the principal baselines.
- Measure safety–availability frontiers.
- Conduct adaptive attack evaluations.
- Run ablations.
- Estimate confidence intervals.
- Analyze generalization failures.

**Deliverable:** Complete experimental results and reproducible analysis.

## Phase V — Theory, synthesis, and publication

**Suggested duration: 2–3 weeks**

Objectives:

- Complete proofs or counterexamples.
- Connect theoretical predictions with empirical findings.
- Refine the paper's central contribution.
- Prepare the main paper and appendix.
- Perform independent internal review.
- Release reproducibility artifacts.

**Deliverable:** Conference submission package.

The full programme would likely require approximately **three to four months of concentrated research**, depending on compute availability, benchmark complexity, and the number of researchers involved.

---

# 24. Minimum Publishable Contribution

The complete research programme is ambitious.

We should distinguish essential contributions from extensions.

The minimum credible main-conference submission would require:

**A. A rigorously established problem**

Demonstrate that existing refusal-handling mechanisms suffer a measurable safety–availability trade-off under realistic multi-agent conditions.

**B. A technically justified intervention**

Introduce an evidence-bound escalation mechanism that differs substantively from conventional authorization or majority voting.

**C. Strong empirical results**

Show improvements over credible baselines across multiple models and domains, with adversarial evaluation and ablations.

**D. A reusable evaluation artifact**

Release a benchmark that allows other researchers to investigate the problem independently.

The theoretical component could strengthen the paper significantly, but weak or trivial formal claims should not be included merely to make the contribution appear more sophisticated.

---

# 25. Research Success Criteria

We consider the research successful if it establishes at least one substantial finding.

### Finding A — A previously undercharacterized failure

We demonstrate that propagating safety decisions introduces a distinct, measurable class of multi-agent availability failures not adequately handled by conventional mechanisms.

### Finding B — A generalizable control mechanism

We develop a protocol that improves the safety–availability trade-off across multiple realistic settings.

### Finding C — A theoretical characterization

We establish meaningful limitations or sufficient conditions for safety and legitimate progress under partial information and adversarial participation.

### Finding D — A benchmark contribution

We produce a validated, reusable evaluation framework that reveals important weaknesses in existing agent-control approaches.

The ideal paper would establish all four.

However, the final contribution should be determined by what the investigation actually demonstrates.

---

# 26. Final Research Thesis

The central thesis of this project is:

**Safety in multi-agent AI systems cannot be understood solely as the collection of safety properties possessed by individual agents. It also depends on how decisions are propagated, challenged, verified, and enforced across the network.**

Unrestricted delegation may undermine valid refusals.

Unconditional refusal propagation may enable adversarial obstruction.

Voting may amplify correlated mistakes.

Provenance may authenticate an incorrect judgment.

External authorization may enforce known rules while leaving unresolved questions about incomplete or unreliable evidence.

We therefore propose studying safety decisions as structured, evidence-dependent objects whose validity must be preserved across delegation without granting arbitrary agents unconditional control over the entire system.

VetoNet is our proposed mechanism for investigating this problem.

VetoBench is our proposed experimental infrastructure.

The theoretical objective is to characterize when safety and progress can coexist under partial information and adversarial participation.

The empirical objective is to determine whether evidence-bound escalation provides a meaningful advantage over established alternatives.

**The ultimate contribution would be a principled framework for building multi-agent AI systems that can resist both unauthorized cooperation and malicious obstruction, without assuming that every participating agent is trustworthy.**

---

# 27. Foundational References

The initial literature review should include the following works:

1. **Ying et al. (2026).** *Delegated Misalignment: How Multi-Agent Structures Amplify LLM Safety Risks.* EMNLP 2026.

2. **Zhou et al. (2026).** *Trust Cascade through Provenance Erasure: How Multi-Agent Delegation Breaks Single-Agent Safety.* EMNLP 2026.

3. **Maliha et al. (2026).** *ATC: Agent Trajectory Control for Role-Contract Enforcement in Black-Box Multi-Agent Systems.* EMNLP 2026.

4. **Greenblatt et al. (2024).** *AI Control: Improving Safety Despite Intentional Subversion.* ICML 2024.

5. **Motwani et al. (2024).** *Secret Collusion among AI Agents: Multi-Agent Deception via Steganography.* NeurIPS 2024.

6. **Debenedetti et al. (2024).** *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* NeurIPS 2024.

7. **Zhu et al. (2025).** *MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents.* ACL 2025.

8. **Yao et al. (2025).** *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* ICLR 2025.

9. **Andriushchenko et al. (2025).** *AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents.* ICLR 2025.

10. **Cutler et al. (2024).** *Cedar: A New Language for Expressive, Fast, Safe, and Analyzable Authorization.*

11. **Fischer, Lynch, and Paterson (1985).** *Impossibility of Distributed Consensus with One Faulty Process.* Journal of the ACM.

12. **Pease, Shostak, and Lamport (1980).** *Reaching Agreement in the Presence of Faults.* Journal of the ACM.

13. **Konda (2026).** *Preserving Evaluation State in Agent Protocol Decisions.* IETF Internet-Draft, work in progress.

These references establish the relevant foundations in multi-agent safety, AI control, provenance, authorization, distributed consensus, and agent evaluation.

The next literature review should specifically investigate recent work on evidence-dependent authorization, adversarial consensus, selective prediction, human escalation, and the propagation of uncertain decisions across distributed workflows.

---

**End of research proposal.**