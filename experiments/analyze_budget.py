"""Paired allocation counterfactuals on shared LLM transcripts."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vetobench.budget_eval import run

policies=('independent_retry','shared_veto','majority','gate_fifo','gate_random','gate_risk','objection_first','evidence_aware')
for filename in sys.argv[1:]:
 data=json.loads(Path(filename).read_text());cases=data['cases']; assert len(cases)==120
 print('\n',filename)
 for attack in (0,.5,1):
  for budget in (0,30,60,120,180):
   for policy in policies:
    result=run(cases,budget,attack,policy,seed=19)
    good=sum(r['executed'] and r['authorized'] for r in result);bad=sum(r['executed'] and not r['authorized'] for r in result)
    spent=sum(c['cost'] for c,r in zip(cases,result) if r['queried']); assert spent<=budget
    print(f'{attack},{budget},{policy},{bad},60,{good},60,{spent}')
