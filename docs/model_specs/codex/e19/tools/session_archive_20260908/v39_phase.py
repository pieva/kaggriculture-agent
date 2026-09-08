import json
from statistics import mean
from pathlib import Path
p=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
for v in [33,38,39]:
    r=json.loads((p/f'daily_routes_v{v}_180903001_0.json').read_text(encoding='utf-8'));s=r['sides']['candidate']
    print(v,{k:round(mean(d[k] for d in s['operational_daily'][20:25]),2) for k in ['MOVE','PASS','weed_tiles']}, {k:round(mean(d['executed_actions'].get(k,0) for d in s['ledger']['daily'][20:25]),2) for k in ['WATER','FEED','CARE','PLANT']})
    if v==39:
        offers=[(d['day'],v['target'],v['commands']) for d in r['daily_routes'] for route in d['routes'] for v in route['visits'] if v['kind']=='NEW_ROTATION' and v['commands'][0]==['DIG']]
        print('Scheduled empty-perennial renewals, repeated plan snapshots:',len(offers),'unique targets:',len({tuple(x[1]) for x in offers}),'examples:',offers[:3])
