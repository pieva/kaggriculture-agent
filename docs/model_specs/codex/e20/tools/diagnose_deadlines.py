"""Replay one frozen observation sequence, recording real scheduler decisions."""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.policy import create_agent
from docs.model_specs.codex.e20.tools.verify_revision import observation_at

def diagnose(path,variant,seat,output):
    with gzip.open(path,'rt',encoding='utf-8') as f:replay=json.load(f)
    policy=create_agent({'player_position':seat},variant)
    core=policy.core
    prepare,certificate=core._prepare_steps,core._day_route_certificate
    events=[]
    def record(kind,worker,target,commands,result):
        tile=core._tile(target)
        if not (isinstance(tile,dict) and tile.get('kind')=='PLANT'
                and tile.get('consecutive_unwatered',0)>=1 and not tile.get('watered_today')
                and any(c[0]=='WATER' for c in commands)):return
        queues=getattr(core,'daily_route_state',{}).get('remaining',{})
        owner=next((w for w,q in queues.items() if list(target) in [list(p) for p in q]),None)
        events.append(dict(day=core.day+1,hour=core.hour+1,kind=kind,worker=worker,
            position=list(core.positions[worker]),target=list(target),crop=tile['crop'],
            commands=commands,result=result,remaining=core.remaining,route_owner=owner,
            queue=queues.get(str(worker),[])))
    def traced_prepare(worker,target,commands,**kwargs):
        steps=prepare(worker,target,commands,**kwargs)
        record('prepare',worker,target,commands,None if steps is None else len(steps))
        return steps
    def traced_certificate(worker,job,services=None):
        accepted=certificate(worker,job,services)
        record('certificate',worker,job['target'],[cmd for cmd,pos in job['steps']],accepted)
        return accepted
    core._prepare_steps=traced_prepare
    core._day_route_certificate=traced_certificate
    for index in range(1,len(replay['steps'])):
        obs=observation_at(replay,index-1,seat)
        action=policy(obs,replay['configuration'])
        assert action==replay['steps'][index][seat]['action'],(index,'instrumentation changed action')
    summary=Counter((e['kind'],str(e['result'])) for e in events)
    payload=dict(variant=variant,seat=seat,source_replay=str(path),action_parity=719,
        counts={str(k):v for k,v in summary.items()},events=events,
        routes=core.daily_route_log,metrics=dict(core.metrics))
    output.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(output,'wt',encoding='utf-8') as f:json.dump(payload,f)
    print(json.dumps(payload['counts']))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('replay',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--variant',default='E20v18');p.add_argument('--seat',type=int,default=0)
    a=p.parse_args();diagnose(a.replay,a.variant,a.seat,a.output)
