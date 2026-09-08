import json
from pathlib import Path
p=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907/daily_routes_v48_180903003_0.json')
r=json.loads(p.read_text(encoding='utf-8'))
for plan in r['daily_routes']:
    if plan['day']!=28:continue
    for route in plan['routes']:
        if any(v['target']==[2,9] for v in route['visits']):
            print('hour',plan['hour'],'worker',route['worker'],'cost',route['cost'],'available',route['available'],'visits',route['visits'])
    for visit in plan['unassigned']:
        if visit['target']==[2,9]:print('UNASSIGNED',plan['hour'],visit)
