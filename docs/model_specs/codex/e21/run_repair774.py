"""Freeze and verify repair1 on exposed seed 301, both roles, serially."""
import gzip,hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]
sys.path.insert(0,str(ROOT))

def main():
    revision=2 if '--v2' in sys.argv else 1
    seed=180911303 if '--seed303' in sys.argv else 180911301
    parent=BASE/'artifacts/fixed774_reconstruction.py'
    overlay=BASE/'repair774_overlay.py'
    bundle=BASE/f'artifacts/repaired774_v{revision}.py'
    content=parent.read_text(encoding='utf-8')+'\n'+overlay.read_text(encoding='utf-8')
    extra=BASE/'repair774_v2_overlay.py'
    if revision==2:content+='\n'+extra.read_text(encoding='utf-8')
    compile(content,'<repaired774>','exec')
    if bundle.exists(): assert bundle.read_text(encoding='utf-8')==content
    else: bundle.write_text(content,encoding='utf-8')
    protocol={'identity':f'CODEX-E21-774-REPAIR{revision}','seed':seed,'roles':[0,1],
              'opponent':'E18','purpose':'technical repair verification, not competitive promotion',
              'invariants':['719 calls','no exceptions or nested fallbacks','774','17 pasture animals plus goose','no unused livestock at terminal','route rejoins','unchanged D1-D11'],
              'changes':['cap17','disable fill into formerly empty Q1 pasture','skip unneeded target excursions with timed rejoin','correct metadata','terminal delivery protection'],
              'sources':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [parent,overlay,bundle]+([extra] if revision==2 else [])}}
    if revision==2:protocol['changes']+=['fill only Q2, keep Q1 (6,3) empty','require next-turn on-target slot before sowing','normalize optional shared step']
    path=BASE/(f'REPAIR774_V{revision}_PROTOCOL.json' if seed==180911301 else f'REPAIR774_V{revision}_{seed}_PROTOCOL.json')
    if path.exists():assert json.loads(path.read_text())==protocol
    else:path.write_text(json.dumps(protocol,indent=2)+'\n')
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
        result=runner.run((f'repair774_v{revision}',left,right,seed))
        seat=0 if left=='Repair774' else 1
        path=BASE/f'artifacts/repair774_v{revision}/{left}_{right}_{seed}.json'
        if seat in agents and hasattr(agents[seat],'events'):
            p=agents[seat]
            path.with_suffix('.repair.json').write_text(json.dumps({'metrics':p.metrics,'events':p.events,'pending_detours':p.detours,'telemetry':p.core.telemetry_snapshot()},indent=2)+'\n')
        assert all(r['calls']==719 for r in result['runtime'])
        assert result['runtime'][seat]['core_errors']==0
        audit(path)

if __name__=='__main__':main()
