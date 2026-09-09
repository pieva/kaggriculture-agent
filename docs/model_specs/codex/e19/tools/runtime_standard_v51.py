"""Serial standard-timeout game using the standalone entry point."""
import gzip,hashlib,json,runpy,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
OUT=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v51'


def main():
    from kaggle_environments import make
    from docs.model_specs.codex.e18.tools.run_e18_27_d10_d15_cashflow_gate import opponent_policy
    bundle=Path(sys.argv[1]);name=sys.argv[2];seed=int(sys.argv[3]);seat=int(sys.argv[4])
    agent=runpy.run_path(str(bundle))['agent'];durations=[];errors=[]
    def capture(obs,cfg):
        start=time.perf_counter()
        try:return agent(obs,cfg)
        except Exception as e:errors.append(repr(e));raise
        finally:durations.append(time.perf_counter()-start)
    opp=opponent_policy('E18.2/V4D',seed,1-seat)
    env=make('kaggriculture',configuration=dict(seed=seed,episodeSteps=720,turnsPerDay=24,actTimeout=1),debug=False)
    env.run([capture,opp] if seat==0 else [opp,capture]);replay=env.toJSON()
    missing=[i for i,s in enumerate(replay['steps'][1:],1) if s[seat].get('action') is None]
    result=dict(variant=name,seed=seed,seat=seat,bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest(),
        configuration=replay['configuration'],calls=len(durations),statuses=replay['statuses'],rewards=replay['rewards'],
        missing=missing,errors=errors,max_seconds=max(durations),overage=sum(max(0,d-1) for d in durations),
        passed=len(durations)==719 and not errors and not missing and replay['statuses']==['DONE','DONE'],
        note='Serial local run with standard actTimeout and engine overage; not a Kaggle publication or hardware equivalence guarantee.')
    base=ROOT/'docs/model_specs/codex/e19/reports/pass_reduction_v49_20260909' if name=='v49f' else OUT
    expected=base/f'development_{name}_{seed}_{seat}.json'
    if expected.exists():
        metadata=json.loads(expected.read_text())
        previous=json.load(gzip.open(ROOT/metadata['details'],'rt'))['replay']
        result['recorded_action_parity']=len(replay['steps'])==720 and all(replay['steps'][i][seat]['action']==previous['steps'][i][seat]['action'] for i in range(1,720))
        result['passed']=result['passed'] and result['recorded_action_parity']
    path=OUT/f'runtime_{name}_{seed}_{seat}.json';path.write_text(json.dumps(result,indent=2))
    with gzip.open(ROOT/f'scratch/v51/runtime_{name}_{seed}_{seat}.json.gz','wt') as f:json.dump(replay,f)
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
