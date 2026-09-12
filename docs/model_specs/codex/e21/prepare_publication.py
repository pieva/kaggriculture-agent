"""Package R2 with an unambiguous final Kaggle callable; replay parity only."""
import gzip,hashlib,json
from copy import deepcopy
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3]
def main():
    original=BASE/'artifacts/repaired774_v2.py'
    assert hashlib.sha256(original.read_bytes()).hexdigest()=='54cdd147b47e74fe43024c9960ffe5308135e83e5618d3cba874339337c36669'
    target=ROOT/'submission/submission_codex_e21_774_repair2.py'
    code=original.read_text(encoding='utf-8')+'\n# Explicit final callable for Kaggle get_last_callable.\ndef kaggle_submission_agent(observation, configuration=None):\n    return agent(observation, configuration)\n'
    if target.exists():assert target.read_text(encoding='utf-8')==code
    else:target.write_text(code,encoding='utf-8')
    from kaggle_environments.agent import get_last_callable
    results=[]
    for path in sorted((BASE/'artifacts/repair774_v2').glob('*_18091130[13].replay.json.gz')):
        r=json.loads(gzip.decompress(path.read_bytes()))
        seat=0 if path.name.startswith('Repair774') else 1
        policy=get_last_callable(code)
        assert policy.__name__=='kaggle_submission_agent'
        for i in range(719):
            obs={'step':i,**deepcopy(r['steps'][i][seat]['observation'])}
            assert policy(obs,deepcopy(r['configuration']))==r['steps'][i+1][seat]['action'],(path.name,i)
        results.append({'replay':path.name,'seat':seat,'calls':719,'mismatches':0})
    manifest={'model':'CODEX-E21-774-REPAIR2','file':target.relative_to(ROOT).as_posix(),
              'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'parent_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
              'packaging_only':'unique final callable delegates to verified agent; no strategy changes','loader_parity':results,'uploaded':False}
    target.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
