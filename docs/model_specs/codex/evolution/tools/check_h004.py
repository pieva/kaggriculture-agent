"""Verify inference from truncated own histories, input immutability and frozen outputs."""
import gzip,hashlib,json,sys
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.evolution.tools.infer_market_order import witness,forecast
from kaggle_environments.envs.kaggriculture import kaggriculture as engine
BASE=ROOT/'docs/model_specs/codex/evolution';OUT=BASE/'reports/H004'
pred_path=OUT/'PREDICTIONS.json';blob=pred_path.read_bytes();pred=json.loads(blob);key=None;checks=0
for p in pred:
    if p['source']!=key:
        key=p['source']
        with gzip.open((ROOT/key).with_suffix('.replay.json.gz'),'rt') as f:r=json.load(f)
        r['steps']=r['steps'][:456]
    evidence=[];seat=p['seat']
    for day in range(15,20):
        i=(day-1)*24
        args=[deepcopy(r['steps'][i][seat]['observation']),deepcopy(r['steps'][i+1][seat]['observation']),deepcopy(r['steps'][i+1][seat]['action']),deepcopy(r['configuration'])]
        # The inference deliberately does not need even the public opposing farm.
        args[0]['farms'][1-seat]={'redacted':True};args[1]['farms'][1-seat]={'redacted':True}
        frozen=deepcopy(args);e=witness(*args,engine)
        assert args==frozen,'Inference mutated caller observations'
        assert e=={k:v for k,v in p['evidence'][day-15].items() if k!='day'}
        evidence.append(e);checks+=1
    assert forecast(evidence)==p['forecast']
assert hashlib.sha256(pred_path.read_bytes()).hexdigest()==hashlib.sha256(blob).hexdigest()==json.loads((OUT/'RESULT.json').read_text())['predictions_sha256']
(OUT/'CHECKS.json').write_text(json.dumps(dict(witnesses_reproduced=checks,forecasts_reproduced=len(pred),all_steps_from_D20_removed=True,opponent_public_farm_redacted=True,opponent_private_state_and_actions_not_passed=True,inputs_unchanged=True,predictions_unchanged_after_evaluation=True),indent=2)+'\n')
print('420 witnesses and84 forecasts reproduced from truncated own histories')
