"""Serial file-loader matches: V53 versus frozen baseline, E22, E20.9fix."""
import gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT));HERE=Path(__file__).resolve().parent
def main():
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.build_e18_26_jesse_770_d30_closure import audit,end_state
    out=HERE/'reports/v53';art=HERE/'artifacts/v53';out.mkdir(parents=True,exist_ok=True);art.mkdir(parents=True,exist_ok=True)
    candidate=ROOT/'submission/archive/e19_rejected/submission_codex_e19_3_770_v53_fixes.py'
    opponents={'E19V51C':ROOT/'submission/submission_codex_e19_770_v51_candidate.py','E22':ROOT/'submission/submission_codex_e22_s56165462_observed_v1.py','E20.9fix':ROOT/'submission/submission_codex_e20_9_placefix_internal.py'}
    protocol=dict(candidate='E19.3 V53 fixes',seeds=[180911301,180911303],opponents={k:str(v.relative_to(ROOT)) for k,v in opponents.items()},method='Serial full 720-step file-loader games; frozen baseline seat0 screening, E22 and E20.9fix both seats. Exposed seeds, shared endogenous market; no external submission.',hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [candidate,*opponents.values()]})
    (out/'PROTOCOL.json').write_text(json.dumps(protocol,indent=2),encoding='utf-8');rows=[]
    for name,other in opponents.items():
        for seed in protocol['seeds']:
            for seat in ([0] if name=='E19V51C' else [0,1]):
                dest=art/f'{name}_{seed}_{seat}.json'
                if dest.exists():rows.append(json.loads(dest.read_text(encoding='utf-8')));continue
                paths=[None,None];paths[seat]=str(candidate);paths[1-seat]=str(other)
                # Each Kaggle file loader owns its execution namespace.
                env=make('kaggriculture',configuration={'seed':seed,'episodeSteps':720,'turnsPerDay':24},debug=False);env.run(paths);r=env.toJSON()
                assert len(r['steps'])==720 and all(s['status']=='DONE' for s in r['steps'][-1]),r['steps'][-1]
                ls=[audit(r,s) for s in [0,1]]
                row=dict(opponent=name,seed=seed,seat=seat,rewards=r['rewards'],margin=r['rewards'][seat]-r['rewards'][1-seat],ledgers=ls,terminal=[end_state(r,s) for s in [0,1]])
                with gzip.open(dest.with_suffix('.replay.json.gz'),'wt',encoding='utf-8') as f:json.dump(r,f,separators=(',',':'))
                dest.write_text(json.dumps(row,separators=(',',':')),encoding='utf-8');rows.append(row)
                (out/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
                print('RESULT',name,seed,seat,r['rewards'],'margin',row['margin'],'escapes',[len(l['animal_escapes']) for l in ls],flush=True)
    (out/'RESULTS.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__':main()
