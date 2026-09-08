import json,runpy
from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as g
p=runpy.run_path('submission/submission_codex_e19_1_662_v1.py')['create_agent']({'player_position':0})
trace=[]
class Trace:
 def __getattr__(self,k):return getattr(p,k)
 def __call__(self,o,c):
  a=p(o,c)
  if o['day']==29:
   trace.append(json.loads(json.dumps(dict(hour=o['hour'],step=o.get('step'),remaining=p.remaining,positions=p.positions,active=p.active,previous=p.previous,inventories=p.private['inventories'],shed=p.private['shed'],action=a))))
  return a
g.MissionRuntimeController=lambda *args:Trace()
r=g.run_one('CROP_POOL','E18.16',180903005,0)
open('scratch/e19_trace.json','w').write(json.dumps(trace,indent=2))
