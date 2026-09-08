"""Extend the frozen assisted 770 through D30 against the same V4D opponent."""
import hashlib
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e19/artifacts/derived/assisted_770_complete_20260907'
BUNDLE=ROOT/'submission/submission_codex_e18_770_assisted_start_v1_candidate.py'


def run(case):
    seed,seat=case
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import opponent_policy
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
    policy=runpy.run_path(str(BUNDLE))['create_agent']({'player_position':seat})
    opponent=opponent_policy('E18.2/V4D',seed,1-seat)
    durations=[]
    def capture(obs,cfg):
        start=time.perf_counter();action=policy(obs,cfg);durations.append(time.perf_counter()-start);return action
    env=make('kaggriculture',configuration=dict(episodeSteps=720,turnsPerDay=24,seed=seed),debug=False)
    env.run([capture,opponent] if seat==0 else [opponent,capture])
    replay=env.toJSON()
    assert len(replay['steps'])==720
    assert all(s['status']=='DONE' for s in replay['steps'][-1])
    prefix=json.loads((OUT.parent/'assisted_start_20260907'/f'770_{seed}_{seat}.json').read_text())
    actions=[s[seat]['action'] for s in replay['steps'][1:265]]
    assert hashlib.sha256(json.dumps(actions,sort_keys=True).encode()).hexdigest()==prefix['actions_sha256']
    sides={}
    for label,position in [('assisted',seat),('v4d',1-seat)]:
        sides[label]=dict(reward=replay['rewards'][position],daily=[snapshot(replay,d,position) for d in range(1,31)],
                          ledger=audit(replay,position),terminal=end_state(replay,position),crop_starvation=crop_service_audit(replay,position))
    from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
    for label,position in [('assisted',seat),('v4d',1-seat)]:
        sides[label]['operational_daily']=daily_operational_kpi(replay,position,sides[label]['ledger'])
    prior=json.loads((OUT.parent/'assisted_770_d30_20260907'/f'{seed}_{seat}.json').read_text())
    for label in sides:
        assert {k:v for k,v in sides[label].items() if k!='operational_daily'}==prior['sides'][label]
    policy.core.acknowledge_terminal(replay['steps'][-1][seat]['observation'])
    result=dict(seed=seed,seat=seat,opponent='E18.2/V4D',sides=sides,prefix_parity=True,
                core_errors=policy.core.error_count,incomplete_missions=policy.core.incomplete_missions,
                core_metrics=dict(policy.core.metrics),core_events=policy.core.events,
                max_call_seconds=max(durations),configuration=replay['configuration'],
                sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [BUNDLE,Path(__file__)]})
    (OUT/f'{seed}_{seat}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(seed=seed,seat=seat,cash=sides['assisted']['reward'],v4d=sides['v4d']['reward'],errors=result['core_errors'],incomplete=result['incomplete_missions'])),flush=True)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(s,t) for s in range(180903001,180903008) for t in (0,1) if not (OUT/f'{s}_{t}.json').exists()]
    with ProcessPoolExecutor(max_workers=2) as pool:list(pool.map(run,cases))
