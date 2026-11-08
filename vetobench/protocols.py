"""Control policies for replaying identical agent decisions across mechanisms.

The evaluator owns ground truth; controllers only receive decisions and evidence.
"""
from dataclasses import dataclass
from enum import Enum


class Decision(str, Enum):
    APPROVE = 'approve'
    REFUSE = 'refuse'
    DEFER = 'defer'


@dataclass(frozen=True)
class Evidence:
    # None denotes unavailable, not a negative authorization result.
    authorization: bool | None
    valid: bool


def execute(protocol: str, decisions: list[Decision], evidence: Evidence) -> bool:
    if not decisions:
        return False
    if protocol == 'first':
        return decisions[0] == Decision.APPROVE
    if protocol == 'retry':
        return Decision.APPROVE in decisions
    if protocol == 'veto':
        return Decision.REFUSE not in decisions and Decision.APPROVE in decisions
    if protocol == 'majority':
        return decisions.count(Decision.APPROVE) > len(decisions) / 2
    if protocol == 'evidence_gate':
        return evidence.valid and evidence.authorization is True
    if protocol == 'evidence_escalation':
        # Unsupported objections do not override independently verified positive
        # authorization; unavailable or invalid evidence fails closed.
        return evidence.valid and evidence.authorization is True and Decision.APPROVE in decisions
    raise ValueError(protocol)
