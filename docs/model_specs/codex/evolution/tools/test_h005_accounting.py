"""Engine-backed synthetic checks for signed lockstep accounting."""
import gzip,json,sys
from copy import deepcopy
from itertools import permutations
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.evolution.tools.infer_market_order_mixed import witness
from kaggle_environments.envs.kaggriculture import kaggriculture as e
BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/H005'
with gzip.open(ROOT/'docs/model_specs/codex/e20/artifacts/e20_1_confirmation/E19_E18_180910201.replay.json.gz','rt') as f:r=json.load(f)
passed=0;statuses={}
for own_op in ['SELL','BUY_PRODUCT']:
 for other_op in ['SELL','BUY_PRODUCT']:
  for order in permutations([['SELL','MILK',5],['SELL','STRAWBERRY',6],[other_op,'WHEAT',4]]):
   before=deepcopy(r['steps'][336][0]['observation']);cfg=r['configuration'];farms=deepcopy(before['farms'])
   for farm in farms:farm.update(money=100000,hands=[],hires_today=0)
   private=e._new_private();private['shed']={'MILK':20,'STRAWBERRY':20,'WHEAT':20};private['seeds']={k:0 for k in e.CROPS}
   market=deepcopy(before['market']);market['inventory']={k:e.MARKET_PARAMS[k]['I0']-100 for k in e.PRODUCTS};e._refresh_prices(market)
   before.update(farms=deepcopy(farms),private=deepcopy(private),market=deepcopy(market))
   action=dict(farmer=['PASS'],hands=[],market=[['SELL','MILK',7],['SELL','STRAWBERRY',8],[own_op,'WHEAT',3],['BUY_SEED','CARROT',2],['HIRE']])
   states=[SimpleNamespace(action=action,observation=SimpleNamespace(farms=farms,private=deepcopy(private),market=market,town=deepcopy(before['town']))),SimpleNamespace(action=dict(market=list(order)),observation=SimpleNamespace(farms=farms,private=deepcopy(private),market=market))]
   env=SimpleNamespace(configuration=SimpleNamespace(**cfg));e._process_market(states,env);e._town_consume(env,states,336)
   after=deepcopy(before);after.update(farms=deepcopy(farms),private=deepcopy(states[0].observation.private),market=deepcopy(market))
   result=witness(before,after,action,cfg,e);actual=next(i for i,o in enumerate(order) if o[1]=='STRAWBERRY')
   assert result['status'] in ['identified','ambiguous'],result
   assert actual in result['possible_positions'],(own_op,other_op,order,result)
   statuses[result['status']]=statuses.get(result['status'],0)+1;passed+=1
(OUT/'SYNTHETIC_CHECKS.json').write_text(json.dumps(dict(engine_cases=passed,statuses=statuses,all_true_positions_retained=True,own_and_competing_buys_and_sells=True,seeds_and_hires_included=True),indent=2)+'\n')
print(passed,statuses)
