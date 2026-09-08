"""Read-only deterministic policy replay: explain D12/D13 PASS decisions."""
import json,runpy,sys
from pathlib import Path
from collections import Counter
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v22 import install
BASE=ROOT/'docs/model_specs/codex/e19'
OUT=BASE/'reports/pass_d12_d13_20260908';OUT.mkdir(exist_ok=True,parents=True)
r=json.loads((BASE/'artifacts/derived/daily_routes_v22_audit_20260907/replay.json').read_text())
p=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':0});install(p.core)
c=p.core;original=c._prepare_steps;cert=c._day_route_certificate
calls=[];checks=[]
def prepare(w,t,commands,**kw):
 result=original(w,t,commands,**kw)
 if c.day in [11,12]:
  queues=c.daily_route_state.get('remaining',{});q=queues.get(str(w),[])
  owner=next((int(k) for k,v in queues.items() if list(t) in v or tuple(t) in v),None)
  gate=(owner is not None and (owner!=w or not q or tuple(q[0])!=tuple(t))) or (q and tuple(q[0])!=tuple(t))
  calls.append(dict(worker=w,target=t,commands=commands,steps=len(result) if result else None,queue_gate=bool(gate)))
 return result
def certificate(w,job,services=None):
 result=cert(w,job,services)
 if c.day in [11,12]:checks.append(dict(worker=w,target=job['target'],kind=job['kind'],accepted=bool(result)))
 return result
c._prepare_steps=prepare;c._day_route_certificate=certificate
rows=[]
for i in range(1,313):
 obs=r['steps'][i-1][0]['observation'];calls.clear();checks.clear();before=Counter(c.metrics)
 a=p(obs,r['configuration']);assert a==r['steps'][i][0]['action'],i
 if obs['day'] not in [11,12]:continue
 cmds=[a['farmer'],*a['hands']];passes=[]
 for w,cmd in enumerate(cmds):
  if cmd!=['PASS']:continue
  j=c.active.get(w);wc=[x for x in calls if x['worker']==w]
  reason='no_mission'
  if j:reason='waiting_'+j['steps'][0][0][0]
  passes.append(dict(worker=w,position=c.positions[w],reason=reason,job=j,queue=c.daily_route_state.get('remaining',{}).get(str(w),[]),attempts=len(wc),queue_rejections=sum(x['steps'] is None and x['queue_gate'] for x in wc),other_rejections=sum(x['steps'] is None and not x['queue_gate'] for x in wc),feasible=sum(x['steps'] is not None for x in wc)))
 tiles=[t for row in c.farm['tiles'] for t in row if isinstance(t,dict)]
 rows.append(deepcopy(dict(day=c.day+1,hour=c.hour+1,actions=dict(Counter(x[0] for x in cmds)),passes=passes,metric_delta=dict(Counter(c.metrics)-before),checks=checks,plan=deepcopy(c.biological_plan),unlocked=c.farm['unlocked_quadrants'],market=a['market'],cash=c.farm['money'],shed=c.private['shed'],remaining=c.remaining,unwatered=sum(t.get('kind')=='PLANT' and not t.get('watered_today') for t in tiles),unfed=sum(bool(t.get('animal')) and not t.get('fed_today') for t in tiles),uncared=sum(bool(t.get('animal')) and not t.get('cared_today') for t in tiles),crops=dict(Counter(t['crop'] for t in tiles if t.get('crop'))))))
(OUT/'hourly_audit.json').write_text(json.dumps(dict(seed=180903001,seat=0,action_parity_through_step=312,rows=rows),indent=2))
for day in [12,13]:
 rr=[x for x in rows if x['day']==day];ac=Counter();reasons=Counter()
 for x in rr:ac.update(x['actions']);reasons.update(y['reason'] for y in x['passes'])
 print('DAY',day,'actions',dict(ac),'pass_reasons',dict(reasons))
 for x in rr:
  if x['passes']:print(x['hour'],'pass',len(x['passes']),'reason',dict(Counter(y['reason'] for y in x['passes'])),'water/feed/care',x['unwatered'],x['unfed'],x['uncared'],'gates',sum(y['queue_rejections'] for y in x['passes']),'other',sum(y['other_rejections'] for y in x['passes']),'feasible',sum(y['feasible'] for y in x['passes']),'cert_reject',sum(not y['accepted'] for y in x['checks']))
