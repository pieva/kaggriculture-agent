"""Audit frozen external E22 histories, recorded actions and standard daily KPIs."""
import json,sys,hashlib,contextlib,io,importlib,gzip
from pathlib import Path
from collections import Counter
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT));OUT=ROOT/'docs/model_specs/codex/e22/reports/external_e22_2_20260914'

def enrich(r,seat,policy=None,trace=False):
 from docs.model_specs.codex.e20.tools.analyze_first_external import profile
 import kaggle_environments.envs.kaggriculture.kaggriculture as engine
 p=profile(r,seat);maps=[]
 for day in range(1,31):
  f=r['steps'][day*24-1][seat]['observation']['farms'][seat]
  maps.append([dict(x=x,y=y,kind=t['kind'],animal=t.get('animal'),crop=t.get('crop')) for y,row in enumerate(f['tiles']) for x,t in enumerate(row) if isinstance(t,dict)])
 p['maps']=maps;p['policy_differences']=[];p['unfed']=[];p['failed_actions']=[];p['transitions']=[];p['harvest_events']=[];routes=[];commands=[]
 for i in range(len(r['steps'])-1):
  obs=r['steps'][i][seat]['observation'];a=r['steps'][i+1][seat]['action'] or {};commands.append(a)
  if policy is not None and policy(obs,r['configuration'])!=a:p['policy_differences'].append(i)
  farm=deepcopy(obs['farms'][seat]);private=deepcopy(obs['private'])
  cmds=[a.get('farmer',['PASS'])]+a.get('hands',[])
  demand=Counter(c[1] for c in cmds if c and len(c)>1 and c[0]=='PLANT');blocked={k for k,n in demand.items() if n>private['seeds'].get(k,0)}
  for w,cmd in enumerate([a.get('farmer',['PASS'])]+a.get('hands',[])):
   pos=engine._farmer_position(farm,w)
   if pos is None or not cmd:continue
   x,y=pos;old=deepcopy(farm['tiles'][y][x]);inv=deepcopy(private['inventories'][w]);cash=farm['money']
   allowed=['PASS'] if cmd[0]=='PLANT' and cmd[1] in blocked else cmd
   engine._apply_unit_action(farm,private,w,allowed,int(r['configuration'].get('boardSize',10)),obs['day'],24,int(r['configuration'].get('shedCapacity',100)))
   t=farm['tiles'][y][x];gain={k:v-inv.get(k,0) for k,v in private['inventories'][w].items() if v>inv.get(k,0)};event=dict(day=obs['day']+1,hour=obs['hour']+1,worker=w,x=x,y=y,command=cmd)
   if trace:routes.append(event)
   if cmd[0] in ['BUILD_PASTURE','BUILD_COOP','PLANT','PLACE','DIG'] and old!=t:p['transitions'].append(dict(event,kind=t.get('kind') if isinstance(t,dict) else t,animal=t.get('animal') if isinstance(t,dict) else None,crop=t.get('crop') if isinstance(t,dict) else None))
   if cmd[0]=='HARVEST' and gain:p['harvest_events'].append(dict(event,gain=gain))
   if cmd[0] in ['FEED','CARE','WATER','HARVEST','PLACE','BUILD_PASTURE','BUILD_COOP','PLANT'] and old==t and inv==private['inventories'][w] and cash==farm['money']:
    p['failed_actions'].append(dict(event,tile=old,inventory=inv))
  if i%24==23:
   f=r['steps'][i+1][seat]['observation']['farms'][seat]
   for y,row in enumerate(f['tiles']):
    for x,t in enumerate(row):
     if isinstance(t,dict) and t.get('animal') and t.get('consecutive_unfed',0):p['unfed'].append(dict(day=i//24+1,x=x,y=y,animal=t['animal'],consecutive=t['consecutive_unfed']))
 p['command_hash']=hashlib.sha256(json.dumps(commands,sort_keys=True).encode()).hexdigest();p['worker_command_hash']=hashlib.sha256(json.dumps([[a.get('farmer'),a.get('hands')] for a in commands],sort_keys=True).encode()).hexdigest()
 if trace:p['routes']=routes;p['commands']=commands
 p['totals']={k:dict(sum((Counter(d[k]) for d in p['ledger']['daily']),Counter())) for k in ['planted','harvested','sold_units','sales_cash','purchase_cash']}
 p['totals'].update({k:sum(d[k] for d in p['ledger']['daily']) for k in ['hire_cash','land_cash','unit_cash_delta']})
 assert abs(3000+sum(p['totals']['sales_cash'].values())-sum(p['totals']['purchase_cash'].values())-p['totals']['hire_cash']-p['totals']['land_cash']+p['totals']['unit_cash_delta']-p['reward'])<.01
 return p

def main():
 with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
  from kaggle_environments.agent import get_last_callable
  from docs.model_specs.codex.e20.tools.analyze_first_external import profile
 policies={sid:get_last_callable((ROOT/'submission'/name).read_text()) for sid,name in [(56212495,'submission_codex_e22_2_pascoli.py'),(56206528,'submission_codex_e22_1_pollai.py')]}
 dest=OUT/'profiles';dest.mkdir(exist_ok=True)
 for g in json.loads((OUT/'COHORT.json').read_text()):
  path=dest/f"{g['submission']}_{g['episode']}.json"
  if path.exists():continue
  raw=(ROOT/g['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256'];r=json.loads(raw);assert len(r['steps'])==720 and all(x['status']=='DONE' for x in r['steps'][-1])
  for i,s in enumerate(r['steps']):s[0]['observation']['step']=i
  p=enrich(r,g['seat'],policies[g['submission']]);op=profile(r,1-g['seat']);path.write_text(json.dumps(dict(meta=g,own=p,opponent=op),separators=(',',':')))
  print('AUDITED',g['submission'],g['episode'],'cash',p['reward'],'escapes',len(p['ledger']['animal_escapes']),'parity',len(p['policy_differences']),flush=True)
if __name__=='__main__':main()
