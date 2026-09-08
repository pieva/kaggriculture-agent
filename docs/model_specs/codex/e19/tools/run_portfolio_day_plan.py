"""Diagnostic CARE-value ablation on the frozen assisted 770; not a release."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
BASE=ROOT/'docs/model_specs/codex/e19'
OUT=BASE/'artifacts/derived/portfolio_succession_20260907'
BUNDLE=ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'


def install_care_value(core):
    original=core._services
    def services():
        result=[]
        for target,commands,priority,value,kind in original():
            tile=core._tile(target)
            if ['CARE'] in commands:
                # Each fed CARE adds one pending unit AFTER the next refresh's
                # production. Price is an observed spot proxy, not booked cash.
                species=tile['animal']
                product='MILK' if species=='COW' else 'WOOL'
                interval=2 if species=='COW' else 3
                first=8 if species=='COW' else 6
                next_income=next((d for d in range(core.day+2,core.final_day+1)
                                  if d-tile['placed_day']>=first and
                                  (d-tile['placed_day']-first)%interval==0),None)
                if next_income is not None:
                    # A saturated pending bonus is not credited again. Harvest
                    # of held product is assumed feasible, not guaranteed.
                    if tile.get('pending_care_bonus',0)<5:
                        value+=core._quote(product,'SELL',1)/(next_income-core.day)
            result.append((target,commands,priority,value,kind))
        return result
    core._services=services


def run(case):
    variant,seed,seat=case
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import opponent_policy
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
    policy=runpy.run_path(str(BUNDLE))['create_agent']({'player_position':seat})
    from docs.model_specs.codex.e19.tools.portfolio_day_plan import install
    install(policy.core)
    opponent=opponent_policy('E18.2/V4D',seed,1-seat)
    trace=[]
    exceptions=[]
    def capture(obs,cfg):
        before=Counter(policy.core.metrics)
        try:
            a=policy(obs,cfg)
        except Exception as exc:
            exceptions.append(repr(exc))
            raise
        if False:  # Metrics and actions are audited from the replay below.
            c=policy.core
            tiles=[t for row in c.farm['tiles'] for t in row if isinstance(t,dict)]
            services=c._services()
            trace.append(dict(day=obs['day']+1,hour=obs['hour']+1,cash=c.farm['money'],
                hands=len(c.farm['hands']),positions=deepcopy(c.positions),
                inventories=deepcopy(c.private['inventories']),shed=dict(c.private['shed']),
                maintenance_floor=c.maintenance_floor,feed_reserve=c.feed_reserve,
                crops=dict(Counter(t['crop'] for t in tiles if t.get('crop'))),
                animals=[dict(position=[x,y],**t) for y,row in enumerate(c.farm['tiles']) for x,t in enumerate(row) if isinstance(t,dict) and t.get('animal')],
                active=deepcopy(c.active),commands=a,
                unclaimed_services=[dict(target=t,commands=cmd,priority=p,value=v) for t,cmd,p,v,k in services],
                metric_delta=dict(Counter(c.metrics)-before)))
        if obs['day']>=11 and obs['hour'] in [0,6,12,18]:
            trace.append(dict(day=obs['day']+1,hour=obs['hour']+1,plan=deepcopy(policy.core.portfolio_latest),governance=deepcopy(policy.core.portfolio_governance)))
        return a
    env=make('kaggriculture',configuration=dict(episodeSteps=720,turnsPerDay=24,seed=seed),debug=False)
    env.run([capture,opponent] if seat==0 else [opponent,capture])
    replay=env.toJSON()
    assert not exceptions, exceptions[:3]
    assert len(replay['steps'])==720 and all(s['status']=='DONE' for s in replay['steps'][-1])
    prefix=json.loads((BASE/'artifacts/derived/assisted_start_20260907'/f'770_{seed}_{seat}.json').read_text())
    phash=hashlib.sha256(json.dumps([s[seat]['action'] for s in replay['steps'][1:265]],sort_keys=True).encode()).hexdigest()
    assert phash==prefix['actions_sha256']
    sides={}
    for label,pos in [('candidate',seat),('v4d',1-seat)]:
        sides[label]=dict(reward=replay['rewards'][pos],daily=[snapshot(replay,d,pos) for d in range(1,31)],
                          ledger=audit(replay,pos),terminal=end_state(replay,pos),crop_starvation=crop_service_audit(replay,pos))
    if variant=='baseline':
        old=json.loads((BASE/'artifacts/derived/assisted_770_d30_20260907'/f'{seed}_{seat}.json').read_text())
        assert sides['candidate']==old['sides']['assisted']
        assert sides['v4d']==old['sides']['v4d']
    from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
    for label,pos in [('candidate',seat),('v4d',1-seat)]:
        sides[label]['operational_daily']=daily_operational_kpi(replay,pos,sides[label]['ledger'])
    policy.core.acknowledge_terminal(replay['steps'][-1][seat]['observation'])
    result=dict(variant=variant,seed=seed,seat=seat,prefix_parity=True,sides=sides,trace=trace,
                errors=policy.core.error_count,incomplete=policy.core.incomplete_missions,metrics=dict(policy.core.metrics),
                sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [BUNDLE,Path(__file__),Path(__file__).with_name('productive_continuity.py'),Path(__file__).with_name('wheat_continuity.py'),Path(__file__).with_name('wheat_safe_continuity.py'),Path(__file__).with_name('wheat_reserved_continuity.py'),Path(__file__).with_name('portfolio_succession.py'),Path(__file__).with_name('portfolio_execution.py'),Path(__file__).with_name('portfolio_execution_v3.py'),Path(__file__).with_name('portfolio_succession_v3.py'),Path(__file__).with_name('portfolio_execution_v4.py'),Path(__file__).with_name('portfolio_succession_v4.py'),Path(__file__).with_name('portfolio_execution_v5.py'),Path(__file__).with_name('portfolio_succession_v5.py'),Path(__file__).with_name('portfolio_execution_v6.py'),Path(__file__).with_name('portfolio_succession_v6.py'),Path(__file__).with_name('portfolio_execution_v7.py'),Path(__file__).with_name('portfolio_succession_v7.py'),Path(__file__).with_name('portfolio_governed.py'),Path(__file__).with_name('portfolio_batched.py'),Path(__file__).with_name('portfolio_concurrent.py'),*[Path(__file__).with_name(n+'.py') for n in ['portfolio_succession_v10','portfolio_execution_v10','portfolio_governed_v10','portfolio_batched_v10','portfolio_concurrent_v10','portfolio_logistics','portfolio_day_plan']],ROOT/'submission/submission_codex_e19_control_770_v2.py']})
    (OUT/f'{variant}_{seed}_{seat}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(variant=variant,seed=seed,seat=seat,cash=sides['candidate']['reward'],reference=sides['v4d']['reward'],errors=result['errors'],incomplete=result['incomplete'])),flush=True)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[('portfolio_v12',s,t) for s in range(180903001,180903004) for t in (0,1)]
    with ProcessPoolExecutor(max_workers=2) as pool:list(pool.map(run,cases))
