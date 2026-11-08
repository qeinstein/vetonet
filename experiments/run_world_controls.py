"""Random attacker/control over newly sampled synthetic worlds (no model calls)."""
import json,random,runpy,sys
from pathlib import Path
base=Path(__file__).resolve().parent; out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
model=sys.argv[2]; template=json.loads(Path(sys.argv[3]).read_text())
for seed in range(900,950):
 rng=random.Random(seed); data=json.loads(json.dumps(template));truth=[False]*60+[True]*60;rng.shuffle(truth);data['world']={};data['registry']={};data['outages']=[]
 for c,granted in zip(data['cases'],truth):
  c.update(risk=rng.choice([.2,.5,.9]),cost=rng.choice([1,2]),source_reliability=rng.choice([.5,.8,1.]),compromised_draw=rng.random())
  cid=c['id'];data['world'][cid]=granted
  data['registry'][cid]=dict(principal=c['principal'],resource=c['resource'],operation=c['operation'],state_version=1 if rng.random()<.1 else 2,allowed=granted ^ (rng.random()<.05),issuer='registry')
  if rng.random()<.2:data['outages'].append(cid)
 worldfile=out/f'world-{seed}.json';worldfile.write_text(json.dumps(data,indent=2)+'\n')
 for name,flag in [('random','--random-attacker'),('control','--no-attack')]:
  sys.argv=[str(base/'model_selected_objections.py'),'--model',model,'--input',str(worldfile),'--seed',str(seed),flag,'--output',str(out/f'{name}-{seed}.json')]
  runpy.run_path(sys.argv[0],run_name='__main__')
