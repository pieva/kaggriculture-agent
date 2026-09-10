"""Attribute H005 abstentions without changing frozen predictions or thresholds."""
import gzip,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.evolution.tools.infer_market_order_mixed import witness
from kaggle_environments.envs.kaggriculture import kaggriculture as engine
BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/H005';pred=json.loads((OUT/'PREDICTIONS.json').read_text());key=None;rows=[]
for p in pred:
 cases=[e for e in p['evidence'] if e['status']=='inconsistent_competing_supply']
 if not cases:continue
 if key!=p['source']:
  key=p['source']
  with gzip.open((ROOT/key).with_suffix('.replay.json.gz'),'rt') as f:r=json.load(f)
 for e in cases:
  captured={}
  def profile(frame,event,value):
   if event=='return' and frame.f_code.co_name=='witness' and isinstance(value,dict) and value.get('status')=='inconsistent_competing_supply':
    v=frame.f_locals;captured.update(item=v['item'],inventory_before=v['inv'],inventory_after_before_consumption=v['last'],own_units=v['q'],apparent_competing_supply=v['other'],initial_price=engine.market_price(v['item'],v['inv'],v['before']['market'].get('params')))
  i=(e['day']-1)*24;s=p['seat'];sys.setprofile(profile)
  try:result=witness(r['steps'][i][s]['observation'],r['steps'][i+1][s]['observation'],r['steps'][i+1][s]['action'],r['configuration'],engine)
  finally:sys.setprofile(None)
  assert result['status']==e['status'] and captured
  rows.append(dict(model=p['model'],seed=p['seed'],seat=s,day=e['day'],**captured))
summary=dict(cases=len(rows),initial_floor=sum(r['initial_price']==1 for r in rows),by_item=dict(Counter(r['item'] for r in rows)),rows=rows)
(OUT/'ABSTENTION_DIAGNOSIS.json').write_text(json.dumps(summary,indent=2)+'\n');print({k:v for k,v in summary.items() if k!='rows'})
