"""Bundle the safety-verified E18.32 V7; does not upload or promote it."""
import ast
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[3]
DERIVED=BASE/'artifacts/derived'
OUTPUT=ROOT/'submission/submission_codex_e18_32_770.py'
VERSION='E18.32-DEMAND-RELEASE-770-V7'
GATE=DERIVED/'E18_32_READY_WORK_GATE_RELEASE_V7_DEVELOPMENT_20260906.json'
MANIFEST=DERIVED/'E18_32_SUBMISSION_MANIFEST_V7.json'


def build():
    from docs.model_specs.codex.e18.tools.summarize_e18_32_ready_work import safety
    parent=ROOT/'submission/submission_codex_e18_31_770.py'
    assert hashlib.sha256(parent.read_bytes()).hexdigest()=='59dcf7b9fb380f60460a2b300fc9043fe6ce816be2c28004a82971420650ed63'
    gate=json.loads(GATE.read_text())
    assert gate['complete'] and len(gate['matches'])==28
    assert all(all(safety(m).values()) for m in gate['matches'])
    excluded={'MODEL_VERSION','SOURCE_HASHES','create_agent','_ACTIVE','agent'}
    nodes=[]
    for node in ast.parse(parent.read_text(encoding='utf-8')).body:
        name=getattr(node,'name',None)
        if isinstance(node,ast.Assign) and len(node.targets)==1:
            name=getattr(node.targets[0],'id',None)
        if name not in excluded:
            nodes.append(node)
    hashes={str(parent.relative_to(ROOT)):hashlib.sha256(parent.read_bytes()).hexdigest()}
    class Namespace(ast.NodeTransformer):
        def visit_Name(self,node):
            if node.id=='FIB':
                node.id='E31_FIB'
            return node
    for filename in ['e18_32_demand_routing_controller.py','e18_32_claim_routing_controller.py']:
        path=BASE/'tools'/filename
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest==gate['source_sha256'][str(path)]
        hashes[str(path.relative_to(ROOT))]=digest
        for node in ast.parse(path.read_text(encoding='utf-8')).body:
            if isinstance(node,(ast.ClassDef,ast.FunctionDef,ast.Assign,ast.AnnAssign)):
                nodes.append(Namespace().visit(node))
    entry=f'''
MODEL_VERSION = {VERSION!r}
SOURCE_HASHES = {hashes!r}
def create_agent(run_context=None):
    return ClaimRoutingController(deepcopy(_PLAN), int((run_context or {{}}).get('player_position',0)), variant='DEMAND_RELEASE', reference_plan=_PARENT_27_PLAN)
_ACTIVE = {{}}
def agent(observation, configuration=None):
    seat=int(observation.get('player',0))
    step=int(observation.get('step',0))
    entry=_ACTIVE.get(seat)
    policy=create_agent({{'player_position':seat}}) if entry is None or step<=entry[0] else entry[1]
    _ACTIVE[seat]=(step,policy)
    return policy(observation,configuration)
'''
    nodes.extend(ast.parse(entry).body)
    if isinstance(nodes[0],ast.Expr) and isinstance(nodes[0].value,ast.Constant):
        nodes[0].value.value='E18.32 V7: demand-sized 770 routes and observed service release. Internal diagnostic, no promotion.'
    result=ast.unparse(ast.Module(body=nodes,type_ignores=[]))+'\n'
    compile(result,str(OUTPUT),'exec')
    assert not any(s in result for s in ['from docs.','kaggle_environments','read_text(','from agricola'])
    if OUTPUT.exists():
        assert OUTPUT.read_text(encoding='utf-8')==result,'Preserve existing submission'
    else:
        OUTPUT.write_text(result,encoding='utf-8',newline='\n')
    manifest=dict(version=VERSION,sources=hashes,submission=str(OUTPUT.relative_to(ROOT)),
                  submission_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),bytes=OUTPUT.stat().st_size,
                  gate_sha256=hashlib.sha256(GATE.read_bytes()).hexdigest(),
                  external_status='NOT_UPLOADED',incumbent_promoted=False,holdout_consumed=False)
    target=MANIFEST
    if target.exists():
        assert json.loads(target.read_text())==manifest
    else:
        target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    build()
