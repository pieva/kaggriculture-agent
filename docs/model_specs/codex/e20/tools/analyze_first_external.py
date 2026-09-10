"""Standard audited 22 KPI for both sides of the frozen external cohort."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.acquire_first_external import OUT
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten

def profile(r,seat):
    ledger=audit(r,seat)
    assert ledger['cash_parity_errors']==0
    daily=[snapshot(r,d,seat) for d in range(1,31)]
    op=daily_operational_kpi(r,seat,ledger)
    kpi=[]
    for s,o,f in zip(daily,op,ledger['daily']):
        row=flatten(s)|o
        row.update({k:f['requested_actions'].get(k,0) for k in ['MOVE','PASS']})
        row.update({k:f['executed_actions'].get(k,0) for k in ['WATER','FEED','CARE']})
        kpi.append(row)
    return dict(seat=seat,reward=r['rewards'][seat],daily=daily,operational_daily=op,kpi=kpi,
                ledger=ledger,terminal=end_state(r,seat),crop_starvation=crop_service_audit(r,seat))

if __name__=='__main__':
    c=json.loads((OUT/'cohort.json').read_text(encoding='utf-8'))
    for g in c['games']:
        p=OUT/f"profile_{g['episode']}.json"
        if p.exists():continue
        raw=(ROOT/g['raw_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==g['sha256']
        r=json.loads(raw);assert r['statuses']==['DONE','DONE'] and len(r['steps'])==720
        result=dict(g,sides=[profile(r,s) for s in range(2)])
        p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(g['episode'],flush=True)
