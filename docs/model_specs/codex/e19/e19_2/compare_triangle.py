"""Three frozen candidates, pairwise serial comparisons; reuse verified V53/E22."""
import gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT));HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    version=sys.argv[1];assert version in ['v52a','v52b','v52c','v52d']
    out=HERE/'reports'/('triangle_'+version);art=HERE/'artifacts'/('triangle_'+version)
    out.mkdir(parents=True,exist_ok=True);art.mkdir(parents=True,exist_ok=True)
    originals={'E19.2':ROOT/f'submission/archive/e19_rejected/submission_codex_e19_2_770_{version}.py','E19.3':ROOT/'submission/archive/e19_rejected/submission_codex_e19_3_770_v53_fixes.py','E22':ROOT/'submission/submission_codex_e22_s56165462_observed_v1.py'}
    old=json.loads((HERE/'reports/v53/PROTOCOL.json').read_text(encoding='utf-8'))
    for name in ['E19.3','E22']:assert old['hashes'][str(originals[name].relative_to(ROOT))]==digest(originals[name])
    protocol=dict(version=version,seeds=[180911301,180911303],roles=[0,1],pairs=[['E19.2','E19.3'],['E19.2','E22'],['E19.3','E22']],hashes={k:digest(v) for k,v in originals.items()},method='Serial pairwise games,2 exposed seeds,both roles. Reuse4 exact-hash V53/E22 games. Namespace-only copies isolate E19 module names. No policy changes or submissions.')
    dest=out/'PROTOCOL.json'
    if dest.exists():assert json.loads(dest.read_text(encoding='utf-8'))==protocol
    else:dest.write_text(json.dumps(protocol,indent=2),encoding='utf-8')
    files={}
    for name,p in originals.items():
        target=out/(name.replace('.','_')+'_isolated.py')
        s=p.read_text(encoding='utf-8').replace('_v51pkg','_triangle_'+name.replace('.','_')).replace('_assisted_770','_triangle_assisted_'+name.replace('.','_'))
        target.write_text(s,encoding='utf-8');files[name]=target
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    rows=[]
    for left,right in protocol['pairs']:
        for seed in protocol['seeds']:
            for seat in protocol['roles']:
                path=art/f'{left}_{right}_{seed}_{seat}.json'
                if left=='E19.3':
                    oldpath=HERE/f'artifacts/v53/E22_{seed}_{seat}.json';row=json.loads(oldpath.read_text(encoding='utf-8'));row.update(left=left,right=right,reused=True,replay=str(oldpath.with_suffix('.replay.json.gz').relative_to(ROOT)))
                elif path.exists():row=json.loads(path.read_text(encoding='utf-8'))
                else:
                    agents=[None,None];agents[seat]=str(files[left]);agents[1-seat]=str(files[right])
                    env=make('kaggriculture',configuration=dict(seed=seed,episodeSteps=720,turnsPerDay=24),debug=False);env.run(agents);r=env.toJSON()
                    assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1])
                    rp=path.with_suffix('.replay.json.gz')
                    with gzip.open(rp,'wt',encoding='utf-8') as f:json.dump(r,f,separators=(',',':'))
                    row=dict(left=left,right=right,seed=seed,seat=seat,rewards=r['rewards'],margin=r['rewards'][seat]-r['rewards'][1-seat],ledgers=[audit(r,s) for s in [0,1]],terminal=[end_state(r,s) for s in [0,1]],reused=False,replay=str(rp.relative_to(ROOT)))
                    path.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8');print('RESULT',left,right,seed,seat,row['rewards'],row['margin'],flush=True)
                rows.append(row);(out/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print('COMPLETE',len(rows),flush=True)
if __name__=='__main__':main()
