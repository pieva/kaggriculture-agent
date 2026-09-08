import json
from pathlib import Path
p=Path('docs/model_specs/codex/e19/artifacts/derived/residual_water_770_20260908/daily_routes_v48_diagnostic_180903003_0.json')
r=json.loads(p.read_text(encoding='utf-8'))
for row in r['trace']:
    if not row.get('probe') or row['day']not in (28,29):continue
    tile=row['tiles'][9][2]
    jobs={w:j for w,j in row['active'].items() if j['target']==[2,9]}
    if row['day']==28 or row['hour']==1:
        print(row['day'],row['hour'],'tile',tile,'jobs',jobs)
