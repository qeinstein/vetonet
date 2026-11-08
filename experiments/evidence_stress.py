"""Counterfactual evidence corruption and staleness stress test.

Synthetic ground truth and source failures are controlled by the evaluator.
These are mechanism checks, not empirical estimates of infrastructure reliability.
"""
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vetobench.ledger import Action, Record, Verdict, evaluate

p = argparse.ArgumentParser()
p.add_argument('--output', default='results/evidence_stress.json')
a = p.parse_args()
N = 1000

def draw(i, stream):
    return int.from_bytes(hashlib.sha256(f'{stream}:{i}'.encode()).digest()[:8], 'big') / 2**64

out = []
for available_rate in (0.25, 0.5, 1.0):
    for corruption_rate in (0.0, 0.05, 0.2):
        for stale_mode in ('fresh', 'detected', 'undetected'):
            counts = Counter()
            for i in range(N):
                truth = bool(i % 2)
                available = draw(i,'available') < available_rate
                corrupt = draw(i,'corrupt') < corruption_rate
                action = Action('principal', 'write', f'resource-{i}', 1, 2)
                # An obsolete record reverses current authorization. Detection
                # represents a state version mismatch at the enforcement point.
                record_action = Action('principal','write',f'resource-{i}',1,1) if stale_mode == 'detected' else action
                asserted = truth ^ corrupt ^ (stale_mode != 'fresh')
                records = [Record(record_action,'registry',Verdict.ALLOW if asserted else Verdict.DENY,10)] if available else []
                decision = evaluate(action,records,{'registry'},0)
                counts[(truth,decision)] += 1
            out.append(dict(availability=available_rate, corruption=corruption_rate, stale_mode=stale_mode,
                            unauthorized_executed=counts[(False,Verdict.ALLOW)], unauthorized_n=N//2,
                            authorized_completed=counts[(True,Verdict.ALLOW)], authorized_n=N//2,
                            unknown=sum(counts[(t,Verdict.UNKNOWN)] for t in (False,True))))
Path(a.output).write_text(json.dumps({'description':'Synthetic counterfactuals; corruption flips the trusted source assertion and stale evidence encodes the opposite of current truth.', 'n':N, 'results':out},indent=2)+'\n')
for row in out: print(row)
