"""Reproducible E20 development and independent round-robin matches."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
BASE = ROOT / 'docs/model_specs/codex/e20'
BUNDLES = {'E18': 'submission_codex_e18_2_capacity_governed_v4d.py',
           'E19': 'submission_codex_e18_770_v48_external.py',
           'E20': 'submission_codex_e20_772_e20v18_candidate.py',
           'E20.1': 'submission_codex_e20_772_e20v28_candidate.py',
           'C770': 'submission_codex_e20_1_control_770.py'}

def policy(name, seat):
    if name.startswith('E20v'):
        from docs.model_specs.codex.e20.tools.policy import create_agent
        return create_agent({'player_position': seat}, name)
    return runpy.run_path(str(ROOT / 'submission' / BUNDLES[name]))['create_agent']({'player_position': seat})

def run(case):
    stage, left, right, seed = case
    out = BASE / 'artifacts' / stage
    out.mkdir(parents=True, exist_ok=True)
    path = out / f'{left}_{right}_{seed}.json'
    if path.exists():
        return json.loads(path.read_text())
    from kaggle_environments import make
    agents = [policy(left, 0), policy(right, 1)]
    source_paths=[Path(__file__),ROOT/'submission'/BUNDLES['E18'],ROOT/'submission'/BUNDLES['E19']]
    for name in (left,right):
        if name in BUNDLES and name not in {'E18','E19'}:source_paths.append(ROOT/'submission'/BUNDLES[name])
    if left.startswith('E20') or right.startswith('E20'):
        source_paths += [Path(__file__).with_name('policy.py'),ROOT/'docs/model_specs/codex/e19/tools/biological_plan_770_v48.py',ROOT/'docs/model_specs/codex/e19/tools/daily_routes_770_v48.py']
    sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    durations = [[], []]
    def capture(i):
        def act(obs, cfg):
            start = time.perf_counter()
            result = agents[i](obs, cfg)
            durations[i].append(time.perf_counter()-start)
            return result
        return act
    env = make('kaggriculture', configuration=dict(episodeSteps=720, turnsPerDay=24, seed=seed), debug=False)
    env.run([capture(0), capture(1)])
    replay = env.toJSON()
    assert len(replay['steps']) == 720 and all(s['status']=='DONE' for s in replay['steps'][-1])
    opening = []
    for i, name in enumerate([left, right]):
        placements = []
        previous = {}
        for step in replay['steps']:
            obs = step[i]['observation']
            farm = obs['farms'][i]
            current = {(x,y):t for y,row in enumerate(farm['tiles']) for x,t in enumerate(row)
                       if isinstance(t,dict) and t.get('kind')=='PASTURE'}
            for pos,t in current.items():
                old = previous.get(pos,{})
                if pos not in previous or t.get('animal') != old.get('animal'):
                    placements.append(dict(day=obs['day']+1,hour=obs['hour']+1,position=pos,animal=t.get('animal')))
            previous = current
        counts = [sum((x<5 and y<5, x>=5 and y<5, x<5 and y>=5)[q] for x,y in previous) for q in range(3)]
        opening.append(dict(name=name,placements=placements,topology=counts))
    raw = json.dumps(replay,separators=(',',':')).encode()
    for i,agent in enumerate(agents):
        core=getattr(agent,'core',None)
        if core is not None:
            diagnostics=dict(routes=getattr(core,'daily_route_log',[]),
                plan=getattr(core,'biological_plan',{}),metrics=dict(getattr(core,'metrics',{})))
            with gzip.open(path.with_suffix(f'.seat{i}.diagnostics.json.gz'),'wt',encoding='utf-8') as f:
                json.dump(diagnostics,f,separators=(',',':'))
    with gzip.open(path.with_suffix('.replay.json.gz'),'wb') as f:f.write(raw)
    result = dict(stage=stage, agents=[left,right],seed=seed,rewards=replay['rewards'],opening=opening,
                  replay_sha256=hashlib.sha256(raw).hexdigest(),
                  sources=sources,
                  runtime=[dict(calls=len(d),max_seconds=max(d),overage_seconds=sum(max(0,t-1) for t in d),
                                core_errors=getattr(getattr(agents[i],'core',None),'error_count',None),
                                metrics=dict(getattr(getattr(agents[i],'core',None),'metrics',{}))) for i,d in enumerate(durations)])
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(agents=result['agents'],seed=seed,rewards=result['rewards'],topologies=[o['topology'] for o in opening])),flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--stage',default='development')
    p.add_argument('--models',nargs='+',default=['E19','E18'])
    p.add_argument('--seeds',nargs='+',type=int,default=[180903001])
    p.add_argument('--workers',type=int,default=2)
    p.add_argument('--screen',action='store_true',help='Only first model against subsequent controls, seat zero.')
    p.add_argument('--sweep',action='store_true',help='Each supplied model against E18, seat zero.')
    a=p.parse_args()
    if a.stage=='e20_1_confirmation':
        gate=json.loads((BASE/'artifacts/E20_1_DEVELOPMENT_GATE.json').read_text())
        assert gate['passed']
        assert hashlib.sha256((ROOT/'submission'/BUNDLES['E20.1']).read_bytes()).hexdigest()==gate['bundle_sha256']
        assert set(a.models)=={'E18','E19','E20.1'} and a.seeds==gate['holdout_seeds']
        assert not a.screen and not a.sweep
    if a.stage=='tournament':
        gate=json.loads((BASE/'artifacts/ECONOMIC_GATE.json').read_text())
        protocol=json.loads((BASE/'VALIDATION_PROTOCOL.json').read_text())
        assert gate['passed']
        assert hashlib.sha256((ROOT/'submission'/BUNDLES['E20']).read_bytes()).hexdigest()==gate['bundle_sha256']
        assert set(a.models)=={'E18','E19','E20'}
        assert a.seeds==protocol['tournament_seeds_reserved_before_results']
        assert not a.screen and not a.sweep
    cases=[(a.stage,x,y,s) for x in a.models for y in a.models if x!=y for s in a.seeds]
    if a.screen:cases=[(a.stage,a.models[0],y,s) for y in a.models[1:] for s in a.seeds]
    if a.sweep:cases=[(a.stage,x,'E18',s) for x in a.models for s in a.seeds]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:list(pool.map(run,cases))
