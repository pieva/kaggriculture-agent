from concurrent.futures import ProcessPoolExecutor
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.run_pass_reduction_v50 import run


def one(case):
    return run(*case,telemetry=False)


if __name__=='__main__':
    variant,stage=sys.argv[1:3]
    assert stage in {'screen','development'}
    cases=[(variant,s,0,'development') for s in [180903001,180903002]] if stage=='screen' else [(variant,s,1,'development') for s in [180903001,180903002,180903003]]
    with ProcessPoolExecutor(max_workers=2) as pool:list(pool.map(one,cases))
