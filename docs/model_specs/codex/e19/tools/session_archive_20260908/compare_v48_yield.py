import json
from pathlib import Path
p=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
for v in (47,48):
    s=json.loads((p/f'daily_routes_v{v}_180903001_0.json').read_text(encoding='utf-8'))['sides']['candidate']
    print(v,{crop:{k:sum(d[k].get(crop,0) for d in s['ledger']['daily'][27:]) for k in ['harvested','sold_units','sales_cash']} for crop in ['WHEAT','CARROT']},'late losses',[e for e in s['crop_starvation'] if e['service_day']>=28])
