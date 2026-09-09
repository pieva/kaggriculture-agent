"""After the paired matrix, run serial standard runtime only for a passing strategy."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from docs.model_specs.codex.e19.tools.analyze_pass_reduction_v51 import analyze

def command(script,args,log):
    with (ROOT/'scratch/v51'/log).open('w') as f:
        subprocess.run([sys.executable,'-B',str(Path(__file__).parent/script),*args],stdout=f,stderr=subprocess.STDOUT,check=True,cwd=ROOT)

if __name__=='__main__':
    report=analyze('v51c')
    assert report['partitions']['development']['n']==6
    assert report['partitions']['validation']['n']==4
    if report['status']=='LOCAL_CANDIDATE_ONLY':
        for seat in [0,1]:
            print(f'Standard runtime seat {seat}',flush=True)
            command('runtime_standard_v51.py',['submission/submission_codex_e19_770_v51_candidate.py','v51c','180903001',str(seat)],f'runtime_c{seat}.log')
    else:print('Validation rejected: standard runtime not needed for promotion.',flush=True)
    command('report_v51.py',['v51c'],'report_c_final.log')
    command('finalize_v51.py',[],'finalize.log')
