"""Explicit development/validation partitions; no automatic candidate selection."""
from concurrent.futures import ProcessPoolExecutor
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.run_pass_reduction_v49 import run


def one(case):
    try:return run(*case,telemetry=False)
    except Exception as exc:
        print('FAILED',case,repr(exc),flush=True)
        return False


if __name__=='__main__':
    split=sys.argv[1]
    assert split in {'development','validation'}
    candidate=sys.argv[2] if len(sys.argv)>2 else 'v49'
    assert candidate in {'v49','v49b','v49c','v49d','v49f'}
    seeds=[180903001,180903002,180903003] if split=='development' else [260909101,260909102]
    variants=(candidate,) if split=='development' and candidate!='v49' else ('v48',candidate)
    cases=[(v,s,t,split) for s in seeds for t in (0,1) for v in variants
           if not (split=='development' and candidate=='v49' and s==180903001 and t==0)
           and not (split=='development' and candidate!='v49' and s==180903003 and t==0)]
    with ProcessPoolExecutor(max_workers=2) as pool:
        outcomes=list(pool.map(one,cases))
    assert all(x is not False for x in outcomes),'Matrix incomplete; inspect FAILED entries'
