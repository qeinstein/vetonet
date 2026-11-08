"""Paired synthetic stress test of objection propagation and evidence availability.

No LLM is called here. Evidence availability and adversarial objections are
experimenter-controlled; correct evidence is a favorable trust assumption.
"""
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vetobench.ledger import Action, Record, Verdict, evaluate
from vetobench.parsing import parse
from vetobench.protocols import Decision, Evidence, execute

p = argparse.ArgumentParser()
p.add_argument('input')
p.add_argument('--output', required=True)
a = p.parse_args()
data = json.loads(Path(a.input).read_text())
rows = data['scenarios']
assert len(rows) == 160 and len({r['id'] for r in rows}) == 160
out = []
for coverage in (0.0, 0.5, 1.0):
    for attack in (False, True):
        counts = Counter()
        for r in rows:
            # Hash makes evidence availability deterministic and paired across
            # interventions and coverage levels, independent of scenario order.
            u = int.from_bytes(hashlib.sha256(('evidence-2026-' + r['id']).encode()).digest()[:8], 'big') / 2**64
            available = u < coverage
            truth = r['authorized']
            votes = [parse(x) for x in r['raw']]
            if attack:
                votes.append(Decision.REFUSE)
            action = Action('requester', 'modify', r['id'], 1, 1)
            records = [Record(action, 'worker', Verdict.DENY, 10)] if attack else []
            if available:
                records.append(Record(action, 'registry', Verdict.ALLOW if truth else Verdict.DENY, 10))
            evidence = Evidence(truth if available else None, available)
            decisions = {
                'first': execute('first', votes, evidence),
                'retry': execute('retry', votes, evidence),
                'veto': execute('veto', votes, evidence),
                'equal_info_gate': execute('evidence_gate', votes, evidence),
                'scoped_ledger': evaluate(action, records, {'registry'}, 0) == Verdict.ALLOW,
            }
            for name, result in decisions.items():
                counts[(name, truth, result)] += 1
        for name in decisions:
            out.append({'coverage':coverage, 'false_objection':attack, 'protocol':name,
                        'unauthorized_executed':counts[(name,False,True)],
                        'unauthorized_n':sum(counts[(name,False,x)] for x in (False,True)),
                        'authorized_completed':counts[(name,True,True)],
                        'authorized_n':sum(counts[(name,True,x)] for x in (False,True))})
result = {'input':a.input, 'input_sha256':hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),
          'assumptions':'Synthetic replay; trusted evidence, when available, equals ground truth; no source corruption or interaction.', 'results':out}
Path(a.output).write_text(json.dumps(result, indent=2)+'\n')
for row in out: print(row)
