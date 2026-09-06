"""Original-engine E18.32 ablations. Frozen E18.31 remains the control."""
import argparse
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from docs.model_specs.codex.e18.tools import run_e18_30_mission_gate as gate
from docs.model_specs.codex.e18.tools.run_e18_31_assignment_gate import traced
from docs.model_specs.codex.e18.tools.e18_32_ready_work_controller import ReadyWorkController
from docs.model_specs.codex.e18.tools.e18_32_demand_routing_controller import DemandRoutingController
from docs.model_specs.codex.e18.tools.e18_32_claim_routing_controller import ClaimRoutingController
from docs.model_specs.codex.e18.tools.e18_32_reservation_routing_controller import ReservationRoutingController


def run_case(variant, opponent, seed, seat):
    original=gate.MissionRuntimeController
    cls=traced(ReservationRoutingController if variant=='RESERVED' else
               ClaimRoutingController if variant=='DEMAND_RELEASE' else
               DemandRoutingController if variant=='DEMAND' else ReadyWorkController)
    gate.MissionRuntimeController=lambda plan,seat,unused:cls(plan,seat,variant)
    try:
        result=gate.run_one('CROP_POOL',opponent,seed,seat)
        agent=cls.instance
        result.update(variant=variant,version='E18.32 '+variant,
                      focus_trace=agent.focus_trace,pass_reasons=[dict(c) for c in agent.pass_reasons],
                      ready_metrics=dict(agent.ready_metrics),assignment_metrics=dict(agent.assignment_metrics),
                      expansion_log=agent.expansion_log)
        result['routing_log']=getattr(agent,'routing_log',[])
        return result
    finally:
        gate.MissionRuntimeController=original


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--variants',nargs='+',default=['COMBINED'])
    p.add_argument('--opponents',nargs='+',choices=['E18.16','E18.2/V4D'],default=['E18.16'])
    p.add_argument('--seeds',nargs='+',type=int,default=[180903001])
    p.add_argument('--seats',nargs='+',type=int,default=[0,1])
    p.add_argument('--jobs',type=int,choices=[1,2],default=2)
    p.add_argument('--label',required=True)
    args=p.parse_args()
    assert set(args.seeds)<=set(range(180903001,180903008))
    assert args.label.replace('_','').isalnum()
    path=gate.DERIVED/f'E18_32_READY_WORK_GATE_{args.label}.json'
    assert not path.exists(),path
    sources=[Path(__file__),Path(__file__).with_name('e18_32_ready_work_controller.py'),
             Path(__file__).with_name('e18_32_demand_routing_controller.py')]
    sources.append(Path(__file__).with_name('e18_32_claim_routing_controller.py'))
    sources.append(Path(__file__).with_name('e18_32_reservation_routing_controller.py'))
    payload=dict(complete=False,holdout_consumed=False,matches=[],failures=[],
                 source_sha256={str(s):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources})
    cases=[(v,o,s,t) for v in args.variants for o in args.opponents for s in args.seeds for t in args.seats]
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        pending={pool.submit(run_case,*c):c for c in cases}
        for f in as_completed(pending):
            try:
                payload['matches'].append(f.result())
            except Exception as exc:
                payload['failures'].append(dict(case=pending[f],error=repr(exc)))
                print(repr(exc),flush=True)
            path.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    payload['complete']=not payload['failures'] and len(payload['matches'])==len(cases)
    path.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(path,flush=True)
    if not payload['complete']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
