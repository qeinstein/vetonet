"""Budgeted simulated evidence monitor, scored only after allocation."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vetobench.evidence_service import EvidenceService,GrantRecord
from vetobench.hidden_budget import coordinate
for path in sys.argv[1:]:
 data=json.loads(Path(path).read_text());cases=data['cases'];world=data['world']
 assert len(cases)==120 and len(world)==120 and sum(world.values())==60
 service=EvidenceService({k:GrantRecord(**v) for k,v in data['registry'].items()},set(data['outages']))
 print('\n',path)
 for attack in (0.0,0.5,1.0):
  for budget in (30,60,120,180):
   for strategy in ('fifo','random','risk','evidence_aware'):
    result=coordinate(cases,service,budget,strategy,attack,19)
    good=sum(r['executed'] and world[r['id']] for r in result);bad=sum(r['executed'] and not world[r['id']] for r in result)
    spent=sum(c['cost'] for c,r in zip(cases,result) if r['queried']);assert spent<=budget
    print(f'{attack},{budget},{strategy},{bad}/60,{good}/60,spent={spent}')
