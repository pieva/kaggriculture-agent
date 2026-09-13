"""Diagnostic only: recorded opponent actions, public initial state, replacement RNG."""
import sys,json,copy,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from kaggle_environments import make
from docs.model_specs.codex.e20.tools.operational_calendar_v44 import Agent
BASE=ROOT/'docs/model_specs/codex/e20'
def main():
 inv=json.loads((BASE/'reports/external_e20_8_20260913/INVENTORY.json').read_text())
 rows=[]
 for g in inv['models']['E20.8']['games']:
  r=json.loads((ROOT/g['raw_path']).read_text());seat=g['seat']
  for label in ['Reference','Candidate']:
   config=dict(r['configuration']);config['seed']=180911301
   env=make('kaggriculture',configuration=config,debug=False);env.reset(2)
   if label=='Candidate':policy=Agent({'player_position':seat})
   else:
    scope={};exec((ROOT/'submission/submission_codex_e20_8_e20v40_calendar_2g.py').read_text(),scope);policy=scope['create_agent']({'player_position':seat})
   points={}
   for i in range(48):
    obs=copy.deepcopy(env.state[seat].observation)
    actions=[copy.deepcopy(x['action']) for x in r['steps'][i+1]]
    actions[seat]=policy(obs,env.configuration)
    env.step(actions)
    if i in (23,24,47):
     o=env.state[seat].observation;f=o.farms[seat]
     points[str(i+1)]={'cash':f.money,'hands':len(f.hands),'animals':sum(bool(t.get('animal')) for row in f.tiles for t in row if isinstance(t,dict)),'wheat':o.private.shed.get('WHEAT',0)}
   recorded=r['steps'][24][seat]['observation']['farms'][seat]['money']
   rows.append(dict(episode=g['episode'],seat=seat,model=label,points=points,recorded_day1_cash=recorded,day1_cash_matches=points['24']['cash']==recorded))
   print(g['episode'],label,points,flush=True)
 out=BASE/'reports/e20_9_release';out.mkdir(exist_ok=True)
 (out/'OPENINGS.json').write_text(json.dumps({'method':'48 steps with recorded opponent commands, exposed replacement seed301 (public seed null). Diagnostic, not reactive opponent benchmark or exact public replay reproduction.','rows':rows},indent=2),encoding='utf-8')
if __name__=='__main__':main()
