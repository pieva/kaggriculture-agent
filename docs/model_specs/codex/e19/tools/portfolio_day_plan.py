"""Admit every mission against a complete packing of today's obligations."""
import ast
from pathlib import Path
from docs.model_specs.codex.e19.tools.portfolio_logistics import install as install_logistics


def install(core):
    install_logistics(core)
    certificate=core._day_route_certificate
    def mission_certificate(worker,job,services=None):
        if job['kind']=='DELIVER':
            # Unloading at a shed-adjacent plant does not water that plant.
            job=dict(job,target=(-1,-1))
        return certificate(worker,job,services)
    core._day_route_certificate=mission_certificate
    source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CommonController')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__call__')
    method.body.insert(0,ast.parse("self.portfolio_shed_capacity=configuration.get('shedCapacity',100)").body[0])
    count=[0,0,0,0,0]
    for n in ast.walk(method):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='score' for t in n.targets):
            n.value.elts[0]=ast.parse('int(priority==5)',mode='eval').body
            count[0]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="steps is None and kind == 'SERVICE'":
            n.test=ast.parse("steps is None and kind in {'SERVICE','BIOLOGICAL'}",mode='eval').body
            count[1]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="job['kind'].startswith('NEW_')":
            n.test=ast.Constant(value=True)
            count[2]+=1
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='products' for t in n.targets):
            n.value=ast.parse("{k:n for k,n in inv.items() if k not in ANIMALS} if self._portfolio_delivery_needed(worker) else {}",mode='eval').body
            count[3]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=='selected is None':
            n.body=ast.parse('''
pure=[o for o in options if o[2]['kind']=='BIOLOGICAL' and all(cmd[0] in {'NORTH','SOUTH','EAST','WEST','PICKUP','FEED','WATER'} for cmd,pos in o[2]['steps'])]
if not pure:
    break
selected=max(pure,key=lambda o:(max(self._tile(o[2]['target']).get('consecutive_unfed',0),self._tile(o[2]['target']).get('consecutive_unwatered',0)),-len(o[2]['steps'])))
self.metrics['portfolio_capacity_emergency']+=1
''').body
            count[4]+=1
    assert count==[1,1,1,1,1]
    scope={}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),str(__file__),'exec'),core.__call__.__func__.__globals__,scope)
    core.__class__=type('PortfolioDayPlanController',(core.__class__,),{'__call__':scope['__call__']})
