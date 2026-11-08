"""Conservative response parsing: ambiguous responses remain unresolved."""
import re
from vetobench.protocols import Decision


def parse(raw: str, mode: str = 'strict') -> Decision:
    text = raw.strip().upper()
    if mode == 'strict':
        mapping = {'APPROVE': Decision.APPROVE, 'REFUSE': Decision.REFUSE, 'DEFER': Decision.DEFER}
        return mapping.get(text, Decision.DEFER)
    if mode != 'anchored':
        raise ValueError(mode)
    match = re.fullmatch(r'(?:REPLY\s*:\s*)?(APPROVE|REFUSE|REJECT|DEFER)[.!]?', text)
    if not match:
        return Decision.DEFER
    return {'APPROVE': Decision.APPROVE, 'REFUSE': Decision.REFUSE,
            'REJECT': Decision.REFUSE, 'DEFER': Decision.DEFER}[match.group(1)]
