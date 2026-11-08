"""Count selected first-stage refusals and matched second-stage outcomes."""
import collections,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vetobench.parsing import parse
for filename in sys.argv[1:]:
 data=json.loads(Path(filename).read_text()); cases=data['cases']
 assert len(cases)==160 and len({r['id'] for r in cases})==160
 selected=[r for r in cases if r['delegated']]
 assert len(selected)==data['selected_refusals']
 print('\n',filename,'selected',len(selected),'of',len(cases))
 print('first stage:',dict(collections.Counter(r['first_raw'].strip().upper() for r in cases).most_common(8)))
 for mode in ('strict','anchored'):
  for truth in (False,True):
   subset=[r for r in selected if r['authorized']==truth]
   for condition in ('fresh','same_worker','shared_refusal'):
    counts=collections.Counter(parse(r['delegated'][condition]['raw'],mode).value for r in subset)
    print(mode,'authorized',truth,condition,'n',len(subset),dict(counts))
