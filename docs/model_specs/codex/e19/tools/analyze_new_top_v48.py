"""Frozen replay census and descriptive benchmarks; no policy changes."""
import sys,json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
B=ROOT/'docs/model_specs/codex/e19';RAW=B/'artifacts/derived/new_top_screen_20260908';OUT=B/'reports/new_top_v48_20260908'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 cohorts=read(B/'artifacts/derived/new_top_cohorts.json'); census=[];profiles=[]
 for name,sub,eps in cohorts:
  for ep in eps:
   path=RAW/f'{ep}.json';r=read(path);seat=r['info']['TeamNames'].index(name)
   assert len(r['steps'])==720 and r['statuses']==['DONE','DONE']
   daily=[snapshot(r,d,seat) for d in range(1,31)];extra=[]
   for d in range(1,31):
    farm=r['steps'][24*d-1][seat]['observation']['farms'][seat]
    pastures=[];plants=[];mix=[];q2=Counter()
    for y,row in enumerate(farm['tiles']):
     for x,t in enumerate(row):
      if isinstance(t,dict):
       if t.get('kind')=='PASTURE':pastures.append([x,y])
       if t.get('kind')=='PLANT':plants.append([x,y,t['crop'],t['planted_day']+1])
       if t.get('animal'):mix.append([x,y,t['animal'],t['placed_day']+1])
       if x<5 and y>=5:q2[t.get('kind')]+=1
    extra.append(dict(day=d,pastures=pastures,plants=plants,animals=mix,q2=dict(q2),q2_unlocked='SW' in farm['unlocked_quadrants']))
   qs=[tuple(z['pasture_topology'].values()) for z in daily]
   mode,count=Counter(qs[14:25]).most_common(1)[0]
   stable_start=next((i+1 for i in range(14,26) if len(set(qs[i:i+5]))==1),None)
   q2open=next((e['day'] for e in extra if e['q2_unlocked']),None)
   q2used=next((e['day'] for e in extra if e['q2'].get('PLANT',0)+e['q2'].get('PASTURE',0)+e['q2'].get('COOP',0)>0),None)
   # Exact pasture layout, not just counts, stable for five checkpoints after unlock.
   q2stable=next((i+1 for i in range(26) if extra[i]['q2_unlocked'] and len({json.dumps([p for p in e['pastures'] if p[0]<5 and p[1]>=5]) for e in extra[i:i+5]})==1),None)
   row=dict(name=name,submission=sub,episode=ep,seat=seat,topology_D11=qs[10],topology_D15=qs[14],topology_D25=qs[24],topology_D30=qs[29],mode_D15_D25=mode,mode_days=count,changes_D15_D25=sum(a!=b for a,b in zip(qs[14:24],qs[15:25])),stable_start=stable_start,q2_open=q2open,q2_used=q2used,q2_layout_stable5=q2stable,checkpoints770=sum(q==(7,7,0,0) for q in qs[14:]),daily=daily,spatial=extra,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
   census.append(row)
   if name in ['Subin An','Matthew Huang','Suliman Tadros']:
    ledger=audit(r,seat)
    profiles.append(dict(name=name,episode=ep,seat=seat,daily=daily,ledger=ledger,terminal=end_state(r,seat),operational_daily=daily_operational_kpi(r,seat,ledger)))
  print(name,flush=True)
 (OUT/'census.json').write_text(json.dumps(census,ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf-8')
 (OUT/'cohorts.json').write_text(json.dumps(cohorts,ensure_ascii=False,indent=2),encoding='utf-8')
 print('DONE',flush=True)
if __name__=='__main__':main()
