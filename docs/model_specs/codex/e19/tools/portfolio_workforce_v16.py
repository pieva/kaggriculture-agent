"""Invalidate impossible work and value animal care after feeding as well."""
from docs.model_specs.codex.e19.tools.portfolio_terminal_v14 import install as install_previous


def care_value(tile, day, final_day, rule, quote):
    if tile.get('cared_today'):
        return 0
    # Today's care is stored AFTER the coming refresh's production.
    production=next((d for d in range(day+2,final_day+1)
                     if d-tile['placed_day']>=rule['first_yield_day']
                     and (d-tile['placed_day']-rule['first_yield_day'])%rule['interval']==0),None)
    if production is None or tile.get('pending_care_bonus',0)>=rule['max_held']-1:
        return 0
    return quote(rule['product'],'SELL',1)


def impossible_harvest(job,tile):
    if not any(cmd[0]=='HARVEST' for cmd,pos in job['steps']):
        return False
    if not isinstance(tile,dict) or not (tile.get('kind')=='PLANT' or tile.get('animal')):
        return True
    return job['steps'][0][0][0]=='HARVEST' and tile.get('yield_units',0)<=0


def install(core):
    install_previous(core)
    acknowledge=core._acknowledge
    services=core._services
    namespace=core.__call__.__func__.__globals__
    def valid_acknowledge():
        acknowledge()
        for worker,job in list(core.active.items()):
            if impossible_harvest(job,core._tile(job['target'])):
                del core.active[worker]
                core.previous.pop(worker,None)
                core.metrics['portfolio_cancelled_impossible_harvest']+=1
    def valued_services():
        result=[]
        for target,commands,priority,value,kind in services():
            tile=core._tile(target)
            if ['CARE'] in commands and tile.get('animal'):
                rule=namespace['ANIMALS'][tile['animal']]
                benefit=care_value(tile,core.day,core.final_day,rule,core._quote)
                if kind=='BIOLOGICAL':
                    # Replace V14's per-interval care estimate, not add twice.
                    value-=core._quote(rule['product'],'SELL',1)/rule['interval']
                value=max(1,value)+benefit
            result.append((target,commands,priority,value,kind))
        return result
    core._acknowledge=valid_acknowledge
    core._services=valued_services
