"""Reconstruct six historical V4C development trajectories; no new strategy."""
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

ROOT=Path(__file__).resolve().parents[5]
OUT=ROOT/'docs/model_specs/codex/e19/artifacts/derived/v4c_top770_20260907'

def run(case):
    seed,seat=case
    from kaggle_environments import make
    from agricola.core.benchmark_opponents import inert_pass_policy
    from agricola.core.observation_contract import stable_payload_hash
    from agricola.strategy.codex.codex_e17_batched_cluster_routing_v4 import create_codex_e17_batched_cluster_routing_v4,DEFAULT_V4C_CONFIG_PATH
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d20_trajectories import snapshot
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    context=dict(run_id=f'E17-ROUTING-V4-capacity_v4c-S{seed}-P{seat}',episode_id=f'E17-ROUTING-V4-capacity_v4c-S{seed}-P{seat}',seed=seed,player_position=seat)
    policy=create_codex_e17_batched_cluster_routing_v4(run_context=context,config_path=DEFAULT_V4C_CONFIG_PATH)
    actions=[]
    def capture(obs,cfg):
        a=policy(obs,cfg);actions.append(a);return a
    env=make('kaggriculture',configuration=dict(episodeSteps=720,turnsPerDay=24,seed=seed),debug=False)
    env.run([capture,inert_pass_policy] if seat==0 else [inert_pass_policy,capture])
    replay=env.toJSON()
    prior=json.loads((ROOT/'docs/model_specs/codex/e17/artifacts/derived/E17_2_CAPACITY_AWARE_BATCHED_ROUTING_V4C_DEVELOPMENT_METRICS.json').read_text())
    expected=next(r for r in prior['results'] if r['seed']==seed and r['seat']==seat and r['policy']=='capacity_v4c')
    action_hash=stable_payload_hash(actions)
    assert action_hash==expected['action_stream_sha256']
    assert replay['rewards'][seat]==expected['reward']
    assert all(r['status']=='DONE' for r in replay['steps'][-1])
    assert policy.codex_e17_batched_cluster_routing_instance.error_count==0
    data=dict(identity='E17.2 V4C',seed=seed,seat=seat,opponent='INERT_PASS',historical_parity=True,
        actions_sha256=action_hash,reward=replay['rewards'][seat],daily=[snapshot(replay,d,seat) for d in range(1,31)],
        ledger=audit(replay,seat),terminal=end_state(replay,seat))
    (OUT/f'{seed}_{seat}.json').write_text(json.dumps(data,indent=2)+'\n')
    print(seed,seat,data['reward'],'parity PASS',flush=True)

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    assert not list(OUT.glob('*.json'))
    with ProcessPoolExecutor(max_workers=2) as pool:
        list(pool.map(run,[(s,t) for s in [26090101,26090102,26090103] for t in [0,1]]))
