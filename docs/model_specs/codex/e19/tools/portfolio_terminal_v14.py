"""No maintenance for a refresh that lies beyond the actual game horizon."""
from docs.model_specs.codex.e19.tools.portfolio_bounded_v14 import install as install_bounded


def install(core):
    install_bounded(core)
    services=core._services
    market_orders=core._market_orders
    rules=core.__call__.__func__.__globals__['CROPS']
    def terminal_services():
        offers=services()
        if core.day!=core.final_day:return offers
        result=[]
        for target,commands,priority,value,kind in offers:
            tile=core._tile(target)
            annual=tile.get('crop') in rules and not rules[tile['crop']]['ongoing']
            age=core.day-tile.get('planted_day',core.day)
            yield_water=annual and (rules[tile['crop']]['max_yield_day']+1)//2<=age<=rules[tile['crop']]['max_yield_day'] and tile.get('yield_units',0)<rules[tile['crop']]['max_yield']
            if kind=='BIOLOGICAL' and not yield_water:
                continue
            commands=[c for c in commands if c[0] not in {'FEED','CARE','FERTILIZE'} and (c[0]!='WATER' or yield_water)]
            if commands:result.append((target,commands,priority,value,kind))
        return result
    def terminal_orders():
        if core.day==core.final_day:core.unfed=0
        return market_orders()
    core._services=terminal_services
    core._market_orders=terminal_orders
