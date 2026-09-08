from pathlib import Path
p=Path('docs/model_specs/codex/e19/tools')
for name in ['biological_plan_770','daily_routes_770','daily_route_dispatch_770','daily_route_scheduler_770','run_daily_routes_770']:
    s=(p/f'{name}_v47.py').read_text(encoding='utf-8').replace('_v47','_v48').replace('V47','V48')
    (p/f'{name}_v48.py').write_text(s,encoding='utf-8')
f=p/'daily_routes_770_v48.py';s=f.read_text(encoding='utf-8')
s=s.replace('def final_water_deadline(','''def yield_water_units(tile,day,rules):
    if not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('watered_today'):return 0
    rule=rules[tile['crop']]
    if rule['ongoing']:return 0
    age=day-tile['planted_day']
    if not (rule['max_yield_day']+1)//2<=age<=rule['max_yield_day']:return 0
    return max(0,min(2 if tile.get('fertilized_until_day',-1)>=day else 1,rule['max_yield']-tile.get('yield_units',0)))


def due_visit(offer,tile,day,turns,rules,quote):
    target,commands,priority,value,kind=offer
    if not harvest_due(tile,day,turns) or not any(c[0]=='HARVEST' for c in commands):return offer,None
    gain=yield_water_units(tile,day,rules) if day>=27 else 0
    if gain:
        old=tile.get('yield_units',0)
        delta=quote(tile['crop'],'SELL',old+gain)-quote(tile['crop'],'SELL',old)
        return (target,[['WATER'],['HARVEST']],6,value+delta,'SERVICE'),(target,[['HARVEST']],5,value,'SERVICE')
    return (target,[['HARVEST']],6,value,'SERVICE'),None


def final_water_deadline(''')
old="        current=[(t,[['HARVEST']],6,v,'SERVICE') if harvest_due(core._tile(t),core.day,core.turns) and any(c[0]=='HARVEST' for c in cmds) else (t,cmds,p,v,k) for t,cmds,p,v,k in current]"
new="""        due_fallbacks=[]
        transformed=[]
        for offer in current:
            full,bare=due_visit(offer,core._tile(offer[0]),core.day,core.turns,core.__call__.__func__.__globals__['CROPS'],core._quote)
            transformed.append(full)
            if bare is not None:due_fallbacks.append(bare)
        current=transformed"""
assert old in s;s=s.replace(old,new)
s=s.replace('if core.day>=29:return current','if core.day>=29:return current+due_fallbacks')
s=s.replace('        return result\n    def route_prepare','        return result+due_fallbacks\n    def route_prepare')
f.write_text(s,encoding='utf-8')
