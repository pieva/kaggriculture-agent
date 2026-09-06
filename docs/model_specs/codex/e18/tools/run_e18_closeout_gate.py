"""Detailed Q0 and autonomy diagnostics; current development seeds only."""
import argparse
import hashlib
import importlib
import json
import time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]

def run_case(case):
    policy,profile_path,opponent,seed,seat=case
    from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as gate
    from docs.model_specs.codex.e18.tools.audit_e18_32_q0_utilization import summarize_farm
    from docs.model_specs.codex.e18.tools.e18_33_common_controller import CommonController
    from docs.model_specs.codex.e18.tools.e18_32_claim_routing_controller import ClaimRoutingController
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    original_snapshot=gate.snapshot
    def detailed(replay,day,seat):
        row=original_snapshot(replay,day,seat)
        row['quadrants']=summarize_farm(replay['steps'][24*day-1][seat]['observation']['farms'][seat])
        return row
    gate.snapshot=detailed
    instances=[]
    timings=[]
    class Timed:
        def __init__(self,wrapped): self.wrapped=wrapped
        def __getattr__(self,key): return getattr(self.wrapped,key)
        def __call__(self,obs,cfg):
            start=time.perf_counter(); action=self.wrapped(obs,cfg)
            timings.append(time.perf_counter()-start)
            return action
    def make(plan,seat,unused):
        agent=(CommonController(json.loads(Path(profile_path).read_text()),engine.market_price,engine.MARKET_PARAMS,seat)
               if policy=='COMMON' else ClaimRoutingController(plan,seat,'DEMAND_RELEASE'))
        instances.append(agent)
        return Timed(agent)
    gate.MissionRuntimeController=make
    try:
        result=gate.run_one('CROP_POOL',opponent,seed,seat)
        a=instances[-1]
        result.update(version='E18.33 AUTONOMY PROBE' if policy=='COMMON' else 'E18.32 DEMAND RELEASE V9',
                      common_events=getattr(a,'events',[]),common_metrics=dict(getattr(a,'metrics',{})),
                      max_call_seconds=max(timings),mean_call_seconds=sum(timings)/len(timings))
        return result
    finally:
        gate.snapshot=original_snapshot

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--policy',choices=['COMMON','E18_32_V9'],default='COMMON')
    p.add_argument('--profile',type=Path,default=BASE/'configs/CODEX_E18_33_COMMON_RESOURCE_POLICY_V3_AUTONOMY.json')
    p.add_argument('--seeds',type=int,nargs='+',default=[180903001])
    p.add_argument('--seats',type=int,nargs='+',default=[0,1])
    p.add_argument('--opponents',nargs='+',choices=['E18.16','E18.2/V4D'],default=['E18.16','E18.2/V4D'])
    p.add_argument('--jobs',type=int,choices=[1,2],default=2)
    p.add_argument('--label',required=True)
    args=p.parse_args()
    assert set(args.seeds)<=set(range(180903001,180903008)) and set(args.seats)<={0,1}
    assert args.label.replace('_','').isalnum()
    profile=args.profile.resolve()
    assert profile.parent==(BASE/'configs').resolve()
    output=BASE/f'artifacts/derived/E18_CLOSEOUT_GATE_{args.label}.json'
    assert not output.exists()
    engine=importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    sources=[Path(__file__),Path(engine.__file__),profile,BASE/'tools/e18_33_common_controller.py',BASE/'tools/e18_33_common_policy.py',BASE/'tools/e18_32_claim_routing_controller.py']
    payload=dict(policy=args.policy,profile=str(profile),complete=False,holdout_consumed=False,e19_started=False,matches=[],failures=[],source_sha256={str(s):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources})
    cases=[(args.policy,str(profile),o,s,t) for o in args.opponents for s in args.seeds for t in args.seats]
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        pending={pool.submit(run_case,c):c for c in cases}
        for f in as_completed(pending):
            try: payload['matches'].append(f.result())
            except Exception as exc: payload['failures'].append(dict(case=pending[f],error=repr(exc)))
            output.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    payload['complete']=not payload['failures'] and len(payload['matches'])==len(cases)
    output.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(output,flush=True)
    if not payload['complete']: raise SystemExit(1)

if __name__=='__main__': main()
