"""Use real daily inventory transfer; batch discretionary shed deliveries."""
import ast
from math import ceil
from pathlib import Path
from types import MethodType
from docs.model_specs.codex.e19.tools.portfolio_concurrent_v10 import install as install_concurrent


def install(core):
    install_concurrent(core)
    namespace=core.__call__.__func__.__globals__
    rules=namespace['CROPS']
    animals=namespace['ANIMALS']

    def harvest_bound(target):
        tile=core._tile(target)
        if not isinstance(tile,dict):return 0
        if tile.get('crop') in rules:
            return rules[tile['crop']]['max_yield']
        return tile.get('yield_units',0)

    def projected_stock():
        value=sum(core.private['shed'].values())+sum(sum(inv.values()) for inv in core.private['inventories'])
        for job in core.active.values():
            if any(cmd[0]=='HARVEST' for cmd,pos in job['steps']):value+=harvest_bound(job['target'])
            value+=sum(cmd[0]=='COLLECT_FERTILIZER' for cmd,pos in job['steps'])
        return value

    def return_required(target,commands):
        # A final-day transfer has no subsequent refresh and sale opportunity.
        if core.day==core.final_day:return True
        output=harvest_bound(target) if ['HARVEST'] in commands else 0
        output+=int(['COLLECT_FERTILIZER'] in commands)
        return projected_stock()+output>core.portfolio_shed_capacity or core.farm['money']<core.maintenance_floor

    def delivery_needed(worker):
        inv=core.private['inventories'][worker]
        carried=sum(n for c,n in inv.items() if c not in animals)
        if not carried:return False
        if core.day==core.final_day:return True
        if core.farm['money']<core.maintenance_floor:return True
        if projected_stock()>=core.portfolio_shed_capacity:return True
        # Share finite overnight capacity among actual, observed workers.
        if carried>=ceil(core.portfolio_shed_capacity/max(1,len(core.positions))):return True
        # A worker already next to the shed can unload without a return trip.
        return tuple(core.positions[worker]) in core.sheds and any(c!='WHEAT' and c not in animals for c in inv)

    core._portfolio_return_required=return_required
    core._portfolio_delivery_needed=delivery_needed
    core.portfolio_shed_capacity=100
    source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CommonController')
    prepare=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_prepare_steps')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__call__')
    count=[0,0,0,0,0]
    for n in ast.walk(prepare):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='return_cost' for t in n.targets):
            assert isinstance(n.value,ast.IfExp)
            n.value.test=ast.parse('output and self._portfolio_return_required(target,commands)',mode='eval').body
            count[0]+=1
    method.body.insert(0,ast.parse("self.portfolio_shed_capacity=configuration.get('shedCapacity',100)").body[0])
    for n in ast.walk(method):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='score' for t in n.targets):
            n.value.elts[0]=ast.parse('3*int(priority==3)+2*int(priority==5)+int(priority==4)',mode='eval').body
            count[1]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="steps is None and kind == 'SERVICE'":
            n.test=ast.parse("steps is None and kind in {'SERVICE','BIOLOGICAL'}",mode='eval').body
            count[2]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="job['kind'].startswith('NEW_')":
            n.test=ast.parse("job['kind'].startswith('NEW_') or job['kind']=='BIOLOGICAL' and any(cmd[0] in {'CARE','HARVEST'} for cmd,pos in job['steps'])",mode='eval').body
            count[3]+=1
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='products' for t in n.targets):
            n.value=ast.parse("{k:n for k,n in inv.items() if k not in ANIMALS} if self._portfolio_delivery_needed(worker) else {}",mode='eval').body
            count[4]+=1
    assert count==[1,1,1,1,1]
    scope={}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[prepare,method],type_ignores=[])),str(__file__),'exec'),namespace,scope)
    core._prepare_steps=MethodType(scope['_prepare_steps'],core)
    core.__class__=type('PortfolioLogisticsController',(core.__class__,),{'__call__':scope['__call__']})
