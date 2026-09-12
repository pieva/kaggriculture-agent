"""Rebuild controller memory and branch the engine; no cross-model state swaps."""
import argparse,copy,gzip,hashlib,json,runpy,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.verify_revision import observation_at

BASE=ROOT/'docs/model_specs/codex/e20';OUT=BASE/'artifacts/e20_2_care_floor'
SOURCE=ROOT/'docs/model_specs/codex/e20/artifacts/e20_1_confirmation'
BUNDLES={'E18':'submission_codex_e18_2_capacity_governed_v4d.py','E19':'submission_codex_e18_770_v48_external.py','E20.1':'submission_codex_e20_772_e20v28_loaderfix.py'}
def canonical(state):
    result=copy.deepcopy(state)
    for side in result:side['observation'].pop('remainingOverageTime',None)
    return result

def run(model,condition,seed,target):
    from kaggle_environments import make
    import kaggle_environments
    opponent='E18';names=[model,opponent] if target==0 else [opponent,model];stem=f'{names[0]}_{names[1]}_{seed}'
    source=SOURCE/(stem+'.json');meta=json.loads(source.read_text())
    with gzip.open(source.with_suffix('.replay.json.gz'),'rb') as f:raw=f.read()
    assert hashlib.sha256(raw).hexdigest()==meta['replay_sha256']
    replay=json.loads(raw);checkpoint=456
    assert replay['steps'][checkpoint][0]['observation']['day']==19 and replay['steps'][checkpoint][0]['observation']['hour']==0
    candidate=ROOT/'submission/submission_codex_e20_772_e20v32_candidate.py'
    baseline=ROOT/'submission/submission_codex_e20_772_e20v28_loaderfix.py'
    sources_for_agents=[baseline if n==model else ROOT/'submission'/BUNDLES[n] for n in names]
    if condition=='candidate':sources_for_agents[target]=candidate
    agents=[]
    for seat,path in enumerate(sources_for_agents):
        namespace={'__name__':'_e20_2_validation'}
        if seat==target and condition=='candidate':
            exec(compile(path.read_text(encoding='utf-8'),str(path),'exec'),namespace)
        else:namespace=runpy.run_path(str(path))
        agents.append(namespace['create_agent']({'player_position':seat}))
    calls=[0,0];max_seconds=[0.,0.]
    def act(seat,obs):
        start=time.perf_counter();value=agents[seat](obs,replay['configuration']);max_seconds[seat]=max(max_seconds[seat],time.perf_counter()-start);calls[seat]+=1
        return value
    for i in range(checkpoint):
        for seat in (0,1):assert act(seat,observation_at(replay,i,seat))==replay['steps'][i+1][seat]['action'],('prefix',model,i,seat)
    env=make('kaggriculture',configuration=copy.deepcopy(replay['configuration']),info=copy.deepcopy(replay['info']),steps=copy.deepcopy(replay['steps'][:checkpoint+1]))
    intervention=None;state_parity=0;action_parity=0
    for i in range(checkpoint,719):
        observations=[]
        for seat in (0,1):
            obs=copy.deepcopy(dict(env.state[seat]['observation']));obs.setdefault('step',env.state[0]['observation']['step']);observations.append(obs)
        actions=[act(seat,observations[seat]) for seat in (0,1)]
        if condition=='control':
            assert actions==[s['action'] for s in replay['steps'][i+1]],('suffix_action',model,i)
            action_parity+=1
        elif i==checkpoint:
            intervention=dict(step=i,day=20,hour=1,reason='care_floor_planning',target_seat=target)
        env.step(actions)
        if condition=='control' or intervention is None:
            assert canonical(env.state)==canonical(replay['steps'][i+1]),('suffix_state',model,i)
            state_parity+=1
    assert calls==[719,719] and env.done and all(s.status=='DONE' for s in env.state)
    errors=[getattr(getattr(a,'core',None),'error_count',None) for a in agents];assert errors[target]==0 and all(e in [0,None] for e in errors)
    out=env.toJSON();out['info']['branch_experiment']='E20.2-care-floor';encoded=json.dumps(out,separators=(',',':')).encode()
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/f'E20.2_{seed}_seat{target}_{condition}.json'
    with gzip.open(path.with_suffix('.replay.json.gz'),'wb') as f:f.write(encoded)
    engine=Path(kaggle_environments.__file__).parent/'envs/kaggriculture/kaggriculture.py'
    result=dict(experiment='E20.2-care-floor',condition=condition,agents=names,target_seat=target,seed=seed,rewards=out['rewards'],checkpoint=checkpoint,intervention=intervention,source_replay_sha256=meta['replay_sha256'],replay_sha256=hashlib.sha256(encoded).hexdigest(),runtime=[dict(calls=c,core_errors=e,max_seconds=t) for c,e,t in zip(calls,errors,max_seconds)],verification=dict(prefix_actions_per_agent=checkpoint,suffix_action_batches=action_parity,suffix_states=state_parity,clock_field_excluded='remainingOverageTime'),sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('policy.py'),BASE/'E20_2_PROTOCOL.md',*sources_for_agents]},engine=dict(version=kaggle_environments.__version__,sha256=hashlib.sha256(engine.read_bytes()).hexdigest()))
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(model=model,condition=condition,rewards=out['rewards'],verification=result['verification'])),flush=True)
if __name__=='__main__':
    for seed in [180910201,180910203]:
        for target in [0,1]:
            for condition in ['control','candidate']:
                print('START',seed,target,condition,flush=True)
                run('E20.1',condition,seed,target)
