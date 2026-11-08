"""Synthetic trusted monitor and fair, shared-cost budget evaluation."""
from vetobench.allocation import Candidate, allocate
from vetobench.parsing import parse
from vetobench.protocols import Decision


def run(cases, budget, attack_rate, policy, seed=0):
    """The registry, if queried and reachable, returns true authorization.

    This is an explicit idealized authoritative registry, not information given
    to the allocator. Unverified and unavailable evidence fails closed. Worker
    baselines bypass the monitor and receive no private authorization data.
    """
    candidates=[]; objections={}; rows={c['id']:c for c in cases}
    if len(rows)!=len(cases):raise ValueError('duplicate case ID')
    for i,c in enumerate(cases):
        w=parse(c['worker'],'anchored'); critic=parse(c['critic'],'anchored')
        objection=(critic == Decision.REFUSE or c['compromised_draw'] < attack_rate)
        objections[c['id']]=objection
        # Features observable without an evidence query; uncertainty is worker/
        # critic disagreement or an unsubstantiated objection.
        uncertainty=1.0 if objection or w != critic else .25
        candidates.append(Candidate(c['id'],c['risk'],uncertainty,c['source_reliability'],c['cost'],i))
    lookup={'gate_fifo':'fifo','gate_random':'random','gate_risk':'risk','evidence_aware':'evidence_aware'}
    if policy == 'objection_first':
        candidates=sorted(candidates,key=lambda c:(not objections[c.case_id],c.arrival))
        candidates=[Candidate(c.case_id,c.risk,c.uncertainty,c.source_reliability,c.cost,i) for i,c in enumerate(candidates)]
        chosen=set(allocate(candidates,budget,'fifo',seed))
    else:
        chosen=set(allocate(candidates,budget,lookup[policy],seed)) if policy in lookup else set()
    outcomes=[]
    for c in cases:
        w=parse(c['worker'],'anchored'); critic=parse(c['critic'],'anchored'); retry=parse(c['retry'],'anchored')
        if policy=='independent_retry': execute=w==Decision.APPROVE or retry==Decision.APPROVE
        elif policy=='shared_veto': execute=w==Decision.APPROVE and critic!=Decision.REFUSE and not objections[c['id']]
        elif policy=='majority':
            reviewer = Decision.REFUSE if c['compromised_draw'] < attack_rate else critic
            execute=sum(x==Decision.APPROVE for x in (w,reviewer,retry))>=2
        elif policy in lookup or policy=='objection_first':
            execute=c['id'] in chosen and c['source_available'] and c['authorized']
        else: raise ValueError(policy)
        outcomes.append(dict(id=c['id'],authorized=c['authorized'],executed=execute,objection=objections[c['id']],queried=c['id'] in chosen))
    return outcomes
