import json
from pathlib import Path
from statistics import mean
p=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
for v in [41,44]:
    ps=[json.loads((p/f'daily_routes_v{v}_{s}_{t}.json').read_text(encoding='utf-8'))['sides']['candidate'] for s in range(180903001,180903004) for t in (0,1)]
    print(v,'ledger keys',list(ps[0]['ledger']['daily'][25]))
    for d in range(25,31):
        print(d,{k:round(mean(x['ledger']['daily'][d-1]['executed_actions'].get(k,0) for x in ps),2) for k in ['HARVEST','PLANT','WATER','FEED','CARE']},'crops',ps[0]['daily'][d-1]['crops'])
    for key in ['harvested','sold_units','sales_cash','purchase_cash']:
        vals=[d[key] for x in ps for d in x['ledger']['daily'][25:] if key in d]
        if vals and isinstance(vals[0],dict):
            print(key,{k:round(sum(v.get(k,0) for v in vals)/6,2) for k in set().union(*vals)})
        elif vals:print(key,sum(vals)/6)
