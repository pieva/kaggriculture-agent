import json
from pathlib import Path
p=Path('docs/model_specs/codex/e19/artifacts/derived/portfolio_succession_20260907')
for v in [33,38,39]:
    r=json.loads((p/f'daily_routes_v{v}_180903001_0.json').read_text(encoding='utf-8'));s=r['sides']['candidate']
    print(v,dict(cash=s['reward'],deaths=len(s['crop_starvation']),cultivated=[d['crop_tiles'] for d in s['daily'][20:25]],wheat=[d['crops']['WHEAT'] for d in s['daily'][20:25]],carrot=[d['crops']['CARROT'] for d in s['daily'][20:25]],weeds=s['operational_daily'][29]['weed_tiles']))
