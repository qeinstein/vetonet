"""Queue model for duplicate and distinct-target verification requests.

Simulation only: a trusted canonicalizer and stable policy/state versions are
assumptions, not implemented security guarantees.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Job:
    job_id: str
    action_key: str
    cost: int
    legitimate: bool


def serve(jobs: list[Job], budget: int, deduplicate: bool) -> dict:
    if budget < 0 or any(j.cost <= 0 for j in jobs):
        raise ValueError('invalid budget or cost')
    # Shared action keys must refer to the same retrieval and cost.
    costs={}
    for j in jobs:
        if j.action_key in costs and costs[j.action_key]!=j.cost:
            raise ValueError('conflicting costs for one action key')
        costs[j.action_key]=j.cost
    seen=set(); spent=0; served=[]; cache_hits=0
    for job in jobs:
        if deduplicate and job.action_key in seen:
            cache_hits+=1; served.append(job.job_id)
        elif job.cost <= budget-spent:
            spent+=job.cost; seen.add(job.action_key); served.append(job.job_id)
    return {'served':served,'spent':spent,'cache_hits':cache_hits}
