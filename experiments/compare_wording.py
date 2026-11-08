"""Paired descriptive comparison; validates scenario identity before comparing."""
import collections, json, sys
left, right = [json.load(open(p))['scenarios'] for p in sys.argv[1:3]]
a, b = ({r['id']: r for r in rows} for rows in (left, right))
assert a.keys() == b.keys()
changes = collections.Counter()
for key in a:
    x, y = a[key], b[key]
    assert all(x[k] == y[k] for k in ('authorized', 'role', 'allowed', 'resource'))
    first = lambda r: r['raw'][0].strip().upper() == 'APPROVE'
    changes[(x['authorized'], first(x), first(y))] += 1
for label in (False, True):
    print('authorized=', label, 'original -> neutral:', {f'{int(x)}->{int(y)}': changes[(label,x,y)] for x in (False,True) for y in (False,True)})
