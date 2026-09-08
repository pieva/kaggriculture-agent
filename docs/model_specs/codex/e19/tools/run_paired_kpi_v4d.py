"""Reproduce frozen matches and measure BOTH farms, including Q0 initialization."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import importlib
import json
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/artifacts/derived/paired_kpi_v4d_20260907'
BUNDLES={'770':'submission_codex_e19_control_770_v2.py','662':'submission_codex_e19_1_662_v2.py'}
GATES={'770':'E19_GATE_CONTROL_770_V2_20260907.json','662':'E19_GATE_V2_DEVELOPMENT_20260907.json'}

def digest(data): return hashlib.sha256(data).hexdigest()

def detail(obs,seat):
    farm=obs['farms'][seat]; private=obs['private']
    q=[]
    for y,row in enumerate(farm['tiles'][:5]):
        q.extend((x,y,t) for x,t in enumerate(row[:5]))
    tiles=[t for x,y,t in q if isinstance(t,dict)]
    crops=Counter(t['crop'] for t in tiles if t.get('crop'))
    animals=Counter(t['animal'] for t in tiles if t.get('animal'))
    carried=sum((Counter(i) for i in private['inventories']),Counter())
    all_tiles=[t for row in farm['tiles'] for t in row if isinstance(t,dict)]
    return dict(q0_crops=dict(crops),q0_animals=dict(animals),
        q0_crop_tiles=sum(crops.values()),q0_animals_total=sum(animals.values()),
        q0_pastures=sum(t.get('kind')=='PASTURE' for t in tiles),
        q0_grid=[[t.get('animal') or t.get('crop') or t.get('kind','EMPTY') if isinstance(t,dict) else t or 'EMPTY'
                  for t in row[:5]] for row in farm['tiles'][:5]],
        unfed=sum(bool(t.get('animal')) and not t.get('fed_today',False) for t in all_tiles),
        uncared=sum(bool(t.get('animal')) and not t.get('cared_today',False) for t in all_tiles),
        shed=dict(private['shed']),carried=dict(carried),seeds=dict(private['seeds']))

def run_case(case):
    topology,seed,seat=case
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import opponent_policy
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    from docs.model_specs.codex.e18.tools.e18_29_crop_service_audit import crop_service_audit
    from experiments.e18.tools.common.replay_daily_operational_kpi import daily_operational_kpi
    bundle=ROOT/'submission'/BUNDLES[topology]
    candidate=runpy.run_path(str(bundle))['create_agent']({'player_position':seat})
    champion=opponent_policy('E18.2/V4D',seed,1-seat)
    env=make('kaggriculture',configuration={'episodeSteps':720,'turnsPerDay':24,'seed':seed},debug=False)
    env.run([candidate,champion] if seat==0 else [champion,candidate])
    replay=env.toJSON()
    assert len(replay['steps'])==720
    assert all(s['status']=='DONE' for s in replay['steps'][-1])
    actions=[s[seat]['action'] for s in replay['steps'][1:]]
    action_hash=digest(json.dumps(actions,sort_keys=True).encode())
    old=json.loads((OUT.parent/GATES[topology]).read_text())
    expected=next(m for m in old['matches'] if m['seed']==seed and m['seat']==seat and m['opponent']=='E18.2/V4D')
    assert action_hash==expected['actions_sha256']
    assert list(replay['rewards'])==([expected['reward'],expected['opponent_reward']] if seat==0 else [expected['opponent_reward'],expected['reward']])
    sides={}
    for label,position in [('parametric',seat),('v4d',1-seat)]:
        ledger=audit(replay,position)
        daily=[]
        for day in range(1,31):
            snap=snapshot(replay,day,position)
            snap.update(detail(replay['steps'][day*24-1][position]['observation'],position))
            daily.append(snap)
        early=[]
        for index in (0,6,12,18,23,47,71,95,119,143,167,191,215,239):
            obs=replay['steps'][index][position]['observation'];farm=obs['farms'][position]
            early.append(dict(step=index,day=obs['day']+1,hour=obs['hour']+1,
                money=farm['money'],hands=len(farm['hands']),**detail(obs,position)))
        sides[label]=dict(seat=position,reward=replay['rewards'][position],daily=daily,early=early,
            ledger=ledger,operational_daily=daily_operational_kpi(replay,position,ledger),
            terminal=end_state(replay,position),crop_starvation=crop_service_audit(replay,position))
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    data=dict(topology=topology,seed=seed,seat=seat,complete=True,reproduces_frozen_gate=True,
        actions_sha256=action_hash,bundle_sha256=digest(bundle.read_bytes()),
        champion_sha256=digest((ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py').read_bytes()),
        engine_sha256=digest(Path(engine.__file__).read_bytes()),configuration=replay['configuration'],sides=sides)
    path=OUT/f'{topology}_{seed}_{seat}.json'
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(topology=topology,seed=seed,seat=seat,parity=True,
        cash=sides['parametric']['reward'],champion_cash=sides['v4d']['reward'])),flush=True)
    return str(path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--topology',choices=BUNDLES,required=True);a=p.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[(a.topology,s,t) for s in range(180903001,180903008) for t in (0,1)]
    assert not any((OUT/f'{top}_{s}_{t}.json').exists() for top,s,t in cases)
    failures=[]
    with ProcessPoolExecutor(max_workers=2) as pool:
        for f in as_completed([pool.submit(run_case,c) for c in cases]):
            try:f.result()
            except Exception as e:failures.append(repr(e));print(repr(e),flush=True)
    if failures:raise RuntimeError(failures)

if __name__=='__main__':main()
