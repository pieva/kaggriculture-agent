"""E19 real-engine gate from a frozen parametric bundle, with terminal diagnostics."""
import argparse
import hashlib
import json
import runpy
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def save(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    for attempt in range(5):
        try:
            temporary.replace(path)
            return
        except OSError:
            if attempt == 4: raise
            time.sleep(0.1*(attempt+1))


def run_case(case):
    bundle, opponent, seed, seat = case
    from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as gate
    module = runpy.run_path(bundle)
    policy = module['create_agent']({'player_position':seat})
    durations = []
    class Timed:
        def __getattr__(self,key): return getattr(policy,key)
        def __call__(self,obs,cfg):
            start = time.perf_counter()
            action = policy(obs,cfg)
            durations.append(time.perf_counter()-start)
            return action
    gate.MissionRuntimeController = lambda *args: Timed()
    result = gate.run_one('CROP_POOL',opponent,seed,seat)
    result.update(version=module['MODEL_VERSION'],common_events=policy.events,
        common_metrics=dict(policy.metrics),max_call_seconds=max(durations),
        overage_seconds=sum(max(0,t-1) for t in durations),
        mean_call_seconds=sum(durations)/len(durations),
        remaining_missions={str(w):job for w,job in policy.active.items()},
        final_positions=policy.positions,final_inventories=policy.private['inventories'])
    budgets = list(policy.profile.pasture_budgets(['NW','NE','SW','SE']).values())
    expected = {f'Q{i}':n for i,n in enumerate(budgets)}
    terminal = result['daily'][-1]
    result['expected_topology'] = expected
    result['exact_populated_topology'] = (terminal['pasture_topology']==expected and
        terminal['occupied_livestock_tiles']==policy.profile.target)
    result['safety_pass'] = (not result['crop_starvation'] and not result['ledger']['animal_escapes']
        and not result['ledger']['cash_parity_errors'] and not result['incomplete_missions']
        and result['max_hands']<=policy.profile.maximum_hands and result['max_resources']<=policy.profile.target
        and result['errors']==0 and all(s=='DONE' for s in result['statuses']))
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--bundle',type=Path,required=True)
    p.add_argument('--label',required=True)
    p.add_argument('--seeds',type=int,nargs='+',default=[180903001])
    p.add_argument('--seats',type=int,nargs='+',default=[0,1])
    p.add_argument('--opponents',nargs='+',default=['E18.16','E18.2/V4D'],choices=['E18.16','E18.2/V4D'])
    args=p.parse_args()
    assert set(args.seeds)<=set(range(180903001,180903008)) and set(args.seats)<={0,1}
    assert args.label.replace('_','').isalnum()
    output=BASE/f'artifacts/derived/E19_GATE_{args.label}.json'
    assert not output.exists()
    manifest=json.loads(args.bundle.with_suffix('.manifest.json').read_text())
    digest=hashlib.sha256(args.bundle.read_bytes()).hexdigest()
    assert digest==manifest['submission_sha256']
    report=dict(complete=False,e19_started=True,holdout_consumed=False,uploaded=False,
        bundle=str(args.bundle.resolve()),bundle_sha256=digest,core_sha256=manifest['core_sha256'],
        profile=manifest['profile'],runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),matches=[],failures=[])
    cases=[(str(args.bundle.resolve()),o,s,t) for o in args.opponents for s in args.seeds for t in args.seats]
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(run_case,c):c for c in cases}
        for f in as_completed(futures):
            try: report['matches'].append(f.result())
            except Exception as exc: report['failures'].append(dict(case=futures[f],error=repr(exc)))
            save(output,report)
    report['complete']=not report['failures'] and len(report['matches'])==len(cases)
    save(output,report)
    print(output,flush=True)
    if not report['complete']: raise SystemExit(1)


if __name__=='__main__': main()
