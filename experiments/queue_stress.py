"""Synthetic queue sensitivity; random arrival orders are independent trials."""
import json,random,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vetobench.objection_queue import Job,serve

results=[]
for attack in ('duplicate','distinct'):
 for flood in (0,25,100,300):
  for budget in (20,50,100):
   for deduplicate in (False,True):
    rates=[]
    for seed in range(200):
     jobs=[Job(f'L{i}',f'L{i}',1,True) for i in range(100)]
     jobs += [Job(f'A{i}','A' if attack=='duplicate' else f'A{i}',1,False) for i in range(flood)]
     random.Random(seed).shuffle(jobs)
     output=serve(jobs,budget,deduplicate); selected=set(output['served'])
     rates.append(sum(j.job_id in selected for j in jobs if j.legitimate)/100)
    mean=statistics.mean(rates);se=statistics.stdev(rates)/len(rates)**.5
    results.append(dict(attack=attack,flood=flood,budget=budget,deduplicate=deduplicate,mean=mean,trial_mean_ci95=[max(0,mean-1.96*se),min(1,mean+1.96*se)],trials=200))
Path('results/queue_stress.json').write_text(json.dumps({'description':'Synthetic random arrival orders, unit costs; CI applies only to simulated trial mean.', 'results':results},indent=2)+'\n')
for r in results:
 if r['budget']==50 and r['flood']==100:print(r)
