"""Budget-constrained allocation on public request metadata, never ground truth."""
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class Candidate:
    case_id: str
    risk: float
    uncertainty: float
    source_reliability: float
    cost: int
    arrival: int


def allocate(candidates: list[Candidate], budget: int, strategy: str, seed: int = 0) -> list[str]:
    if budget < 0 or any(x.cost <= 0 for x in candidates):
        raise ValueError('budget must be nonnegative and costs positive')
    if len({c.case_id for c in candidates}) != len(candidates):
        raise ValueError('candidate IDs must be unique')
    if strategy == 'fifo':
        ordered=sorted(candidates,key=lambda x:(x.arrival,x.case_id))
    elif strategy == 'random':
        ordered=sorted(candidates,key=lambda x:x.case_id)
        random.Random(seed).shuffle(ordered)
    elif strategy == 'risk':
        ordered=sorted(candidates,key=lambda x:(-x.risk,x.arrival,x.case_id))
    elif strategy == 'evidence_aware':
        # A prespecified heuristic, not learned or claimed optimal. Reliability
        # is source metadata available before the costly lookup, not its answer.
        ordered=sorted(candidates,key=lambda x:(-(x.uncertainty*x.source_reliability/x.cost),x.arrival,x.case_id))
    else:
        raise ValueError(strategy)
    chosen=[]
    for candidate in ordered:
        if candidate.cost <= budget:
            chosen.append(candidate.case_id); budget-=candidate.cost
    return chosen
