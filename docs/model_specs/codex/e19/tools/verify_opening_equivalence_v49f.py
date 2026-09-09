"""Check the intended D2 state equivalence and measure any later divergence."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909'


def verify(path):
    b=json.loads(path.read_text());seat=b['seat']
    a=json.loads((OUT/f"{b['split']}_v48_{b['seed']}_{seat}.json").read_text())
    old=json.load(gzip.open(ROOT/a['details'],'rt',encoding='utf-8'))['replay']
    new=json.load(gzip.open(ROOT/b['details'],'rt',encoding='utf-8'))['replay']
    first_a=deepcopy(old['steps'][48][seat]['observation']['farms'][seat])
    first_b=deepcopy(new['steps'][48][seat]['observation']['farms'][seat])
    cash_difference=first_b.pop('money')-first_a.pop('money')
    assert cash_difference==3 and first_a==first_b,path.name
    assert old['steps'][48][seat]['observation']['private']==new['steps'][48][seat]['observation']['private']
    actions=[i for i in range(49,720) if old['steps'][i][seat]['action']!=new['steps'][i][seat]['action']]
    fields=[i for i in range(48,720) if old['steps'][i][seat]['observation']['farms'][seat]['tiles']!=new['steps'][i][seat]['observation']['farms'][seat]['tiles']]
    return dict(split=b['split'],seed=b['seed'],seat=seat,d2_closed_farm_and_private_equal=True,
        d2_cash_gain=cash_difference,post_d2_action_differences=actions,post_d2_tile_differences=fields,
        monthly_pass_delta=sum(d['pass_count'] for d in b['daily'])-sum(d['pass_count'] for d in a['daily']),
        monthly_move_delta=sum(d['move'] for d in b['daily'])-sum(d['move'] for d in a['daily']))


if __name__=='__main__':
    rows=[verify(p) for p in sorted(OUT.glob('*_v49f_*.json')) if p.name.startswith(('development_','validation_')) and not p.name.endswith('_obligations.json')]
    (OUT/'opening_equivalence.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps(rows),flush=True)
