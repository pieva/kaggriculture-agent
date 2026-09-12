"""One diagnostic run of surviving reclaim logic, not the lost historical build."""
import gzip, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
BASE=Path(__file__).resolve().parent
PARENT=ROOT/'submission/submission_codex_e18_2_capacity_governed_v4d.py'
SOURCE=ROOT/'src/agricola/strategy/codex/codex_e18_capacity_governed_v4d.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(seat, reclaim=False):
    ns={'__name__':'_e21_diagnostic'}
    exec(compile(PARENT.read_text(encoding='utf-8'),str(PARENT),'exec'),ns)
    p=ns['create_agent']({'player_position':seat})
    core=p.codex_e18_capacity_governed_instance
    if reclaim:
        core.e18_config['topology_reclaim_enabled']=True
        # Dormant membership expression hashes dict tiles. Preserve its intended
        # empty/locked predicate without raising TypeError on occupied tiles.
        source=SOURCE.read_text(encoding='utf-8')
        a=source.index('    def _observe_day(');b=source.index('    def _reclaimed_crop_tasks(',a)
        import textwrap,types
        method=textwrap.dedent(source[a:b]).replace(
            'if _tile(_farm(observation), target) in {None, "LOCKED"}:',
            'if _tile(_farm(observation), target) is None or _tile(_farm(observation), target) == "LOCKED":')
        scope={};exec(compile(method,'e21_safe_tile_predicate','exec'),ns['_e18_2'].__dict__,scope)
        core._observe_day=types.MethodType(scope['_observe_day'],core)
    class Capture:
        def __init__(self):self.core=core;self.trace=[]
        def __call__(self,obs,cfg):
            action=p(obs,cfg)
            self.trace.append(dict(day=obs['day']+1,hour=obs['hour']+1,mode=core.mode,
                reclaim=sorted(core.committed_reclaims),aborts=core.aborted_reclaim_batches,
                errors=core.error_count,last_exception=getattr(core,'last_exception',None)))
            return action
    return Capture()
def main():
    from docs.model_specs.codex.e20.tools import run_experiment as runner
    protocol=BASE/'RECONSTRUCTION_PROTOCOL.json'
    spec=dict(status='DIAGNOSTIC_RECONSTRUCTION_NOT_HISTORICAL_774',seed=180911301,seat=0,
        opponent='E18',runs=1,reference_772='E20.2',
        changes=['Enable topology_reclaim_enabled after loading frozen E18',
                 'Repair unhashable dict membership in dormant empty/locked predicate'],
        preserved=['capacity and pressure thresholds','crop selection and inherited filters',
                   'rollback to dense','terminal passthrough','all other frozen E18 behavior'],
        evaluation='22 KPI D1-30, Q0/Q1 D1-11 and D12-19; realized topology and first divergence; no promotion',
        sources={str(p.relative_to(ROOT)):sha(p) for p in [PARENT,SOURCE,Path(__file__)]})
    if protocol.exists():assert json.loads(protocol.read_text())==spec
    else:protocol.write_text(json.dumps(spec,indent=2)+'\n')
    assert sha(PARENT)=='c5fb1fc4966b81f238cdd0de4ca5e15b16ea6b8ae077a08ecc881f8729fd01f7'
    runner.BASE=BASE
    agents={}
    def factory(name,seat):
        agents[seat]=load(seat,name=='R774')
        return agents[seat]
    runner.policy=factory
    result=runner.run(('reconstruction','R774','E18',180911301))
    if agents:
        (BASE/'artifacts/reconstruction/CONTROLLER_TRACE.json').write_text(json.dumps(
            {str(i):dict(trace=a.trace,telemetry=a.core.telemetry_snapshot()) for i,a in agents.items()},indent=2)+'\n')
    assert all(r['calls']==719 and r['core_errors']==0 for r in result['runtime'])
    from docs.model_specs.codex.e20.tools.audit_results import run as audit
    audit(BASE/'artifacts/reconstruction/R774_E18_180911301.json')
if __name__=='__main__':main()
