"""770 candidate: do not hire for crop cycles outside the biological horizon."""
import ast
from pathlib import Path
from types import MethodType
from docs.model_specs.codex.e19.tools.local_service_770_v49b import install as install_local


def sowing_has_horizon(day,final_day,crops,rules):
    return any(day+rules[c]['first_yield_day']<=final_day for c in crops)


def install(core):
    # Preserve the terminal and fertilizer-retention wrappers around the core
    # market method. Replace only the unsupported future-crop workload term.
    source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CommonController')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_market_orders')
    count=0
    for node in ast.walk(method):
        if isinstance(node,ast.If) and any(isinstance(n,ast.Name) and n.id=='free_tiles' for n in ast.walk(node)) and ast.unparse(node.test).startswith('self.day < self.final_day'):
            node.test=ast.BoolOp(op=ast.And(),values=[node.test,ast.parse(
                'sowing_has_horizon(self.day,self.final_day,self.profile.crops,CROPS)',mode='eval').body])
            count+=1
    assert count==1
    # Bound the effect of the approximate route workload estimator.
    for index,node in enumerate(method.body):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='target' for t in node.targets):
            block=ast.parse("""
if self.day < self.final_day and not sowing_has_horizon(self.day,self.final_day,self.profile.crops,CROPS):
    old_work=work
    if budget>self.maintenance_floor and self.remaining>6:
        old_work+=min(free_tiles,int((budget-self.maintenance_floor)//min(CROPS[c]['seed'] for c in self.profile.crops)))*4
    old_target=min(self.profile.maximum_hands,max(0,ceil(old_work/max(1,self.remaining-2))-1))
    target=max(target,old_target-1)
""").body
            method.body[index+1:index+1]=block
            break
    else:raise AssertionError('Missing staffing target')
    scope={}
    namespace=dict(core.__call__.__func__.__globals__,sowing_has_horizon=sowing_has_horizon)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),str(__file__),'exec'),namespace,scope)
    replacement=MethodType(scope['_market_orders'],core)
    replaced=0
    def replace(function):
        nonlocal replaced
        for cell in function.__closure__ or ():
            value=cell.cell_contents
            if isinstance(value,MethodType) and value.__name__=='_market_orders':
                cell.cell_contents=replacement;replaced+=1
            elif callable(value) and hasattr(value,'__closure__'):
                replace(value)
    replace(core._market_orders)
    assert replaced==1
    install_local(core)
