"""Reconcile both players against engine and export the standard 22 KPI."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))

def run(path):
    path=Path(path)
    output=path.with_suffix('.kpi.json')
    if output.exists():return str(output)
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
    from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
    from docs.model_specs.codex.e18.tools.build_e18_27_top770_complete_kpi import flatten
    meta=json.loads(path.read_text())
    with gzip.open(path.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
    assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256']
    replay=json.loads(raw)
    sides=[]
    for seat,name in enumerate(meta['agents']):
        ledger=audit(replay,seat)
        daily=[snapshot(replay,d,seat) for d in range(1,31)]
        operations=daily_operational_kpi(replay,seat,ledger)
        kpi=[]
        for s,o,f in zip(daily,operations,ledger['daily']):
            row=flatten(s)|o
            row.update({k:f['executed_actions'].get(k,0) for k in ['WATER','FEED','CARE']})
            kpi.append(row)
        sides.append(dict(name=name,seat=seat,reward=meta['rewards'][seat],daily=daily,
                          ledger=ledger,operational_daily=operations,kpi=kpi,
                          terminal=end_state(replay,seat),crop_starvation=crop_service_audit(replay,seat)))
    output.write_text(json.dumps(dict(seed=meta['seed'],sides=sides,replay_sha256=meta['replay_sha256']),indent=2)+'\n')
    print(str(output),flush=True)
    return str(output)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage');p.add_argument('--workers',type=int,default=2);a=p.parse_args()
    paths=[str(p) for p in (ROOT/'docs/model_specs/codex/e20/artifacts'/a.stage).glob('*.json') if '.kpi.' not in p.name]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:list(pool.map(run,paths))
