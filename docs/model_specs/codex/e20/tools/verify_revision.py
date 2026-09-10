"""Verify opening parity, intraday caps and provenance for a revision cohort."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import runpy
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
BASE=ROOT/'docs/model_specs/codex/e20'

def read_replay(path):
    with gzip.open(path,'rb') as f:raw=f.read()
    return json.loads(raw),hashlib.sha256(raw).hexdigest()

def observation_at(replay,index,seat):
    # Kaggle serializes the shared step only on seat zero; the live agent receives it in both seats.
    observation=dict(replay['steps'][index][seat]['observation'])
    observation.setdefault('step',replay['steps'][index][0]['observation']['step'])
    assert observation['step']==observation['day']*replay['configuration'].get('turnsPerDay',24)+observation['hour']
    return observation

def verify(stage,model,bundle=None,parity_seeds=None):
    cases=[]
    output=BASE/f'reports/e20_1/verification_{stage}_{model}.json'
    previous=json.loads(output.read_text()) if output.exists() else {}
    bundle_sha=hashlib.sha256(bundle.read_bytes()).hexdigest() if bundle else None
    cached={(c['replay_sha256'],c['seat']) for c in previous.get('cases',[]) if c.get('bundle_action_parity')==719}
    if previous.get('bundle_sha256')!=bundle_sha:cached=set()
    for path in sorted((BASE/'artifacts'/stage).glob('*.json')):
        if '.kpi.' in path.name:continue
        meta=json.loads(path.read_text())
        if model not in meta['agents']:continue
        seat=meta['agents'].index(model)
        replay,sha=read_replay(path.with_suffix('.replay.json.gz'))
        assert sha==meta['replay_sha256']
        assert len(replay['steps'])==720 and all(s['status']=='DONE' for s in replay['steps'][-1])
        assert meta['runtime'][seat]['calls']==719 and meta['runtime'][seat]['core_errors']==0
        seed=meta['seed']
        references=[]
        for folder in ['tournament','baseline','validation','e20_1_baseline','e20_1_confirmation']:
            for name in (f'E19_E18_{seed}',f'E18_E19_{seed}',f'E20_E18_{seed}',f'E18_E20_{seed}'):
                p=BASE/'artifacts'/folder/(name+'.replay.json.gz')
                if p.exists() and ((name.startswith('E18_'))==(seat==1)):references.append(p)
        opening_parity=None
        if meta['agents'][1-seat]=='E18':
            assert references,('Missing reference opening',seed,seat)
            reference,_=read_replay(references[0])
            assert [s[seat]['action'] for s in replay['steps'][1:265]]==[s[seat]['action'] for s in reference['steps'][1:265]]
            opening_parity=264
        for step in replay['steps']:
            farm=step[seat]['observation']['farms'][seat]
            counts=[0,0,0,0]
            for y,row in enumerate(farm['tiles']):
                for x,t in enumerate(row):
                    if isinstance(t,dict) and t.get('kind')=='PASTURE':counts[(x>=5)+2*(y>=5)]+=1
            caps=[7,7,0,0] if model=='C770' else [7,7,2,0]
            assert all(n<=cap for n,cap in zip(counts,caps)),(path,counts)
        parity=None
        if bundle and (parity_seeds is None or seed in parity_seeds):
            if (sha,seat) not in cached:
                p=runpy.run_path(str(bundle))['create_agent']({'player_position':seat})
                for index in range(1,720):
                    action=p(observation_at(replay,index-1,seat),replay['configuration'])
                    assert action==replay['steps'][index][seat]['action'],(path,index,'bundle mismatch')
            parity=719
        cases.append(dict(file=str(path.relative_to(ROOT)),seed=seed,seat=seat,
            replay_sha256=sha,opening_parity=opening_parity,all_intraday_caps=True,final_topology=counts,
            bundle_action_parity=parity,core_errors=0))
    assert cases
    result=dict(stage=stage,model=model,cases=cases,passed=True,
        bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest() if bundle else None)
    out=BASE/'reports/e20_1';out.mkdir(parents=True,exist_ok=True)
    (out/f'verification_{stage}_{model}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(stage=stage,model=model,passed=True,cases=len(cases),bundle_action_parity=bool(bundle))))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage');p.add_argument('model');p.add_argument('--bundle',type=Path);p.add_argument('--parity-seeds',nargs='+',type=int);a=p.parse_args();verify(a.stage,a.model,a.bundle,a.parity_seeds)
