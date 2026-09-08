import sys,json,runpy
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.daily_route_scheduler_770_v29 import install
r=json.loads((ROOT/'docs/model_specs/codex/e19/artifacts/derived/v29_external_20260908/106724977.json').read_text(encoding='utf-8'))
p=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'))['create_agent']({'player_position':0})
install(p.core);c=p.core; stats=defaultdict(Counter);examples=[]
growth,prepare,cert=c._growth,c._prepare_steps,c._day_route_certificate
def g(cash):
    offers=growth(cash)
    for o in offers:stats[c.day+1]['offer_'+o[4]]+=1
    return offers
def prep(w,t,cmds,**kw):
    v=prepare(w,t,cmds,**kw)
    if any(x[0]=='PLANT' for x in cmds):stats[c.day+1]['prepare_'+str(v is not None)]+=1
    return v
def certificate(w,job,services=None):
    before=Counter(c.metrics);v=cert(w,job,services)
    stats[c.day+1]['certificate_'+str(v)]+=1
    stats[c.day+1].update(Counter(c.metrics)-before)
    if 20<=c.day<=21 and len(examples)<10:examples.append(dict(day=c.day+1,hour=c.hour,job=job,ok=v,metrics=dict(Counter(c.metrics)-before)))
    return v
c._growth=g;c._prepare_steps=prep;c._day_route_certificate=certificate
for i in range(719):
    obs=r['steps'][i][0]['observation'];a=p(obs,r['configuration'])
    assert a==r['steps'][i+1][0]['action'],i
print(json.dumps(dict(stats=stats,examples=examples),indent=2))
