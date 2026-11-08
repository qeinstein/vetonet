"""Budget coordinator sees only public cases and query results, never world truth."""
from vetobench.allocation import Candidate, allocate
from vetobench.evidence_service import Request, monitor
from vetobench.parsing import parse
from vetobench.protocols import Decision


def coordinate(cases, service, budget, strategy, attack_rate=0.0, seed=0):
    if not 0 <= attack_rate <= 1:raise ValueError('invalid attack rate')
    allowed_keys={'id','principal','resource','operation','state_version','risk','cost','source_reliability','compromised_draw','request','worker','critic'}
    if any(set(c)-allowed_keys for c in cases):raise ValueError('unexpected or private case fields')
    if len({c['id'] for c in cases})!=len(cases):raise ValueError('duplicate IDs')
    candidates=[]
    for i,c in enumerate(cases):
        worker=parse(c['worker'],'anchored');critic=parse(c['critic'],'anchored')
        objection=critic==Decision.REFUSE or c['compromised_draw']<attack_rate
        uncertainty=1.0 if objection or worker!=critic else .25
        candidates.append(Candidate(c['id'],c['risk'],uncertainty,c['source_reliability'],c['cost'],i))
    chosen=set(allocate(candidates,budget,strategy,seed))
    results=[]
    for c in cases:
        record=service.lookup(c['id']) if c['id'] in chosen else None
        request=Request(c['principal'],c['resource'],c['operation'],c['state_version'])
        results.append({'id':c['id'],'queried':c['id'] in chosen,'executed':monitor(request,record,{'registry'})})
    return results
