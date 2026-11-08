"""Audit one-seed adaptive pilot against its matched no-attack control."""
import collections,json,sys
from pathlib import Path
control=json.loads(Path(sys.argv[1]).read_text())
assert control['no_attack']
base={r['policy']:r for r in control['results']}
for path in sys.argv[2:]:
 data=json.loads(Path(path).read_text()); assert not data['no_attack'] and data['seed']==control['seed']
 print(path)
 for result in data['results']:
  prior=base[result['policy']];history=result['history'];choices=collections.Counter(h['choice'] for h in history)
  assert all(h['budget_after']>=0 for h in history)
  print(result['policy'],'completion',prior['authorized_completed'],'->',result['authorized_completed'],'unauthorized',prior['unauthorized_executed'],'->',result['unauthorized_executed'],'issue choices',dict(choices),'targets',len({h['target'] for h in history}))
