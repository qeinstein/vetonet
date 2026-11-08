"""Simulated external grants, with separate world truth and observed evidence.

This models an external registry; tokens and versions are simulated and do not
provide actual authentication or atomicity.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    principal: str
    resource: str
    operation: str
    state_version: int

@dataclass(frozen=True)
class GrantRecord:
    principal: str
    resource: str
    operation: str
    state_version: int
    allowed: bool
    issuer: str

class EvidenceService:
    def __init__(self, records: dict[str, GrantRecord], unavailable: set[str]):
        self._records=records
        self._unavailable=unavailable
    def lookup(self, case_id: str) -> GrantRecord | None:
        if case_id in self._unavailable:return None
        return self._records.get(case_id)

def monitor(request: Request, record: GrantRecord | None, trusted_issuers: set[str]) -> bool:
    if record is None or record.issuer not in trusted_issuers:return False
    return (record.principal,record.resource,record.operation,record.state_version)==(request.principal,request.resource,request.operation,request.state_version) and record.allowed
