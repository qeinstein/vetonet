"""Paired outcomes across queue/attacker seeds for one fixed world."""
import json,math,statistics
from pathlib import Path
rows={}
for seed in range(780,810):
 vals=[]
 for name in ('control','random'):
  x=json.loads(Path(f'results/random-controls/{name}-{seed}.json').read_text())
  assert x['seed']==seed and x['no_attack']==(name=='control')
  vals.append({r['policy']:r for r in x['results']})
 for policy in ('fifo','risk','quota'):
  a,b=vals[0][policy],vals[1][policy]
  rows.setdefault(policy,[]).append((b['authorized_completed']-a['authorized_completed'],b['unauthorized_executed']-a['unauthorized_executed']))
for policy,values in rows.items():
 print(policy)
 for i,metric in enumerate(('completion_delta','unsafe_delta')):
  v=[x[i] for x in values]; m=statistics.mean(v); se=statistics.stdev(v)/math.sqrt(len(v))
  print(metric,'mean',round(m,3),'normal_ci95',[round(m-1.96*se,3),round(m+1.96*se,3)],'range',[min(v),max(v)])
