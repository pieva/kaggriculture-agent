"""Paired local experiment, independent of frozen historical run directories."""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v50'


def run(variant, seed, seat, split, telemetry=True):
    from kaggle_environments import make
    from docs.model_specs.codex.e19.tools.pass_diagnostic_v49 import Diagnostic, summary
    from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import opponent_policy
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit
    from docs.model_specs.codex.e19.tools.crop_lifecycle_audit_v48 import crop_service_audit
    bundle=ROOT/'submission/submission_codex_e19_770_v49f_candidate.py'
    policy=runpy.run_path(str(bundle))['create_agent']({'player_position':seat})
    if variant=='v50a':
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50 import install
        install(policy.core)
    elif variant=='v50b':
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50b import install
        install(policy.core)
    elif variant=='v50c':
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50c import install
        install(policy.core)
    elif variant=='v50d':
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50d import install
        install(policy.core)
    elif variant=='v50e':
        from docs.model_specs.codex.e19.tools.input_routes_v50 import install
        install(policy.core)
    elif variant=='v50f':
        from docs.model_specs.codex.e19.tools.input_routes_v50 import install
        install(policy.core)
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50d import install
        install(policy.core)
    elif variant=='v50g':
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50g import install
        install(policy.core)
    elif variant=='v50h':
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50h import install
        install(policy.core)
    elif variant=='v50i':
        from docs.model_specs.codex.e19.tools.optional_fertilizer_v50 import install
        install(policy.core)
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50h import install
        install(policy.core)
    elif variant=='v50j':
        from docs.model_specs.codex.e19.tools.input_routes_v50 import install
        install(policy.core)
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50h import install
        install(policy.core)
    elif variant=='v50k':
        from docs.model_specs.codex.e19.tools.optional_fertilizer_v50 import install
        install(policy.core)
        from docs.model_specs.codex.e19.tools.input_routes_v50 import install
        install(policy.core)
        from docs.model_specs.codex.e19.tools.workforce_certificate_v50h import install
        install(policy.core)
    instrument=Diagnostic(policy) if telemetry else policy
    durations=[];exceptions=[]
    def capture(obs,cfg):
        start=time.perf_counter()
        try:result=instrument(obs,cfg)
        except Exception as exc:
            exceptions.append(repr(exc));raise
        durations.append(time.perf_counter()-start)
        return result
    opponent=opponent_policy('E18.2/V4D',seed,1-seat)
    env=make('kaggriculture',configuration=dict(seed=seed,episodeSteps=720,turnsPerDay=24,actTimeout=120),debug=False)
    env.run([capture,opponent] if seat==0 else [opponent,capture])
    replay=env.toJSON()
    invalid=[dict(step=i,status=s[seat]['status'],missing_action=s[seat].get('action') is None)
        for i,s in enumerate(replay['steps'][1:],1)
        if s[seat].get('action') is None or s[seat]['status'] not in ['ACTIVE','DONE']]
    if exceptions or invalid:
        failure=ROOT/'scratch/v50'/f'failure_{split}_{variant}_{seed}_{seat}.json.gz'
        with gzip.open(failure,'wt',encoding='utf-8') as f:json.dump(replay,f)
    assert not invalid,invalid[:5]
    assert not exceptions,exceptions
    assert len(replay['steps'])==720 and replay['statuses']==['DONE','DONE'],replay['statuses']
    ledger=audit(replay,seat)
    assert ledger['cash_parity_errors']==0
    losses=crop_service_audit(replay,seat)
    days=[]
    for day in range(30):
        count=Counter();slots=0
        for i in range(1,len(replay['steps'])):
            obs=replay['steps'][i-1][seat]['observation']
            if obs['day']!=day:continue
            n=1+len(obs['farms'][seat]['hands']);slots+=n
            a=replay['steps'][i][seat]['action']
            count.update(c[0] for c in [a['farmer'],*a['hands']][:n])
        l=ledger['daily'][day]
        state=replay['steps'][min(24*(day+1)-1,719)][seat]['observation']['farms'][seat]
        tiles=[t for row in state['tiles'] for t in row if isinstance(t,dict)]
        days.append(dict(day=day+1,slots=slots,pass_count=count['PASS'],
            move=sum(count[x] for x in ['NORTH','SOUTH','EAST','WEST']),
            cash=state['money'],requested=dict(count),executed=l['executed_actions'],
            hire_cash=l['hire_cash'],animals=sum(bool(t.get('animal')) for t in tiles),
            crops=sum(t.get('kind')=='PLANT' for t in tiles)))
    OUT.mkdir(parents=True,exist_ok=True)
    name=f'{split}_{variant}_{seed}_{seat}'
    details=ROOT/'scratch/v50'/f'{name}.json.gz'
    with gzip.open(details,'wt',encoding='utf-8') as f:
        json.dump(dict(replay=replay,passes=instrument.rows if telemetry else [],routes=policy.core.daily_route_log),f)
    policy.core.acknowledge_terminal(replay['steps'][-1][seat]['observation'])
    result=dict(variant=variant,seed=seed,seat=seat,split=split,opponent='V4D exposed internal control',
        reward=replay['rewards'][seat],opponent_reward=replay['rewards'][1-seat],
        baseline_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest(),
        candidate_sources={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
            for name in ['local_service_770_v49.py','workload_770_v49.py']} if variant=='v49' else {},
        actions_sha256=hashlib.sha256(json.dumps([s[seat]['action'] for s in replay['steps'][1:]],sort_keys=True).encode()).hexdigest(),
        daily=days,pass_diagnostic=summary(instrument.rows) if telemetry else None,losses=losses,
        metrics=dict(policy.core.metrics),errors=policy.core.error_count,
        incomplete=policy.core.incomplete_missions,ledger=ledger,
        runtime=dict(telemetry=telemetry,configured_act_timeout=120,calls=len(durations),max_seconds=max(durations),overage=sum(max(0,t-1) for t in durations)),
        recoveries=getattr(policy.core,'v49_recovery_log',[]),
        details=str(details.relative_to(ROOT)))
    result['staffing']=getattr(policy.core,'v50_staffing_log',[])
    result['input_routes']=getattr(policy.core,'v50_route_log',[])
    result['candidate_sources']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['workforce_certificate_v50.py','workforce_certificate_v50b.py','workforce_certificate_v50c.py','workforce_certificate_v50d.py','closed_routes_v50.py','supplied_routes_v50.py']} if variant.startswith('v50') else {}
    if variant=='v50e':result['candidate_sources']={'input_routes_v50.py':hashlib.sha256((Path(__file__).parent/'input_routes_v50.py').read_bytes()).hexdigest()}
    if variant=='v50f':result['candidate_sources']['input_routes_v50.py']=hashlib.sha256((Path(__file__).parent/'input_routes_v50.py').read_bytes()).hexdigest()
    if variant=='v50g':result['candidate_sources']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['workforce_certificate_v50g.py','workforce_certificate_v50.py','input_routes_v50.py']}
    if variant=='v50h':result['candidate_sources']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['workforce_certificate_v50h.py','workforce_certificate_v50.py','input_routes_v50.py']}
    if variant=='v50i':result['candidate_sources']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['workforce_certificate_v50h.py','workforce_certificate_v50.py','input_routes_v50.py','optional_fertilizer_v50.py']}
    if variant=='v50j':result['candidate_sources']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['workforce_certificate_v50h.py','workforce_certificate_v50.py','input_routes_v50.py']}
    if variant=='v50k':result['candidate_sources']={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['workforce_certificate_v50h.py','workforce_certificate_v50.py','input_routes_v50.py','optional_fertilizer_v50.py']}
    (OUT/f'{name}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ['variant','seed','seat','reward','errors','incomplete','runtime','staffing']})+f" PASS={sum(d['pass_count'] for d in days)} MOVE={sum(d['move'] for d in days)}",flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--variant',choices=['v49f','v50a','v50b','v50c','v50d','v50e','v50f','v50g','v50h','v50i','v50j','v50k'],default='v50k')
    p.add_argument('--seed',type=int,default=180903003);p.add_argument('--seat',type=int,default=0)
    p.add_argument('--split',default='development')
    a=p.parse_args();run(a.variant,a.seed,a.seat,a.split,False)
