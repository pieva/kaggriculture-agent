"""Offline counterfactual preparation; never dispatch the probed jobs."""
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import sys
from collections import Counter

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.pass_diagnostic_v49 import Diagnostic,closure
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v50'


def main():
    old=ROOT/'docs/model_specs/codex/e19/reports/v48_external_pass_update_20260908'
    entry=next(g for g in json.loads((old/'cohort.json').read_text())['games'] if g['episode']==106843637)
    raw=ROOT/entry['raw_path']
    if not raw.exists():raw=Path('C:/Users/pietr/Projects/kaggriculture-agent')/entry['raw_path']
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==entry['sha256']
    replay=json.loads(raw.read_text());seat=entry['seat']
    policy=runpy.run_path(str(ROOT/'submission/submission_codex_e18_770_v48_external.py'))['create_agent']({'player_position':seat})
    diagnostic=Diagnostic(policy);prepare=closure(diagnostic.route_prepare)['prepare']
    rows=[];mismatches=[]
    for i in range(1,720):
        obs=deepcopy(replay['steps'][i-1][seat]['observation']);obs.update(player=seat,step=i-1)
        action=diagnostic(obs,replay['configuration'])
        if action!=replay['steps'][i][seat]['action']:mismatches.append(i)
        core=policy.core
        if obs['day'] not in [11,12,13,14,28]:continue
        claims={tuple(j['target']) for j in core.active.values() if j['kind']!='DELIVER'}
        state=closure(diagnostic.route_prepare);queues=state['queues']
        for w,cmd in enumerate([action['farmer'],*action['hands']]):
            if cmd!=['PASS'] or w in core.active:continue
            for target,commands,priority,value,kind in diagnostic.offers:
                target=tuple(target)
                if target in claims or kind not in {'SERVICE','BIOLOGICAL'}:continue
                steps=prepare(w,target,commands,buy=False,requirements=core._requirements()[0])
                owners=[p for p,q in queues.items() if target in q]
                rows.append(dict(day=core.day+1,hour=core.hour+1,worker=w,target=target,
                    commands=commands,owners=owners,queue=deepcopy(queues.get(w,[])),
                    ungated_feasible=bool(steps),steps=steps,
                    carried=deepcopy(core.private['inventories'][w]),
                    owner_committed={p:len(core.active.get(p,{}).get('steps',[])) for p in owners}))
    assert not mismatches,mismatches
    OUT.mkdir(parents=True,exist_ok=True)
    (ROOT/'scratch/v50').mkdir(parents=True,exist_ok=True)
    detail=ROOT/'scratch/v50/route_probes.json.gz'
    with gzip.open(detail,'wt',encoding='utf-8') as f:json.dump(rows,f)
    result=dict(episode=entry['episode'],replay_sha256=entry['sha256'],actions=719,mismatches=mismatches,
        note='Preparation without route gate at the actual post-dispatch state; feasibility does not certify profitability or capacity of the full day.',
        detail=str(detail.relative_to(ROOT)),days=[])
    for day in [12,13,14,15,29]:
        r=[x for x in rows if x['day']==day];feasible=[x for x in r if x['ungated_feasible']]
        result['days'].append(dict(day=day,probes=len(r),feasible=len(feasible),
            pass_slots_with_feasible=len({(x['hour'],x['worker']) for x in feasible}),
            kinds=dict(Counter(','.join(c[0] for c in x['commands']) for x in feasible)),examples=feasible[:4]))
    (OUT/'route_causality.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
