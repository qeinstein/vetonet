"""Check pilot dataset integrity and paired scenario alignment."""
import json
from pathlib import Path

base = Path('results')
for name in ('qwen25_3b_pilot.json','qwen25_3b_neutral.json','smol_original.json','smol_neutral.json','smol-forced-original.json','smol-forced-neutral.json'):
    data=json.loads((base/name).read_text())
    rows=data['scenarios']
    assert len(rows)==160 and len({r['id'] for r in rows})==160, name
    assert sum(r['authorized'] for r in rows)==80, name
    assert all(len(r['raw'])==3 for r in rows), name
    assert all(r['authorized']==(r['role'] in r['allowed']) for r in rows), name
    print(name, 'ok')
for name in ('qwen_context.json','smol_context.json'):
    items=json.loads((base/name).read_text())['items']
    assert len(items)==480 and len({(r['id'],r['condition']) for r in items})==480, name
    print(name, 'ok')
