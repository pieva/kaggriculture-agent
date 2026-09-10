"""Complete the common-opponent role swap without rerunning cached forward cases."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e20.tools.run_experiment import run

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--stage',required=True)
    p.add_argument('--workers',type=int,default=2);p.add_argument('--seeds',nargs='+',type=int,required=True)
    p.add_argument('--baseline',action='store_true');a=p.parse_args()
    cases=[(a.stage,'E18',a.model,s) for s in a.seeds]
    if a.baseline:cases += [('e20_1_baseline','E18','E19',s) for s in a.seeds if s<180910100]
    with ProcessPoolExecutor(max_workers=a.workers) as pool:list(pool.map(run,cases))
