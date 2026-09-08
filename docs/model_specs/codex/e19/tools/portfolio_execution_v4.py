"""Separate daily biological service from certified portfolio rotations."""
import ast
from pathlib import Path
from docs.model_specs.codex.e19.tools.portfolio_succession_v4 import install as install_portfolio


def install(core):
    install_portfolio(core)
    services=core._services
    growth=core._growth
    certificate=core._day_route_certificate
    market_orders=core._market_orders

    def retain_observed_fertilizer():
        orders=market_orders()
        rules=core.__call__.__func__.__globals__['CROPS']
        needed=0
        for row in core.farm['tiles']:
            for tile in row:
                if not isinstance(tile,dict) or tile.get('kind')!='PLANT':
                    continue
                rule=rules[tile['crop']]
                if not rule['ongoing']:continue
                dates=[tile['planted_day']+rule['first_yield_day']+i*rule['interval'] for i in range(rule['max_yield'])]
                if any(core.day<d<=min(core.day+3,core.final_day) and tile.get('fertilized_until_day',-1)<d-1 for d in dates):
                    needed+=1
        # Retain observed stock for the forthcoming production window. No
        # speculative fertilizer purchases or unobserved cash are introduced.
        req,_=core._requirements()
        extra=max(0,needed-req['FERTILIZER'])
        result=[]
        for order in orders:
            if order[0]=='SELL' and order[1]=='FERTILIZER':
                order=[*order[:2],max(0,order[2]-extra)]
                if not order[2]:continue
            result.append(order)
        return result

    core._market_orders=retain_observed_fertilizer

    def split_services():
        result=[]
        for target,commands,priority,value,kind in services():
            required=[c for c in commands if c[0] in {'FEED','WATER'}]
            if required:
                result.append((target,required,3,1,'BIOLOGICAL'))
            optional=[c for c in commands if c[0] not in {'FEED','WATER'}]
            if optional:
                # A full service can still be selected after all free workers
                # have been matched to observed biological obligations.
                tile=core._tile(target)
                due=core.portfolio_planted_ends.get((tuple(target),tile.get('planted_day')))
                rules=core.__call__.__func__.__globals__['CROPS']
                crop=tile.get('crop')
                expiring=(due is not None and core.day>=due or crop in rules and not rules[crop]['ongoing'] and core.day-tile['planted_day']>=rules[crop]['max_yield_day'])
                priority=4 if ['HARVEST'] in commands and (expiring or core.day==core.final_day) else 0
                result.append((target,commands,priority,value,kind))
        return result

    def rotation_offers(cash):
        return [(t,cmd,5 if k=='NEW_ROTATION' else p,v,k) for t,cmd,p,v,k in growth(cash)]

    def required_once(worker,job,offers=None):
        offers=split_services() if offers is None else offers
        # The BIOLOGICAL offer already contains the full mandatory service.
        return certificate(worker,job,[s for s in offers if s[4]=='BIOLOGICAL'])

    core._services=split_services
    core._growth=rotation_offers
    core._day_route_certificate=required_once
    source=Path(__file__).resolve().parents[5]/'submission/submission_codex_e19_control_770_v2.py'
    tree=ast.parse(source.read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='CommonController')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__call__')
    replacements=[0,0]
    for n in ast.walk(method):
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='score' for t in n.targets):
            assert ast.unparse(n.value.elts[0])=='int(priority == 3)'
            n.value.elts[0]=ast.parse('3*int(priority==3)+2*int(priority==5)+int(priority==4)',mode='eval').body
            replacements[0]+=1
        if isinstance(n,ast.If) and ast.unparse(n.test)=="steps is None and kind == 'SERVICE'":
            n.test=ast.parse("steps is None and kind in {'SERVICE','BIOLOGICAL'}",mode='eval').body
            replacements[1]+=1
    assert replacements==[1,1]
    namespace={}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method],type_ignores=[])),str(__file__),'exec'),core.__call__.__func__.__globals__,namespace)
    core.__class__=type('PortfolioExecutionController',(core.__class__,),{'__call__':namespace['__call__']})
