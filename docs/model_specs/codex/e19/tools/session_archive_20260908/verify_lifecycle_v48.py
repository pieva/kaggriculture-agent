import importlib
import json
from copy import deepcopy
from pathlib import Path
engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
base=Path('docs/model_specs/codex/e19')
probe=json.loads((base/'artifacts/derived/residual_water_770_20260908/daily_routes_v48_diagnostic_180903003_0.json').read_text(encoding='utf-8'))
row=next(r for r in probe['trace'] if r.get('probe') and r['day']==28 and r['hour']==24)
tile=row['tiles'][9][2]
assert row['positions'][9]==[2,9]
assert row['commands']['hands'][8]==['HARVEST']
assert tile['yield_units']==1
out={}
for watered in [False,True]:
    t=deepcopy(tile)
    t['yield_units']=0 # HARVEST transfers the last held unit into inventory.
    t['watered_today']=watered
    f={'tiles':[[t]]}
    engine._decay_plants(f,671)
    assert f['tiles'][0][0]['kind']=='PLANT'
    engine._daily_refresh_plants(f,27,24)
    out[str(watered)]={'after_D28':deepcopy(f['tiles'][0][0])}
    engine._decay_plants(f,672)
    out[str(watered)]['after_first_D29_action']=deepcopy(f['tiles'][0][0])
    assert f['tiles'][0][0]['kind']=='WEED'
assert out['False']['after_D28']['kind']=='WEED'
assert out['True']['after_D28']['kind']=='PLANT'
(base/'artifacts/derived/lifecycle_audit_770_20260908/counterfactual.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('Verified: final unit harvested; WATER only delays WEED by one action, no further yield.')
