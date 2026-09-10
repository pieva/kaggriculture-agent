"""Identify CARE with zero optimistic production gain, using only observed state."""
import argparse
import gzip
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.policy import care_can_add_yield
BASE=ROOT/'docs/model_specs/codex/e20'
RULES={'COW':dict(first_yield_day=8,interval=2,max_held=6),
       'SHEEP':dict(first_yield_day=6,interval=3,max_held=6)}

def audit(path,seat):
    with gzip.open(path,'rt') as f:r=json.load(f)
    events=[]
    for i in range(1,len(r['steps'])):
        o=r['steps'][i-1][seat]['observation'];farm=o['farms'][seat]
        action=r['steps'][i][seat]['action'] or {};day=o['day']
        for w,c in enumerate([action.get('farmer',[]),*action.get('hands',[])]):
            if c!=['CARE']:continue
            x,y=[farm['farmer'],*farm['hands']][w];t=farm['tiles'][y][x]
            if not isinstance(t,dict) or t.get('animal') not in RULES:continue
            if not care_can_add_yield(t,day,29,RULES[t['animal']]):
                events.append(dict(day=day+1,hour=o['hour']+1,position=[x,y],animal=t['animal'],
                    pending_bonus=t.get('pending_care_bonus',0)))
    return dict(replay=str(path.relative_to(ROOT)),seat=seat,zero_gain_care=events)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage');p.add_argument('--model',required=True);a=p.parse_args()
    result=[audit(p,0) for p in sorted((BASE/'artifacts'/a.stage).glob(f'{a.model}_E18_*.replay.json.gz'))]
    out=BASE/f'reports/e20_1/care_audit_{a.model}.json';out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({r['replay']:len(r['zero_gain_care']) for r in result}))
