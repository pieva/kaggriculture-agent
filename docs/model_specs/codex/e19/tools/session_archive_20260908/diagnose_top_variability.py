import json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
p=Path('docs/model_specs/codex/e19/artifacts/derived/new_top_screen_20260908')
cases=[(106815633,'SpaTaro'),(106824217,'SpaTaro'),(106817281,'SpaTaro'),(106823287,'Matthew Huang'),(106829776,'Matthew Huang'),(106831569,'Suliman Tadros')]
out=[]
for ep,name in cases:
 r=json.loads((p/f'{ep}.json').read_text(encoding='utf-8'));seat=r['info']['TeamNames'].index(name)
 ledger=audit(r,seat);ops=daily_operational_kpi(r,seat,ledger)
 events=[dict(day=x['day'],loss=x['verified_animal_losses']) for x in ops if x['verified_animal_losses']]
 out.append(dict(episode=ep,name=name,animal_losses=events,ledger=ledger,operations=ops))
 print(json.dumps(dict(episode=ep,name=name,animal_losses=events)),flush=True)
(p/'variability_diagnosis.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
