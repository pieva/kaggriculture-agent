"""Frozen external leader benchmark, with original cash and explicit audit residuals."""
import sys,json,hashlib,importlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.audit_v51_external_ledger import audit
from docs.model_specs.codex.e19.tools.audit_v49_obligations import audit_obligations
from docs.model_specs.codex.e19.tools.replay_real_worker_slots import slots
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
B=ROOT/'docs/model_specs/codex/e19';O=B/'reports/top_v51_20260909'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
dump=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
pinned=read(ROOT/'docs/foundation/ENGINE_SOURCE_MANIFEST.json')['files']
assert all(hashlib.sha256((Path(engine.__file__).parent/n).read_bytes()).hexdigest()==h for n,h in pinned.items())
groups=read(O/'cohorts.json')
own=read(B/'reports/v51_external_20260909/cohort.json')
jobs=[dict(group='V51C',name='Pietro Valocchi',submission=56124996,episode=g['episode'],raw_path=g['raw_path']) for g in own['games']]
jobs += [dict(group=g['alias'],name=g['name'],submission=g['submission'],episode=ep,raw_path=f'data/replays/json/top_v51_20260909/{ep}.json') for g in groups for ep in g['episodes']]
catalog=[]
for j in jobs:
    ep=j['episode'];cache=O/f"profile_{j['group']}_{ep}.json"
    raw=(ROOT/j['raw_path']).read_bytes();sha=hashlib.sha256(raw).hexdigest()
    if cache.exists():
        p=read(cache);assert p['sha256']==sha
    else:
        r=json.loads(raw);assert r['info']['EpisodeId']==ep and r['statuses']==['DONE','DONE'] and len(r['steps'])==720
        assert r['info']['TeamNames'].count(j['name'])==1
        seat=r['info']['TeamNames'].index(j['name'])
        if j['group']=='V51C':
            prev=read(B/f'reports/v51_external_20260909/profile_{ep}.json')
            ledger=prev['candidate_ledger'];ss=prev['candidate'];bio=prev['biological_obligations']
        else:
            ledger=audit(r,seat);ss=slots(r,seat);bio=audit_obligations(r,seat)
        snaps=[snapshot(r,d,seat) for d in range(1,31)]
        ops=daily_operational_kpi(r,seat,ledger);daily=[]
        for d,(snap,op,sl,l) in enumerate(zip(snaps,ops,ss,ledger['daily'])):
            row=flatten(snap)|op
            row.update(day=d+1,PASS=sl['explicit_pass'],MOVE=sl['move'],slots=sl['slots'],pass_share=sl['explicit_pass']/sl['slots'],implicit_idle=sl['implicit_idle'],hire_cash=l['hire_cash'],sales_cash=sum(l['sales_cash'].values()),purchase_cash=sum(l['purchase_cash'].values()),land_cash=l['land_cash'],unit_cash_delta=l['unit_cash_delta'])
            row.update({k:l['executed_actions'].get(k,0) for k in ['WATER','FEED','CARE','HARVEST']})
            row.update({k:bio[d][k] for k in ['missed_feed','missed_useful_care','missed_critical_water','decay_lost_units','productive_water_loss_units']})
            daily.append(row)
        qs=[list(z['pasture_topology'].values()) for z in snaps]
        p=dict(**j,seat=seat,opponent=r['info']['TeamNames'][1-seat],sha256=sha,cash=r['rewards'][seat],opponent_cash=r['rewards'][1-seat],daily=daily,topology_daily=qs,topology_D15=qs[14],topology_D30=qs[29],checkpoints770=sum(q==[7,7,0,0] for q in qs[14:]),cash_discrepancies=ledger.get('cash_discrepancies',[]),net_cash_residual=ledger.get('net_cash_residual',0),biological_obligations=bio)
        dump(cache,p)
    catalog.append({k:v for k,v in p.items() if k not in ['daily','biological_obligations']})
    print(j['group'],ep,'verified',flush=True)
dump(O/'catalog.json',catalog)
print('DONE',flush=True)
