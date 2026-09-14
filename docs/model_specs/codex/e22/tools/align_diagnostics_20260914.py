"""Align diagnostic unit events with the engine's atomic seed-demand rule."""
import json,gzip,importlib,contextlib,io
from collections import Counter
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[5]
def main():
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
 records=[]
 for group in ['external_e22_2_20260914','top_2750_3000_20260914']:
  out=ROOT/'docs/model_specs/codex/e22/reports'/group
  for g in json.loads((out/'COHORT.json').read_text()):
   r=json.loads((ROOT/g['path']).read_text());seat=g['seat'];cases=[]
   for i in range(719):
    obs=r['steps'][i][seat]['observation'];a=r['steps'][i+1][seat]['action'];cmds=[a.get('farmer',[])]+a.get('hands',[]);demand=Counter(c[1] for c in cmds if c and len(c)>1 and c[0]=='PLANT');blocked={k for k,n in demand.items() if n>obs['private']['seeds'].get(k,0)}
    if blocked:cases.append((i,blocked))
   if not cases:continue
   path=out/'profiles'/f"{g['submission']}_{g['episode']}.json";top=group.startswith('top')
   if top:path=path.with_suffix('.json.gz');data=json.load(gzip.open(path,'rt'))
   else:data=json.loads(path.read_text())
   p=data['profile' if top else 'own']
   for i,blocked in cases:
    obs=r['steps'][i][seat]['observation'];a=r['steps'][i+1][seat]['action'];day=obs['day']+1;hour=obs['hour']+1
    for key in ['failed_actions','transitions','harvest_events']:p[key]=[e for e in p[key] if (e['day'],e['hour'])!=(day,hour)]
    farm=deepcopy(obs['farms'][seat]);private=deepcopy(obs['private'])
    for w,c in enumerate([a.get('farmer',[])]+a.get('hands',[])):
     pos=engine._farmer_position(farm,w)
     if pos is None or not c:continue
     x,y=pos;old=deepcopy(farm['tiles'][y][x]);inv=deepcopy(private['inventories'][w]);cash=farm['money'];allowed=['PASS'] if c[0]=='PLANT' and c[1] in blocked else c
     engine._apply_unit_action(farm,private,w,allowed,10,obs['day'],24,100);t=farm['tiles'][y][x];gain={k:v-inv.get(k,0) for k,v in private['inventories'][w].items() if v>inv.get(k,0)};event=dict(day=day,hour=hour,worker=w,x=x,y=y,command=c)
     if c[0] in ['BUILD_PASTURE','BUILD_COOP','PLANT','PLACE','DIG'] and old!=t:p['transitions'].append(dict(event,kind=t.get('kind') if isinstance(t,dict) else t,animal=t.get('animal') if isinstance(t,dict) else None,crop=t.get('crop') if isinstance(t,dict) else None))
     if c[0]=='HARVEST' and gain:p['harvest_events'].append(dict(event,gain=gain))
     if c[0] in ['FEED','CARE','WATER','HARVEST','PLACE','BUILD_PASTURE','BUILD_COOP','PLANT'] and old==t and inv==private['inventories'][w] and cash==farm['money']:p['failed_actions'].append(dict(event,tile=old,inventory=inv))
    records.append(dict(group=group,episode=g['episode'],step=i,blocked=sorted(blocked)))
   for key in ['failed_actions','transitions','harvest_events']:p[key].sort(key=lambda e:(e['day'],e['hour'],e['worker']))
   if top:
    with gzip.open(path,'wt') as f:json.dump(data,f,separators=(',',':'))
   else:path.write_text(json.dumps(data,separators=(',',':')))
   print('ALIGNED',group,g['episode'],len(cases),flush=True)
 (ROOT/'docs/model_specs/codex/e22/reports/external_e22_2_20260914/ATOMIC_SEED_VERIFICATION.json').write_text(json.dumps(records,indent=2))
if __name__=='__main__':main()
