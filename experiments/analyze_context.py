"""Report all decisions, including unresolved outputs, and paired transitions."""
import collections, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vetobench.parsing import parse
from vetobench.protocols import Decision

for filename in sys.argv[1:]:
    data=json.loads(Path(filename).read_text()); items=data['items']
    conditions=('no_prior','prior_refusal','prior_refusal_verified')
    assert len(items)==480 and len({(r['id'],r['condition']) for r in items})==480
    bykey={(r['id'],r['condition']):r for r in items}
    assert all((r['id'],c) in bykey for r in items for c in conditions)
    print('\n',filename, data['model'])
    for mode in ('strict','anchored'):
        print('parser',mode)
        for condition in conditions:
            for truth in (False,True):
                rows=[r for r in items if r['condition']==condition and r['authorized']==truth]
                counts=collections.Counter(parse(r['raw'],mode).value for r in rows)
                print(condition,'authorized',truth,'n',len(rows),dict(counts))
        for truth in (False,True):
            counts=collections.Counter()
            for item in items:
                if item['condition'] != 'no_prior' or item['authorized'] != truth: continue
                x=parse(item['raw'],mode).value
                y=parse(bykey[(item['id'],'prior_refusal')]['raw'],mode).value
                counts[(x,y)]+=1
            print('paired no_prior -> refusal authorized',truth,dict(counts))
