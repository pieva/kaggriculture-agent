import gzip,hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3];sys.path.insert(0,str(ROOT))
def main():
    bundle=BASE/"artifacts/repaired774_v3.py"
    seed=int(sys.argv[1])
    from docs.model_specs.codex.e20.tools import run_experiment as runner
    from docs.model_specs.codex.e20.tools.audit_results import run as audit
    runner.BASE=BASE
    agents={}
    def factory(name,seat):
        p=bundle if name=='Repair774' else ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'
        ns={'__name__':'_repair_test'}
        exec(compile(p.read_text(encoding='utf-8'),'<standalone>','exec'),ns)
        result=ns['create_agent']({'player_position':seat});agents[seat]=result
        return result
    runner.policy=factory
    for left,right in [('Repair774','E18'),('E18','Repair774')]:
        result=runner.run(('repair774_v3',left,right,seed))
        seat=0 if left=='Repair774' else 1
        path=BASE/f'artifacts/repair774_v3/{left}_{right}_{seed}.json'
        if seat in agents and hasattr(agents[seat],'events'):
            p=agents[seat]
            path.with_suffix('.repair.json').write_text(json.dumps({'metrics':p.metrics,'events':p.events,'pending_detours':p.detours,'telemetry':p.core.telemetry_snapshot()},indent=2)+'\n')
        assert all(r['calls']==719 for r in result['runtime'])
        assert result['runtime'][seat]['core_errors']==0
        audit(path)

if __name__=='__main__':main()
