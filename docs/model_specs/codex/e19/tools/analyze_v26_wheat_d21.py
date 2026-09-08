import json,runpy,sys
from pathlib import Path
from collections import Counter
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v26 import install
B=ROOT/'docs/model_specs/codex/e19';O=B/'reports/wheat_d21_v26_20260908';O.mkdir(exist_ok=True,parents=True)
A=B/'artifacts/derived/daily_routes_v26_audit_20260908'
r=json.loads((A/'replay.json').read_text());a=json.loads((A/'daily_routes_v26_audit_180903001_0.json').read_text());original=json.loads((B/'artifacts/derived/portfolio_succession_20260907/daily_routes_v26_180903001_0.json').read_text());assert a['sides']==original['sides']
events=[];plantings=[]
for i in range(1,len(r['steps'])):
 before=r['steps'][i-1][0]['observation'];after=r['steps'][i][0]['observation'];f=before['farms'][0];g=after['farms'][0];act=r['steps'][i][0]['action'];pos=[f['farmer'],*f['hands']];cmd=[act['farmer'],*act['hands']]
 for y,row in enumerate(f['tiles']):
  for x,t in enumerate(row):
   n=g['tiles'][y][x]
   if isinstance(n,dict) and n.get('kind')=='WEED' and not (isinstance(t,dict) and t.get('kind')=='WEED'):
    at=[c for pp,c in zip(pos,cmd) if pp==[x,y]]
    cause='decay' if t.get('max_lifespan_step',-1)>=0 and t['max_lifespan_step']<=i else 'water'
    events.append(dict(day=before['day']+1,hour=before['hour']+1,position=[x,y],cause=cause,previous=t,actions_here=at))
   if isinstance(n,dict) and n.get('kind')=='PLANT' and (not isinstance(t,dict) or t.get('kind')!='PLANT' or t.get('planted_day')!=n.get('planted_day') or t.get('crop')!=n.get('crop')):
    plantings.append(dict(day=before['day']+1,hour=before['hour']+1,position=[x,y],crop=n['crop']))
p=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':0});install(p.core);c=p.core;grow=c._growth;prep=c._prepare_steps;cert=c._day_route_certificate;offers=[];checks=[];preps=[]
def growth(cash):
 out=grow(cash)
 if obs['day']>=15:offers.extend(deepcopy(out))
 return out
def prepare(w,t,cmds,**kw):
 out=prep(w,t,cmds,**kw)
 if c.day>=15 and any(z[0]=='PLANT' for z in cmds):preps.append(dict(worker=w,target=t,crop=next(z[1] for z in cmds if z[0]=='PLANT'),steps=len(out) if out else None,queue=deepcopy(c.daily_route_state.get('remaining',{}).get(str(w),[])),remaining=c.remaining))
 return out
def certificate(w,j,services=None):
 out=cert(w,j,services)
 if obs['day']>=15:checks.append(dict(worker=w,target=j['target'],accepted=bool(out)))
 return out
c._growth=growth;c._prepare_steps=prepare;c._day_route_certificate=certificate;hours=[]
for i in range(1,529):
 offers.clear();checks.clear();preps.clear();obs=r['steps'][i-1][0]['observation'];action=p(obs,r['configuration']);assert action==r['steps'][i][0]['action'],i
 if obs['day']>=15:
  unique={(tuple(o[0]),tuple(tuple(z) for z in o[1])):o for o in offers}
  hours.append(deepcopy(dict(day=c.day+1,hour=c.hour+1,cash=c.farm['money'],floor=c.maintenance_floor,feed_reserve=c.feed_reserve,active=c.active,positions=c.positions,options=c.portfolio_latest,offers=list(unique.values()),prepares=preps,certificates=checks,actions=action)))
(O/'audit.json').write_text(json.dumps(dict(action_parity=528,weed_events=events,plantings=plantings,hours=hours),indent=2))
print('Weed events',dict(Counter((x['cause'],x['previous']['crop']) for x in events)))
for d in range(16,31):
 ee=[x for x in events if x['day']==d];hh=[x for x in hours if x['day']==d];print(d,'weeds',dict(Counter((x['cause'],x['previous']['crop']) for x in ee)),'plantings',dict(Counter(x['crop'] for x in plantings if x['day']==d)),'growth unique',len({tuple(o[0]) for h in hh for o in h['offers']}),'feasible prep',sum(p['steps'] is not None for h in hh for p in h['prepares']),'cert rejects',sum(not p['accepted'] for h in hh for p in h['certificates']))

