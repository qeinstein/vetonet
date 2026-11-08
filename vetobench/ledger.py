"""A small in-memory model of scoped evidence; not a production reference monitor."""
from dataclasses import dataclass
from enum import Enum

class Verdict(str, Enum):
    ALLOW = 'allow'
    DENY = 'deny'
    UNKNOWN = 'unknown'

@dataclass(frozen=True)
class Action:
    principal: str
    operation: str
    resource: str
    policy_version: int
    state_version: int

@dataclass(frozen=True)
class Record:
    action: Action
    source: str
    verdict: Verdict
    expires_at: int


def evaluate(action: Action, records: list[Record], trusted_sources: set[str], now: int) -> Verdict:
    """Only current, in-scope trusted evidence can establish a decision.

    Conflict and missing evidence both return UNKNOWN, which a caller must not
    execute. Source trust is assumed by this model; it does not authenticate
    signatures or establish that source assertions are correct.
    """
    verdicts = {r.verdict for r in records if r.action == action and r.source in trusted_sources
                and now < r.expires_at and r.verdict != Verdict.UNKNOWN}
    if verdicts == {Verdict.ALLOW}:
        return Verdict.ALLOW
    if verdicts == {Verdict.DENY}:
        return Verdict.DENY
    return Verdict.UNKNOWN
