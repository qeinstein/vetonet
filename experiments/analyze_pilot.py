"""Summarize pilot outcomes; deterministic, fail closed on unknown outputs."""
import collections, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vetobench.protocols import Decision, Evidence, execute
from vetobench.parsing import parse

p = Path(sys.argv[1] if len(sys.argv) > 1 else 'results/qwen25_3b_pilot.json')
data = json.loads(p.read_text())
mode = sys.argv[2] if len(sys.argv) > 2 else 'strict'
rows = data['scenarios']
protocols = ['first', 'retry', 'veto', 'majority', 'evidence_gate', 'evidence_escalation']
print(f"model={data['model']} seed={data['seed']} n={len(rows)} elapsed={data['elapsed_seconds']:.2f}s")
print('Unique ordered templates:', len({(r['role'], tuple(r['allowed']), r['resource']) for r in rows}))
unknown = 0
for r in rows:
    r['parsed'] = []
    for raw in r['raw']:
        value = parse(raw, mode)
        if value == Decision.DEFER and raw.strip().lower() != 'defer':
            unknown += 1
        r['parsed'].append(value)
print('Parser:', mode, 'unresolved outputs:', unknown)
print('protocol,unauthorized_executed,unauthorized_n,authorized_completed,authorized_n')
for protocol in protocols:
    counts = collections.Counter()
    for r in rows:
        # Pilot provides complete, correct evidence, so this is an oracle-information
        # comparison, not evidence of deployable verification performance.
        evidence = Evidence(r['authorized'], True)
        outcome = execute(protocol, r['parsed'], evidence)
        counts[(r['authorized'], outcome)] += 1
    print(f"{protocol},{counts[(False, True)]},{sum(counts[(False,x)] for x in (False,True))},{counts[(True, True)]},{sum(counts[(True,x)] for x in (False,True))}")
