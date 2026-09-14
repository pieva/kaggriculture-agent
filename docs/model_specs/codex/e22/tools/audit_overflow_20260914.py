"""Replay daily closing batches and verify losses due to shed overflow."""
import json,sys,contextlib,io,importlib
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
from collections import Counter
ROOT=Path(__file__).resolve().parents[5];OUT=ROOT/'docs/model_specs/codex/e22/reports/external_e22_2_20260914'
def total(p):return Counter(p['shed'])+sum((Counter(i) for i in p['inventories']),Counter())
def main():
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
 results=[]
 for g in json.loads((OUT/'COHORT.json').read_text()):
  r=json.loads((ROOT/g['path']).read_text());seat=g['seat'];events=[]
  for index,step in enumerate(r['steps']):step[0]['observation']['step']=index
  for i in range(23,719,24):
   before=r['steps'][i];after=r['steps'][i+1];obs=before[0]['observation'];farms=deepcopy(obs['farms']);market=deepcopy(obs['market']);cfg=SimpleNamespace(**r['configuration']);cap=int(r['configuration'].get('shedCapacity',100));states=[SimpleNamespace(action=s['action'] or {},observation=SimpleNamespace(farms=farms,market=market,private=deepcopy(before[j]['observation']['private']))) for j,s in enumerate(after)]
   for j,state in enumerate(states):
    cmds=[state.action.get('farmer',['PASS'])]+state.action.get('hands',[]);private=state.observation.private
    demand=Counter(c[1] for c in cmds if c and len(c)>1 and c[0]=='PLANT');blocked={k for k,n in demand.items() if n>private['seeds'].get(k,0)}
    for w,c in enumerate(cmds):
     allowed=['PASS'] if c and c[0]=='PLANT' and c[1] in blocked else c
     engine._apply_unit_action(farms[j],private,w,allowed,10,obs['day'],24,cap)
   engine._process_market(states,SimpleNamespace(configuration=cfg));private=states[seat].observation.private;stock=total(private);shed_before=deepcopy(private['shed']);actual=total(after[seat]['observation']['private'])
   assert not actual-stock,(g['episode'],i,'unexpected stock gain')
   lost=stock-actual
   assert sum(lost.values())==max(0,sum(stock.values())-cap),(g['episode'],i,'capacity mismatch')
   if lost:events.append(dict(day=obs['day']+1,discarded=dict(lost),shed_before=shed_before))
  result=dict(submission=g['submission'],episode=g['episode'],events=events);results.append(result)
  print('OVERFLOW',g['submission'],g['episode'],[(e['day'],e['discarded']) for e in events],flush=True)
 (OUT/'OVERFLOW.json').write_text(json.dumps(results,indent=2))
if __name__=='__main__':main()
