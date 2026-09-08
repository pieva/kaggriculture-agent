import json,hashlib
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];B=ROOT/'docs/model_specs/codex/e19';O=B/'reports/harvest_deadlines_770_20260908';O.mkdir(exist_ok=True,parents=True)
summary={};sources={}
for v,date in [('v25','20260908'),('v26','20260908')]:
 a=B/f'artifacts/derived/daily_routes_{v}_audit_{date}'
 replay=a/'replay.json';r=json.loads(replay.read_text())
 result=json.loads((a/f'daily_routes_{v}_audit_180903001_0.json').read_text())
 original=json.loads((B/f'artifacts/derived/portfolio_succession_20260907/daily_routes_{v}_180903001_0.json').read_text())
 assert result['sides']==original['sides']
 events=[]
 for i in range(1,len(r['steps'])):
  prev=r['steps'][i-1][0]['observation'];now=r['steps'][i][0]['observation']
  for y,row in enumerate(prev['farms'][0]['tiles']):
   for x,t in enumerate(row):
    n=now['farms'][0]['tiles'][y][x]
    if isinstance(t,dict) and t.get('kind')=='PLANT' and isinstance(n,dict) and n.get('kind')=='WEED':
     expired=t.get('max_lifespan_step',-1)>=0 and t['max_lifespan_step']<=i
     cause=('decay_with_product' if t.get('yield_units',0)>0 else 'spent_crop') if expired else 'water'
     events.append(dict(day=prev['day']+1,hour=prev['hour']+1,position=[x,y],crop=t['crop'],cause=cause,before=t))
 water=[e for e in events if e['cause']=='water'];assert len(water)==len(original['sides']['candidate']['crop_starvation'])
 summary[v]=dict(counts=dict(Counter(e['cause'] for e in events)),by_crop=dict(Counter(e['cause']+':'+e['crop'] for e in events)),events=events)
 sources[str(replay.relative_to(ROOT))]=hashlib.sha256(replay.read_bytes()).hexdigest()
(O/'decay_audit.json').write_text(json.dumps(dict(case=dict(seed=180903001,seat=0),source_hashes=sources,variants=summary),indent=2))
print(json.dumps({v:{k:x for k,x in s.items() if k!='events'} for v,s in summary.items()},indent=2))
