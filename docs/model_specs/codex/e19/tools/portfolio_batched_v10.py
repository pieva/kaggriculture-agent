"""Keep profitable same-tile work without sacrificing compulsory route packing."""
import ast
from pathlib import Path
from docs.model_specs.codex.e19.tools.portfolio_governed_v10 import install as install_governed


def install(core):
    install_governed(core)
    services=core._services
    namespace=core.__call__.__func__.__globals__
    rules=namespace['CROPS']
    base_certificate=next(c for c in core.__class__.__mro__ if '_day_route_certificate' in c.__dict__).__dict__['_day_route_certificate']

    def batched_services():
        offers=services()
        full={tuple(t):(commands,value) for t,commands,p,value,k in offers if k!='BIOLOGICAL'}
        result=[]
        for target,commands,priority,value,kind in offers:
            if kind=='BIOLOGICAL' and tuple(target) in full:
                optional,benefit=full[tuple(target)]
                tile=core._tile(target)
                extras=[]
                if tile.get('animal'):
                    extras=[c for c in optional if c[0] in {'CARE','HARVEST'}]
                    if ['CARE'] in extras:
                        rule=namespace['ANIMALS'][tile['animal']]
                        benefit+=core._quote(rule['product'],'SELL',1)/rule['interval']
                elif tile.get('crop') in rules and rules[tile['crop']]['ongoing']:
                    extras=[c for c in optional if c[0]=='HARVEST']
                if extras:result.append((target,commands+extras,priority,max(1,benefit),kind))
            # Always retain the original short alternative.
            result.append((target,commands,priority,value,kind))
        return result

    def certificate(worker,job,offers=None):
        offers=batched_services() if offers is None else offers
        required={}
        for target,commands,priority,value,kind in offers:
            if kind!='BIOLOGICAL':continue
            commands=[c for c in commands if c[0] in {'FEED','WATER'}]
            required[tuple(target)]=(target,commands,priority,1,kind)
        return base_certificate(core,worker,job,list(required.values()))

    core._services=batched_services
    core._day_route_certificate=certificate
    source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CommonController')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__call__')
    count=[0,0,0]
    for n in ast.walk(method):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='score' for t in n.targets):
            n.value.elts[0]=ast.parse('3*int(priority==3)+2*int(priority==5)+int(priority==4)',mode='eval').body
            count[0]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="steps is None and kind == 'SERVICE'":
            n.test=ast.parse("steps is None and kind in {'SERVICE','BIOLOGICAL'}",mode='eval').body
            count[1]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="job['kind'].startswith('NEW_')":
            n.test=ast.parse("job['kind'].startswith('NEW_') or job['kind']=='BIOLOGICAL' and any(cmd[0] in {'CARE','HARVEST'} for cmd,pos in job['steps'])",mode='eval').body
            count[2]+=1
    assert count==[1,1,1]
    scope={}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),str(__file__),'exec'),namespace,scope)
    core.__class__=type('PortfolioBatchedController',(core.__class__,),{'__call__':scope['__call__']})
