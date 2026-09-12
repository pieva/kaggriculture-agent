"""Persistent 774 reconstruction, distinct from the historical aborted build."""
import ast,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
BASE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    from docs.model_specs.codex.e20.tools import run_experiment as runner
    parent=ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'
    transfer=ROOT/'docs/model_specs/codex/e20/tools/build_e20_v39.py'
    tree=ast.parse(transfer.read_text(encoding='utf-8'))
    overlay=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OVERLAY' for t in n.targets))
    start=overlay.index("            action=self.policy(observation,configuration)")
    end=overlay.index('        t=self.core',start)
    overlay=overlay[:start]+'            return self.policy(observation,configuration)\n'+overlay[end:]
    overlay=overlay.replace('{(3,5),(3,6),(4,7)}','{(4,7)}').replace("{'Q0':7,'Q1':7,'Q2':2}","{'Q0':7,'Q1':7,'Q2':4}")
    overlay=overlay.replace('t.livestock_resource_cap=16','t.livestock_resource_cap=19').replace("t.config['pre_q2_livestock_resource_cap']=16","t.config['pre_q2_livestock_resource_cap']=18").replace("t.config['reclaimed_seed_backfill_units']=3","t.config['reclaimed_seed_backfill_units']=1")
    overlay=overlay.replace('772','774').replace('E20V39','Fixed774').replace('E20_V39','FIXED774').replace('E20-774-E20V39','E21-DIAGNOSTIC-FIXED774')
    # All artifacts stay outside the release/submission directory.
    bundle=BASE/'artifacts/fixed774_reconstruction.py';bundle.parent.mkdir(exist_ok=True)
    content=parent.read_text(encoding='utf-8')+overlay
    if bundle.exists():assert bundle.read_text(encoding='utf-8')==content
    else:bundle.write_text(content,encoding='utf-8')
    protocol=dict(identity='FIXED774_MODERN_RECONSTRUCTION_NOT_HISTORICAL',seed=180911301,seat=0,opponent='E18',runs=1,
        activation='D12 (day index 11), preserve E18 opening including coop',target=[4,7],
        mechanism='E20v39 inherited persistent topology filter, reduced to one reclaim; no E20 planner',
        cap='18 pre-Q2, 19 after Q2, matching surviving E18 reclaim envelope; does not guarantee one fewer purchased animal',
        differences_from_surviving_reclaim=['fixed D12 activation','no rollback','filters persist at terminal','inherited topology-cap service/fill routing'],
        limits='Diagnostic trajectory only; no claim of historical reproduction or isolated pasture value; no tuning',
        sources={str(p.relative_to(ROOT)):sha(p) for p in [parent,transfer,Path(__file__),bundle]})
    p=BASE/'FIXED774_PROTOCOL.json'
    if p.exists():assert json.loads(p.read_text())==protocol
    else:p.write_text(json.dumps(protocol,indent=2)+'\n')
    runner.BASE=BASE;agents={}
    def factory(name,seat):
        p=bundle if name=='Fixed774' else parent;ns={'__name__':'_fixed774'}
        exec(compile(p.read_text(encoding='utf-8'),str(p),'exec'),ns)
        agent=ns['create_agent']({'player_position':seat});agents[seat]=agent;return agent
    runner.policy=factory
    result=runner.run(('fixed774','Fixed774','E18',180911301))
    assert all(r['calls']==719 for r in result['runtime'])
    assert result['runtime'][0]['core_errors']==0
    assert result['opening'][0]['topology']==[7,7,4]
    if agents:
        (BASE/'artifacts/fixed774/TELEMETRY.json').write_text(json.dumps(agents[0].core.telemetry_snapshot(),indent=2)+'\n')
    from docs.model_specs.codex.e20.tools.audit_results import run as audit
    audit(BASE/'artifacts/fixed774/Fixed774_E18_180911301.json')
if __name__=='__main__':main()
